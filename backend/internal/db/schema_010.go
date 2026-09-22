package db

const Schema010 = `
CREATE TABLE IF NOT EXISTS custom_domains (
    id TEXT PRIMARY KEY DEFAULT gen_random_uuid()::text,
    user_id TEXT NOT NULL,
    invitation_id TEXT NOT NULL,
    domain TEXT NOT NULL UNIQUE,
    verification_token TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'pending',
    verified_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_custom_domains_user ON custom_domains(user_id);
CREATE INDEX IF NOT EXISTS idx_custom_domains_invitation ON custom_domains(invitation_id);
`
