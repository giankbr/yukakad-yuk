package api

import (
	"encoding/json"
	"errors"
	"net/http"
	"strings"
	"yukakad/internal/store"
	templateservice "yukakad/internal/templates"
)

func (s *Server) handleInvitationContent(w http.ResponseWriter, r *http.Request, invitationID, resource string) {
	claims, ok := s.requireAuth(w, r)
	if !ok {
		return
	}
	invitation, exists := s.store.FindInvitationByID(invitationID)
	if !exists {
		writeJSON(w, http.StatusNotFound, map[string]string{"error": "invitation not found"})
		return
	}
	if invitation.UserID != claims.UserID {
		writeJSON(w, http.StatusForbidden, map[string]string{"error": "forbidden"})
		return
	}

	switch resource {
	case "settings":
		if r.Method == http.MethodGet {
			writeJSON(w, http.StatusOK, s.store.GetSettings(invitationID))
			return
		}
		if r.Method == http.MethodPatch {
			var payload map[string]any
			if json.NewDecoder(r.Body).Decode(&payload) != nil {
				writeJSON(w, http.StatusBadRequest, map[string]string{"error": "invalid payload"})
				return
			}
			writeJSON(w, http.StatusOK, s.store.UpdateSettings(invitationID, payload))
			return
		}
	case "stories":
		if r.Method == http.MethodGet {
			writeJSON(w, http.StatusOK, map[string]any{"items": s.store.ListStories(invitationID)})
			return
		}
		if r.Method == http.MethodPost {
			var payload struct {
				Title   string `json:"title"`
				Content string `json:"content"`
			}
			if json.NewDecoder(r.Body).Decode(&payload) != nil || strings.TrimSpace(payload.Content) == "" {
				writeJSON(w, http.StatusBadRequest, map[string]string{"error": "content is required"})
				return
			}
			story, err := s.store.CreateStory(invitationID, payload.Title, payload.Content)
			if err != nil {
				writeJSON(w, http.StatusBadRequest, map[string]string{"error": err.Error()})
				return
			}
			writeJSON(w, http.StatusCreated, story)
			return
		}
	case "gallery":
		if r.Method == http.MethodGet {
			writeJSON(w, http.StatusOK, map[string]any{"items": s.store.ListGallery(invitationID)})
			return
		}
		if r.Method == http.MethodPost {
			var payload struct {
				ImageURL string `json:"image_url"`
				Caption  string `json:"caption"`
			}
			if json.NewDecoder(r.Body).Decode(&payload) != nil || strings.TrimSpace(payload.ImageURL) == "" {
				writeJSON(w, http.StatusBadRequest, map[string]string{"error": "image_url is required"})
				return
			}
			image, err := s.store.CreateGallery(invitationID, payload.ImageURL, payload.Caption)
			if err != nil {
				writeJSON(w, http.StatusBadRequest, map[string]string{"error": err.Error()})
				return
			}
			writeJSON(w, http.StatusCreated, image)
			return
		}
	case "template":
		if r.Method != http.MethodPut {
			writeJSON(w, http.StatusMethodNotAllowed, map[string]string{"error": "method not allowed"})
			return
		}
		var payload struct {
			TemplateID string `json:"template_id"`
		}
		if json.NewDecoder(r.Body).Decode(&payload) != nil || payload.TemplateID == "" {
			writeJSON(w, http.StatusBadRequest, map[string]string{"error": "template_id is required"})
			return
		}
		if err := s.templates.Assign(claims.UserID, invitationID, payload.TemplateID); err != nil {
			status := http.StatusBadRequest
			if errors.Is(err, templateservice.ErrNotFound) {
				status = http.StatusNotFound
			}
			if errors.Is(err, templateservice.ErrPremiumDenied) {
				status = http.StatusForbidden
			}
			writeJSON(w, status, map[string]string{"error": err.Error()})
			return
		}
		writeJSON(w, http.StatusOK, map[string]string{"template_id": payload.TemplateID})
		return
	}
	writeJSON(w, http.StatusMethodNotAllowed, map[string]string{"error": "method not allowed"})
}

