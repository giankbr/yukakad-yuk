package api

import (
	"context"
	"encoding/json"
	"fmt"
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"
	"time"
	"yukakad/internal/auth"
	"yukakad/internal/config"
	"yukakad/internal/mailer"
	"yukakad/internal/store"
)

func TestRegisterAndLoginFlow(t *testing.T) {
	cfg := config.Config{Port: "8080", Environment: "test", JWTSecret: "secret"}
	server := NewServer(cfg)

	registerReq := httptest.NewRequest(http.MethodPost, "/api/auth/register", strings.NewReader(`{"name":"Ayu","email":"ayu@example.com","password":"secret123"}`))
	registerRecorder := httptest.NewRecorder()
	server.handleRegister(registerRecorder, registerReq)
	if registerRecorder.Code != http.StatusCreated {
		t.Fatalf("register expected 201, got %d: %s", registerRecorder.Code, registerRecorder.Body.String())
	}

	loginReq := httptest.NewRequest(http.MethodPost, "/api/auth/login", strings.NewReader(`{"email":"ayu@example.com","password":"secret123"}`))
	loginRecorder := httptest.NewRecorder()
	server.handleLogin(loginRecorder, loginReq)
	if loginRecorder.Code != http.StatusOK {
		t.Fatalf("login expected 200, got %d: %s", loginRecorder.Code, loginRecorder.Body.String())
	}
}

func TestV1RegisterRouteUsesCanonicalNamespace(t *testing.T) {
	cfg := config.Config{Port: "8080", Environment: "test", JWTSecret: "secret"}
	server := NewServer(cfg)
	req := httptest.NewRequest(http.MethodPost, "/api/v1/auth/register", strings.NewReader(`{"name":"Ayu","email":"v1@example.com","password":"secret123"}`))
	recorder := httptest.NewRecorder()
	server.handleV1(recorder, req)
	if recorder.Code != http.StatusCreated {
		t.Fatalf("v1 register expected 201, got %d: %s", recorder.Code, recorder.Body.String())
	}
}

func TestV1HealthRoute(t *testing.T) {
	server := NewServer(config.Config{Port: "8080", Environment: "test", JWTSecret: "secret"})
	req := httptest.NewRequest(http.MethodGet, "/api/v1/health", nil)
	recorder := httptest.NewRecorder()
	server.handleHealth(recorder, req)
	if recorder.Code != http.StatusOK {
		t.Fatalf("v1 health expected 200, got %d", recorder.Code)
	}
}

func TestV1ErrorsUseErrorEnvelope(t *testing.T) {
	server := NewServer(config.Config{Port: "8080", Environment: "test", JWTSecret: "secret"})
	req := httptest.NewRequest(http.MethodGet, "/api/v1/invitations", nil)
	recorder := httptest.NewRecorder()
	server.handleV1(recorder, req)
	if recorder.Code != http.StatusUnauthorized {
		t.Fatalf("expected 401, got %d", recorder.Code)
	}
	if !strings.Contains(recorder.Body.String(), `"error"`) || !strings.Contains(recorder.Body.String(), "missing authorization token") {
		t.Fatalf("expected v1 error envelope, got %s", recorder.Body.String())
	}
}

func TestCreateInvitationAndPublicRoute(t *testing.T) {
	cfg := config.Config{Port: "8080", Environment: "test", JWTSecret: "secret"}
	server := NewServer(cfg)

	user, err := server.store.CreateUser("Ayu", "ayu@example.com", "hash")
	if err != nil {
		t.Fatalf("create user: %v", err)
	}

	invitation, err := server.store.CreateInvitation(user.ID, "alya-rizky", "Alya & Rizky")
	if err != nil {
		t.Fatalf("create invitation: %v", err)
	}
	invitation.Published = true

	invitation.Couple = store.Couple{
		GroomName: "Rizky",
		BrideName: "Alya",
	}
	invitation.Event = store.Event{
		Title: "Akad Nikah",
		Venue: "Gedung Serbaguna",
	}

	publicReq := httptest.NewRequest(http.MethodGet, "/api/public/invitation/alya-rizky", nil)
	publicRecorder := httptest.NewRecorder()
	server.handlePublicInvitation(publicRecorder, publicReq)
	if publicRecorder.Code != http.StatusOK {
		t.Fatalf("public invitation expected 200, got %d: %s", publicRecorder.Code, publicRecorder.Body.String())
	}

	var body map[string]any
	if err := json.Unmarshal(publicRecorder.Body.Bytes(), &body); err != nil {
		t.Fatalf("decode response: %v", err)
	}
	if body["slug"] != "alya-rizky" {
		t.Fatalf("expected slug alya-rizky, got %v", body["slug"])
	}
	if body["title"] != "Alya & Rizky" {
		t.Fatalf("expected title Alya & Rizky, got %v", body["title"])
	}
	if _, ok := body["couple"]; !ok {
		t.Fatal("expected couple data in public response")
	}
	if _, ok := body["event"]; !ok {
		t.Fatal("expected event data in public response")
	}
	if invitation.Couple.GroomName != "Rizky" || invitation.Event.Venue != "Gedung Serbaguna" {
		t.Fatal("invitation details were not stored as expected")
	}
}

