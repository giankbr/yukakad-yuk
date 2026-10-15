package api

import (
	"bytes"
	"context"
	"crypto/rand"
	"encoding/json"
	"io"
	"math/big"
	"net/http"
	"sort"
	"strings"
	"time"

	mediaservice "yukakad/internal/media"
	"yukakad/internal/store"
)

// Hari-H & after-event features: buku buwuh, venue screen feed, doorprize, guest photos,
// wishlist crowdfunding and the public recap.

// objectUploader is the part of object storage the guest photo upload needs (fakeable in tests).
type objectUploader interface {
	Upload(ctx context.Context, key string, r io.Reader, size int64, contentType string) (string, error)
}

// SetPhotoUploader overrides where guest photos are stored (local development without MinIO).
func (s *Server) SetPhotoUploader(u objectUploader) { s.photoStore = u }

func sectionsConfig(settings map[string]any) map[string]any {
	sections, _ := settings["sections_config"].(map[string]any)
	if sections == nil {
		return map[string]any{}
	}
	return sections
}

func sectionOn(settings map[string]any, key string) (bool, map[string]any) {
	cfg, _ := sectionsConfig(settings)[key].(map[string]any)
	if cfg == nil {
		return false, nil
	}
	enabled, _ := cfg["enabled"].(bool)
	return enabled, cfg
}

func trimTo(value string, max int) string {
	value = strings.TrimSpace(value)
	if len([]rune(value)) > max {
		value = string([]rune(value)[:max])
	}
	return value
}

/* ── 1. Buku buwuh ─────────────────────────────────────────────── */

var ledgerKinds = map[string]bool{"cash": true, "transfer": true, "kado": true}

type ledgerPayload struct {
	GuestID string  `json:"guest_id"`
	Name    string  `json:"name"`
	Kind    string  `json:"kind"`
	Amount  float64 `json:"amount"`
	Item    string  `json:"item"`
	Note    string  `json:"note"`
}

func (p ledgerPayload) entry(invitationID string) (store.LedgerEntry, bool) {
	entry := store.LedgerEntry{InvitationID: invitationID, GuestID: strings.TrimSpace(p.GuestID), Name: trimTo(p.Name, 120), Kind: p.Kind, Amount: p.Amount, Item: trimTo(p.Item, 160), Note: trimTo(p.Note, 300)}
	if entry.Kind == "" {
		entry.Kind = "cash"
	}
	valid := entry.Name != "" && ledgerKinds[entry.Kind] && entry.Amount >= 0 && entry.Amount <= 10_000_000_000
	if entry.Kind == "kado" && entry.Item == "" && entry.Amount == 0 {
		valid = false
	}
	// A sealed envelope can be logged at the door (amount 0) and filled in after it is opened.
	if entry.Kind == "transfer" && entry.Amount <= 0 {
		valid = false
	}
	return entry, valid
}

// GET/POST /api/invitations/{id}/ledger, PATCH/DELETE /api/invitations/{id}/ledger/{entryId}
func (s *Server) handleLedger(w http.ResponseWriter, r *http.Request, invitationID, entryID string) {
	invitation, userID, ok := s.ownedInvitation(w, r, invitationID)
	if !ok {
		return
	}
	switch {
	case entryID == "" && r.Method == http.MethodGet:
		s.writeLedger(w, invitation.ID)
	case entryID == "" && r.Method == http.MethodPost, entryID != "" && (r.Method == http.MethodPatch || r.Method == http.MethodPut):
		var payload ledgerPayload
		if json.NewDecoder(http.MaxBytesReader(w, r.Body, 8192)).Decode(&payload) != nil {
			writeJSON(w, http.StatusBadRequest, map[string]string{"error": "invalid payload"})
			return
		}
		entry, valid := payload.entry(invitation.ID)
		if !valid {
			writeJSON(w, http.StatusBadRequest, map[string]string{"error": "nama, jenis, dan nominal/barang wajib diisi"})
			return
		}
		if entry.GuestID != "" {
			if guest, found := s.store.FindGuestByID(entry.GuestID); !found || guest.InvitationID != invitation.ID {
				writeJSON(w, http.StatusBadRequest, map[string]string{"error": "guest not found"})
				return
			}
		}
		var saved *store.LedgerEntry
		var err error
		status := http.StatusCreated
		if entryID == "" {
			entry.RecordedBy = userID
			saved, err = s.store.CreateLedgerEntry(entry)
		} else {
			entry.ID = entryID
			saved, err = s.store.UpdateLedgerEntry(entry)
			status = http.StatusOK
		}
		if err != nil {
			writeJSON(w, http.StatusNotFound, map[string]string{"error": err.Error()})
			return
		}
		writeJSON(w, status, saved)
	case entryID != "" && r.Method == http.MethodDelete:
		if err := s.store.DeleteLedgerEntry(invitation.ID, entryID); err != nil {
			writeJSON(w, http.StatusNotFound, map[string]string{"error": err.Error()})
			return
		}
		writeJSON(w, http.StatusOK, map[string]bool{"deleted": true})
	default:
		writeJSON(w, http.StatusMethodNotAllowed, map[string]string{"error": "method not allowed"})
	}
}

