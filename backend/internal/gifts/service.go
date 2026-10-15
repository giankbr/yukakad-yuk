package gifts

import (
	"context"
	"errors"
	"fmt"
	"log"
	"math"
	"strings"
	"sync"
	"time"
	"yukakad/internal/payments"
	"yukakad/internal/store"
)

var (
	ErrNotFound    = errors.New("gift transaction not found")
	ErrInvalid     = errors.New("invalid gift transaction")
	ErrUnavailable = errors.New("online envelopes are not available")
	ErrNotPaid     = errors.New("payment not completed")
	ErrBalance     = errors.New("amount exceeds available balance")
)

// Limits for a single online envelope (Rupiah).
const (
	MinAmount = 10000
	MaxAmount = 100000000
)

// Service handles online envelopes: guests pay through Rawuh's payment gateway (Mayar), the money is held
// by Rawuh and the couple withdraws it with a payout request. Direct transfers to the couple's own accounts
// are the separate "gifts" methods (bank / e-wallet / QRIS) and never pass through here.
type Service struct {
	store   store.Store
	gateway payments.Gateway
	mu      sync.Mutex // serialises confirmations and payout requests
}

func NewService(dataStore store.Store, gateway payments.Gateway) *Service {
	return &Service{store: dataStore, gateway: gateway}
}

// Provider is the active gateway name, or "" when online envelopes can't be paid.
func (s *Service) Provider() string {
	if s.gateway == nil {
		return ""
	}
	return s.gateway.Name()
}

// online reports whether a transaction was paid through a gateway (and is therefore held by Rawuh).
func online(tx *store.GiftTransaction) bool { return tx.Gateway == "mayar" || tx.Gateway == "dummy" }

type CreateOptions struct {
	RedirectURL string
	Email       string
	Title       string
}

func (s *Service) Create(invitationID, guestID, sender, message string, amount float64, options CreateOptions) (*store.GiftTransaction, error) {
	if _, ok := s.store.FindInvitationByID(invitationID); !ok {
		return nil, ErrNotFound
	}
	if guestID != "" {
		guest, ok := s.store.FindGuestByID(guestID)
		if !ok || guest.InvitationID != invitationID {
			return nil, ErrNotFound
		}
	}
	amount = math.Round(amount)
	sender = strings.TrimSpace(sender)
	if amount < MinAmount || amount > MaxAmount || sender == "" || len(sender) > 80 || len(message) > 1000 {
		return nil, ErrInvalid
	}
	if s.gateway == nil {
		return nil, ErrUnavailable
	}
	title := strings.TrimSpace(options.Title)
	if title == "" {
		title = "undangan"
	}
	ctx, cancel := context.WithTimeout(context.Background(), 25*time.Second)
	defer cancel()
	payment, err := s.gateway.Create(ctx, payments.Request{
		Amount:      amount,
		Name:        "Amplop untuk " + title,
		Description: "Amplop digital dari " + sender,
		Email:       options.Email,
		RedirectURL: options.RedirectURL,
		ExpiresAt:   time.Now().UTC().Add(24 * time.Hour),
		Extra:       map[string]string{"invitation_id": invitationID, "kind": "gift"},
	})
	if err != nil {
		return nil, fmt.Errorf("create payment: %w", err)
	}
	tx, err := s.store.CreateGiftTransaction(store.GiftTransaction{InvitationID: invitationID, GuestID: guestID, Gateway: s.gateway.Name(), GatewayReference: payment.Reference, Amount: amount, Status: "pending", SenderName: sender, Message: strings.TrimSpace(message)})
	if err != nil {
		return nil, err
	}
	tx.PaymentURL = payment.CheckoutURL
	return tx, nil
}

func (s *Service) List(ownerID, invitationID string) ([]*store.GiftTransaction, error) {
	inv, ok := s.store.FindInvitationByID(invitationID)
	if !ok || inv.UserID != ownerID {
		return nil, ErrNotFound
	}
	return s.store.ListGiftTransactions(invitationID), nil
}

// Moderate lets the couple record manual gifts. Online envelopes are only ever confirmed by the gateway,
// otherwise a couple could mark one paid and withdraw money Rawuh never received.
func (s *Service) Moderate(ownerID, invitationID, id, status, reference string) (*store.GiftTransaction, error) {
	if status != "pending" && status != "confirmed" && status != "failed" && status != "refunded" {
		return nil, ErrInvalid
	}
	items, err := s.List(ownerID, invitationID)
	if err != nil {
		return nil, err
	}
	var found *store.GiftTransaction
	for _, item := range items {
		if item.ID == id {
			found = item
			break
		}
	}
	if found == nil {
		return nil, ErrNotFound
	}
	if online(found) {
		return nil, fmt.Errorf("%w: online envelopes are confirmed by the payment gateway", ErrInvalid)
	}
	tx, err := s.store.UpdateGiftTransactionStatus(id, status, reference)
	if err != nil {
		return nil, ErrNotFound
	}
	if tx.InvitationID != invitationID {
		return nil, ErrNotFound
	}
	return tx, nil
}

