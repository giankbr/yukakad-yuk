package db

// Table / seat assignment per guest, shown on the guest's personal invitation and at check-in.
const Schema018 = `
ALTER TABLE guests ADD COLUMN IF NOT EXISTS table_number TEXT NOT NULL DEFAULT '';
`
