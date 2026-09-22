package config

import (
	"fmt"
	"os"
	"strings"
)

type Config struct {
	Port           string
	Environment    string
	JWTSecret      string
	DatabaseURL    string
	RedisURL       string
	FrontendOrigin string

	MinioEndpoint      string
	MinioAccessKey     string
	MinioSecretKey     string
	MinioBucket        string
	MinioUseSSL        bool
	MinioPublicBaseURL string

	SMTPHost             string
	SMTPPort             string
	SMTPUsername         string
	SMTPPassword         string
	SMTPFrom             string
	PaymentWebhookSecret string

	AdminEmail    string
	AdminPassword string
}

func Load() Config {
	cfg := Config{
		Port:           getEnv("PORT", "8080"),
		Environment:    getEnv("ENVIRONMENT", "development"),
		JWTSecret:      getEnv("JWT_SECRET", "yukakad-dev-secret-change-me"),
		DatabaseURL:    getEnv("DATABASE_URL", "postgres://postgres:postgres@localhost:5432/yukakad?sslmode=disable"),
		RedisURL:       getEnv("REDIS_URL", ""),
		FrontendOrigin: getEnv("FRONTEND_ORIGIN", "http://localhost:3000"),

		MinioEndpoint:        getEnv("MINIO_ENDPOINT", ""),
		MinioAccessKey:       getEnv("MINIO_ACCESS_KEY", ""),
		MinioSecretKey:       getEnv("MINIO_SECRET_KEY", ""),
		MinioBucket:          getEnv("MINIO_BUCKET", "yukakad-media"),
		MinioUseSSL:          getEnv("MINIO_USE_SSL", "false") == "true",
		MinioPublicBaseURL:   getEnv("MINIO_PUBLIC_BASE_URL", ""),
		SMTPHost:             getEnv("SMTP_HOST", ""),
		SMTPPort:             getEnv("SMTP_PORT", "587"),
		SMTPUsername:         getEnv("SMTP_USERNAME", ""),
		SMTPPassword:         getEnv("SMTP_PASSWORD", ""),
		SMTPFrom:             getEnv("SMTP_FROM", ""),
		PaymentWebhookSecret: getEnv("PAYMENT_WEBHOOK_SECRET", ""),

		AdminEmail:    getEnv("ADMIN_EMAIL", ""),
		AdminPassword: getEnv("ADMIN_PASSWORD", ""),
	}
	return cfg
}

// Validate rejects an incomplete runtime configuration before the server can
// accept traffic. Tests construct Config directly and do not call this.
func (c Config) Validate() error {
	missing := make([]string, 0, 6)
	for key, value := range map[string]string{
		"DATABASE_URL":     c.DatabaseURL,
		"REDIS_URL":        c.RedisURL,
		"JWT_SECRET":       c.JWTSecret,
		"FRONTEND_ORIGIN":  c.FrontendOrigin,
		"MINIO_ENDPOINT":   c.MinioEndpoint,
		"MINIO_ACCESS_KEY": c.MinioAccessKey,
		"MINIO_SECRET_KEY": c.MinioSecretKey,
		"MINIO_BUCKET":     c.MinioBucket,
	} {
		if strings.TrimSpace(value) == "" {
			missing = append(missing, key)
		}
	}
	if c.Environment == "production" && c.JWTSecret == "yukakad-dev-secret-change-me" {
		return fmt.Errorf("JWT_SECRET must be changed in production")
	}
	if len(missing) > 0 {
		return fmt.Errorf("missing required configuration: %s", strings.Join(missing, ", "))
	}
	if c.Environment == "production" && (strings.TrimSpace(c.SMTPHost) == "" || strings.TrimSpace(c.SMTPFrom) == "") {
		return fmt.Errorf("SMTP_HOST and SMTP_FROM are required in production")
	}
	if c.Environment == "production" && strings.TrimSpace(c.PaymentWebhookSecret) == "" {
		return fmt.Errorf("PAYMENT_WEBHOOK_SECRET is required in production")
	}
	return nil
}

func getEnv(key, fallback string) string {
	if value, ok := os.LookupEnv(key); ok && value != "" {
		return value
	}
	return fallback
}
