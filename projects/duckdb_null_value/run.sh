set -ueo pipefail

cd `dirname $0`

BUILD_DIR=build

if [ -f /.dockerenv ]; then
    echo "Running in Docker";
    BUILD_DIR=build_in_docker
fi

mkdir -p ${BUILD_DIR}

# Check if clean argument is provided
if [[ "$@" == *"clean"* ]]; then
    echo "Cleaning build directory..."
    rm -rf ${BUILD_DIR}/*
fi

cd ${BUILD_DIR}

# check if clang-19 is installed
if ! command -v clang-19 &> /dev/null; then
    echo "clang-19 could not be found"
    exit 1
else
    echo "clang-19 found"
fi

export CC=clang-19
export CXX=clang++-19

cmake .. -DCMAKE_EXPORT_COMPILE_COMMANDS=ON -G Ninja

ln -sf ${BUILD_DIR}/compile_commands.json ../

cmake --build . -j 4

ctest -V

