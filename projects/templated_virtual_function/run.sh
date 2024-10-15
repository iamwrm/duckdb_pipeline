#!/bin/bash
set -ueo pipefail

cd `dirname $0`

mkdir -p build
cd build

# Turn on all sanitizers
export ASAN_OPTIONS=detect_leaks=1
export UBSAN_OPTIONS=print_stacktrace=1
cmake .. -DCMAKE_EXPORT_COMPILE_COMMANDS=ON -DCMAKE_CXX_FLAGS="-fsanitize=address,undefined,leak -fno-omit-frame-pointer"


ln -sf build/compile_commands.json ../compile_commands.json

cmake --build .

./templated_virtual_function



