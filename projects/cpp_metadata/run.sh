cd `dirname $0`

mkdir -p build
cd build
cmake .. -G Ninja -DCMAKE_EXPORT_COMPILE_COMMANDS=1
ln -sf build/compile_commands.json ../compile_commands.json

cmake --build .

./tests/runTests
# ./metadata_example
