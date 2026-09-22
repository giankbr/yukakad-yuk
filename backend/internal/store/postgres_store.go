package store

import (
	"database/sql"
	"encoding/json"
	"fmt"
	"strings"
	"time"
)

type PostgresStore struct {
	db *sql.DB
}

func NewPostgresStore(db *sql.DB) *PostgresStore {
	return &PostgresStore{db: db}
}

func (s *PostgresStore) CreateUser(name, email, password string) (*User, error) {
	user := &User{}
	err := s.db.QueryRow(`INSERT INTO users (id, name, email, password_hash) VALUES (gen_random_uuid()::text, $1, $2, $3) RETURNING id, role, created_at`, name, email, password).Scan(&user.ID, &user.Role, &user.CreatedAt)
	if err != nil {
		return nil, fmt.Errorf("create user: %w", err)
	}
	user.Name, user.Email, user.Password = name, email, password
	return user, nil
}

func (s *PostgresStore) FindUserByEmail(email string) (*User, bool) {
	user := &User{}
	err := s.db.QueryRow(`SELECT id, name, email, password_hash, role, COALESCE(avatar,''), created_at FROM users WHERE email = $1`, email).Scan(&user.ID, &user.Name, &user.Email, &user.Password, &user.Role, &user.Avatar, &user.CreatedAt)
	return user, err == nil
}

func (s *PostgresStore) FindUserByID(id string) (*User, bool) {
	user := &User{}
	err := s.db.QueryRow(`SELECT id, name, email, password_hash, role, COALESCE(avatar,''), created_at FROM users WHERE id = $1`, id).Scan(&user.ID, &user.Name, &user.Email, &user.Password, &user.Role, &user.Avatar, &user.CreatedAt)
	return user, err == nil
}

func (s *PostgresStore) UpdateUser(id, name string) (*User, error) {
	user := &User{}
	err := s.db.QueryRow(`UPDATE users SET name = $1 WHERE id = $2 RETURNING id, name, email, password_hash, role, created_at`, name, id).Scan(&user.ID, &user.Name, &user.Email, &user.Password, &user.Role, &user.CreatedAt)
	if err != nil {
		return nil, fmt.Errorf("update user: %w", err)
	}
	return user, nil
}

func (s *PostgresStore) UpdateUserRole(id, role string) (*User, error) {
	user := &User{}
	err := s.db.QueryRow(`UPDATE users SET role = $1 WHERE id = $2 RETURNING id, name, email, password_hash, role, created_at`, role, id).Scan(&user.ID, &user.Name, &user.Email, &user.Password, &user.Role, &user.CreatedAt)
	if err != nil {
		return nil, fmt.Errorf("update user role: %w", err)
	}
	return user, nil
}

func (s *PostgresStore) UpdatePassword(id, password string) error {
	result, err := s.db.Exec(`UPDATE users SET password_hash = $1, updated_at = NOW() WHERE id = $2`, password, id)
	if err != nil {
		return err
	}
	count, _ := result.RowsAffected()
	if count == 0 {
		return fmt.Errorf("user not found")
	}
	return nil
}

func (s *PostgresStore) CreatePasswordResetToken(userID, tokenHash string, expiresAt time.Time) error {
	_, err := s.db.Exec(`INSERT INTO password_reset_tokens (user_id, token_hash, expires_at) VALUES ($1, $2, $3)`, userID, tokenHash, expiresAt)
	return err
}

func (s *PostgresStore) ConsumePasswordResetToken(tokenHash string) (string, error) {
	var userID string
	err := s.db.QueryRow(`UPDATE password_reset_tokens SET used_at = NOW() WHERE token_hash = $1 AND used_at IS NULL AND expires_at > NOW() RETURNING user_id`, tokenHash).Scan(&userID)
	if err != nil {
		return "", fmt.Errorf("invalid or expired reset token: %w", err)
	}
	return userID, nil
}

func (s *PostgresStore) CreateInvitation(userID, slug, title string) (*Invitation, error) {
	invitation := &Invitation{}
	err := s.db.QueryRow(`INSERT INTO invitations (id, user_id, slug, title) VALUES (gen_random_uuid()::text, $1, $2, $3) RETURNING id, created_at`, userID, slug, title).Scan(&invitation.ID, &invitation.CreatedAt)
	if err != nil {
		return nil, fmt.Errorf("create invitation: %w", err)
	}
	invitation.UserID, invitation.Slug, invitation.Title = userID, slug, title
	return invitation, nil
}

func (s *PostgresStore) scanInvitation(row *sql.Row) (*Invitation, error) {
	invitation := &Invitation{}
	var publishedAt sql.NullTime
	err := row.Scan(&invitation.ID, &invitation.UserID, &invitation.Slug, &invitation.Title, &invitation.Published, &invitation.TemplateID, &publishedAt, &invitation.UpdatedAt, &invitation.CreatedAt)
	if err != nil {
		return nil, err
	}
	if publishedAt.Valid {
		invitation.PublishedAt = &publishedAt.Time
	}
	_ = s.db.QueryRow(`SELECT groom_name, bride_name, COALESCE(groom_nickname,''), COALESCE(bride_nickname,''), COALESCE(groom_photo,''), COALESCE(bride_photo,''), COALESCE(groom_parents,''), COALESCE(bride_parents,'') FROM couples WHERE invitation_id = $1`, invitation.ID).
		Scan(&invitation.Couple.GroomName, &invitation.Couple.BrideName, &invitation.Couple.GroomNickname, &invitation.Couple.BrideNickname, &invitation.Couple.GroomPhoto, &invitation.Couple.BridePhoto, &invitation.Couple.GroomParents, &invitation.Couple.BrideParents)
	_ = s.db.QueryRow(`SELECT title, venue, event_date, COALESCE(maps_url,''), COALESCE(type,''), COALESCE(start_time,''), COALESCE(end_time,''), COALESCE(address,'') FROM events WHERE invitation_id = $1`, invitation.ID).
		Scan(&invitation.Event.Title, &invitation.Event.Venue, &invitation.Event.Date, &invitation.Event.MapsURL, &invitation.Event.Type, &invitation.Event.StartTime, &invitation.Event.EndTime, &invitation.Event.Address)
	return invitation, nil
}

func (s *PostgresStore) FindInvitationByID(id string) (*Invitation, bool) {
	invitation, err := s.scanInvitation(s.db.QueryRow(`SELECT id, user_id, slug, title, published, COALESCE(template_id, ''), published_at, updated_at, created_at FROM invitations WHERE id = $1`, id))
	return invitation, err == nil
}

func (s *PostgresStore) FindInvitationBySlug(slug string) (*Invitation, bool) {
	invitation, err := s.scanInvitation(s.db.QueryRow(`SELECT id, user_id, slug, title, published, COALESCE(template_id, ''), published_at, updated_at, created_at FROM invitations WHERE slug = $1`, slug))
	return invitation, err == nil
}

func (s *PostgresStore) ListInvitationsByUser(userID string) []*Invitation {
	rows, err := s.db.Query(`SELECT id, user_id, slug, title, published, COALESCE(template_id, ''), published_at, updated_at, created_at FROM invitations WHERE user_id = $1 ORDER BY created_at DESC`, userID)
	if err != nil {
		return []*Invitation{}
	}
	defer rows.Close()
	items := make([]*Invitation, 0)
	for rows.Next() {
		item := &Invitation{}
		var publishedAt sql.NullTime
		if rows.Scan(&item.ID, &item.UserID, &item.Slug, &item.Title, &item.Published, &item.TemplateID, &publishedAt, &item.UpdatedAt, &item.CreatedAt) == nil {
			if publishedAt.Valid {
				item.PublishedAt = &publishedAt.Time
			}
			_ = s.db.QueryRow(`SELECT groom_name, bride_name, COALESCE(groom_nickname,''), COALESCE(bride_nickname,''), COALESCE(groom_photo,''), COALESCE(bride_photo,''), COALESCE(groom_parents,''), COALESCE(bride_parents,'') FROM couples WHERE invitation_id = $1`, item.ID).
				Scan(&item.Couple.GroomName, &item.Couple.BrideName, &item.Couple.GroomNickname, &item.Couple.BrideNickname, &item.Couple.GroomPhoto, &item.Couple.BridePhoto, &item.Couple.GroomParents, &item.Couple.BrideParents)
			_ = s.db.QueryRow(`SELECT title, venue, event_date, COALESCE(maps_url,''), COALESCE(type,''), COALESCE(start_time,''), COALESCE(end_time,''), COALESCE(address,'') FROM events WHERE invitation_id = $1`, item.ID).
				Scan(&item.Event.Title, &item.Event.Venue, &item.Event.Date, &item.Event.MapsURL, &item.Event.Type, &item.Event.StartTime, &item.Event.EndTime, &item.Event.Address)
			items = append(items, item)
		}
	}
	if err := rows.Err(); err != nil {
		return []*Invitation{}
	}
	return items
}

