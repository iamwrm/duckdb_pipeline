// main.cpp
#include "MetaData.h"
#include <iostream>

int main() {
    MetaData metadata;

    // Adding key-value pairs
    if (metadata.AddKv("key1", "12312") != 0) {
        std::cerr << "Failed to add key1\n";
    }
    if (metadata.AddKv("key2", "12.3") != 0) {
        std::cerr << "Failed to add key2\n";
    }
    // Attempt to add a duplicate key
    if (metadata.AddKv("key1", "45678") != 0) {
        std::cerr << "Duplicate key1 not added\n";
    }

    // Output to CSV
    if (metadata.OutputToCsv("output.csv") != 0) {
        std::cerr << "Failed to write to CSV\n";
        return 1;
    }

    std::cout << "Metadata successfully written to output.csv\n";
    return 0;
}