package main

import (
	"encoding/json"
	"net/http"
)

type HealthResponse struct {
	Service string `json:"service"`
	Status  string `json:"status"`
}

func main() {
	http.HandleFunc("/health", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode(HealthResponse{Service: "iam", Status: "ok"})
	})

	http.ListenAndServe(":8082", nil)
}
