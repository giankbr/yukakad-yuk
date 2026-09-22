package api

import (
	"encoding/json"
	"net/http"
	"strings"
)

var siteContentSections = map[string]bool{"hero": true, "kontak": true, "footer": true}

func (s *Server) handlePublicSiteContent(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodGet {
		writeJSON(w, http.StatusMethodNotAllowed, map[string]string{"error": "method not allowed"})
		return
	}
	section := strings.TrimPrefix(r.URL.Path, "/api/public/site-content/")
	if !siteContentSections[section] {
		writeJSON(w, http.StatusNotFound, map[string]string{"error": "unknown section"})
		return
	}
	writeJSON(w, http.StatusOK, s.store.GetSiteContent(section))
}

func (s *Server) handleAdminSiteContent(w http.ResponseWriter, r *http.Request) {
	section := strings.TrimPrefix(r.URL.Path, "/api/admin/site-content/")
	if !siteContentSections[section] {
		writeJSON(w, http.StatusNotFound, map[string]string{"error": "unknown section"})
		return
	}
	if r.Method == http.MethodGet {
		if _, ok := s.requireAdmin(w, r); !ok {
			return
		}
		writeJSON(w, http.StatusOK, s.store.GetSiteContent(section))
		return
	}
	if r.Method != http.MethodPut {
		writeJSON(w, http.StatusMethodNotAllowed, map[string]string{"error": "method not allowed"})
		return
	}
	if _, ok := s.requireAdmin(w, r); !ok {
		return
	}
	var payload map[string]any
	if err := json.NewDecoder(r.Body).Decode(&payload); err != nil {
		writeJSON(w, http.StatusBadRequest, map[string]string{"error": "invalid payload"})
		return
	}
	writeJSON(w, http.StatusOK, s.store.UpdateSiteContent(section, payload))
}

func (s *Server) handlePublicFeatures(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodGet {
		writeJSON(w, http.StatusMethodNotAllowed, map[string]string{"error": "method not allowed"})
		return
	}
	writeJSON(w, http.StatusOK, map[string]any{"items": s.store.ListFeatures()})
}

func (s *Server) handleAdminFeatures(w http.ResponseWriter, r *http.Request) {
	if _, ok := s.requireAdmin(w, r); !ok {
		return
	}
	if r.Method == http.MethodGet {
		writeJSON(w, http.StatusOK, map[string]any{"items": s.store.ListFeatures()})
		return
	}
	if r.Method != http.MethodPost {
		writeJSON(w, http.StatusMethodNotAllowed, map[string]string{"error": "method not allowed"})
		return
	}
	var payload struct {
		Title       string `json:"title"`
		Description string `json:"description"`
		Icon        string `json:"icon"`
	}
	if err := json.NewDecoder(r.Body).Decode(&payload); err != nil {
		writeJSON(w, http.StatusBadRequest, map[string]string{"error": "invalid payload"})
		return
	}
	if payload.Title == "" || payload.Description == "" {
		writeJSON(w, http.StatusBadRequest, map[string]string{"error": "title and description are required"})
		return
	}
	created, err := s.store.CreateFeature(payload.Title, payload.Description, payload.Icon)
	if err != nil {
		writeJSON(w, http.StatusBadRequest, map[string]string{"error": err.Error()})
		return
	}
	writeJSON(w, http.StatusCreated, created)
}

