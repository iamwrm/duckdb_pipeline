cd `dirname $0`

mkdir -p build

# Check if clean flag is passed
if [ "$1" = "clean" ]; then
    echo "Cleaning build directory..."
    rm -rf build/*
fi



cd build

cargo build --release

cmake .. -G Ninja -DCMAKE_EXPORT_COMPILE_COMMANDS=ON

ln -s $(realpath compile_commands.json) ../compile_commands.json

cmake --build .

./main