func (s *PostgresStore) UpdateInvitation(id, slug, title string, published bool, couple Couple, event Event) (*Invitation, error) {
	invitation := &Invitation{}
	var publishedAt sql.NullTime
	err := s.db.QueryRow(`UPDATE invitations SET slug = $1, title = $2, published = $3, updated_at = NOW(), published_at = CASE WHEN $3 = true AND published = false THEN NOW() ELSE published_at END WHERE id = $4 RETURNING id, user_id, slug, title, published, published_at, updated_at, created_at`, slug, title, published, id).Scan(&invitation.ID, &invitation.UserID, &invitation.Slug, &invitation.Title, &invitation.Published, &publishedAt, &invitation.UpdatedAt, &invitation.CreatedAt)
	if publishedAt.Valid {
		invitation.PublishedAt = &publishedAt.Time
	}
	if err != nil {
		return nil, fmt.Errorf("update invitation: %w", err)
	}
	invitation.Couple, invitation.Event = couple, event
	_, _ = s.db.Exec(`INSERT INTO couples (invitation_id, groom_name, bride_name, groom_nickname, bride_nickname, groom_photo, bride_photo, groom_parents, bride_parents) VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9) ON CONFLICT (invitation_id) DO UPDATE SET groom_name=EXCLUDED.groom_name, bride_name=EXCLUDED.bride_name, groom_nickname=EXCLUDED.groom_nickname, bride_nickname=EXCLUDED.bride_nickname, groom_photo=EXCLUDED.groom_photo, bride_photo=EXCLUDED.bride_photo, groom_parents=EXCLUDED.groom_parents, bride_parents=EXCLUDED.bride_parents`,
		id, couple.GroomName, couple.BrideName, couple.GroomNickname, couple.BrideNickname, couple.GroomPhoto, couple.BridePhoto, couple.GroomParents, couple.BrideParents)
	_, _ = s.db.Exec(`INSERT INTO events (invitation_id, title, venue, event_date, maps_url, type, start_time, end_time, address) VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9) ON CONFLICT (invitation_id) DO UPDATE SET title=EXCLUDED.title, venue=EXCLUDED.venue, event_date=EXCLUDED.event_date, maps_url=EXCLUDED.maps_url, type=EXCLUDED.type, start_time=EXCLUDED.start_time, end_time=EXCLUDED.end_time, address=EXCLUDED.address`,
		id, event.Title, event.Venue, event.Date, event.MapsURL, event.Type, event.StartTime, event.EndTime, event.Address)
	return invitation, nil
}

func (s *PostgresStore) DeleteInvitation(id string) error {
	result, err := s.db.Exec(`DELETE FROM invitations WHERE id = $1`, id)
	if err != nil {
		return err
	}
	count, err := result.RowsAffected()
	if err != nil || count == 0 {
		return fmt.Errorf("invitation not found")
	}
	return nil
}

func (s *PostgresStore) CreateGuest(invitationID, name, phone, category string) (*Guest, error) {
	guest := &Guest{}
	err := s.db.QueryRow(`INSERT INTO guests (id, invitation_id, name, phone, category, invitation_token) VALUES (gen_random_uuid()::text, $1, $2, $3, $4, encode(gen_random_bytes(18), 'hex')) RETURNING id, invitation_token, created_at`, invitationID, name, phone, category).Scan(&guest.ID, &guest.Token, &guest.CreatedAt)
	if err != nil {
		return nil, fmt.Errorf("create guest: %w", err)
	}
	guest.InvitationID, guest.Name, guest.Phone, guest.Category = invitationID, name, phone, category
	return guest, nil
}

func (s *PostgresStore) ListGuests(invitationID string) []*Guest {
	rows, err := s.db.Query(`SELECT id, invitation_id, name, phone, category, invitation_token, checked_in_at, checked_in_by, created_at FROM guests WHERE invitation_id = $1 ORDER BY created_at DESC`, invitationID)
	if err != nil {
		return []*Guest{}
	}
	defer rows.Close()
	items := make([]*Guest, 0)
	for rows.Next() {
		item := &Guest{}
		var checkedInBy sql.NullString
		if rows.Scan(&item.ID, &item.InvitationID, &item.Name, &item.Phone, &item.Category, &item.Token, &item.CheckedInAt, &checkedInBy, &item.CreatedAt) == nil {
			if checkedInBy.Valid {
				item.CheckedInBy = &checkedInBy.String
			}
			items = append(items, item)
		}
	}
	if err := rows.Err(); err != nil {
		return []*Guest{}
	}
	return items
}

func (s *PostgresStore) FindGuestByID(id string) (*Guest, bool) {
	guest := &Guest{}
	var checkedInBy sql.NullString
	err := s.db.QueryRow(`SELECT id, invitation_id, name, phone, category, invitation_token, checked_in_at, checked_in_by, created_at FROM guests WHERE id = $1`, id).
		Scan(&guest.ID, &guest.InvitationID, &guest.Name, &guest.Phone, &guest.Category, &guest.Token, &guest.CheckedInAt, &checkedInBy, &guest.CreatedAt)
	if err != nil {
		return nil, false
	}
	if checkedInBy.Valid {
		guest.CheckedInBy = &checkedInBy.String
	}
	return guest, true
}

func (s *PostgresStore) FindGuestByToken(invitationID, token string) (*Guest, bool) {
	guest := &Guest{}
	var checkedInBy sql.NullString
	err := s.db.QueryRow(`SELECT id, invitation_id, name, phone, category, invitation_token, checked_in_at, checked_in_by, created_at FROM guests WHERE invitation_id = $1 AND invitation_token = $2`, invitationID, token).
		Scan(&guest.ID, &guest.InvitationID, &guest.Name, &guest.Phone, &guest.Category, &guest.Token, &guest.CheckedInAt, &checkedInBy, &guest.CreatedAt)
	if err != nil {
		return nil, false
	}
	if checkedInBy.Valid {
		guest.CheckedInBy = &checkedInBy.String
	}
	return guest, true
}

func (s *PostgresStore) UpdateGuest(id, name, phone, category string) (*Guest, error) {
	guest := &Guest{}
	err := s.db.QueryRow(`UPDATE guests SET name = $1, phone = $2, category = $3, updated_at = NOW() WHERE id = $4 RETURNING id, invitation_id, name, phone, category, invitation_token, created_at`, name, phone, category, id).Scan(&guest.ID, &guest.InvitationID, &guest.Name, &guest.Phone, &guest.Category, &guest.Token, &guest.CreatedAt)
	if err != nil {
		return nil, fmt.Errorf("update guest: %w", err)
	}
	return guest, nil
}

func (s *PostgresStore) DeleteGuest(id string) error {
	result, err := s.db.Exec(`DELETE FROM guests WHERE id = $1`, id)
	if err != nil {
		return err
	}
	count, _ := result.RowsAffected()
	if count == 0 {
		return fmt.Errorf("guest not found")
	}
	return nil
}

func (s *PostgresStore) CheckInGuest(id, actorUserID string) (*Guest, error) {
	guest := &Guest{}
	var checkedInBy sql.NullString
	err := s.db.QueryRow(`UPDATE guests SET checked_in_at = NOW(), checked_in_by = $2, updated_at = NOW() WHERE id = $1 RETURNING id, invitation_id, name, phone, category, invitation_token, created_at, checked_in_at, checked_in_by`, id, actorUserID).
		Scan(&guest.ID, &guest.InvitationID, &guest.Name, &guest.Phone, &guest.Category, &guest.Token, &guest.CreatedAt, &guest.CheckedInAt, &checkedInBy)
	if err != nil {
		return nil, fmt.Errorf("check in guest: %w", err)
	}
	if checkedInBy.Valid {
		guest.CheckedInBy = &checkedInBy.String
	}
	return guest, nil
}

func (s *PostgresStore) CreateRSVP(invitationID, guestID, attendance string, attendeesCount int, message string) (*RSVP, error) {
	rsvp := &RSVP{}
	err := s.db.QueryRow(`INSERT INTO rsvps (id, invitation_id, guest_id, attendance, attendees_count, message) VALUES (gen_random_uuid()::text, $1, NULLIF($2, ''), $3, $4, $5) RETURNING id, submitted_at`, invitationID, guestID, attendance, attendeesCount, message).Scan(&rsvp.ID, &rsvp.SubmittedAt)
	if err != nil {
		return nil, fmt.Errorf("create rsvp: %w", err)
	}
	rsvp.InvitationID, rsvp.GuestID, rsvp.Attendance, rsvp.AttendeesCount, rsvp.Message = invitationID, guestID, attendance, attendeesCount, message
	return rsvp, nil
}

func (s *PostgresStore) UpsertRSVP(invitationID, guestID, attendance string, attendeesCount int, message string) (*RSVP, error) {
	rsvp := &RSVP{}
	err := s.db.QueryRow(`INSERT INTO rsvps (id, invitation_id, guest_id, attendance, attendees_count, message)
		VALUES (gen_random_uuid()::text, $1, NULLIF($2, ''), $3, $4, $5)
		ON CONFLICT (invitation_id, guest_id) WHERE guest_id IS NOT NULL
		DO UPDATE SET attendance = EXCLUDED.attendance, attendees_count = EXCLUDED.attendees_count, message = EXCLUDED.message, submitted_at = NOW()
		RETURNING id, invitation_id, COALESCE(guest_id::text, ''), attendance, attendees_count, COALESCE(message, ''), submitted_at`, invitationID, guestID, attendance, attendeesCount, message).
		Scan(&rsvp.ID, &rsvp.InvitationID, &rsvp.GuestID, &rsvp.Attendance, &rsvp.AttendeesCount, &rsvp.Message, &rsvp.SubmittedAt)
	if err != nil {
		return nil, fmt.Errorf("upsert rsvp: %w", err)
	}
	return rsvp, nil
}

func (s *PostgresStore) ListRSVPs(invitationID string) []*RSVP {
	rows, err := s.db.Query(`SELECT id, invitation_id, COALESCE(guest_id::text, ''), attendance, attendees_count, COALESCE(message, ''), submitted_at FROM rsvps WHERE invitation_id = $1 ORDER BY submitted_at DESC`, invitationID)
	if err != nil {
		return []*RSVP{}
	}
	defer rows.Close()
	items := make([]*RSVP, 0)
	for rows.Next() {
		item := &RSVP{}
		if rows.Scan(&item.ID, &item.InvitationID, &item.GuestID, &item.Attendance, &item.AttendeesCount, &item.Message, &item.SubmittedAt) == nil {
			items = append(items, item)
		}
	}
	if err := rows.Err(); err != nil {
		return []*RSVP{}
	}
	return items
}

