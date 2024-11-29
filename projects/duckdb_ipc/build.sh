cd ret_arrow
cargo build -r
cd ..

cmake -S . -B build -DCMAKE_EXPORT_COMPILE_COMMANDS=ON
cmake --build build
build/arrow_reader cpp
build/arrow_reader rust

