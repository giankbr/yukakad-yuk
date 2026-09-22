package auth

import (
	"crypto/hmac"
	"crypto/rand"
	"crypto/sha256"
	"encoding/hex"
	"fmt"
	"strings"
	"time"

	"golang.org/x/crypto/bcrypt"
)

func GenerateOpaqueToken() (string, error) {
	buf := make([]byte, 32)
	if _, err := rand.Read(buf); err != nil {
		return "", fmt.Errorf("generate token: %w", err)
	}
	return hex.EncodeToString(buf), nil
}

func HashOpaqueToken(token string) string {
	sum := sha256.Sum256([]byte(token))
	return hex.EncodeToString(sum[:])
}

type TokenClaims struct {
	UserID string
	Email  string
	Role   string
	Exp    int64
}

func HashPassword(password string) (string, error) {
	hash, err := bcrypt.GenerateFromPassword([]byte(password), bcrypt.DefaultCost)
	if err != nil {
		return "", fmt.Errorf("hash password: %w", err)
	}
	return string(hash), nil
}

func VerifyPassword(password, hash string) bool {
	return bcrypt.CompareHashAndPassword([]byte(hash), []byte(password)) == nil
}

func GenerateResetToken(userID, secret string) string {
	exp := time.Now().Add(30 * time.Minute).Unix()
	payload := fmt.Sprintf("reset:%s:%d", userID, exp)
	signature := hmac.New(sha256.New, []byte(secret))
	_, _ = signature.Write([]byte(payload))
	return fmt.Sprintf("%s.%s", payload, hex.EncodeToString(signature.Sum(nil)))
}

func ValidateResetToken(token, secret string) (string, bool) {
	parts := splitToken(token)
	if len(parts) != 2 {
		return "", false
	}
	signature := hmac.New(sha256.New, []byte(secret))
	_, _ = signature.Write([]byte(parts[0]))
	if !hmac.Equal([]byte(parts[1]), []byte(hex.EncodeToString(signature.Sum(nil)))) {
		return "", false
	}
	segments := strings.Split(parts[0], ":")
	if len(segments) != 3 || segments[0] != "reset" {
		return "", false
	}
	var exp int64
	if _, err := fmt.Sscanf(segments[2], "%d", &exp); err != nil || exp < time.Now().Unix() {
		return "", false
	}
	return segments[1], true
}

func GenerateToken(userID string, email string, role string, secret string) string {
	exp := time.Now().Add(24 * time.Hour).Unix()
	payload := fmt.Sprintf("%s:%s:%s:%d", userID, email, role, exp)
	signature := hmac.New(sha256.New, []byte(secret))
	_, _ = signature.Write([]byte(payload))
	return fmt.Sprintf("%s.%s", payload, hex.EncodeToString(signature.Sum(nil)))
}

func ValidateToken(token string, secret string) (TokenClaims, bool) {
	parts := splitToken(token)
	if len(parts) != 2 {
		return TokenClaims{}, false
	}
	payload, sig := parts[0], parts[1]
	signature := hmac.New(sha256.New, []byte(secret))
	_, _ = signature.Write([]byte(payload))
	expected := hex.EncodeToString(signature.Sum(nil))
	if !hmac.Equal([]byte(sig), []byte(expected)) {
		return TokenClaims{}, false
	}

	segments := strings.Split(payload, ":")
	if len(segments) != 4 {
		return TokenClaims{}, false
	}

	claims := TokenClaims{
		UserID: segments[0],
		Email:  segments[1],
		Role:   segments[2],
	}
	if _, err := fmt.Sscanf(segments[3], "%d", &claims.Exp); err != nil {
		return TokenClaims{}, false
	}
	if claims.Exp < time.Now().Unix() {
		return TokenClaims{}, false
	}
	return claims, true
}

func splitToken(token string) []string {
	if token == "" {
		return nil
	}
	separator := strings.LastIndexByte(token, '.')
	if separator <= 0 || separator == len(token)-1 {
		return nil
	}
	return []string{token[:separator], token[separator+1:]}
}
