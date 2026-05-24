FROM golang:1.22-alpine AS builder
WORKDIR /app
COPY . .
RUN go build -o gateway .

FROM alpine:latest
WORKDIR /root/
COPY --from=builder /app/gateway .
EXPOSE 8081
CMD ["./gateway"]
