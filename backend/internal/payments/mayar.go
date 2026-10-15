package payments

import (
	"bytes"
	"context"
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"math"
	"net/http"
	"net/url"
	"strings"
	"time"
)

// Mayar base URLs (API v2). Sandbox keys come from web.mayar.io, production keys from web.mayar.id.
const (
	MayarProductionURL = "https://api.mayar.id/hl/v2"
	MayarSandboxURL    = "https://api.mayar.io/hl/v2"
)

// Mayar creates "single payment requests" (https://docs.mayar.id/api-reference-v2/reqpayment/create).
type Mayar struct {
	APIKey  string
	BaseURL string
	Client  *http.Client
}

func NewMayar(apiKey, environment string) *Mayar {
	base := MayarSandboxURL
	if strings.EqualFold(environment, "production") {
		base = MayarProductionURL
	}
	return &Mayar{APIKey: apiKey, BaseURL: base, Client: &http.Client{Timeout: 20 * time.Second}}
}

func (*Mayar) Name() string { return "mayar" }

type mayarEnvelope struct {
	StatusCode int             `json:"statusCode"`
	Messages   any             `json:"messages"`
	Data       json.RawMessage `json:"data"`
}

func (m *Mayar) do(ctx context.Context, method, path string, body any) (json.RawMessage, error) {
	var reader io.Reader
	if body != nil {
		raw, err := json.Marshal(body)
		if err != nil {
			return nil, err
		}
		reader = bytes.NewReader(raw)
	}
	req, err := http.NewRequestWithContext(ctx, method, strings.TrimRight(m.BaseURL, "/")+path, reader)
	if err != nil {
		return nil, err
	}
	req.Header.Set("Authorization", "Bearer "+m.APIKey)
	req.Header.Set("Accept", "application/json")
	if body != nil {
		req.Header.Set("Content-Type", "application/json")
	}
	client := m.Client
	if client == nil {
		client = http.DefaultClient
	}
	res, err := client.Do(req)
	if err != nil {
		return nil, fmt.Errorf("mayar: %w", err)
	}
	defer res.Body.Close()
	raw, _ := io.ReadAll(io.LimitReader(res.Body, 1<<20))
	var envelope mayarEnvelope
	_ = json.Unmarshal(raw, &envelope)
	if res.StatusCode >= 300 || (envelope.StatusCode != 0 && envelope.StatusCode >= 300) {
		return nil, fmt.Errorf("mayar: HTTP %d: %s", res.StatusCode, mayarMessage(envelope.Messages, raw))
	}
	return envelope.Data, nil
}

func mayarMessage(messages any, raw []byte) string {
	switch v := messages.(type) {
	case string:
		return v
	case nil:
		text := strings.TrimSpace(string(raw))
		if len(text) > 200 {
			text = text[:200]
		}
		return text
	default:
		out, _ := json.Marshal(v)
		return string(out)
	}
}

func (m *Mayar) Create(ctx context.Context, request Request) (Payment, error) {
	if m.APIKey == "" {
		return Payment{}, errors.New("mayar: API key is not configured")
	}
	amount := int64(math.Round(request.Amount))
	if amount <= 0 {
		return Payment{}, errors.New("mayar: amount must be positive")
	}
	body := map[string]any{"name": request.Name, "amount": amount}
	optional := map[string]string{"email": request.Email, "mobile": request.Mobile, "description": request.Description, "redirectUrl": request.RedirectURL}
	for key, value := range optional {
		if strings.TrimSpace(value) != "" {
			body[key] = value
		}
	}
	if !request.ExpiresAt.IsZero() {
		body["expiredAt"] = request.ExpiresAt.UTC().Format("2006-01-02T15:04:05.000Z")
	}
	if len(request.Extra) > 0 {
		body["extraData"] = request.Extra
	}
	data, err := m.do(ctx, http.MethodPost, "/payments/create", body)
	if err != nil {
		return Payment{}, err
	}
	var created struct {
		ID   string `json:"id"`
		Link string `json:"link"`
	}
	if err := json.Unmarshal(data, &created); err != nil || created.ID == "" || created.Link == "" {
		return Payment{}, errors.New("mayar: unexpected create response")
	}
	return Payment{Reference: created.ID, CheckoutURL: created.Link}, nil
}

func (m *Mayar) Status(ctx context.Context, reference string) (string, error) {
	if m.APIKey == "" {
		return StatusUnknown, errors.New("mayar: API key is not configured")
	}
	data, err := m.do(ctx, http.MethodGet, "/payments/"+url.PathEscape(reference), nil)
	if err != nil {
		return StatusUnknown, err
	}
	var detail struct {
		Status string `json:"status"`
	}
	if err := json.Unmarshal(data, &detail); err != nil {
		return StatusUnknown, errors.New("mayar: unexpected detail response")
	}
	switch strings.ToLower(detail.Status) {
	case "paid", "success", "settled":
		return StatusPaid, nil
	case "unpaid", "pending":
		return StatusUnpaid, nil
	case "closed", "expired", "failed", "cancelled", "canceled":
		return StatusClosed, nil
	default:
		return StatusUnknown, nil
	}
}
