package api

import (
	"encoding/json"
	"net/http"
	"strings"
)

func (s *Server) handleProfile(w http.ResponseWriter, r *http.Request) {
	claims, ok := s.requireAuth(w, r)
	if !ok {
		return
	}
	user, exists := s.store.FindUserByID(claims.UserID)
	if !exists {
		writeJSON(w, http.StatusNotFound, map[string]string{"error": "user not found"})
		return
	}
	if r.Method == http.MethodGet {
		writeJSON(w, http.StatusOK, map[string]any{
			"id": user.ID, "name": user.Name, "email": user.Email,
			"role": user.Role, "avatar": user.Avatar,
		})
		return
	}
	if r.Method == http.MethodPatch {
		var payload struct {
			Name   string `json:"name"`
			Avatar string `json:"avatar"`
		}
		if err := json.NewDecoder(http.MaxBytesReader(w, r.Body, 8<<10)).Decode(&payload); err != nil {
			writeJSON(w, http.StatusBadRequest, map[string]string{"error": "invalid payload"})
			return
		}
		if strings.TrimSpace(payload.Name) == "" && payload.Avatar == "" {
			writeJSON(w, http.StatusBadRequest, map[string]string{"error": "name or avatar is required"})
			return
		}
		payload.Avatar = strings.TrimSpace(payload.Avatar)
		if payload.Avatar != "" && (len(payload.Avatar) > 500 || !(strings.HasPrefix(payload.Avatar, "https://") || (strings.HasPrefix(payload.Avatar, "/") && !strings.HasPrefix(payload.Avatar, "//")))) {
			writeJSON(w, http.StatusBadRequest, map[string]string{"error": "Foto profil harus berupa tautan https"})
			return
		}
		if len([]rune(strings.TrimSpace(payload.Name))) > 80 {
			writeJSON(w, http.StatusBadRequest, map[string]string{"error": "Nama maksimal 80 karakter"})
			return
		}
		if strings.TrimSpace(payload.Name) != "" {
			updated, err := s.store.UpdateUser(user.ID, strings.TrimSpace(payload.Name))
			if err != nil {
				writeJSON(w, http.StatusNotFound, map[string]string{"error": err.Error()})
				return
			}
			user = updated
		}
		if payload.Avatar != "" {
			updated, err := s.store.UpdateUserAvatar(user.ID, payload.Avatar)
			if err != nil {
				writeJSON(w, http.StatusNotFound, map[string]string{"error": err.Error()})
				return
			}
			user = updated
		}
		writeJSON(w, http.StatusOK, map[string]any{
			"id": user.ID, "name": user.Name, "email": user.Email,
			"role": user.Role, "avatar": user.Avatar,
		})
		return
	}
	writeJSON(w, http.StatusMethodNotAllowed, map[string]string{"error": "method not allowed"})
}
