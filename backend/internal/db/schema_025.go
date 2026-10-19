package db

// Changing or resetting a password invalidates every token issued before it.
const Schema025 = `
ALTER TABLE users ADD COLUMN IF NOT EXISTS password_changed_at TIMESTAMPTZ;
`
