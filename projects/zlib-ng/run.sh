
mkdir build -p

# rm -rf build/*

cmake -S . -B build -G Ninja
cmake --build build

build/compression_tests
