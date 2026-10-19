package api

import (
	"crypto/hmac"
	"crypto/sha256"
	"encoding/hex"
	"net/http"
	"strconv"
	"strings"
	"time"
)

// Preview tokens let the owner (or a team member) show an unpublished invitation without putting their
// session token in a URL: read-only, bound to one invitation, valid for previewValidity.
const previewValidity = 6 * time.Hour

func (s *Server) previewSignature(invitationID string, exp int64) string {
	mac := hmac.New(sha256.New, []byte("preview:"+s.config.JWTSecret))
	mac.Write([]byte(invitationID + ":" + strconv.FormatInt(exp, 10)))
	return hex.EncodeToString(mac.Sum(nil))
}

func (s *Server) issuePreviewToken(invitationID string, now time.Time) (string, time.Time) {
	expires := now.Add(previewValidity).UTC()
	exp := expires.Unix()
	return "pv1." + invitationID + "." + strconv.FormatInt(exp, 10) + "." + s.previewSignature(invitationID, exp), expires
}

func (s *Server) validPreviewToken(token, invitationID string, now time.Time) bool {
	parts := strings.Split(strings.TrimSpace(token), ".")
	if len(parts) != 4 || parts[0] != "pv1" || parts[1] != invitationID {
		return false
	}
	exp, err := strconv.ParseInt(parts[2], 10, 64)
	if err != nil || now.Unix() > exp {
		return false
	}
	return hmac.Equal([]byte(parts[3]), []byte(s.previewSignature(invitationID, exp)))
}

// POST /api/invitations/{id}/preview-token (owner or any team member; gated by gateInvitation).
func (s *Server) handlePreviewToken(w http.ResponseWriter, r *http.Request, invitationID string) {
	if r.Method != http.MethodPost {
		writeJSON(w, http.StatusMethodNotAllowed, map[string]string{"error": "method not allowed"})
		return
	}
	claims, ok := s.requireAuth(w, r)
	if !ok {
		return
	}
	invitation, exists := s.store.FindInvitationByID(invitationID)
	if !exists || invitation.UserID != claims.UserID {
		writeJSON(w, http.StatusNotFound, map[string]string{"error": "undangan tidak ditemukan"})
		return
	}
	token, expires := s.issuePreviewToken(invitation.ID, time.Now())
	writeJSON(w, http.StatusOK, map[string]any{"token": token, "expires_at": expires.Format(time.RFC3339)})
}
