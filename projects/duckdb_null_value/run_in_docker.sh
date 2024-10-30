cd `dirname $0`


docker build -t duckdb_null_value .

docker run -it --rm \
    -v $(pwd):/build \
    duckdb_null_value \
    bash -c "bash /build/run.sh"

