package api

import (
	"bytes"
	"context"
	"encoding/json"
	"io"
	"mime/multipart"
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"

	"yukakad/internal/auth"
	"yukakad/internal/config"
	"yukakad/internal/store"
)

type fakeUploader struct{ keys []string }

func (f *fakeUploader) Upload(_ context.Context, key string, _ io.Reader, _ int64, _ string) (string, error) {
	f.keys = append(f.keys, key)
	return "https://cdn.test/" + key, nil
}

// A 1x1 PNG.
var tinyPNG = []byte{0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a, 0, 0, 0, 0x0d, 0x49, 0x48, 0x44, 0x52, 0, 0, 0, 1, 0, 0, 0, 1, 8, 6, 0, 0, 0, 0x1f, 0x15, 0xc4, 0x89, 0, 0, 0, 0x0a, 0x49, 0x44, 0x41, 0x54, 0x78, 0x9c, 0x63, 0, 1, 0, 0, 5, 0, 1, 0x0d, 0x0a, 0x2d, 0xb4, 0, 0, 0, 0, 0x49, 0x45, 0x4e, 0x44, 0xae, 0x42, 0x60, 0x82}

func TestHariHFeatures(t *testing.T) {
	cfg := config.Config{Port: "8080", Environment: "test", JWTSecret: "secret", FrontendOrigin: "https://rawuh.test"}
	server := NewServer(cfg)
	owner, _ := server.store.CreateUser("Rina", "rina@example.com", "hash")
	other, _ := server.store.CreateUser("Eve", "eve@example.com", "hash")
	token := auth.GenerateToken(owner.ID, owner.Email, "user", cfg.JWTSecret)
	otherToken := auth.GenerateToken(other.ID, other.Email, "user", cfg.JWTSecret)
	inv, _ := server.store.CreateInvitation(owner.ID, "rina-bima", "Rina & Bima")
	_, _ = server.store.UpdateInvitation(inv.ID, "rina-bima", "Rina & Bima", true, store.Couple{BrideName: "Rina", GroomName: "Bima"}, store.Event{})
	budi, _ := server.store.CreateGuest(inv.ID, "Pak Budi", "0812", "family")
	ani, _ := server.store.CreateGuest(inv.ID, "Bu Ani", "0813", "friend")
	_, _ = server.store.CreateGuest(inv.ID, "Mas Joko", "0814", "friend")

	call := func(tok, method, path, body string) *httptest.ResponseRecorder {
		req := httptest.NewRequest(method, path, strings.NewReader(body))
		if tok != "" {
			req.Header.Set("Authorization", "Bearer "+tok)
		}
		rec := httptest.NewRecorder()
		server.handleInvitationDetail(rec, req)
		return rec
	}
	base := "/api/invitations/" + inv.ID

	// 1. Buku buwuh
	if code := call(otherToken, http.MethodGet, base+"/ledger", "").Code; code != http.StatusNotFound {
		t.Fatalf("other user ledger should be 404, got %d", code)
	}
	if code := call(token, http.MethodPost, base+"/ledger", `{"name":"Pak Budi","kind":"transfer","amount":0}`).Code; code != http.StatusBadRequest {
		t.Fatalf("zero transfer should be 400, got %d", code)
	}
	rec := call(token, http.MethodPost, base+"/ledger", `{"guest_id":"`+budi.ID+`","name":"Pak Budi","kind":"cash","amount":300000,"note":"amplop meja 12"}`)
	if rec.Code != http.StatusCreated {
		t.Fatalf("ledger create: %d %s", rec.Code, rec.Body.String())
	}
	var entry store.LedgerEntry
	_ = json.Unmarshal(rec.Body.Bytes(), &entry)
	call(token, http.MethodPost, base+"/ledger", `{"name":"Keluarga Hasan","kind":"kado","item":"Rice cooker"}`)
	_, _ = server.store.CreateGiftTransaction(store.GiftTransaction{InvitationID: inv.ID, Gateway: "mayar", GatewayReference: "r1", Amount: 150000, Status: "confirmed", SenderName: "Dina"})
	body := call(token, http.MethodGet, base+"/ledger", "").Body.String()
	if !strings.Contains(body, `"total":450000`) || !strings.Contains(body, `"kado_count":1`) || !strings.Contains(body, `"source":"online"`) {
		t.Fatalf("ledger totals: %s", body)
	}
	if code := call(token, http.MethodPatch, base+"/ledger/"+entry.ID, `{"name":"Pak Budi Santoso","kind":"transfer","amount":350000}`).Code; code != http.StatusOK {
		t.Fatalf("ledger update: %d", code)
	}
	if code := call(token, http.MethodDelete, base+"/ledger/"+entry.ID, "").Code; code != http.StatusOK {
		t.Fatalf("ledger delete: %d", code)
	}

	// 2/3. Live feed + doorprize
	if code := call(token, http.MethodPut, base+"/doorprize", `{"prizes":[{"name":"Kulkas","qty":1},{"name":"Voucher","qty":5}]}`).Code; code != http.StatusOK {
		t.Fatalf("doorprize save: %d", code)
	}
	var state doorprizeState
	_ = json.Unmarshal(call(token, http.MethodGet, base+"/doorprize", "").Body.Bytes(), &state)
	kulkas := state.Prizes[0].ID
	if code := call(token, http.MethodPost, base+"/doorprize/draw", `{"prize_id":"`+kulkas+`"}`).Code; code != http.StatusConflict {
		t.Fatalf("draw with nobody checked in should be 409, got %d", code)
	}
	_, _ = server.store.CheckInGuest(budi.ID, owner.ID)
	_, _ = server.store.CheckInGuest(ani.ID, owner.ID)
	live := call(token, http.MethodGet, base+"/live", "").Body.String()
	if !strings.Contains(live, `"checked_in":2`) || !strings.Contains(live, "Bu Ani") {
		t.Fatalf("live feed: %s", live)
	}
	rec = call(token, http.MethodPost, base+"/doorprize/draw", `{"prize_id":"`+kulkas+`"}`)
	if rec.Code != http.StatusOK || !strings.Contains(rec.Body.String(), `"prize":"Kulkas"`) {
		t.Fatalf("draw: %d %s", rec.Code, rec.Body.String())
	}
	if code := call(token, http.MethodPost, base+"/doorprize/draw", `{"prize_id":"`+kulkas+`"}`).Code; code != http.StatusConflict {
		t.Fatalf("kulkas qty 1 should be exhausted, got %d", code)
	}
	voucher := state.Prizes[1].ID
	call(token, http.MethodPost, base+"/doorprize/draw", `{"prize_id":"`+voucher+`"}`)
	if code := call(token, http.MethodPost, base+"/doorprize/draw", `{"prize_id":"`+voucher+`"}`).Code; code != http.StatusConflict {
		t.Fatalf("each checked-in guest wins once; third draw should be 409, got %d", code)
	}

	// 4. Guest photos
	upload := func(name string) *httptest.ResponseRecorder {
		var buf bytes.Buffer
		mw := multipart.NewWriter(&buf)
		part, _ := mw.CreateFormFile("file", "a.png")
		_, _ = part.Write(tinyPNG)
		_ = mw.WriteField("name", name)
		_ = mw.WriteField("guest", budi.Token)
		_ = mw.Close()
		req := httptest.NewRequest(http.MethodPost, "/api/public/invitation/rina-bima/photos", &buf)
		req.Header.Set("Content-Type", mw.FormDataContentType())
		out := httptest.NewRecorder()
		server.handlePublicInvitation(out, req)
		return out
	}
	if code := upload("Budi").Code; code != http.StatusForbidden {
		t.Fatalf("photos disabled should be 403, got %d", code)
	}
	server.store.UpdateSettings(inv.ID, map[string]any{"sections_config": map[string]any{"guestPhotos": map[string]any{"enabled": true, "moderate": true}}})
	if code := upload("Budi").Code; code != http.StatusServiceUnavailable {
		t.Fatalf("no storage should be 503, got %d", code)
	}
	uploader := &fakeUploader{}
	server.photoStore = uploader
	rec = upload("Budi")
	if rec.Code != http.StatusCreated || !strings.Contains(rec.Body.String(), `"status":"pending"`) {
		t.Fatalf("upload: %d %s", rec.Code, rec.Body.String())
	}
	publicList := httptest.NewRecorder()
	server.handlePublicInvitation(publicList, httptest.NewRequest(http.MethodGet, "/api/public/invitation/rina-bima/photos", nil))
	if strings.Contains(publicList.Body.String(), "cdn.test") {
		t.Fatalf("pending photo must not be public: %s", publicList.Body.String())
	}
	photos := server.store.ListGuestPhotos(inv.ID, "")
	if code := call(token, http.MethodPatch, base+"/guest-photos/"+photos[0].ID, `{"status":"approved"}`).Code; code != http.StatusOK {
		t.Fatalf("approve: %d", code)
	}
	publicList = httptest.NewRecorder()
	server.handlePublicInvitation(publicList, httptest.NewRequest(http.MethodGet, "/api/public/invitation/rina-bima/photos", nil))
	if !strings.Contains(publicList.Body.String(), "cdn.test") || photos[0].GuestID != budi.ID {
		t.Fatalf("approved photo should be public and linked to guest: %s", publicList.Body.String())
	}

	// 5. Patungan: only items marked as fundable accept contributions; funds are summed.
	server.store.UpdateSettings(inv.ID, map[string]any{"sections_config": map[string]any{
		"wishlist": map[string]any{"items": []any{
			map[string]any{"id": "w1", "name": "Kulkas", "fund": true, "target": 4000000},
			map[string]any{"id": "w2", "name": "Sprei"},
		}},
	}})
	settings := server.store.GetSettings(inv.ID)
	if _, ok := fundableWishlistItem(settings, "w1"); !ok {
		t.Fatal("w1 should be fundable")
	}
	if _, ok := fundableWishlistItem(settings, "w2"); ok {
		t.Fatal("w2 is not fundable")
	}
	_, _ = server.store.CreateGiftTransaction(store.GiftTransaction{InvitationID: inv.ID, Gateway: "mayar", GatewayReference: "r2", Amount: 500000, Status: "confirmed", SenderName: "Tim kantor", Purpose: "wishlist:w1"})
	_, _ = server.store.CreateGiftTransaction(store.GiftTransaction{InvitationID: inv.ID, Gateway: "mayar", GatewayReference: "r3", Amount: 900000, Status: "pending", SenderName: "X", Purpose: "wishlist:w1"})
	if funds := server.wishlistFunds(inv.ID); funds["w1"] != 500000 {
		t.Fatalf("funds = %v", funds)
	}

	// 7. Recap
	recap := httptest.NewRecorder()
	server.handlePublicInvitation(recap, httptest.NewRequest(http.MethodGet, "/api/public/invitation/rina-bima/recap", nil))
	if !strings.Contains(recap.Body.String(), `"checked_in":2`) {
		t.Fatalf("recap: %s", recap.Body.String())
	}
}