func (s *PostgresStore) RSVPSummary(invitationID string) map[string]int {
	summary := map[string]int{"yes": 0, "no": 0, "maybe": 0, "attendees": 0}
	rows, err := s.db.Query(`SELECT attendance, COUNT(*), COALESCE(SUM(attendees_count), 0) FROM rsvps WHERE invitation_id = $1 GROUP BY attendance`, invitationID)
	if err != nil {
		return summary
	}
	defer rows.Close()
	for rows.Next() {
		var attendance string
		var count, attendees int
		if rows.Scan(&attendance, &count, &attendees) == nil {
			summary[attendance] = count
			summary["attendees"] += attendees
		}
	}
	if err := rows.Err(); err != nil {
		return map[string]int{"yes": 0, "no": 0, "maybe": 0, "attendees": 0}
	}
	return summary
}

func (s *PostgresStore) CreateWish(invitationID, guestID, name, message string) (*Wish, error) {
	wish := &Wish{}
	err := s.db.QueryRow(`INSERT INTO wishes (id, invitation_id, guest_id, name, message) VALUES (gen_random_uuid()::text, $1, NULLIF($2, ''), $3, $4) RETURNING id, status, created_at`, invitationID, guestID, name, message).Scan(&wish.ID, &wish.Status, &wish.CreatedAt)
	if err != nil {
		return nil, fmt.Errorf("create wish: %w", err)
	}
	wish.InvitationID, wish.GuestID, wish.Name, wish.Message = invitationID, guestID, name, message
	return wish, nil
}

func (s *PostgresStore) ListPublishedWishes(invitationID string) []*Wish {
	return s.listWishes(invitationID, "published")
}
func (s *PostgresStore) ListWishes(invitationID string) []*Wish {
	return s.listWishes(invitationID, "")
}

func (s *PostgresStore) listWishes(invitationID, status string) []*Wish {
	query := `SELECT id, invitation_id, COALESCE(guest_id::text, ''), name, message, status, created_at FROM wishes WHERE invitation_id = $1`
	args := []any{invitationID}
	if status != "" {
		query += ` AND status = $2`
		args = append(args, status)
	}
	query += ` ORDER BY created_at DESC`
	rows, err := s.db.Query(query, args...)
	if err != nil {
		return []*Wish{}
	}
	defer rows.Close()
	items := make([]*Wish, 0)
	for rows.Next() {
		item := &Wish{}
		if rows.Scan(&item.ID, &item.InvitationID, &item.GuestID, &item.Name, &item.Message, &item.Status, &item.CreatedAt) == nil {
			items = append(items, item)
		}
	}
	if err := rows.Err(); err != nil {
		return []*Wish{}
	}
	return items
}

func (s *PostgresStore) UpdateWishStatus(id, status string) (*Wish, error) {
	wish := &Wish{}
	err := s.db.QueryRow(`UPDATE wishes SET status = $1, updated_at = NOW() WHERE id = $2 RETURNING id, invitation_id, COALESCE(guest_id::text, ''), name, message, status, created_at`, status, id).Scan(&wish.ID, &wish.InvitationID, &wish.GuestID, &wish.Name, &wish.Message, &wish.Status, &wish.CreatedAt)
	if err != nil {
		return nil, fmt.Errorf("update wish: %w", err)
	}
	return wish, nil
}

func (s *PostgresStore) CreateGift(invitationID string, gift Gift) (*Gift, error) {
	created := &Gift{}
	err := s.db.QueryRow(`INSERT INTO gifts (id, invitation_id, type, bank_name, account_number, account_name, ewallet_provider, ewallet_number, qris_image_url, address) VALUES (gen_random_uuid()::text, $1, $2, $3, $4, $5, $6, $7, $8, $9) RETURNING id, is_active, created_at`, invitationID, gift.Type, gift.BankName, gift.AccountNumber, gift.AccountName, gift.EwalletProvider, gift.EwalletNumber, gift.QRISImageURL, gift.Address).Scan(&created.ID, &created.Active, &created.CreatedAt)
	if err != nil {
		return nil, fmt.Errorf("create gift: %w", err)
	}
	created.InvitationID, created.Type, created.BankName, created.AccountNumber, created.AccountName = invitationID, gift.Type, gift.BankName, gift.AccountNumber, gift.AccountName
	created.EwalletProvider, created.EwalletNumber, created.QRISImageURL, created.Address = gift.EwalletProvider, gift.EwalletNumber, gift.QRISImageURL, gift.Address
	return created, nil
}

func (s *PostgresStore) ListActiveGifts(invitationID string) []*Gift {
	rows, err := s.db.Query(`SELECT id, invitation_id, type, COALESCE(bank_name, ''), COALESCE(account_number, ''), COALESCE(account_name, ''), COALESCE(ewallet_provider, ''), COALESCE(ewallet_number, ''), COALESCE(qris_image_url, ''), COALESCE(address, ''), is_active, created_at FROM gifts WHERE invitation_id = $1 AND is_active = true ORDER BY created_at DESC`, invitationID)
	if err != nil {
		return []*Gift{}
	}
	defer rows.Close()
	items := make([]*Gift, 0)
	for rows.Next() {
		item := &Gift{}
		if rows.Scan(&item.ID, &item.InvitationID, &item.Type, &item.BankName, &item.AccountNumber, &item.AccountName, &item.EwalletProvider, &item.EwalletNumber, &item.QRISImageURL, &item.Address, &item.Active, &item.CreatedAt) == nil {
			items = append(items, item)
		}
	}
	if err := rows.Err(); err != nil {
		return []*Gift{}
	}
	return items
}

func (s *PostgresStore) ListGifts(invitationID string) []*Gift {
	rows, err := s.db.Query(`SELECT id, invitation_id, type, COALESCE(bank_name, ''), COALESCE(account_number, ''), COALESCE(account_name, ''), COALESCE(ewallet_provider, ''), COALESCE(ewallet_number, ''), COALESCE(qris_image_url, ''), COALESCE(address, ''), is_active, created_at FROM gifts WHERE invitation_id = $1 ORDER BY created_at DESC`, invitationID)
	if err != nil {
		return []*Gift{}
	}
	defer rows.Close()
	items := make([]*Gift, 0)
	for rows.Next() {
		item := &Gift{}
		if rows.Scan(&item.ID, &item.InvitationID, &item.Type, &item.BankName, &item.AccountNumber, &item.AccountName, &item.EwalletProvider, &item.EwalletNumber, &item.QRISImageURL, &item.Address, &item.Active, &item.CreatedAt) == nil {
			items = append(items, item)
		}
	}
	if err := rows.Err(); err != nil {
		return []*Gift{}
	}
	return items
}

func (s *PostgresStore) SetGiftActive(id string, active bool) (*Gift, error) {
	gift := &Gift{}
	err := s.db.QueryRow(`UPDATE gifts SET is_active = $1 WHERE id = $2 RETURNING id, invitation_id, type, COALESCE(bank_name, ''), COALESCE(account_number, ''), COALESCE(account_name, ''), COALESCE(ewallet_provider, ''), COALESCE(ewallet_number, ''), COALESCE(qris_image_url, ''), COALESCE(address, ''), is_active, created_at`, active, id).
		Scan(&gift.ID, &gift.InvitationID, &gift.Type, &gift.BankName, &gift.AccountNumber, &gift.AccountName, &gift.EwalletProvider, &gift.EwalletNumber, &gift.QRISImageURL, &gift.Address, &gift.Active, &gift.CreatedAt)
	if err != nil {
		return nil, fmt.Errorf("set gift active: %w", err)
	}
	return gift, nil
}

func (s *PostgresStore) CreateGiftTransaction(tx GiftTransaction) (*GiftTransaction, error) {
	created := &GiftTransaction{InvitationID: tx.InvitationID, GuestID: tx.GuestID, Gateway: tx.Gateway, GatewayReference: tx.GatewayReference, Amount: tx.Amount, Status: tx.Status, SenderName: tx.SenderName, Message: tx.Message}
	err := s.db.QueryRow(`INSERT INTO gift_transactions (invitation_id, guest_id, gateway, gateway_reference_id, amount, status, sender_name, message) VALUES ($1, NULLIF($2,''), $3, NULLIF($4,''), $5, $6, $7, $8) RETURNING id, created_at`, tx.InvitationID, tx.GuestID, tx.Gateway, tx.GatewayReference, tx.Amount, tx.Status, tx.SenderName, tx.Message).Scan(&created.ID, &created.CreatedAt)
	if err != nil {
		return nil, err
	}
	return created, nil
}

func (s *PostgresStore) ListGiftTransactions(invitationID string) []*GiftTransaction {
	rows, err := s.db.Query(`SELECT id, invitation_id, COALESCE(guest_id,''), gateway, COALESCE(gateway_reference_id,''), amount, status, COALESCE(sender_name,''), COALESCE(message,''), created_at FROM gift_transactions WHERE invitation_id = $1 ORDER BY created_at DESC`, invitationID)
	if err != nil {
		return []*GiftTransaction{}
	}
	defer rows.Close()
	items := make([]*GiftTransaction, 0)
	for rows.Next() {
		tx := &GiftTransaction{}
		if rows.Scan(&tx.ID, &tx.InvitationID, &tx.GuestID, &tx.Gateway, &tx.GatewayReference, &tx.Amount, &tx.Status, &tx.SenderName, &tx.Message, &tx.CreatedAt) == nil {
			items = append(items, tx)
		}
	}
	return items
}

