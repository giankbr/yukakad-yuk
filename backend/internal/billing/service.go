package billing

import (
	"context"
	"errors"
	"time"
	"yukakad/internal/payments"
	"yukakad/internal/store"
)

var (
	ErrPlanNotFound = errors.New("plan not found")
	ErrUserNotFound = errors.New("user not found")
)

const (
	FeaturePremiumTemplates = "premium_templates"
	FeatureCustomDomain     = "custom_domain"
	FeaturePaymentGateway   = "payment_gateway"
)

type Service struct {
	store   store.Store
	gateway payments.Gateway
}

func NewService(dataStore store.Store, gateway payments.Gateway) *Service {
	return &Service{store: dataStore, gateway: gateway}
}

func (s *Service) Current(userID string) (*store.Plan, error) {
	if _, ok := s.store.FindUserByID(userID); !ok {
		return nil, ErrUserNotFound
	}
	return s.store.GetUserPlan(userID)
}

func (s *Service) History(userID string) ([]*store.Subscription, error) {
	if _, ok := s.store.FindUserByID(userID); !ok {
		return nil, ErrUserNotFound
	}
	return s.store.ListSubscriptions(userID), nil
}

func (s *Service) Allows(userID, feature string) (bool, error) {
	if override, ok := s.store.GetUserEntitlement(userID, feature); ok {
		return override.Enabled, nil
	}
	plan, err := s.Current(userID)
	if err != nil {
		return false, err
	}
	switch feature {
	case FeaturePremiumTemplates:
		return plan.PremiumTemplatesAllowed, nil
	case FeatureCustomDomain:
		return plan.CustomDomainAllowed, nil
	case FeaturePaymentGateway:
		return plan.PaymentGatewayAllowed, nil
	default:
		return false, nil
	}
}

func (s *Service) ChangePlan(userID, planID string) (*store.Plan, error) {
	if _, ok := s.store.FindUserByID(userID); !ok {
		return nil, ErrUserNotFound
	}
	var found bool
	for _, plan := range s.store.ListPlans() {
		if plan.ID == planID {
			found = true
			break
		}
	}
	if !found {
		return nil, ErrPlanNotFound
	}
	if err := s.store.SetUserPlan(userID, planID); err != nil {
		return nil, err
	}
	if planID == "free" {
		_ = s.store.CancelActiveSubscriptions(userID)
	}
	return s.store.GetUserPlan(userID)
}

func (s *Service) Checkout(userID, planID string) (*store.Subscription, string, error) {
	if _, ok := s.store.FindUserByID(userID); !ok {
		return nil, "", ErrUserNotFound
	}
	var plan *store.Plan
	for _, item := range s.store.ListPlans() {
		if item.ID == planID {
			plan = item
			break
		}
	}
	if plan == nil {
		return nil, "", ErrPlanNotFound
	}
	if plan.Price <= 0 {
		return nil, "", errors.New("free plan does not require checkout")
	}
	if s.gateway == nil {
		return nil, "", errors.New("payment gateway unavailable")
	}
	var endsAt *time.Time
	if plan.DurationDays != nil {
		expiry := time.Now().UTC().AddDate(0, 0, *plan.DurationDays)
		endsAt = &expiry
	}
	payment, err := s.gateway.Create(context.Background(), plan.Price)
	if err != nil {
		return nil, "", err
	}
	sub, err := s.store.CreateSubscription(store.Subscription{UserID: userID, PlanID: planID, Status: "pending", Provider: "dummy", ProviderReference: payment.Reference, EndsAt: endsAt})
	if err != nil {
		return nil, "", err
	}
	return sub, payment.CheckoutURL, nil
}

func (s *Service) Confirm(reference string) (*store.Subscription, error) {
	sub, ok := s.store.FindSubscriptionByReference(reference)
	if !ok || sub.Status != "pending" {
		return nil, ErrPlanNotFound
	}
	if err := s.store.CancelActiveSubscriptions(sub.UserID); err != nil {
		return nil, err
	}
	updated, err := s.store.UpdateSubscriptionStatus(sub.ID, "active")
	if err != nil {
		return nil, err
	}
	if err := s.store.SetUserPlan(updated.UserID, updated.PlanID); err != nil {
		return nil, err
	}
	plan, err := s.store.GetUserPlan(updated.UserID)
	if err != nil {
		return nil, err
	}
	paidAt := time.Now().UTC()
	if _, err := s.store.CreateInvoice(store.Invoice{UserID: updated.UserID, SubscriptionID: updated.ID, InvoiceNumber: "INV-" + updated.ID, Amount: plan.Price, Status: "paid", PaidAt: &paidAt}); err != nil {
		return nil, err
	}
	return updated, nil
}
