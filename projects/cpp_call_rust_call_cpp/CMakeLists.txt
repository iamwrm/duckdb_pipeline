# CMakeLists.txt
cmake_minimum_required(VERSION 3.10)
project(CppRustFFI)

set(CMAKE_CXX_STANDARD 17)

# Add Rust library
add_library(cpp_state_inspector STATIC IMPORTED)
set_target_properties(cpp_state_inspector PROPERTIES
    IMPORTED_LOCATION ${CMAKE_SOURCE_DIR}/target/release/libcpp_state_inspector.a)

# Add executable
add_executable(main main.cpp)
target_link_libraries(main
    cpp_state_inspector
    dl
    pthread)