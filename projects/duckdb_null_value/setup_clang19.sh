

echo "Setting up clang-19..."

export DEBIAN_FRONTEND=noninteractive

sudo apt-get update
sudo apt-get install git cmake ccache python3 ninja-build nasm yasm gawk lsb-release wget software-properties-common gnupg

sudo bash -c "$(wget -O - https://apt.llvm.org/llvm.sh)"


sudo apt-get install clang-19 clangd-19

