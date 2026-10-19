package api

import (
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"

	"yukakad/internal/auth"
	"yukakad/internal/config"
	"yukakad/internal/store"
)

func TestTeamRolesAndPermissions(t *testing.T) {
	cfg := config.Config{Port: "8080", Environment: "test", JWTSecret: "secret", FrontendOrigin: "https://rawuh.test"}
	server := NewServer(cfg)
	server.store.SeedPlans()
	mk := func(name, email string) (string, string) {
		u, _ := server.store.CreateUser(name, email, "hash")
		return u.ID, auth.GenerateToken(u.ID, u.Email, "user", cfg.JWTSecret)
	}
	ownerID, owner := mk("Rina", "rina@example.com")
	_, family := mk("Tante Sri", "sri@example.com")
	_, wo := mk("WO Bahagia", "wo@example.com")
	desk, deskToken := mk("Penerima", "desk@example.com")
	_, stranger := mk("Eve", "eve@example.com")
	inv, _ := server.store.CreateInvitation(ownerID, "rina-bima", "Rina & Bima")
	_, _ = server.store.UpdateInvitation(inv.ID, "rina-bima", "Rina & Bima", true, store.Couple{BrideName: "Rina", GroomName: "Bima"}, store.Event{})
	guest, _ := server.store.CreateGuest(inv.ID, "Pak Budi", "0812", "family")
	base := "/api/invitations/" + inv.ID
	_ = server.store.SetUserPlan(ownerID, "premium") // free plans only allow 2 members

	call := func(tok, method, path, body string) *httptest.ResponseRecorder {
		req := httptest.NewRequest(method, path, strings.NewReader(body))
		if tok != "" {
			req.Header.Set("Authorization", "Bearer "+tok)
		}
		rec := httptest.NewRecorder()
		if strings.HasPrefix(path, "/api/team-invites/") {
			server.handleTeamInvite(rec, req)
		} else {
			server.handleInvitationDetail(rec, req)
		}
		return rec
	}
	invite := func(role, email string) string {
		rec := call(owner, http.MethodPost, base+"/team", `{"role":"`+role+`","email":"`+email+`"}`)
		if rec.Code != http.StatusCreated {
			t.Fatalf("invite %s: %d %s", role, rec.Code, rec.Body.String())
		}
		var body struct {
			URL string `json:"invite_url"`
		}
		_ = json.Unmarshal(rec.Body.Bytes(), &body)
		return body.URL[strings.LastIndex(body.URL, "/")+1:]
	}

	// Only the owner manages the team.
	if code := call(family, http.MethodPost, base+"/team", `{"role":"editor"}`).Code; code != http.StatusNotFound {
		t.Fatalf("non-owner invite should be 404, got %d", code)
	}
	if code := call(owner, http.MethodPost, base+"/team", `{"role":"boss"}`).Code; code != http.StatusBadRequest {
		t.Fatalf("unknown role should be 400, got %d", code)
	}
	famToken := invite("editor", "sri@example.com")
	woToken := invite("organizer", "")
	deskInvite := invite("receptionist", "desk@example.com")

	// Before accepting, the invitee has no access.
	if code := call(family, http.MethodGet, base, "").Code; code != http.StatusNotFound {
		t.Fatalf("pending invitee should not see the invitation, got %d", code)
	}
	if body := call("", http.MethodGet, "/api/team-invites/"+famToken, "").Body.String(); !strings.Contains(body, `"role":"editor"`) || !strings.Contains(body, "Rina") {
		t.Fatalf("invite preview: %s", body)
	}
	for tok, inviteToken := range map[string]string{family: famToken, wo: woToken, deskToken: deskInvite} {
		if code := call(tok, http.MethodPost, "/api/team-invites/"+inviteToken+"/accept", "").Code; code != http.StatusOK {
			t.Fatalf("accept: %d", code)
		}
	}
	if code := call(stranger, http.MethodPost, "/api/team-invites/"+famToken+"/accept", "").Code; code != http.StatusNotFound {
		t.Fatalf("used invite link should be 404, got %d", code)
	}

	expect := func(name, tok, method, path, body string, want int) {
		t.Helper()
		if rec := call(tok, method, path, body); rec.Code != want {
			t.Fatalf("%s %s %s: want %d got %d %s", name, method, path, want, rec.Code, rec.Body.String())
		}
	}
	// Editor (keluarga): content + guests, no money/team/hari-H/delete/publish.
	expect("editor", family, http.MethodGet, base, "", http.StatusOK)
	expect("editor", family, http.MethodPut, base, `{"title":"Rina & Bima ❤","published":false,"slug":"hijack","couple":{"bride_nickname":"Rina"}}`, http.StatusOK)
	if updated, _ := server.store.FindInvitationByID(inv.ID); updated.Slug != "rina-bima" || !updated.Published || updated.Title != "Rina & Bima ❤" {
		t.Fatalf("editor must not change slug/publish: %+v", updated)
	}
	expect("editor", family, http.MethodPost, base+"/guests", `{"name":"Bu Ani"}`, http.StatusCreated)
	expect("editor", family, http.MethodGet, base+"/gift-wallet", "", http.StatusForbidden)
	expect("editor", family, http.MethodGet, base+"/gifts", "", http.StatusForbidden)
	expect("editor", family, http.MethodPost, base+"/doorprize/draw", `{}`, http.StatusForbidden)
	expect("editor", family, http.MethodDelete, base, "", http.StatusForbidden)
	expect("editor", family, http.MethodGet, base+"/team", "", http.StatusNotFound)

	// Penerima tamu: check-in + log envelopes + screen only.
	expect("desk", deskToken, http.MethodGet, base+"/guests", "", http.StatusOK)
	expect("desk", deskToken, http.MethodPost, base+"/guests/"+guest.ID+"/check-in", "", http.StatusOK)
	rec := call(deskToken, http.MethodPost, base+"/ledger", `{"guest_id":"`+guest.ID+`","name":"Pak Budi","kind":"cash","amount":0}`)
	if rec.Code != http.StatusCreated || !strings.Contains(rec.Body.String(), `"recorded_by":"`+desk+`"`) {
		t.Fatalf("desk ledger entry should record the receptionist: %d %s", rec.Code, rec.Body.String())
	}
	expect("desk", deskToken, http.MethodGet, base+"/ledger", "", http.StatusForbidden)
	expect("desk", deskToken, http.MethodGet, base+"/live", "", http.StatusOK)
	expect("desk", deskToken, http.MethodPost, base+"/guests", `{"name":"X"}`, http.StatusForbidden)
	expect("desk", deskToken, http.MethodPut, base, `{"title":"Hacked"}`, http.StatusForbidden)
	expect("desk", deskToken, http.MethodGet, base+"/rsvps", "", http.StatusForbidden)
	if body := call(deskToken, http.MethodGet, base, "").Body.String(); !strings.Contains(body, `"role":"receptionist"`) {
		t.Fatalf("access info: %s", body)
	}

	// WO: hari-H too.
	expect("wo", wo, http.MethodPut, base+"/doorprize", `{"prizes":[{"name":"Voucher","qty":1}]}`, http.StatusOK)
	expect("wo", wo, http.MethodGet, base+"/ledger", "", http.StatusOK)
	expect("wo", wo, http.MethodGet, base+"/gift-transactions", "", http.StatusForbidden)
	expect("wo", wo, http.MethodPost, base+"/duplicate", `{}`, http.StatusForbidden)

	// Strangers still see nothing.
	expect("stranger", stranger, http.MethodGet, base, "", http.StatusNotFound)
	expect("stranger", stranger, http.MethodGet, base+"/guests", "", http.StatusNotFound)

	// Shared invitations show up in the member's list.
	listReq := httptest.NewRequest(http.MethodGet, "/api/invitations", nil)
	listReq.Header.Set("Authorization", "Bearer "+family)
	listRec := httptest.NewRecorder()
	server.handleInvitations(listRec, listReq)
	if !strings.Contains(listRec.Body.String(), `"role":"editor"`) {
		t.Fatalf("shared list: %s", listRec.Body.String())
	}

	// Owner demotes, then removes; member can also leave.
	var team struct {
		Items []store.Member `json:"items"`
	}
	_ = json.Unmarshal(call(owner, http.MethodGet, base+"/team", "").Body.Bytes(), &team)
	if len(team.Items) != 3 {
		t.Fatalf("team size %d", len(team.Items))
	}
	var famID, woID string
	for _, m := range team.Items {
		if m.Role == "editor" {
			famID = m.ID
		}
		if m.Role == "organizer" {
			woID = m.ID
		}
	}
	expect("owner", owner, http.MethodPatch, base+"/team/"+famID, `{"role":"receptionist"}`, http.StatusOK)
	expect("editor-now-desk", family, http.MethodPut, base, `{"title":"x"}`, http.StatusForbidden)
	expect("owner", owner, http.MethodDelete, base+"/team/"+famID, "", http.StatusOK)
	expect("removed", family, http.MethodGet, base, "", http.StatusNotFound)
	expect("wo leaves", wo, http.MethodDelete, base+"/team/me", "", http.StatusOK)
	expect("wo gone", wo, http.MethodGet, base+"/ledger", "", http.StatusNotFound)
	_ = woID
}

