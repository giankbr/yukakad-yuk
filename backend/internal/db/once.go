package db

import (
	"database/sql"
	"fmt"
)

// One-off data changes keyed by name instead of by position in the numbered migration list, so they can't
// collide with schema files that are appended in parallel (theme batches). Each runs once per database, in a
// transaction, the first time a server with it starts.
type onceChange struct {
	key string
	sql string
}

// planVisibility is idempotent and runs every start: the public pricing page lists only active plans.
const planVisibility = `ALTER TABLE plans ADD COLUMN IF NOT EXISTS active BOOLEAN NOT NULL DEFAULT TRUE;`

var onceChanges = []onceChange{
	{
		// Four tiers (Free / Basic 49rb / Premium 129rb / Prioritas 249rb) with 6–12 months active.
		// "pro" is hidden from sale; existing Pro subscriptions keep their plan row and entitlements.
		key: "pricing-2026-10",
		sql: `
INSERT INTO plans (id, name, max_guests, max_team_members, has_watermark, custom_domain_allowed, payment_gateway_allowed, premium_templates_allowed, price, duration_days)
VALUES
  ('basic', 'Basic', 300, 3, FALSE, FALSE, FALSE, FALSE, 49000, 180),
  ('prioritas', 'Prioritas', 5000, 0, FALSE, TRUE, TRUE, TRUE, 249000, 365)
ON CONFLICT (id) DO NOTHING;
UPDATE plans SET name = 'Premium', max_guests = 1000, max_team_members = 10, has_watermark = FALSE, custom_domain_allowed = FALSE,
  payment_gateway_allowed = TRUE, premium_templates_allowed = TRUE, price = 129000, duration_days = 365
WHERE id = 'premium';
UPDATE plans SET active = FALSE WHERE id = 'pro';
`,
	},
}

func applyOnceChanges(db *sql.DB) error {
	// Partial migration sets (tests) may not have created the plans table yet.
	var plans sql.NullString
	if err := db.QueryRow(`SELECT to_regclass('plans')::text`).Scan(&plans); err != nil || !plans.Valid {
		return nil
	}
	if _, err := db.Exec(planVisibility); err != nil {
		return fmt.Errorf("plan visibility column: %w", err)
	}
	if _, err := db.Exec(`CREATE TABLE IF NOT EXISTS data_changes (key TEXT PRIMARY KEY, applied_at TIMESTAMPTZ NOT NULL DEFAULT NOW())`); err != nil {
		return fmt.Errorf("create data_changes: %w", err)
	}
	for _, change := range onceChanges {
		tx, err := db.Begin()
		if err != nil {
			return err
		}
		result, err := tx.Exec(`INSERT INTO data_changes (key) VALUES ($1) ON CONFLICT (key) DO NOTHING`, change.key)
		if err != nil {
			_ = tx.Rollback()
			return fmt.Errorf("data change %s: %w", change.key, err)
		}
		if inserted, _ := result.RowsAffected(); inserted == 0 {
			_ = tx.Rollback()
			continue
		}
		if _, err := tx.Exec(change.sql); err != nil {
			_ = tx.Rollback()
			return fmt.Errorf("data change %s: %w", change.key, err)
		}
		if err := tx.Commit(); err != nil {
			return fmt.Errorf("data change %s: %w", change.key, err)
		}
	}
	return nil
}