func (s *PostgresStore) FindGiftTransactionByReference(reference string) (*GiftTransaction, bool) {
	tx := &GiftTransaction{}
	err := s.db.QueryRow(`SELECT id, invitation_id, COALESCE(guest_id,''), gateway, COALESCE(gateway_reference_id,''), amount, status, COALESCE(sender_name,''), COALESCE(message,''), created_at FROM gift_transactions WHERE gateway_reference_id = $1`, reference).Scan(&tx.ID, &tx.InvitationID, &tx.GuestID, &tx.Gateway, &tx.GatewayReference, &tx.Amount, &tx.Status, &tx.SenderName, &tx.Message, &tx.CreatedAt)
	return tx, err == nil
}

func (s *PostgresStore) UpdateGiftTransactionStatus(id, status, reference string) (*GiftTransaction, error) {
	tx := &GiftTransaction{}
	err := s.db.QueryRow(`UPDATE gift_transactions SET status=$1, gateway_reference_id=NULLIF($2,'') WHERE id=$3 RETURNING id, invitation_id, COALESCE(guest_id,''), gateway, COALESCE(gateway_reference_id,''), amount, status, COALESCE(sender_name,''), COALESCE(message,''), created_at`, status, reference, id).Scan(&tx.ID, &tx.InvitationID, &tx.GuestID, &tx.Gateway, &tx.GatewayReference, &tx.Amount, &tx.Status, &tx.SenderName, &tx.Message, &tx.CreatedAt)
	if err != nil {
		return nil, err
	}
	return tx, nil
}
func (s *PostgresStore) ListTemplates() []*Template {
	rows, err := s.db.Query(`SELECT ` + templateColumns + ` FROM templates WHERE status = 'active' ORDER BY sort_order,name`)
	if err != nil {
		return []*Template{}
	}
	defer rows.Close()
	items := make([]*Template, 0)
	for rows.Next() {
		if item, err := scanTemplate(rows); err == nil {
			items = append(items, item)
		}
	}
	if err := rows.Err(); err != nil || len(items) == 0 {
		return []*Template{}
	}
	return items
}

func scanTemplate(row interface{ Scan(...any) error }) (*Template, error) {
	item := &Template{}
	var tags []byte
	err := row.Scan(&item.ID, &item.Name, &item.Slug, &item.Description, &item.EventType, &item.Category, &tags, &item.PreviewImage, &item.PreviewURL, &item.Premium, &item.Price, &item.Tier, &item.SupportsPhoto, &item.SupportsMusic, &item.SupportsRSVP, &item.SupportsGift, &item.SortOrder, &item.Status, &item.CreatedAt, &item.UpdatedAt)
	if err == nil {
		_ = json.Unmarshal(tags, &item.Tags)
	}
	return item, err
}

const templateColumns = `id,name,slug,description,event_type,category,tags,COALESCE(preview_image,''),preview_url,is_premium,price,tier,supports_photo,supports_music,supports_rsvp,supports_gift,sort_order,status,created_at,updated_at`

func (s *PostgresStore) ListTemplatesAdmin() []*Template {
	rows, err := s.db.Query(`SELECT ` + templateColumns + ` FROM templates ORDER BY sort_order,name`)
	if err != nil {
		return []*Template{}
	}
	defer rows.Close()
	items := make([]*Template, 0)
	for rows.Next() {
		if item, err := scanTemplate(rows); err == nil {
			items = append(items, item)
		}
	}
	return items
}

func (s *PostgresStore) FindTemplate(id string) (*Template, bool) {
	item, err := scanTemplate(s.db.QueryRow(`SELECT `+templateColumns+` FROM templates WHERE id=$1`, id))
	return item, err == nil
}

func (s *PostgresStore) FindTemplateBySlug(slug string) (*Template, bool) {
	item, err := scanTemplate(s.db.QueryRow(`SELECT `+templateColumns+` FROM templates WHERE slug=$1`, slug))
	return item, err == nil
}

func (s *PostgresStore) CreateTemplate(item Template) (*Template, error) {
	tags, _ := json.Marshal(item.Tags)
	created := &Template{}
	err := s.db.QueryRow(`INSERT INTO templates (id,name,slug,description,event_type,category,tags,preview_image,preview_url,is_premium,price,tier,supports_photo,supports_music,supports_rsvp,supports_gift,sort_order,status) VALUES (COALESCE(NULLIF($1,''),gen_random_uuid()::text),$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13,$14,$15,$16,$17,$18) RETURNING `+templateColumns, item.ID, item.Name, item.Slug, item.Description, item.EventType, item.Category, tags, item.PreviewImage, item.PreviewURL, item.Premium, item.Price, item.Tier, item.SupportsPhoto, item.SupportsMusic, item.SupportsRSVP, item.SupportsGift, item.SortOrder, item.Status).Scan(&created.ID, &created.Name, &created.Slug, &created.Description, &created.EventType, &created.Category, &tags, &created.PreviewImage, &created.PreviewURL, &created.Premium, &created.Price, &created.Tier, &created.SupportsPhoto, &created.SupportsMusic, &created.SupportsRSVP, &created.SupportsGift, &created.SortOrder, &created.Status, &created.CreatedAt, &created.UpdatedAt)
	if err != nil {
		return nil, err
	}
	_ = json.Unmarshal(tags, &created.Tags)
	return created, nil
}

func (s *PostgresStore) UpdateTemplate(item Template) (*Template, error) {
	tags, _ := json.Marshal(item.Tags)
	updated := &Template{}
	err := s.db.QueryRow(`UPDATE templates SET name=$2,slug=$3,description=$4,event_type=$5,category=$6,tags=$7,preview_image=$8,preview_url=$9,is_premium=$10,price=$11,tier=$12,supports_photo=$13,supports_music=$14,supports_rsvp=$15,supports_gift=$16,sort_order=$17,status=$18,updated_at=NOW() WHERE id=$1 RETURNING `+templateColumns, item.ID, item.Name, item.Slug, item.Description, item.EventType, item.Category, tags, item.PreviewImage, item.PreviewURL, item.Premium, item.Price, item.Tier, item.SupportsPhoto, item.SupportsMusic, item.SupportsRSVP, item.SupportsGift, item.SortOrder, item.Status).Scan(&updated.ID, &updated.Name, &updated.Slug, &updated.Description, &updated.EventType, &updated.Category, &tags, &updated.PreviewImage, &updated.PreviewURL, &updated.Premium, &updated.Price, &updated.Tier, &updated.SupportsPhoto, &updated.SupportsMusic, &updated.SupportsRSVP, &updated.SupportsGift, &updated.SortOrder, &updated.Status, &updated.CreatedAt, &updated.UpdatedAt)
	if err != nil {
		return nil, err
	}
	_ = json.Unmarshal(tags, &updated.Tags)
	return updated, nil
}

func (s *PostgresStore) DeleteTemplate(id string) error {
	result, err := s.db.Exec(`DELETE FROM templates WHERE id=$1`, id)
	if err != nil {
		return err
	}
	count, _ := result.RowsAffected()
	if count == 0 {
		return fmt.Errorf("template not found")
	}
	return nil
}

func (s *PostgresStore) SeedTemplates() {
	// Catalog data is owned by migrations, not runtime constructors.
}

func (s *PostgresStore) AssignTemplate(invitationID, templateID string) error {
	result, err := s.db.Exec(`UPDATE invitations SET template_id = $1 WHERE id = $2`, templateID, invitationID)
	if err != nil {
		return err
	}
	count, _ := result.RowsAffected()
	if count == 0 {
		return fmt.Errorf("invitation not found")
	}
	return nil
}

func (s *PostgresStore) GetSettings(invitationID string) map[string]any {
	settings := map[string]any{
		"theme": "classic", "primary_color": "#d97706", "secondary_color": "#f59e0b",
		"font": "poppins", "music_url": "", "autoplay_music": false,
		"opening_text": "", "closing_text": "", "cover_image": "", "sections_config": []any{},
	}
	var theme, primaryColor, secondaryColor, font, musicURL, openingText, closingText, coverImage string
	var autoplay bool
	var sectionsConfig []byte
	err := s.db.QueryRow(`SELECT theme, primary_color, secondary_color, font, COALESCE(music_url,''), autoplay_music, COALESCE(opening_text,''), COALESCE(closing_text,''), COALESCE(cover_image,''), COALESCE(sections_config,'[]'::jsonb) FROM invitation_settings WHERE invitation_id = $1`, invitationID).
		Scan(&theme, &primaryColor, &secondaryColor, &font, &musicURL, &autoplay, &openingText, &closingText, &coverImage, &sectionsConfig)
	if err == nil {
		settings["theme"], settings["primary_color"], settings["secondary_color"] = theme, primaryColor, secondaryColor
		settings["font"], settings["music_url"], settings["autoplay_music"] = font, musicURL, autoplay
		settings["opening_text"], settings["closing_text"], settings["cover_image"] = openingText, closingText, coverImage
		var sc any
		if json.Unmarshal(sectionsConfig, &sc) == nil {
			settings["sections_config"] = sc
		}
	}
	return settings
}

func (s *PostgresStore) UpdateSettings(invitationID string, settings map[string]any) map[string]any {
	current := s.GetSettings(invitationID)
	for key, value := range settings {
		current[key] = value
	}
	sectionsConfigJSON, err := json.Marshal(current["sections_config"])
	if err != nil {
		sectionsConfigJSON = []byte("[]")
	}
	_, _ = s.db.Exec(`INSERT INTO invitation_settings (invitation_id, theme, primary_color, secondary_color, font, music_url, autoplay_music, opening_text, closing_text, cover_image, sections_config)
		VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11)
		ON CONFLICT (invitation_id) DO UPDATE SET
			theme=EXCLUDED.theme, primary_color=EXCLUDED.primary_color, secondary_color=EXCLUDED.secondary_color,
			font=EXCLUDED.font, music_url=EXCLUDED.music_url, autoplay_music=EXCLUDED.autoplay_music,
			opening_text=EXCLUDED.opening_text, closing_text=EXCLUDED.closing_text,
			cover_image=EXCLUDED.cover_image, sections_config=EXCLUDED.sections_config`,
		invitationID, current["theme"], current["primary_color"], current["secondary_color"],
		current["font"], current["music_url"], current["autoplay_music"],
		current["opening_text"], current["closing_text"], current["cover_image"], sectionsConfigJSON)
	return current
}

