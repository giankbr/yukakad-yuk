package api

import (
	"encoding/json"
	"net/http"
	"regexp"
	"strings"

	"yukakad/internal/store"
)

var planIDPattern = regexp.MustCompile(`^[a-z0-9][a-z0-9-]{1,30}$`)

// handleAdminPlans manages pricing plans.
// GET /api/admin/plans · POST /api/admin/plans · PUT /api/admin/plans/{id}
func (s *Server) handleAdminPlans(w http.ResponseWriter, r *http.Request) {
	if _, ok := s.requireAdmin(w, r); !ok {
		return
	}
	id := strings.Trim(strings.TrimPrefix(r.URL.Path, "/api/admin/plans"), "/")
	if r.Method == http.MethodGet && id == "" {
		writeJSON(w, http.StatusOK, map[string]any{"items": s.store.ListPlans()})
		return
	}
	if !(r.Method == http.MethodPost && id == "") && !((r.Method == http.MethodPut || r.Method == http.MethodPatch) && id != "") {
		writeJSON(w, http.StatusMethodNotAllowed, map[string]string{"error": "method not allowed"})
		return
	}
	// "active" is optional in the payload: absent keeps the current value (or true for a new plan).
	var payload struct {
		store.Plan
		Active *bool `json:"active"`
	}
	if err := json.NewDecoder(http.MaxBytesReader(w, r.Body, 8192)).Decode(&payload); err != nil {
		writeJSON(w, http.StatusBadRequest, map[string]string{"error": "invalid payload"})
		return
	}
	plan := payload.Plan
	plan.Active = true
	if id != "" {
		plan.ID = id
		exists := false
		for _, item := range s.store.ListPlans() {
			if item.ID == id {
				exists = true
				plan.Active = item.Active
				break
			}
		}
		if !exists {
			writeJSON(w, http.StatusNotFound, map[string]string{"error": "plan not found"})
			return
		}
	} else {
		plan.ID = strings.ToLower(strings.TrimSpace(plan.ID))
		if !planIDPattern.MatchString(plan.ID) {
			writeJSON(w, http.StatusBadRequest, map[string]string{"error": "id must be 2-31 lowercase letters, numbers or dashes"})
			return
		}
		for _, item := range s.store.ListPlans() {
			if item.ID == plan.ID {
				writeJSON(w, http.StatusConflict, map[string]string{"error": "plan id already exists"})
				return
			}
		}
	}
	if payload.Active != nil {
		plan.Active = *payload.Active
	}
	plan.Name = strings.TrimSpace(plan.Name)
	if plan.Name == "" || plan.Price < 0 || plan.MaxGuests < 0 || plan.MaxTeamMembers < 0 || (plan.DurationDays != nil && *plan.DurationDays < 0) {
		writeJSON(w, http.StatusBadRequest, map[string]string{"error": "name is required and numbers cannot be negative"})
		return
	}
	saved, err := s.store.SavePlan(plan)
	if err != nil {
		writeJSON(w, http.StatusInternalServerError, map[string]string{"error": err.Error()})
		return
	}
	status := http.StatusOK
	if id == "" {
		status = http.StatusCreated
	}
	writeJSON(w, status, saved)
}
