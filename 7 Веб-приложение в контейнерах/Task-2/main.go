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