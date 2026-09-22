package gifts

import (
	"context"
	"errors"
	"fmt"
	"strings"
	"yukakad/internal/payments"
	"yukakad/internal/store"
)

var (
	ErrNotFound = errors.New("gift transaction not found")
	ErrInvalid  = errors.New("invalid gift transaction")
)

type Service struct {
	store   store.Store
	gateway payments.Gateway
}

func NewService(dataStore store.Store, gateway payments.Gateway) *Service {
	return &Service{store: dataStore, gateway: gateway}
}

func (s *Service) Create(invitationID, guestID, gateway, sender, message string, amount float64) (*store.GiftTransaction, error) {
	if _, ok := s.store.FindInvitationByID(invitationID); !ok {
		return nil, ErrNotFound
	}
	if guestID != "" {
		guest, ok := s.store.FindGuestByID(guestID)
		if !ok || guest.InvitationID != invitationID {
			return nil, ErrNotFound
		}
	}
	if amount <= 0 || amount > 1000000000 || strings.TrimSpace(sender) == "" || len(message) > 1000 {
		return nil, ErrInvalid
	}
	if gateway == "" {
		gateway = "dummy"
	}
	if gateway != "dummy" || s.gateway == nil {
		return nil, fmt.Errorf("%w: unsupported gateway", ErrInvalid)
	}
	payment, err := s.gateway.Create(context.Background(), amount)
	if err != nil {
		return nil, fmt.Errorf("create payment: %w", err)
	}
	tx, err := s.store.CreateGiftTransaction(store.GiftTransaction{InvitationID: invitationID, GuestID: guestID, Gateway: gateway, GatewayReference: payment.Reference, Amount: amount, Status: "pending", SenderName: strings.TrimSpace(sender), Message: strings.TrimSpace(message)})
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

func (s *Service) Moderate(ownerID, invitationID, id, status, reference string) (*store.GiftTransaction, error) {
	if status != "pending" && status != "confirmed" && status != "failed" && status != "refunded" {
		return nil, ErrInvalid
	}
	items, err := s.List(ownerID, invitationID)
	if err != nil {
		return nil, err
	}
	found := false
	for _, item := range items {
		if item.ID == id {
			found = true
			break
		}
	}
	if !found {
		return nil, ErrNotFound
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

func (s *Service) ConfirmDummy(reference string) (*store.GiftTransaction, error) {
	tx, ok := s.store.FindGiftTransactionByReference(reference)
	if !ok || tx.Gateway != "dummy" {
		return nil, ErrNotFound
	}
	return s.store.UpdateGiftTransactionStatus(tx.ID, "confirmed", reference)
}
