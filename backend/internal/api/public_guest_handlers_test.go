package api

import (
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"

	"yukakad/internal/auth"
	"yukakad/internal/config"
)

func TestGuestTableAndPublicLookup(t *testing.T) {
	cfg := config.Config{Port: "8080", Environment: "test", JWTSecret: "secret"}
	server := NewServer(cfg)
	user, _ := server.store.CreateUser("Ayu", "ayu@example.com", "hash")
	invitation, _ := server.store.CreateInvitation(user.ID, "alya-rizky", "Alya & Rizky")
	invitation.Published = true
	token := auth.GenerateToken(user.ID, user.Email, user.Role, cfg.JWTSecret)

	createReq := httptest.NewRequest(http.MethodPost, "/api/invitations/"+invitation.ID+"/guests", strings.NewReader(`{"name":"Budi","phone":"0812","category":"friend","table":"12"}`))
	createReq.Header.Set("Authorization", "Bearer "+token)
	createRecorder := httptest.NewRecorder()
	server.handleInvitationDetail(createRecorder, createReq)
	if createRecorder.Code != http.StatusCreated {
		t.Fatalf("create guest expected 201, got %d: %s", createRecorder.Code, createRecorder.Body.String())
	}
	var created struct {
		ID    string `json:"id"`
		Token string `json:"token"`
		Table string `json:"table"`
	}
	_ = json.Unmarshal(createRecorder.Body.Bytes(), &created)
	if created.Table != "12" {
		t.Fatalf("table expected 12, got %q", created.Table)
	}

	updateReq := httptest.NewRequest(http.MethodPatch, "/api/invitations/"+invitation.ID+"/guests/"+created.ID, strings.NewReader(`{"name":"Budi","phone":"0812","category":"friend","table":"VIP A"}`))
	updateReq.Header.Set("Authorization", "Bearer "+token)
	updateRecorder := httptest.NewRecorder()
	server.handleInvitationDetail(updateRecorder, updateReq)
	if updateRecorder.Code != http.StatusOK {
		t.Fatalf("update guest expected 200, got %d: %s", updateRecorder.Code, updateRecorder.Body.String())
	}

	lookup := httptest.NewRequest(http.MethodGet, "/api/public/invitation/alya-rizky/guest?token="+created.Token, nil)
	lookupRecorder := httptest.NewRecorder()
	server.handlePublicInvitation(lookupRecorder, lookup)
	if lookupRecorder.Code != http.StatusOK || !strings.Contains(lookupRecorder.Body.String(), `"table":"VIP A"`) {
		t.Fatalf("public lookup expected table VIP A, got %d: %s", lookupRecorder.Code, lookupRecorder.Body.String())
	}

	missing := httptest.NewRequest(http.MethodGet, "/api/public/invitation/alya-rizky/guest?token=nope", nil)
	missingRecorder := httptest.NewRecorder()
	server.handlePublicInvitation(missingRecorder, missing)
	if missingRecorder.Code != http.StatusNotFound {
		t.Fatalf("unknown token expected 404, got %d", missingRecorder.Code)
	}
}