func (s *PostgresStore) CreateStory(invitationID, title, content string) (map[string]any, error) {
	story := map[string]any{}
	var id string
	var order int
	err := s.db.QueryRow(`INSERT INTO stories (id, invitation_id, title, content, sort_order) VALUES (gen_random_uuid()::text, $1, $2, $3, (SELECT COUNT(*) FROM stories WHERE invitation_id = $1)) RETURNING id, sort_order`, invitationID, title, content).Scan(&id, &order)
	if err != nil {
		return nil, fmt.Errorf("create story: %w", err)
	}
	story["id"], story["sort_order"], story["invitation_id"], story["title"], story["content"] = id, order, invitationID, title, content
	return story, nil
}

func (s *PostgresStore) ListStories(invitationID string) []map[string]any {
	rows, err := s.db.Query(`SELECT id, invitation_id, COALESCE(title, ''), content, sort_order FROM stories WHERE invitation_id = $1 ORDER BY sort_order`, invitationID)
	if err != nil {
		return []map[string]any{}
	}
	defer rows.Close()
	items := []map[string]any{}
	for rows.Next() {
		var id, inviteID, title, content string
		var order int
		if rows.Scan(&id, &inviteID, &title, &content, &order) == nil {
			items = append(items, map[string]any{"id": id, "invitation_id": inviteID, "title": title, "content": content, "sort_order": order})
		}
	}
	if err := rows.Err(); err != nil {
		return []map[string]any{}
	}
	return items
}

func (s *PostgresStore) CreateGallery(invitationID, imageURL, caption string) (map[string]any, error) {
	image := map[string]any{}
	var id string
	var order int
	err := s.db.QueryRow(`INSERT INTO galleries (id, invitation_id, image_url, caption, sort_order) VALUES (gen_random_uuid()::text, $1, $2, $3, (SELECT COUNT(*) FROM galleries WHERE invitation_id = $1)) RETURNING id, sort_order`, invitationID, imageURL, caption).Scan(&id, &order)
	if err != nil {
		return nil, fmt.Errorf("create gallery: %w", err)
	}
	image["id"], image["sort_order"], image["invitation_id"], image["image_url"], image["caption"] = id, order, invitationID, imageURL, caption
	return image, nil
}

func (s *PostgresStore) ListGallery(invitationID string) []map[string]any {
	rows, err := s.db.Query(`SELECT id, invitation_id, image_url, COALESCE(caption, ''), sort_order FROM galleries WHERE invitation_id = $1 ORDER BY sort_order`, invitationID)
	if err != nil {
		return []map[string]any{}
	}
	defer rows.Close()
	items := []map[string]any{}
	for rows.Next() {
		var id, inviteID, imageURL, caption string
		var order int
		if rows.Scan(&id, &inviteID, &imageURL, &caption, &order) == nil {
			items = append(items, map[string]any{"id": id, "invitation_id": inviteID, "image_url": imageURL, "caption": caption, "sort_order": order})
		}
	}
	if err := rows.Err(); err != nil {
		return []map[string]any{}
	}
	return items
}

func (s *PostgresStore) CreateBroadcastLog(invitationID, guestID, message, status string) (map[string]any, error) {
	item := map[string]any{}
	var id string
	err := s.db.QueryRow(`INSERT INTO broadcast_logs (id, invitation_id, guest_id, message_snapshot, status) VALUES (gen_random_uuid()::text, $1, NULLIF($2, ''), $3, $4) RETURNING id`, invitationID, guestID, message, status).Scan(&id)
	if err != nil {
		return nil, fmt.Errorf("create broadcast log: %w", err)
	}
	item["id"], item["status"], item["invitation_id"], item["guest_id"], item["channel"], item["message"] = id, status, invitationID, guestID, "whatsapp", message
	return item, nil
}

func (s *PostgresStore) ListBroadcastLogs(invitationID string) []map[string]any {
	rows, err := s.db.Query(`SELECT id, invitation_id, COALESCE(guest_id, ''), channel, status, COALESCE(message_snapshot, '') FROM broadcast_logs WHERE invitation_id = $1 ORDER BY created_at DESC`, invitationID)
	if err != nil {
		return []map[string]any{}
	}
	defer rows.Close()
	items := []map[string]any{}
	for rows.Next() {
		var id, inviteID, guestID, channel, status, message string
		if rows.Scan(&id, &inviteID, &guestID, &channel, &status, &message) == nil {
			items = append(items, map[string]any{"id": id, "invitation_id": inviteID, "guest_id": guestID, "channel": channel, "status": status, "message": message})
		}
	}
	if err := rows.Err(); err != nil {
		return []map[string]any{}
	}
	return items
}

func (s *PostgresStore) LatestBroadcastLogForGuest(invitationID, guestID string) (map[string]any, bool) {
	item := map[string]any{}
	var id, status, message string
	err := s.db.QueryRow(`SELECT id, status, COALESCE(message_snapshot, '') FROM broadcast_logs WHERE invitation_id = $1 AND guest_id = $2 ORDER BY created_at DESC LIMIT 1`, invitationID, guestID).Scan(&id, &status, &message)
	if err != nil {
		return nil, false
	}
	item["id"], item["invitation_id"], item["guest_id"], item["channel"], item["status"], item["message"] = id, invitationID, guestID, "whatsapp", status, message
	return item, true
}

func (s *PostgresStore) UpdateBroadcastLogStatus(id, status string) (map[string]any, error) {
	item := map[string]any{}
	var invitationID, guestID, message string
	err := s.db.QueryRow(`UPDATE broadcast_logs SET status = $1, sent_at = CASE WHEN $1 = 'sent' THEN NOW() ELSE sent_at END WHERE id = $2 RETURNING invitation_id, COALESCE(guest_id, ''), COALESCE(message_snapshot, '')`, status, id).Scan(&invitationID, &guestID, &message)
	if err != nil {
		return nil, fmt.Errorf("update broadcast log: %w", err)
	}
	item["id"], item["invitation_id"], item["guest_id"], item["channel"], item["status"], item["message"] = id, invitationID, guestID, "whatsapp", status, message
	return item, nil
}

func (s *PostgresStore) CreateMedia(invitationID, mediaType, path, mime string, size int64) (map[string]any, error) {
	item := map[string]any{}
	var id string
	err := s.db.QueryRow(`INSERT INTO media (id, invitation_id, type, path, mime_type, size_bytes) VALUES (gen_random_uuid()::text, $1, $2, $3, $4, $5) RETURNING id`, invitationID, mediaType, path, mime, size).Scan(&id)
	if err != nil {
		return nil, fmt.Errorf("create media: %w", err)
	}
	item["id"], item["invitation_id"], item["type"], item["path"], item["mime_type"], item["size_bytes"] = id, invitationID, mediaType, path, mime, size
	return item, nil
}

func (s *PostgresStore) ListMedia(invitationID string) []map[string]any {
	rows, err := s.db.Query(`SELECT id, invitation_id, type, path, COALESCE(mime_type, ''), COALESCE(size_bytes, 0) FROM media WHERE invitation_id = $1 ORDER BY created_at DESC`, invitationID)
	if err != nil {
		return []map[string]any{}
	}
	defer rows.Close()
	items := []map[string]any{}
	for rows.Next() {
		var id, inviteID, mediaType, path, mime string
		var size int64
		if rows.Scan(&id, &inviteID, &mediaType, &path, &mime, &size) == nil {
			items = append(items, map[string]any{"id": id, "invitation_id": inviteID, "type": mediaType, "path": path, "mime_type": mime, "size_bytes": size})
		}
	}
	if err := rows.Err(); err != nil {
		return []map[string]any{}
	}
	return items
}

func (s *PostgresStore) FindMedia(id string) (map[string]any, bool) {
	item := map[string]any{}
	var invitationID, mediaType, path, mime string
	var size int64
	err := s.db.QueryRow(`SELECT invitation_id, type, path, COALESCE(mime_type, ''), COALESCE(size_bytes, 0) FROM media WHERE id = $1`, id).Scan(&invitationID, &mediaType, &path, &mime, &size)
	if err != nil {
		return nil, false
	}
	item["id"], item["invitation_id"], item["type"], item["path"], item["mime_type"], item["size_bytes"] = id, invitationID, mediaType, path, mime, size
	return item, true
}

func (s *PostgresStore) DeleteMedia(id string) error {
	result, err := s.db.Exec(`DELETE FROM media WHERE id = $1`, id)
	if err != nil {
		return err
	}
	if count, _ := result.RowsAffected(); count == 0 {
		return fmt.Errorf("media not found")
	}
	return nil
}

func (s *PostgresStore) SeedPlans() {
	// Catalog data is owned by migrations, not runtime constructors.
}

func (s *PostgresStore) ListPlans() []*Plan {
	rows, err := s.db.Query(`SELECT id, name, max_guests, has_watermark, custom_domain_allowed, payment_gateway_allowed, premium_templates_allowed, price, duration_days FROM plans ORDER BY price ASC`)
	if err != nil {
		return []*Plan{}
	}
	defer rows.Close()
	items := make([]*Plan, 0)
	for rows.Next() {
		item := &Plan{}
		var durationDays sql.NullInt64
		if rows.Scan(&item.ID, &item.Name, &item.MaxGuests, &item.HasWatermark, &item.CustomDomainAllowed, &item.PaymentGatewayAllowed, &item.PremiumTemplatesAllowed, &item.Price, &durationDays) == nil {
			if durationDays.Valid {
				days := int(durationDays.Int64)
				item.DurationDays = &days
			}
			items = append(items, item)
		}
	}
	if err := rows.Err(); err != nil || len(items) == 0 {
		return []*Plan{}
	}
	return items
}

