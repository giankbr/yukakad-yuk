package db

const Schema003 = `
-- Required by guests.invitation_token generation (gen_random_bytes), which
-- has been broken since schema_001 introduced it: pgcrypto was never enabled.
CREATE EXTENSION IF NOT EXISTS pgcrypto;

ALTER TABLE users ADD COLUMN IF NOT EXISTS role TEXT NOT NULL DEFAULT 'user';

-- store.RSVP has carried a Message field since before this schema existed,
-- but no migration ever added the column, so every public RSVP submit
-- against Postgres has been failing with "column message does not exist".
ALTER TABLE rsvps ADD COLUMN IF NOT EXISTS message TEXT;

CREATE TABLE IF NOT EXISTS site_content (
    section TEXT PRIMARY KEY,
    data JSONB NOT NULL DEFAULT '{}'::jsonb,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS features (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    icon TEXT,
    sort_order INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS testimonials (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    role TEXT,
    quote TEXT NOT NULL,
    avatar_url TEXT,
    sort_order INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
`