// ConfirmPaid marks an envelope confirmed only after the gateway reports it paid.
func (s *Service) ConfirmPaid(ctx context.Context, reference string) (*store.GiftTransaction, error) {
	tx, ok := s.store.FindGiftTransactionByReference(reference)
	if !ok || !online(tx) {
		return nil, ErrNotFound
	}
	if tx.Status == "confirmed" {
		return tx, nil
	}
	if tx.Status != "pending" || s.gateway == nil || tx.Gateway != s.gateway.Name() {
		return nil, ErrNotFound
	}
	status, err := s.gateway.Status(ctx, reference)
	if err != nil {
		return nil, err
	}
	s.mu.Lock()
	defer s.mu.Unlock()
	switch status {
	case payments.StatusPaid:
		return s.store.UpdateGiftTransactionStatus(tx.ID, "confirmed", reference)
	case payments.StatusClosed:
		_, _ = s.store.UpdateGiftTransactionStatus(tx.ID, "failed", reference)
	}
	return nil, ErrNotPaid
}

// VerifyPending re-checks every pending online envelope of an invitation (webhook fallback).
func (s *Service) VerifyPending(ctx context.Context, invitationID string) int {
	confirmed := 0
	for _, tx := range s.store.ListGiftTransactions(invitationID) {
		if tx.Status != "pending" || !online(tx) || tx.GatewayReference == "" || time.Since(tx.CreatedAt) > 7*24*time.Hour {
			continue
		}
		if _, err := s.ConfirmPaid(ctx, tx.GatewayReference); err == nil {
			confirmed++
		} else if !errors.Is(err, ErrNotPaid) && !errors.Is(err, payments.ErrStatusUnsupported) {
			log.Printf("gifts: verify %s: %v", tx.GatewayReference, err)
		}
	}
	return confirmed
}

// ConfirmDummy is the simulated checkout's "I paid" button; only works while the dummy gateway is active.
func (s *Service) ConfirmDummy(reference string) (*store.GiftTransaction, error) {
	if s.Provider() != "dummy" {
		return nil, ErrNotFound
	}
	tx, ok := s.store.FindGiftTransactionByReference(reference)
	if !ok || tx.Gateway != "dummy" {
		return nil, ErrNotFound
	}
	return s.store.UpdateGiftTransactionStatus(tx.ID, "confirmed", reference)
}

// Wallet summarises online envelopes held by Rawuh for one invitation.
type Wallet struct {
	FeePercent float64 `json:"fee_percent"`
	Count      int     `json:"count"`
	Received   float64 `json:"received"`  // gross paid by guests
	Fee        float64 `json:"fee"`       // Rawuh's service fee
	Net        float64 `json:"net"`       // received - fee
	PaidOut    float64 `json:"paid_out"`  // payouts already transferred
	Requested  float64 `json:"requested"` // payouts waiting to be processed
	Available  float64 `json:"available"` // net - paid_out - requested
}

func (s *Service) Wallet(invitationID string, feePercent float64) Wallet {
	w := Wallet{FeePercent: feePercent}
	for _, tx := range s.store.ListGiftTransactions(invitationID) {
		if online(tx) && tx.Status == "confirmed" {
			w.Count++
			w.Received += tx.Amount
		}
	}
	w.Fee = math.Round(w.Received * feePercent / 100)
	w.Net = w.Received - w.Fee
	for _, p := range s.store.ListGiftPayouts(invitationID) {
		switch p.Status {
		case "paid":
			w.PaidOut += p.Amount
		case "requested":
			w.Requested += p.Amount
		}
	}
	w.Available = math.Max(0, w.Net-w.PaidOut-w.Requested)
	return w
}

type PayoutRequest struct {
	Amount        float64
	BankName      string
	AccountNumber string
	AccountName   string
}

func (s *Service) RequestPayout(ownerID, invitationID string, request PayoutRequest, feePercent, minPayout float64) (*store.GiftPayout, error) {
	inv, ok := s.store.FindInvitationByID(invitationID)
	if !ok || inv.UserID != ownerID {
		return nil, ErrNotFound
	}
	request.Amount = math.Floor(request.Amount)
	request.BankName = strings.TrimSpace(request.BankName)
	request.AccountNumber = strings.TrimSpace(request.AccountNumber)
	request.AccountName = strings.TrimSpace(request.AccountName)
	if request.Amount <= 0 || request.Amount < minPayout || request.BankName == "" || request.AccountName == "" ||
		len(request.AccountNumber) < 5 || len(request.AccountNumber) > 30 || len(request.BankName) > 60 || len(request.AccountName) > 80 {
		return nil, ErrInvalid
	}
	s.mu.Lock()
	defer s.mu.Unlock()
	if request.Amount > s.Wallet(invitationID, feePercent).Available {
		return nil, ErrBalance
	}
	return s.store.CreateGiftPayout(store.GiftPayout{
		InvitationID: invitationID, UserID: ownerID, Amount: request.Amount,
		BankName: request.BankName, AccountNumber: request.AccountNumber, AccountName: request.AccountName, Status: "requested",
	})
}

// ProcessPayout is the admin step after transferring (paid) or declining (rejected) a request.
func (s *Service) ProcessPayout(id, status, note string) (*store.GiftPayout, error) {
	if status != "paid" && status != "rejected" {
		return nil, ErrInvalid
	}
	s.mu.Lock()
	defer s.mu.Unlock()
	payout, ok := s.store.FindGiftPayout(id)
	if !ok {
		return nil, ErrNotFound
	}
	if payout.Status != "requested" {
		return nil, fmt.Errorf("%w: payout already %s", ErrInvalid, payout.Status)
	}
	return s.store.UpdateGiftPayout(id, status, strings.TrimSpace(note))
}