func TestInvitationDetailAndUpdateFlow(t *testing.T) {
	cfg := config.Config{Port: "8080", Environment: "test", JWTSecret: "secret"}
	server := NewServer(cfg)

	user, err := server.store.CreateUser("Ayu", "ayu@example.com", "hash")
	if err != nil {
		t.Fatalf("create user: %v", err)
	}

	token := auth.GenerateToken(user.ID, user.Email, user.Role, cfg.JWTSecret)

	createReq := httptest.NewRequest(http.MethodPost, "/api/invitations", strings.NewReader(`{"slug":"alya-rizky","title":"Alya & Rizky"}`))
	createReq.Header.Set("Authorization", "Bearer "+token)
	createRecorder := httptest.NewRecorder()
	server.handleInvitations(createRecorder, createReq)
	if createRecorder.Code != http.StatusCreated {
		t.Fatalf("create invitation expected 201, got %d: %s", createRecorder.Code, createRecorder.Body.String())
	}

	var created map[string]any
	if err := json.Unmarshal(createRecorder.Body.Bytes(), &created); err != nil {
		t.Fatalf("decode created invitation: %v", err)
	}
	invitationID := created["id"].(string)

	getReq := httptest.NewRequest(http.MethodGet, "/api/invitations/"+invitationID, nil)
	getReq.Header.Set("Authorization", "Bearer "+token)
	getRecorder := httptest.NewRecorder()
	server.handleInvitationDetail(getRecorder, getReq)
	if getRecorder.Code != http.StatusOK {
		t.Fatalf("get invitation expected 200, got %d: %s", getRecorder.Code, getRecorder.Body.String())
	}

	updateReq := httptest.NewRequest(http.MethodPut, "/api/invitations/"+invitationID, strings.NewReader(`{"slug":"alya-rizky","title":"Alya & Rizky","published":true,"couple":{"groom_name":"Rizky","bride_name":"Alya"},"event":{"title":"Akad Nikah","venue":"Gedung Serbaguna","date":"2026-12-12"}}`))
	updateReq.Header.Set("Authorization", "Bearer "+token)
	updateRecorder := httptest.NewRecorder()
	server.handleInvitationDetail(updateRecorder, updateReq)
	if updateRecorder.Code != http.StatusOK {
		t.Fatalf("update invitation expected 200, got %d: %s", updateRecorder.Code, updateRecorder.Body.String())
	}

	var updated map[string]any
	if err := json.Unmarshal(updateRecorder.Body.Bytes(), &updated); err != nil {
		t.Fatalf("decode updated invitation: %v", err)
	}
	if updated["published"] != true {
		t.Fatalf("expected published=true after update, got %v", updated["published"])
	}
	if updated["couple"].(map[string]any)["groom_name"] != "Rizky" {
		t.Fatalf("expected groom_name Rizky, got %v", updated["couple"])
	}

	publicReq := httptest.NewRequest(http.MethodGet, "/api/public/invitation/alya-rizky", nil)
	publicRecorder := httptest.NewRecorder()
	server.handlePublicInvitation(publicRecorder, publicReq)
	if publicRecorder.Code != http.StatusOK {
		t.Fatalf("published invitation route expected 200, got %d: %s", publicRecorder.Code, publicRecorder.Body.String())
	}
}

