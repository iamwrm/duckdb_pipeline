cmake_minimum_required(VERSION 3.14)
project(zlib_example)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

include(FetchContent)

# Fetch zlib-ng
FetchContent_Declare(
    zlib-ng
    GIT_REPOSITORY https://github.com/zlib-ng/zlib-ng.git
    GIT_TAG 2.1.3
)
set(ZLIB_COMPAT ON CACHE BOOL "Compile with zlib compatible API")
set(ZLIB_ENABLE_TESTS OFF CACHE BOOL "Build test binaries")
FetchContent_MakeAvailable(zlib-ng)

# Fetch Catch2
FetchContent_Declare(
    Catch2
    GIT_REPOSITORY https://github.com/catchorg/Catch2.git
    GIT_TAG v3.4.0
)
FetchContent_MakeAvailable(Catch2)

# Add your source files
add_library(compression_lib
    src/compression.cpp
)
target_link_libraries(compression_lib PRIVATE zlib)
target_include_directories(compression_lib PUBLIC include)

# Add test executable
add_executable(compression_tests
    tests/compression_tests.cpp
)
target_link_libraries(compression_tests
    PRIVATE
    compression_lib
    Catch2::Catch2WithMain
)