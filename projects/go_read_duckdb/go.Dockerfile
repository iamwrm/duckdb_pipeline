# Build stage
FROM golang:1.23-bookworm

# install go
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libc6-dev \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download

COPY read_data.go .
# Build with static linking
RUN CGO_ENABLED=1 GOOS=linux go build -o read_data


CMD ["./read_data"]