func TestGuestRSVPAndWishesFlow(t *testing.T) {
	cfg := config.Config{Port: "8080", Environment: "test", JWTSecret: "secret"}
	server := NewServer(cfg)
	user, err := server.store.CreateUser("Ayu", "ayu@example.com", "hash")
	if err != nil {
		t.Fatalf("create user: %v", err)
	}
	invitation, err := server.store.CreateInvitation(user.ID, "alya-rizky", "Alya & Rizky")
	if err != nil {
		t.Fatalf("create invitation: %v", err)
	}
	invitation.Published = true
	token := auth.GenerateToken(user.ID, user.Email, user.Role, cfg.JWTSecret)

	guestReq := httptest.NewRequest(http.MethodPost, "/api/invitations/"+invitation.ID+"/guests", strings.NewReader(`{"name":"Budi","phone":"0812","category":"friend"}`))
	guestReq.Header.Set("Authorization", "Bearer "+token)
	guestRecorder := httptest.NewRecorder()
	server.handleInvitationDetail(guestRecorder, guestReq)
	if guestRecorder.Code != http.StatusCreated {
		t.Fatalf("create guest expected 201, got %d: %s", guestRecorder.Code, guestRecorder.Body.String())
	}

	rsvpReq := httptest.NewRequest(http.MethodPost, "/api/public/invitation/alya-rizky/rsvp", strings.NewReader(`{"attendance":"yes","attendees_count":2,"message":"See you"}`))
	rsvpRecorder := httptest.NewRecorder()
	server.handlePublicInvitation(rsvpRecorder, rsvpReq)
	if rsvpRecorder.Code != http.StatusCreated {
		t.Fatalf("create RSVP expected 201, got %d: %s", rsvpRecorder.Code, rsvpRecorder.Body.String())
	}

	wishReq := httptest.NewRequest(http.MethodPost, "/api/public/invitation/alya-rizky/wishes", strings.NewReader(`{"name":"Budi","message":"Happy wedding"}`))
	wishRecorder := httptest.NewRecorder()
	server.handlePublicInvitation(wishRecorder, wishReq)
	if wishRecorder.Code != http.StatusCreated {
		t.Fatalf("create wish expected 201, got %d: %s", wishRecorder.Code, wishRecorder.Body.String())
	}

}

func TestGiftTemplateAndWishModerationFlow(t *testing.T) {
	cfg := config.Config{Port: "8080", Environment: "test", JWTSecret: "secret"}
	server := NewServer(cfg)
	user, err := server.store.CreateUser("Ayu", "ayu@example.com", "hash")
	if err != nil {
		t.Fatalf("create user: %v", err)
	}
	invitation, err := server.store.CreateInvitation(user.ID, "alya-rizky", "Alya & Rizky")
	if err != nil {
		t.Fatalf("create invitation: %v", err)
	}
	invitation.Published = true
	token := auth.GenerateToken(user.ID, user.Email, user.Role, cfg.JWTSecret)

	templateReq := httptest.NewRequest(http.MethodGet, "/api/templates", nil)
	templateRecorder := httptest.NewRecorder()
	server.handleTemplates(templateRecorder, templateReq)
	if templateRecorder.Code != http.StatusOK || !strings.Contains(templateRecorder.Body.String(), "classic") {
		t.Fatalf("expected seeded templates, got %d: %s", templateRecorder.Code, templateRecorder.Body.String())
	}

	giftReq := httptest.NewRequest(http.MethodPost, "/api/invitations/"+invitation.ID+"/gifts", strings.NewReader(`{"type":"bank","bank_name":"BCA","account_number":"1234567890","account_name":"Alya"}`))
	giftReq.Header.Set("Authorization", "Bearer "+token)
	giftRecorder := httptest.NewRecorder()
	server.handleInvitationDetail(giftRecorder, giftReq)
	if giftRecorder.Code != http.StatusCreated {
		t.Fatalf("create gift expected 201, got %d: %s", giftRecorder.Code, giftRecorder.Body.String())
	}

	publicGiftReq := httptest.NewRequest(http.MethodGet, "/api/public/invitation/alya-rizky/gifts", nil)
	publicGiftRecorder := httptest.NewRecorder()
	server.handlePublicInvitation(publicGiftRecorder, publicGiftReq)
	if publicGiftRecorder.Code != http.StatusOK || !strings.Contains(publicGiftRecorder.Body.String(), "BCA") {
		t.Fatalf("public gifts expected 200 with BCA, got %d: %s", publicGiftRecorder.Code, publicGiftRecorder.Body.String())
	}
}

func TestTemplateCatalogResolvesPublicSlug(t *testing.T) {
	server := NewServer(config.Config{Port: "8080", Environment: "test", JWTSecret: "secret"})
	req := httptest.NewRequest(http.MethodGet, "/api/v1/templates/slug/classic", nil)
	recorder := httptest.NewRecorder()
	server.handleV1(recorder, req)
	if recorder.Code != http.StatusOK || !strings.Contains(recorder.Body.String(), `"slug":"classic"`) {
		t.Fatalf("expected classic template by slug, got %d: %s", recorder.Code, recorder.Body.String())
	}
}

