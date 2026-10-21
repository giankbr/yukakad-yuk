package db

// Six more Javanese (adat Jawa) themes. Additive: existing rows are kept.
const Schema027 = `
INSERT INTO templates (id, name, slug, description, category, preview_image, preview_url, event_type, tier, supports_photo, supports_rsvp, supports_gift, sort_order, status)
VALUES
('joglo-marun', 'Joglo Marun', 'joglo-marun', 'Krem-marun dengan bingkai ukir gebyok, joglo samar, dan rangkaian bunga cat air yang rimbun.', 'Adat Jawa', '/themes/previews/joglo-marun.webp', '/invitation/demo?template=joglo-marun', 'wedding', 'premium', true, true, true, 240, 'active'),
('kawung-biru', 'Kawung Biru', 'kawung-biru', 'Biru nila bergaya toile: joglo, wayang, dan bingkai kawung dengan bunga lili dan anggrek.', 'Adat Jawa', '/themes/previews/kawung-biru.webp', '/invitation/demo?template=kawung-biru', 'wedding', 'premium', true, true, true, 241, 'active'),
('gebyok-sogan', 'Gebyok Sogan', 'gebyok-sogan', 'Krem dan cokelat sogan dengan gapura gebyok berukir, kembar mayang emas, dan kabut pegunungan.', 'Adat Jawa', '/themes/previews/gebyok-sogan.webp', '/invitation/demo?template=gebyok-sogan', 'wedding', 'premium', true, true, true, 242, 'active'),
('busana-jawi', 'Busana Jawi', 'busana-jawi', 'Foto penuh pasangan berbusana adat dengan tulisan putih elegan dan aksen batik parang emas.', 'Adat Jawa', '/themes/previews/busana-jawi.webp', '/invitation/demo?template=busana-jawi', 'wedding', 'premium', true, true, true, 243, 'active'),
('wayang-mega', 'Wayang Mega', 'wayang-mega', 'Tanpa foto: awan mega mendung, sepasang wayang kulit, dan pinggiran batik sogan.', 'Adat Jawa', '/themes/previews/wayang-mega.webp', '/invitation/demo?template=wayang-mega', 'wedding', 'free', true, true, true, 244, 'active'),
('kereta-kencana', 'Kereta Kencana', 'kereta-kencana', 'Kemegahan keraton Solo-Jogja: hijau tua dan emas, kereta kencana, payung agung, dan motif paes.', 'Adat Jawa', '/themes/previews/kereta-kencana.webp', '/invitation/demo?template=kereta-kencana', 'wedding', 'premium', true, true, true, 245, 'active')
ON CONFLICT (id) DO NOTHING;
`
