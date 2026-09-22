package api

import (
	"crypto/rand"
	"encoding/hex"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"net/url"
	"regexp"
	"strings"
	mediaservice "yukakad/internal/media"
)

const defaultBroadcastTemplate = "Halo {nama_tamu}, kami mengundang Anda ke acara kami. Silakan lihat undangan lengkap di sini: {link}"

var nonDigitPattern = regexp.MustCompile(`[^0-9]`)

// normalizeIndonesianPhone converts a locally-formatted Indonesian number
// (e.g. "0812...") into the international format wa.me expects ("62812...").
func normalizeIndonesianPhone(phone string) string {
	digits := nonDigitPattern.ReplaceAllString(phone, "")
	if strings.HasPrefix(digits, "0") {
		digits = "62" + digits[1:]
	}
	return digits
}

const maxUploadSize = 10 << 20 // 10MB

func (s *Server) handleOperations(w http.ResponseWriter, r *http.Request, invitationID, resource string) {
	claims, ok := s.requireAuth(w, r)
	if !ok {
		return
	}
	invitation, exists := s.store.FindInvitationByID(invitationID)
	if !exists {
		writeJSON(w, http.StatusNotFound, map[string]string{"error": "invitation not found"})
		return
	}
	if invitation.UserID != claims.UserID {
		writeJSON(w, http.StatusForbidden, map[string]string{"error": "forbidden"})
		return
	}

	if resource == "broadcast" {
		if r.Method == http.MethodGet {
			writeJSON(w, http.StatusOK, map[string]any{"items": s.store.ListBroadcastLogs(invitationID)})
			return
		}
		if r.Method == http.MethodPost {
			s.handleBroadcastCreate(w, r, invitationID, invitation.Slug)
			return
		}
	}
	if resource == "media" {
		if r.Method == http.MethodGet {
			writeJSON(w, http.StatusOK, map[string]any{"items": s.store.ListMedia(invitationID)})
			return
		}
		if r.Method == http.MethodPost {
			s.handleMediaUpload(w, r, claims.UserID, invitationID)
			return
		}
	}
	writeJSON(w, http.StatusMethodNotAllowed, map[string]string{"error": "method not allowed"})
}

func (s *Server) handleMediaUpload(w http.ResponseWriter, r *http.Request, ownerID, invitationID string) {
	if s.storage == nil {
		writeJSON(w, http.StatusServiceUnavailable, map[string]string{"error": "media storage is not configured"})
		return
	}

	r.Body = http.MaxBytesReader(w, r.Body, maxUploadSize)
	if err := r.ParseMultipartForm(maxUploadSize); err != nil {
		writeJSON(w, http.StatusRequestEntityTooLarge, map[string]string{"error": "file too large (max 10MB)"})
		return
	}
	file, _, err := r.FormFile("file")
	if err != nil {
		writeJSON(w, http.StatusBadRequest, map[string]string{"error": "file is required"})
		return
	}
	defer file.Close()

	buf, err := io.ReadAll(file)
	if err != nil {
		writeJSON(w, http.StatusBadRequest, map[string]string{"error": "could not read file"})
		return
	}
	contentType := mediaservice.DetectContentType(buf)
	item, err := s.media.Upload(r.Context(), ownerID, invitationID, r.FormValue("type"), contentType, buf)
	if err != nil {
		status := http.StatusBadRequest
		if err == mediaservice.ErrNotFound {
			status = http.StatusNotFound
		}
		if strings.Contains(err.Error(), "upload media") {
			status = http.StatusBadGateway
		}
		writeJSON(w, status, map[string]string{"error": err.Error()})
		return
	}
	writeJSON(w, http.StatusCreated, item)
}

