package pcapreader

import (
	"context"
	"io"
	"log"
	"os"
	"sync"

	"cloud.google.com/go/storage"
	"github.com/google/gopacket"
	"github.com/google/gopacket/pcap"
	"golang.org/x/sync/errgroup"
)

type PcapProcessor struct {
	client *storage.Client
	config Config
}

func NewPcapProcessor(ctx context.Context, config Config) (*PcapProcessor, error) {
	// Set default config if not fully specified
	if config.NumWorkers == 0 {
		config.NumWorkers = DefaultConfig().NumWorkers
	}
	if config.BufferSize == 0 {
		config.BufferSize = DefaultConfig().BufferSize
	}

	// Create GCS client
	client, err := storage.NewClient(ctx)
	if err != nil {
		return nil, err
	}

	return &PcapProcessor{
		client: client,
		config: config,
	}, nil
}

func (p *PcapProcessor) Close() {
	if p.client != nil {
		p.client.Close()
	}
}

func (p *PcapProcessor) ProcessPcap(
	ctx context.Context,
	processFn func(packet gopacket.Packet) error,
) error {
	// Open GCS object
	bucket := p.client.Bucket(p.config.BucketName)
	obj := bucket.Object(p.config.ObjectName)

	// Stream the object
	reader, err := obj.NewReader(ctx)
	if err != nil {
		return err
	}
	defer reader.Close()

	// Create a temporary file to work with gopacket/pcap
	tmpFile, err := os.CreateTemp("", "gcs-pcap-*.pcap")
	if err != nil {
		return err
	}
	defer os.Remove(tmpFile.Name())

	// Copy GCS stream to temp file
	if _, err := io.Copy(tmpFile, reader); err != nil {
		return err
	}
	tmpFile.Close()
	println("Copied to temp file")

	// Open PCAP file
	handle, err := pcap.OpenOffline(tmpFile.Name())
	if err != nil {
		return err
	}
	defer handle.Close()
	println("Opened PCAP file")

	// Parallel packet processing
	packetSource := gopacket.NewPacketSource(handle, handle.LinkType())

	// Use errgroup for concurrent processing with error handling
	g, ctx := errgroup.WithContext(ctx)

	// Buffered channel for packets
	packetChan := make(chan gopacket.Packet, p.config.BufferSize)

	// Packet reading goroutine
	g.Go(func() error {
		defer close(packetChan)
		for packet := range packetSource.Packets() {
			select {
			case packetChan <- packet:
			case <-ctx.Done():
				return ctx.Err()
			}
		}
		return nil
	})

	// Parallel processing goroutines
	var processingWg sync.WaitGroup
	processingWg.Add(p.config.NumWorkers)

	for i := 0; i < p.config.NumWorkers; i++ {
		go func() {
			defer processingWg.Done()
			for packet := range packetChan {
				if err := processFn(packet); err != nil {
					if p.config.DebugMode {
						log.Printf("Packet processing error: %v", err)
					}
				}
			}
		}()
	}

	// Wait for all processing to complete
	processingWg.Wait()

	return g.Wait()
}
