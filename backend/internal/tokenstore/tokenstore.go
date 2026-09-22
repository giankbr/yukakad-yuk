package tokenstore

import (
	"context"
	"crypto/sha256"
	"encoding/hex"
	"sync"
	"time"

	"github.com/redis/go-redis/v9"
)

// Revoker tracks tokens that have been explicitly logged out before their
// natural JWT-style expiry.
type Revoker interface {
	Revoke(token string, exp time.Time) error
	IsRevoked(token string) (bool, error)
}

// MemoryRevoker is an in-process fallback used in tests and when Redis is
// not configured. State is lost on restart.
type MemoryRevoker struct {
	mu      sync.RWMutex
	revoked map[string]time.Time
}

func NewMemoryRevoker() *MemoryRevoker {
	return &MemoryRevoker{revoked: make(map[string]time.Time)}
}

func (m *MemoryRevoker) Revoke(token string, exp time.Time) error {
	m.mu.Lock()
	defer m.mu.Unlock()
	m.revoked[token] = exp
	return nil
}

func (m *MemoryRevoker) IsRevoked(token string) (bool, error) {
	m.mu.RLock()
	defer m.mu.RUnlock()
	_, ok := m.revoked[token]
	return ok, nil
}

// RedisRevoker persists revocations with a TTL matching the token's
// remaining lifetime, so entries self-clean and survive process restarts.
type RedisRevoker struct {
	client *redis.Client
}

func NewRedisRevoker(client *redis.Client) *RedisRevoker {
	return &RedisRevoker{client: client}
}

func hashToken(token string) string {
	sum := sha256.Sum256([]byte(token))
	return hex.EncodeToString(sum[:])
}

func (r *RedisRevoker) Revoke(token string, exp time.Time) error {
	ttl := time.Until(exp)
	if ttl <= 0 {
		ttl = time.Minute
	}
	return r.client.Set(context.Background(), "revoked:"+hashToken(token), "1", ttl).Err()
}

func (r *RedisRevoker) IsRevoked(token string) (bool, error) {
	n, err := r.client.Exists(context.Background(), "revoked:"+hashToken(token)).Result()
	if err != nil {
		return false, err
	}
	return n > 0, nil
}
