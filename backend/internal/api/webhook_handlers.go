package api

import (
	"bytes"
	"encoding/json"
	"io"
	"net/http"
	"yukakad/internal/webhooks"
)

func (s *Server) handlePaymentWebhook(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		writeJSON(w, http.StatusMethodNotAllowed, map[string]string{"error": "method not allowed"})
		return
	}
	if s.config.PaymentWebhookSecret == "" {
		writeJSON(w, http.StatusServiceUnavailable, map[string]string{"error": "payment webhook is not configured"})
		return
	}
	body, err := io.ReadAll(io.LimitReader(r.Body, 1<<20))
	if err != nil || !webhooks.Verify(body, r.Header.Get("X-Webhook-Signature"), s.config.PaymentWebhookSecret) {
		writeJSON(w, http.StatusUnauthorized, map[string]string{"error": "invalid webhook signature"})
		return
	}
	r.Body = io.NopCloser(bytes.NewReader(body))
	var payload struct {
		Reference string `json:"reference"`
		Status    string `json:"status"`
	}
	if json.NewDecoder(r.Body).Decode(&payload) != nil || payload.Reference == "" || payload.Status == "" {
		writeJSON(w, http.StatusBadRequest, map[string]string{"error": "reference and status are required"})
		return
	}
	if payload.Status != "confirmed" {
		writeJSON(w, http.StatusBadRequest, map[string]string{"error": "unsupported webhook status"})
		return
	}
	sub, err := s.billing.Confirm(payload.Reference)
	if err != nil {
		writeJSON(w, http.StatusNotFound, map[string]string{"error": err.Error()})
		return
	}
	writeJSON(w, http.StatusOK, sub)
}
