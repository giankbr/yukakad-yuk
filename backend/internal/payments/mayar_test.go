package payments

import (
	"context"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"testing"
)

func TestMayarCreateAndStatus(t *testing.T) {
	var body map[string]any
	srv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		if r.Header.Get("Authorization") != "Bearer test-key" {
			w.WriteHeader(http.StatusUnauthorized)
			_, _ = w.Write([]byte(`{"statusCode":401,"messages":"unauthorized"}`))
			return
		}
		switch {
		case r.Method == http.MethodPost && r.URL.Path == "/hl/v2/payments/create":
			_ = json.NewDecoder(r.Body).Decode(&body)
			_, _ = w.Write([]byte(`{"statusCode":200,"messages":"success","data":{"id":"req-1","transactionId":"tx-1","link":"https://rawuh.myr.id/pl/abc"}}`))
		case r.Method == http.MethodGet && r.URL.Path == "/hl/v2/payments/req-1":
			_, _ = w.Write([]byte(`{"statusCode":200,"messages":"success","data":{"id":"req-1","status":"paid"}}`))
		default:
			w.WriteHeader(http.StatusNotFound)
			_, _ = w.Write([]byte(`{"statusCode":404,"messages":"not found"}`))
		}
	}))
	defer srv.Close()

	m := &Mayar{APIKey: "test-key", BaseURL: srv.URL + "/hl/v2", Client: srv.Client()}
	payment, err := m.Create(context.Background(), Request{Amount: 149000.4, Name: "Paket Rayakan", Email: "a@b.id", RedirectURL: "https://rawuh.id/payments/selesai"})
	if err != nil {
		t.Fatal(err)
	}
	if payment.Reference != "req-1" || payment.CheckoutURL != "https://rawuh.myr.id/pl/abc" {
		t.Fatalf("unexpected payment %+v", payment)
	}
	if body["amount"].(float64) != 149000 || body["name"] != "Paket Rayakan" || body["redirectUrl"] != "https://rawuh.id/payments/selesai" {
		t.Fatalf("unexpected body %v", body)
	}
	if _, has := body["mobile"]; has {
		t.Fatalf("empty optional fields must be omitted: %v", body)
	}
	status, err := m.Status(context.Background(), "req-1")
	if err != nil || status != StatusPaid {
		t.Fatalf("status = %q, %v", status, err)
	}
	if _, err := m.Status(context.Background(), "missing"); err == nil {
		t.Fatal("expected error for missing payment")
	}
	bad := &Mayar{APIKey: "wrong", BaseURL: m.BaseURL, Client: srv.Client()}
	if _, err := bad.Create(context.Background(), Request{Amount: 1000, Name: "x"}); err == nil {
		t.Fatal("expected auth error")
	}
}

func TestNewMayarEnvironment(t *testing.T) {
	if NewMayar("k", "production").BaseURL != MayarProductionURL || NewMayar("k", "").BaseURL != MayarSandboxURL {
		t.Fatal("wrong base URL selection")
	}
}
