FROM debian:12

ENV DEBIAN_FRONTEND=noninteractive

RUN \
    apt-get update -y \
    && apt-get install -y locales \
    && echo "en_US.UTF-8 UTF-8" >> /etc/locale.gen \
    && locale-gen \
    && update-locale LANG=en_US.UTF-8

RUN \
    apt update -y \
    && apt install -y \
        ninja-build \
        cmake \
        zip \
        git \
        curl \
        wget \
        lsb-release \
        software-properties-common \
        gpg


WORKDIR /build
RUN \
    wget https://apt.llvm.org/llvm.sh \
    && chmod +x llvm.sh \
    && ./llvm.sh 19 \
    && apt-get update \
    && apt-get install clang-19 clang++-19 clangd-19

ENV CC=clang-19
ENV CXX=clang++-19

ENV LC_ALL=en_US.UTF-8
ENV LANG=en_US.UTF-8