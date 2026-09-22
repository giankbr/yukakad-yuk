package db

const Schema011 = `
CREATE TABLE IF NOT EXISTS invoices (
    id TEXT PRIMARY KEY DEFAULT gen_random_uuid()::text,
    user_id TEXT NOT NULL,
    subscription_id TEXT NOT NULL,
    invoice_number TEXT NOT NULL UNIQUE,
    amount NUMERIC(12,2) NOT NULL,
    status TEXT NOT NULL DEFAULT 'paid',
    issued_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    paid_at TIMESTAMPTZ
);
CREATE INDEX IF NOT EXISTS idx_invoices_user ON invoices(user_id, issued_at DESC);
`
