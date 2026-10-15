package api

import (
	"encoding/json"
	"errors"
	"net/http"
	"strconv"
	"strings"

	billingservice "yukakad/internal/billing"
	giftservice "yukakad/internal/gifts"
	"yukakad/internal/store"
)

// Online envelopes ("amplop online lewat Rawuh"): guests pay via Mayar into Rawuh's account and the
// couple withdraws the balance with a payout request that an admin transfers manually.

type giftSettings struct {
	FeePercent float64 `json:"fee_percent"`
	MinPayout  float64 `json:"min_payout"`
}

// Admin-editable (site-content "gift_settings"); defaults: no fee, Rp50.000 minimum payout.
func (s *Server) giftSettings() giftSettings {
	settings := giftSettings{FeePercent: 0, MinPayout: 50000}
	content := s.store.GetSiteContent("gift_settings")
	if v, ok := number(content["fee_percent"]); ok && v >= 0 && v <= 50 {
		settings.FeePercent = v
	}
	if v, ok := number(content["min_payout"]); ok && v >= 0 {
		settings.MinPayout = v
	}
	return settings
}

func number(value any) (float64, bool) {
	switch v := value.(type) {
	case float64:
		return v, true
	case int:
		return float64(v), true
	case string:
		f, err := strconv.ParseFloat(strings.TrimSpace(v), 64)
		return f, err == nil
	}
	return 0, false
}

// onlineGiftConfig reads sections_config.onlineGift written by the dashboard.
func onlineGiftConfig(settings map[string]any) (enabled bool, note string) {
	sections, _ := settings["sections_config"].(map[string]any)
	if sections == nil {
		return false, ""
	}
	cfg, _ := sections["onlineGift"].(map[string]any)
	if cfg == nil {
		return false, ""
	}
	enabled, _ = cfg["enabled"].(bool)
	note, _ = cfg["note"].(string)
	return enabled, note
}

// onlineGiftState says whether guests of this invitation can pay an online envelope right now.
type onlineGiftState struct {
	Enabled      bool   `json:"enabled"`       // switched on by the couple
	Allowed      bool   `json:"allowed"`       // the couple's plan includes it
	GatewayReady bool   `json:"gateway_ready"` // a payment gateway is configured
	Active       bool   `json:"active"`        // all of the above
	Note         string `json:"note,omitempty"`
}

func (s *Server) onlineGift(invitation *store.Invitation) onlineGiftState {
	enabled, note := onlineGiftConfig(s.store.GetSettings(invitation.ID))
	allowed, _ := s.billing.Allows(invitation.UserID, billingservice.FeaturePaymentGateway)
	ready := s.gifts.Provider() != ""
	return onlineGiftState{Enabled: enabled, Allowed: allowed, GatewayReady: ready, Active: enabled && allowed && ready, Note: note}
}

// POST /api/public/invitation/{slug}/gift-transactions
func (s *Server) handlePublicGiftTransaction(w http.ResponseWriter, r *http.Request, slug string) {
	invitation, exists := s.store.FindInvitationBySlug(slug)
	if !exists || !invitation.Published {
		writeJSON(w, http.StatusNotFound, map[string]string{"error": "invitation not found"})
		return
	}
	if r.Method != http.MethodPost {
		writeJSON(w, http.StatusMethodNotAllowed, map[string]string{"error": "method not allowed"})
		return
	}
	if !s.onlineGift(invitation).Active {
		writeJSON(w, http.StatusForbidden, map[string]string{"error": "amplop online tidak aktif untuk undangan ini"})
		return
	}
	var payload struct {
		GuestID    string  `json:"guest_id"`
		SenderName string  `json:"sender_name"`
		Message    string  `json:"message"`
		Email      string  `json:"email"`
		Amount     float64 `json:"amount"`
		ReturnURL  string  `json:"return_url"`
		WishlistID string  `json:"wishlist_item_id"`
	}
	if json.NewDecoder(http.MaxBytesReader(w, r.Body, 8192)).Decode(&payload) != nil {
		writeJSON(w, http.StatusBadRequest, map[string]string{"error": "invalid payload"})
		return
	}
	// Only send guests back to this invitation on our own site.
	base := strings.TrimRight(s.config.FrontendOrigin, "/") + "/invitation/" + invitation.Slug
	returnURL := base + "?amplop=selesai"
	if strings.HasPrefix(payload.ReturnURL, base+"?") || payload.ReturnURL == base {
		returnURL = payload.ReturnURL
	}
	title := invitation.Title
	if invitation.Couple.BrideName != "" && invitation.Couple.GroomName != "" {
		title = invitation.Couple.BrideName + " & " + invitation.Couple.GroomName
	}
	email := strings.TrimSpace(payload.Email)
	if !strings.Contains(email, "@") || len(email) > 120 {
		email = ""
	}
	options := giftservice.CreateOptions{RedirectURL: returnURL, Email: email, Title: title}
	if payload.WishlistID != "" {
		itemName, ok := fundableWishlistItem(s.store.GetSettings(invitation.ID), payload.WishlistID)
		if !ok {
			writeJSON(w, http.StatusBadRequest, map[string]string{"error": "kado ini tidak menerima patungan"})
			return
		}
		options.Purpose = "wishlist:" + payload.WishlistID
		options.Title = itemName + " untuk " + title
	}
	tx, err := s.gifts.Create(invitation.ID, payload.GuestID, payload.SenderName, payload.Message, payload.Amount, options)
	if err != nil {
		status := http.StatusBadRequest
		switch {
		case errors.Is(err, giftservice.ErrNotFound):
			status = http.StatusNotFound
		case errors.Is(err, giftservice.ErrUnavailable):
			status = http.StatusServiceUnavailable
		case !errors.Is(err, giftservice.ErrInvalid):
			status = http.StatusBadGateway
		}
		writeJSON(w, status, map[string]string{"error": err.Error()})
		return
	}
	writeJSON(w, http.StatusCreated, map[string]any{"id": tx.ID, "reference": tx.GatewayReference, "amount": tx.Amount, "status": tx.Status, "payment_url": tx.PaymentURL})
}

