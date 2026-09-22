package mailer

import (
	"context"
	"fmt"
	"net/smtp"
)

type Sender interface {
	SendPasswordReset(ctx context.Context, email, resetURL string) error
}

type Func func(context.Context, string, string) error

func (f Func) SendPasswordReset(ctx context.Context, email, resetURL string) error {
	return f(ctx, email, resetURL)
}

type SMTP struct {
	Host     string
	Port     string
	Username string
	Password string
	From     string
}

func (s SMTP) SendPasswordReset(ctx context.Context, email, resetURL string) error {
	select {
	case <-ctx.Done():
		return ctx.Err()
	default:
	}
	body := []byte(fmt.Sprintf("To: %s\r\nSubject: Yukakad password reset\r\nContent-Type: text/plain; charset=UTF-8\r\n\r\nReset password Anda melalui link berikut (berlaku 30 menit):\r\n%s\r\n", email, resetURL))
	var auth smtp.Auth
	if s.Username != "" {
		auth = smtp.PlainAuth("", s.Username, s.Password, s.Host)
	}
	return smtp.SendMail(s.Host+":"+s.Port, auth, s.From, []string{email}, body)
}
