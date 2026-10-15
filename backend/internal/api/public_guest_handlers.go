package api

import (
	"net/http"
	"strings"
	"time"
)

// handlePublicGuest resolves a guest's personal link token to the details their invitation may show:
// display name and table. Only the holder of the token learns anything.
// Route: GET /api/public/invitation/{slug}/guest?token=...
func (s *Server) handlePublicGuest(w http.ResponseWriter, r *http.Request, slug string) {
	if r.Method != http.MethodGet {
		writeJSON(w, http.StatusMethodNotAllowed, map[string]string{"error": "method not allowed"})
		return
	}
	invitation, exists := s.store.FindInvitationBySlug(slug)
	if !exists || (!invitation.Published && !s.canPreviewUnpublished(r, invitation)) {
		writeJSON(w, http.StatusNotFound, map[string]string{"error": "invitation not found"})
		return
	}
	token := strings.TrimSpace(r.URL.Query().Get("token"))
	if token == "" {
		writeJSON(w, http.StatusBadRequest, map[string]string{"error": "token is required"})
		return
	}
	if !s.allowRate(w, "guest-lookup:"+invitation.ID+":"+clientIP(r), 30, time.Minute) {
		return
	}
	guest, ok := s.store.FindGuestByToken(invitation.ID, token)
	if !ok {
		writeJSON(w, http.StatusNotFound, map[string]string{"error": "guest not found"})
		return
	}
	writeJSON(w, http.StatusOK, map[string]string{"name": guest.Name, "table": guest.Table})
}
