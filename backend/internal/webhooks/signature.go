package webhooks

import (
	"crypto/hmac"
	"crypto/sha256"
	"encoding/hex"
)

func Sign(payload []byte, secret string) string {
	h := hmac.New(sha256.New, []byte(secret))
	_, _ = h.Write(payload)
	return hex.EncodeToString(h.Sum(nil))
}

func Verify(payload []byte, signature, secret string) bool {
	if secret == "" || signature == "" {
		return false
	}
	expected := Sign(payload, secret)
	return hmac.Equal([]byte(expected), []byte(signature))
}
