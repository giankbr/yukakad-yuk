package api

import (
	"encoding/json"
	"errors"
	"net/http"
	"strings"
	billingservice "yukakad/internal/billing"
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
		sub, paymentURL, err := s.billing.Checkout(claims.UserID, payload.PlanID)
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
	sub, url, err := s.billing.Checkout(claims.UserID, payload.PlanID)
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
