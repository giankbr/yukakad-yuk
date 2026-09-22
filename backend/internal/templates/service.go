package templates

import (
	"errors"
	"fmt"
	"regexp"
	"strings"
	"yukakad/internal/store"
)

var (
	ErrNotFound      = errors.New("template or invitation not found")
	ErrPremiumDenied = errors.New("premium template requires an eligible plan")
	ErrInvalid       = errors.New("invalid template")
)

type Service struct{ store store.Store }

var slugPattern = regexp.MustCompile(`^[a-z0-9]+(?:-[a-z0-9]+)*$`)

func NewService(dataStore store.Store) *Service { return &Service{store: dataStore} }

func (s *Service) List() []*store.Template      { return s.store.ListTemplates() }
func (s *Service) ListAdmin() []*store.Template { return s.store.ListTemplatesAdmin() }

func validateTemplate(item store.Template) error {
	item.Name = strings.TrimSpace(item.Name)
	item.Slug = strings.TrimSpace(item.Slug)
	if item.Name == "" || len(item.Name) > 160 || !slugPattern.MatchString(item.Slug) || len(item.Slug) > 80 {
		return ErrInvalid
	}
	if item.Tier != "free" && item.Tier != "premium" && item.Tier != "signature" {
		return ErrInvalid
	}
	if item.Status != "draft" && item.Status != "active" && item.Status != "archived" {
		return ErrInvalid
	}
	if item.Price < 0 {
		return ErrInvalid
	}
	return nil
}

func (s *Service) Create(item store.Template) (*store.Template, error) {
	if err := validateTemplate(item); err != nil {
		return nil, err
	}
	return s.store.CreateTemplate(item)
}
func (s *Service) Update(item store.Template) (*store.Template, error) {
	if err := validateTemplate(item); err != nil {
		return nil, err
	}
	return s.store.UpdateTemplate(item)
}
func (s *Service) Delete(id string) error { return s.store.DeleteTemplate(id) }

func (s *Service) Assign(ownerID, invitationID, templateID string) error {
	invitation, ok := s.store.FindInvitationByID(invitationID)
	if !ok || invitation.UserID != ownerID {
		return ErrNotFound
	}

	var selected *store.Template
	for _, item := range s.store.ListTemplates() {
		if item.ID == templateID {
			selected = item
			break
		}
	}
	if selected == nil {
		return ErrNotFound
	}
	if selected.Premium {
		plan, err := s.store.GetUserPlan(ownerID)
		if err != nil {
			return fmt.Errorf("load plan: %w", err)
		}
		if !plan.PremiumTemplatesAllowed {
			return ErrPremiumDenied
		}
	}
	return s.store.AssignTemplate(invitationID, selected.ID)
}