func (s *Server) handlePublicContent(w http.ResponseWriter, r *http.Request, slug, resource string) {
	if r.Method != http.MethodGet {
		writeJSON(w, http.StatusMethodNotAllowed, map[string]string{"error": "method not allowed"})
		return
	}
	invitation, exists := s.store.FindInvitationBySlug(slug)
	if !exists || (!invitation.Published && !s.canPreviewUnpublished(r, invitation)) {
		writeJSON(w, http.StatusNotFound, map[string]string{"error": "invitation not found"})
		return
	}
	switch resource {
	case "gallery":
		writeJSON(w, http.StatusOK, map[string]any{"items": s.store.ListGallery(invitation.ID)})
	case "stories":
		writeJSON(w, http.StatusOK, map[string]any{"items": s.store.ListStories(invitation.ID)})
	case "settings":
		writeJSON(w, http.StatusOK, s.store.GetSettings(invitation.ID))
	default:
		writeJSON(w, http.StatusNotFound, map[string]string{"error": "resource not found"})
	}
}

// handleInvitationEventsCollection handles GET (list) and POST (create) for multi-events.
// Route: /api/invitations/{invitationID}/events
func (s *Server) handleInvitationEventsCollection(w http.ResponseWriter, r *http.Request, invitationID string) {
	claims, ok := s.requireAuth(w, r)
	if !ok {
		return
	}
	invitation, exists := s.store.FindInvitationByID(invitationID)
	if !exists {
		writeJSON(w, http.StatusNotFound, map[string]string{"error": "invitation not found"})
		return
	}
	if invitation.UserID != claims.UserID {
		writeJSON(w, http.StatusForbidden, map[string]string{"error": "forbidden"})
		return
	}

	if r.Method == http.MethodGet {
		writeJSON(w, http.StatusOK, map[string]any{"items": s.store.ListInvitationEvents(invitationID)})
		return
	}
	if r.Method == http.MethodPost {
		var payload struct {
			Title     string  `json:"title"`
			Type      string  `json:"type"`
			Date      string  `json:"date"`
			StartTime string  `json:"start_time"`
			EndTime   string  `json:"end_time"`
			Venue     string  `json:"venue"`
			Address   string  `json:"address"`
			MapsURL   string  `json:"maps_url"`
			Latitude  float64 `json:"latitude"`
			Longitude float64 `json:"longitude"`
			SortOrder int     `json:"sort_order"`
		}
		if err := json.NewDecoder(r.Body).Decode(&payload); err != nil {
			writeJSON(w, http.StatusBadRequest, map[string]string{"error": "invalid payload"})
			return
		}
		if strings.TrimSpace(payload.Title) == "" || strings.TrimSpace(payload.Venue) == "" {
			writeJSON(w, http.StatusBadRequest, map[string]string{"error": "title and venue are required"})
			return
		}
		if payload.Type == "" {
			payload.Type = "reception"
		}
		ev, err := s.store.CreateInvitationEvent(invitationID, store.InvitationEvent{
			Title:     payload.Title,
			Type:      payload.Type,
			Date:      payload.Date,
			StartTime: payload.StartTime,
			EndTime:   payload.EndTime,
			Venue:     payload.Venue,
			Address:   payload.Address,
			MapsURL:   payload.MapsURL,
			Latitude:  payload.Latitude,
			Longitude: payload.Longitude,
			SortOrder: payload.SortOrder,
		})
		if err != nil {
			writeJSON(w, http.StatusBadRequest, map[string]string{"error": err.Error()})
			return
		}
		_ = s.store.CreateAuditLog(claims.UserID, invitationID, "event.create", map[string]any{"event_id": ev.ID})
		writeJSON(w, http.StatusCreated, ev)
		return
	}
	writeJSON(w, http.StatusMethodNotAllowed, map[string]string{"error": "method not allowed"})
}

