package pcapreader

type Config struct {
	BucketName string
	ObjectName string
	NumWorkers int
	BufferSize int
	DebugMode  bool
}

func DefaultConfig() Config {
	return Config{
		NumWorkers: 8,
		BufferSize: 1000,
		DebugMode:  false,
	}
}
