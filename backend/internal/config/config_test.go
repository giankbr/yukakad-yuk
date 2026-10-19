package config

import "testing"

func TestValidateRequiresProductionDependencies(t *testing.T) {
	cfg := Config{Environment: "production", JWTSecret: "change-me"}
	if err := cfg.Validate(); err == nil {
		t.Fatal("expected missing dependency error")
	}

	cfg = Config{
		Environment: "production", DatabaseURL: "postgres://db", RedisURL: "redis://redis",
		JWTSecret: "a-real-secret-0123456789", FrontendOrigin: "https://app.example.com",
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

func TestValidateRejectsWeakSecretInAnyEnvironment(t *testing.T) {
	for _, secret := range []string{"", "yukakad-dev-secret-change-me", "short"} {
		cfg := Config{Environment: "development", DatabaseURL: "postgres://db", RedisURL: "redis://redis", JWTSecret: secret,
			FrontendOrigin: "http://localhost:3000", MinioEndpoint: "m", MinioAccessKey: "a", MinioSecretKey: "s", MinioBucket: "b"}
		if err := cfg.Validate(); err == nil {
			t.Fatalf("secret %q should be rejected", secret)
		}
	}
	t.Setenv("JWT_SECRET", "")
	if a, b := jwtSecretFromEnv(), jwtSecretFromEnv(); a == b || len(a) < 32 {
		t.Fatal("unset JWT_SECRET should produce a random secret")
	}
}
