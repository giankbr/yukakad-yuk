package session

import (
	"context"
	"crypto/rand"
	"crypto/sha256"
	"encoding/base64"
	"encoding/hex"
	"encoding/json"
	"fmt"
	"strings"
	"time"

	"github.com/redis/go-redis/v9"
)

type Claims struct {
	UserID string
	Email  string
	Role   string
	Exp    int64
}

type Manager interface {
	Create(userID, email, role string, ttl time.Duration) (string, Claims, error)
	Get(token string) (Claims, bool, error)
	Revoke(token string) error
}

type RedisManager struct{ client *redis.Client }

func NewRedisManager(client *redis.Client) *RedisManager { return &RedisManager{client: client} }

func (m *RedisManager) Create(userID, email, role string, ttl time.Duration) (string, Claims, error) {
	if ttl <= 0 {
		return "", Claims{}, fmt.Errorf("session ttl must be positive")
	}
	raw := make([]byte, 32)
	if _, err := rand.Read(raw); err != nil {
		return "", Claims{}, fmt.Errorf("generate session token: %w", err)
	}
	token := base64.RawURLEncoding.EncodeToString(raw)
	claims := Claims{UserID: userID, Email: email, Role: role, Exp: time.Now().Add(ttl).Unix()}
	payload, err := json.Marshal(claims)
	if err != nil {
		return "", Claims{}, fmt.Errorf("encode session: %w", err)
	}
	if err := m.client.Set(context.Background(), key(token), payload, ttl).Err(); err != nil {
		return "", Claims{}, fmt.Errorf("store session: %w", err)
	}
	return token, claims, nil
}

func (m *RedisManager) Get(token string) (Claims, bool, error) {
	if strings.TrimSpace(token) == "" {
		return Claims{}, false, nil
	}
	payload, err := m.client.Get(context.Background(), key(token)).Bytes()
	if err == redis.Nil {
		return Claims{}, false, nil
	}
	if err != nil {
		return Claims{}, false, fmt.Errorf("read session: %w", err)
	}
	var claims Claims
	if err := json.Unmarshal(payload, &claims); err != nil {
		return Claims{}, false, fmt.Errorf("decode session: %w", err)
	}
	if claims.Exp <= time.Now().Unix() {
		return Claims{}, false, nil
	}
	return claims, true, nil
}

func (m *RedisManager) Revoke(token string) error {
	if strings.TrimSpace(token) == "" {
		return nil
	}
	return m.client.Del(context.Background(), key(token)).Err()
}

func key(token string) string {
	sum := sha256.Sum256([]byte(token))
	return "session:" + hex.EncodeToString(sum[:])
}
