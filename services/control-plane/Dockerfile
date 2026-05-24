FROM golang:1.22-alpine AS builder
WORKDIR /app
COPY . .
RUN go build -o control-plane .

FROM alpine:latest
WORKDIR /root/
COPY --from=builder /app/control-plane .
EXPOSE 8080
CMD ["./control-plane"]
