package db

const Schema004 = `
-- Extend couples with photo and parent fields
ALTER TABLE couples ADD COLUMN IF NOT EXISTS groom_photo TEXT;
ALTER TABLE couples ADD COLUMN IF NOT EXISTS bride_photo TEXT;
ALTER TABLE couples ADD COLUMN IF NOT EXISTS groom_parents TEXT;
ALTER TABLE couples ADD COLUMN IF NOT EXISTS bride_parents TEXT;

-- Extend legacy 1:1 events table with richer fields (for backward compat)
ALTER TABLE events ADD COLUMN IF NOT EXISTS type TEXT NOT NULL DEFAULT 'reception';
ALTER TABLE events ADD COLUMN IF NOT EXISTS start_time TEXT;
ALTER TABLE events ADD COLUMN IF NOT EXISTS end_time TEXT;
ALTER TABLE events ADD COLUMN IF NOT EXISTS address TEXT;

-- New 1:N multi-event table (akad, reception, etc.)
CREATE TABLE IF NOT EXISTS invitation_events (
    id TEXT PRIMARY KEY DEFAULT gen_random_uuid()::text,
    invitation_id TEXT NOT NULL,
    title TEXT NOT NULL DEFAULT '',
    type TEXT NOT NULL DEFAULT 'reception',
    event_date TEXT NOT NULL DEFAULT '',
    start_time TEXT,
    end_time TEXT,
    venue TEXT NOT NULL DEFAULT '',
    address TEXT,
    maps_url TEXT,
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    sort_order INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Migrate existing single events into the new multi-event table (idempotent)
INSERT INTO invitation_events (id, invitation_id, title, type, event_date, venue, maps_url, latitude, longitude, sort_order)
SELECT
    gen_random_uuid()::text,
    e.invitation_id,
    e.title,
    'reception',
    e.event_date,
    e.venue,
    COALESCE(e.maps_url, ''),
    COALESCE(e.latitude, 0),
    COALESCE(e.longitude, 0),
    0
FROM events e
WHERE NOT EXISTS (
    SELECT 1 FROM invitation_events ie WHERE ie.invitation_id = e.invitation_id
);

-- Performance indexes
CREATE INDEX IF NOT EXISTS idx_invitation_events_inv_id ON invitation_events(invitation_id, sort_order);
CREATE INDEX IF NOT EXISTS idx_guests_inv_id ON guests(invitation_id);
CREATE INDEX IF NOT EXISTS idx_rsvps_inv_id ON rsvps(invitation_id);
CREATE INDEX IF NOT EXISTS idx_wishes_inv_id ON wishes(invitation_id);
CREATE INDEX IF NOT EXISTS idx_invitations_user_id ON invitations(user_id);
`
