package api

import (
	"bytes"
	"mime/multipart"
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

	for _, section := range []string{"about", "terms", "privacy", "products"} {
		if code := call(server.handleAdminSiteContent, adminToken, http.MethodPut, "/api/admin/site-content/"+section, `{"intro":"Halo `+section+`"}`).Code; code != http.StatusOK {
			t.Fatalf("save %s expected 200, got %d", section, code)
		}
		rec := httptest.NewRecorder()
		server.handlePublicSiteContent(rec, httptest.NewRequest(http.MethodGet, "/api/public/site-content/"+section, nil))
		if !strings.Contains(rec.Body.String(), "Halo "+section) {
			t.Fatalf("public %s missing: %s", section, rec.Body.String())
		}
	}
	if code := call(server.handleAdminUploads, memberToken, http.MethodPost, "/api/admin/uploads", "").Code; code != http.StatusForbidden {
		t.Fatalf("non-admin upload expected 403, got %d", code)
	}
	if code := call(server.handleAdminUploads, adminToken, http.MethodPost, "/api/admin/uploads", "").Code; code != http.StatusServiceUnavailable {
		t.Fatalf("upload without storage expected 503, got %d", code)
	}

	// Uploads land under site/ without a doubled prefix.
	uploader := &fakeUploader{}
	server.photoStore = uploader
	upload := func(folder string) int {
		var buf bytes.Buffer
		mw := multipart.NewWriter(&buf)
		part, _ := mw.CreateFormFile("file", "a.png")
		_, _ = part.Write(tinyPNG)
		if folder != "" {
			_ = mw.WriteField("folder", folder)
		}
		_ = mw.Close()
		req := httptest.NewRequest(http.MethodPost, "/api/admin/uploads", &buf)
		req.Header.Set("Content-Type", mw.FormDataContentType())
		req.Header.Set("Authorization", "Bearer "+adminToken)
		rec := httptest.NewRecorder()
		server.handleAdminUploads(rec, req)
		return rec.Code
	}
	if code := upload(""); code != http.StatusOK {
		t.Fatalf("upload without folder: %d", code)
	}
	if code := upload("team"); code != http.StatusOK {
		t.Fatalf("upload with folder: %d", code)
	}
	if code := upload("../etc"); code != http.StatusBadRequest {
		t.Fatalf("bad folder should be 400, got %d", code)
	}
	if len(uploader.keys) != 2 || strings.HasPrefix(uploader.keys[0], "site/site/") || !strings.HasPrefix(uploader.keys[0], "site/") || !strings.HasPrefix(uploader.keys[1], "site/team/") {
		t.Fatalf("unexpected keys %v", uploader.keys)
	}
}
