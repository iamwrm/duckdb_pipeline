cd `dirname $0`

mkdir -p build
cd build
cmake .. -G Ninja -DCMAKE_EXPORT_COMPILE_COMMANDS=ON

ln -s $(realpath compile_commands.json) ../compile_commands.json

cmake --build .

./main
