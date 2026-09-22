package api

import (
	"encoding/csv"
	"encoding/json"
	"errors"
	"io"
	"net/http"
	"strings"
	"time"
	guestservice "yukakad/internal/guests"
	rsvpservice "yukakad/internal/rsvp"
	"yukakad/internal/store"
	wishservice "yukakad/internal/wishes"
)

func (s *Server) handleInvitationGuests(w http.ResponseWriter, r *http.Request, invitationID string) {
	claims, ok := s.requireAuth(w, r)
	if !ok {
		return
	}
	if _, err := s.invitations.Owned(claims.UserID, invitationID); err != nil {
		writeJSON(w, http.StatusNotFound, map[string]string{"error": err.Error()})
		return
	}
	pathID := strings.TrimPrefix(r.URL.Path, "/api/invitations/"+invitationID+"/guests/")
	if pathID != r.URL.Path && pathID != "" {
		if strings.HasSuffix(pathID, "/check-in") {
			guestID := strings.TrimSuffix(pathID, "/check-in")
			if r.Method != http.MethodPost {
				writeJSON(w, http.StatusMethodNotAllowed, map[string]string{"error": "method not allowed"})
				return
			}
			if !s.allowRate(w, "checkin:"+invitationID+":"+clientIP(r), 20, time.Minute) {
				return
			}
			guest, err := s.guests.CheckIn(claims.UserID, invitationID, guestID)
			if err != nil {
				writeJSON(w, http.StatusNotFound, map[string]string{"error": err.Error()})
				return
			}
			_ = s.store.CreateAuditLog(claims.UserID, invitationID, "guest.check_in", map[string]any{"guest_id": guestID})
			writeJSON(w, http.StatusOK, guest)
			return
		}
		guestID := pathID
		if r.Method == http.MethodDelete {
			if err := s.guests.Delete(claims.UserID, invitationID, guestID); err != nil {
				writeJSON(w, http.StatusNotFound, map[string]string{"error": err.Error()})
				return
			}
			w.WriteHeader(http.StatusNoContent)
			return
		}
		if r.Method == http.MethodPut || r.Method == http.MethodPatch {
			var payload struct {
				Name     string `json:"name"`
				Phone    string `json:"phone"`
				Category string `json:"category"`
			}
			if err := json.NewDecoder(r.Body).Decode(&payload); err != nil || strings.TrimSpace(payload.Name) == "" {
				writeJSON(w, http.StatusBadRequest, map[string]string{"error": "name is required"})
				return
			}
			guest, err := s.guests.Update(claims.UserID, invitationID, guestID, payload.Name, payload.Phone, payload.Category)
			if err != nil {
				status := http.StatusNotFound
				if errors.Is(err, guestservice.ErrInvalid) {
					status = http.StatusBadRequest
				}
				writeJSON(w, status, map[string]string{"error": err.Error()})
				return
			}
			writeJSON(w, http.StatusOK, guest)
			return
		}
	}

	if r.Method == http.MethodGet {
		search := strings.TrimSpace(r.URL.Query().Get("search"))
		category := strings.TrimSpace(r.URL.Query().Get("category"))
		items, err := s.guests.List(claims.UserID, invitationID, search, category)
		if err != nil {
			writeJSON(w, http.StatusNotFound, map[string]string{"error": err.Error()})
			return
		}
		if isV1(r) {
			start, end, meta := paginateRequest(r, len(items))
			writeJSON(w, http.StatusOK, map[string]any{"items": items[start:end], "pagination": meta})
		} else {
			writeJSON(w, http.StatusOK, map[string]any{"items": items})
		}
		return
	}
	if r.Method == http.MethodPost {
		if r.Header.Get("Content-Type") == "text/csv" {
			reader := csv.NewReader(r.Body)
			created := make([]*store.Guest, 0)
			for {
				record, err := reader.Read()
				if err == io.EOF {
					break
				}
				if err != nil || len(record) < 1 {
					writeJSON(w, http.StatusBadRequest, map[string]string{"error": "invalid CSV"})
					return
				}
				if strings.EqualFold(strings.TrimSpace(record[0]), "name") {
					continue
				}
				phone, category := "", "family"
				if len(record) > 1 {
					phone = strings.TrimSpace(record[1])
				}
				if len(record) > 2 && strings.TrimSpace(record[2]) != "" {
					category = strings.TrimSpace(record[2])
				}
				guest, err := s.guests.Create(claims.UserID, invitationID, record[0], phone, category)
				if err != nil {
					status := http.StatusBadRequest
					if errors.Is(err, guestservice.ErrNotFound) {
						status = http.StatusNotFound
					}
					if errors.Is(err, guestservice.ErrQuotaExceeded) {
						status = http.StatusUnprocessableEntity
					}
					if errors.Is(err, guestservice.ErrPlanUnavailable) {
						status = http.StatusServiceUnavailable
					}
					writeJSON(w, status, map[string]string{"error": err.Error()})
					return
				}
				created = append(created, guest)
			}
			writeJSON(w, http.StatusCreated, map[string]any{"items": created})
			return
		}
		var payload struct {
			Name     string `json:"name"`
			Phone    string `json:"phone"`
			Category string `json:"category"`
		}
		if err := json.NewDecoder(r.Body).Decode(&payload); err != nil || strings.TrimSpace(payload.Name) == "" {
			writeJSON(w, http.StatusBadRequest, map[string]string{"error": "name is required"})
			return
		}
		if payload.Category == "" {
			payload.Category = "family"
		}
		guest, err := s.guests.Create(claims.UserID, invitationID, payload.Name, payload.Phone, payload.Category)
		if err != nil {
			status := http.StatusBadRequest
			if errors.Is(err, guestservice.ErrNotFound) {
				status = http.StatusNotFound
			}
			if errors.Is(err, guestservice.ErrQuotaExceeded) {
				status = http.StatusUnprocessableEntity
			}
			if errors.Is(err, guestservice.ErrPlanUnavailable) {
				status = http.StatusServiceUnavailable
			}
			writeJSON(w, status, map[string]string{"error": err.Error()})
			return
		}
		writeJSON(w, http.StatusCreated, guest)
		return
	}
	writeJSON(w, http.StatusMethodNotAllowed, map[string]string{"error": "method not allowed"})
}

