# CMakeLists.txt at the root of your_project/
cmake_minimum_required(VERSION 3.14)
project(MetaDataProject LANGUAGES CXX)

# Set C++ standard
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# Add the main executable
add_executable(metadata_example main.cpp MetaData.cpp)

# Include directories
target_include_directories(metadata_example PRIVATE ${CMAKE_CURRENT_SOURCE_DIR})

# Enable testing
enable_testing()

# Add subdirectory for tests
add_subdirectory(tests)