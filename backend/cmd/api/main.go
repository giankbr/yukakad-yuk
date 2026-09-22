package main

import (
	"context"
	"log"
	"net/http"
	"os/signal"
	"syscall"
	"time"
	"yukakad/internal/api"
	"yukakad/internal/auth"
	"yukakad/internal/config"
	"yukakad/internal/db"
	"yukakad/internal/mailer"
	"yukakad/internal/maintenance"
	"yukakad/internal/ratelimit"
	"yukakad/internal/session"
	"yukakad/internal/storage"
	"yukakad/internal/store"
	"yukakad/internal/tokenstore"

	"github.com/redis/go-redis/v9"
)

func main() {
	cfg := config.Load()
	if err := cfg.Validate(); err != nil {
		log.Fatal(err)
	}

	postgres, err := db.NewPostgres(cfg.DatabaseURL)
	if err != nil {
		log.Fatalf("database unavailable: %v", err)
	}
	defer postgres.Close()
	if err := db.MustMigrate(postgres, []string{db.Schema001, db.Schema002, db.Schema003, db.Schema004, db.Schema005, db.Schema006, db.Schema007, db.Schema008, db.Schema009, db.Schema010, db.Schema011, db.Schema012, db.Schema013}); err != nil {
		log.Fatalf("database migration failed: %v", err)
	}
	dataStore := store.Store(store.NewPostgresStore(postgres))
	log.Println("database connected and migrated")

	bootstrapAdmin(dataStore, cfg)

	server := api.NewServerWithStore(cfg, dataStore)
	if cfg.SMTPHost != "" && cfg.SMTPFrom != "" {
		server.SetPasswordResetSender(mailer.SMTP{Host: cfg.SMTPHost, Port: cfg.SMTPPort, Username: cfg.SMTPUsername, Password: cfg.SMTPPassword, From: cfg.SMTPFrom})
	}

	opts, err := redis.ParseURL(cfg.RedisURL)
	if err != nil {
		log.Fatalf("redis url invalid: %v", err)
	}
	redisClient := redis.NewClient(opts)
	if err := redisClient.Ping(context.Background()).Err(); err != nil {
		log.Fatalf("redis unavailable: %v", err)
	}
	defer redisClient.Close()
	log.Println("redis connected")
	server.SetRevoker(tokenstore.NewRedisRevoker(redisClient))
	server.SetLimiter(ratelimit.NewRedisLimiter(redisClient))
	server.SetSessions(session.NewRedisManager(redisClient))

	storageClient, err := storage.New(cfg)
	if err != nil {
		log.Fatalf("object storage unavailable: %v", err)
	}
	server.SetStorage(storageClient)

	ctx, stop := signal.NotifyContext(context.Background(), syscall.SIGINT, syscall.SIGTERM)
	defer stop()
	go maintenance.New(postgres, 5*time.Minute).Start(ctx)
	go func() {
		<-ctx.Done()
		shutdownCtx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
		defer cancel()
		if err := server.Shutdown(shutdownCtx); err != nil {
			log.Printf("server shutdown: %v", err)
		}
	}()

	log.Printf("Yukakad API starting on :%s", cfg.Port)
	if err := server.ListenAndServe(); err != nil && err != http.ErrServerClosed {
		log.Fatal(err)
	}
}

// bootstrapAdmin ensures ADMIN_EMAIL/ADMIN_PASSWORD (if set) always resolves to
// a working admin login: creates the account on first boot, or just re-promotes
// it to admin on later boots without touching its password.
func bootstrapAdmin(dataStore store.Store, cfg config.Config) {
	if cfg.AdminEmail == "" || cfg.AdminPassword == "" {
		return
	}
	if user, exists := dataStore.FindUserByEmail(cfg.AdminEmail); exists {
		if _, err := dataStore.UpdateUserRole(user.ID, "admin"); err != nil {
			log.Printf("admin bootstrap: failed to promote existing user: %v", err)
		} else {
			log.Printf("admin bootstrap: %s promoted to admin", cfg.AdminEmail)
		}
		return
	}
	hashed, err := auth.HashPassword(cfg.AdminPassword)
	if err != nil {
		log.Printf("admin bootstrap: failed to hash password: %v", err)
		return
	}
	user, err := dataStore.CreateUser("Admin", cfg.AdminEmail, hashed)
	if err != nil {
		log.Printf("admin bootstrap: failed to create user: %v", err)
		return
	}
	if _, err := dataStore.UpdateUserRole(user.ID, "admin"); err != nil {
		log.Printf("admin bootstrap: failed to set role: %v", err)
		return
	}
	log.Printf("admin bootstrap: created admin account %s", cfg.AdminEmail)
}
