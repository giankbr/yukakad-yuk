package db

// Payouts of online envelopes (amplop online) that guests paid through Rawuh's Mayar account.
const Schema020 = `
CREATE TABLE IF NOT EXISTS gift_payouts (
    id TEXT PRIMARY KEY DEFAULT gen_random_uuid()::text,
    invitation_id TEXT NOT NULL,
    user_id TEXT NOT NULL,
    amount NUMERIC(14,2) NOT NULL,
    bank_name TEXT NOT NULL,
    account_number TEXT NOT NULL,
    account_name TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'requested',
    note TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    processed_at TIMESTAMPTZ
);
CREATE INDEX IF NOT EXISTS idx_gift_payouts_invitation ON gift_payouts(invitation_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_gift_payouts_status ON gift_payouts(status, created_at);
CREATE INDEX IF NOT EXISTS idx_gift_transactions_reference ON gift_transactions(gateway_reference_id);
`
