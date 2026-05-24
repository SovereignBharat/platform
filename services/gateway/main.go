package main

import (
	"encoding/json"
	"fmt"
	"net/http"
	"os"

	"github.com/SovereignBharat/platform/services/gateway/internal/proxy"
)

type GatewayStatus struct {
	Service string            `json:"service"`
	Status  string            `json:"status"`
	Routes  map[string]string `json:"routes"`
}

func main() {
	routes := map[string]string{
		"/v1/auth/":        env("IAM_URL", "http://localhost:8082"),
		"/v1/clusters":     env("CONTROL_PLANE_URL", "http://localhost:8080"),
		"/v1/deployments":  env("CONTROL_PLANE_URL", "http://localhost:8080"),
		"/v1/chat/":        env("INFERENCE_URL", "http://localhost:8083"),
		"/v1/embeddings":   env("INFERENCE_URL", "http://localhost:8083"),
	}

	http.HandleFunc("/health", func(w http.ResponseWriter, r *http.Request) {
		writeJSON(w, GatewayStatus{Service: "gateway", Status: "ok", Routes: routes}, http.StatusOK)
	})

	for prefix, target := range routes {
		p, err := proxy.ReverseProxy(target)
		if err != nil {
			panic(err)
		}

		http.Handle(prefix, p)
	}

	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		writeJSON(w, map[string]string{"service": "SovereignBharat API Gateway"}, http.StatusOK)
	})

	fmt.Println("Gateway running on :8081")
	http.ListenAndServe(":8081", nil)
}

func env(key string, fallback string) string {
	value := os.Getenv(key)
	if value == "" {
		return fallback
	}
	return value
}

func writeJSON(w http.ResponseWriter, payload any, status int) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(status)
	json.NewEncoder(w).Encode(payload)
}
