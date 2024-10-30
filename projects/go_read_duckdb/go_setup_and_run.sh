#!/bin/bash

# Initialize Go module if go.mod doesn't exist
if [ ! -f "go.mod" ]; then
    echo "Initializing Go module..."
    go mod init read_csv_project
fi

# Get Go dependencies
echo "Getting Go dependencies..."
go get github.com/marcboeker/go-duckdb
go mod tidy

# Run the Go program
echo "Running Go program..."
go run read_data.go 