func (s *Server) writeLedger(w http.ResponseWriter, invitationID string) {
	type row struct {
		*store.LedgerEntry
		Source string `json:"source"` // manual, online
	}
	items := []row{}
	totals := map[string]float64{"cash": 0, "transfer": 0, "online": 0, "total": 0}
	kado := 0
	for _, entry := range s.store.ListLedger(invitationID) {
		items = append(items, row{entry, "manual"})
		if entry.Kind == "kado" {
			kado++ // estimated value of goods is not counted as money
		} else {
			totals[entry.Kind] += entry.Amount
			totals["total"] += entry.Amount
		}
	}
	// Confirmed online envelopes appear automatically (read-only).
	for _, tx := range s.store.ListGiftTransactions(invitationID) {
		if (tx.Gateway != "mayar" && tx.Gateway != "dummy") || tx.Status != "confirmed" {
			continue
		}
		note := tx.Message
		if strings.HasPrefix(tx.Purpose, "wishlist:") {
			note = strings.TrimSpace("Patungan kado. " + note)
		}
		items = append(items, row{&store.LedgerEntry{ID: "online-" + tx.ID, InvitationID: invitationID, GuestID: tx.GuestID, Name: tx.SenderName, Kind: "online", Amount: tx.Amount, Note: note, CreatedAt: tx.CreatedAt}, "online"})
		totals["online"] += tx.Amount
		totals["total"] += tx.Amount
	}
	sort.SliceStable(items, func(i, j int) bool { return items[i].CreatedAt.After(items[j].CreatedAt) })
	writeJSON(w, http.StatusOK, map[string]any{"items": items, "totals": totals, "kado_count": kado, "count": len(items)})
}

/* ── 2. Layar sapa (venue screen feed) ─────────────────────────── */

// GET /api/invitations/{id}/live — polled every few seconds by the venue screen.
func (s *Server) handleLiveFeed(w http.ResponseWriter, r *http.Request, invitationID string) {
	invitation, _, ok := s.ownedInvitation(w, r, invitationID)
	if !ok {
		return
	}
	if r.Method != http.MethodGet {
		writeJSON(w, http.StatusMethodNotAllowed, map[string]string{"error": "method not allowed"})
		return
	}
	type checkin struct {
		ID          string    `json:"id"`
		Name        string    `json:"name"`
		Table       string    `json:"table,omitempty"`
		Category    string    `json:"category,omitempty"`
		CheckedInAt time.Time `json:"checked_in_at"`
	}
	guests := s.store.ListGuests(invitation.ID)
	checkins := []checkin{}
	for _, g := range guests {
		if g.CheckedInAt != nil {
			checkins = append(checkins, checkin{g.ID, g.Name, g.Table, g.Category, *g.CheckedInAt})
		}
	}
	sort.Slice(checkins, func(i, j int) bool { return checkins[i].CheckedInAt.After(checkins[j].CheckedInAt) })
	total := len(checkins)
	if len(checkins) > 30 {
		checkins = checkins[:30]
	}
	wishes := s.store.ListPublishedWishes(invitation.ID)
	sort.Slice(wishes, func(i, j int) bool { return wishes[i].CreatedAt.After(wishes[j].CreatedAt) })
	if len(wishes) > 40 {
		wishes = wishes[:40]
	}
	photos := s.store.ListGuestPhotos(invitation.ID, "approved")
	if len(photos) > 40 {
		photos = photos[:40]
	}
	writeJSON(w, http.StatusOK, map[string]any{
		"invitation": map[string]any{"id": invitation.ID, "slug": invitation.Slug, "title": invitation.Title, "couple": invitation.Couple},
		"stats":      map[string]int{"checked_in": total, "guests": len(guests)},
		"checkins":   checkins,
		"wishes":     wishes,
		"photos":     photos,
		"doorprize":  s.doorprize(invitation.ID),
		"now":        time.Now().UTC(),
	})
}

