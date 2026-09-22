package api

import (
	"encoding/json"
	"errors"
	"net/http"
	"strings"
	domainservice "yukakad/internal/domains"
)

func (s *Server) handleCustomDomains(w http.ResponseWriter, r *http.Request, invitationID string) {
	claims, ok := s.requireAuth(w, r)
	if !ok {
		return
	}
	base := "/api/invitations/" + invitationID + "/domains"
	id := strings.Trim(strings.TrimPrefix(r.URL.Path, base), "/")
	if r.Method == http.MethodGet && id == "" {
		items, err := s.domains.List(claims.UserID, invitationID)
		if err != nil {
			writeJSON(w, http.StatusNotFound, map[string]string{"error": err.Error()})
			return
		}
		writeJSON(w, http.StatusOK, map[string]any{"items": items})
		return
	}
	if r.Method == http.MethodPost && id == "" {
		var payload struct {
			Domain string `json:"domain"`
		}
		if json.NewDecoder(r.Body).Decode(&payload) != nil {
			writeJSON(w, http.StatusBadRequest, map[string]string{"error": "invalid payload"})
			return
		}
		item, err := s.domains.Create(claims.UserID, invitationID, payload.Domain)
		if err != nil {
			status := http.StatusBadRequest
			if errors.Is(err, domainservice.ErrNotAllowed) {
				status = http.StatusForbidden
			}
			if errors.Is(err, domainservice.ErrNotFound) {
				status = http.StatusNotFound
			}
			writeJSON(w, status, map[string]string{"error": err.Error()})
			return
		}
		writeJSON(w, http.StatusCreated, item)
		return
	}
	if r.Method == http.MethodPost && id != "" && strings.HasSuffix(id, "/verify") {
		domainID := strings.TrimSuffix(id, "/verify")
		var payload struct {
			Token string `json:"verification_token"`
		}
		if json.NewDecoder(r.Body).Decode(&payload) != nil {
			writeJSON(w, http.StatusBadRequest, map[string]string{"error": "invalid payload"})
			return
		}
		item, err := s.domains.Verify(claims.UserID, domainID, payload.Token)
		if err != nil {
			status := http.StatusBadRequest
			if errors.Is(err, domainservice.ErrNotFound) {
				status = http.StatusNotFound
			}
			writeJSON(w, status, map[string]string{"error": err.Error()})
			return
		}
		writeJSON(w, http.StatusOK, item)
		return
	}
	writeJSON(w, http.StatusMethodNotAllowed, map[string]string{"error": "method not allowed"})
}
