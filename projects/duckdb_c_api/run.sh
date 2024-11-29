mkdir -p build

cmake \
    -S . \
    -B build \
    -G Ninja \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_EXPORT_COMPILE_COMMANDS=ON

cmake --build build

ln -sf build/compile_commands.json .

./build/duckdb_c_api