func (s *Server) handleMediaDetail(w http.ResponseWriter, r *http.Request, invitationID, mediaID string) {
	claims, ok := s.requireAuth(w, r)
	if !ok {
		return
	}
	if r.Method != http.MethodDelete {
		writeJSON(w, http.StatusMethodNotAllowed, map[string]string{"error": "method not allowed"})
		return
	}
	if err := s.media.Delete(r.Context(), claims.UserID, mediaID); err != nil {
		writeJSON(w, http.StatusNotFound, map[string]string{"error": err.Error()})
		return
	}
	w.WriteHeader(http.StatusNoContent)
}

func randomID() string {
	b := make([]byte, 16)
	_, _ = rand.Read(b)
	return hex.EncodeToString(b)
}

// handleBroadcastCreate generates a personal wa.me link per requested
// guest. wa.me cannot confirm delivery — it only opens a chat — so each
// generated link is logged with status "generated" until the frontend
// calls the confirm endpoint right before opening it, at which point the
// log flips to "sent". Without resend=true, a guest whose latest log is
// already "sent" is skipped so the same guest isn't re-notified by
// accident.
func (s *Server) handleBroadcastCreate(w http.ResponseWriter, r *http.Request, invitationID, slug string) {
	var payload struct {
		GuestIDs []string `json:"guest_ids"`
		Template string   `json:"template"`
		Resend   bool     `json:"resend"`
	}
	if json.NewDecoder(r.Body).Decode(&payload) != nil || len(payload.GuestIDs) == 0 {
		writeJSON(w, http.StatusBadRequest, map[string]string{"error": "guest_ids is required"})
		return
	}
	template := strings.TrimSpace(payload.Template)
	if template == "" {
		template = defaultBroadcastTemplate
	}

	results := make([]map[string]any, 0, len(payload.GuestIDs))
	for _, guestID := range payload.GuestIDs {
		guest, ok := s.store.FindGuestByID(guestID)
		if !ok || guest.InvitationID != invitationID {
			results = append(results, map[string]any{"guest_id": guestID, "status": "error", "error": "guest not found"})
			continue
		}
		if !payload.Resend {
			if latest, found := s.store.LatestBroadcastLogForGuest(invitationID, guestID); found && latest["status"] == "sent" {
				results = append(results, map[string]any{"guest_id": guestID, "status": "skipped_already_sent", "id": latest["id"]})
				continue
			}
		}
		link := fmt.Sprintf("%s/invitation/%s?guest=%s", s.config.FrontendOrigin, slug, guest.Token)
		message := strings.NewReplacer("{nama_tamu}", guest.Name, "{link}", link).Replace(template)
		log, err := s.store.CreateBroadcastLog(invitationID, guestID, message, "generated")
		if err != nil {
			results = append(results, map[string]any{"guest_id": guestID, "status": "error", "error": err.Error()})
			continue
		}
		log["wa_link"] = "https://wa.me/" + normalizeIndonesianPhone(guest.Phone) + "?text=" + url.QueryEscape(message)
		results = append(results, log)
	}
	writeJSON(w, http.StatusCreated, map[string]any{"items": results})
}

func (s *Server) handleBroadcastConfirm(w http.ResponseWriter, r *http.Request, invitationID, logID string) {
	claims, ok := s.requireAuth(w, r)
	if !ok {
		return
	}
	invitation, exists := s.store.FindInvitationByID(invitationID)
	if !exists {
		writeJSON(w, http.StatusNotFound, map[string]string{"error": "invitation not found"})
		return
	}
	if invitation.UserID != claims.UserID {
		writeJSON(w, http.StatusForbidden, map[string]string{"error": "forbidden"})
		return
	}
	if r.Method != http.MethodPost {
		writeJSON(w, http.StatusMethodNotAllowed, map[string]string{"error": "method not allowed"})
		return
	}

	log, err := s.store.UpdateBroadcastLogStatus(logID, "sent")
	if err != nil || log["invitation_id"] != invitationID {
		writeJSON(w, http.StatusNotFound, map[string]string{"error": "broadcast log not found"})
		return
	}
	writeJSON(w, http.StatusOK, log)
}
