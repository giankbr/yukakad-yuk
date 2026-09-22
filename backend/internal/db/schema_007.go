package db

const Schema007 = `
CREATE TABLE IF NOT EXISTS sessions (
    id TEXT PRIMARY KEY DEFAULT gen_random_uuid()::text,
    user_id TEXT NOT NULL,
    token_hash TEXT NOT NULL UNIQUE,
    expires_at TIMESTAMPTZ NOT NULL,
    revoked_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    last_seen_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS password_reset_tokens (
    id TEXT PRIMARY KEY DEFAULT gen_random_uuid()::text,
    user_id TEXT NOT NULL,
    token_hash TEXT NOT NULL UNIQUE,
    expires_at TIMESTAMPTZ NOT NULL,
    used_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS audit_events (
    id TEXT PRIMARY KEY DEFAULT gen_random_uuid()::text,
    user_id TEXT,
    invitation_id TEXT,
    action TEXT NOT NULL,
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    request_id TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS guest_checkins (
    id TEXT PRIMARY KEY DEFAULT gen_random_uuid()::text,
    invitation_id TEXT NOT NULL,
    guest_id TEXT NOT NULL,
    checked_in_by TEXT NOT NULL,
    checked_in_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS subscriptions (
    id TEXT PRIMARY KEY DEFAULT gen_random_uuid()::text,
    user_id TEXT NOT NULL,
    plan_id TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'active',
    started_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    ends_at TIMESTAMPTZ,
    provider TEXT,
    provider_reference TEXT
);

CREATE TABLE IF NOT EXISTS user_entitlements (
    user_id TEXT NOT NULL,
    feature TEXT NOT NULL,
    value JSONB NOT NULL DEFAULT 'true'::jsonb,
    expires_at TIMESTAMPTZ,
    PRIMARY KEY (user_id, feature)
);

CREATE INDEX IF NOT EXISTS idx_sessions_user_id ON sessions(user_id);
CREATE INDEX IF NOT EXISTS idx_sessions_expiry ON sessions(expires_at);
CREATE INDEX IF NOT EXISTS idx_password_reset_expiry ON password_reset_tokens(expires_at);
CREATE INDEX IF NOT EXISTS idx_audit_events_user ON audit_events(user_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_audit_events_invitation ON audit_events(invitation_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_guest_checkins_invitation ON guest_checkins(invitation_id, checked_in_at DESC);
CREATE INDEX IF NOT EXISTS idx_subscriptions_user ON subscriptions(user_id, status);

CREATE INDEX IF NOT EXISTS idx_invitations_slug_published ON invitations(slug, published);
CREATE INDEX IF NOT EXISTS idx_guests_invitation_category ON guests(invitation_id, category);
CREATE INDEX IF NOT EXISTS idx_rsvps_invitation_attendance ON rsvps(invitation_id, attendance);
CREATE INDEX IF NOT EXISTS idx_wishes_invitation_status ON wishes(invitation_id, status, created_at DESC);
`
