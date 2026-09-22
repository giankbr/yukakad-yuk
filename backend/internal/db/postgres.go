package db

import (
	"crypto/sha256"
	"database/sql"
	"encoding/hex"
	"fmt"

	_ "github.com/lib/pq"
)

func NewPostgres(url string) (*sql.DB, error) {
	db, err := sql.Open("postgres", url)
	if err != nil {
		return nil, err
	}
	if err := db.Ping(); err != nil {
		return nil, err
	}
	return db, nil
}

func MustMigrate(db *sql.DB, migrations []string) error {
	if _, err := db.Exec(`CREATE TABLE IF NOT EXISTS schema_migrations (
		version INTEGER PRIMARY KEY,
		checksum TEXT NOT NULL,
		applied_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
	)`); err != nil {
		return fmt.Errorf("create schema_migrations: %w", err)
	}
	for i, migrationSQL := range migrations {
		checksum := sha256.Sum256([]byte(migrationSQL))
		checksumText := hex.EncodeToString(checksum[:])
		var existing string
		err := db.QueryRow(`SELECT checksum FROM schema_migrations WHERE version = $1`, i+1).Scan(&existing)
		if err == nil {
			if existing != checksumText {
				return fmt.Errorf("migration %d checksum mismatch", i+1)
			}
			continue
		}
		if err != sql.ErrNoRows {
			return fmt.Errorf("read migration %d: %w", i+1, err)
		}
		tx, err := db.Begin()
		if err != nil {
			return fmt.Errorf("begin migration %d: %w", i+1, err)
		}
		if _, err := tx.Exec(migrationSQL); err != nil {
			_ = tx.Rollback()
			return fmt.Errorf("migrate step %d: %w", i+1, err)
		}
		if _, err := tx.Exec(`INSERT INTO schema_migrations(version, checksum) VALUES ($1, $2)`, i+1, checksumText); err != nil {
			_ = tx.Rollback()
			return fmt.Errorf("record migration %d: %w", i+1, err)
		}
		if err := tx.Commit(); err != nil {
			return fmt.Errorf("commit migration %d: %w", i+1, err)
		}
	}
	return nil
}
