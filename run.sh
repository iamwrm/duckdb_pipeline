set -ueo pipefail 

sudo apt install gcc cmake g++ ninja-build

mkdir build -p
# rm -rf build/*
cd build

cmake .. \
    -G Ninja \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_INSTALL_PREFIX=../install

cmake --build .

./n_body_distances