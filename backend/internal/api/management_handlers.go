package api

import (
	"encoding/json"
	"errors"
	"net/http"
	"regexp"
	"strings"
	"yukakad/internal/store"
	wishservice "yukakad/internal/wishes"
)

func (s *Server) handleInvitationManagement(w http.ResponseWriter, r *http.Request, invitationID, resource string) {
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
	case "rsvp-summary":
		if r.Method != http.MethodGet {
			writeJSON(w, http.StatusMethodNotAllowed, map[string]string{"error": "method not allowed"})
			return
		}
		summary, err := s.rsvps.Summary(claims.UserID, invitationID)
		if err != nil {
			writeJSON(w, http.StatusNotFound, map[string]string{"error": err.Error()})
			return
		}
		writeJSON(w, http.StatusOK, summary)
	case "rsvps":
		if r.Method != http.MethodGet {
			writeJSON(w, http.StatusMethodNotAllowed, map[string]string{"error": "method not allowed"})
			return
		}
		items, err := s.rsvps.List(claims.UserID, invitationID)
		if err != nil {
			writeJSON(w, http.StatusNotFound, map[string]string{"error": err.Error()})
			return
		}
		writeJSON(w, http.StatusOK, map[string]any{"items": items})
	case "wishes":
		s.handleManagedWishes(w, r, claims.UserID, invitationID)
	case "gifts":
		s.handleManagedGifts(w, r, invitationID, claims.UserID)
	default:
		writeJSON(w, http.StatusNotFound, map[string]string{"error": "resource not found"})
	}
}

func (s *Server) handleManagedWishes(w http.ResponseWriter, r *http.Request, ownerID, invitationID string) {
	if r.Method == http.MethodGet {
		items, err := s.wishes.List(ownerID, invitationID)
		if err != nil {
			writeJSON(w, http.StatusNotFound, map[string]string{"error": err.Error()})
			return
		}
		writeJSON(w, http.StatusOK, map[string]any{"items": items})
		return
	}
	if r.Method != http.MethodPatch {
		writeJSON(w, http.StatusMethodNotAllowed, map[string]string{"error": "method not allowed"})
		return
	}

	wishID := strings.TrimSuffix(strings.TrimPrefix(r.URL.Path, "/api/invitations/"+invitationID+"/wishes/"), "/")
	if wishID == "" {
		writeJSON(w, http.StatusBadRequest, map[string]string{"error": "wish id is required"})
		return
	}
	var payload struct {
		Status string `json:"status"`
	}
	if err := json.NewDecoder(r.Body).Decode(&payload); err != nil {
		writeJSON(w, http.StatusBadRequest, map[string]string{"error": "invalid payload"})
		return
	}
	wish, err := s.wishes.Moderate(ownerID, invitationID, wishID, payload.Status)
	if err != nil {
		status := http.StatusBadRequest
		if errors.Is(err, wishservice.ErrNotFound) {
			status = http.StatusNotFound
		}
		writeJSON(w, status, map[string]string{"error": err.Error()})
		return
	}
	writeJSON(w, http.StatusOK, wish)
}

var bankAccountNumberPattern = regexp.MustCompile(`^[0-9]{6,20}$`)
var ewalletNumberPattern = regexp.MustCompile(`^08[0-9]{8,12}$`)
var validEwalletProviders = map[string]bool{"gopay": true, "ovo": true, "dana": true, "shopeepay": true}

func validateGift(gift store.Gift) string {
	switch gift.Type {
	case "bank":
		if strings.TrimSpace(gift.BankName) == "" {
			return "bank_name is required"
		}
		if !bankAccountNumberPattern.MatchString(gift.AccountNumber) {
			return "account_number must be 6-20 digits"
		}
		if strings.TrimSpace(gift.AccountName) == "" {
			return "account_name is required"
		}
	case "ewallet":
		if !validEwalletProviders[gift.EwalletProvider] {
			return "ewallet_provider must be one of gopay, ovo, dana, shopeepay"
		}
		if !ewalletNumberPattern.MatchString(gift.EwalletNumber) {
			return "ewallet_number must be a valid Indonesian phone number starting with 08"
		}
	case "qris":
		if strings.TrimSpace(gift.QRISImageURL) == "" {
			return "qris_image_url is required (upload the QRIS image first)"
		}
	case "address":
		if strings.TrimSpace(gift.Address) == "" {
			return "address is required"
		}
	default:
		return "type must be one of bank, ewallet, qris, address"
	}
	return ""
}

