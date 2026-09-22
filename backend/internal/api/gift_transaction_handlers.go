package api

import (
	"encoding/json"
	"errors"
	"net/http"
	"strings"
	giftservice "yukakad/internal/gifts"
)

func (s *Server) handleGiftTransactions(w http.ResponseWriter, r *http.Request, invitationID string) {
	claims, ok := s.requireAuth(w, r)
	if !ok {
		return
	}
	base := "/api/invitations/" + invitationID + "/gift-transactions"
	id := strings.Trim(strings.TrimPrefix(r.URL.Path, base), "/")
	if r.Method == http.MethodGet && id == "" {
		items, err := s.gifts.List(claims.UserID, invitationID)
		if err != nil {
			writeJSON(w, http.StatusNotFound, map[string]string{"error": err.Error()})
			return
		}
		writeJSON(w, http.StatusOK, map[string]any{"items": items})
		return
	}
	if r.Method != http.MethodPatch || id == "" {
		writeJSON(w, http.StatusMethodNotAllowed, map[string]string{"error": "method not allowed"})
		return
	}
	var payload struct {
		Status    string `json:"status"`
		Reference string `json:"gateway_reference_id"`
	}
	if json.NewDecoder(r.Body).Decode(&payload) != nil {
		writeJSON(w, http.StatusBadRequest, map[string]string{"error": "invalid payload"})
		return
	}
	tx, err := s.gifts.Moderate(claims.UserID, invitationID, id, payload.Status, payload.Reference)
	if err != nil {
		status := http.StatusBadRequest
		if errors.Is(err, giftservice.ErrNotFound) {
			status = http.StatusNotFound
		}
		writeJSON(w, status, map[string]string{"error": err.Error()})
		return
	}
	writeJSON(w, http.StatusOK, tx)
}
