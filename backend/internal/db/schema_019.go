package db

// Story photo for the "Kisah cinta" timeline (stories.date already exists since Schema005).
const Schema019 = `
ALTER TABLE stories ADD COLUMN IF NOT EXISTS image_url TEXT;
`
