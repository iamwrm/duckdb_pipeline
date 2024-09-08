cmake_minimum_required(VERSION 3.10)

project(NBodySimulation VERSION 1.0)

set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# Find Eigen library
find_package(Eigen3 3.3 REQUIRED NO_MODULE)

# Add the executable
add_executable(nbody_sim nbody.cpp)

# Link Eigen to our target
target_link_libraries(nbody_sim Eigen3::Eigen)

# Include directories
target_include_directories(nbody_sim PRIVATE ${EIGEN3_INCLUDE_DIR})

# Set compiler flags
if(MSVC)
    target_compile_options(nbody_sim PRIVATE /W4)
else()
    target_compile_options(nbody_sim PRIVATE -Wall -Wextra -pedantic)
endif()