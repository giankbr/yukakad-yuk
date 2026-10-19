package api

import (
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"strings"
	"sync"
	"testing"

	"yukakad/internal/auth"
	billingservice "yukakad/internal/billing"
	"yukakad/internal/config"
	giftservice "yukakad/internal/gifts"
	"yukakad/internal/payments"
	"yukakad/internal/store"
)

func TestOnlineGiftFlow(t *testing.T) {
	var mu sync.Mutex
	status := map[string]string{}
	var lastBody map[string]any
	next := 0
	fake := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		mu.Lock()
		defer mu.Unlock()
		if r.Method == http.MethodPost {
			_ = json.NewDecoder(r.Body).Decode(&lastBody)
			next++
			id := "gift-req-" + string(rune('0'+next))
			status[id] = "unpaid"
			_, _ = w.Write([]byte(`{"statusCode":200,"data":{"id":"` + id + `","link":"https://rawuh.myr.id/pl/` + id + `"}}`))
			return
		}
		id := r.URL.Path[strings.LastIndex(r.URL.Path, "/")+1:]
		_, _ = w.Write([]byte(`{"statusCode":200,"data":{"id":"` + id + `","status":"` + status[id] + `"}}`))
	}))
	defer fake.Close()
	pay := func(id string) { mu.Lock(); status[id] = "paid"; mu.Unlock() }

	cfg := config.Config{Port: "8080", Environment: "test", JWTSecret: "secret", FrontendOrigin: "https://rawuh.test", PaymentWebhookSecret: "tok"}
	server := NewServer(cfg)
	server.store.SeedPlans()
	mayar := &payments.Mayar{APIKey: "k", BaseURL: fake.URL + "/hl/v2", Client: fake.Client()}
	server.billing = billingservice.NewService(server.store, mayar)
	server.gifts = giftservice.NewService(server.store, mayar)

	owner, _ := server.store.CreateUser("Rina", "rina@example.com", "hash")
	other, _ := server.store.CreateUser("Eve", "eve@example.com", "hash")
	admin, _ := server.store.CreateUser("Admin", "admin@example.com", "hash")
	ownerToken := auth.GenerateToken(owner.ID, owner.Email, "user", cfg.JWTSecret)
	otherToken := auth.GenerateToken(other.ID, other.Email, "user", cfg.JWTSecret)
	adminToken := auth.GenerateToken(admin.ID, admin.Email, "admin", cfg.JWTSecret)
	inv, _ := server.store.CreateInvitation(owner.ID, "rina-bima", "Rina & Bima")
	_, _ = server.store.UpdateInvitation(inv.ID, "rina-bima", "Rina & Bima", true, store.Couple{BrideName: "Rina", GroomName: "Bima"}, store.Event{})

	call := func(handler http.HandlerFunc, token, method, path, body string) *httptest.ResponseRecorder {
		req := httptest.NewRequest(method, path, strings.NewReader(body))
		if token != "" {
			req.Header.Set("Authorization", "Bearer "+token)
		}
		rec := httptest.NewRecorder()
		handler(rec, req)
		return rec
	}
	public := func(method, path, body string) *httptest.ResponseRecorder {
		return call(server.handlePublicInvitation, "", method, path, body)
	}
	give := `{"sender_name":"Pak Budi","message":"Selamat!","amount":250000,"return_url":"https://rawuh.test/invitation/rina-bima?to=abc&amplop=selesai"}`

	// Not switched on → 403, and the public payload says inactive.
	if code := public(http.MethodPost, "/api/public/invitation/rina-bima/gift-transactions", give).Code; code != http.StatusForbidden {
		t.Fatalf("disabled online gift should be 403, got %d", code)
	}
	server.store.UpdateSettings(inv.ID, map[string]any{"sections_config": map[string]any{"onlineGift": map[string]any{"enabled": true}}})
	// Enabled but the free plan doesn't include it.
	if code := public(http.MethodPost, "/api/public/invitation/rina-bima/gift-transactions", give).Code; code != http.StatusForbidden {
		t.Fatalf("plan without payment gateway should be 403, got %d", code)
	}
	_ = server.store.SetUserPlan(owner.ID, "premium")
	// Plan + couple OK, but Rawuh hasn't opened online envelopes platform-wide yet.
	if code := public(http.MethodPost, "/api/public/invitation/rina-bima/gift-transactions", give).Code; code != http.StatusForbidden {
		t.Fatalf("platform switch off should be 403, got %d", code)
	}
	server.store.UpdateSiteContent("gift_settings", map[string]any{"online_enabled": true})
	if body := public(http.MethodGet, "/api/public/invitation/rina-bima", "").Body.String(); !strings.Contains(body, `"online_gift":{"active":true`) {
		t.Fatalf("public payload should expose active online gift: %s", body)
	}

	// Too small amount rejected; valid one goes to Mayar with our return URL.
	if code := public(http.MethodPost, "/api/public/invitation/rina-bima/gift-transactions", `{"sender_name":"x","amount":5000}`).Code; code != http.StatusBadRequest {
		t.Fatalf("small amount should be 400, got %d", code)
	}
	rec := public(http.MethodPost, "/api/public/invitation/rina-bima/gift-transactions", give)
	if rec.Code != http.StatusCreated || !strings.Contains(rec.Body.String(), "https://rawuh.myr.id/pl/gift-req-1") {
		t.Fatalf("create gift: %d %s", rec.Code, rec.Body.String())
	}
	if lastBody["redirectUrl"] != "https://rawuh.test/invitation/rina-bima?to=abc&amplop=selesai" || lastBody["name"] != "Amplop untuk Rina & Bima" {
		t.Fatalf("unexpected mayar body %v", lastBody)
	}
	// Foreign return URLs are replaced.
	public(http.MethodPost, "/api/public/invitation/rina-bima/gift-transactions", `{"sender_name":"Ani","amount":100000,"return_url":"https://evil.example/phish"}`)
	if lastBody["redirectUrl"] != "https://rawuh.test/invitation/rina-bima?amplop=selesai" {
		t.Fatalf("return url must stay on our site: %v", lastBody["redirectUrl"])
	}

	// Owner cannot mark an online envelope paid by hand.
	txs := server.store.ListGiftTransactions(inv.ID)
	var first *store.GiftTransaction
	for _, tx := range txs {
		if tx.GatewayReference == "gift-req-1" {
			first = tx
		}
	}
	if code := call(func(w http.ResponseWriter, r *http.Request) { server.handleGiftTransactions(w, r, inv.ID) }, ownerToken, http.MethodPatch, "/api/invitations/"+inv.ID+"/gift-transactions/"+first.ID, `{"status":"confirmed"}`).Code; code != http.StatusBadRequest {
		t.Fatalf("manual confirm of online envelope should be 400, got %d", code)
	}

	verify := func(ref string) string {
		return call(server.handlePublicGiftVerify, "", http.MethodPost, "/api/public/gift-transactions/"+ref+"/verify", "").Body.String()
	}
	if body := verify("gift-req-1"); !strings.Contains(body, `"pending"`) {
		t.Fatalf("unpaid verify: %s", body)
	}
	pay("gift-req-1")
	if body := verify("gift-req-1"); !strings.Contains(body, `"confirmed"`) {
		t.Fatalf("paid verify: %s", body)
	}
	// Second envelope confirmed by webhook.
	pay("gift-req-2")
	if body := call(server.handleMayarWebhook, "", http.MethodPost, "/api/webhooks/mayar?token=tok", `{"event":"payment.received","data":{"productId":"gift-req-2"}}`).Body.String(); !strings.Contains(body, `"confirmed":1`) {
		t.Fatalf("webhook gift: %s", body)
	}

	// Wallet with a 5% fee: 350.000 received → 17.500 fee → 332.500 available.
	server.store.UpdateSiteContent("gift_settings", map[string]any{"online_enabled": true, "fee_percent": 5, "min_payout": 50000})
	wallet := func(token string) *httptest.ResponseRecorder {
		return call(func(w http.ResponseWriter, r *http.Request) { server.handleGiftWallet(w, r, inv.ID, "wallet") }, token, http.MethodGet, "/", "")
	}
	if code := wallet(otherToken).Code; code != http.StatusNotFound {
		t.Fatalf("other user wallet should be 404, got %d", code)
	}
	body := wallet(ownerToken).Body.String()
	if !strings.Contains(body, `"received":350000`) || !strings.Contains(body, `"available":332500`) {
		t.Fatalf("wallet: %s", body)
	}
	payout := func(amount string) *httptest.ResponseRecorder {
		return call(func(w http.ResponseWriter, r *http.Request) { server.handleGiftWallet(w, r, inv.ID, "payout") }, ownerToken, http.MethodPost, "/",
			`{"amount":`+amount+`,"bank_name":"BCA","account_number":"1234567890","account_name":"Rina Maharani"}`)
	}
	if code := payout("400000").Code; code != http.StatusBadRequest {
		t.Fatalf("over-balance payout should be 400, got %d", code)
	}
	if code := payout("20000").Code; code != http.StatusBadRequest {
		t.Fatalf("below minimum payout should be 400, got %d", code)
	}
	rec = payout("300000")
	if rec.Code != http.StatusCreated {
		t.Fatalf("payout: %d %s", rec.Code, rec.Body.String())
	}
	var created store.GiftPayout
	_ = json.Unmarshal(rec.Body.Bytes(), &created)
	if code := payout("40000").Code; code != http.StatusBadRequest {
		t.Fatalf("requested amount must be reserved, got %d", code)
	}

	// Admin sees and settles it.
	list := call(server.handleAdminGiftPayouts, adminToken, http.MethodGet, "/api/admin/gift-payouts?status=requested", "").Body.String()
	if !strings.Contains(list, created.ID) || !strings.Contains(list, "rina@example.com") {
		t.Fatalf("admin list: %s", list)
	}
	if code := call(server.handleAdminGiftPayouts, ownerToken, http.MethodGet, "/api/admin/gift-payouts", "").Code; code != http.StatusForbidden {
		t.Fatalf("non-admin should be 403, got %d", code)
	}
	if code := call(server.handleAdminGiftPayouts, adminToken, http.MethodPatch, "/api/admin/gift-payouts/"+created.ID, `{"status":"paid","note":"BCA ref 889"}`).Code; code != http.StatusOK {
		t.Fatalf("mark paid: %d", code)
	}
	if code := call(server.handleAdminGiftPayouts, adminToken, http.MethodPatch, "/api/admin/gift-payouts/"+created.ID, `{"status":"rejected"}`).Code; code != http.StatusBadRequest {
		t.Fatalf("double processing should be 400, got %d", code)
	}
	if body := wallet(ownerToken).Body.String(); !strings.Contains(body, `"paid_out":300000`) || !strings.Contains(body, `"available":32500`) {
		t.Fatalf("wallet after payout: %s", body)
	}
}
