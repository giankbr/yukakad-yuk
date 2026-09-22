package api

import (
	"bytes"
	"encoding/json"
	"errors"
	"io"
	"net/http"
	"strings"
	mediaservice "yukakad/internal/media"
	"yukakad/internal/store"
	templateservice "yukakad/internal/templates"
)

func (s *Server) handleAdminTemplates(w http.ResponseWriter, r *http.Request) {
	if _, ok := s.requireAdmin(w, r); !ok {
		return
	}
	id := strings.Trim(strings.TrimPrefix(r.URL.Path, "/api/admin/templates"), "/")
	if r.Method == http.MethodGet && id == "" {
		items := s.templates.ListAdmin()
		query := r.URL.Query()
		status, eventType, tier := query.Get("status"), query.Get("event_type"), query.Get("tier")
		search := strings.ToLower(strings.TrimSpace(query.Get("search")))
		filtered := make([]*store.Template, 0, len(items))
		for _, item := range items {
			if status != "" && item.Status != status || eventType != "" && item.EventType != eventType || tier != "" && item.Tier != tier {
				continue
			}
			if search != "" && !strings.Contains(strings.ToLower(item.Name+" "+item.Description+" "+item.Slug), search) {
				continue
			}
			filtered = append(filtered, item)
		}
		if isV1(r) {
			start, end, meta := paginateRequest(r, len(filtered))
			writeJSON(w, http.StatusOK, map[string]any{"items": filtered[start:end], "pagination": meta})
			return
		}
		writeJSON(w, http.StatusOK, map[string]any{"items": filtered})
		return
	}
	if r.Method == http.MethodPost && id == "" {
		var item store.Template
		if json.NewDecoder(r.Body).Decode(&item) != nil {
			writeJSON(w, http.StatusBadRequest, map[string]string{"error": "invalid payload"})
			return
		}
		created, err := s.templates.Create(item)
		if err != nil {
			writeTemplateError(w, err)
			return
		}
		writeJSON(w, http.StatusCreated, created)
		return
	}
	if id == "" {
		writeJSON(w, http.StatusMethodNotAllowed, map[string]string{"error": "method not allowed"})
		return
	}
	if r.Method == http.MethodPost && strings.HasSuffix(id, "/preview") {
		if s.storage == nil {
			writeJSON(w, http.StatusServiceUnavailable, map[string]string{"error": "object storage is not configured"})
			return
		}
		templateID := strings.TrimSuffix(id, "/preview")
		item, ok := s.store.FindTemplate(templateID)
		if !ok {
			writeJSON(w, http.StatusNotFound, map[string]string{"error": "template not found"})
			return
		}
		r.Body = http.MaxBytesReader(w, r.Body, 10<<20)
		if err := r.ParseMultipartForm(10 << 20); err != nil {
			writeJSON(w, http.StatusRequestEntityTooLarge, map[string]string{"error": "file too large"})
			return
		}
		file, _, err := r.FormFile("file")
		if err != nil {
			writeJSON(w, http.StatusBadRequest, map[string]string{"error": "file is required"})
			return
		}
		defer file.Close()
		data, err := io.ReadAll(file)
		if err != nil {
			writeJSON(w, http.StatusBadRequest, map[string]string{"error": "could not read file"})
			return
		}
		contentType := mediaservice.DetectContentType(data)
		if contentType != "image/jpeg" && contentType != "image/png" && contentType != "image/webp" {
			writeJSON(w, http.StatusBadRequest, map[string]string{"error": "preview must be jpeg, png, or webp"})
			return
		}
		url, err := s.storage.Upload(r.Context(), "templates/"+templateID+"/"+randomID(), bytes.NewReader(data), int64(len(data)), contentType)
		if err != nil {
			writeJSON(w, http.StatusBadGateway, map[string]string{"error": err.Error()})
			return
		}
		oldURL := item.PreviewImage
		item.PreviewImage = url
		updated, err := s.templates.Update(*item)
		if err != nil {
			writeTemplateError(w, err)
			return
		}
		if oldURL != "" {
			_ = s.storage.DeleteURL(r.Context(), oldURL)
		}
		writeJSON(w, http.StatusOK, updated)
		return
	}
	if (r.Method == http.MethodPost) && (id != "" && (strings.HasSuffix(id, "/publish") || strings.HasSuffix(id, "/archive"))) {
		status := "active"
		if strings.HasSuffix(id, "/archive") {
			status = "archived"
		}
		templateID := strings.TrimSuffix(strings.TrimSuffix(id, "/publish"), "/archive")
		item, ok := s.store.FindTemplate(templateID)
		if !ok {
			writeJSON(w, http.StatusNotFound, map[string]string{"error": "template not found"})
			return
		}
		item.Status = status
		updated, err := s.templates.Update(*item)
		if err != nil {
			writeTemplateError(w, err)
			return
		}
		writeJSON(w, http.StatusOK, updated)
		return
	}
	if r.Method == http.MethodGet {
		item, ok := s.store.FindTemplate(id)
		if !ok {
			writeJSON(w, http.StatusNotFound, map[string]string{"error": "template not found"})
			return
		}
		writeJSON(w, http.StatusOK, item)
		return
	}
	if r.Method == http.MethodDelete {
		if err := s.templates.Delete(id); err != nil {
			writeJSON(w, http.StatusNotFound, map[string]string{"error": err.Error()})
			return
		}
		w.WriteHeader(http.StatusNoContent)
		return
	}
	if r.Method == http.MethodPatch || r.Method == http.MethodPut {
		current, ok := s.store.FindTemplate(id)
		if !ok {
			writeJSON(w, http.StatusNotFound, map[string]string{"error": "template not found"})
			return
		}
		var patch map[string]any
		if json.NewDecoder(r.Body).Decode(&patch) != nil {
			writeJSON(w, http.StatusBadRequest, map[string]string{"error": "invalid payload"})
			return
		}
		base, _ := json.Marshal(current)
		merged := map[string]any{}
		_ = json.Unmarshal(base, &merged)
		for key, value := range patch {
			merged[key] = value
		}
		mergedJSON, _ := json.Marshal(merged)
		var item store.Template
		if json.Unmarshal(mergedJSON, &item) != nil {
			writeJSON(w, http.StatusBadRequest, map[string]string{"error": "invalid template payload"})
			return
		}
		item.ID = id
		updated, err := s.templates.Update(item)
		if err != nil {
			writeTemplateError(w, err)
			return
		}
		writeJSON(w, http.StatusOK, updated)
		return
	}
	writeJSON(w, http.StatusMethodNotAllowed, map[string]string{"error": "method not allowed"})
}

func writeTemplateError(w http.ResponseWriter, err error) {
	status := http.StatusBadRequest
	if errors.Is(err, templateservice.ErrNotFound) {
		status = http.StatusNotFound
	}
	writeJSON(w, status, map[string]string{"error": err.Error()})
}
