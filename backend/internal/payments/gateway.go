package payments

import (
	"context"
	"crypto/rand"
	"encoding/hex"
	"fmt"
)

type Payment struct {
	Reference   string
	CheckoutURL string
}
type Gateway interface {
	Create(context.Context, float64) (Payment, error)
}
type Dummy struct{ BaseURL string }

func (d Dummy) Create(ctx context.Context, amount float64) (Payment, error) {
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
