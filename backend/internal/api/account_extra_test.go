package api

import (
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"
	"time"

	"yukakad/internal/auth"
	"yukakad/internal/config"
	"yukakad/internal/store"
)

func TestChangePasswordAndAdminPayments(t *testing.T) {
	cfg := config.Config{Port: "8080", Environment: "test", JWTSecret: "secret"}
	server := NewServer(cfg)
	server.store.SeedPlans()
	hash, _ := auth.HashPassword("lama-12345")
	user, _ := server.store.CreateUser("Ayu", "ayu@example.com", hash)
	admin, _ := server.store.CreateUser("Admin", "admin@example.com", hash)
	token := auth.GenerateToken(user.ID, user.Email, "user", cfg.JWTSecret)
	adminToken := auth.GenerateToken(admin.ID, admin.Email, "admin", cfg.JWTSecret)
	call := func(h http.HandlerFunc, tok, method, body string) *httptest.ResponseRecorder {
		req := httptest.NewRequest(method, "/", strings.NewReader(body))
		req.Header.Set("Authorization", "Bearer "+tok)
		rec := httptest.NewRecorder()
		h(rec, req)
		return rec
	}
	if code := call(server.handleChangePassword, token, http.MethodPost, `{"current_password":"salah","new_password":"baru-12345"}`).Code; code != http.StatusBadRequest {
		t.Fatalf("wrong current password should be 400, got %d", code)
	}
	if code := call(server.handleChangePassword, token, http.MethodPost, `{"current_password":"lama-12345","new_password":"pendek"}`).Code; code != http.StatusBadRequest {
		t.Fatalf("short password should be 400, got %d", code)
	}
	time.Sleep(1100 * time.Millisecond) // the old token must come from an earlier second than the change
	changed := call(server.handleChangePassword, token, http.MethodPost, `{"current_password":"lama-12345","new_password":"baru-12345"}`)
	if changed.Code != http.StatusOK {
		t.Fatalf("change password: %d", changed.Code)
	}
	var fresh struct {
		Token string `json:"token"`
	}
	_ = json.Unmarshal(changed.Body.Bytes(), &fresh)
	if fresh.Token == "" {
		t.Fatal("change password should return a fresh token")
	}
	if code := call(server.handleProfile, token, http.MethodGet, "").Code; code != http.StatusUnauthorized {
		t.Fatalf("old token should be revoked after password change, got %d", code)
	}
	if code := call(server.handleProfile, fresh.Token, http.MethodGet, "").Code; code != http.StatusOK {
		t.Fatalf("fresh token should work, got %d", code)
	}
	token = fresh.Token
	updated, _ := server.store.FindUserByID(user.ID)
	if !auth.VerifyPassword("baru-12345", updated.Password) {
		t.Fatal("new password not stored")
	}

	sub, _ := server.store.CreateSubscription(store.Subscription{UserID: user.ID, PlanID: "pro", Status: "pending", Provider: "dummy", ProviderReference: "DUMMY-1"})
	if _, err := server.billing.Confirm(sub.ProviderReference); err != nil {
		t.Fatal(err)
	}
	if code := call(server.handleAdminPayments, token, http.MethodGet, "").Code; code != http.StatusForbidden {
		t.Fatalf("non-admin should be 403, got %d", code)
	}
	body := call(server.handleAdminPayments, adminToken, http.MethodGet, "").Body.String()
	if !strings.Contains(body, `"revenue_total":99000`) || !strings.Contains(body, "ayu@example.com") {
		t.Fatalf("admin payments: %s", body)
	}
}
