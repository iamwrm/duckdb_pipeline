#ifndef METADATA_H
#define METADATA_H

#include <string>
#include <vector>
#include <utility>

class MetaData {
public:
    // Adds a key-value pair. Returns 0 on success, -1 if key already exists.
    int AddKv(const std::string& key, const std::string& value);

    // Outputs the metadata to a CSV file at the given path.
    // Returns 0 on success, -1 on failure.
    int OutputToCsv(const std::string& path) const;

private:
    // Stores key-value pairs. Using vector to maintain insertion order.
    std::vector<std::pair<std::string, std::string>> data_;
};

#endif // METADATA_H