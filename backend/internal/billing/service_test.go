package billing

import (
	"errors"
	"testing"
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
