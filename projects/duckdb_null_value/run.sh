set -ueo pipefail

cd `dirname $0`

mkdir -p build

# Check if clean argument is provided
if [[ "$@" == *"clean"* ]]; then
    echo "Cleaning build directory..."
    rm -rf build/*
fi

cd build

# if not found clang-19, run setup_clang19.sh
if ! command -v clang-19 &>/dev/null; then
    bash ./setup_clang19.sh
fi

export CC=clang-19
export CXX=clang++-19

cmake .. -DCMAKE_EXPORT_COMPILE_COMMANDS=ON -G Ninja

ln -sf build/compile_commands.json ../

cmake --build . -j 4

./duckdb_null_value

ctest -V

