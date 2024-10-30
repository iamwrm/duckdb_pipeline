set -ueo pipefail 

sudo apt update
sudo apt install -y gcc cmake g++ ninja-build

cd `dirname $0`

mkdir build -p
# rm -rf build/*
cd build

cmake .. \
    -G Ninja \
    -DCMAKE_EXPORT_COMPILE_COMMANDS=ON \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_INSTALL_PREFIX=../install

ln -sf build/compile_commands.json ../

cmake --build .

./n_body_distances