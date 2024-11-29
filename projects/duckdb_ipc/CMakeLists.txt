cmake_minimum_required(VERSION 3.14)
project(arrow_reader)

include(FetchContent)

# Set Arrow options
set(ARROW_BUILD_STATIC OFF)
set(ARROW_BUILD_SHARED ON)
set(ARROW_BUILD_TESTS OFF)
set(ARROW_BUILD_INTEGRATION OFF)
set(ARROW_BUILD_EXAMPLES OFF)
set(ARROW_BUILD_UTILITIES OFF)
set(ARROW_BUILD_BENCHMARKS OFF)
set(ARROW_WITH_BROTLI OFF)
set(ARROW_WITH_BZ2 OFF)
set(ARROW_WITH_LZ4 OFF)
set(ARROW_WITH_SNAPPY OFF)
set(ARROW_WITH_ZLIB OFF)
set(ARROW_WITH_ZSTD OFF)
set(ARROW_WITH_UTF8PROC OFF)
set(ARROW_WITH_RE2 OFF)

find_package(Arrow REQUIRED)


# Your executable
add_executable(arrow_reader cxx/main.cpp)

find_library(RUST_ARROW_LIB
    NAMES ret_arrow
    PATHS ${CMAKE_SOURCE_DIR}/ret_arrow/target/release
    REQUIRED
)

# Add include directories
target_include_directories(arrow_reader PRIVATE 
    ${arrow_SOURCE_DIR}/cpp/src
    ${arrow_BINARY_DIR}/cpp/src
)

target_link_libraries(arrow_reader PRIVATE 
    Arrow::arrow_shared
    ${RUST_ARROW_LIB}
)
set_target_properties(arrow_reader PROPERTIES
    BUILD_WITH_INSTALL_RPATH TRUE
    INSTALL_RPATH "${arrow_BINARY_DIR}/release:${CMAKE_SOURCE_DIR}/ret_arrow/target/release"
)

# Ensure C++17 is used
set_target_properties(arrow_reader PROPERTIES
    CXX_STANDARD 17
    CXX_STANDARD_REQUIRED ON
)