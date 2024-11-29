cmake_minimum_required(VERSION 3.20)
project(duckdb_c_api)

cmake_policy(SET CMP0135 NEW)

include(FetchContent)

FetchContent_Declare(
    fmt
    URL https://github.com/fmtlib/fmt/archive/refs/tags/11.0.2.zip
    URL_HASH SHA256=7aa4b58e361de10b8e5d7b6c18aebd98be1886ab3efe43e368527a75cd504ae4
)
FetchContent_MakeAvailable(fmt)

FetchContent_Declare(
  Catch2
  GIT_REPOSITORY https://github.com/catchorg/Catch2.git
  GIT_TAG        v3.4.0
)
FetchContent_MakeAvailable(Catch2)


if(CMAKE_SYSTEM_PROCESSOR STREQUAL "x86_64")
    FetchContent_Declare(
        duckdb
        URL https://github.com/duckdb/duckdb/releases/download/v1.1.3/libduckdb-linux-amd64.zip
        URL_HASH SHA256=8080808080808080808080808080808080808080808080808080808080808080
    )
elseif(CMAKE_SYSTEM_PROCESSOR STREQUAL "aarch64")
    FetchContent_Declare(
        duckdb
        URL https://github.com/duckdb/duckdb/releases/download/v1.1.3/libduckdb-linux-aarch64.zip
        URL_HASH SHA256=9069db3627456ab8b14399a73cd8d450c7863b1bc93b2b197d157ea18bad7801
    )
else()
    message(FATAL_ERROR "Unsupported architecture: ${CMAKE_SYSTEM_PROCESSOR}")
endif()

FetchContent_MakeAvailable(duckdb)
find_library(DUCKDB_LIBRARY
    NAMES duckdb
    PATHS ${duckdb_SOURCE_DIR}
    NO_DEFAULT_PATH
    REQUIRED
)
add_library(duckdb::duckdb SHARED IMPORTED)
set_target_properties(duckdb::duckdb PROPERTIES
    IMPORTED_LOCATION ${DUCKDB_LIBRARY}
    INTERFACE_INCLUDE_DIRECTORIES ${duckdb_SOURCE_DIR}
)


add_executable(duckdb_c_api main.cpp)

target_link_libraries(duckdb_c_api 
    PRIVATE 
        fmt::fmt
        Catch2::Catch2WithMain
    PUBLIC
        duckdb::duckdb
)
