package rsvp

import (
	"errors"
	"strings"
	"yukakad/internal/store"
)

var (
	ErrInvalid  = errors.New("invalid RSVP")
	ErrNotFound = errors.New("guest not found")
)

type Service struct{ store store.Store }

func NewService(dataStore store.Store) *Service { return &Service{store: dataStore} }

func (s *Service) Submit(invitationID, guestID, guestToken, attendance string, attendees int, message string) (*store.RSVP, error) {
	if (attendance != "yes" && attendance != "no" && attendance != "maybe") || attendees < 0 || attendees > 10 || len(message) > 1000 {
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
	if attendance == "no" {
		attendees = 0
	}
	return s.store.UpsertRSVP(invitationID, guestID, attendance, attendees, strings.TrimSpace(message))
}

func (s *Service) List(ownerID, invitationID string) ([]*store.RSVP, error) {
	invitation, ok := s.store.FindInvitationByID(invitationID)
	if !ok || invitation.UserID != ownerID {
		return nil, ErrNotFound
	}
	return s.store.ListRSVPs(invitationID), nil
}

func (s *Service) Summary(ownerID, invitationID string) (map[string]int, error) {
	invitation, ok := s.store.FindInvitationByID(invitationID)
	if !ok || invitation.UserID != ownerID {
		return nil, ErrNotFound
	}
	return s.store.RSVPSummary(invitationID), nil
}
