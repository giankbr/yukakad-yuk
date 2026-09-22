package db

const Schema013 = `
ALTER TABLE templates ADD COLUMN IF NOT EXISTS description TEXT NOT NULL DEFAULT '';
ALTER TABLE templates ADD COLUMN IF NOT EXISTS event_type TEXT NOT NULL DEFAULT 'wedding';
ALTER TABLE templates ADD COLUMN IF NOT EXISTS tags JSONB NOT NULL DEFAULT '[]'::jsonb;
ALTER TABLE templates ADD COLUMN IF NOT EXISTS preview_url TEXT NOT NULL DEFAULT '';
ALTER TABLE templates ADD COLUMN IF NOT EXISTS price NUMERIC(12,2) NOT NULL DEFAULT 0;
ALTER TABLE templates ADD COLUMN IF NOT EXISTS tier TEXT NOT NULL DEFAULT 'free';
ALTER TABLE templates ADD COLUMN IF NOT EXISTS supports_photo BOOLEAN NOT NULL DEFAULT true;
ALTER TABLE templates ADD COLUMN IF NOT EXISTS supports_music BOOLEAN NOT NULL DEFAULT false;
ALTER TABLE templates ADD COLUMN IF NOT EXISTS supports_rsvp BOOLEAN NOT NULL DEFAULT true;
ALTER TABLE templates ADD COLUMN IF NOT EXISTS supports_gift BOOLEAN NOT NULL DEFAULT false;
ALTER TABLE templates ADD COLUMN IF NOT EXISTS sort_order INTEGER NOT NULL DEFAULT 0;
ALTER TABLE templates ADD COLUMN IF NOT EXISTS updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW();
CREATE INDEX IF NOT EXISTS idx_templates_catalog ON templates(status, event_type, tier, sort_order);
UPDATE templates SET event_type='wedding', tier=CASE WHEN is_premium THEN 'premium' ELSE 'free' END WHERE event_type='wedding' AND tier='free';
`