func TestGuestLifecycleAndRSVPSummary(t *testing.T) {
	cfg := config.Config{Port: "8080", Environment: "test", JWTSecret: "secret"}
	server := NewServer(cfg)
	user, err := server.store.CreateUser("Ayu", "ayu@example.com", "hash")
	if err != nil {
		t.Fatalf("create user: %v", err)
	}
	invitation, err := server.store.CreateInvitation(user.ID, "alya-rizky", "Alya & Rizky")
	if err != nil {
		t.Fatalf("create invitation: %v", err)
	}
	token := auth.GenerateToken(user.ID, user.Email, user.Role, cfg.JWTSecret)

	importReq := httptest.NewRequest(http.MethodPost, "/api/invitations/"+invitation.ID+"/guests", strings.NewReader("name,phone,category\nBudi,0812,friend\n"))
	importReq.Header.Set("Authorization", "Bearer "+token)
	importReq.Header.Set("Content-Type", "text/csv")
	importRecorder := httptest.NewRecorder()
	server.handleInvitationDetail(importRecorder, importReq)
	if importRecorder.Code != http.StatusCreated {
		t.Fatalf("CSV import expected 201, got %d: %s", importRecorder.Code, importRecorder.Body.String())
	}

	guest := server.store.ListGuests(invitation.ID)[0]
	updateReq := httptest.NewRequest(http.MethodPatch, "/api/invitations/"+invitation.ID+"/guests/"+guest.ID, strings.NewReader(`{"name":"Budi Updated","phone":"0813","category":"vip"}`))
	updateReq.Header.Set("Authorization", "Bearer "+token)
	updateRecorder := httptest.NewRecorder()
	server.handleInvitationDetail(updateRecorder, updateReq)
	if updateRecorder.Code != http.StatusOK {
		t.Fatalf("guest update expected 200, got %d: %s", updateRecorder.Code, updateRecorder.Body.String())
	}

	checkInReq := httptest.NewRequest(http.MethodPost, "/api/invitations/"+invitation.ID+"/guests/"+guest.ID+"/check-in", nil)
	checkInReq.Header.Set("Authorization", "Bearer "+token)
	checkInRecorder := httptest.NewRecorder()
	server.handleInvitationDetail(checkInRecorder, checkInReq)
	if checkInRecorder.Code != http.StatusOK {
		t.Fatalf("check-in expected 200, got %d: %s", checkInRecorder.Code, checkInRecorder.Body.String())
	}

	rsvp, err := server.store.CreateRSVP(invitation.ID, guest.ID, "yes", 2, "ok")
	if err != nil {
		t.Fatalf("create rsvp: %v", err)
	}
	if rsvp.AttendeesCount != 2 || server.store.RSVPSummary(invitation.ID)["attendees"] != 2 {
		t.Fatal("RSVP summary did not include attendees")
	}
}

func TestInvitationContentManagement(t *testing.T) {
	cfg := config.Config{Port: "8080", Environment: "test", JWTSecret: "secret"}
	server := NewServer(cfg)
	user, err := server.store.CreateUser("Ayu", "ayu@example.com", "hash")
	if err != nil {
		t.Fatalf("create user: %v", err)
	}
	invitation, err := server.store.CreateInvitation(user.ID, "alya-rizky", "Alya & Rizky")
	if err != nil {
		t.Fatalf("create invitation: %v", err)
	}
	token := auth.GenerateToken(user.ID, user.Email, user.Role, cfg.JWTSecret)

	settingsReq := httptest.NewRequest(http.MethodPatch, "/api/invitations/"+invitation.ID+"/settings", strings.NewReader(`{"theme":"botanical","autoplay_music":true}`))
	settingsReq.Header.Set("Authorization", "Bearer "+token)
	settingsRecorder := httptest.NewRecorder()
	server.handleInvitationDetail(settingsRecorder, settingsReq)
	if settingsRecorder.Code != http.StatusOK {
		t.Fatalf("settings expected 200, got %d: %s", settingsRecorder.Code, settingsRecorder.Body.String())
	}

	storyReq := httptest.NewRequest(http.MethodPost, "/api/invitations/"+invitation.ID+"/stories", strings.NewReader(`{"title":"First meeting","content":"We met in 2020"}`))
	storyReq.Header.Set("Authorization", "Bearer "+token)
	storyRecorder := httptest.NewRecorder()
	server.handleInvitationDetail(storyRecorder, storyReq)
	if storyRecorder.Code != http.StatusCreated {
		t.Fatalf("story expected 201, got %d: %s", storyRecorder.Code, storyRecorder.Body.String())
	}

	galleryReq := httptest.NewRequest(http.MethodPost, "/api/invitations/"+invitation.ID+"/gallery", strings.NewReader(`{"image_url":"https://example.com/photo.jpg","caption":"Us"}`))
	galleryReq.Header.Set("Authorization", "Bearer "+token)
	galleryRecorder := httptest.NewRecorder()
	server.handleInvitationDetail(galleryRecorder, galleryReq)
	if galleryRecorder.Code != http.StatusCreated {
		t.Fatalf("gallery expected 201, got %d: %s", galleryRecorder.Code, galleryRecorder.Body.String())
	}

	templateReq := httptest.NewRequest(http.MethodPut, "/api/invitations/"+invitation.ID+"/template", strings.NewReader(`{"template_id":"classic"}`))
	templateReq.Header.Set("Authorization", "Bearer "+token)
	templateRecorder := httptest.NewRecorder()
	server.handleInvitationDetail(templateRecorder, templateReq)
	if templateRecorder.Code != http.StatusOK {
		t.Fatalf("template assignment expected 200, got %d: %s", templateRecorder.Code, templateRecorder.Body.String())
	}
}

