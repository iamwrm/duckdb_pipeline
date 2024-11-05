#include <catch2/catch_test_macros.hpp>
#include "compression.hpp"

TEST_CASE("Compression of empty data", "[compression]") {
    std::vector<uint8_t> empty;
    auto compressed = Compression::compress(empty);
    REQUIRE(compressed.empty());
}

TEST_CASE("Decompression of empty data", "[compression]") {
    std::vector<uint8_t> empty;
    auto decompressed = Compression::decompress(empty);
    REQUIRE(decompressed.empty());
}

TEST_CASE("Compression and decompression of string data", "[compression]") {
    std::string original = "Hello, World! This is a test string for compression.";
    
    // Test string compression
    std::string compressed = Compression::compressString(original);
    REQUIRE(compressed.length() > 0);
    // REQUIRE(compressed.length() < original.length());
    
    // Test string decompression
    std::string decompressed = Compression::decompressString(compressed);
    REQUIRE(decompressed == original);
}

TEST_CASE("Compression and decompression of binary data", "[compression]") {
    std::vector<uint8_t> original(1000, 0xFF);
    
    // Test compression
    auto compressed = Compression::compress(original);
    REQUIRE(compressed.size() > 0);
    REQUIRE(compressed.size() < original.size());
    
    // Test decompression
    auto decompressed = Compression::decompress(compressed);
    REQUIRE(decompressed == original);
}

TEST_CASE("Compression of repeated data", "[compression]") {
    std::string repeatedData(1000, 'A');
    std::string compressed = Compression::compressString(repeatedData);
    
    REQUIRE(compressed.length() > 0);
    REQUIRE(compressed.length() < repeatedData.length());
    
    std::string decompressed = Compression::decompressString(compressed);
    REQUIRE(decompressed == repeatedData);
}