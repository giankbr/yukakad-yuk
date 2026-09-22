package config

import "testing"

func TestValidateRequiresProductionDependencies(t *testing.T) {
	cfg := Config{Environment: "production", JWTSecret: "change-me"}
	if err := cfg.Validate(); err == nil {
		t.Fatal("expected missing dependency error")
	}

	cfg = Config{
		Environment: "production", DatabaseURL: "postgres://db", RedisURL: "redis://redis",
		JWTSecret: "a-real-secret", FrontendOrigin: "https://app.example.com",
		MinioEndpoint: "minio:9000", MinioAccessKey: "access", MinioSecretKey: "secret", MinioBucket: "media",
		SMTPHost: "smtp.example.com", SMTPFrom: "no-reply@example.com",
		PaymentWebhookSecret: "webhook-secret",
	}
	if err := cfg.Validate(); err != nil {
		t.Fatalf("expected valid config, got %v", err)
	}
}

func TestValidateRejectsDefaultProductionSecret(t *testing.T) {
	cfg := Config{
		Environment: "production", DatabaseURL: "postgres://db", RedisURL: "redis://redis",
		JWTSecret: "yukakad-dev-secret-change-me", FrontendOrigin: "https://app.example.com",
		MinioEndpoint: "minio:9000", MinioAccessKey: "access", MinioSecretKey: "secret", MinioBucket: "media",
	}
	if err := cfg.Validate(); err == nil {
		t.Fatal("expected default production secret error")
	}
}
