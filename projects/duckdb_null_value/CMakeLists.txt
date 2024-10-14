cmake_minimum_required(VERSION 3.14)
project(duckdb_null_value)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED True)

include(FetchContent)

FetchContent_Declare(
    duckdb
    URL https://github.com/duckdb/duckdb/archive/refs/tags/v1.1.1.zip
    URL_HASH SHA256=cedf308dca577d2c5e44b34948529cb0ce932da27cd54ed611c926d49473c732
)

FetchContent_MakeAvailable(duckdb)

FetchContent_Declare(
    fmt
    URL https://github.com/fmtlib/fmt/archive/refs/tags/11.0.2.zip
)

FetchContent_MakeAvailable(fmt)

add_executable(duckdb_null_value main.cpp)

target_link_libraries(duckdb_null_value PRIVATE 
    duckdb 
    fmt
)

target_include_directories(duckdb_null_value PRIVATE 
    ${duckdb_SOURCE_DIR}/src/include
)

