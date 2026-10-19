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

func TestRequiredPermissionRejectsSecondResource(t *testing.T) {
	for _, path := range []string{"settings/x/gift-wallet", "media/x/gift-payouts", "guests/x/rsvps", "stories/a/domains", "ledger/x/wishes"} {
		for _, method := range []string{http.MethodGet, http.MethodPost} {
			if got := requiredPermission(path, method); got != ownerOnly {
				t.Fatalf("%s %s should be owner-only, got %q", method, path, got)
			}
		}
	}
	if got := requiredPermission("guests/abc/check-in", http.MethodPost); got != permCheckIn {
		t.Fatalf("check-in permission changed: %q", got)
	}
	if got := requiredPermission("preview-token", http.MethodPost); got != permView {
		t.Fatalf("preview-token should need view, got %q", got)
	}
}

func auditServer(t *testing.T) (*Server, *store.User, string, *store.Invitation) {
	t.Helper()
	cfg := config.Config{Port: "8080", Environment: "test", JWTSecret: "secret-for-tests-0123456789"}
	server := NewServer(cfg)
	server.store.SeedPlans()
	user, _ := server.store.CreateUser("Rina", "rina@example.com", "hash")
	token := auth.GenerateToken(user.ID, user.Email, "user", cfg.JWTSecret)
	inv, _ := server.store.CreateInvitation(user.ID, "rina-bima", "Rina & Bima")
	return server, user, token, inv
}

func doReq(handler http.HandlerFunc, method, path, token, body string, headers map[string]string) *httptest.ResponseRecorder {
	req := httptest.NewRequest(method, path, strings.NewReader(body))
	if token != "" {
		req.Header.Set("Authorization", "Bearer "+token)
	}
	for k, v := range headers {
		req.Header.Set(k, v)
	}
	rec := httptest.NewRecorder()
	handler(rec, req)
	return rec
}

func TestPreviewTokenShowsDraftOnly(t *testing.T) {
	server, _, token, inv := auditServer(t)
	public := "/api/public/invitation/rina-bima"
	if code := doReq(server.handlePublicInvitation, http.MethodGet, public, "", "", nil).Code; code != http.StatusNotFound {
		t.Fatalf("draft should be hidden, got %d", code)
	}
	rec := doReq(server.handleInvitationDetail, http.MethodPost, "/api/invitations/"+inv.ID+"/preview-token", token, "", nil)
	var body struct {
		Token string `json:"token"`
	}
	_ = json.Unmarshal(rec.Body.Bytes(), &body)
	if rec.Code != http.StatusOK || !strings.HasPrefix(body.Token, "pv1.") {
		t.Fatalf("preview token: %d %s", rec.Code, rec.Body.String())
	}
	if code := doReq(server.handlePublicInvitation, http.MethodGet, public, "", "", map[string]string{"X-Preview-Token": body.Token}).Code; code != http.StatusOK {
		t.Fatalf("preview token should open draft, got %d", code)
	}
	forged := body.Token[:len(body.Token)-1] + "0"
	if forged == body.Token {
		forged = body.Token[:len(body.Token)-1] + "1"
	}
	if code := doReq(server.handlePublicInvitation, http.MethodGet, public, "", "", map[string]string{"X-Preview-Token": forged}).Code; code != http.StatusNotFound {
		t.Fatalf("forged preview token should fail, got %d", code)
	}
	if server.validPreviewToken(body.Token, "other-invitation", time.Now()) {
		t.Fatal("preview token must be bound to its invitation")
	}
	if server.validPreviewToken(body.Token, inv.ID, time.Now().Add(previewValidity+time.Minute)) {
		t.Fatal("preview token must expire")
	}
}