// POST /api/public/gift-transactions/{reference}/verify — the guest's return page asks for the outcome.
func (s *Server) handlePublicGiftVerify(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		writeJSON(w, http.StatusMethodNotAllowed, map[string]string{"error": "method not allowed"})
		return
	}
	reference := strings.TrimSuffix(strings.Trim(strings.TrimPrefix(r.URL.Path, "/api/public/gift-transactions/"), "/"), "/verify")
	if reference == "" || strings.Contains(reference, "/") {
		writeJSON(w, http.StatusNotFound, map[string]string{"error": "not found"})
		return
	}
	tx, err := s.gifts.ConfirmPaid(r.Context(), reference)
	if err == nil {
		writeJSON(w, http.StatusOK, map[string]any{"status": "confirmed", "amount": tx.Amount, "sender_name": tx.SenderName})
		return
	}
	if errors.Is(err, giftservice.ErrNotFound) {
		writeJSON(w, http.StatusNotFound, map[string]string{"error": "not found"})
		return
	}
	status := "pending"
	if current, ok := s.store.FindGiftTransactionByReference(reference); ok && current.Status == "failed" {
		status = "failed"
	}
	writeJSON(w, http.StatusOK, map[string]any{"status": status})
}

func (s *Server) ownedInvitation(w http.ResponseWriter, r *http.Request, invitationID string) (*store.Invitation, string, bool) {
	claims, ok := s.requireAuth(w, r)
	if !ok {
		return nil, "", false
	}
	invitation, exists := s.store.FindInvitationByID(invitationID)
	if !exists || invitation.UserID != claims.UserID {
		writeJSON(w, http.StatusNotFound, map[string]string{"error": "invitation not found"})
		return nil, "", false
	}
	return invitation, claims.UserID, true
}

func onlineTransactions(items []*store.GiftTransaction) []*store.GiftTransaction {
	out := make([]*store.GiftTransaction, 0, len(items))
	for _, tx := range items {
		if tx.Gateway == "mayar" || tx.Gateway == "dummy" {
			out = append(out, tx)
		}
	}
	return out
}

