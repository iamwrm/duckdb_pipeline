cmake_minimum_required(VERSION 3.25)
project(NBodyDistances)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

include(ExternalProject)

# DuckDB
ExternalProject_Add(
    duckdb_ext
    GIT_REPOSITORY https://github.com/duckdb/duckdb.git
    GIT_TAG v0.7.1
    CMAKE_ARGS -DCMAKE_INSTALL_PREFIX=${CMAKE_BINARY_DIR}/duckdb
    BUILD_BYPRODUCTS ${CMAKE_BINARY_DIR}/duckdb/lib/libduckdb_static.a
)

# Eigen
ExternalProject_Add(
    eigen_ext
    GIT_REPOSITORY https://gitlab.com/libeigen/eigen.git
    GIT_TAG 3.4.0
    CMAKE_ARGS -DCMAKE_INSTALL_PREFIX=${CMAKE_BINARY_DIR}/eigen
    BUILD_BYPRODUCTS ${CMAKE_BINARY_DIR}/eigen/include/eigen3
)

# Add the executable
add_executable(n_body_distances main.cpp)

# Include directories
target_include_directories(n_body_distances PRIVATE 
    ${CMAKE_BINARY_DIR}/duckdb/include
    ${CMAKE_BINARY_DIR}/eigen/include/eigen3
)

# Link libraries
target_link_libraries(n_body_distances PRIVATE 
    ${CMAKE_BINARY_DIR}/duckdb/lib/libduckdb_static.a
)

# Add dependencies
add_dependencies(n_body_distances duckdb_ext eigen_ext)