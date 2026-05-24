package main

import (
	"fmt"
	"net/http"
)

func main() {
	http.HandleFunc("/health", func(w http.ResponseWriter, r *http.Request) {
		fmt.Fprintf(w, "SovereignBharat Control Plane OK")
	})

	fmt.Println("Control plane running on :8080")
	http.ListenAndServe(":8080", nil)
}