/* ── 3. Doorprize ──────────────────────────────────────────────── */

type prize struct {
	ID   string `json:"id"`
	Name string `json:"name"`
	Qty  int    `json:"qty"`
}

type winner struct {
	GuestID string    `json:"guest_id"`
	Name    string    `json:"name"`
	Table   string    `json:"table,omitempty"`
	PrizeID string    `json:"prize_id"`
	Prize   string    `json:"prize"`
	At      time.Time `json:"at"`
}

type doorprizeState struct {
	Prizes  []prize  `json:"prizes"`
	Winners []winner `json:"winners"`
}

func (s *Server) doorprize(invitationID string) doorprizeState {
	state := doorprizeState{Prizes: []prize{}, Winners: []winner{}}
	raw, _ := json.Marshal(s.store.GetPrivateData(invitationID, "doorprize"))
	_ = json.Unmarshal(raw, &state)
	if state.Prizes == nil {
		state.Prizes = []prize{}
	}
	if state.Winners == nil {
		state.Winners = []winner{}
	}
	return state
}

func (s *Server) saveDoorprize(invitationID string, state doorprizeState) error {
	raw, _ := json.Marshal(state)
	data := map[string]any{}
	_ = json.Unmarshal(raw, &data)
	return s.store.SetPrivateData(invitationID, "doorprize", data)
}

func randomIndex(n int) int {
	v, err := rand.Int(rand.Reader, big.NewInt(int64(n)))
	if err != nil {
		return 0
	}
	return int(v.Int64())
}

// GET/PUT /api/invitations/{id}/doorprize, POST /api/invitations/{id}/doorprize/draw
func (s *Server) handleDoorprize(w http.ResponseWriter, r *http.Request, invitationID, action string) {
	invitation, _, ok := s.ownedInvitation(w, r, invitationID)
	if !ok {
		return
	}
	s.doorprizeMu.Lock()
	defer s.doorprizeMu.Unlock()
	state := s.doorprize(invitation.ID)
	switch {
	case action == "" && r.Method == http.MethodGet:
		writeJSON(w, http.StatusOK, state)
	case action == "" && (r.Method == http.MethodPut || r.Method == http.MethodPatch):
		var payload struct {
			Prizes []prize `json:"prizes"`
			Reset  bool    `json:"reset_winners"`
		}
		if json.NewDecoder(http.MaxBytesReader(w, r.Body, 16384)).Decode(&payload) != nil || len(payload.Prizes) > 50 {
			writeJSON(w, http.StatusBadRequest, map[string]string{"error": "invalid payload"})
			return
		}
		prizes := []prize{}
		for i, p := range payload.Prizes {
			p.Name = trimTo(p.Name, 80)
			if p.Name == "" {
				continue
			}
			if p.Qty < 1 {
				p.Qty = 1
			}
			if p.Qty > 500 {
				p.Qty = 500
			}
			if p.ID == "" {
				p.ID = "p" + randomID()[:8] + string(rune('a'+i%26))
			}
			prizes = append(prizes, p)
		}
		state.Prizes = prizes
		if payload.Reset {
			state.Winners = []winner{}
		}
		if err := s.saveDoorprize(invitation.ID, state); err != nil {
			writeJSON(w, http.StatusInternalServerError, map[string]string{"error": err.Error()})
			return
		}
		writeJSON(w, http.StatusOK, state)
	case action == "draw" && r.Method == http.MethodPost:
		var payload struct {
			PrizeID string `json:"prize_id"`
		}
		_ = json.NewDecoder(http.MaxBytesReader(w, r.Body, 1024)).Decode(&payload)
		var chosen *prize
		for i := range state.Prizes {
			if state.Prizes[i].ID == payload.PrizeID {
				chosen = &state.Prizes[i]
			}
		}
		if chosen == nil {
			writeJSON(w, http.StatusBadRequest, map[string]string{"error": "hadiah tidak ditemukan"})
			return
		}
		given := 0
		won := map[string]bool{}
		for _, wnr := range state.Winners {
			won[wnr.GuestID] = true
			if wnr.PrizeID == chosen.ID {
				given++
			}
		}
		if given >= chosen.Qty {
			writeJSON(w, http.StatusConflict, map[string]string{"error": "semua " + chosen.Name + " sudah diundi"})
			return
		}
		// Only guests who are actually at the venue, and each guest wins at most once.
		pool := []*store.Guest{}
		for _, g := range s.store.ListGuests(invitation.ID) {
			if g.CheckedInAt != nil && !won[g.ID] {
				pool = append(pool, g)
			}
		}
		if len(pool) == 0 {
			writeJSON(w, http.StatusConflict, map[string]string{"error": "belum ada tamu check-in yang bisa diundi"})
			return
		}
		g := pool[randomIndex(len(pool))]
		result := winner{GuestID: g.ID, Name: g.Name, Table: g.Table, PrizeID: chosen.ID, Prize: chosen.Name, At: time.Now().UTC()}
		state.Winners = append(state.Winners, result)
		if err := s.saveDoorprize(invitation.ID, state); err != nil {
			writeJSON(w, http.StatusInternalServerError, map[string]string{"error": err.Error()})
			return
		}
		writeJSON(w, http.StatusOK, map[string]any{"winner": result, "pool": len(pool), "state": state})
	default:
		writeJSON(w, http.StatusMethodNotAllowed, map[string]string{"error": "method not allowed"})
	}
}

