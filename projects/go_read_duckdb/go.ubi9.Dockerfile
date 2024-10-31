# Build stage
FROM registry.access.redhat.com/ubi9:latest

# install go
RUN dnf install -y \
    golang gcc g++ \
    && rm -rf /var/cache/dnf

WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download


CMD ["/bin/bash"]
