#!/bin/bash
set -ueo pipefail

cd `dirname $0`

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "Docker is not installed. Please install Docker first."
    exit 1
fi

echo "Create CSV file..."

# Use buildx
export DOCKER_BUILDKIT=1

docker build -t csv-reader-py . -f python.Dockerfile
echo "Generating CSV file..."
docker run --rm -v "$(pwd):/app" csv-reader-py python3 create_data.py

echo "Run golang in ubi9"
DOCKER_NAME=csv-reader-go-ubi9
docker build -t $DOCKER_NAME . -f go.ubi9.Dockerfile
docker run --rm -v "$(pwd):/data/" -w /data $DOCKER_NAME \
    /bin/bash -c "CGO_ENABLED=1 GOOS=linux go build -o read_data && ./read_data"

echo "Run golang in golang"
DOCKER_NAME=csv-reader-go-golang
docker build -t $DOCKER_NAME . -f go.golang.Dockerfile
docker run --rm -v "$(pwd):/data/" -w /data $DOCKER_NAME \
    /bin/bash -c "CGO_ENABLED=1 GOOS=linux go build -o read_data && ./read_data"
