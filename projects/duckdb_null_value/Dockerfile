FROM debian:12

ENV DEBIAN_FRONTEND=noninteractive


RUN \
    apt update -y \
    && apt install -y \
        clang \
        ninja-build \
        cmake \
        zip \
        git

RUN \
    apt-get install -y locales \
        libc-bin \
    && echo "en_US.UTF-8 UTF-8" >> /etc/locale.gen \
    && locale-gen \
    && update-locale LANG=en_US.UTF-8

ENV LC_ALL=en_US.UTF-8
ENV LANG=en_US.UTF-8