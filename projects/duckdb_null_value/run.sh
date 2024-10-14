set -ueo pipefail

cd `dirname $0`

mkdir -p build
cd build
cmake .. -DCMAKE_EXPORT_COMPILE_COMMANDS=ON -G Ninja
ln -sf build/compile_commands.json ../
cmake --build . -j 4
./duckdb_null_value
