cd `dirname $0`

docker build -t uv_replace_pip .
docker run -it uv_replace_pip
