package main

import (
	"context"
	"fmt"
	"log"
	"time"

	"github.com/google/gopacket"
	"github.com/google/gopacket/layers"
	"github.com/yourusername/pcap-gcs-reader/pkg/pcapreader"
)

func main() {
	// Create a context with timeout
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Minute)
	defer cancel()

	// Create configuration
	config := pcapreader.Config{
		BucketName: "iamwrm1_cloudbuild",
		ObjectName: "export/data/200722_win_scale_examples_anon.pcapng",
		NumWorkers: 8,
		BufferSize: 1000,
	}

	// Create PCAP processor
	processor, err := pcapreader.NewPcapProcessor(ctx, config)
	if err != nil {
		log.Fatalf("Failed to create processor: %v", err)
	}
	defer processor.Close()

	// Packet analysis counters
	var (
		totalPackets int
		tcpPackets   int
		udpPackets   int
		httpPackets  int
	)

	// Process PCAP with detailed logging and analysis
	err = processor.ProcessPcap(
		ctx,
		func(packet gopacket.Packet) error {
			totalPackets++

			// Analyze packet layers
			if tcpLayer := packet.Layer(layers.LayerTypeTCP); tcpLayer != nil {
				tcpPackets++
				tcp, _ := tcpLayer.(*layers.TCP)

				// Check for HTTP ports
				if tcp.DstPort == 80 || tcp.DstPort == 443 {
					httpPackets++
				}
			}

			if udpLayer := packet.Layer(layers.LayerTypeUDP); udpLayer != nil {
				udpPackets++
			}

			// Optional: Print every 10,000th packet for large captures
			if totalPackets%10000 == 0 {
				fmt.Printf("Processed %d packets\n", totalPackets)
			}

			return nil
		},
	)

	// Check processing results
	if err != nil {
		log.Fatalf("PCAP processing failed: %v", err)
	}

	// Print final statistics
	fmt.Printf("Packet Analysis Complete:\n")
	fmt.Printf("Total Packets:    %d\n", totalPackets)
	fmt.Printf("TCP Packets:      %d\n", tcpPackets)
	fmt.Printf("UDP Packets:      %d\n", udpPackets)
	fmt.Printf("HTTP Packets:     %d\n", httpPackets)
}
