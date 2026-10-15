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

func TestInvitationCoupleEventsAndStories(t *testing.T) {
	cfg := config.Config{Port: "8080", Environment: "test", JWTSecret: "secret"}
	server := NewServer(cfg)
	user, _ := server.store.CreateUser("Ayu", "ayu@example.com", "hash")
	invitation, _ := server.store.CreateInvitation(user.ID, "alya-rizky", "Alya & Rizky")
	token := auth.GenerateToken(user.ID, user.Email, user.Role, cfg.JWTSecret)
	call := func(method, path, body string) *httptest.ResponseRecorder {
		req := httptest.NewRequest(method, path, strings.NewReader(body))
		req.Header.Set("Authorization", "Bearer "+token)
		recorder := httptest.NewRecorder()
		server.handleInvitationDetail(recorder, req)
		return recorder
	}

	put := call(http.MethodPut, "/api/invitations/"+invitation.ID, `{"published":true,"couple":{"groom_name":"Rizky Pratama","bride_name":"Alya Putri","bride_nickname":"Alya","groom_parents":"Putra Bpk. Hadi","bride_photo":"https://cdn.example.com/a.jpg"},"event":{"title":"Resepsi","type":"pernikahan","address":"Jl. Melati 1","start_time":"11:00","end_time":"14:00"}}`)
	if put.Code != http.StatusOK {
		t.Fatalf("update expected 200, got %d: %s", put.Code, put.Body.String())
	}
	var detail struct {
		Couple map[string]string `json:"couple"`
		Event  map[string]string `json:"event"`
	}
	_ = json.Unmarshal(call(http.MethodGet, "/api/invitations/"+invitation.ID, "").Body.Bytes(), &detail)
	if detail.Couple["bride_nickname"] != "Alya" || detail.Couple["groom_parents"] != "Putra Bpk. Hadi" || detail.Couple["bride_photo"] == "" {
		t.Fatalf("couple fields not saved: %#v", detail.Couple)
	}
	if detail.Event["type"] != "pernikahan" || detail.Event["start_time"] != "11:00" || detail.Event["address"] != "Jl. Melati 1" {
		t.Fatalf("event fields not saved: %#v", detail.Event)
	}

	if code := call(http.MethodPost, "/api/invitations/"+invitation.ID+"/events", `{"title":"Akad","type":"akad","date":"2026-12-12","start_time":"08:00","venue":"Masjid"}`).Code; code != http.StatusCreated && code != http.StatusOK {
		t.Fatalf("create event expected 201, got %d", code)
	}

	created := call(http.MethodPost, "/api/invitations/"+invitation.ID+"/stories", `{"title":"Pertama bertemu","content":"Di kampus.","date":"2019","image_url":"https://cdn.example.com/s.jpg"}`)
	if created.Code != http.StatusCreated {
		t.Fatalf("create story expected 201, got %d: %s", created.Code, created.Body.String())
	}
	var story map[string]any
	_ = json.Unmarshal(created.Body.Bytes(), &story)
	if story["date"] != "2019" || story["image_url"] == "" {
		t.Fatalf("story date/image not saved: %#v", story)
	}
	storyID, _ := story["id"].(string)
	if code := call(http.MethodPut, "/api/invitations/"+invitation.ID+"/stories/"+storyID, `{"title":"Jadian","content":"Tahun kedua.","date":"2020"}`).Code; code != http.StatusOK {
		t.Fatalf("update story expected 200, got %d", code)
	}

	other, _ := server.store.CreateInvitation(user.ID, "lain", "Lain")
	if code := call(http.MethodDelete, "/api/invitations/"+other.ID+"/stories/"+storyID, "").Code; code != http.StatusNotFound {
		t.Fatalf("deleting a story through another invitation expected 404, got %d", code)
	}

	public := httptest.NewRecorder()
	server.handlePublicInvitation(public, httptest.NewRequest(http.MethodGet, "/api/public/invitation/alya-rizky", nil))
	body := public.Body.String()
	if public.Code != http.StatusOK || !strings.Contains(body, `"bride_nickname":"Alya"`) || !strings.Contains(body, `"events":[{`) {
		t.Fatalf("public invitation missing couple/events: %d %s", public.Code, body)
	}
}
