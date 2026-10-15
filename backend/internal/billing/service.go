package billing

import (
	"context"
	"errors"
	"fmt"
	"log"
	"sync"
	"time"
	"yukakad/internal/payments"
	"yukakad/internal/store"
)

var (
	ErrPlanNotFound    = errors.New("plan not found")
	ErrUserNotFound    = errors.New("user not found")
	ErrNotPaid         = errors.New("payment not completed")
	ErrGatewayDisabled = errors.New("payment gateway unavailable")
)

// CheckoutOptions carries the URL the payer returns to after paying.
type CheckoutOptions struct {
	RedirectURL string
}

const (
	FeaturePremiumTemplates = "premium_templates"
	FeatureCustomDomain     = "custom_domain"
	FeaturePaymentGateway   = "payment_gateway"
)

type Service struct {
	store   store.Store
	gateway payments.Gateway
	confirm sync.Mutex // serialises activation so a webhook and the return page can't both create an invoice
}

// Provider is the active gateway's name ("dummy", "mayar"), or "" when payments are disabled.
func (s *Service) Provider() string {
	if s.gateway == nil {
		return ""
	}
	return s.gateway.Name()
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

func (s *Service) Checkout(userID, planID string, options ...CheckoutOptions) (*store.Subscription, string, error) {
	user, ok := s.store.FindUserByID(userID)
	if !ok {
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
		return nil, "", ErrGatewayDisabled
	}
	var endsAt *time.Time
	if plan.DurationDays != nil {
		expiry := time.Now().UTC().AddDate(0, 0, *plan.DurationDays)
		endsAt = &expiry
	}
	request := payments.Request{
		Amount:      plan.Price,
		Name:        "Paket " + plan.Name + " · Rawuh",
		Description: fmt.Sprintf("Paket %s untuk %s", plan.Name, user.Email),
		Email:       user.Email,
		ExpiresAt:   time.Now().UTC().Add(24 * time.Hour),
		Extra:       map[string]string{"user_id": userID, "plan_id": planID},
	}
	if len(options) > 0 {
		request.RedirectURL = options[0].RedirectURL
	}
	ctx, cancel := context.WithTimeout(context.Background(), 25*time.Second)
	defer cancel()
	payment, err := s.gateway.Create(ctx, request)
	if err != nil {
		return nil, "", err
	}
	sub, err := s.store.CreateSubscription(store.Subscription{UserID: userID, PlanID: planID, Status: "pending", Provider: s.gateway.Name(), ProviderReference: payment.Reference, EndsAt: endsAt})
	if err != nil {
		return nil, "", err
	}
	return sub, payment.CheckoutURL, nil
}

func (s *Service) Confirm(reference string) (*store.Subscription, error) {
	s.confirm.Lock()
	defer s.confirm.Unlock()
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

// ConfirmPaid activates a pending subscription only after the gateway itself reports it paid.
// Used by webhooks and the return page, so a forged callback cannot unlock a plan.
func (s *Service) ConfirmPaid(ctx context.Context, reference string) (*store.Subscription, error) {
	sub, ok := s.store.FindSubscriptionByReference(reference)
	if !ok {
		return nil, ErrPlanNotFound
	}
	if sub.Status == "active" {
		return sub, nil
	}
	if sub.Status != "pending" || s.gateway == nil || sub.Provider != s.gateway.Name() {
		return nil, ErrPlanNotFound
	}
	status, err := s.gateway.Status(ctx, reference)
	if err != nil {
		return nil, err
	}
	if status == payments.StatusClosed {
		// Expired or cancelled at the provider: stop checking it.
		_, _ = s.store.UpdateSubscriptionStatus(sub.ID, "expired")
		return nil, ErrNotPaid
	}
	if status != payments.StatusPaid {
		return nil, ErrNotPaid
	}
	confirmed, err := s.Confirm(reference)
	if err != nil {
		// Activated concurrently by another caller.
		if current, ok := s.store.FindSubscriptionByReference(reference); ok && current.Status == "active" {
			return current, nil
		}
	}
	return confirmed, err
}

// VerifyPending re-checks the user's pending payments with the gateway and activates any that were paid.
// Returns the subscriptions that became active.
func (s *Service) VerifyPending(ctx context.Context, userID string) ([]*store.Subscription, error) {
	if _, ok := s.store.FindUserByID(userID); !ok {
		return nil, ErrUserNotFound
	}
	if s.gateway == nil {
		return nil, ErrGatewayDisabled
	}
	activated := []*store.Subscription{}
	for _, sub := range s.store.ListSubscriptions(userID) {
		if sub.Status != "pending" || sub.Provider != s.gateway.Name() || sub.ProviderReference == "" {
			continue
		}
		confirmed, err := s.ConfirmPaid(ctx, sub.ProviderReference)
		if err == nil {
			activated = append(activated, confirmed)
			continue
		}
		if !errors.Is(err, ErrNotPaid) && !errors.Is(err, payments.ErrStatusUnsupported) {
			log.Printf("billing: verify %s: %v", sub.ProviderReference, err)
		}
	}
	return activated, nil
}