func (s *Server) handlePublicRSVP(w http.ResponseWriter, r *http.Request, slug string) {
	invitation, exists := s.store.FindInvitationBySlug(slug)
	if !exists || !invitation.Published {
		writeJSON(w, http.StatusNotFound, map[string]string{"error": "invitation not found"})
		return
	}
	if r.Method != http.MethodPost {
		writeJSON(w, http.StatusMethodNotAllowed, map[string]string{"error": "method not allowed"})
		return
	}
	if !s.allowRate(w, "rsvp:"+invitation.ID+":"+clientIP(r), 5, time.Minute) {
		return
	}

	var payload struct {
		GuestID        string `json:"guest_id"`
		GuestToken     string `json:"guest_token"`
		Attendance     string `json:"attendance"`
		AttendeesCount int    `json:"attendees_count"`
		Message        string `json:"message"`
	}
	if err := json.NewDecoder(r.Body).Decode(&payload); err != nil || (payload.Attendance != "yes" && payload.Attendance != "no" && payload.Attendance != "maybe") {
		writeJSON(w, http.StatusBadRequest, map[string]string{"error": "attendance must be yes, no, or maybe"})
		return
	}
	if payload.AttendeesCount < 0 {
		writeJSON(w, http.StatusBadRequest, map[string]string{"error": "attendees_count cannot be negative"})
		return
	}
	rsvp, err := s.rsvps.Submit(invitation.ID, payload.GuestID, payload.GuestToken, payload.Attendance, payload.AttendeesCount, payload.Message)
	if err != nil {
		status := http.StatusBadRequest
		if errors.Is(err, rsvpservice.ErrNotFound) {
			status = http.StatusNotFound
		}
		writeJSON(w, status, map[string]string{"error": err.Error()})
		return
	}
	writeJSON(w, http.StatusCreated, rsvp)
}

func (s *Server) handlePublicWishes(w http.ResponseWriter, r *http.Request, slug string) {
	invitation, exists := s.store.FindInvitationBySlug(slug)
	if !exists || !invitation.Published {
		writeJSON(w, http.StatusNotFound, map[string]string{"error": "invitation not found"})
		return
	}

	if r.Method == http.MethodGet {
		writeJSON(w, http.StatusOK, map[string]any{"items": s.wishes.Published(invitation.ID)})
		return
	}
	if r.Method == http.MethodPost {
		if !s.allowRate(w, "wishes:"+invitation.ID+":"+clientIP(r), 5, time.Minute) {
			return
		}
		var payload struct {
			GuestID    string `json:"guest_id"`
			GuestToken string `json:"guest_token"`
			Name       string `json:"name"`
			Message    string `json:"message"`
		}
		if err := json.NewDecoder(r.Body).Decode(&payload); err != nil || strings.TrimSpace(payload.Name) == "" || strings.TrimSpace(payload.Message) == "" {
			writeJSON(w, http.StatusBadRequest, map[string]string{"error": "name and message are required"})
			return
		}
		wish, err := s.wishes.Create(invitation.ID, payload.GuestID, payload.GuestToken, payload.Name, payload.Message)
		if err != nil {
			status := http.StatusBadRequest
			if errors.Is(err, wishservice.ErrNotFound) {
				status = http.StatusNotFound
			}
			writeJSON(w, status, map[string]string{"error": err.Error()})
			return
		}
		writeJSON(w, http.StatusCreated, wish)
		return
	}
	writeJSON(w, http.StatusMethodNotAllowed, map[string]string{"error": "method not allowed"})
}
