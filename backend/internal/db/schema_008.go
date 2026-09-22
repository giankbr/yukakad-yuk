package db

const Schema008 = `
DELETE FROM rsvps a
USING rsvps b
WHERE a.invitation_id = b.invitation_id
  AND a.guest_id IS NOT NULL
  AND a.guest_id = b.guest_id
  AND a.submitted_at < b.submitted_at;

CREATE UNIQUE INDEX IF NOT EXISTS idx_rsvps_invitation_guest
ON rsvps(invitation_id, guest_id) WHERE guest_id IS NOT NULL;
`
