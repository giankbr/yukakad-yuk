package db

// Team size per plan (keluarga / WO / penerima tamu). 0 means unlimited.
const Schema023 = `
ALTER TABLE plans ADD COLUMN IF NOT EXISTS max_team_members INTEGER NOT NULL DEFAULT 15;
UPDATE plans SET max_team_members = 2 WHERE id = 'free' OR price = 0;
UPDATE plans SET max_team_members = 5 WHERE id = 'pro';
UPDATE plans SET max_team_members = 15 WHERE id = 'premium';
`
