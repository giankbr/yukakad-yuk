package config

import (
	"crypto/rand"
	"encoding/hex"
	"fmt"
	"log"
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
	// InternalAPISecret identifies server-to-server calls from the Next.js server (skips the global per-IP limit).
	InternalAPISecret string
	// CustomDomainTarget is the hostname couples point their own domain at (CNAME), e.g. domains.rawuh.id.
	CustomDomainTarget string
	MayarAPIKey        string
	MayarEnvironment   string
	MayarBaseURL       string // optional override, e.g. a local fake in tests

	AdminEmail    string
	AdminPassword string
}

func Load() Config {
	cfg := Config{
		Port:           getEnv("PORT", "8080"),
		Environment:    getEnv("ENVIRONMENT", "development"),
		JWTSecret:      jwtSecretFromEnv(),
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
		InternalAPISecret:    getEnv("INTERNAL_API_SECRET", ""),
		CustomDomainTarget:   getEnv("CUSTOM_DOMAIN_TARGET", "domains.rawuh.id"),
		MayarAPIKey:          getEnv("MAYAR_API_KEY", ""),
		MayarEnvironment:     getEnv("MAYAR_ENV", "sandbox"),
		MayarBaseURL:         getEnv("MAYAR_BASE_URL", ""),

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
	// Tokens are HMAC-signed with this secret; a known or short value lets anyone mint admin tokens.
	if weakSecrets[c.JWTSecret] || len(c.JWTSecret) < 16 {
		return fmt.Errorf("JWT_SECRET is missing, a known default or shorter than 16 characters")
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

// weakSecrets are values that appeared in docs/examples; never accept them.
var weakSecrets = map[string]bool{"yukakad-dev-secret-change-me": true, "change-me": true, "secret": true, "changeme": true}

// jwtSecretFromEnv returns JWT_SECRET, or a random per-process secret when it is unset, so a missing variable
// can never fall back to a public default (sessions then last until the next restart).
func jwtSecretFromEnv() string {
	if value := strings.TrimSpace(os.Getenv("JWT_SECRET")); value != "" {
		return value
	}
	buf := make([]byte, 32)
	if _, err := rand.Read(buf); err != nil {
		panic("config: cannot generate JWT secret: " + err.Error())
	}
	log.Println("config: JWT_SECRET is not set; using a random secret for this process (logins reset on restart)")
	return hex.EncodeToString(buf)
}

func getEnv(key, fallback string) string {
	if value, ok := os.LookupEnv(key); ok && value != "" {
		return value
	}
	return fallback
}
