#!/bin/bash

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "Docker is not installed. Please install Docker first."
    exit 1
fi

# Build the Docker image
echo "Building Docker image..."
docker build -t csv-reader-py . -f python.Dockerfile
docker build -t csv-reader-go . -f go.Dockerfile

# Run Python script in container to generate CSV
echo "Generating CSV file..."
docker run --rm -v "$(pwd):/app" csv-reader-py python3 create_data.py

# Run Go program in container
echo "Running Go program..."
docker run --rm -v "$(pwd):/app" csv-reader-go ./read_data 