FROM golang:1.22-alpine AS builder
WORKDIR /app
COPY . .
RUN go build -o iam .

FROM alpine:latest
WORKDIR /root/
COPY --from=builder /app/iam .
EXPOSE 8082
CMD ["./iam"]
