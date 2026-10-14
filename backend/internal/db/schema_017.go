package db

// Retire the pre-Rawuh templates. Invitations that used them move to the Rawuh "Linen Putih" theme
// (the frontend also falls back to it for any unknown template id).
const Schema017 = `
UPDATE invitations SET template_id = 'linen-putih'
WHERE template_id IN ('alyra', 'weddings', 'veloria', 'classic', 'botanical', 'minimal', 'aksara');
DELETE FROM templates WHERE id IN ('alyra', 'weddings', 'veloria', 'classic', 'botanical', 'minimal', 'aksara');
`
