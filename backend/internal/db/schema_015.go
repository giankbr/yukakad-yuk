package db

// The catalog scanner includes created_at, which was absent from older schemas.
const Schema015 = `ALTER TABLE templates ADD COLUMN IF NOT EXISTS created_at TIMESTAMPTZ NOT NULL DEFAULT NOW();`
