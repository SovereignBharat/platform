package auth

import (
	"crypto/hmac"
	"crypto/sha256"
	"encoding/base64"
	"encoding/json"
	"errors"
	"strings"
	"time"
)

type Claims struct {
	Subject string   `json:"sub"`
	Issuer  string   `json:"iss"`
	Audience string  `json:"aud"`
	Roles   []string `json:"roles"`
	Expiry  int64    `json:"exp"`
}

func Sign(claims Claims, secret string) (string, error) {
	claims.Expiry = time.Now().Add(time.Hour).Unix()

	header := map[string]string{"alg": "HS256", "typ": "JWT"}
	headerBytes, err := json.Marshal(header)
	if err != nil {
		return "", err
	}

	claimsBytes, err := json.Marshal(claims)
	if err != nil {
		return "", err
	}

	encodedHeader := base64.RawURLEncoding.EncodeToString(headerBytes)
	encodedClaims := base64.RawURLEncoding.EncodeToString(claimsBytes)
	payload := encodedHeader + "." + encodedClaims

	signature := sign(payload, secret)
	return payload + "." + signature, nil
}

func Verify(token string, secret string) (*Claims, error) {
	parts := strings.Split(token, ".")
	if len(parts) != 3 {
		return nil, errors.New("invalid token")
	}

	payload := parts[0] + "." + parts[1]
	if !hmac.Equal([]byte(parts[2]), []byte(sign(payload, secret))) {
		return nil, errors.New("invalid signature")
	}

	claimsBytes, err := base64.RawURLEncoding.DecodeString(parts[1])
	if err != nil {
		return nil, err
	}

	var claims Claims
	if err := json.Unmarshal(claimsBytes, &claims); err != nil {
		return nil, err
	}

	if claims.Expiry < time.Now().Unix() {
		return nil, errors.New("token expired")
	}

	return &claims, nil
}

func sign(payload string, secret string) string {
	mac := hmac.New(sha256.New, []byte(secret))
	mac.Write([]byte(payload))
	return base64.RawURLEncoding.EncodeToString(mac.Sum(nil))
}
