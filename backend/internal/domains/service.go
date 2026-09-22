package domains

import (
	"crypto/rand"
	"encoding/hex"
	"errors"
	"fmt"
	"regexp"
	"strings"
	"yukakad/internal/billing"
	"yukakad/internal/store"
)

var (
	ErrNotFound   = errors.New("custom domain not found")
	ErrInvalid    = errors.New("invalid custom domain")
	ErrNotAllowed = errors.New("custom domain requires an eligible plan")
)

var domainPattern = regexp.MustCompile(`^(?i)([a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z]{2,63}$`)

type Service struct {
	store   store.Store
	billing *billing.Service
}

func NewService(dataStore store.Store, billingService *billing.Service) *Service {
	return &Service{store: dataStore, billing: billingService}
}

func (s *Service) List(ownerID, invitationID string) ([]*store.CustomDomain, error) {
	inv, ok := s.store.FindInvitationByID(invitationID)
	if !ok || inv.UserID != ownerID {
		return nil, ErrNotFound
	}
	return s.store.ListCustomDomains(invitationID), nil
}

func (s *Service) Create(ownerID, invitationID, domain string) (*store.CustomDomain, error) {
	inv, ok := s.store.FindInvitationByID(invitationID)
	if !ok || inv.UserID != ownerID {
		return nil, ErrNotFound
	}
	allowed, err := s.billing.Allows(ownerID, billing.FeatureCustomDomain)
	if err != nil {
		return nil, err
	}
	if !allowed {
		return nil, ErrNotAllowed
	}
	domain = strings.ToLower(strings.TrimSpace(domain))
	if !domainPattern.MatchString(domain) || len(domain) > 253 {
		return nil, ErrInvalid
	}
	buf := make([]byte, 24)
	if _, err := rand.Read(buf); err != nil {
		return nil, fmt.Errorf("generate verification token: %w", err)
	}
	return s.store.CreateCustomDomain(store.CustomDomain{UserID: ownerID, InvitationID: invitationID, Domain: domain, VerificationToken: hex.EncodeToString(buf)})
}

func (s *Service) Verify(ownerID, domainID, token string) (*store.CustomDomain, error) {
	if strings.TrimSpace(token) == "" {
		return nil, ErrInvalid
	}
	item, err := s.store.VerifyCustomDomain(domainID, ownerID, strings.TrimSpace(token))
	if err != nil {
		return nil, ErrNotFound
	}
	return item, nil
}
