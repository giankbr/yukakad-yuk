package templates

import (
	"errors"
	"testing"
	"yukakad/internal/store"
)

func TestAssignPremiumTemplateRequiresEntitlement(t *testing.T) {
	dataStore := store.NewMemoryStore()
	dataStore.SeedTemplates()
	dataStore.SeedPlans()
	user, err := dataStore.CreateUser("A", "a@example.com", "hash")
	if err != nil {
		t.Fatal(err)
	}
	invitation, err := dataStore.CreateInvitation(user.ID, "demo", "Demo")
	if err != nil {
		t.Fatal(err)
	}
	service := NewService(dataStore)
	if err := service.Assign(user.ID, invitation.ID, "aksara"); !errors.Is(err, ErrPremiumDenied) {
		t.Fatalf("expected premium denial, got %v", err)
	}
	if err := dataStore.SetUserPlan(user.ID, "pro"); err != nil {
		t.Fatal(err)
	}
	if err := service.Assign(user.ID, invitation.ID, "aksara"); err != nil {
		t.Fatal(err)
	}
}

func TestAssignHidesForeignInvitation(t *testing.T) {
	dataStore := store.NewMemoryStore()
	dataStore.SeedTemplates()
	dataStore.SeedPlans()
	owner, _ := dataStore.CreateUser("Owner", "owner@example.com", "hash")
	other, _ := dataStore.CreateUser("Other", "other@example.com", "hash")
	invitation, _ := dataStore.CreateInvitation(owner.ID, "demo", "Demo")
	if err := NewService(dataStore).Assign(other.ID, invitation.ID, "classic"); !errors.Is(err, ErrNotFound) {
		t.Fatal(err)
	}
}
