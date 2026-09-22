package wishes

import (
	"errors"
	"strings"
	"yukakad/internal/store"
)

var (
	ErrInvalid  = errors.New("invalid wish")
	ErrNotFound = errors.New("wish not found")
)

type Service struct{ store store.Store }

func NewService(dataStore store.Store) *Service { return &Service{store: dataStore} }

func (s *Service) Create(invitationID, guestID, guestToken, name, message string) (*store.Wish, error) {
	name, message = strings.TrimSpace(name), strings.TrimSpace(message)
	if name == "" || len(name) > 120 || message == "" || len(message) > 1000 {
		return nil, ErrInvalid
	}
	if guestToken != "" {
		guest, ok := s.store.FindGuestByToken(invitationID, guestToken)
		if !ok {
			return nil, ErrNotFound
		}
		guestID = guest.ID
	}
	if guestID != "" {
		guest, ok := s.store.FindGuestByID(guestID)
		if !ok || guest.InvitationID != invitationID {
			return nil, ErrNotFound
		}
	}
	return s.store.CreateWish(invitationID, guestID, name, message)
}

func (s *Service) Published(invitationID string) []*store.Wish {
	return s.store.ListPublishedWishes(invitationID)
}

func (s *Service) List(ownerID, invitationID string) ([]*store.Wish, error) {
	invitation, ok := s.store.FindInvitationByID(invitationID)
	if !ok || invitation.UserID != ownerID {
		return nil, ErrNotFound
	}
	return s.store.ListWishes(invitationID), nil
}

func (s *Service) Moderate(ownerID, invitationID, wishID, status string) (*store.Wish, error) {
	if status != "pending" && status != "published" && status != "rejected" {
		return nil, ErrInvalid
	}
	items, err := s.List(ownerID, invitationID)
	if err != nil {
		return nil, err
	}
	for _, item := range items {
		if item.ID == wishID {
			return s.store.UpdateWishStatus(wishID, status)
		}
	}
	return nil, ErrNotFound
}
