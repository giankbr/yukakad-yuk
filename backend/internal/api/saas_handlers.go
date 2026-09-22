package api

import (
	"encoding/json"
	"errors"
	"net/http"
	"strings"
	guestservice "yukakad/internal/guests"
	"yukakad/internal/invitations"
)

// POST /api/invitations/{id}/duplicate
func (s *Server) handleInvitationDuplicate(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		writeJSON(w, http.StatusMethodNotAllowed, map[string]string{"error": "method not allowed"})
		return
	}
	claims, ok := s.requireAuth(w, r)
	if !ok {
		return
	}

	// Path: /api/invitations/{id}/duplicate
	invitationID := strings.TrimSuffix(strings.TrimPrefix(r.URL.Path, "/api/invitations/"), "/duplicate")

	invitation, err := s.invitations.Owned(claims.UserID, invitationID)
	if err != nil {
		writeJSON(w, http.StatusNotFound, map[string]string{"error": err.Error()})
		return
	}

	var payload struct {
		Slug  string `json:"slug"`
		Title string `json:"title"`
	}
	// Payload is optional — default slug/title derived from source
	_ = json.NewDecoder(r.Body).Decode(&payload)

	slug := strings.TrimSpace(payload.Slug)
	title := strings.TrimSpace(payload.Title)
	if slug == "" {
		slug = invitation.Slug + "-copy"
	}
	if title == "" {
		title = "Copy of " + invitation.Title
	}

	newInv, err := s.invitations.Duplicate(claims.UserID, invitationID, slug, title)
	if err != nil {
		status := http.StatusConflict
		if errors.Is(err, invitations.ErrInvalid) {
			status = http.StatusBadRequest
		}
		writeJSON(w, status, map[string]string{"error": err.Error()})
		return
	}
	_ = s.store.CreateAuditLog(claims.UserID, newInv.ID, "invitation.duplicate", map[string]any{"source_id": invitationID})
	writeJSON(w, http.StatusCreated, newInv)
}

// DELETE /api/invitations/{id}/guests  (body: {"ids": ["gid1","gid2"]})
func (s *Server) handleBulkDeleteGuests(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodDelete {
		writeJSON(w, http.StatusMethodNotAllowed, map[string]string{"error": "method not allowed"})
		return
	}
	claims, ok := s.requireAuth(w, r)
	if !ok {
		return
	}

	invitationID := strings.TrimSuffix(strings.TrimPrefix(r.URL.Path, "/api/invitations/"), "/guests")

	if _, err := s.invitations.Owned(claims.UserID, invitationID); err != nil {
		writeJSON(w, http.StatusNotFound, map[string]string{"error": err.Error()})
		return
	}

	var payload struct {
		IDs []string `json:"ids"`
	}
	if err := json.NewDecoder(r.Body).Decode(&payload); err != nil || len(payload.IDs) == 0 {
		writeJSON(w, http.StatusBadRequest, map[string]string{"error": "ids array is required"})
		return
	}

	if err := s.guests.BulkDelete(claims.UserID, invitationID, payload.IDs); err != nil {
		status := http.StatusInternalServerError
		if errors.Is(err, guestservice.ErrNotFound) {
			status = http.StatusNotFound
		}
		if errors.Is(err, guestservice.ErrInvalid) {
			status = http.StatusBadRequest
		}
		writeJSON(w, status, map[string]string{"error": err.Error()})
		return
	}
	_ = s.store.CreateAuditLog(claims.UserID, invitationID, "guests.bulk_delete", map[string]any{"count": len(payload.IDs)})
	w.WriteHeader(http.StatusNoContent)
}
