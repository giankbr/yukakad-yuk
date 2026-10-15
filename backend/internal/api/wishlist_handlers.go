package api

import (
	"encoding/json"
	"net/http"
	"strings"
	"sync"
	"time"
)

// wishlistMu serialises claims so two guests can't reserve the same gift at the same moment.
var wishlistMu sync.Mutex

// handlePublicWishlistClaim lets a guest mark a wishlist gift as "I'll buy this".
// The wishlist lives in the invitation settings (sections_config.wishlist.items), managed from the dashboard.
// Route: POST /api/public/invitation/{slug}/wishlist/claim  {"item_id": "...", "name": "..."}
func (s *Server) handlePublicWishlistClaim(w http.ResponseWriter, r *http.Request, slug string) {
	if r.Method != http.MethodPost {
		writeJSON(w, http.StatusMethodNotAllowed, map[string]string{"error": "method not allowed"})
		return
	}
	invitation, exists := s.store.FindInvitationBySlug(slug)
	if !exists || !invitation.Published {
		writeJSON(w, http.StatusNotFound, map[string]string{"error": "invitation not found"})
		return
	}
	if !s.allowRate(w, "wishlist:"+invitation.ID+":"+clientIP(r), 10, time.Minute) {
		return
	}
	var payload struct {
		ItemID string `json:"item_id"`
		Name   string `json:"name"`
	}
	if err := json.NewDecoder(http.MaxBytesReader(w, r.Body, 4096)).Decode(&payload); err != nil {
		writeJSON(w, http.StatusBadRequest, map[string]string{"error": "invalid payload"})
		return
	}
	name := strings.TrimSpace(payload.Name)
	if payload.ItemID == "" || name == "" {
		writeJSON(w, http.StatusBadRequest, map[string]string{"error": "item_id and name are required"})
		return
	}
	if runes := []rune(name); len(runes) > 60 {
		name = string(runes[:60])
	}

	wishlistMu.Lock()
	defer wishlistMu.Unlock()

	settings := s.store.GetSettings(invitation.ID)
	config, _ := settings["sections_config"].(map[string]any)
	wishlist, _ := config["wishlist"].(map[string]any)
	items, _ := wishlist["items"].([]any)
	for index, raw := range items {
		item, ok := raw.(map[string]any)
		if !ok {
			continue
		}
		if id, _ := item["id"].(string); id != payload.ItemID {
			continue
		}
		if claimed, _ := item["claimed_by"].(string); strings.TrimSpace(claimed) != "" {
			writeJSON(w, http.StatusConflict, map[string]string{"error": "gift already claimed"})
			return
		}
		item["claimed_by"] = name
		item["claimed_at"] = time.Now().UTC().Format(time.RFC3339)
		items[index] = item
		wishlist["items"] = items
		config["wishlist"] = wishlist
		s.store.UpdateSettings(invitation.ID, map[string]any{"sections_config": config})
		writeJSON(w, http.StatusOK, map[string]any{"item_id": payload.ItemID, "claimed_by": name})
		return
	}
	writeJSON(w, http.StatusNotFound, map[string]string{"error": "gift not found"})
}
