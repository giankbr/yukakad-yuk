-- NOTE: This file is not executed by the application. It exists purely as a
-- readable snapshot of the schema for reference. The actual migrations that
-- run at startup are the Go string constants db.Schema001 and db.Schema002
-- in backend/internal/db/migrations.go and schema_002.go, applied via
-- db.MustMigrate in backend/cmd/api/main.go. Keep this file in sync manually
-- when those constants change.

CREATE TABLE IF NOT EXISTS users (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    plan_id TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

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

CREATE TABLE IF NOT EXISTS invitations (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    template_id TEXT,
    slug TEXT NOT NULL UNIQUE,
    title TEXT NOT NULL,
    published BOOLEAN NOT NULL DEFAULT false,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS invitation_settings (
    invitation_id TEXT PRIMARY KEY,
    theme TEXT NOT NULL DEFAULT 'classic',
    primary_color TEXT NOT NULL DEFAULT '#d97706',
    secondary_color TEXT NOT NULL DEFAULT '#f59e0b',
    font TEXT NOT NULL DEFAULT 'poppins',
    music_url TEXT,
    autoplay_music BOOLEAN NOT NULL DEFAULT false
);

CREATE TABLE IF NOT EXISTS couples (
    invitation_id TEXT PRIMARY KEY,
    groom_name TEXT NOT NULL,
    bride_name TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS events (
    invitation_id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    venue TEXT NOT NULL,
    event_date TEXT NOT NULL,
    maps_url TEXT,
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS stories (
    id TEXT PRIMARY KEY,
    invitation_id TEXT NOT NULL,
    title TEXT,
    content TEXT NOT NULL,
    sort_order INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS galleries (
    id TEXT PRIMARY KEY,
    invitation_id TEXT NOT NULL,
    image_url TEXT NOT NULL,
    caption TEXT,
    sort_order INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS guests (
    id TEXT PRIMARY KEY,
    invitation_id TEXT NOT NULL,
    name TEXT NOT NULL,
    phone TEXT,
    category TEXT NOT NULL DEFAULT 'family',
    invitation_token TEXT NOT NULL UNIQUE,
    checked_in_at TIMESTAMPTZ,
    checked_in_by TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS broadcast_logs (
    id TEXT PRIMARY KEY,
    invitation_id TEXT NOT NULL,
    guest_id TEXT,
    channel TEXT NOT NULL DEFAULT 'whatsapp',
    status TEXT NOT NULL DEFAULT 'queued',
    message_snapshot TEXT,
    sent_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS rsvps (
    id TEXT PRIMARY KEY,
    invitation_id TEXT NOT NULL,
    guest_id TEXT,
    attendance TEXT NOT NULL DEFAULT 'pending',
    attendees_count INTEGER NOT NULL DEFAULT 0,
    submitted_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS wishes (
    id TEXT PRIMARY KEY,
    invitation_id TEXT NOT NULL,
    guest_id TEXT,
    name TEXT NOT NULL,
    message TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'pending',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS gifts (
    id TEXT PRIMARY KEY,
    invitation_id TEXT NOT NULL,
    type TEXT NOT NULL,
    bank_name TEXT,
    account_number TEXT,
    account_name TEXT,
    ewallet_provider TEXT,
    ewallet_number TEXT,
    qris_image_url TEXT,
    address TEXT,
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS templates (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    slug TEXT NOT NULL UNIQUE,
    category TEXT NOT NULL,
    preview_image TEXT,
    is_premium BOOLEAN NOT NULL DEFAULT false,
    status TEXT NOT NULL DEFAULT 'active'
);

CREATE TABLE IF NOT EXISTS media (
    id TEXT PRIMARY KEY,
    user_id TEXT,
    invitation_id TEXT NOT NULL,
    type TEXT NOT NULL,
    path TEXT NOT NULL,
    mime_type TEXT,
    size_bytes BIGINT,
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
