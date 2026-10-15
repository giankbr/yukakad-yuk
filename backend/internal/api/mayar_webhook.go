package api

import (
	"crypto/subtle"
	"encoding/json"
	"io"
	"log"
	"net/http"
	"strings"
)

// POST /api/webhooks/mayar?token=PAYMENT_WEBHOOK_SECRET
//
// Mayar webhooks are not signed, so the body is only a hint: every candidate payment is re-checked
// against Mayar's API (GET /payments/{id}) before a plan is activated. The URL token just keeps
// strangers from making us call Mayar.
func (s *Server) handleMayarWebhook(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		writeJSON(w, http.StatusMethodNotAllowed, map[string]string{"error": "method not allowed"})
		return
	}
	if s.billing.Provider() != "mayar" && s.gifts.Provider() != "mayar" {
		writeJSON(w, http.StatusServiceUnavailable, map[string]string{"error": "mayar is not configured"})
		return
	}
	if secret := s.config.PaymentWebhookSecret; secret != "" {
		token := r.URL.Query().Get("token")
		if subtle.ConstantTimeCompare([]byte(token), []byte(secret)) != 1 {
			writeJSON(w, http.StatusUnauthorized, map[string]string{"error": "invalid webhook token"})
			return
		}
	}
	raw, err := io.ReadAll(io.LimitReader(r.Body, 1<<20))
	if err != nil {
		writeJSON(w, http.StatusBadRequest, map[string]string{"error": "invalid payload"})
		return
	}
	var payload struct {
		Event string         `json:"event"`
		Data  map[string]any `json:"data"`
	}
	if json.Unmarshal(raw, &payload) != nil {
		writeJSON(w, http.StatusBadRequest, map[string]string{"error": "invalid payload"})
		return
	}
	event := strings.ToLower(payload.Event)
	if event == "" {
		var alt struct {
			Event struct {
				Received string `json:"received"`
			} `json:"event"`
		}
		if json.Unmarshal(raw, &alt) == nil {
			event = strings.ToLower(alt.Event.Received)
		}
	}
	if event != "" && event != "payment.received" {
		writeJSON(w, http.StatusOK, map[string]any{"ok": true, "ignored": event})
		return
	}

	// Candidate references: the payment request id may arrive as id, productId, paymentRequestId, …
	seen := map[string]bool{}
	candidates := []string{}
	for _, key := range []string{"productId", "paymentRequestId", "paymentLinkId", "id", "transactionId"} {
		if value, ok := payload.Data[key].(string); ok && value != "" && !seen[value] {
			seen[value] = true
			candidates = append(candidates, value)
		}
	}
	confirmed := 0
	for _, reference := range candidates {
		if _, ok := s.store.FindGiftTransactionByReference(reference); ok {
			if _, err := s.gifts.ConfirmPaid(r.Context(), reference); err == nil {
				confirmed++
			} else {
				log.Printf("mayar webhook gift: %s: %v", reference, err)
			}
			continue
		}
		if _, ok := s.store.FindSubscriptionByReference(reference); !ok {
			continue
		}
		if _, err := s.billing.ConfirmPaid(r.Context(), reference); err == nil {
			confirmed++
		} else {
			log.Printf("mayar webhook: %s: %v", reference, err)
		}
	}
	// Fallback: no id matched, so re-check the payer's pending payments by email.
	if confirmed == 0 {
		if email, ok := payload.Data["customerEmail"].(string); ok && email != "" {
			if user, found := s.store.FindUserByEmail(strings.ToLower(strings.TrimSpace(email))); found {
				activated, _ := s.billing.VerifyPending(r.Context(), user.ID)
				confirmed += len(activated)
			}
		}
	}
	writeJSON(w, http.StatusOK, map[string]any{"ok": true, "confirmed": confirmed})
}
