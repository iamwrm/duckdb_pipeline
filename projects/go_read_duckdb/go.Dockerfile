# Build stage
FROM golang:1.23-bookworm
FROM registry.access.redhat.com/ubi9:latest

# install go
RUN dnf install -y \
    golang \
    && rm -rf /var/cache/dnf

WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download

COPY read_data.go .
# Build with static linking
RUN CGO_ENABLED=1 GOOS=linux go build -o read_data


CMD ["./read_data"]
