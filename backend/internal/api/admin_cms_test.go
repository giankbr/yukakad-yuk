package api

import (
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"

	"yukakad/internal/auth"
	"yukakad/internal/config"
)

func TestAdminPlansUsersAndContent(t *testing.T) {
	cfg := config.Config{Port: "8080", Environment: "test", JWTSecret: "secret"}
	server := NewServer(cfg)
	server.store.SeedPlans()
	admin, _ := server.store.CreateUser("Admin", "admin@example.com", "hash")
	member, _ := server.store.CreateUser("Ayu", "ayu@example.com", "hash")
	adminToken := auth.GenerateToken(admin.ID, admin.Email, "admin", cfg.JWTSecret)
	memberToken := auth.GenerateToken(member.ID, member.Email, "user", cfg.JWTSecret)

	call := func(handler http.HandlerFunc, token, method, path, body string) *httptest.ResponseRecorder {
		req := httptest.NewRequest(method, path, strings.NewReader(body))
		req.Header.Set("Authorization", "Bearer "+token)
		recorder := httptest.NewRecorder()
		handler(recorder, req)
		return recorder
	}

	if code := call(server.handleAdminPlans, memberToken, http.MethodGet, "/api/admin/plans", "").Code; code != http.StatusForbidden {
		t.Fatalf("non-admin expected 403, got %d", code)
	}
	if code := call(server.handleAdminPlans, adminToken, http.MethodPost, "/api/admin/plans", `{"id":"vip","name":"VIP","max_guests":5000,"price":499000,"premium_templates_allowed":true}`).Code; code != http.StatusCreated {
		t.Fatalf("create plan expected 201, got %d", code)
	}
	if code := call(server.handleAdminPlans, adminToken, http.MethodPost, "/api/admin/plans", `{"id":"vip","name":"Dup"}`).Code; code != http.StatusConflict {
		t.Fatalf("duplicate plan expected 409, got %d", code)
	}
	if code := call(server.handleAdminPlans, adminToken, http.MethodPut, "/api/admin/plans/pro", `{"name":"Rayakan","max_guests":1000,"price":149000}`).Code; code != http.StatusOK {
		t.Fatalf("update plan expected 200, got %d", code)
	}
	list := call(server.handleAdminPlans, adminToken, http.MethodGet, "/api/admin/plans", "").Body.String()
	if !strings.Contains(list, `"name":"Rayakan"`) || !strings.Contains(list, `"id":"vip"`) {
		t.Fatalf("plans list missing changes: %s", list)
	}

	if code := call(server.handleAdminUsers, adminToken, http.MethodPatch, "/api/admin/users/"+member.ID+"/plan", `{"plan_id":"vip"}`).Code; code != http.StatusOK {
		t.Fatalf("set user plan expected 200, got %d", code)
	}
	users := call(server.handleAdminUsers, adminToken, http.MethodGet, "/api/admin/users", "").Body.String()
	if !strings.Contains(users, `"plan_id":"vip"`) {
		t.Fatalf("users list missing plan: %s", users)
	}

	if code := call(server.handleAdminSiteContent, adminToken, http.MethodPut, "/api/admin/site-content/faq", `{"items":[{"q":"Gratis?","a":"Ya."}]}`).Code; code != http.StatusOK {
		t.Fatalf("save faq expected 200, got %d", code)
	}
	public := httptest.NewRecorder()
	server.handlePublicSiteContent(public, httptest.NewRequest(http.MethodGet, "/api/public/site-content/faq", nil))
	if !strings.Contains(public.Body.String(), "Gratis?") {
		t.Fatalf("public faq missing: %s", public.Body.String())
	}
}