/* ── 4. Galeri dari tamu ───────────────────────────────────────── */

// POST /api/public/invitation/{slug}/photos (multipart: file, name, guest) — GET lists approved photos.
func (s *Server) handlePublicGuestPhotos(w http.ResponseWriter, r *http.Request, slug string) {
	invitation, exists := s.store.FindInvitationBySlug(slug)
	if !exists || (!invitation.Published && !s.canPreviewUnpublished(r, invitation)) {
		writeJSON(w, http.StatusNotFound, map[string]string{"error": "invitation not found"})
		return
	}
	enabled, cfg := sectionOn(s.store.GetSettings(invitation.ID), "guestPhotos")
	if r.Method == http.MethodGet {
		items := []map[string]any{}
		if enabled {
			for _, p := range s.store.ListGuestPhotos(invitation.ID, "approved") {
				items = append(items, map[string]any{"id": p.ID, "url": p.URL, "uploader_name": p.UploaderName, "created_at": p.CreatedAt})
			}
		}
		writeJSON(w, http.StatusOK, map[string]any{"items": items})
		return
	}
	if r.Method != http.MethodPost {
		writeJSON(w, http.StatusMethodNotAllowed, map[string]string{"error": "method not allowed"})
		return
	}
	if !enabled || !invitation.Published {
		writeJSON(w, http.StatusForbidden, map[string]string{"error": "upload foto tamu tidak aktif"})
		return
	}
	if s.photoStore == nil {
		writeJSON(w, http.StatusServiceUnavailable, map[string]string{"error": "penyimpanan foto belum dikonfigurasi"})
		return
	}
	if !s.allowRate(w, "guest-photo:"+invitation.ID+":"+clientIP(r), 15, 10*time.Minute) {
		return
	}
	r.Body = http.MaxBytesReader(w, r.Body, 12<<20)
	if err := r.ParseMultipartForm(12 << 20); err != nil {
		writeJSON(w, http.StatusRequestEntityTooLarge, map[string]string{"error": "foto maksimal 10 MB"})
		return
	}
	file, _, err := r.FormFile("file")
	if err != nil {
		writeJSON(w, http.StatusBadRequest, map[string]string{"error": "file is required"})
		return
	}
	defer file.Close()
	data, err := io.ReadAll(io.LimitReader(file, 10<<20+1))
	if err != nil || len(data) > 10<<20 {
		writeJSON(w, http.StatusRequestEntityTooLarge, map[string]string{"error": "foto maksimal 10 MB"})
		return
	}
	contentType := mediaservice.DetectContentType(data)
	if contentType != "image/jpeg" && contentType != "image/png" && contentType != "image/webp" {
		writeJSON(w, http.StatusBadRequest, map[string]string{"error": "gunakan foto JPG, PNG, atau WebP"})
		return
	}
	guestID := ""
	if token := strings.TrimSpace(r.FormValue("guest")); token != "" {
		if guest, ok := s.store.FindGuestByToken(invitation.ID, token); ok {
			guestID = guest.ID
		}
	}
	url, err := s.photoStore.Upload(r.Context(), "guest-photos/"+invitation.ID+"/"+randomID(), bytes.NewReader(data), int64(len(data)), contentType)
	if err != nil {
		writeJSON(w, http.StatusBadGateway, map[string]string{"error": "foto belum terunggah, coba lagi"})
		return
	}
	status := "approved"
	if moderate, _ := cfg["moderate"].(bool); moderate {
		status = "pending"
	}
	photo, err := s.store.CreateGuestPhoto(store.GuestPhoto{InvitationID: invitation.ID, GuestID: guestID, UploaderName: trimTo(r.FormValue("name"), 60), URL: url, Status: status})
	if err != nil {
		writeJSON(w, http.StatusInternalServerError, map[string]string{"error": err.Error()})
		return
	}
	writeJSON(w, http.StatusCreated, map[string]any{"id": photo.ID, "url": photo.URL, "status": photo.Status})
}

