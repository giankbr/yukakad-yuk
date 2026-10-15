package db

// Team members per invitation (keluarga, WO/vendor, penerima tamu) with an invite link.
const Schema022 = `
CREATE TABLE IF NOT EXISTS invitation_members (
    id TEXT PRIMARY KEY DEFAULT gen_random_uuid()::text,
    invitation_id TEXT NOT NULL,
    user_id TEXT,
    email TEXT,
    role TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'pending',
    token_hash TEXT,
    invited_by TEXT,
    expires_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    accepted_at TIMESTAMPTZ
);
CREATE INDEX IF NOT EXISTS idx_invitation_members_invitation ON invitation_members(invitation_id);
CREATE INDEX IF NOT EXISTS idx_invitation_members_user ON invitation_members(user_id) WHERE user_id IS NOT NULL;
CREATE UNIQUE INDEX IF NOT EXISTS idx_invitation_members_token ON invitation_members(token_hash) WHERE token_hash IS NOT NULL;
CREATE UNIQUE INDEX IF NOT EXISTS idx_invitation_members_active ON invitation_members(invitation_id, user_id) WHERE user_id IS NOT NULL;
`
