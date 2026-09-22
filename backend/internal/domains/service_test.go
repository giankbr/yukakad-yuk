package domains

import (
	"errors"
	"testing"
	"yukakad/internal/billing"
	"yukakad/internal/payments"
	"yukakad/internal/store"
)

func TestCustomDomainRequiresPlanAndVerifies(t *testing.T) {
	data := store.NewMemoryStore()
	data.SeedPlans()
	user, _ := data.CreateUser("A", "a@example.com", "hash")
	inv, _ := data.CreateInvitation(user.ID, "demo", "Demo")
	b := billing.NewService(data, payments.Dummy{BaseURL: "http://localhost"})
	service := NewService(data, b)
	if _, err := service.Create(user.ID, inv.ID, "invite.example.com"); !errors.Is(err, ErrNotAllowed) {
		t.Fatalf("expected denial, got %v", err)
	}
	_ = data.SetUserPlan(user.ID, "premium")
	domain, err := service.Create(user.ID, inv.ID, "invite.example.com")
	if err != nil {
		t.Fatal(err)
	}
	verified, err := service.Verify(user.ID, domain.ID, domain.VerificationToken)
	if err != nil || verified.Status != "verified" {
		t.Fatalf("verify failed: %v", err)
	}
}