func TestEveryMemberRouteIsMapped(t *testing.T) {
	// Owner-only areas stay owner-only even for the broadest member role.
	for _, sub := range []string{"gifts", "gift-wallet", "gift-payouts", "gift-transactions", "domains", "duplicate", "unknown-new-endpoint"} {
		if p := requiredPermission(sub, http.MethodGet); p != ownerOnly {
			t.Fatalf("%s should be owner-only, got %q", sub, p)
		}
	}
	if requiredPermission("", http.MethodDelete) != ownerOnly {
		t.Fatal("deleting an invitation must be owner-only")
	}
}

func TestTeamLimitFollowsPlan(t *testing.T) {
	cfg := config.Config{Port: "8080", Environment: "test", JWTSecret: "secret", FrontendOrigin: "https://rawuh.test"}
	server := NewServer(cfg)
	server.store.SeedPlans()
	u, _ := server.store.CreateUser("Rina", "rina@example.com", "hash")
	token := auth.GenerateToken(u.ID, u.Email, "user", cfg.JWTSecret)
	inv, _ := server.store.CreateInvitation(u.ID, "rina-bima", "Rina & Bima")
	invite := func() int {
		req := httptest.NewRequest(http.MethodPost, "/api/invitations/"+inv.ID+"/team", strings.NewReader(`{"role":"receptionist"}`))
		req.Header.Set("Authorization", "Bearer "+token)
		rec := httptest.NewRecorder()
		server.handleInvitationDetail(rec, req)
		return rec.Code
	}
	for i := 0; i < 2; i++ {
		if code := invite(); code != http.StatusCreated {
			t.Fatalf("free invite %d: %d", i, code)
		}
	}
	if code := invite(); code != http.StatusConflict {
		t.Fatalf("free plan third member should be 409, got %d", code)
	}
	_ = server.store.SetUserPlan(u.ID, "pro")
	if code := invite(); code != http.StatusCreated {
		t.Fatalf("pro plan should allow more members, got %d", code)
	}
}