// handleInvitationEventDetail handles PUT (update) and DELETE for a specific event.
// Route: /api/invitations/{invitationID}/events/{eventID}
func (s *Server) handleInvitationEventDetail(w http.ResponseWriter, r *http.Request, invitationID, eventID string) {
	claims, ok := s.requireAuth(w, r)
	if !ok {
		return
	}
	invitation, exists := s.store.FindInvitationByID(invitationID)
	if !exists {
		writeJSON(w, http.StatusNotFound, map[string]string{"error": "invitation not found"})
		return
	}
	if invitation.UserID != claims.UserID {
		writeJSON(w, http.StatusForbidden, map[string]string{"error": "forbidden"})
		return
	}

	if r.Method == http.MethodPut || r.Method == http.MethodPatch {
		var payload struct {
			Title     string  `json:"title"`
			Type      string  `json:"type"`
			Date      string  `json:"date"`
			StartTime string  `json:"start_time"`
			EndTime   string  `json:"end_time"`
			Venue     string  `json:"venue"`
			Address   string  `json:"address"`
			MapsURL   string  `json:"maps_url"`
			Latitude  float64 `json:"latitude"`
			Longitude float64 `json:"longitude"`
			SortOrder int     `json:"sort_order"`
		}
		if err := json.NewDecoder(r.Body).Decode(&payload); err != nil {
			writeJSON(w, http.StatusBadRequest, map[string]string{"error": "invalid payload"})
			return
		}
		if strings.TrimSpace(payload.Title) == "" || strings.TrimSpace(payload.Venue) == "" {
			writeJSON(w, http.StatusBadRequest, map[string]string{"error": "title and venue are required"})
			return
		}
		updated, err := s.store.UpdateInvitationEvent(eventID, store.InvitationEvent{
			Title:     payload.Title,
			Type:      payload.Type,
			Date:      payload.Date,
			StartTime: payload.StartTime,
			EndTime:   payload.EndTime,
			Venue:     payload.Venue,
			Address:   payload.Address,
			MapsURL:   payload.MapsURL,
			Latitude:  payload.Latitude,
			Longitude: payload.Longitude,
			SortOrder: payload.SortOrder,
		})
		if err != nil {
			writeJSON(w, http.StatusNotFound, map[string]string{"error": err.Error()})
			return
		}
		writeJSON(w, http.StatusOK, updated)
		return
	}
	if r.Method == http.MethodDelete {
		if err := s.store.DeleteInvitationEvent(eventID); err != nil {
			writeJSON(w, http.StatusNotFound, map[string]string{"error": err.Error()})
			return
		}
		_ = s.store.CreateAuditLog(claims.UserID, invitationID, "event.delete", map[string]any{"event_id": eventID})
		w.WriteHeader(http.StatusNoContent)
		return
	}
	writeJSON(w, http.StatusMethodNotAllowed, map[string]string{"error": "method not allowed"})
}

// handleGalleryItemDetail handles DELETE for a specific gallery item.
// Route: /api/invitations/{invitationID}/gallery/{galleryID}
func (s *Server) handleGalleryItemDetail(w http.ResponseWriter, r *http.Request, invitationID, galleryID string) {
	claims, ok := s.requireAuth(w, r)
	if !ok {
		return
	}
	invitation, exists := s.store.FindInvitationByID(invitationID)
	if !exists {
		writeJSON(w, http.StatusNotFound, map[string]string{"error": "invitation not found"})
		return
	}
	if invitation.UserID != claims.UserID {
		writeJSON(w, http.StatusForbidden, map[string]string{"error": "forbidden"})
		return
	}
	if r.Method != http.MethodDelete {
		writeJSON(w, http.StatusMethodNotAllowed, map[string]string{"error": "method not allowed"})
		return
	}
	gallery, found := s.store.FindGalleryItem(galleryID)
	if !found || gallery["invitation_id"] != invitationID {
		writeJSON(w, http.StatusNotFound, map[string]string{"error": "gallery item not found"})
		return
	}
	if err := s.store.DeleteGalleryItem(galleryID); err != nil {
		writeJSON(w, http.StatusNotFound, map[string]string{"error": err.Error()})
		return
	}
	w.WriteHeader(http.StatusNoContent)
}

// handleStoryItemDetail handles DELETE for a specific story.
// Route: /api/invitations/{invitationID}/stories/{storyID}
func (s *Server) handleStoryItemDetail(w http.ResponseWriter, r *http.Request, invitationID, storyID string) {
	claims, ok := s.requireAuth(w, r)
	if !ok {
		return
	}
	invitation, exists := s.store.FindInvitationByID(invitationID)
	if !exists {
		writeJSON(w, http.StatusNotFound, map[string]string{"error": "invitation not found"})
		return
	}
	if invitation.UserID != claims.UserID {
		writeJSON(w, http.StatusForbidden, map[string]string{"error": "forbidden"})
		return
	}
	if r.Method != http.MethodDelete {
		writeJSON(w, http.StatusMethodNotAllowed, map[string]string{"error": "method not allowed"})
		return
	}
	if err := s.store.DeleteStoryItem(storyID); err != nil {
		writeJSON(w, http.StatusNotFound, map[string]string{"error": err.Error()})
		return
	}
	w.WriteHeader(http.StatusNoContent)
}
