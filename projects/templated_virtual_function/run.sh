cd `dirname $0`

mkdir -p build
cd build

g++ -std=c++20 -Wall -Wextra -pedantic -o main.out ../main.cpp

./main.out


