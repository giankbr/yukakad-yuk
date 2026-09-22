package db

const Schema005 = `
-- Users: avatar + updated_at (fixes the existing UpdatePassword bug that already uses updated_at)
ALTER TABLE users ADD COLUMN IF NOT EXISTS avatar TEXT;
ALTER TABLE users ADD COLUMN IF NOT EXISTS updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW();

-- Invitations: track publish timestamp and last modification
ALTER TABLE invitations ADD COLUMN IF NOT EXISTS published_at TIMESTAMPTZ;
ALTER TABLE invitations ADD COLUMN IF NOT EXISTS updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW();

-- Couples: nicknames
ALTER TABLE couples ADD COLUMN IF NOT EXISTS groom_nickname TEXT;
ALTER TABLE couples ADD COLUMN IF NOT EXISTS bride_nickname TEXT;

-- Stories: date (e.g. "Pertama bertemu: 2019-06-01")
ALTER TABLE stories ADD COLUMN IF NOT EXISTS date TEXT;

-- Invitation settings: rich content fields
ALTER TABLE invitation_settings ADD COLUMN IF NOT EXISTS opening_text TEXT;
ALTER TABLE invitation_settings ADD COLUMN IF NOT EXISTS closing_text TEXT;
ALTER TABLE invitation_settings ADD COLUMN IF NOT EXISTS cover_image TEXT;
ALTER TABLE invitation_settings ADD COLUMN IF NOT EXISTS sections_config JSONB NOT NULL DEFAULT '[]'::jsonb;

-- Templates: data-driven section/theme configuration
ALTER TABLE templates ADD COLUMN IF NOT EXISTS config JSONB NOT NULL DEFAULT '{}'::jsonb;

-- Gift transactions (post-MVP foundation — no endpoints yet)
CREATE TABLE IF NOT EXISTS gift_transactions (
    id TEXT PRIMARY KEY DEFAULT gen_random_uuid()::text,
    invitation_id TEXT NOT NULL,
    guest_id TEXT,
    gateway TEXT NOT NULL DEFAULT 'manual',
    gateway_reference_id TEXT,
    amount NUMERIC(12,2) NOT NULL DEFAULT 0,
    status TEXT NOT NULL DEFAULT 'pending',
    sender_name TEXT,
    message TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_gift_transactions_inv_id ON gift_transactions(invitation_id);
CREATE INDEX IF NOT EXISTS idx_invitations_published ON invitations(published, published_at DESC);
`
