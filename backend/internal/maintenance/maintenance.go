package maintenance

import (
	"context"
	"database/sql"
	"log/slog"
	"time"
)

type Runner struct {
	db       *sql.DB
	interval time.Duration
}

func New(db *sql.DB, interval time.Duration) *Runner {
	if interval <= 0 {
		interval = 5 * time.Minute
	}
	return &Runner{db: db, interval: interval}
}

func (r *Runner) RunOnce(ctx context.Context) error {
	if _, err := r.db.ExecContext(ctx, `UPDATE subscriptions SET status='expired' WHERE status='active' AND ends_at IS NOT NULL AND ends_at <= NOW()`); err != nil {
		return err
	}
	if _, err := r.db.ExecContext(ctx, `UPDATE users SET plan_id='free' WHERE plan_id IS NOT NULL AND plan_id <> 'free' AND NOT EXISTS (SELECT 1 FROM subscriptions s WHERE s.user_id=users.id AND s.status='active' AND (s.ends_at IS NULL OR s.ends_at > NOW()))`); err != nil {
		return err
	}
	if _, err := r.db.ExecContext(ctx, `DELETE FROM password_reset_tokens WHERE used_at IS NOT NULL OR expires_at <= NOW()`); err != nil {
		return err
	}
	if _, err := r.db.ExecContext(ctx, `DELETE FROM user_entitlements WHERE expires_at IS NOT NULL AND expires_at <= NOW()`); err != nil {
		return err
	}
	return nil
}

func (r *Runner) Start(ctx context.Context) {
	ticker := time.NewTicker(r.interval)
	defer ticker.Stop()
	for {
		if err := r.RunOnce(ctx); err != nil && ctx.Err() == nil {
			slog.Error("maintenance run failed", "error", err)
		}
		select {
		case <-ctx.Done():
			return
		case <-ticker.C:
		}
	}
}