func TestPasswordResetFlow(t *testing.T) {
	cfg := config.Config{Port: "8080", Environment: "test", JWTSecret: "secret"}
	server := NewServer(cfg)
	server.SetPasswordResetSender(mailer.Func(func(_ context.Context, _, _ string) error { return nil }))
	oldHash, err := auth.HashPassword("oldpassword")
	if err != nil {
		t.Fatalf("hash password: %v", err)
	}
	created, err := server.store.CreateUser("Ayu", "ayu@example.com", oldHash)
	if err != nil {
		t.Fatalf("create user: %v", err)
	}

	forgotReq := httptest.NewRequest(http.MethodPost, "/api/auth/forgot-password", strings.NewReader(`{"email":"ayu@example.com"}`))
	forgotRecorder := httptest.NewRecorder()
	server.handleForgotPassword(forgotRecorder, forgotReq)
	if forgotRecorder.Code != http.StatusOK {
		t.Fatalf("forgot password expected 200, got %d", forgotRecorder.Code)
	}
	var forgotBody map[string]any
	if json.Unmarshal(forgotRecorder.Body.Bytes(), &forgotBody) != nil {
		t.Fatal("invalid forgot password response")
	}
	resetToken, err := auth.GenerateOpaqueToken()
	if err != nil {
		t.Fatalf("generate reset token: %v", err)
	}
	if err := server.store.CreatePasswordResetToken(created.ID, auth.HashOpaqueToken(resetToken), time.Now().Add(time.Minute)); err != nil {
		t.Fatalf("store reset token: %v", err)
	}

	resetReq := httptest.NewRequest(http.MethodPost, "/api/auth/reset-password", strings.NewReader(`{"token":"`+resetToken+`","password":"newpassword"}`))
	resetRecorder := httptest.NewRecorder()
	server.handleResetPassword(resetRecorder, resetReq)
	if resetRecorder.Code != http.StatusOK {
		t.Fatalf("reset password expected 200, got %d: %s", resetRecorder.Code, resetRecorder.Body.String())
	}
	user, _ := server.store.FindUserByEmail("ayu@example.com")
	if !auth.VerifyPassword("newpassword", user.Password) {
		t.Fatal("password was not reset")
	}
}

func TestPublicRSVPRateLimited(t *testing.T) {
	cfg := config.Config{Port: "8080", Environment: "test", JWTSecret: "secret"}
	server := NewServer(cfg)
	user, _ := server.store.CreateUser("Ayu", "ayu@example.com", "hash")
	invitation, _ := server.store.CreateInvitation(user.ID, "alya-rizky", "Alya & Rizky")
	invitation.Published = true

	body := `{"attendance":"yes","attendees_count":1}`
	var lastCode int
	for i := 0; i < 6; i++ {
		req := httptest.NewRequest(http.MethodPost, "/api/public/invitation/alya-rizky/rsvp", strings.NewReader(body))
		recorder := httptest.NewRecorder()
		server.handlePublicInvitation(recorder, req)
		lastCode = recorder.Code
	}
	if lastCode != http.StatusTooManyRequests {
		t.Fatalf("expected 429 after exceeding rate limit, got %d", lastCode)
	}
}