func (s *Server) handleManagedGifts(w http.ResponseWriter, r *http.Request, invitationID, actorUserID string) {
	giftID := strings.TrimSuffix(strings.TrimPrefix(r.URL.Path, "/api/invitations/"+invitationID+"/gifts/"), "/")
	if giftID != "" && giftID != r.URL.Path {
		if r.Method != http.MethodPatch {
			writeJSON(w, http.StatusMethodNotAllowed, map[string]string{"error": "method not allowed"})
			return
		}
		var payload struct {
			Active *bool `json:"is_active"`
		}
		if err := json.NewDecoder(r.Body).Decode(&payload); err != nil || payload.Active == nil {
			writeJSON(w, http.StatusBadRequest, map[string]string{"error": "is_active is required"})
			return
		}
		gift, err := s.store.SetGiftActive(giftID, *payload.Active)
		if err != nil || gift.InvitationID != invitationID {
			writeJSON(w, http.StatusNotFound, map[string]string{"error": "gift not found"})
			return
		}
		_ = s.store.CreateAuditLog(actorUserID, invitationID, "gift.toggle", map[string]any{"gift_id": giftID, "is_active": *payload.Active})
		writeJSON(w, http.StatusOK, gift)
		return
	}

	if r.Method == http.MethodGet {
		writeJSON(w, http.StatusOK, map[string]any{"items": s.store.ListGifts(invitationID)})
		return
	}
	if r.Method != http.MethodPost {
		writeJSON(w, http.StatusMethodNotAllowed, map[string]string{"error": "method not allowed"})
		return
	}
	var gift store.Gift
	if err := json.NewDecoder(r.Body).Decode(&gift); err != nil {
		writeJSON(w, http.StatusBadRequest, map[string]string{"error": "invalid payload"})
		return
	}
	if msg := validateGift(gift); msg != "" {
		writeJSON(w, http.StatusBadRequest, map[string]string{"error": msg})
		return
	}
	gift.Active = true
	created, err := s.store.CreateGift(invitationID, gift)
	if err != nil {
		writeJSON(w, http.StatusBadRequest, map[string]string{"error": err.Error()})
		return
	}
	_ = s.store.CreateAuditLog(actorUserID, invitationID, "gift.create", map[string]any{"gift_id": created.ID, "type": created.Type})
	writeJSON(w, http.StatusCreated, created)
}

func (s *Server) handleTemplates(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodGet {
		writeJSON(w, http.StatusMethodNotAllowed, map[string]string{"error": "method not allowed"})
		return
	}
	id := strings.Trim(strings.TrimPrefix(r.URL.Path, "/api/templates"), "/")
	if id != "" {
		var item *store.Template
		var ok bool
		if strings.HasPrefix(id, "slug/") {
			item, ok = s.store.FindTemplateBySlug(strings.TrimPrefix(id, "slug/"))
		} else {
			item, ok = s.store.FindTemplate(id)
		}
		if !ok || item.Status != "active" {
			writeJSON(w, http.StatusNotFound, map[string]string{"error": "template not found"})
			return
		}
		writeJSON(w, http.StatusOK, item)
		return
	}
	items := s.templates.List()
	eventType, category, tier, tag, search := r.URL.Query().Get("event_type"), r.URL.Query().Get("category"), r.URL.Query().Get("tier"), r.URL.Query().Get("tag"), strings.ToLower(strings.TrimSpace(r.URL.Query().Get("search")))
	filtered := make([]*store.Template, 0, len(items))
	for _, item := range items {
		if eventType != "" && item.EventType != eventType {
			continue
		}
		if tag != "" {
			foundTag := false
			for _, itemTag := range item.Tags {
				if itemTag == tag {
					foundTag = true
					break
				}
			}
			if !foundTag {
				continue
			}
		}
		if category != "" && item.Category != category {
			continue
		}
		if tier != "" && item.Tier != tier {
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
}
