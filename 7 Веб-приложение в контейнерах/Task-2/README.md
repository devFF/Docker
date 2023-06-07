Итак, пришло время вернуться к докерфайлу.

Go завернем в контейнер простейшую программу на Go 🙂

Вам нужно создать папку, в которой завести 3 файла — **Dockerfile**, **go.mod** и **main.go**.

Содержимое файла **go.mod**:
```go
module main

go 1.19
```

Содержимое файла **main.go**:
```go
package main

import "net/http"

func DockerTask(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "text/html")
	w.Write([]byte("<h1>Let's Go write a multi-stage build</h1>"))
}

func main() {
	http.HandleFunc("/", DockerTask)
	http.ListenAndServe(":5000", nil)
}
```

И, наконец, содержимое докерфайла:
```Dockerfile
FROM golang:1.19 AS APP
WORKDIR /app
COPY go.mod go.mod
COPY main.go main.go
RUN go build

FROM ubuntu:22.04
WORKDIR /app
EXPOSE 5000
COPY ...
ENTRYPOINT ["/app/main"]
```

Как вы видите, в докерфайле чего-то не хватает. 

Дополните инструкцию COPY так, чтобы при поднятии контейнера всё работало.