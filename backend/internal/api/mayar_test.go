package api

import (
	"net/http"
	"net/http/httptest"
	"strings"
	"sync"
	"testing"

	"yukakad/internal/auth"
	billingservice "yukakad/internal/billing"
	"yukakad/internal/config"
	"yukakad/internal/payments"
)

func TestMayarCheckoutWebhookAndVerify(t *testing.T) {
	var mu sync.Mutex
	status := map[string]string{}
	next := 0
	fake := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		mu.Lock()
		defer mu.Unlock()
		if r.Method == http.MethodPost && strings.HasSuffix(r.URL.Path, "/payments/create") {
			next++
			id := "req-" + string(rune('0'+next))
			status[id] = "unpaid"
			_, _ = w.Write([]byte(`{"statusCode":200,"messages":"success","data":{"id":"` + id + `","link":"https://rawuh.myr.id/pl/` + id + `"}}`))
			return
		}
		id := r.URL.Path[strings.LastIndex(r.URL.Path, "/")+1:]
		if s, ok := status[id]; ok {
			_, _ = w.Write([]byte(`{"statusCode":200,"messages":"success","data":{"id":"` + id + `","status":"` + s + `"}}`))
			return
		}
		w.WriteHeader(http.StatusNotFound)
	}))
	defer fake.Close()
	markPaid := func(id string) { mu.Lock(); status[id] = "paid"; mu.Unlock() }

	cfg := config.Config{Port: "8080", Environment: "test", JWTSecret: "secret", FrontendOrigin: "https://rawuh.test", PaymentWebhookSecret: "hook-token"}
	server := NewServer(cfg)
	server.store.SeedPlans()
	server.billing = billingservice.NewService(server.store, &payments.Mayar{APIKey: "k", BaseURL: fake.URL + "/hl/v2", Client: fake.Client()})
	user, _ := server.store.CreateUser("Ayu", "ayu@example.com", "hash")
	token := auth.GenerateToken(user.ID, user.Email, "user", cfg.JWTSecret)

	call := func(handler http.HandlerFunc, method, path, body string) *httptest.ResponseRecorder {
		req := httptest.NewRequest(method, path, strings.NewReader(body))
		req.Header.Set("Authorization", "Bearer "+token)
		rec := httptest.NewRecorder()
		handler(rec, req)
		return rec
	}

	// Checkout returns Mayar's link.
	rec := call(server.handleBillingCheckout, http.MethodPost, "/api/billing/checkout", `{"plan_id":"pro"}`)
	if rec.Code != http.StatusCreated || !strings.Contains(rec.Body.String(), "https://rawuh.myr.id/pl/req-1") {
		t.Fatalf("checkout: %d %s", rec.Code, rec.Body.String())
	}
	// Dummy confirm is disabled while Mayar is active.
	if code := call(server.handleBillingDummyConfirm, http.MethodPost, "/api/billing/dummy/req-1", "").Code; code != http.StatusNotFound {
		t.Fatalf("dummy confirm should be 404, got %d", code)
	}
	// Webhook without token is rejected; with token but unpaid it does nothing.
	if code := call(server.handleMayarWebhook, http.MethodPost, "/api/webhooks/mayar", `{"event":"payment.received","data":{"productId":"req-1"}}`).Code; code != http.StatusUnauthorized {
		t.Fatalf("webhook without token: %d", code)
	}
	rec = call(server.handleMayarWebhook, http.MethodPost, "/api/webhooks/mayar?token=hook-token", `{"event":"payment.received","data":{"productId":"req-1"}}`)
	if !strings.Contains(rec.Body.String(), `"confirmed":0`) {
		t.Fatalf("forged webhook must not activate: %s", rec.Body.String())
	}
	if plan, _ := server.billing.Current(user.ID); plan.ID == "pro" {
		t.Fatal("plan activated without payment")
	}
	// Paid at Mayar → webhook activates.
	markPaid("req-1")
	rec = call(server.handleMayarWebhook, http.MethodPost, "/api/webhooks/mayar?token=hook-token", `{"event":"payment.received","data":{"id":"tx-9","productId":"req-1"}}`)
	if !strings.Contains(rec.Body.String(), `"confirmed":1`) {
		t.Fatalf("webhook should confirm: %s", rec.Body.String())
	}
	if plan, _ := server.billing.Current(user.ID); plan.ID != "pro" {
		t.Fatalf("expected pro, got %s", plan.ID)
	}
	// Duplicate webhook is harmless (one invoice).
	call(server.handleMayarWebhook, http.MethodPost, "/api/webhooks/mayar?token=hook-token", `{"event":"payment.received","data":{"productId":"req-1"}}`)
	if n := len(server.store.ListInvoices(user.ID)); n != 1 {
		t.Fatalf("expected 1 invoice, got %d", n)
	}

	// Second checkout confirmed through the return page instead (email fallback not needed).
	call(server.handleBillingCheckout, http.MethodPost, "/api/billing/checkout", `{"plan_id":"pro"}`)
	rec = call(server.handleBillingVerify, http.MethodPost, "/api/billing/verify", "")
	if !strings.Contains(rec.Body.String(), `"pending":1`) {
		t.Fatalf("verify should report pending: %s", rec.Body.String())
	}
	markPaid("req-2")
	rec = call(server.handleBillingVerify, http.MethodPost, "/api/billing/verify", "")
	if !strings.Contains(rec.Body.String(), `"pending":0`) || !strings.Contains(rec.Body.String(), "req-2") {
		t.Fatalf("verify should activate: %s", rec.Body.String())
	}

	// Webhook matched only by customer email.
	call(server.handleBillingCheckout, http.MethodPost, "/api/billing/checkout", `{"plan_id":"pro"}`)
	markPaid("req-3")
	rec = call(server.handleMayarWebhook, http.MethodPost, "/api/webhooks/mayar?token=hook-token", `{"event":"payment.received","data":{"id":"unknown","customerEmail":"ayu@example.com"}}`)
	if !strings.Contains(rec.Body.String(), `"confirmed":1`) {
		t.Fatalf("email fallback should confirm: %s", rec.Body.String())
	}
}

func TestProductionWithoutMayarHasNoGateway(t *testing.T) {
	if billingGateway(config.Config{Environment: "production"}) != nil {
		t.Fatal("production without MAYAR_API_KEY must not fall back to the dummy gateway")
	}
	if billingGateway(config.Config{Environment: "development"}).Name() != "dummy" {
		t.Fatal("development should use dummy")
	}
	if billingGateway(config.Config{Environment: "production", MayarAPIKey: "k"}).Name() != "mayar" {
		t.Fatal("key should select mayar")
	}
}