// GET  /api/invitations/{id}/gift-wallet          balance, envelopes, payouts
// POST /api/invitations/{id}/gift-wallet/verify   re-check pending envelopes with the gateway
// POST /api/invitations/{id}/gift-payouts         request a withdrawal
func (s *Server) handleGiftWallet(w http.ResponseWriter, r *http.Request, invitationID, action string) {
	invitation, userID, ok := s.ownedInvitation(w, r, invitationID)
	if !ok {
		return
	}
	settings := s.giftSettings()
	switch {
	case action == "wallet" && r.Method == http.MethodGet:
	case action == "verify" && r.Method == http.MethodPost:
		s.gifts.VerifyPending(r.Context(), invitation.ID)
	case action == "payout" && r.Method == http.MethodPost:
		var payload struct {
			Amount        float64 `json:"amount"`
			BankName      string  `json:"bank_name"`
			AccountNumber string  `json:"account_number"`
			AccountName   string  `json:"account_name"`
		}
		if json.NewDecoder(http.MaxBytesReader(w, r.Body, 4096)).Decode(&payload) != nil {
			writeJSON(w, http.StatusBadRequest, map[string]string{"error": "invalid payload"})
			return
		}
		payout, err := s.gifts.RequestPayout(userID, invitation.ID, giftservice.PayoutRequest{Amount: payload.Amount, BankName: payload.BankName, AccountNumber: payload.AccountNumber, AccountName: payload.AccountName}, settings.FeePercent, settings.MinPayout)
		if err != nil {
			status := http.StatusBadRequest
			if errors.Is(err, giftservice.ErrNotFound) {
				status = http.StatusNotFound
			}
			writeJSON(w, status, map[string]string{"error": err.Error()})
			return
		}
		_ = s.store.CreateAuditLog(userID, invitation.ID, "gift.payout.request", map[string]any{"payout_id": payout.ID, "amount": payout.Amount})
		writeJSON(w, http.StatusCreated, payout)
		return
	default:
		writeJSON(w, http.StatusMethodNotAllowed, map[string]string{"error": "method not allowed"})
		return
	}
	writeJSON(w, http.StatusOK, map[string]any{
		"online":       s.onlineGift(invitation),
		"settings":     settings,
		"wallet":       s.gifts.Wallet(invitation.ID, settings.FeePercent),
		"transactions": onlineTransactions(s.store.ListGiftTransactions(invitation.ID)),
		"payouts":      s.store.ListGiftPayouts(invitation.ID),
	})
}

// GET   /api/admin/gift-payouts?status=requested
// PATCH /api/admin/gift-payouts/{id}  {status: paid|rejected, note}
func (s *Server) handleAdminGiftPayouts(w http.ResponseWriter, r *http.Request) {
	claims, ok := s.requireAdmin(w, r)
	if !ok {
		return
	}
	id := strings.Trim(strings.TrimPrefix(r.URL.Path, "/api/admin/gift-payouts"), "/")
	if id == "" && r.Method == http.MethodGet {
		items := s.store.ListAllGiftPayouts(r.URL.Query().Get("status"))
		out := make([]map[string]any, 0, len(items))
		for _, p := range items {
			row := map[string]any{"payout": p}
			if inv, ok := s.store.FindInvitationByID(p.InvitationID); ok {
				row["invitation"] = map[string]string{"id": inv.ID, "slug": inv.Slug, "title": inv.Title}
			}
			if user, ok := s.store.FindUserByID(p.UserID); ok {
				row["user"] = map[string]string{"id": user.ID, "name": user.Name, "email": user.Email}
			}
			if p.Status == "requested" {
				row["wallet"] = s.gifts.Wallet(p.InvitationID, s.giftSettings().FeePercent)
			}
			out = append(out, row)
		}
		writeJSON(w, http.StatusOK, map[string]any{"items": out, "settings": s.giftSettings()})
		return
	}
	if id == "" || (r.Method != http.MethodPatch && r.Method != http.MethodPut) {
		writeJSON(w, http.StatusMethodNotAllowed, map[string]string{"error": "method not allowed"})
		return
	}
	var payload struct {
		Status string `json:"status"`
		Note   string `json:"note"`
	}
	if json.NewDecoder(http.MaxBytesReader(w, r.Body, 4096)).Decode(&payload) != nil {
		writeJSON(w, http.StatusBadRequest, map[string]string{"error": "invalid payload"})
		return
	}
	payout, err := s.gifts.ProcessPayout(id, payload.Status, payload.Note)
	if err != nil {
		status := http.StatusBadRequest
		if errors.Is(err, giftservice.ErrNotFound) {
			status = http.StatusNotFound
		}
		writeJSON(w, status, map[string]string{"error": err.Error()})
		return
	}
	_ = s.store.CreateAuditLog(claims.UserID, payout.InvitationID, "gift.payout."+payout.Status, map[string]any{"payout_id": payout.ID, "amount": payout.Amount})
	writeJSON(w, http.StatusOK, payout)
}

func publicOnlineGift(state onlineGiftState, settings giftSettings) map[string]any {
	if !state.Active {
		return map[string]any{"active": false}
	}
	return map[string]any{"active": true, "note": state.Note, "min_amount": giftservice.MinAmount, "max_amount": giftservice.MaxAmount, "fee_percent": settings.FeePercent}
}
