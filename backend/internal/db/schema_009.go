package db

const Schema009 = `
ALTER TABLE plans ADD COLUMN IF NOT EXISTS premium_templates_allowed BOOLEAN NOT NULL DEFAULT false;
UPDATE plans SET premium_templates_allowed = (id IN ('pro', 'premium'));
INSERT INTO templates (id, name, slug, category, is_premium, status)
VALUES ('aksara', 'Aksara', 'aksara', 'premium', true, 'active')
ON CONFLICT (id) DO UPDATE SET name = EXCLUDED.name, slug = EXCLUDED.slug, category = EXCLUDED.category, is_premium = EXCLUDED.is_premium, status = EXCLUDED.status;
`
