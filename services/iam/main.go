package main

import (
	"encoding/json"
	"net/http"
	"os"
	"strings"

	"github.com/SovereignBharat/platform/services/iam/internal/auth"
)

type HealthResponse struct {
	Service string `json:"service"`
	Status  string `json:"status"`
}

type TokenRequest struct {
	Subject string   `json:"subject"`
	Roles   []string `json:"roles"`
}

type TokenResponse struct {
	Token string `json:"token"`
}

type VerifyResponse struct {
	Valid  bool         `json:"valid"`
	Claims *auth.Claims `json:"claims,omitempty"`
	Error  string       `json:"error,omitempty"`
}

func main() {
	secret := os.Getenv("JWT_SECRET")
	if secret == "" {
		secret = "dev-sovereignbharat-secret"
	}

	http.HandleFunc("/health", func(w http.ResponseWriter, r *http.Request) {
		writeJSON(w, HealthResponse{Service: "iam", Status: "ok"}, http.StatusOK)
	})

	http.HandleFunc("/v1/auth/token", func(w http.ResponseWriter, r *http.Request) {
		if r.Method != http.MethodPost {
			writeJSON(w, map[string]string{"error": "method not allowed"}, http.StatusMethodNotAllowed)
			return
		}

		var req TokenRequest
		if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
			writeJSON(w, map[string]string{"error": "invalid request"}, http.StatusBadRequest)
			return
		}

		if req.Subject == "" {
			writeJSON(w, map[string]string{"error": "subject is required"}, http.StatusBadRequest)
			return
		}

		token, err := auth.Sign(auth.Claims{
			Subject:  req.Subject,
			Issuer:   "sovereignbharat",
			Audience: "sovereignbharat-platform",
			Roles:    req.Roles,
		}, secret)
		if err != nil {
			writeJSON(w, map[string]string{"error": "token generation failed"}, http.StatusInternalServerError)
			return
		}

		writeJSON(w, TokenResponse{Token: token}, http.StatusOK)
	})

	http.HandleFunc("/v1/auth/verify", func(w http.ResponseWriter, r *http.Request) {
		token := strings.TrimPrefix(r.Header.Get("Authorization"), "Bearer ")
		if token == "" {
			writeJSON(w, VerifyResponse{Valid: false, Error: "missing bearer token"}, http.StatusUnauthorized)
			return
		}

		claims, err := auth.Verify(token, secret)
		if err != nil {
			writeJSON(w, VerifyResponse{Valid: false, Error: err.Error()}, http.StatusUnauthorized)
			return
		}

		writeJSON(w, VerifyResponse{Valid: true, Claims: claims}, http.StatusOK)
	})

	http.ListenAndServe(":8082", nil)
}

func writeJSON(w http.ResponseWriter, payload any, status int) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(status)
	json.NewEncoder(w).Encode(payload)
}
