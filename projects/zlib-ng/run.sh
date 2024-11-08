
mkdir build -p

# rm -rf build/*

cmake -S . -B build -G Ninja -DCMAKE_EXPORT_COMPILE_COMMANDS=ON

ln -sf build/compile_commands.json compile_commands.json

cmake --build build

build/compression_tests