func TestGiftToggleActive(t *testing.T) {
	cfg := config.Config{Port: "8080", Environment: "test", JWTSecret: "secret"}
	server := NewServer(cfg)
	user, _ := server.store.CreateUser("Ayu", "ayu@example.com", "hash")
	invitation, _ := server.store.CreateInvitation(user.ID, "alya-rizky", "Alya & Rizky")
	token := auth.GenerateToken(user.ID, user.Email, user.Role, cfg.JWTSecret)

	giftReq := httptest.NewRequest(http.MethodPost, "/api/invitations/"+invitation.ID+"/gifts", strings.NewReader(`{"type":"bank","bank_name":"BCA","account_number":"1234567890","account_name":"Alya"}`))
	giftReq.Header.Set("Authorization", "Bearer "+token)
	giftRecorder := httptest.NewRecorder()
	server.handleInvitationDetail(giftRecorder, giftReq)
	if giftRecorder.Code != http.StatusCreated {
		t.Fatalf("create gift expected 201, got %d: %s", giftRecorder.Code, giftRecorder.Body.String())
	}
	var created store.Gift
	if json.Unmarshal(giftRecorder.Body.Bytes(), &created) != nil {
		t.Fatal("invalid create gift response")
	}

	toggleReq := httptest.NewRequest(http.MethodPatch, "/api/invitations/"+invitation.ID+"/gifts/"+created.ID, strings.NewReader(`{"is_active":false}`))
	toggleReq.Header.Set("Authorization", "Bearer "+token)
	toggleRecorder := httptest.NewRecorder()
	server.handleInvitationDetail(toggleRecorder, toggleReq)
	if toggleRecorder.Code != http.StatusOK {
		t.Fatalf("toggle gift expected 200, got %d: %s", toggleRecorder.Code, toggleRecorder.Body.String())
	}
	if active := server.store.ListActiveGifts(invitation.ID); len(active) != 0 {
		t.Fatalf("expected 0 active gifts after deactivation, got %d", len(active))
	}
}

func TestGuestLimitEnforcedByPlan(t *testing.T) {
	cfg := config.Config{Port: "8080", Environment: "test", JWTSecret: "secret"}
	server := NewServer(cfg)
	user, _ := server.store.CreateUser("Ayu", "ayu@example.com", "hash")
	_ = server.store.SetUserPlan(user.ID, "free")
	invitation, _ := server.store.CreateInvitation(user.ID, "alya-rizky", "Alya & Rizky")
	token := auth.GenerateToken(user.ID, user.Email, user.Role, cfg.JWTSecret)

	plan, err := server.store.GetUserPlan(user.ID)
	if err != nil {
		t.Fatalf("get user plan: %v", err)
	}
	for i := 0; i < plan.MaxGuests; i++ {
		if _, err := server.store.CreateGuest(invitation.ID, "Guest", "", "family"); err != nil {
			t.Fatalf("seed guest %d: %v", i, err)
		}
	}

	req := httptest.NewRequest(http.MethodPost, "/api/invitations/"+invitation.ID+"/guests", strings.NewReader(`{"name":"One Too Many"}`))
	req.Header.Set("Authorization", "Bearer "+token)
	recorder := httptest.NewRecorder()
	server.handleInvitationDetail(recorder, req)
	if recorder.Code != http.StatusUnprocessableEntity {
		t.Fatalf("expected 422 once plan guest limit is reached, got %d: %s", recorder.Code, recorder.Body.String())
	}
}

func TestMediaUploadWithoutStorageReturns503(t *testing.T) {
	cfg := config.Config{Port: "8080", Environment: "test", JWTSecret: "secret"}
	server := NewServer(cfg)
	user, _ := server.store.CreateUser("Ayu", "ayu@example.com", "hash")
	invitation, _ := server.store.CreateInvitation(user.ID, "alya-rizky", "Alya & Rizky")
	token := auth.GenerateToken(user.ID, user.Email, user.Role, cfg.JWTSecret)

	req := httptest.NewRequest(http.MethodPost, "/api/invitations/"+invitation.ID+"/media", strings.NewReader(""))
	req.Header.Set("Authorization", "Bearer "+token)
	req.Header.Set("Content-Type", "multipart/form-data; boundary=x")
	recorder := httptest.NewRecorder()
	server.handleInvitationDetail(recorder, req)
	if recorder.Code != http.StatusServiceUnavailable {
		t.Fatalf("expected 503 when storage unconfigured, got %d: %s", recorder.Code, recorder.Body.String())
	}
}

