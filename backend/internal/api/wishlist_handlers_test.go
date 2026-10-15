package api

import (
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"

	"yukakad/internal/config"
)

func TestPublicWishlistClaim(t *testing.T) {
	cfg := config.Config{Port: "8080", Environment: "test", JWTSecret: "secret"}
	server := NewServer(cfg)
	user, _ := server.store.CreateUser("Ayu", "ayu@example.com", "hash")
	invitation, _ := server.store.CreateInvitation(user.ID, "alya-rizky", "Alya & Rizky")
	invitation.Published = true
	server.store.UpdateSettings(invitation.ID, map[string]any{"sections_config": map[string]any{
		"wishlist": map[string]any{"items": []any{map[string]any{"id": "w1", "name": "Rice cooker"}}},
	}})

	claim := func(body string) *httptest.ResponseRecorder {
		req := httptest.NewRequest(http.MethodPost, "/api/public/invitation/alya-rizky/wishlist/claim", strings.NewReader(body))
		recorder := httptest.NewRecorder()
		server.handlePublicInvitation(recorder, req)
		return recorder
	}

	if code := claim(`{"item_id":"w1","name":"Budi"}`).Code; code != http.StatusOK {
		t.Fatalf("first claim expected 200, got %d", code)
	}
	if code := claim(`{"item_id":"w1","name":"Sinta"}`).Code; code != http.StatusConflict {
		t.Fatalf("second claim expected 409, got %d", code)
	}
	if code := claim(`{"item_id":"missing","name":"Budi"}`).Code; code != http.StatusNotFound {
		t.Fatalf("unknown gift expected 404, got %d", code)
	}
	if code := claim(`{"item_id":"w1","name":"  "}`).Code; code != http.StatusBadRequest {
		t.Fatalf("blank name expected 400, got %d", code)
	}

	sections, _ := server.store.GetSettings(invitation.ID)["sections_config"].(map[string]any)
	items := sections["wishlist"].(map[string]any)["items"].([]any)
	if got := items[0].(map[string]any)["claimed_by"]; got != "Budi" {
		t.Fatalf("claimed_by expected Budi, got %v", got)
	}
}
