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
		writeJSON(w, http.StatusBadRequest, map[string]string{"error": "email is required"})
		return
	}
	user, exists := s.store.FindUserByEmail(strings.TrimSpace(payload.Email))
	response := map[string]any{"message": "if the account exists, reset instructions will be sent"}
	if exists {
		if s.resetMailer == nil {
			writeJSON(w, http.StatusServiceUnavailable, map[string]string{"error": "password reset delivery is not configured"})
			return
		}
		token, err := auth.GenerateOpaqueToken()
		if err == nil {
			err = s.store.CreatePasswordResetToken(user.ID, auth.HashOpaqueToken(token), time.Now().Add(30*time.Minute))
		}
		if err != nil {
			writeJSON(w, http.StatusServiceUnavailable, map[string]string{"error": "password reset service unavailable"})
			return
		}
		resetURL := strings.TrimRight(s.config.FrontendOrigin, "/") + "/reset-password?token=" + url.QueryEscape(token)
		if err := s.resetMailer.SendPasswordReset(r.Context(), user.Email, resetURL); err != nil {
			writeJSON(w, http.StatusServiceUnavailable, map[string]string{"error": "password reset delivery failed"})
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
		writeJSON(w, http.StatusBadRequest, map[string]string{"error": "valid token and password of at least 8 characters are required"})
		return
	}
	userID, err := s.store.ConsumePasswordResetToken(auth.HashOpaqueToken(payload.Token))
	if err != nil {
		writeJSON(w, http.StatusUnauthorized, map[string]string{"error": "invalid or expired reset token"})
		return
	}
	hashed, err := auth.HashPassword(payload.Password)
	if err != nil {
		writeJSON(w, http.StatusBadRequest, map[string]string{"error": "password is too long"})
		return
	}
	if err := s.store.UpdatePassword(userID, hashed); err != nil {
		writeJSON(w, http.StatusNotFound, map[string]string{"error": "user not found"})
		return
	}
	writeJSON(w, http.StatusOK, map[string]string{"message": "password reset successfully"})
}
