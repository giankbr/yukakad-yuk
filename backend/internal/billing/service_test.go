package billing

import (
	"errors"
	"testing"
	"time"
	"yukakad/internal/payments"
	"yukakad/internal/store"
)

func TestChangePlanValidatesCatalog(t *testing.T) {
	data := store.NewMemoryStore()
	data.SeedPlans()
	user, err := data.CreateUser("A", "a@example.com", "hash")
	if err != nil {
		t.Fatal(err)
	}
	service := NewService(data, payments.Dummy{BaseURL: "http://localhost"})
	if _, err := service.ChangePlan(user.ID, "unknown"); !errors.Is(err, ErrPlanNotFound) {
		t.Fatalf("expected plan error, got %v", err)
	}
	plan, err := service.ChangePlan(user.ID, "pro")
	if err != nil || plan.ID != "pro" {
		t.Fatalf("change plan failed: %v", err)
	}
}

func TestCheckoutConfirmCreatesInvoice(t *testing.T) {
	data := store.NewMemoryStore()
	data.SeedPlans()
	user, err := data.CreateUser("A", "billing@example.com", "hash")
	if err != nil {
		t.Fatal(err)
	}
	service := NewService(data, payments.Dummy{BaseURL: "http://localhost"})
	sub, _, err := service.Checkout(user.ID, "pro")
	if err != nil {
		t.Fatal(err)
	}
	if sub.Status != "pending" || sub.EndsAt == nil {
		t.Fatalf("invalid pending subscription: %+v", sub)
	}
	confirmed, err := service.Confirm(sub.ProviderReference)
	if err != nil || confirmed.Status != "active" {
		t.Fatalf("confirm failed: %v", err)
	}
	plan, err := data.GetUserPlan(user.ID)
	if err != nil || plan.ID != "pro" {
		t.Fatalf("plan was not activated: %v", err)
	}
	invoices := data.ListInvoices(user.ID)
	if len(invoices) != 1 || invoices[0].Status != "paid" {
		t.Fatalf("invoice missing: %+v", invoices)
	}
}

func TestGrantPlanRecordsManualSubscription(t *testing.T) {
	data := store.NewMemoryStore()
	data.SeedPlans()
	user, _ := data.CreateUser("A", "grant@example.com", "hash")
	service := NewService(data, nil)
	sub, err := service.GrantPlan(user.ID, "pro")
	if err != nil || sub == nil {
		t.Fatalf("grant: %v", err)
	}
	if sub.Status != "active" || sub.Provider != "manual" || sub.EndsAt == nil || sub.EndsAt.Sub(time.Now()) < 29*24*time.Hour {
		t.Fatalf("unexpected subscription %+v", sub)
	}
	if plan, _ := data.GetUserPlan(user.ID); plan.ID != "pro" {
		t.Fatalf("plan = %s", plan.ID)
	}
	if _, err := service.GrantPlan(user.ID, "free"); err != nil {
		t.Fatal(err)
	}
	for _, s := range data.ListSubscriptions(user.ID) {
		if s.Status == "active" {
			t.Fatal("downgrading to free must end the manual subscription")
		}
	}
}

func TestConfirmStartsPeriodAtPayment(t *testing.T) {
	data := store.NewMemoryStore()
	data.SeedPlans()
	user, _ := data.CreateUser("A", "period@example.com", "hash")
	service := NewService(data, payments.Dummy{BaseURL: "http://localhost"})
	sub, _, err := service.Checkout(user.ID, "pro")
	if err != nil {
		t.Fatal(err)
	}
	early := time.Now().UTC().Add(-48 * time.Hour)
	sub.EndsAt = &early // simulate a stale end date computed at checkout
	confirmed, err := service.Confirm(sub.ProviderReference)
	if err != nil {
		t.Fatal(err)
	}
	if confirmed.EndsAt == nil || confirmed.EndsAt.Sub(time.Now()) < 29*24*time.Hour {
		t.Fatalf("period should run from confirmation, got %v", confirmed.EndsAt)
	}
}