func (s *PostgresStore) GetSiteContent(section string) map[string]any {
	var raw []byte
	if err := s.db.QueryRow(`SELECT data FROM site_content WHERE section = $1`, section).Scan(&raw); err != nil {
		return map[string]any{}
	}
	data := map[string]any{}
	if err := json.Unmarshal(raw, &data); err != nil {
		return map[string]any{}
	}
	return data
}

func (s *PostgresStore) UpdateSiteContent(section string, data map[string]any) map[string]any {
	current := s.GetSiteContent(section)
	for key, value := range data {
		current[key] = value
	}
	payload, err := json.Marshal(current)
	if err != nil {
		payload = []byte("{}")
	}
	_, _ = s.db.Exec(`INSERT INTO site_content (section, data, updated_at) VALUES ($1, $2, NOW()) ON CONFLICT (section) DO UPDATE SET data = EXCLUDED.data, updated_at = NOW()`, section, payload)
	return current
}

func (s *PostgresStore) ListFeatures() []map[string]any {
	rows, err := s.db.Query(`SELECT id, title, description, COALESCE(icon, ''), sort_order FROM features ORDER BY sort_order`)
	if err != nil {
		return []map[string]any{}
	}
	defer rows.Close()
	items := []map[string]any{}
	for rows.Next() {
		var id, title, description, icon string
		var order int
		if rows.Scan(&id, &title, &description, &icon, &order) == nil {
			items = append(items, map[string]any{"id": id, "title": title, "description": description, "icon": icon, "sort_order": order})
		}
	}
	if err := rows.Err(); err != nil {
		return []map[string]any{}
	}
	return items
}

func (s *PostgresStore) CreateFeature(title, description, icon string) (map[string]any, error) {
	var id string
	var order int
	err := s.db.QueryRow(`INSERT INTO features (id, title, description, icon, sort_order) VALUES (gen_random_uuid()::text, $1, $2, $3, (SELECT COUNT(*) FROM features)) RETURNING id, sort_order`, title, description, icon).Scan(&id, &order)
	if err != nil {
		return nil, fmt.Errorf("create feature: %w", err)
	}
	return map[string]any{"id": id, "title": title, "description": description, "icon": icon, "sort_order": order}, nil
}

func (s *PostgresStore) DeleteFeature(id string) error {
	result, err := s.db.Exec(`DELETE FROM features WHERE id = $1`, id)
	if err != nil {
		return err
	}
	count, _ := result.RowsAffected()
	if count == 0 {
		return fmt.Errorf("feature not found")
	}
	return nil
}

func (s *PostgresStore) ListTestimonials() []map[string]any {
	rows, err := s.db.Query(`SELECT id, name, COALESCE(role, ''), quote, COALESCE(avatar_url, ''), sort_order FROM testimonials ORDER BY sort_order`)
	if err != nil {
		return []map[string]any{}
	}
	defer rows.Close()
	items := []map[string]any{}
	for rows.Next() {
		var id, name, role, quote, avatarURL string
		var order int
		if rows.Scan(&id, &name, &role, &quote, &avatarURL, &order) == nil {
			items = append(items, map[string]any{"id": id, "name": name, "role": role, "quote": quote, "avatar_url": avatarURL, "sort_order": order})
		}
	}
	if err := rows.Err(); err != nil {
		return []map[string]any{}
	}
	return items
}

func (s *PostgresStore) CreateTestimonial(name, role, quote, avatarURL string) (map[string]any, error) {
	var id string
	var order int
	err := s.db.QueryRow(`INSERT INTO testimonials (id, name, role, quote, avatar_url, sort_order) VALUES (gen_random_uuid()::text, $1, $2, $3, $4, (SELECT COUNT(*) FROM testimonials)) RETURNING id, sort_order`, name, role, quote, avatarURL).Scan(&id, &order)
	if err != nil {
		return nil, fmt.Errorf("create testimonial: %w", err)
	}
	return map[string]any{"id": id, "name": name, "role": role, "quote": quote, "avatar_url": avatarURL, "sort_order": order}, nil
}

func (s *PostgresStore) DeleteTestimonial(id string) error {
	result, err := s.db.Exec(`DELETE FROM testimonials WHERE id = $1`, id)
	if err != nil {
		return err
	}
	count, _ := result.RowsAffected()
	if count == 0 {
		return fmt.Errorf("testimonial not found")
	}
	return nil
}

func (s *PostgresStore) SetUserPlan(userID, planID string) error {
	result, err := s.db.Exec(`UPDATE users SET plan_id = $1 WHERE id = $2`, planID, userID)
	if err != nil {
		return err
	}
	count, _ := result.RowsAffected()
	if count == 0 {
		return fmt.Errorf("user not found")
	}
	return nil
}

func (s *PostgresStore) GetUserPlan(userID string) (*Plan, error) {
	var planID sql.NullString
	if err := s.db.QueryRow(`SELECT plan_id FROM users WHERE id = $1`, userID).Scan(&planID); err != nil {
		return nil, fmt.Errorf("user not found")
	}
	id := "free"
	if planID.Valid && planID.String != "" {
		id = planID.String
	}
	plan := &Plan{}
	var durationDays sql.NullInt64
	err := s.db.QueryRow(`SELECT id, name, max_guests, has_watermark, custom_domain_allowed, payment_gateway_allowed, premium_templates_allowed, price, duration_days FROM plans WHERE id = $1`, id).
		Scan(&plan.ID, &plan.Name, &plan.MaxGuests, &plan.HasWatermark, &plan.CustomDomainAllowed, &plan.PaymentGatewayAllowed, &plan.PremiumTemplatesAllowed, &plan.Price, &durationDays)
	if err != nil {
		return nil, fmt.Errorf("plan not found: %w", err)
	}
	if durationDays.Valid {
		days := int(durationDays.Int64)
		plan.DurationDays = &days
	}
	return plan, nil
}

func (s *PostgresStore) CreateSubscription(sub Subscription) (*Subscription, error) {
	created := sub
	err := s.db.QueryRow(`INSERT INTO subscriptions (user_id, plan_id, status, provider, provider_reference, ends_at) VALUES ($1,$2,$3,$4,NULLIF($5,''),$6) RETURNING id, started_at`, sub.UserID, sub.PlanID, sub.Status, sub.Provider, sub.ProviderReference, sub.EndsAt).Scan(&created.ID, &created.StartedAt)
	if err != nil {
		return nil, err
	}
	return &created, nil
}

func scanSubscription(row interface{ Scan(...any) error }) (*Subscription, error) {
	sub := &Subscription{}
	err := row.Scan(&sub.ID, &sub.UserID, &sub.PlanID, &sub.Status, &sub.Provider, &sub.ProviderReference, &sub.StartedAt, &sub.EndsAt)
	return sub, err
}

func (s *PostgresStore) FindSubscriptionByReference(reference string) (*Subscription, bool) {
	sub, err := scanSubscription(s.db.QueryRow(`SELECT id,user_id,plan_id,status,COALESCE(provider,''),COALESCE(provider_reference,''),started_at,ends_at FROM subscriptions WHERE provider_reference=$1`, reference))
	return sub, err == nil
}

func (s *PostgresStore) GetActiveSubscription(userID string) (*Subscription, error) {
	return scanSubscription(s.db.QueryRow(`SELECT id,user_id,plan_id,status,COALESCE(provider,''),COALESCE(provider_reference,''),started_at,ends_at FROM subscriptions WHERE user_id=$1 AND status='active' ORDER BY started_at DESC LIMIT 1`, userID))
}

func (s *PostgresStore) UpdateSubscriptionStatus(id, status string) (*Subscription, error) {
	return scanSubscription(s.db.QueryRow(`UPDATE subscriptions SET status=$1 WHERE id=$2 RETURNING id,user_id,plan_id,status,COALESCE(provider,''),COALESCE(provider_reference,''),started_at,ends_at`, status, id))
}

func (s *PostgresStore) CancelActiveSubscriptions(userID string) error {
	_, err := s.db.Exec(`UPDATE subscriptions SET status='cancelled' WHERE user_id=$1 AND status='active'`, userID)
	return err
}

func (s *PostgresStore) ListSubscriptions(userID string) []*Subscription {
	rows, err := s.db.Query(`SELECT id,user_id,plan_id,status,COALESCE(provider,''),COALESCE(provider_reference,''),started_at,ends_at FROM subscriptions WHERE user_id=$1 ORDER BY started_at DESC`, userID)
	if err != nil {
		return []*Subscription{}
	}
	defer rows.Close()
	items := make([]*Subscription, 0)
	for rows.Next() {
		sub := &Subscription{}
		if rows.Scan(&sub.ID, &sub.UserID, &sub.PlanID, &sub.Status, &sub.Provider, &sub.ProviderReference, &sub.StartedAt, &sub.EndsAt) == nil {
			items = append(items, sub)
		}
	}
	return items
}

func (s *PostgresStore) CreateInvoice(invoice Invoice) (*Invoice, error) {
	created := invoice
	err := s.db.QueryRow(`INSERT INTO invoices (user_id, subscription_id, invoice_number, amount, status, paid_at) VALUES ($1,$2,$3,$4,$5,$6) RETURNING id,issued_at`, invoice.UserID, invoice.SubscriptionID, invoice.InvoiceNumber, invoice.Amount, invoice.Status, invoice.PaidAt).Scan(&created.ID, &created.IssuedAt)
	if err != nil {
		return nil, err
	}
	return &created, nil
}

