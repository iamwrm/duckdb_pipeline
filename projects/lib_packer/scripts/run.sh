set -ueo pipefail

cd `dirname $0`/..

rm -rf build
mkdir -p build

cmake -S . -B build \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_EXPORT_COMPILE_COMMANDS=ON \
    -DCMAKE_C_COMPILER=gcc \
    -DCMAKE_CXX_COMPILER=g++

ln -sf build/compile_commands.json .

cmake --build build

./build/fetch_google