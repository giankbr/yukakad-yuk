package db

// Buku buwuh (gift ledger), guest photo uploads, private per-invitation data (doorprize)
// and the purpose of an online envelope (e.g. a crowdfunded wishlist item).
const Schema021 = `
CREATE TABLE IF NOT EXISTS gift_ledger (
    id TEXT PRIMARY KEY DEFAULT gen_random_uuid()::text,
    invitation_id TEXT NOT NULL,
    guest_id TEXT,
    name TEXT NOT NULL,
    kind TEXT NOT NULL DEFAULT 'cash',
    amount NUMERIC(14,2) NOT NULL DEFAULT 0,
    item TEXT,
    note TEXT,
    recorded_by TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_gift_ledger_invitation ON gift_ledger(invitation_id, created_at DESC);

CREATE TABLE IF NOT EXISTS guest_photos (
    id TEXT PRIMARY KEY DEFAULT gen_random_uuid()::text,
    invitation_id TEXT NOT NULL,
    guest_id TEXT,
    uploader_name TEXT,
    url TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'approved',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_guest_photos_invitation ON guest_photos(invitation_id, created_at DESC);

CREATE TABLE IF NOT EXISTS invitation_private (
    invitation_id TEXT NOT NULL,
    key TEXT NOT NULL,
    data JSONB NOT NULL DEFAULT '{}'::jsonb,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (invitation_id, key)
);

ALTER TABLE gift_transactions ADD COLUMN IF NOT EXISTS purpose TEXT;
`