func (s *PostgresStore) ListInvoices(userID string) []*Invoice {
	rows, err := s.db.Query(`SELECT id,user_id,subscription_id,invoice_number,amount,status,issued_at,paid_at FROM invoices WHERE user_id=$1 ORDER BY issued_at DESC`, userID)
	if err != nil {
		return []*Invoice{}
	}
	defer rows.Close()
	items := make([]*Invoice, 0)
	for rows.Next() {
		invoice := &Invoice{}
		if rows.Scan(&invoice.ID, &invoice.UserID, &invoice.SubscriptionID, &invoice.InvoiceNumber, &invoice.Amount, &invoice.Status, &invoice.IssuedAt, &invoice.PaidAt) == nil {
			items = append(items, invoice)
		}
	}
	return items
}

func (s *PostgresStore) GetUserEntitlement(userID, feature string) (*Entitlement, bool) {
	var raw []byte
	var expiresAt sql.NullTime
	err := s.db.QueryRow(`SELECT value, expires_at FROM user_entitlements WHERE user_id=$1 AND feature=$2 AND (expires_at IS NULL OR expires_at > NOW())`, userID, feature).Scan(&raw, &expiresAt)
	if err != nil {
		return nil, false
	}
	item := &Entitlement{UserID: userID, Feature: feature, Enabled: true}
	if err := json.Unmarshal(raw, &item.Enabled); err != nil {
		item.Enabled = true
	}
	if expiresAt.Valid {
		item.ExpiresAt = &expiresAt.Time
	}
	return item, true
}

func (s *PostgresStore) SetUserEntitlement(item Entitlement) error {
	value, err := json.Marshal(item.Enabled)
	if err != nil {
		return err
	}
	_, err = s.db.Exec(`INSERT INTO user_entitlements (user_id, feature, value, expires_at) VALUES ($1,$2,$3,$4) ON CONFLICT (user_id,feature) DO UPDATE SET value=EXCLUDED.value, expires_at=EXCLUDED.expires_at`, item.UserID, item.Feature, value, item.ExpiresAt)
	return err
}

func (s *PostgresStore) CreateCustomDomain(domain CustomDomain) (*CustomDomain, error) {
	created := domain
	err := s.db.QueryRow(`INSERT INTO custom_domains (user_id, invitation_id, domain, verification_token) VALUES ($1,$2,$3,$4) RETURNING id, status, created_at`, domain.UserID, domain.InvitationID, domain.Domain, domain.VerificationToken).Scan(&created.ID, &created.Status, &created.CreatedAt)
	if err != nil {
		return nil, err
	}
	return &created, nil
}

func (s *PostgresStore) ListCustomDomains(invitationID string) []*CustomDomain {
	rows, err := s.db.Query(`SELECT id,user_id,invitation_id,domain,COALESCE(verification_token,''),status,verified_at,created_at FROM custom_domains WHERE invitation_id=$1 ORDER BY created_at DESC`, invitationID)
	if err != nil {
		return []*CustomDomain{}
	}
	defer rows.Close()
	items := make([]*CustomDomain, 0)
	for rows.Next() {
		item := &CustomDomain{}
		if rows.Scan(&item.ID, &item.UserID, &item.InvitationID, &item.Domain, &item.VerificationToken, &item.Status, &item.VerifiedAt, &item.CreatedAt) == nil {
			items = append(items, item)
		}
	}
	return items
}

func (s *PostgresStore) FindInvitationByCustomDomain(domain string) (*Invitation, bool) {
	inv := &Invitation{}
	err := s.db.QueryRow(`SELECT i.id,i.user_id,i.slug,i.title,i.published,i.created_at FROM invitations i JOIN custom_domains d ON d.invitation_id=i.id WHERE d.domain=$1 AND d.status='verified'`, domain).Scan(&inv.ID, &inv.UserID, &inv.Slug, &inv.Title, &inv.Published, &inv.CreatedAt)
	if err != nil {
		return nil, false
	}
	return s.FindInvitationByID(inv.ID)
}

func (s *PostgresStore) VerifyCustomDomain(id, userID, token string) (*CustomDomain, error) {
	item := &CustomDomain{}
	err := s.db.QueryRow(`UPDATE custom_domains SET status='verified', verified_at=NOW() WHERE id=$1 AND user_id=$2 AND verification_token=$3 RETURNING id,user_id,invitation_id,domain,COALESCE(verification_token,''),status,verified_at,created_at`, id, userID, token).Scan(&item.ID, &item.UserID, &item.InvitationID, &item.Domain, &item.VerificationToken, &item.Status, &item.VerifiedAt, &item.CreatedAt)
	return item, err
}

func (s *PostgresStore) CreateAuditLog(userID, invitationID, action string, metadata map[string]any) error {
	metadataJSON, err := json.Marshal(metadata)
	if err != nil {
		metadataJSON = []byte("{}")
	}
	_, err = s.db.Exec(`INSERT INTO audit_logs (id, user_id, invitation_id, action, metadata) VALUES (gen_random_uuid()::text, $1, NULLIF($2, ''), $3, $4)`, userID, invitationID, action, metadataJSON)
	return err
}

func (s *PostgresStore) UpdateFeature(id, title, description, icon string) (map[string]any, error) {
	_, err := s.db.Exec(`UPDATE features SET title=COALESCE(NULLIF($2,''),title), description=COALESCE(NULLIF($3,''),description), icon=$4 WHERE id=$1`, id, title, description, icon)
	if err != nil {
		return nil, err
	}
	row := s.db.QueryRow(`SELECT id, title, description, icon FROM features WHERE id=$1`, id)
	m := map[string]any{}
	var fid, ftitle, fdesc, ficon string
	if err := row.Scan(&fid, &ftitle, &fdesc, &ficon); err != nil {
		return nil, err
	}
	m["id"], m["title"], m["description"], m["icon"] = fid, ftitle, fdesc, ficon
	return m, nil
}

func (s *PostgresStore) UpdateTestimonial(id, name, role, quote, avatarURL string) (map[string]any, error) {
	_, err := s.db.Exec(`UPDATE testimonials SET name=COALESCE(NULLIF($2,''),name), role=$3, quote=COALESCE(NULLIF($4,''),quote), avatar_url=$5 WHERE id=$1`, id, name, role, quote, avatarURL)
	if err != nil {
		return nil, err
	}
	row := s.db.QueryRow(`SELECT id, name, role, quote, avatar_url FROM testimonials WHERE id=$1`, id)
	m := map[string]any{}
	var tid, tname, trole, tquote, tavatar string
	if err := row.Scan(&tid, &tname, &trole, &tquote, &tavatar); err != nil {
		return nil, err
	}
	m["id"], m["name"], m["role"], m["quote"], m["avatar_url"] = tid, tname, trole, tquote, tavatar
	return m, nil
}

func (s *PostgresStore) CreateInvitationEvent(invitationID string, ev InvitationEvent) (*InvitationEvent, error) {
	result := &InvitationEvent{}
	err := s.db.QueryRow(
		`INSERT INTO invitation_events (id, invitation_id, title, type, event_date, start_time, end_time, venue, address, maps_url, latitude, longitude, sort_order)
		 VALUES (gen_random_uuid()::text,$1,$2,$3,$4,NULLIF($5,''),NULLIF($6,''),$7,NULLIF($8,''),NULLIF($9,''),$10,$11,$12)
		 RETURNING id, invitation_id, title, type, event_date, COALESCE(start_time,''), COALESCE(end_time,''), venue, COALESCE(address,''), COALESCE(maps_url,''), COALESCE(latitude,0), COALESCE(longitude,0), sort_order, created_at`,
		invitationID, ev.Title, ev.Type, ev.Date, ev.StartTime, ev.EndTime, ev.Venue, ev.Address, ev.MapsURL, ev.Latitude, ev.Longitude, ev.SortOrder,
	).Scan(&result.ID, &result.InvitationID, &result.Title, &result.Type, &result.Date, &result.StartTime, &result.EndTime, &result.Venue, &result.Address, &result.MapsURL, &result.Latitude, &result.Longitude, &result.SortOrder, &result.CreatedAt)
	if err != nil {
		return nil, fmt.Errorf("create invitation event: %w", err)
	}
	return result, nil
}

func (s *PostgresStore) ListInvitationEvents(invitationID string) []*InvitationEvent {
	rows, err := s.db.Query(`SELECT id, invitation_id, title, type, event_date, COALESCE(start_time,''), COALESCE(end_time,''), venue, COALESCE(address,''), COALESCE(maps_url,''), COALESCE(latitude,0), COALESCE(longitude,0), sort_order, created_at FROM invitation_events WHERE invitation_id=$1 ORDER BY sort_order ASC, created_at ASC`, invitationID)
	if err != nil {
		return []*InvitationEvent{}
	}
	defer rows.Close()
	result := make([]*InvitationEvent, 0)
	for rows.Next() {
		e := &InvitationEvent{}
		if err := rows.Scan(&e.ID, &e.InvitationID, &e.Title, &e.Type, &e.Date, &e.StartTime, &e.EndTime, &e.Venue, &e.Address, &e.MapsURL, &e.Latitude, &e.Longitude, &e.SortOrder, &e.CreatedAt); err != nil {
			continue
		}
		result = append(result, e)
	}
	return result
}

