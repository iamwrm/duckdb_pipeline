# Build stage
FROM golang:1.23


WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download

COPY read_data.go .
# Build with static linking
RUN CGO_ENABLED=1 GOOS=linux go build -o read_data


CMD ["/app/read_data"]
