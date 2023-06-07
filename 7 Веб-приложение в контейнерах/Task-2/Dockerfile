FROM golang:1.19 AS APP
WORKDIR /app
COPY go.mod go.mod
COPY main.go main.go
RUN go build

FROM ubuntu:22.04
WORKDIR /app
EXPOSE 5000
COPY --from=APP /app/main main
ENTRYPOINT ["/app/main"]