func (s *PostgresStore) UpdateInvitationEvent(id string, ev InvitationEvent) (*InvitationEvent, error) {
	result := &InvitationEvent{}
	err := s.db.QueryRow(
		`UPDATE invitation_events SET title=$2, type=$3, event_date=$4, start_time=NULLIF($5,''), end_time=NULLIF($6,''), venue=$7, address=NULLIF($8,''), maps_url=NULLIF($9,''), latitude=$10, longitude=$11, sort_order=$12
		 WHERE id=$1
		 RETURNING id, invitation_id, title, type, event_date, COALESCE(start_time,''), COALESCE(end_time,''), venue, COALESCE(address,''), COALESCE(maps_url,''), COALESCE(latitude,0), COALESCE(longitude,0), sort_order, created_at`,
		id, ev.Title, ev.Type, ev.Date, ev.StartTime, ev.EndTime, ev.Venue, ev.Address, ev.MapsURL, ev.Latitude, ev.Longitude, ev.SortOrder,
	).Scan(&result.ID, &result.InvitationID, &result.Title, &result.Type, &result.Date, &result.StartTime, &result.EndTime, &result.Venue, &result.Address, &result.MapsURL, &result.Latitude, &result.Longitude, &result.SortOrder, &result.CreatedAt)
	if err != nil {
		return nil, fmt.Errorf("event not found: %w", err)
	}
	return result, nil
}

func (s *PostgresStore) DeleteInvitationEvent(id string) error {
	_, err := s.db.Exec(`DELETE FROM invitation_events WHERE id=$1`, id)
	return err
}

func (s *PostgresStore) DeleteGalleryItem(id string) error {
	result, err := s.db.Exec(`DELETE FROM galleries WHERE id=$1`, id)
	if err != nil {
		return err
	}
	if n, _ := result.RowsAffected(); n == 0 {
		return fmt.Errorf("gallery item not found")
	}
	return nil
}

func (s *PostgresStore) FindGalleryItem(id string) (map[string]any, bool) {
	item := map[string]any{}
	var invitationID, imageURL, caption string
	var order int
	err := s.db.QueryRow(`SELECT invitation_id, image_url, COALESCE(caption, ''), sort_order FROM galleries WHERE id = $1`, id).Scan(&invitationID, &imageURL, &caption, &order)
	if err != nil {
		return nil, false
	}
	item["id"], item["invitation_id"], item["image_url"], item["caption"], item["sort_order"] = id, invitationID, imageURL, caption, order
	return item, true
}

func (s *PostgresStore) DeleteStoryItem(id string) error {
	result, err := s.db.Exec(`DELETE FROM stories WHERE id=$1`, id)
	if err != nil {
		return err
	}
	if n, _ := result.RowsAffected(); n == 0 {
		return fmt.Errorf("story not found")
	}
	return nil
}

func (s *PostgresStore) AdminListUsers() []*User {
	rows, err := s.db.Query(`SELECT id, name, email, password_hash, role, created_at FROM users ORDER BY created_at DESC`)
	if err != nil {
		return nil
	}
	defer rows.Close()
	var result []*User
	for rows.Next() {
		u := &User{}
		if err := rows.Scan(&u.ID, &u.Name, &u.Email, &u.Password, &u.Role, &u.CreatedAt); err != nil {
			continue
		}
		result = append(result, u)
	}
	return result
}

func (s *PostgresStore) AdminStats() map[string]any {
	stats := map[string]any{}
	var n int
	for _, q := range []struct {
		key string
		sql string
	}{
		{"total_users", `SELECT COUNT(*) FROM users`},
		{"total_invitations", `SELECT COUNT(*) FROM invitations`},
		{"published_invitations", `SELECT COUNT(*) FROM invitations WHERE published=true`},
		{"total_guests", `SELECT COUNT(*) FROM guests`},
		{"total_rsvps", `SELECT COUNT(*) FROM rsvps`},
		{"total_wishes", `SELECT COUNT(*) FROM wishes`},
	} {
		if err := s.db.QueryRow(q.sql).Scan(&n); err == nil {
			stats[q.key] = n
		}
	}
	return stats
}

func (s *PostgresStore) DuplicateInvitation(sourceID, newSlug, newTitle, userID string) (*Invitation, error) {
	tx, err := s.db.Begin()
	if err != nil {
		return nil, err
	}
	defer tx.Rollback() //nolint:errcheck

	var newID string
	err = tx.QueryRow(`
		INSERT INTO invitations (id, user_id, template_id, slug, title, published, updated_at)
		SELECT gen_random_uuid()::text, $1, template_id, $2, $3, false, NOW()
		FROM invitations WHERE id = $4
		RETURNING id`,
		userID, newSlug, newTitle, sourceID,
	).Scan(&newID)
	if err != nil {
		return nil, fmt.Errorf("duplicate invitation: %w", err)
	}

	// Copy couples (with all fields including schema_004 + schema_005 columns)
	_, _ = tx.Exec(`INSERT INTO couples (invitation_id, groom_name, bride_name, groom_nickname, bride_nickname, groom_photo, bride_photo, groom_parents, bride_parents)
		SELECT $1, groom_name, bride_name, groom_nickname, bride_nickname, groom_photo, bride_photo, groom_parents, bride_parents FROM couples WHERE invitation_id = $2`,
		newID, sourceID)

	// Copy legacy 1:1 event
	_, _ = tx.Exec(`INSERT INTO events (invitation_id, title, type, event_date, start_time, end_time, venue, address, maps_url)
		SELECT $1, title, type, event_date, start_time, end_time, venue, address, maps_url FROM events WHERE invitation_id = $2`,
		newID, sourceID)

	// Copy multi-events
	_, _ = tx.Exec(`INSERT INTO invitation_events (id, invitation_id, title, type, event_date, start_time, end_time, venue, address, maps_url, latitude, longitude, sort_order)
		SELECT gen_random_uuid()::text, $1, title, type, event_date, start_time, end_time, venue, address, maps_url, latitude, longitude, sort_order
		FROM invitation_events WHERE invitation_id = $2`,
		newID, sourceID)

	// Copy stories
	_, _ = tx.Exec(`INSERT INTO stories (id, invitation_id, title, content, sort_order)
		SELECT gen_random_uuid()::text, $1, title, content, sort_order FROM stories WHERE invitation_id = $2`,
		newID, sourceID)

	// Copy gallery
	_, _ = tx.Exec(`INSERT INTO galleries (id, invitation_id, image_url, caption, sort_order)
		SELECT gen_random_uuid()::text, $1, image_url, caption, sort_order FROM galleries WHERE invitation_id = $2`,
		newID, sourceID)

	// Copy gifts
	_, _ = tx.Exec(`INSERT INTO gifts (id, invitation_id, type, bank_name, account_number, account_name, ewallet_provider, ewallet_number, qris_image_url, address, is_active)
		SELECT gen_random_uuid()::text, $1, type, bank_name, account_number, account_name, ewallet_provider, ewallet_number, qris_image_url, address, is_active
		FROM gifts WHERE invitation_id = $2`,
		newID, sourceID)

	// Copy invitation_settings
	_, _ = tx.Exec(`INSERT INTO invitation_settings (invitation_id, theme, primary_color, secondary_color, font, music_url, autoplay_music, opening_text, closing_text, cover_image, sections_config)
		SELECT $1, theme, primary_color, secondary_color, font, music_url, autoplay_music, opening_text, closing_text, cover_image, sections_config
		FROM invitation_settings WHERE invitation_id = $2`,
		newID, sourceID)

	if err := tx.Commit(); err != nil {
		return nil, fmt.Errorf("commit duplicate: %w", err)
	}

	inv, exists := s.FindInvitationByID(newID)
	if !exists {
		return nil, fmt.Errorf("failed to retrieve duplicated invitation")
	}
	return inv, nil
}

func (s *PostgresStore) BulkDeleteGuests(invitationID string, guestIDs []string) error {
	if len(guestIDs) == 0 {
		return nil
	}
	placeholders := make([]string, len(guestIDs))
	args := make([]any, 0, len(guestIDs)+1)
	args = append(args, invitationID)
	for i, id := range guestIDs {
		placeholders[i] = fmt.Sprintf("$%d", i+2)
		args = append(args, id)
	}
	query := fmt.Sprintf(`DELETE FROM guests WHERE invitation_id = $1 AND id IN (%s)`, strings.Join(placeholders, ","))
	_, err := s.db.Exec(query, args...)
	return err
}

func (s *PostgresStore) ListGuestsFiltered(invitationID, search, category string) []*Guest {
	base := `SELECT id, invitation_id, name, phone, category, invitation_token, checked_in_at, checked_in_by, created_at FROM guests WHERE invitation_id = $1`
	args := []any{invitationID}
	if category != "" {
		args = append(args, category)
		base += fmt.Sprintf(" AND category = $%d", len(args))
	}
	if search != "" {
		args = append(args, "%"+strings.ToLower(search)+"%")
		base += fmt.Sprintf(" AND (LOWER(name) LIKE $%d OR phone LIKE $%d)", len(args), len(args))
	}
	base += " ORDER BY created_at DESC"
	rows, err := s.db.Query(base, args...)
	if err != nil {
		return []*Guest{}
	}
	defer rows.Close()
	items := make([]*Guest, 0)
	for rows.Next() {
		item := &Guest{}
		var checkedInBy sql.NullString
		if rows.Scan(&item.ID, &item.InvitationID, &item.Name, &item.Phone, &item.Category, &item.Token, &item.CheckedInAt, &checkedInBy, &item.CreatedAt) == nil {
			if checkedInBy.Valid {
				item.CheckedInBy = &checkedInBy.String
			}
			items = append(items, item)
		}
	}
	return items
}

func (s *PostgresStore) UpdateUserAvatar(userID, avatarURL string) (*User, error) {
	_, err := s.db.Exec(`UPDATE users SET avatar = $1 WHERE id = $2`, avatarURL, userID)
	if err != nil {
		return nil, fmt.Errorf("update avatar: %w", err)
	}
	user, ok := s.FindUserByID(userID)
	if !ok {
		return nil, fmt.Errorf("user not found")
	}
	return user, nil
}

var _ Store = (*PostgresStore)(nil)
