#include "compression.hpp"
#include <zlib-ng.h>
#include <stdexcept>

std::vector<uint8_t> Compression::compress(const std::vector<uint8_t>& input) {
    if (input.empty()) return {};

    zng_stream stream;
    stream.zalloc = Z_NULL;
    stream.zfree = Z_NULL;
    stream.opaque = Z_NULL;

    if (zng_deflateInit(&stream, Z_DEFAULT_COMPRESSION) != Z_OK) {
        throw std::runtime_error("Failed to initialize deflate");
    }

    stream.next_in = const_cast<uint8_t*>(input.data());
    stream.avail_in = input.size();

    std::vector<uint8_t> output;
    const size_t CHUNK_SIZE = 32768;
    std::vector<uint8_t> chunk(CHUNK_SIZE);

    do {
        stream.next_out = chunk.data();
        stream.avail_out = CHUNK_SIZE;

        int ret = zng_deflate(&stream, Z_FINISH);
        if (ret == Z_STREAM_ERROR) {
            zng_deflateEnd(&stream);
            throw std::runtime_error("Compression failed");
        }

        int have = CHUNK_SIZE - stream.avail_out;
        output.insert(output.end(), chunk.begin(), chunk.begin() + have);
    } while (stream.avail_out == 0);

    zng_deflateEnd(&stream);
    return output;
}

std::vector<uint8_t> Compression::decompress(const std::vector<uint8_t>& input) {
    if (input.empty()) return {};

    zng_stream stream;
    stream.zalloc = Z_NULL;
    stream.zfree = Z_NULL;
    stream.opaque = Z_NULL;
    stream.avail_in = 0;
    stream.next_in = Z_NULL;

    if (zng_inflateInit(&stream) != Z_OK) {
        throw std::runtime_error("Failed to initialize inflate");
    }

    stream.next_in = const_cast<uint8_t*>(input.data());
    stream.avail_in = input.size();

    std::vector<uint8_t> output;
    const size_t CHUNK_SIZE = 32768;
    std::vector<uint8_t> chunk(CHUNK_SIZE);

    do {
        stream.next_out = chunk.data();
        stream.avail_out = CHUNK_SIZE;

        int ret = zng_inflate(&stream, Z_NO_FLUSH);
        if (ret == Z_STREAM_ERROR || ret == Z_NEED_DICT || ret == Z_DATA_ERROR || ret == Z_MEM_ERROR) {
            zng_inflateEnd(&stream);
            throw std::runtime_error("Decompression failed");
        }

        int have = CHUNK_SIZE - stream.avail_out;
        output.insert(output.end(), chunk.begin(), chunk.begin() + have);
    } while (stream.avail_out == 0);

    zng_inflateEnd(&stream);
    return output;
}

std::string Compression::compressString(const std::string& input) {
    std::vector<uint8_t> data(input.begin(), input.end());
    auto compressed = compress(data);
    return std::string(compressed.begin(), compressed.end());
}

std::string Compression::decompressString(const std::string& input) {
    std::vector<uint8_t> data(input.begin(), input.end());
    auto decompressed = decompress(data);
    return std::string(decompressed.begin(), decompressed.end());
}