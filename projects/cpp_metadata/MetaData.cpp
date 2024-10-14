#include "MetaData.h"
#include <fstream>
#include <algorithm>

// Adds a key-value pair. Ensures that keys are unique.
int MetaData::AddKv(const std::string& key, const std::string& value) {
    // Check if key already exists
    auto it = std::find_if(data_.begin(), data_.end(),
                           [&key](const std::pair<std::string, std::string>& pair) {
                               return pair.first == key;
                           });
    if (it != data_.end()) {
        // Key already exists
        return -1;
    }

    data_.emplace_back(key, value);
    return 0;
}

// Helper function to escape double quotes in CSV
std::string EscapeCsv(const std::string& field) {
    std::string escaped = "\"";
    for (char c : field) {
        if (c == '"') {
            escaped += "\"\""; // Escape double quotes
        } else {
            escaped += c;
        }
    }
    escaped += "\"";
    return escaped;
}

int MetaData::OutputToCsv(const std::string& path) const {
    std::ofstream ofs(path);
    if (!ofs.is_open()) {
        return -1;
    }

    // Write header
    ofs << "key,value\n";

    // Write data
    for (const auto& pair : data_) {
        ofs << EscapeCsv(pair.first) << "," << EscapeCsv(pair.second) << "\n";
    }

    ofs.close();
    if (ofs.fail()) {
        return -1;
    }

    return 0;
}