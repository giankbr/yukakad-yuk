package db

const Schema012 = `
UPDATE plans SET duration_days = 30 WHERE id IN ('pro', 'premium') AND duration_days IS NULL;
`
