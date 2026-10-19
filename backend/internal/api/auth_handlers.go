package api

import (
	"encoding/json"
	"net/http"
	"net/url"
	"strings"
	"time"
	"yukakad/internal/auth"
)

func (s *Server) handleLogout(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		writeJSON(w, http.StatusMethodNotAllowed, map[string]string{"error": "method not allowed"})
		return
	}
	authorization := strings.TrimSpace(strings.TrimPrefix(r.Header.Get("Authorization"), "Bearer "))
	if authorization == "" {
		writeJSON(w, http.StatusUnauthorized, map[string]string{"error": "missing authorization token"})
		return
	}
	claims, ok := s.authenticateToken(authorization)
	if !ok {
		writeJSON(w, http.StatusUnauthorized, map[string]string{"error": "invalid token"})
		return
	}
	if s.sessions != nil {
		if err := s.sessions.Revoke(authorization); err != nil {
			writeJSON(w, http.StatusServiceUnavailable, map[string]string{"error": "authentication service unavailable"})
			return
		}
	} else {
		_ = s.revoker.Revoke(authorization, time.Unix(claims.Exp, 0))
	}
	w.WriteHeader(http.StatusNoContent)
}

func (s *Server) handleForgotPassword(w http.ResponseWriter, r *http.Request) {
	if !s.allowRate(w, "auth:forgot-password:"+clientIP(r), 5, time.Minute) {
		return
	}
	if r.Method != http.MethodPost {
		writeJSON(w, http.StatusMethodNotAllowed, map[string]string{"error": "method not allowed"})
		return
	}
	var payload struct {
		Email string `json:"email"`
	}
	if json.NewDecoder(r.Body).Decode(&payload) != nil || strings.TrimSpace(payload.Email) == "" {
		writeJSON(w, http.StatusBadRequest, map[string]string{"error": "Email wajib diisi"})
		return
	}
	// Checked before the lookup so the response never reveals whether an account exists.
	if s.resetMailer == nil {
		writeJSON(w, http.StatusServiceUnavailable, map[string]string{"error": "Reset lewat email belum aktif. Hubungi admin Rawuh.", "code": "reset_unavailable"})
		return
	}
	user, exists := s.store.FindUserByEmail(strings.TrimSpace(payload.Email))
	response := map[string]any{"message": "Kalau emailnya terdaftar, link reset sudah kami kirim."}
	if exists {
		token, err := auth.GenerateOpaqueToken()
		if err == nil {
			err = s.store.CreatePasswordResetToken(user.ID, auth.HashOpaqueToken(token), time.Now().Add(30*time.Minute))
		}
		if err != nil {
			writeJSON(w, http.StatusServiceUnavailable, map[string]string{"error": "Layanan reset sedang bermasalah. Coba lagi nanti."})
			return
		}
		resetURL := strings.TrimRight(s.config.FrontendOrigin, "/") + "/auth/reset-password?token=" + url.QueryEscape(token)
		if err := s.resetMailer.SendPasswordReset(r.Context(), user.Email, resetURL); err != nil {
			writeJSON(w, http.StatusServiceUnavailable, map[string]string{"error": "Email reset belum terkirim. Coba lagi nanti."})
			return
		}
	}
	writeJSON(w, http.StatusOK, response)
}

func (s *Server) handleResetPassword(w http.ResponseWriter, r *http.Request) {
	if !s.allowRate(w, "auth:reset-password:"+clientIP(r), 5, time.Minute) {
		return
	}
	if r.Method != http.MethodPost {
		writeJSON(w, http.StatusMethodNotAllowed, map[string]string{"error": "method not allowed"})
		return
	}
	var payload struct {
		Token    string `json:"token"`
		Password string `json:"password"`
	}
	if json.NewDecoder(r.Body).Decode(&payload) != nil || payload.Token == "" || len(payload.Password) < 8 {
		writeJSON(w, http.StatusBadRequest, map[string]string{"error": "Link reset tidak valid atau password kurang dari 8 karakter"})
		return
	}
	userID, err := s.store.ConsumePasswordResetToken(auth.HashOpaqueToken(payload.Token))
	if err != nil {
		writeJSON(w, http.StatusUnauthorized, map[string]string{"error": "Link reset sudah kedaluwarsa atau sudah dipakai. Minta link baru."})
		return
	}
	hashed, err := auth.HashPassword(payload.Password)
	if err != nil {
		writeJSON(w, http.StatusBadRequest, map[string]string{"error": "Password terlalu panjang"})
		return
	}
	if err := s.store.UpdatePassword(userID, hashed); err != nil {
		writeJSON(w, http.StatusNotFound, map[string]string{"error": "user not found"})
		return
	}
	writeJSON(w, http.StatusOK, map[string]string{"message": "Password berhasil diganti. Silakan masuk."})
}
