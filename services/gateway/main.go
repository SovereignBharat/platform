package main

import (
	"fmt"
	"net/http"
)

func main() {
	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		fmt.Fprintf(w, "SovereignBharat API Gateway")
	})

	fmt.Println("Gateway running on :8081")
	http.ListenAndServe(":8081", nil)
}
