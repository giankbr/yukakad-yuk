package db

// Schema006 contains the initial product catalog. Catalog data belongs in the
// database so a production boot never depends on an in-memory seed store.
const Schema006 = `
INSERT INTO templates (id, name, slug, category, is_premium, status)
VALUES
    ('classic', 'Classic', 'classic', 'elegant', false, 'active'),
    ('botanical', 'Botanical', 'botanical', 'nature', false, 'active'),
    ('minimal', 'Minimal', 'minimal', 'modern', false, 'active')
ON CONFLICT (id) DO UPDATE SET
    name = EXCLUDED.name,
    slug = EXCLUDED.slug,
    category = EXCLUDED.category,
    is_premium = EXCLUDED.is_premium,
    status = EXCLUDED.status;

INSERT INTO plans (id, name, max_guests, has_watermark, custom_domain_allowed, payment_gateway_allowed, price)
VALUES
    ('free', 'Free', 50, true, false, false, 0),
    ('pro', 'Pro', 500, false, false, false, 99000),
    ('premium', 'Premium', 2000, false, true, true, 249000)
ON CONFLICT (id) DO UPDATE SET
    name = EXCLUDED.name,
    max_guests = EXCLUDED.max_guests,
    has_watermark = EXCLUDED.has_watermark,
    custom_domain_allowed = EXCLUDED.custom_domain_allowed,
    payment_gateway_allowed = EXCLUDED.payment_gateway_allowed,
    price = EXCLUDED.price;
`