func TestBroadcastDedupeAndConfirm(t *testing.T) {
	cfg := config.Config{Port: "8080", Environment: "test", JWTSecret: "secret", FrontendOrigin: "http://localhost:3000"}
	server := NewServer(cfg)
	user, _ := server.store.CreateUser("Ayu", "ayu@example.com", "hash")
	invitation, _ := server.store.CreateInvitation(user.ID, "alya-rizky", "Alya & Rizky")
	sentGuest, _ := server.store.CreateGuest(invitation.ID, "Budi", "081234567890", "family")
	freshGuest, _ := server.store.CreateGuest(invitation.ID, "Citra", "081234567891", "family")
	token := auth.GenerateToken(user.ID, user.Email, user.Role, cfg.JWTSecret)

	// Pre-seed a "sent" log for sentGuest so the dedupe path has something to skip.
	preLog, err := server.store.CreateBroadcastLog(invitation.ID, sentGuest.ID, "previously sent", "sent")
	if err != nil {
		t.Fatalf("seed broadcast log: %v", err)
	}

	body := `{"guest_ids":["` + sentGuest.ID + `","` + freshGuest.ID + `"]}`
	req := httptest.NewRequest(http.MethodPost, "/api/invitations/"+invitation.ID+"/broadcast", strings.NewReader(body))
	req.Header.Set("Authorization", "Bearer "+token)
	recorder := httptest.NewRecorder()
	server.handleInvitationDetail(recorder, req)
	if recorder.Code != http.StatusCreated {
		t.Fatalf("broadcast create expected 201, got %d: %s", recorder.Code, recorder.Body.String())
	}
	var body2 struct {
		Items []map[string]any `json:"items"`
	}
	if json.Unmarshal(recorder.Body.Bytes(), &body2) != nil {
		t.Fatal("invalid broadcast response")
	}
	if len(body2.Items) != 2 {
		t.Fatalf("expected 2 results, got %d", len(body2.Items))
	}

	var sentResult, freshResult map[string]any
	for _, item := range body2.Items {
		if item["guest_id"] == sentGuest.ID {
			sentResult = item
		}
		if item["guest_id"] == freshGuest.ID {
			freshResult = item
		}
	}
	if sentResult["status"] != "skipped_already_sent" {
		t.Fatalf("expected already-sent guest to be skipped, got %+v", sentResult)
	}
	if freshResult["status"] != "generated" || freshResult["wa_link"] == nil {
		t.Fatalf("expected fresh guest to get a generated wa_link, got %+v", freshResult)
	}

	// Confirming the fresh guest's log flips it to sent.
	confirmReq := httptest.NewRequest(http.MethodPost, "/api/invitations/"+invitation.ID+"/broadcast/"+fmt.Sprint(freshResult["id"])+"/confirm", nil)
	confirmReq.Header.Set("Authorization", "Bearer "+token)
	confirmRecorder := httptest.NewRecorder()
	server.handleInvitationDetail(confirmRecorder, confirmReq)
	if confirmRecorder.Code != http.StatusOK {
		t.Fatalf("confirm expected 200, got %d: %s", confirmRecorder.Code, confirmRecorder.Body.String())
	}
	latest, found := server.store.LatestBroadcastLogForGuest(invitation.ID, freshGuest.ID)
	if !found || latest["status"] != "sent" {
		t.Fatalf("expected confirmed log to be status=sent, got %+v", latest)
	}

	// Resend=true bypasses the dedupe skip even for an already-sent guest.
	_ = preLog
	resendBody := `{"guest_ids":["` + sentGuest.ID + `"],"resend":true}`
	resendReq := httptest.NewRequest(http.MethodPost, "/api/invitations/"+invitation.ID+"/broadcast", strings.NewReader(resendBody))
	resendReq.Header.Set("Authorization", "Bearer "+token)
	resendRecorder := httptest.NewRecorder()
	server.handleInvitationDetail(resendRecorder, resendReq)
	var resendResp struct {
		Items []map[string]any `json:"items"`
	}
	if json.Unmarshal(resendRecorder.Body.Bytes(), &resendResp) != nil {
		t.Fatal("invalid resend response")
	}
	if len(resendResp.Items) != 1 || resendResp.Items[0]["status"] != "generated" {
		t.Fatalf("expected resend to regenerate a link, got %+v", resendResp.Items)
	}
}

