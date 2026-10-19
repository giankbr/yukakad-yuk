package api

import (
	"encoding/json"
	"net/http"
	"sort"
	"time"

	"yukakad/internal/auth"
	"yukakad/internal/store"
)

// POST /api/auth/change-password {current_password, new_password}
func (s *Server) handleChangePassword(w http.ResponseWriter, r *http.Request) {
	claims, ok := s.requireAuth(w, r)
	if !ok {
		return
	}
	if r.Method != http.MethodPost {
		writeJSON(w, http.StatusMethodNotAllowed, map[string]string{"error": "method not allowed"})
		return
	}
	if !s.allowRate(w, "auth:change-password:"+claims.UserID, 10, 10*time.Minute) {
		return
	}
	var payload struct {
		Current string `json:"current_password"`
		New     string `json:"new_password"`
	}
	if json.NewDecoder(http.MaxBytesReader(w, r.Body, 4096)).Decode(&payload) != nil || len(payload.New) < 8 {
		writeJSON(w, http.StatusBadRequest, map[string]string{"error": "password baru minimal 8 karakter"})
		return
	}
	user, exists := s.store.FindUserByID(claims.UserID)
	if !exists || !auth.VerifyPassword(payload.Current, user.Password) {
		// 400, not 401: the session itself is fine, and clients log out on 401.
		writeJSON(w, http.StatusBadRequest, map[string]string{"error": "Password saat ini salah"})
		return
	}
	hashed, err := auth.HashPassword(payload.New)
	if err != nil {
		writeJSON(w, http.StatusBadRequest, map[string]string{"error": "password terlalu panjang"})
		return
	}
	if err := s.store.UpdatePassword(user.ID, hashed); err != nil {
		writeJSON(w, http.StatusInternalServerError, map[string]string{"error": "password belum tersimpan"})
		return
	}
	_ = s.store.CreateAuditLog(user.ID, "", "auth.password.change", nil)
	// Every earlier token is now invalid (see authenticateToken); hand this device a fresh one.
	token, err := s.issueToken(user)
	if err != nil {
		writeJSON(w, http.StatusOK, map[string]any{"changed": true})
		return
	}
	writeJSON(w, http.StatusOK, map[string]any{"changed": true, "token": token})
}

// GET /api/admin/payments — plan purchases and online-envelope money across all users.
func (s *Server) handleAdminPayments(w http.ResponseWriter, r *http.Request) {
	if _, ok := s.requireAdmin(w, r); !ok {
		return
	}
	if r.Method != http.MethodGet {
		writeJSON(w, http.StatusMethodNotAllowed, map[string]string{"error": "method not allowed"})
		return
	}
	type row struct {
		Subscription *store.Subscription `json:"subscription"`
		User         map[string]string   `json:"user"`
		PlanName     string              `json:"plan_name"`
		Amount       float64             `json:"amount"`
	}
	plans := map[string]*store.Plan{}
	for _, p := range s.store.ListPlans() {
		plans[p.ID] = p
	}
	rows := []row{}
	now := time.Now().UTC()
	monthStart := time.Date(now.Year(), now.Month(), 1, 0, 0, 0, 0, time.UTC)
	totals := map[string]float64{"revenue_total": 0, "revenue_month": 0, "paid_count": 0, "pending_count": 0}
	for _, user := range s.store.AdminListUsers() {
		for _, inv := range s.store.ListInvoices(user.ID) {
			if inv.Status != "paid" {
				continue
			}
			totals["revenue_total"] += inv.Amount
			totals["paid_count"]++
			if inv.PaidAt != nil && !inv.PaidAt.Before(monthStart) {
				totals["revenue_month"] += inv.Amount
			}
		}
		for _, sub := range s.store.ListSubscriptions(user.ID) {
			if sub.Provider == "" || sub.Provider == "manual" {
				continue
			}
			if sub.Status == "pending" {
				totals["pending_count"]++
			}
			name, amount := sub.PlanID, 0.0
			if p := plans[sub.PlanID]; p != nil {
				name, amount = p.Name, p.Price
			}
			rows = append(rows, row{sub, map[string]string{"id": user.ID, "name": user.Name, "email": user.Email}, name, amount})
		}
	}
	sort.Slice(rows, func(i, j int) bool { return rows[i].Subscription.StartedAt.After(rows[j].Subscription.StartedAt) })
	if len(rows) > 300 {
		rows = rows[:300]
	}
	envelopes := map[string]float64{"paid_out": 0, "requested": 0}
	for _, p := range s.store.ListAllGiftPayouts("") {
		if p.Status == "paid" || p.Status == "requested" {
			envelopes[p.Status] += p.Amount
		}
	}
	writeJSON(w, http.StatusOK, map[string]any{"items": rows, "totals": totals, "envelopes": envelopes, "gateway": s.billing.Provider()})
}
