package api

import (
	"encoding/json"
	"net/http"
	"strings"
	"time"
	"yukakad/internal/store"
)

// GET /api/admin/stats
func (s *Server) handleAdminStats(w http.ResponseWriter, r *http.Request) {
	if _, ok := s.requireAdmin(w, r); !ok {
		return
	}
	if r.Method != http.MethodGet {
		writeJSON(w, http.StatusMethodNotAllowed, map[string]string{"error": "method not allowed"})
		return
	}
	writeJSON(w, http.StatusOK, s.store.AdminStats())
}

// GET /api/admin/users
// PATCH /api/admin/users/{id}/role
func (s *Server) handleAdminUsers(w http.ResponseWriter, r *http.Request) {
	if _, ok := s.requireAdmin(w, r); !ok {
		return
	}

	path := strings.TrimPrefix(r.URL.Path, "/api/admin/users")
	path = strings.Trim(path, "/")
	if strings.HasSuffix(path, "/entitlements") && (r.Method == http.MethodPut || r.Method == http.MethodPatch) {
		userID := strings.TrimSuffix(path, "/entitlements")
		var payload struct {
			Feature   string `json:"feature"`
			Enabled   bool   `json:"enabled"`
			ExpiresAt string `json:"expires_at"`
		}
		if json.NewDecoder(r.Body).Decode(&payload) != nil || payload.Feature == "" {
			writeJSON(w, http.StatusBadRequest, map[string]string{"error": "feature and valid payload are required"})
			return
		}
		if _, ok := s.store.FindUserByID(userID); !ok {
			writeJSON(w, http.StatusNotFound, map[string]string{"error": "user not found"})
			return
		}
		var expiry *time.Time
		if payload.ExpiresAt != "" {
			parsed, err := time.Parse(time.RFC3339, payload.ExpiresAt)
			if err != nil {
				writeJSON(w, http.StatusBadRequest, map[string]string{"error": "expires_at must be RFC3339"})
				return
			}
			expiry = &parsed
		}
		item := store.Entitlement{UserID: userID, Feature: payload.Feature, Enabled: payload.Enabled, ExpiresAt: expiry}
		if err := s.store.SetUserEntitlement(item); err != nil {
			writeJSON(w, http.StatusBadRequest, map[string]string{"error": err.Error()})
			return
		}
		writeJSON(w, http.StatusOK, item)
		return
	}

	// PATCH /api/admin/users/{id}/role
	if strings.HasSuffix(r.URL.Path, "/role") && r.Method == http.MethodPatch {
		userID := strings.TrimSuffix(path, "/role")
		var payload struct {
			Role string `json:"role"`
		}
		if err := json.NewDecoder(r.Body).Decode(&payload); err != nil || (payload.Role != "admin" && payload.Role != "user") {
			writeJSON(w, http.StatusBadRequest, map[string]string{"error": "role must be 'admin' or 'user'"})
			return
		}
		user, err := s.store.UpdateUserRole(userID, payload.Role)
		if err != nil {
			writeJSON(w, http.StatusNotFound, map[string]string{"error": "user not found"})
			return
		}
		writeJSON(w, http.StatusOK, map[string]any{
			"id": user.ID, "name": user.Name, "email": user.Email, "role": user.Role,
		})
		return
	}

	// GET /api/admin/users
	if r.Method != http.MethodGet {
		writeJSON(w, http.StatusMethodNotAllowed, map[string]string{"error": "method not allowed"})
		return
	}
	users := s.store.AdminListUsers()
	items := make([]map[string]any, 0, len(users))
	for _, u := range users {
		items = append(items, map[string]any{
			"id":         u.ID,
			"name":       u.Name,
			"email":      u.Email,
			"role":       u.Role,
			"created_at": u.CreatedAt,
		})
	}
	writeJSON(w, http.StatusOK, map[string]any{"items": items})
}