func TestRSVPClosedInThankYouMode(t *testing.T) {
	server, user, _, inv := auditServer(t)
	_, _ = server.store.UpdateInvitation(inv.ID, "rina-bima", "Rina & Bima", true, store.Couple{BrideName: "Rina", GroomName: "Bima"}, store.Event{Date: "2020-01-01"})
	_ = user
	rsvp := `{"attendance":"yes","attendees_count":1,"message":"Hadir"}`
	if code := doReq(server.handlePublicInvitation, http.MethodPost, "/api/public/invitation/rina-bima/rsvp", "", rsvp, nil).Code; code != http.StatusConflict {
		t.Fatalf("past event (auto thank-you) should close RSVP, got %d", code)
	}
	server.store.UpdateSettings(inv.ID, map[string]any{"sections_config": map[string]any{"thankYou": map[string]any{"mode": "off"}}})
	if code := doReq(server.handlePublicInvitation, http.MethodPost, "/api/public/invitation/rina-bima/rsvp", "", rsvp, nil).Code; code != http.StatusCreated && code != http.StatusOK {
		t.Fatalf("thank-you off should accept RSVP, got %d", code)
	}
}

func TestGuestCSVImport(t *testing.T) {
	server, user, token, inv := auditServer(t)
	path := "/api/invitations/" + inv.ID + "/guests"
	csvBody := "\ufeffnama;telepon;kategori;meja\nPak Andi;0833;family;7\nBu Sri;;friend;\n"
	rec := doReq(server.handleInvitationDetail, http.MethodPost, path, token, csvBody, map[string]string{"Content-Type": "text/csv"})
	if rec.Code != http.StatusCreated {
		t.Fatalf("semicolon csv: %d %s", rec.Code, rec.Body.String())
	}
	guests := server.store.ListGuests(inv.ID)
	if len(guests) != 2 || guests[0].Name == "" || strings.Contains(guests[0].Name, ";") {
		t.Fatalf("semicolon csv parsed wrong: %+v", guests)
	}
	// Free plan: 50 guests. A 60-row file must be refused as a whole.
	var big strings.Builder
	for i := 0; i < 60; i++ {
		big.WriteString("Tamu " + string(rune('A'+i%26)) + ",08,family\n")
	}
	rec = doReq(server.handleInvitationDetail, http.MethodPost, path, token, big.String(), map[string]string{"Content-Type": "text/csv"})
	if rec.Code != http.StatusConflict || !strings.Contains(rec.Body.String(), `"code":"guest_limit"`) {
		t.Fatalf("over-quota import should be 409 guest_limit: %d %s", rec.Code, rec.Body.String())
	}
	if n := len(server.store.ListGuests(inv.ID)); n != 2 {
		t.Fatalf("nothing should be imported on quota error, have %d", n)
	}
	_ = user
}

func TestCheckInFlagsRepeat(t *testing.T) {
	server, _, token, inv := auditServer(t)
	guest, _ := server.store.CreateGuest(inv.ID, "Pak Budi", "0812", "family")
	path := "/api/invitations/" + inv.ID + "/guests/" + guest.ID + "/check-in"
	first := doReq(server.handleInvitationDetail, http.MethodPost, path, token, "", nil)
	second := doReq(server.handleInvitationDetail, http.MethodPost, path, token, "", nil)
	if !strings.Contains(first.Body.String(), `"already":false`) || !strings.Contains(second.Body.String(), `"already":true`) {
		t.Fatalf("already flag wrong: %s / %s", first.Body.String(), second.Body.String())
	}
}

func TestInvitationUpdateKeepsPublishedAndValidatesSchedule(t *testing.T) {
	server, _, token, inv := auditServer(t)
	path := "/api/invitations/" + inv.ID
	if code := doReq(server.handleInvitationDetail, http.MethodPut, path, token, `{"published":true}`, nil).Code; code != http.StatusOK {
		t.Fatalf("publish: %d", code)
	}
	if code := doReq(server.handleInvitationDetail, http.MethodPut, path, token, `{"title":"Rina dan Bima"}`, nil).Code; code != http.StatusOK {
		t.Fatalf("update: %d", code)
	}
	if got, _ := server.store.FindInvitationByID(inv.ID); !got.Published {
		t.Fatal("omitting published must keep the invitation published")
	}
	rec := doReq(server.handleInvitationDetail, http.MethodPut, path, token, `{"event":{"date":"2026-02-30","start_time":"25:99"}}`, nil)
	if rec.Code != http.StatusBadRequest {
		t.Fatalf("invalid date should be 400, got %d", rec.Code)
	}
}
