#ifndef COMPRESSION_HPP
#define COMPRESSION_HPP

#include <string>
#include <vector>
#include <cstdint>

class Compression {
public:
    // Compress data using zlib-ng
    static std::vector<uint8_t> compress(const std::vector<uint8_t>& input);
    
    // Decompress data using zlib-ng
    static std::vector<uint8_t> decompress(const std::vector<uint8_t>& input);
    
    // Helper functions for string compression
    static std::string compressString(const std::string& input);
    static std::string decompressString(const std::string& input);
};

#endif // COMPRESSION_HPP