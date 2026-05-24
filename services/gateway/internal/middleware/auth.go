package middleware

import (
	"net/http"
	"strings"
)

// RequireBearerToken is a minimal gateway auth middleware.
// It only checks that a bearer token exists. Full verification should call IAM.
func RequireBearerToken(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		authorization := r.Header.Get("Authorization")
		if !strings.HasPrefix(authorization, "Bearer ") || strings.TrimPrefix(authorization, "Bearer ") == "" {
			w.Header().Set("Content-Type", "application/json")
			w.WriteHeader(http.StatusUnauthorized)
			_, _ = w.Write([]byte(`{"error":"missing bearer token"}`))
			return
		}

		next.ServeHTTP(w, r)
	})
}