func (s *Server) handleAdminFeatureDetail(w http.ResponseWriter, r *http.Request) {
	if _, ok := s.requireAdmin(w, r); !ok {
		return
	}
	id := strings.TrimPrefix(r.URL.Path, "/api/admin/features/")
	if r.Method == http.MethodPatch {
		var payload struct {
			Title       string `json:"title"`
			Description string `json:"description"`
			Icon        string `json:"icon"`
		}
		if err := json.NewDecoder(r.Body).Decode(&payload); err != nil {
			writeJSON(w, http.StatusBadRequest, map[string]string{"error": "invalid payload"})
			return
		}
		updated, err := s.store.UpdateFeature(id, payload.Title, payload.Description, payload.Icon)
		if err != nil {
			writeJSON(w, http.StatusNotFound, map[string]string{"error": err.Error()})
			return
		}
		writeJSON(w, http.StatusOK, updated)
		return
	}
	if r.Method != http.MethodDelete {
		writeJSON(w, http.StatusMethodNotAllowed, map[string]string{"error": "method not allowed"})
		return
	}
	if err := s.store.DeleteFeature(id); err != nil {
		writeJSON(w, http.StatusNotFound, map[string]string{"error": err.Error()})
		return
	}
	w.WriteHeader(http.StatusNoContent)
}

func (s *Server) handlePublicTestimonials(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodGet {
		writeJSON(w, http.StatusMethodNotAllowed, map[string]string{"error": "method not allowed"})
		return
	}
	writeJSON(w, http.StatusOK, map[string]any{"items": s.store.ListTestimonials()})
}

func (s *Server) handleAdminTestimonials(w http.ResponseWriter, r *http.Request) {
	if _, ok := s.requireAdmin(w, r); !ok {
		return
	}
	if r.Method == http.MethodGet {
		writeJSON(w, http.StatusOK, map[string]any{"items": s.store.ListTestimonials()})
		return
	}
	if r.Method != http.MethodPost {
		writeJSON(w, http.StatusMethodNotAllowed, map[string]string{"error": "method not allowed"})
		return
	}
	var payload struct {
		Name      string `json:"name"`
		Role      string `json:"role"`
		Quote     string `json:"quote"`
		AvatarURL string `json:"avatar_url"`
	}
	if err := json.NewDecoder(r.Body).Decode(&payload); err != nil {
		writeJSON(w, http.StatusBadRequest, map[string]string{"error": "invalid payload"})
		return
	}
	if payload.Name == "" || payload.Quote == "" {
		writeJSON(w, http.StatusBadRequest, map[string]string{"error": "name and quote are required"})
		return
	}
	created, err := s.store.CreateTestimonial(payload.Name, payload.Role, payload.Quote, payload.AvatarURL)
	if err != nil {
		writeJSON(w, http.StatusBadRequest, map[string]string{"error": err.Error()})
		return
	}
	writeJSON(w, http.StatusCreated, created)
}

func (s *Server) handleAdminTestimonialDetail(w http.ResponseWriter, r *http.Request) {
	if _, ok := s.requireAdmin(w, r); !ok {
		return
	}
	id := strings.TrimPrefix(r.URL.Path, "/api/admin/testimonials/")
	if r.Method == http.MethodPatch {
		var payload struct {
			Name      string `json:"name"`
			Role      string `json:"role"`
			Quote     string `json:"quote"`
			AvatarURL string `json:"avatar_url"`
		}
		if err := json.NewDecoder(r.Body).Decode(&payload); err != nil {
			writeJSON(w, http.StatusBadRequest, map[string]string{"error": "invalid payload"})
			return
		}
		updated, err := s.store.UpdateTestimonial(id, payload.Name, payload.Role, payload.Quote, payload.AvatarURL)
		if err != nil {
			writeJSON(w, http.StatusNotFound, map[string]string{"error": err.Error()})
			return
		}
		writeJSON(w, http.StatusOK, updated)
		return
	}
	if r.Method != http.MethodDelete {
		writeJSON(w, http.StatusMethodNotAllowed, map[string]string{"error": "method not allowed"})
		return
	}
	if err := s.store.DeleteTestimonial(id); err != nil {
		writeJSON(w, http.StatusNotFound, map[string]string{"error": err.Error()})
		return
	}
	w.WriteHeader(http.StatusNoContent)
}

func (s *Server) handlePublicPlans(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodGet {
		writeJSON(w, http.StatusMethodNotAllowed, map[string]string{"error": "method not allowed"})
		return
	}
	writeJSON(w, http.StatusOK, map[string]any{"items": s.store.ListPlans()})
}
