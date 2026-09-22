package guests

import (
	"errors"
	"fmt"
	"strings"

	"yukakad/internal/store"
)

var (
	ErrNotFound        = errors.New("guest not found")
	ErrInvalid         = errors.New("invalid guest")
	ErrQuotaExceeded   = errors.New("guest limit reached for your plan")
	ErrPlanUnavailable = errors.New("plan unavailable")
)

type Service struct{ store store.Store }

func NewService(dataStore store.Store) *Service { return &Service{store: dataStore} }

func (s *Service) ensureOwner(ownerID, invitationID string) error {
	invitation, ok := s.store.FindInvitationByID(invitationID)
	if !ok || invitation.UserID != ownerID {
		return ErrNotFound
	}
	return nil
}

func validate(name, phone, category string) (string, string, string, error) {
	name = strings.TrimSpace(name)
	phone = strings.TrimSpace(phone)
	category = strings.TrimSpace(category)
	if name == "" || len(name) > 160 || len(phone) > 32 || len(category) > 40 {
		return "", "", "", ErrInvalid
	}
	if category == "" {
		category = "family"
	}
	return name, phone, category, nil
}

func (s *Service) List(ownerID, invitationID, search, category string) ([]*store.Guest, error) {
	if err := s.ensureOwner(ownerID, invitationID); err != nil {
		return nil, err
	}
	if strings.TrimSpace(search) != "" || strings.TrimSpace(category) != "" {
		return s.store.ListGuestsFiltered(invitationID, strings.TrimSpace(search), strings.TrimSpace(category)), nil
	}
	return s.store.ListGuests(invitationID), nil
}

func (s *Service) Create(ownerID, invitationID, name, phone, category string) (*store.Guest, error) {
	if err := s.ensureOwner(ownerID, invitationID); err != nil {
		return nil, err
	}
	name, phone, category, err := validate(name, phone, category)
	if err != nil {
		return nil, err
	}
	plan, err := s.store.GetUserPlan(ownerID)
	if err != nil {
		return nil, fmt.Errorf("%w: %v", ErrPlanUnavailable, err)
	}
	if plan.MaxGuests > 0 && len(s.store.ListGuests(invitationID)) >= plan.MaxGuests {
		return nil, ErrQuotaExceeded
	}
	return s.store.CreateGuest(invitationID, name, phone, category)
}

func (s *Service) Update(ownerID, invitationID, guestID, name, phone, category string) (*store.Guest, error) {
	if err := s.ensureOwner(ownerID, invitationID); err != nil {
		return nil, err
	}
	guest, ok := s.store.FindGuestByID(guestID)
	if !ok || guest.InvitationID != invitationID {
		return nil, ErrNotFound
	}
	name, phone, category, err := validate(name, phone, category)
	if err != nil {
		return nil, err
	}
	return s.store.UpdateGuest(guestID, name, phone, category)
}

func (s *Service) Delete(ownerID, invitationID, guestID string) error {
	if err := s.ensureOwner(ownerID, invitationID); err != nil {
		return err
	}
	guest, ok := s.store.FindGuestByID(guestID)
	if !ok || guest.InvitationID != invitationID {
		return ErrNotFound
	}
	if err := s.store.DeleteGuest(guestID); err != nil {
		return fmt.Errorf("delete guest: %w", err)
	}
	return nil
}

func (s *Service) CheckIn(ownerID, invitationID, guestID string) (*store.Guest, error) {
	if err := s.ensureOwner(ownerID, invitationID); err != nil {
		return nil, err
	}
	guest, ok := s.store.FindGuestByID(guestID)
	if !ok || guest.InvitationID != invitationID {
		return nil, ErrNotFound
	}
	return s.store.CheckInGuest(guestID, ownerID)
}

func (s *Service) BulkDelete(ownerID, invitationID string, ids []string) error {
	if err := s.ensureOwner(ownerID, invitationID); err != nil {
		return err
	}
	if len(ids) == 0 {
		return ErrInvalid
	}
	for _, id := range ids {
		guest, ok := s.store.FindGuestByID(id)
		if !ok || guest.InvitationID != invitationID {
			return ErrNotFound
		}
	}
	return s.store.BulkDeleteGuests(invitationID, ids)
}
