#!/bin/bash

if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <output_directory> <script_to_trace>"
    exit 1
fi

OUTPUT_DIR="$1"
SCRIPT_TO_TRACE="$2"

# Create output directory if it doesn't exist
mkdir -p "$OUTPUT_DIR"

# Run strace and capture all system calls, focusing on file operations
strace -f -e trace=open,openat,stat,access,execve -o strace_output.txt bash "$SCRIPT_TO_TRACE"

# Extract unique file paths from strace output
cat strace_output.txt | grep -E '".*"' | sed -n 's/.*"\([^"]*\)".*/\1/p' | sort -u | while read -r file; do
    # Skip if file doesn't exist or is a directory
    if [ ! -f "$file" ]; then
        continue
    fi

    # Skip if it's /proc
    if [[ "$file" == /proc/* ]]; then
        continue
    fi
    
    # Create directory structure in output directory
    dir_path=$(dirname "$file")
    mkdir -p "$OUTPUT_DIR/$dir_path"
    
    # Copy file preserving path structure
    echo "Copying $file to $OUTPUT_DIR/$file"
    cp -p "$file" "$OUTPUT_DIR/$file"
done

# Cleanup
# rm strace_output.txt

echo "\nFile copying complete. Check $OUTPUT_DIR for copied files."
