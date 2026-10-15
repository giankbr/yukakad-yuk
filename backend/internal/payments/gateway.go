package payments

import (
	"context"
	"crypto/rand"
	"encoding/hex"
	"errors"
	"fmt"
	"time"
)

// Payment is a created checkout: Reference is the provider's id, CheckoutURL is where the payer goes.
type Payment struct {
	Reference   string
	CheckoutURL string
}

// Request describes what is being paid for.
type Request struct {
	Amount      float64
	Name        string
	Description string
	Email       string
	Mobile      string
	RedirectURL string
	ExpiresAt   time.Time
	Extra       map[string]string
}

// Payment statuses reported by Status.
const (
	StatusPaid    = "paid"
	StatusUnpaid  = "unpaid"
	StatusClosed  = "closed"
	StatusUnknown = "unknown"
)

var ErrStatusUnsupported = errors.New("payment status lookup not supported")

type Gateway interface {
	// Name is stored as the subscription provider ("dummy", "mayar").
	Name() string
	Create(context.Context, Request) (Payment, error)
	// Status asks the provider for the current state of a payment by its reference.
	Status(ctx context.Context, reference string) (string, error)
}

// Dummy simulates a gateway for local development: checkout goes to a confirm page on the frontend.
type Dummy struct{ BaseURL string }

func (Dummy) Name() string { return "dummy" }

func (d Dummy) Create(ctx context.Context, _ Request) (Payment, error) {
	select {
	case <-ctx.Done():
		return Payment{}, ctx.Err()
	default:
	}
	buf := make([]byte, 12)
	if _, err := rand.Read(buf); err != nil {
		return Payment{}, err
	}
	ref := "DUMMY-" + hex.EncodeToString(buf)
	return Payment{Reference: ref, CheckoutURL: fmt.Sprintf("%s/payments/dummy/%s", d.BaseURL, ref)}, nil
}

func (Dummy) Status(context.Context, string) (string, error) {
	return StatusUnknown, ErrStatusUnsupported
}
