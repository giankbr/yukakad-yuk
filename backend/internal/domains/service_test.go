package domains

import (
	"context"
	"errors"
	"testing"

	"yukakad/internal/billing"
	"yukakad/internal/payments"
	"yukakad/internal/store"
)

type fakeDNS struct {
	txt   map[string][]string
	cname map[string]string
	hosts map[string][]string
}

func (f *fakeDNS) LookupTXT(_ context.Context, name string) ([]string, error) {
	if v, ok := f.txt[name]; ok {
		return v, nil
	}
	return nil, errors.New("no such host")
}

func (f *fakeDNS) LookupCNAME(_ context.Context, host string) (string, error) {
	if v, ok := f.cname[host]; ok {
		return v, nil
	}
	return host + ".", nil
}

func (f *fakeDNS) LookupHost(_ context.Context, host string) ([]string, error) {
	return f.hosts[host], nil
}

func TestCustomDomainRequiresPlanAndDNSProof(t *testing.T) {
	data := store.NewMemoryStore()
	data.SeedPlans()
	user, _ := data.CreateUser("A", "a@example.com", "hash")
	other, _ := data.CreateUser("B", "b@example.com", "hash")
	inv, _ := data.CreateInvitation(user.ID, "demo", "Demo")
	b := billing.NewService(data, payments.Dummy{BaseURL: "http://localhost"})
	dns := &fakeDNS{txt: map[string][]string{}, cname: map[string]string{}, hosts: map[string][]string{"domains.rawuh.id": {"203.0.113.7"}}}
	service := NewService(data, b).WithResolver(dns)

	if _, err := service.Create(user.ID, inv.ID, "invite.example.com"); !errors.Is(err, ErrNotAllowed) {
		t.Fatalf("expected plan denial, got %v", err)
	}
	_ = data.SetUserPlan(user.ID, "premium")
	if _, err := service.Create(user.ID, inv.ID, "rawuh.id"); !errors.Is(err, ErrReserved) {
		t.Fatalf("own domain must be reserved, got %v", err)
	}
	domain, err := service.Create(user.ID, inv.ID, "https://Invite.Example.com/")
	if err != nil || domain.Domain != "invite.example.com" {
		t.Fatalf("create: %v %+v", err, domain)
	}
	if _, err := service.Create(user.ID, inv.ID, "invite.example.com"); !errors.Is(err, ErrTaken) {
		t.Fatalf("duplicate should be taken, got %v", err)
	}

	// Knowing the token is not enough: the TXT record must exist.
	item, check, err := service.Verify(context.Background(), user.ID, inv.ID, domain.ID)
	if err != nil || item.Status == "verified" || check.Ownership {
		t.Fatalf("verify without DNS should stay pending: %v %+v %+v", err, item, check)
	}
	dns.txt[TXTName("invite.example.com")] = []string{TXTValue(domain.VerificationToken)}
	dns.cname["invite.example.com"] = "domains.rawuh.id."
	item, check, err = service.Verify(context.Background(), user.ID, inv.ID, domain.ID)
	if err != nil || item.Status != "verified" || !check.Ownership || !check.Routing {
		t.Fatalf("verify with DNS: %v %+v %+v", err, item, check)
	}
	if _, _, err := service.Verify(context.Background(), other.ID, inv.ID, domain.ID); !errors.Is(err, ErrNotFound) {
		t.Fatalf("other user must not verify, got %v", err)
	}

	// Apex domain whose A record matches the target's address.
	apex, err := service.Create(user.ID, inv.ID, "example.org")
	if err != nil {
		t.Fatal(err)
	}
	dns.txt[TXTName("example.org")] = []string{TXTValue(apex.VerificationToken)}
	dns.hosts["example.org"] = []string{"203.0.113.7"}
	if _, check, _ := service.Verify(context.Background(), user.ID, inv.ID, apex.ID); !check.Routing {
		t.Fatal("apex A record should count as routing")
	}
	if err := service.Delete(user.ID, inv.ID, apex.ID); err != nil {
		t.Fatal(err)
	}
	if n := len(data.ListCustomDomains(inv.ID)); n != 1 {
		t.Fatalf("expected 1 domain after delete, got %d", n)
	}
}