// GET /api/invitations/{id}/guest-photos, PATCH /api/invitations/{id}/guest-photos/{photoId} {status}
func (s *Server) handleGuestPhotosAdmin(w http.ResponseWriter, r *http.Request, invitationID, photoID string) {
	invitation, _, ok := s.ownedInvitation(w, r, invitationID)
	if !ok {
		return
	}
	if photoID == "" && r.Method == http.MethodGet {
		writeJSON(w, http.StatusOK, map[string]any{"items": s.store.ListGuestPhotos(invitation.ID, r.URL.Query().Get("status")), "storage_ready": s.photoStore != nil})
		return
	}
	if photoID == "" || (r.Method != http.MethodPatch && r.Method != http.MethodPut) {
		writeJSON(w, http.StatusMethodNotAllowed, map[string]string{"error": "method not allowed"})
		return
	}
	var payload struct {
		Status string `json:"status"`
	}
	if json.NewDecoder(http.MaxBytesReader(w, r.Body, 1024)).Decode(&payload) != nil || (payload.Status != "approved" && payload.Status != "hidden" && payload.Status != "pending") {
		writeJSON(w, http.StatusBadRequest, map[string]string{"error": "status must be approved, hidden, or pending"})
		return
	}
	photo, err := s.store.UpdateGuestPhotoStatus(invitation.ID, photoID, payload.Status)
	if err != nil {
		writeJSON(w, http.StatusNotFound, map[string]string{"error": err.Error()})
		return
	}
	writeJSON(w, http.StatusOK, photo)
}

/* ── 5. Patungan kado ──────────────────────────────────────────── */

// fundableWishlistItem returns the item's name when it exists and accepts contributions.
func fundableWishlistItem(settings map[string]any, itemID string) (string, bool) {
	// The wishlist block is on unless explicitly switched off.
	cfg, _ := sectionsConfig(settings)["wishlist"].(map[string]any)
	if cfg == nil || cfg["enabled"] == false {
		return "", false
	}
	items, _ := cfg["items"].([]any)
	for _, raw := range items {
		item, _ := raw.(map[string]any)
		if item == nil || item["id"] != itemID {
			continue
		}
		fund, _ := item["fund"].(bool)
		target, _ := number(item["target"])
		name, _ := item["name"].(string)
		return name, fund && target > 0
	}
	return "", false
}

// wishlistFunds sums confirmed contributions per wishlist item.
func (s *Server) wishlistFunds(invitationID string) map[string]float64 {
	funds := map[string]float64{}
	for _, tx := range s.store.ListGiftTransactions(invitationID) {
		if tx.Status == "confirmed" && strings.HasPrefix(tx.Purpose, "wishlist:") {
			funds[strings.TrimPrefix(tx.Purpose, "wishlist:")] += tx.Amount
		}
	}
	return funds
}

/* ── 7. Kenangan (public recap) ────────────────────────────────── */

// GET /api/public/invitation/{slug}/recap — counts only, no names or amounts.
func (s *Server) handlePublicRecap(w http.ResponseWriter, r *http.Request, slug string) {
	invitation, exists := s.store.FindInvitationBySlug(slug)
	if !exists || (!invitation.Published && !s.canPreviewUnpublished(r, invitation)) {
		writeJSON(w, http.StatusNotFound, map[string]string{"error": "invitation not found"})
		return
	}
	if r.Method != http.MethodGet {
		writeJSON(w, http.StatusMethodNotAllowed, map[string]string{"error": "method not allowed"})
		return
	}
	checkedIn := 0
	for _, g := range s.store.ListGuests(invitation.ID) {
		if g.CheckedInAt != nil {
			checkedIn++
		}
	}
	attending := 0
	for _, rsvp := range s.store.ListRSVPs(invitation.ID) {
		if rsvp.Attendance == "yes" {
			attending += max(1, rsvp.AttendeesCount)
		}
	}
	photos := 0
	if enabled, _ := sectionOn(s.store.GetSettings(invitation.ID), "guestPhotos"); enabled {
		photos = len(s.store.ListGuestPhotos(invitation.ID, "approved"))
	}
	writeJSON(w, http.StatusOK, map[string]int{
		"checked_in": checkedIn,
		"attending":  attending,
		"wishes":     len(s.store.ListPublishedWishes(invitation.ID)),
		"photos":     photos,
	})
}