func TestOwnerCanPreviewUnpublishedInvitation(t *testing.T) {
	cfg := config.Config{Port: "8080", Environment: "test", JWTSecret: "secret"}
	server := NewServer(cfg)
	owner, _ := server.store.CreateUser("Ayu", "ayu@example.com", "hash")
	other, _ := server.store.CreateUser("Budi", "budi@example.com", "hash")
	_, _ = server.store.CreateInvitation(owner.ID, "alya-rizky", "Alya & Rizky")
	// published defaults to false (draft)

	anonReq := httptest.NewRequest(http.MethodGet, "/api/public/invitation/alya-rizky", nil)
	anonRecorder := httptest.NewRecorder()
	server.handlePublicInvitation(anonRecorder, anonReq)
	if anonRecorder.Code != http.StatusNotFound {
		t.Fatalf("anonymous view of draft expected 404, got %d", anonRecorder.Code)
	}

	otherToken := auth.GenerateToken(other.ID, other.Email, other.Role, cfg.JWTSecret)
	otherReq := httptest.NewRequest(http.MethodGet, "/api/public/invitation/alya-rizky", nil)
	otherReq.Header.Set("Authorization", "Bearer "+otherToken)
	otherRecorder := httptest.NewRecorder()
	server.handlePublicInvitation(otherRecorder, otherReq)
	if otherRecorder.Code != http.StatusNotFound {
		t.Fatalf("non-owner view of draft expected 404, got %d", otherRecorder.Code)
	}

	ownerToken := auth.GenerateToken(owner.ID, owner.Email, owner.Role, cfg.JWTSecret)
	ownerReq := httptest.NewRequest(http.MethodGet, "/api/public/invitation/alya-rizky", nil)
	ownerReq.Header.Set("Authorization", "Bearer "+ownerToken)
	ownerRecorder := httptest.NewRecorder()
	server.handlePublicInvitation(ownerRecorder, ownerReq)
	if ownerRecorder.Code != http.StatusOK {
		t.Fatalf("owner preview of draft expected 200, got %d: %s", ownerRecorder.Code, ownerRecorder.Body.String())
	}
}

func TestPublicRSVPResolvesGuestToken(t *testing.T) {
	cfg := config.Config{Port: "8080", Environment: "test", JWTSecret: "secret"}
	server := NewServer(cfg)
	user, _ := server.store.CreateUser("Ayu", "ayu@example.com", "hash")
	invitation, _ := server.store.CreateInvitation(user.ID, "alya-rizky", "Alya & Rizky")
	invitation.Published = true
	guest, _ := server.store.CreateGuest(invitation.ID, "Budi", "", "family")

	body := `{"guest_token":"` + guest.Token + `","guest_id":"someone-elses-id","attendance":"yes","attendees_count":2}`
	req := httptest.NewRequest(http.MethodPost, "/api/public/invitation/alya-rizky/rsvp", strings.NewReader(body))
	recorder := httptest.NewRecorder()
	server.handlePublicInvitation(recorder, req)
	if recorder.Code != http.StatusCreated {
		t.Fatalf("rsvp expected 201, got %d: %s", recorder.Code, recorder.Body.String())
	}
	var rsvp store.RSVP
	if json.Unmarshal(recorder.Body.Bytes(), &rsvp) != nil {
		t.Fatal("invalid rsvp response")
	}
	if rsvp.GuestID != guest.ID {
		t.Fatalf("expected guest_token to resolve to guest %s, got guest_id %s", guest.ID, rsvp.GuestID)
	}
}

func TestGuestCheckInRecordsActor(t *testing.T) {
	cfg := config.Config{Port: "8080", Environment: "test", JWTSecret: "secret"}
	server := NewServer(cfg)
	user, _ := server.store.CreateUser("Ayu", "ayu@example.com", "hash")
	invitation, _ := server.store.CreateInvitation(user.ID, "alya-rizky", "Alya & Rizky")
	guest, _ := server.store.CreateGuest(invitation.ID, "Budi", "", "family")
	token := auth.GenerateToken(user.ID, user.Email, user.Role, cfg.JWTSecret)

	req := httptest.NewRequest(http.MethodPost, "/api/invitations/"+invitation.ID+"/guests/"+guest.ID+"/check-in", nil)
	req.Header.Set("Authorization", "Bearer "+token)
	recorder := httptest.NewRecorder()
	server.handleInvitationDetail(recorder, req)
	if recorder.Code != http.StatusOK {
		t.Fatalf("check-in expected 200, got %d: %s", recorder.Code, recorder.Body.String())
	}
	var checkedIn store.Guest
	if json.Unmarshal(recorder.Body.Bytes(), &checkedIn) != nil {
		t.Fatal("invalid check-in response")
	}
	if checkedIn.CheckedInAt == nil || checkedIn.CheckedInBy == nil || *checkedIn.CheckedInBy != user.ID {
		t.Fatalf("expected checked_in_at/checked_in_by to be set to %s, got %+v", user.ID, checkedIn)
	}
}
