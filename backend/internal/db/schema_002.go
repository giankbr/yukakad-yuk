package db

const Schema002 = `
ALTER TABLE guests ADD COLUMN IF NOT EXISTS checked_in_by TEXT;
ALTER TABLE gifts ADD COLUMN IF NOT EXISTS qris_image_url TEXT;
ALTER TABLE broadcast_logs ADD COLUMN IF NOT EXISTS sent_at TIMESTAMPTZ;
ALTER TABLE users ADD COLUMN IF NOT EXISTS plan_id TEXT;
ALTER TABLE media ADD COLUMN IF NOT EXISTS user_id TEXT;
ALTER TABLE events ADD COLUMN IF NOT EXISTS maps_url TEXT;
ALTER TABLE events ADD COLUMN IF NOT EXISTS latitude DOUBLE PRECISION;
ALTER TABLE events ADD COLUMN IF NOT EXISTS longitude DOUBLE PRECISION;

CREATE TABLE IF NOT EXISTS plans (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    max_guests INTEGER NOT NULL DEFAULT 0,
    has_watermark BOOLEAN NOT NULL DEFAULT true,
    custom_domain_allowed BOOLEAN NOT NULL DEFAULT false,
    payment_gateway_allowed BOOLEAN NOT NULL DEFAULT false,
    price NUMERIC(12,2) NOT NULL DEFAULT 0,
    duration_days INTEGER,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS audit_logs (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    invitation_id TEXT,
    action TEXT NOT NULL,
    metadata JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
`
