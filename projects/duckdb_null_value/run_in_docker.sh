set -ueo pipefail

cd `dirname $0`

docker build -t duckdb_null_value .

docker run --rm \
    -v $(pwd):/build \
    duckdb_null_value \
    bash -c "bash /build/run.sh clean"

