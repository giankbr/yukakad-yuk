package db

// Additive catalog migration: existing templates and assignments are preserved.
const Schema014 = `
INSERT INTO templates (id, name, slug, description, category, preview_image, preview_url, event_type, tier, supports_photo, supports_rsvp, supports_gift, sort_order, status)
VALUES
('alyra', 'Alyra', 'alyra', 'Editorial ivory, oversized serif names and intimate photography.', 'editorial', '/templates/alyra-preview.png', '/invitation/demo?template=alyra', 'wedding', 'free', true, true, true, 1, 'active'),
('weddings', 'Weddings', 'weddings', 'Classic cream, romantic portraits and a clean wedding timeline.', 'modern', '/templates/weddings-preview.png', '/invitation/demo?template=weddings', 'wedding', 'free', true, true, true, 2, 'active'),
('veloria', 'Veloria', 'veloria', 'Warm taupe, olive accents and a romantic asymmetrical layout.', 'editorial', '/templates/veloria-preview.png', '/invitation/demo?template=veloria', 'wedding', 'free', true, true, true, 3, 'active')
ON CONFLICT (id) DO NOTHING;
`
