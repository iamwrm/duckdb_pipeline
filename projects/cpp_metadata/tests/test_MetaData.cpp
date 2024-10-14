// tests/test_MetaData.cpp
#define CATCH_CONFIG_MAIN
#include <catch2/catch_test_macros.hpp>

#include <fstream>
#include <cstdio> // For std::remove

#include "MetaData.h"

TEST_CASE("MetaData AddKv Functionality", "[AddKv]") {
    MetaData metadata;

    SECTION("Add a single key-value pair") {
        int result = metadata.AddKv("key1", "value1");
        REQUIRE(result == 0);
    }

    SECTION("Add multiple unique key-value pairs") {
        REQUIRE(metadata.AddKv("key1", "value1") == 0);
        REQUIRE(metadata.AddKv("key2", "value2") == 0);
        REQUIRE(metadata.AddKv("key3", "value3") == 0);
    }

    SECTION("Attempt to add duplicate keys") {
        REQUIRE(metadata.AddKv("key1", "value1") == 0);
        REQUIRE(metadata.AddKv("key1", "value2") == -1); // Duplicate
    }
}

TEST_CASE("MetaData OutputToCsv Functionality", "[OutputToCsv]") {
    MetaData metadata;
    metadata.AddKv("key1", "12312");
    metadata.AddKv("key2", "12.3");
    metadata.AddKv("key3", "value with \"quotes\" and, commas");

    std::string test_csv = "test_output.csv";

    // Ensure the file does not exist before the test
    std::remove(test_csv.c_str());

    SECTION("Successfully output to CSV") {
        int result = metadata.OutputToCsv(test_csv);
        REQUIRE(result == 0);

        // Check if the file exists
        std::ifstream ifs(test_csv);
        REQUIRE(ifs.is_open());

        // Read and verify the contents
        std::string line;
        std::getline(ifs, line);
        REQUIRE(line == "key,value");

        std::getline(ifs, line);
        REQUIRE(line == "\"key1\",\"12312\"");

        std::getline(ifs, line);
        REQUIRE(line == "\"key2\",\"12.3\"");

        std::getline(ifs, line);
        REQUIRE(line == "\"key3\",\"value with \"\"quotes\"\" and, commas\"");

        ifs.close();
    }

    SECTION("Handle file write failure") {
        // Attempt to write to an invalid directory
        std::string invalid_path = "/invalid_path/output.csv";
        int result = metadata.OutputToCsv(invalid_path);
        REQUIRE(result == -1);
    }

    // Clean up the test CSV file after tests
    std::remove(test_csv.c_str());
}