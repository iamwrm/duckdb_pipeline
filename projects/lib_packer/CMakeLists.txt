cmake_minimum_required(VERSION 3.10)

# Set the project name
project(FetchGoogle)

# Find the libcurl package
find_package(CURL REQUIRED)

# Add the executable
add_executable(fetch_google src/main.c)

# Link the libcurl library
target_link_libraries(fetch_google CURL::libcurl)