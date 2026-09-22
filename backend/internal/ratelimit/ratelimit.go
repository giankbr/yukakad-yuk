package ratelimit

import (
	"context"
	"sync"
	"time"

	"github.com/redis/go-redis/v9"
)

type Limiter interface {
	Allow(key string, limit int, window time.Duration) (bool, error)
}

type MemoryLimiter struct {
	mu      sync.Mutex
	buckets map[string]*bucket
}

type bucket struct {
	count   int
	resetAt time.Time
}

func NewMemoryLimiter() *MemoryLimiter {
	return &MemoryLimiter{buckets: make(map[string]*bucket)}
}

func (m *MemoryLimiter) Allow(key string, limit int, window time.Duration) (bool, error) {
	m.mu.Lock()
	defer m.mu.Unlock()
	now := time.Now()
	b, ok := m.buckets[key]
	if !ok || now.After(b.resetAt) {
		b = &bucket{count: 0, resetAt: now.Add(window)}
		m.buckets[key] = b
	}
	b.count++
	return b.count <= limit, nil
}

// RedisLimiter is a fixed-window limiter backed by INCR+EXPIRE, shared
// across backend instances.
type RedisLimiter struct {
	client *redis.Client
}

func NewRedisLimiter(client *redis.Client) *RedisLimiter {
	return &RedisLimiter{client: client}
}

func (r *RedisLimiter) Allow(key string, limit int, window time.Duration) (bool, error) {
	ctx := context.Background()
	fullKey := "ratelimit:" + key
	count, err := r.client.Incr(ctx, fullKey).Result()
	if err != nil {
		return false, err
	}
	if count == 1 {
		r.client.Expire(ctx, fullKey, window)
	}
	return count <= int64(limit), nil
}
