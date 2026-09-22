package guests

import (
	"errors"
	"testing"
	"yukakad/internal/store"
)

func fixture(t *testing.T) (*Service, *store.MemoryStore, string) {
	t.Helper()
	data := store.NewMemoryStore()
	data.SeedPlans()
	if _, err := data.CreateUser("Test User", "user@example.com", "hash"); err != nil {
		t.Fatal(err)
	}
	inv, err := data.CreateInvitation("user-1", "alya-rizky", "Alya & Rizky")
	if err != nil {
		t.Fatal(err)
	}
	return NewService(data), data, inv.ID
}

func TestCreateEnforcesPlanQuota(t *testing.T) {
	service, dataStore, invitationID := fixture(t)
	user, ok := dataStore.FindInvitationByID(invitationID)
	if !ok {
		t.Fatal("invitation missing")
	}
	if err := dataStore.SetUserPlan(user.UserID, "free"); err != nil {
		t.Fatal(err)
	}
	for i := 0; i < 50; i++ {
		if _, err := service.Create(user.UserID, invitationID, "Guest", "", "family"); err != nil {
			t.Fatalf("guest %d: %v", i, err)
		}
	}
	if _, err := service.Create(user.UserID, invitationID, "Over limit", "", "family"); !errors.Is(err, ErrQuotaExceeded) {
		t.Fatalf("expected quota error, got %v", err)
	}
}

func TestGuestServiceEnforcesOwnershipAndValidation(t *testing.T) {
	svc, _, invitationID := fixture(t)
	if _, err := svc.Create("user-2", invitationID, "Budi", "0812", "friend"); !errors.Is(err, ErrNotFound) {
		t.Fatalf("expected hidden invitation, got %v", err)
	}
	if _, err := svc.Create("user-1", invitationID, "", "0812", "friend"); !errors.Is(err, ErrInvalid) {
		t.Fatalf("expected invalid guest, got %v", err)
	}
}

func TestGuestServiceCRUDAndCheckIn(t *testing.T) {
	svc, data, invitationID := fixture(t)
	guest, err := svc.Create("user-1", invitationID, "Budi", "0812", "friend")
	if err != nil {
		t.Fatal(err)
	}
	updated, err := svc.Update("user-1", invitationID, guest.ID, "Budi Updated", "0813", "vip")
	if err != nil || updated.Category != "vip" {
		t.Fatalf("update failed: %v", err)
	}
	checked, err := svc.CheckIn("user-1", invitationID, guest.ID)
	if err != nil || checked.CheckedInAt == nil {
		t.Fatalf("check-in failed: %v", err)
	}
	if err := svc.BulkDelete("user-1", invitationID, []string{guest.ID}); err != nil {
		t.Fatal(err)
	}
	if len(data.ListGuests(invitationID)) != 0 {
		t.Fatal("guest was not deleted")
	}
}
