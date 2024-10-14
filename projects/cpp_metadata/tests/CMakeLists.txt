# tests/CMakeLists.txt
# Add Catch2
include(FetchContent)
FetchContent_Declare(
    Catch2
    GIT_REPOSITORY https://github.com/catchorg/Catch2.git
    GIT_TAG v3.4.0
)
FetchContent_MakeAvailable(Catch2)

# Define the test executable
add_executable(runTests test_MetaData.cpp ../MetaData.cpp)

# Include directories
target_include_directories(runTests PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}/..)

# Link Catch2
target_link_libraries(runTests PRIVATE Catch2::Catch2WithMain)

# Discover and add tests
include(Catch)
catch_discover_tests(runTests)