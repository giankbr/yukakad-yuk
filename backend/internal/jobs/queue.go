package jobs

import (
	"context"
	"encoding/json"
	"fmt"
	"github.com/redis/go-redis/v9"
	"time"
)

type Job struct {
	ID        string          `json:"id"`
	Type      string          `json:"type"`
	Payload   json.RawMessage `json:"payload"`
	Attempts  int             `json:"attempts"`
	CreatedAt time.Time       `json:"created_at"`
}

type Queue struct {
	client *redis.Client
	key    string
}

func NewQueue(client *redis.Client, key string) *Queue { return &Queue{client: client, key: key} }

func (q *Queue) Enqueue(ctx context.Context, job Job) error {
	if job.Type == "" {
		return fmt.Errorf("job type is required")
	}
	if job.CreatedAt.IsZero() {
		job.CreatedAt = time.Now().UTC()
	}
	data, err := json.Marshal(job)
	if err != nil {
		return err
	}
	return q.client.RPush(ctx, q.key, data).Err()
}

func (q *Queue) Dequeue(ctx context.Context, timeout time.Duration) (Job, error) {
	result, err := q.client.BLPop(ctx, timeout, q.key).Result()
	if err != nil {
		return Job{}, err
	}
	var job Job
	if err := json.Unmarshal([]byte(result[1]), &job); err != nil {
		return Job{}, err
	}
	return job, nil
}

type Handler func(context.Context, Job) error

func (q *Queue) Run(ctx context.Context, handlers map[string]Handler) {
	for {
		job, err := q.Dequeue(ctx, 30*time.Second)
		if err != nil {
			if ctx.Err() != nil {
				return
			}
			continue
		}
		handler, ok := handlers[job.Type]
		if !ok {
			continue
		}
		if err := handler(ctx, job); err != nil {
			job.Attempts++
			if job.Attempts < 3 {
				_ = q.Enqueue(ctx, job)
			}
		}
	}
}
