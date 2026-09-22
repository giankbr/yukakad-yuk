package invitations

import (
	"errors"
	"fmt"
	"regexp"
	"strings"

	"yukakad/internal/store"
)

var (
	ErrNotFound = errors.New("invitation not found")
	ErrInvalid  = errors.New("invalid invitation")
)

var slugPattern = regexp.MustCompile(`^[a-z0-9]+(?:-[a-z0-9]+)*$`)

type Service struct{ store store.Store }

func NewService(dataStore store.Store) *Service { return &Service{store: dataStore} }

func (s *Service) Create(ownerID, slug, title string) (*store.Invitation, error) {
	slug = strings.ToLower(strings.TrimSpace(slug))
	title = strings.TrimSpace(title)
	if !slugPattern.MatchString(slug) || len(slug) > 80 || title == "" || len(title) > 160 {
		return nil, ErrInvalid
	}
	return s.store.CreateInvitation(ownerID, slug, title)
}

func (s *Service) Owned(ownerID, id string) (*store.Invitation, error) {
	invitation, ok := s.store.FindInvitationByID(id)
	if !ok || invitation.UserID != ownerID {
		return nil, ErrNotFound
	}
	return invitation, nil
}

func (s *Service) Update(ownerID, id, slug, title string, published bool, couple store.Couple, event store.Event) (*store.Invitation, error) {
	current, err := s.Owned(ownerID, id)
	if err != nil {
		return nil, err
	}
	slug = strings.ToLower(strings.TrimSpace(slug))
	title = strings.TrimSpace(title)
	if slug == "" {
		slug = current.Slug
	}
	if title == "" {
		title = current.Title
	}
	if !slugPattern.MatchString(slug) || len(slug) > 80 || len(title) > 160 {
		return nil, ErrInvalid
	}
	return s.store.UpdateInvitation(id, slug, title, published, couple, event)
}

func (s *Service) Delete(ownerID, id string) error {
	if _, err := s.Owned(ownerID, id); err != nil {
		return err
	}
	if err := s.store.DeleteInvitation(id); err != nil {
		return fmt.Errorf("delete invitation: %w", err)
	}
	return nil
}

func (s *Service) Duplicate(ownerID, sourceID, slug, title string) (*store.Invitation, error) {
	source, err := s.Owned(ownerID, sourceID)
	if err != nil {
		return nil, err
	}
	slug = strings.ToLower(strings.TrimSpace(slug))
	title = strings.TrimSpace(title)
	if slug == "" {
		slug = source.Slug + "-copy"
	}
	if title == "" {
		title = "Copy of " + source.Title
	}
	if !slugPattern.MatchString(slug) || len(slug) > 80 || len(title) > 160 {
		return nil, ErrInvalid
	}
	return s.store.DuplicateInvitation(sourceID, slug, title, ownerID)
}
