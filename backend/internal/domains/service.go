package domains

import (
	"context"
	"crypto/rand"
	"encoding/hex"
	"errors"
	"fmt"
	"net"
	"regexp"
	"strings"
	"time"

	"yukakad/internal/billing"
	"yukakad/internal/store"
)

var (
	ErrNotFound   = errors.New("Domain tidak ditemukan")
	ErrInvalid    = errors.New("Nama domain tidak valid. Contoh: rinadanbima.com atau undangan.rinadanbima.com")
	ErrNotAllowed = errors.New("Domain sendiri tersedia di paket Premium")
	ErrTaken      = errors.New("Domain ini sudah dipakai undangan lain")
	ErrLimit      = errors.New("Maksimal 3 domain per undangan")
	ErrReserved   = errors.New("Domain ini tidak bisa dipakai")
)

const maxPerInvitation = 3

var domainPattern = regexp.MustCompile(`^(?i)([a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z]{2,63}$`)

// Resolver is the DNS lookups verification needs (net.DefaultResolver in production, a fake in tests).
type Resolver interface {
	LookupTXT(ctx context.Context, name string) ([]string, error)
	LookupCNAME(ctx context.Context, host string) (string, error)
	LookupHost(ctx context.Context, host string) ([]string, error)
}

type Service struct {
	store    store.Store
	billing  *billing.Service
	resolver Resolver
	// Target is the hostname custom domains must point to (CNAME), e.g. "domains.rawuh.id".
	Target string
	// Reserved hosts (Rawuh's own domains) can never be claimed.
	Reserved []string
}

func NewService(dataStore store.Store, billingService *billing.Service) *Service {
	return &Service{store: dataStore, billing: billingService, resolver: net.DefaultResolver, Target: "domains.rawuh.id", Reserved: []string{"rawuh.id"}}
}

// WithResolver swaps the DNS resolver (tests).
func (s *Service) WithResolver(resolver Resolver) *Service { s.resolver = resolver; return s }

// TXTName is the DNS record that proves ownership of a domain.
func TXTName(domain string) string { return "_rawuh." + domain }

// TXTValue is the value that record must contain.
func TXTValue(token string) string { return "rawuh-verify=" + token }

func (s *Service) owned(ownerID, invitationID string) error {
	inv, ok := s.store.FindInvitationByID(invitationID)
	if !ok || inv.UserID != ownerID {
		return ErrNotFound
	}
	return nil
}

func (s *Service) List(ownerID, invitationID string) ([]*store.CustomDomain, error) {
	if err := s.owned(ownerID, invitationID); err != nil {
		return nil, err
	}
	return s.store.ListCustomDomains(invitationID), nil
}

// Normalize lowercases a domain and strips a scheme, path, port and trailing dot people often paste.
func Normalize(domain string) string {
	domain = strings.ToLower(strings.TrimSpace(domain))
	domain = strings.TrimPrefix(strings.TrimPrefix(domain, "https://"), "http://")
	if i := strings.IndexAny(domain, "/?#"); i >= 0 {
		domain = domain[:i]
	}
	if host, _, err := net.SplitHostPort(domain); err == nil {
		domain = host
	}
	return strings.TrimSuffix(domain, ".")
}

func (s *Service) Create(ownerID, invitationID, domain string) (*store.CustomDomain, error) {
	if err := s.owned(ownerID, invitationID); err != nil {
		return nil, err
	}
	allowed, err := s.billing.Allows(ownerID, billing.FeatureCustomDomain)
	if err != nil {
		return nil, err
	}
	if !allowed {
		return nil, ErrNotAllowed
	}
	domain = Normalize(domain)
	if !domainPattern.MatchString(domain) || len(domain) > 253 {
		return nil, ErrInvalid
	}
	for _, reserved := range append([]string{s.Target}, s.Reserved...) {
		if reserved != "" && (domain == reserved || strings.HasSuffix(domain, "."+reserved)) {
			return nil, ErrReserved
		}
	}
	if len(s.store.ListCustomDomains(invitationID)) >= maxPerInvitation {
		return nil, ErrLimit
	}
	buf := make([]byte, 16)
	if _, err := rand.Read(buf); err != nil {
		return nil, fmt.Errorf("generate verification token: %w", err)
	}
	item, err := s.store.CreateCustomDomain(store.CustomDomain{UserID: ownerID, InvitationID: invitationID, Domain: domain, VerificationToken: hex.EncodeToString(buf)})
	if err != nil {
		return nil, ErrTaken // unique(domain)
	}
	return item, nil
}

// Check is the DNS state of one domain.
type Check struct {
	Ownership bool   `json:"ownership"` // TXT record found
	Routing   bool   `json:"routing"`   // CNAME/A records point at Rawuh
	Detail    string `json:"detail,omitempty"`
}

func (s *Service) find(ownerID, invitationID, domainID string) (*store.CustomDomain, error) {
	items, err := s.List(ownerID, invitationID)
	if err != nil {
		return nil, err
	}
	for _, item := range items {
		if item.ID == domainID {
			return item, nil
		}
	}
	return nil, ErrNotFound
}

// Inspect looks up the domain's DNS records.
func (s *Service) Inspect(ctx context.Context, item *store.CustomDomain) Check {
	ctx, cancel := context.WithTimeout(ctx, 8*time.Second)
	defer cancel()
	var check Check
	if records, err := s.resolver.LookupTXT(ctx, TXTName(item.Domain)); err == nil {
		for _, record := range records {
			if strings.TrimSpace(record) == TXTValue(item.VerificationToken) {
				check.Ownership = true
			}
		}
	}
	target := strings.TrimSuffix(strings.ToLower(s.Target), ".")
	if cname, err := s.resolver.LookupCNAME(ctx, item.Domain); err == nil && strings.TrimSuffix(strings.ToLower(cname), ".") == target {
		check.Routing = true
	} else if target != "" {
		// Apex domains can't CNAME: accept A/AAAA records that match the target's addresses.
		want, _ := s.resolver.LookupHost(ctx, target)
		got, _ := s.resolver.LookupHost(ctx, item.Domain)
		for _, a := range got {
			for _, b := range want {
				if a == b {
					check.Routing = true
				}
			}
		}
	}
	switch {
	case !check.Ownership:
		check.Detail = "Record TXT " + TXTName(item.Domain) + " belum ditemukan. Perubahan DNS bisa butuh beberapa menit sampai 24 jam."
	case !check.Routing:
		check.Detail = "Kepemilikan terverifikasi, tapi domain belum mengarah ke " + target + "."
	}
	return check
}

// Verify checks DNS and marks the domain verified once the ownership TXT record is in place.
func (s *Service) Verify(ctx context.Context, ownerID, invitationID, domainID string) (*store.CustomDomain, Check, error) {
	item, err := s.find(ownerID, invitationID, domainID)
	if err != nil {
		return nil, Check{}, err
	}
	check := s.Inspect(ctx, item)
	if !check.Ownership || item.Status == "verified" {
		return item, check, nil
	}
	verified, err := s.store.VerifyCustomDomain(item.ID, ownerID, item.VerificationToken)
	if err != nil {
		return nil, check, ErrNotFound
	}
	return verified, check, nil
}

func (s *Service) Delete(ownerID, invitationID, domainID string) error {
	if _, err := s.find(ownerID, invitationID, domainID); err != nil {
		return err
	}
	return s.store.DeleteCustomDomain(domainID, ownerID)
}
