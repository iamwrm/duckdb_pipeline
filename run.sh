sudo apt install gcc cmake g++ ninja-build

mkdir build
rm -rf build/*
cd build

cmake .. \
    -G Ninja \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_INSTALL_PREFIX=../install

cmake --build .

./n_body_distances