package api

import (
	"encoding/json"
	"errors"
	"net/http"
	"strings"
	billingservice "yukakad/internal/billing"
	"yukakad/internal/store"
)

func (s *Server) handleBillingPlan(w http.ResponseWriter, r *http.Request) {
	claims, ok := s.requireAuth(w, r)
	if !ok {
		return
	}
	if r.Method == http.MethodGet {
		plan, err := s.billing.Current(claims.UserID)
		if err != nil {
			writeJSON(w, http.StatusNotFound, map[string]string{"error": err.Error()})
			return
		}
		writeJSON(w, http.StatusOK, plan)
		return
	}
	if r.Method != http.MethodPost {
		writeJSON(w, http.StatusMethodNotAllowed, map[string]string{"error": "method not allowed"})
		return
	}
	var payload struct {
		PlanID string `json:"plan_id"`
	}
	if json.NewDecoder(r.Body).Decode(&payload) != nil || payload.PlanID == "" {
		writeJSON(w, http.StatusBadRequest, map[string]string{"error": "plan_id is required"})
		return
	}
	if payload.PlanID != "free" {
		sub, paymentURL, err := s.billing.Checkout(claims.UserID, payload.PlanID, s.checkoutOptions())
		if err != nil {
			writeJSON(w, http.StatusBadRequest, map[string]string{"error": err.Error()})
			return
		}
		writeJSON(w, http.StatusCreated, map[string]any{"subscription": sub, "payment_url": paymentURL})
		return
	}
	plan, err := s.billing.ChangePlan(claims.UserID, payload.PlanID)
	if err != nil {
		status := http.StatusBadRequest
		if errors.Is(err, billingservice.ErrUserNotFound) {
			status = http.StatusNotFound
		}
		writeJSON(w, status, map[string]string{"error": err.Error()})
		return
	}
	_ = s.store.CreateAuditLog(claims.UserID, "", "billing.plan.change", map[string]any{"plan_id": plan.ID})
	writeJSON(w, http.StatusOK, plan)
}

func (s *Server) handleBillingCheckout(w http.ResponseWriter, r *http.Request) {
	claims, ok := s.requireAuth(w, r)
	if !ok {
		return
	}
	if r.Method != http.MethodPost {
		writeJSON(w, http.StatusMethodNotAllowed, map[string]string{"error": "method not allowed"})
		return
	}
	var payload struct {
		PlanID string `json:"plan_id"`
	}
	if json.NewDecoder(r.Body).Decode(&payload) != nil || payload.PlanID == "" {
		writeJSON(w, http.StatusBadRequest, map[string]string{"error": "plan_id is required"})
		return
	}
	sub, url, err := s.billing.Checkout(claims.UserID, payload.PlanID, s.checkoutOptions())
	if err != nil {
		writeJSON(w, http.StatusBadRequest, map[string]string{"error": err.Error()})
		return
	}
	writeJSON(w, http.StatusCreated, map[string]any{"subscription": sub, "payment_url": url})
}

func (s *Server) handleBillingSubscriptions(w http.ResponseWriter, r *http.Request) {
	claims, ok := s.requireAuth(w, r)
	if !ok {
		return
	}
	if r.Method != http.MethodGet {
		writeJSON(w, http.StatusMethodNotAllowed, map[string]string{"error": "method not allowed"})
		return
	}
	items, err := s.billing.History(claims.UserID)
	if err != nil {
		writeJSON(w, http.StatusNotFound, map[string]string{"error": err.Error()})
		return
	}
	writeJSON(w, http.StatusOK, map[string]any{"items": items})
}

func (s *Server) handleBillingInvoices(w http.ResponseWriter, r *http.Request) {
	claims, ok := s.requireAuth(w, r)
	if !ok {
		return
	}
	if r.Method != http.MethodGet {
		writeJSON(w, http.StatusMethodNotAllowed, map[string]string{"error": "method not allowed"})
		return
	}
	if _, err := s.billing.Current(claims.UserID); err != nil {
		writeJSON(w, http.StatusNotFound, map[string]string{"error": err.Error()})
		return
	}
	writeJSON(w, http.StatusOK, map[string]any{"items": s.store.ListInvoices(claims.UserID)})
}

func (s *Server) handleBillingEntitlements(w http.ResponseWriter, r *http.Request) {
	claims, ok := s.requireAuth(w, r)
	if !ok {
		return
	}
	if r.Method != http.MethodGet {
		writeJSON(w, http.StatusMethodNotAllowed, map[string]string{"error": "method not allowed"})
		return
	}
	features := []string{billingservice.FeaturePremiumTemplates, billingservice.FeatureCustomDomain, billingservice.FeaturePaymentGateway}
	result := make(map[string]bool, len(features))
	for _, feature := range features {
		allowed, err := s.billing.Allows(claims.UserID, feature)
		if err != nil {
			writeJSON(w, http.StatusServiceUnavailable, map[string]string{"error": err.Error()})
			return
		}
		result[feature] = allowed
	}
	writeJSON(w, http.StatusOK, map[string]any{"items": result})
}

func (s *Server) handleBillingDummyConfirm(w http.ResponseWriter, r *http.Request) {
	// Simulated payments only exist while the dummy gateway is active (never with Mayar or in production).
	if s.billing.Provider() != "dummy" {
		writeJSON(w, http.StatusNotFound, map[string]string{"error": "not found"})
		return
	}
	if r.Method != http.MethodPost {
		writeJSON(w, http.StatusMethodNotAllowed, map[string]string{"error": "method not allowed"})
		return
	}
	reference := strings.Trim(strings.TrimPrefix(r.URL.Path, "/api/billing/dummy/"), "/")
	if reference == "" {
		writeJSON(w, http.StatusBadRequest, map[string]string{"error": "reference is required"})
		return
	}
	sub, err := s.billing.Confirm(reference)
	if err != nil {
		writeJSON(w, http.StatusNotFound, map[string]string{"error": err.Error()})
		return
	}
	writeJSON(w, http.StatusOK, sub)
}

func (s *Server) checkoutOptions() billingservice.CheckoutOptions {
	return billingservice.CheckoutOptions{RedirectURL: strings.TrimRight(s.config.FrontendOrigin, "/") + "/payments/selesai"}
}

// POST /api/billing/verify — called by the return page: asks the gateway about the user's pending payments.
func (s *Server) handleBillingVerify(w http.ResponseWriter, r *http.Request) {
	claims, ok := s.requireAuth(w, r)
	if !ok {
		return
	}
	if r.Method != http.MethodPost {
		writeJSON(w, http.StatusMethodNotAllowed, map[string]string{"error": "method not allowed"})
		return
	}
	activated, err := s.billing.VerifyPending(r.Context(), claims.UserID)
	if err != nil && !errors.Is(err, billingservice.ErrGatewayDisabled) {
		writeJSON(w, http.StatusNotFound, map[string]string{"error": err.Error()})
		return
	}
	plan, err := s.billing.Current(claims.UserID)
	if err != nil {
		writeJSON(w, http.StatusNotFound, map[string]string{"error": err.Error()})
		return
	}
	pending := 0
	var latest *store.Subscription
	for _, sub := range s.store.ListSubscriptions(claims.UserID) {
		if sub.Status == "pending" {
			pending++
		}
		if latest == nil || sub.StartedAt.After(latest.StartedAt) {
			latest = sub
		}
	}
	latestStatus := ""
	if latest != nil {
		latestStatus = latest.Status
	}
	writeJSON(w, http.StatusOK, map[string]any{"plan": plan, "activated": activated, "pending": pending, "latest_status": latestStatus})
}
