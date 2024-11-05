rm -rf build-1

mkdir build-1
cd build-1
patch -p1 < ../0001-Initial-commit-with-all-files.patch

bash run.sh