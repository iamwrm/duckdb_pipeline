cmake_minimum_required(VERSION 3.14)  # FetchContent is available in 3.14+

project(NBodySimulation VERSION 1.0)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED True)

include(FetchContent)

FetchContent_Declare(
  eigen
  GIT_REPOSITORY https://gitlab.com/libeigen/eigen.git
  GIT_TAG 3.4.0
)

FetchContent_MakeAvailable(eigen)

# Add the executable
add_executable(nbody_sim nbody.cpp)

# Link Eigen to our target
target_link_libraries(nbody_sim Eigen3::Eigen)

# Set compiler flags
if(MSVC)
    target_compile_options(nbody_sim PRIVATE /W4)
else()
    target_compile_options(nbody_sim PRIVATE -Wall -Wextra -pedantic)
endif()