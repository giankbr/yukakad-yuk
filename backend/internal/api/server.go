package api

import (
	"context"
	"encoding/json"
	"errors"
	"net"
	"net/http"
	"strings"
	"time"
	"yukakad/internal/auth"
	billingservice "yukakad/internal/billing"
	"yukakad/internal/config"
	domainservice "yukakad/internal/domains"
	giftservice "yukakad/internal/gifts"
	guestservice "yukakad/internal/guests"
	"yukakad/internal/invitations"
	"yukakad/internal/mailer"
	mediaservice "yukakad/internal/media"
	"yukakad/internal/payments"
	"yukakad/internal/ratelimit"
	rsvpservice "yukakad/internal/rsvp"
	"yukakad/internal/session"
	"yukakad/internal/storage"
	"yukakad/internal/store"
	templateservice "yukakad/internal/templates"
	"yukakad/internal/tokenstore"
	wishservice "yukakad/internal/wishes"
)

type Server struct {
	config      *config.Config
	store       store.Store
	revoker     tokenstore.Revoker
	limiter     ratelimit.Limiter
	storage     *storage.Client
	httpServer  *http.Server
	sessions    session.Manager
	invitations *invitations.Service
	guests      *guestservice.Service
	media       *mediaservice.Service
	rsvps       *rsvpservice.Service
	wishes      *wishservice.Service
	gifts       *giftservice.Service
	billing     *billingservice.Service
	domains     *domainservice.Service
	templates   *templateservice.Service
	resetMailer mailer.Sender
}

func NewServer(cfg config.Config) *Server {
	memoryStore := store.NewMemoryStore()
	memoryStore.SeedTemplates()
	memoryStore.SeedPlans()
	return NewServerWithStore(cfg, memoryStore)
}

func NewServerWithStore(cfg config.Config, dataStore store.Store) *Server {
	return &Server{
		config:      &cfg,
		store:       dataStore,
		revoker:     tokenstore.NewMemoryRevoker(),
		limiter:     ratelimit.NewMemoryLimiter(),
		invitations: invitations.NewService(dataStore),
		guests:      guestservice.NewService(dataStore),
		media:       mediaservice.NewService(dataStore, nil),
		rsvps:       rsvpservice.NewService(dataStore),
		wishes:      wishservice.NewService(dataStore),
		templates:   templateservice.NewService(dataStore),
		gifts:       giftservice.NewService(dataStore, payments.Dummy{BaseURL: cfg.FrontendOrigin}),
		billing:     billingservice.NewService(dataStore, payments.Dummy{BaseURL: cfg.FrontendOrigin}),
		domains:     domainservice.NewService(dataStore, billingservice.NewService(dataStore, payments.Dummy{BaseURL: cfg.FrontendOrigin})),
	}
}

// SetRevoker overrides the default in-memory token revocation store, e.g.
// with a Redis-backed one in production.
func (s *Server) SetRevoker(r tokenstore.Revoker) { s.revoker = r }

// SetLimiter overrides the default in-memory rate limiter, e.g. with a
// Redis-backed one shared across instances.
func (s *Server) SetLimiter(l ratelimit.Limiter) { s.limiter = l }

// SetStorage wires an object storage client for media uploads. Left nil,
// the media upload endpoint responds 503 instead of panicking.
func (s *Server) SetStorage(c *storage.Client) {
	s.storage = c
	s.media = mediaservice.NewService(s.store, c)
}

func (s *Server) SetSessions(manager session.Manager) { s.sessions = manager }

func (s *Server) SetPasswordResetSender(sender mailer.Sender) { s.resetMailer = sender }

func (s *Server) ListenAndServe() error {
	mux := http.NewServeMux()
	mux.HandleFunc("/health", s.handleHealth)
	mux.HandleFunc("/api/v1/health", s.handleHealth)
	mux.HandleFunc("/api/auth/register", s.handleRegister)
	mux.HandleFunc("/api/auth/login", s.handleLogin)
	mux.HandleFunc("/api/auth/logout", s.handleLogout)
	mux.HandleFunc("/api/auth/forgot-password", s.handleForgotPassword)
	mux.HandleFunc("/api/auth/reset-password", s.handleResetPassword)
	mux.HandleFunc("/api/profile", s.handleProfile)
	mux.HandleFunc("/api/invitations", s.handleInvitations)
	mux.HandleFunc("/api/templates", s.handleTemplates)
	mux.HandleFunc("/api/templates/", s.handleTemplates)
	mux.HandleFunc("/api/public/invitation/", s.handlePublicInvitation)
	mux.HandleFunc("/api/public/current", s.handlePublicCurrent)
	mux.HandleFunc("/api/payments/dummy/", s.handleDummyPayment)
	mux.HandleFunc("/api/billing/plan", s.handleBillingPlan)
	mux.HandleFunc("/api/billing/checkout", s.handleBillingCheckout)
	mux.HandleFunc("/api/billing/subscriptions", s.handleBillingSubscriptions)
	mux.HandleFunc("/api/billing/invoices", s.handleBillingInvoices)
	mux.HandleFunc("/api/billing/entitlements", s.handleBillingEntitlements)
	mux.HandleFunc("/api/billing/dummy/", s.handleBillingDummyConfirm)
	mux.HandleFunc("/api/webhooks/payment", s.handlePaymentWebhook)
	mux.HandleFunc("/api/invitations/", s.handleInvitationDetail)
	mux.HandleFunc("/api/public/site-content/", s.handlePublicSiteContent)
	mux.HandleFunc("/api/public/features", s.handlePublicFeatures)
	mux.HandleFunc("/api/public/testimonials", s.handlePublicTestimonials)
	mux.HandleFunc("/api/public/plans", s.handlePublicPlans)
	mux.HandleFunc("/api/admin/site-content/", s.handleAdminSiteContent)
	mux.HandleFunc("/api/admin/features", s.handleAdminFeatures)
	mux.HandleFunc("/api/admin/features/", s.handleAdminFeatureDetail)
	mux.HandleFunc("/api/admin/testimonials", s.handleAdminTestimonials)
	mux.HandleFunc("/api/admin/testimonials/", s.handleAdminTestimonialDetail)
	mux.HandleFunc("/api/admin/templates", s.handleAdminTemplates)
	mux.HandleFunc("/api/admin/templates/", s.handleAdminTemplates)
	mux.HandleFunc("/api/admin/stats", s.handleAdminStats)
	mux.HandleFunc("/api/admin/users", s.handleAdminUsers)
	mux.HandleFunc("/api/admin/users/", s.handleAdminUsers)
	// v1 is the canonical API namespace. The adapter normalizes the prefix
	// before invoking the existing domain handlers while the handler modules
	// are migrated behind services.
	mux.HandleFunc("/api/v1/", s.handleV1)

	var handler http.Handler = mux
	handler = s.rateLimitMiddleware(handler)
	handler = s.corsMiddleware(handler)
	handler = s.securityHeadersMiddleware(handler)
	handler = s.requestIDMiddleware(handler)
	handler = s.loggingMiddleware(handler)

	s.httpServer = &http.Server{
		Addr:              ":" + s.config.Port,
		Handler:           handler,
		ReadHeaderTimeout: 10 * time.Second,
		ReadTimeout:       30 * time.Second,
		WriteTimeout:      30 * time.Second,
		IdleTimeout:       120 * time.Second,
	}
	return s.httpServer.ListenAndServe()
}

func (s *Server) handleV1(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("X-API-Version", "v1")
	path := strings.TrimPrefix(r.URL.Path, "/api/v1")
	if path == "" {
		path = "/"
	}
	r2 := r.Clone(r.Context())
	r2.URL.Path = "/api" + path
	r2.Header.Set("X-API-Version", "v1")

	switch {
	case strings.HasPrefix(path, "/auth/"):
		s.handleAuthV1(w, r2)
	case path == "/profile" || path == "/me":
		s.handleProfile(w, r2)
	case path == "/invitations" || strings.HasPrefix(path, "/invitations/"):
		s.handleInvitationV1(w, r2)
	case path == "/templates" || strings.HasPrefix(path, "/templates/"):
		s.handleTemplates(w, r2)
	case path == "/billing/plan":
		s.handleBillingPlan(w, r2)
	case path == "/billing/checkout":
		s.handleBillingCheckout(w, r2)
	case path == "/billing/subscriptions":
		s.handleBillingSubscriptions(w, r2)
	case path == "/billing/invoices":
		s.handleBillingInvoices(w, r2)
	case path == "/billing/entitlements":
		s.handleBillingEntitlements(w, r2)
	case strings.HasPrefix(path, "/billing/dummy/"):
		s.handleBillingDummyConfirm(w, r2)
	case strings.HasPrefix(path, "/payments/dummy/"):
		s.handleDummyPayment(w, r2)
	case path == "/webhooks/payment":
		s.handlePaymentWebhook(w, r2)
	case strings.HasPrefix(path, "/public/invitations/"):
		r2.URL.Path = "/api/public/invitation/" + strings.TrimPrefix(path, "/public/invitations/")
		s.handlePublicInvitation(w, r2)
	case strings.HasPrefix(path, "/public/invitation/"):
		s.handlePublicInvitation(w, r2)
	case path == "/public/current":
		s.handlePublicCurrent(w, r2)
	case strings.HasPrefix(path, "/public/site-content/") || path == "/public/features" || path == "/public/testimonials" || path == "/public/plans":
		s.handlePublicV1(w, r2)
	case strings.HasPrefix(path, "/admin/"):
		s.handleAdminV1(w, r2)
	default:
		writeJSON(w, http.StatusNotFound, map[string]string{"error": "route not found"})
	}
}

func (s *Server) handleAuthV1(w http.ResponseWriter, r *http.Request) {
	switch r.URL.Path {
	case "/api/auth/register":
		s.handleRegister(w, r)
	case "/api/auth/login":
		s.handleLogin(w, r)
	case "/api/auth/logout":
		s.handleLogout(w, r)
	case "/api/auth/forgot-password":
		s.handleForgotPassword(w, r)
	case "/api/auth/reset-password":
		s.handleResetPassword(w, r)
	default:
		writeJSON(w, http.StatusNotFound, map[string]string{"error": "route not found"})
	}
}

func (s *Server) handleInvitationV1(w http.ResponseWriter, r *http.Request) {
	if r.URL.Path == "/api/invitations" {
		s.handleInvitations(w, r)
		return
	}
	s.handleInvitationDetail(w, r)
}

func (s *Server) handlePublicV1(w http.ResponseWriter, r *http.Request) {
	switch {
	case strings.HasPrefix(r.URL.Path, "/api/public/invitation/"):
		s.handlePublicInvitation(w, r)
	case strings.HasPrefix(r.URL.Path, "/api/public/site-content/"):
		s.handlePublicSiteContent(w, r)
	case r.URL.Path == "/api/public/features":
		s.handlePublicFeatures(w, r)
	case r.URL.Path == "/api/public/testimonials":
		s.handlePublicTestimonials(w, r)
	case r.URL.Path == "/api/public/plans":
		s.handlePublicPlans(w, r)
	default:
		writeJSON(w, http.StatusNotFound, map[string]string{"error": "route not found"})
	}
}

func (s *Server) handleAdminV1(w http.ResponseWriter, r *http.Request) {
	switch {
	case strings.HasPrefix(r.URL.Path, "/api/admin/site-content/"):
		s.handleAdminSiteContent(w, r)
	case r.URL.Path == "/api/admin/features" || strings.HasPrefix(r.URL.Path, "/api/admin/features/"):
		if strings.HasSuffix(r.URL.Path, "/features") {
			s.handleAdminFeatures(w, r)
		} else {
			s.handleAdminFeatureDetail(w, r)
		}
	case r.URL.Path == "/api/admin/testimonials" || strings.HasPrefix(r.URL.Path, "/api/admin/testimonials/"):
		if strings.HasSuffix(r.URL.Path, "/testimonials") {
			s.handleAdminTestimonials(w, r)
		} else {
			s.handleAdminTestimonialDetail(w, r)
		}
	case r.URL.Path == "/api/admin/stats":
		s.handleAdminStats(w, r)
	case r.URL.Path == "/api/admin/users" || strings.HasPrefix(r.URL.Path, "/api/admin/users/"):
		s.handleAdminUsers(w, r)
	case r.URL.Path == "/api/admin/templates" || strings.HasPrefix(r.URL.Path, "/api/admin/templates/"):
		s.handleAdminTemplates(w, r)
	default:
		writeJSON(w, http.StatusNotFound, map[string]string{"error": "route not found"})
	}
}

func (s *Server) Shutdown(ctx context.Context) error {
	if s.httpServer == nil {
		return nil
	}
	return s.httpServer.Shutdown(ctx)
}

func (s *Server) handleHealth(w http.ResponseWriter, r *http.Request) {
	writeJSON(w, http.StatusOK, map[string]any{
		"status":  "ok",
		"service": "yukakad-api",
		"time":    time.Now().UTC().Format(time.RFC3339),
	})
}

func (s *Server) handleRegister(w http.ResponseWriter, r *http.Request) {
	if !s.allowRate(w, "auth:register:"+clientIP(r), 10, time.Minute) {
		return
	}
	if r.Method != http.MethodPost {
		writeJSON(w, http.StatusMethodNotAllowed, map[string]string{"error": "method not allowed"})
		return
	}

	var payload struct {
		Name     string `json:"name"`
		Email    string `json:"email"`
		Password string `json:"password"`
	}
	if err := json.NewDecoder(r.Body).Decode(&payload); err != nil {
		writeJSON(w, http.StatusBadRequest, map[string]string{"error": "invalid payload"})
		return
	}
	if payload.Name == "" || payload.Email == "" || payload.Password == "" {
		writeJSON(w, http.StatusBadRequest, map[string]string{"error": "name, email, and password are required"})
		return
	}

	hashed, err := auth.HashPassword(payload.Password)
	if err != nil {
		writeJSON(w, http.StatusBadRequest, map[string]string{"error": "password is too long"})
		return
	}
	user, err := s.store.CreateUser(payload.Name, payload.Email, hashed)
	if err != nil {
		writeJSON(w, http.StatusConflict, map[string]string{"error": err.Error()})
		return
	}
	_ = s.store.SetUserPlan(user.ID, "free")

	token, err := s.issueToken(user)
	if err != nil {
		writeJSON(w, http.StatusServiceUnavailable, map[string]string{"error": "authentication service unavailable"})
		return
	}
	writeJSON(w, http.StatusCreated, map[string]any{
		"user": map[string]any{
			"id":    user.ID,
			"name":  user.Name,
			"email": user.Email,
			"role":  user.Role,
		},
		"token": token,
	})
}

func (s *Server) handleLogin(w http.ResponseWriter, r *http.Request) {
	if !s.allowRate(w, "auth:login:"+clientIP(r), 10, time.Minute) {
		return
	}
	if r.Method != http.MethodPost {
		writeJSON(w, http.StatusMethodNotAllowed, map[string]string{"error": "method not allowed"})
		return
	}

	var payload struct {
		Email    string `json:"email"`
		Password string `json:"password"`
	}
	if err := json.NewDecoder(r.Body).Decode(&payload); err != nil {
		writeJSON(w, http.StatusBadRequest, map[string]string{"error": "invalid payload"})
		return
	}

	user, exists := s.store.FindUserByEmail(payload.Email)
	if !exists || !auth.VerifyPassword(payload.Password, user.Password) {
		writeJSON(w, http.StatusUnauthorized, map[string]string{"error": "invalid credentials"})
		return
	}

	token, err := s.issueToken(user)
	if err != nil {
		writeJSON(w, http.StatusServiceUnavailable, map[string]string{"error": "authentication service unavailable"})
		return
	}
	writeJSON(w, http.StatusOK, map[string]any{
		"user": map[string]any{
			"id":    user.ID,
			"name":  user.Name,
			"email": user.Email,
			"role":  user.Role,
		},
		"token": token,
	})
}

func (s *Server) handleInvitations(w http.ResponseWriter, r *http.Request) {
	claims, ok := s.requireAuth(w, r)
	if !ok {
		return
	}

	if r.Method == http.MethodGet {
		items := s.store.ListInvitationsByUser(claims.UserID)
		if isV1(r) {
			start, end, meta := paginateRequest(r, len(items))
			writeJSON(w, http.StatusOK, map[string]any{"items": items[start:end], "pagination": meta})
			return
		}
		writeJSON(w, http.StatusOK, map[string]any{"items": items})
		return
	}
	if r.Method == http.MethodPost {
		var payload struct {
			Slug  string `json:"slug"`
			Title string `json:"title"`
		}
		if err := json.NewDecoder(r.Body).Decode(&payload); err != nil {
			writeJSON(w, http.StatusBadRequest, map[string]string{"error": "invalid payload"})
			return
		}
		if payload.Slug == "" || payload.Title == "" {
			writeJSON(w, http.StatusBadRequest, map[string]string{"error": "slug and title are required"})
			return
		}
		invitation, err := s.invitations.Create(claims.UserID, payload.Slug, payload.Title)
		if err != nil {
			status := http.StatusConflict
			if errors.Is(err, invitations.ErrInvalid) {
				status = http.StatusBadRequest
			}
			writeJSON(w, status, map[string]string{"error": err.Error()})
			return
		}
		writeJSON(w, http.StatusCreated, invitation)
		return
	}
	writeJSON(w, http.StatusMethodNotAllowed, map[string]string{"error": "method not allowed"})
}

func (s *Server) handleInvitationDetail(w http.ResponseWriter, r *http.Request) {
	path := strings.TrimPrefix(r.URL.Path, "/api/invitations/")
	if strings.HasSuffix(path, "/rsvps/summary") {
		invitationID := strings.Split(path, "/")[0]
		s.handleInvitationManagement(w, r, invitationID, "rsvp-summary")
		return
	}
	for _, resource := range []string{"rsvps", "wishes", "gifts"} {
		if strings.HasSuffix(path, "/"+resource) || strings.Contains(path, "/"+resource+"/") {
			invitationID := strings.Split(path, "/")[0]
			s.handleInvitationManagement(w, r, invitationID, resource)
			return
		}
	}
	if strings.HasSuffix(path, "/domains") || strings.Contains(path, "/domains/") {
		s.handleCustomDomains(w, r, strings.Split(path, "/")[0])
		return
	}
	if strings.HasSuffix(path, "/gift-transactions") || strings.Contains(path, "/gift-transactions/") {
		s.handleGiftTransactions(w, r, strings.Split(path, "/")[0])
		return
	}
	// Multi-event sub-resource: /events and /events/{id}
	if strings.HasSuffix(path, "/events") || strings.Contains(path, "/events/") {
		parts := strings.Split(path, "/")
		invitationID := parts[0]
		if len(parts) >= 3 && parts[1] == "events" {
			s.handleInvitationEventDetail(w, r, invitationID, parts[2])
		} else {
			s.handleInvitationEventsCollection(w, r, invitationID)
		}
		return
	}

	// Per-item deletes: /gallery/{id} and /stories/{id}
	if strings.Contains(path, "/gallery/") {
		parts := strings.Split(path, "/")
		if len(parts) >= 3 && parts[1] == "gallery" {
			s.handleGalleryItemDetail(w, r, parts[0], parts[2])
			return
		}
	}
	if strings.Contains(path, "/stories/") {
		parts := strings.Split(path, "/")
		if len(parts) >= 3 && parts[1] == "stories" {
			s.handleStoryItemDetail(w, r, parts[0], parts[2])
			return
		}
	}

	for _, resource := range []string{"settings", "stories", "gallery", "template"} {
		if strings.HasSuffix(path, "/"+resource) {
			s.handleInvitationContent(w, r, strings.Split(path, "/")[0], resource)
			return
		}
	}
	if strings.Contains(path, "/broadcast/") && strings.HasSuffix(path, "/confirm") {
		parts := strings.Split(path, "/")
		invitationID := parts[0]
		logID := parts[len(parts)-2]
		s.handleBroadcastConfirm(w, r, invitationID, logID)
		return
	}
	for _, resource := range []string{"broadcast", "media"} {
		if resource == "media" && strings.Contains(path, "/media/") {
			parts := strings.Split(path, "/")
			if len(parts) >= 3 {
				s.handleMediaDetail(w, r, parts[0], parts[2])
				return
			}
		}
		if strings.HasSuffix(path, "/"+resource) {
			s.handleOperations(w, r, strings.Split(path, "/")[0], resource)
			return
		}
	}
	// POST /api/invitations/{id}/duplicate
	if strings.HasSuffix(path, "/duplicate") {
		s.handleInvitationDuplicate(w, r)
		return
	}

	// DELETE /api/invitations/{id}/guests (bulk delete — only when method is DELETE with no trailing id)
	if strings.HasSuffix(path, "/guests") && r.Method == http.MethodDelete {
		s.handleBulkDeleteGuests(w, r)
		return
	}

	if strings.HasSuffix(path, "/guests") || strings.Contains(path, "/guests/") {
		invitationID := strings.Split(path, "/")[0]
		s.handleInvitationGuests(w, r, invitationID)
		return
	}

	claims, ok := s.requireAuth(w, r)
	if !ok {
		return
	}
	if path == "" || path == "/api/invitations" {
		writeJSON(w, http.StatusNotFound, map[string]string{"error": "invitation not found"})
		return
	}

	invitation, err := s.invitations.Owned(claims.UserID, path)
	if err != nil {
		writeJSON(w, http.StatusNotFound, map[string]string{"error": err.Error()})
		return
	}

	if r.Method == http.MethodGet {
		writeJSON(w, http.StatusOK, map[string]any{
			"id":          invitation.ID,
			"user_id":     invitation.UserID,
			"slug":        invitation.Slug,
			"title":       invitation.Title,
			"published":   invitation.Published,
			"template_id": invitation.TemplateID,
			"couple": map[string]any{
				"groom_name": invitation.Couple.GroomName,
				"bride_name": invitation.Couple.BrideName,
			},
			"event": map[string]any{
				"title":    invitation.Event.Title,
				"venue":    invitation.Event.Venue,
				"date":     invitation.Event.Date,
				"maps_url": invitation.Event.MapsURL,
			},
		})
		return
	}

	if r.Method == http.MethodPut {
		var payload struct {
			Slug      string            `json:"slug"`
			Title     string            `json:"title"`
			Published bool              `json:"published"`
			Couple    map[string]string `json:"couple"`
			Event     map[string]string `json:"event"`
		}
		if err := json.NewDecoder(r.Body).Decode(&payload); err != nil {
			writeJSON(w, http.StatusBadRequest, map[string]string{"error": "invalid payload"})
			return
		}

		couple := invitation.Couple
		if payload.Couple != nil {
			if groom, ok := payload.Couple["groom_name"]; ok {
				couple.GroomName = groom
			}
			if bride, ok := payload.Couple["bride_name"]; ok {
				couple.BrideName = bride
			}
		}

		event := invitation.Event
		if payload.Event != nil {
			if title, ok := payload.Event["title"]; ok {
				event.Title = title
			}
			if venue, ok := payload.Event["venue"]; ok {
				event.Venue = venue
			}
			if date, ok := payload.Event["date"]; ok {
				event.Date = date
			}
			if mapsURL, ok := payload.Event["maps_url"]; ok {
				event.MapsURL = mapsURL
			}
		}

		if payload.Slug == "" {
			payload.Slug = invitation.Slug
		}
		if payload.Title == "" {
			payload.Title = invitation.Title
		}

		wasPublished := invitation.Published
		updated, err := s.invitations.Update(claims.UserID, invitation.ID, payload.Slug, payload.Title, payload.Published, couple, event)
		if err != nil {
			status := http.StatusConflict
			if errors.Is(err, invitations.ErrInvalid) {
				status = http.StatusBadRequest
			}
			writeJSON(w, status, map[string]string{"error": err.Error()})
			return
		}
		if !wasPublished && updated.Published {
			_ = s.store.CreateAuditLog(claims.UserID, invitation.ID, "invitation.publish", nil)
		}

		writeJSON(w, http.StatusOK, map[string]any{
			"id":        updated.ID,
			"slug":      updated.Slug,
			"title":     updated.Title,
			"published": updated.Published,
			"couple": map[string]any{
				"groom_name": updated.Couple.GroomName,
				"bride_name": updated.Couple.BrideName,
			},
			"event": map[string]any{
				"title":    updated.Event.Title,
				"venue":    updated.Event.Venue,
				"date":     updated.Event.Date,
				"maps_url": updated.Event.MapsURL,
			},
		})
		return
	}

	if r.Method == http.MethodDelete {
		if err := s.invitations.Delete(claims.UserID, invitation.ID); err != nil {
			writeJSON(w, http.StatusNotFound, map[string]string{"error": err.Error()})
			return
		}
		_ = s.store.CreateAuditLog(claims.UserID, invitation.ID, "invitation.delete", nil)
		w.WriteHeader(http.StatusNoContent)
		return
	}

	writeJSON(w, http.StatusMethodNotAllowed, map[string]string{"error": "method not allowed"})
}

func (s *Server) requireAuth(w http.ResponseWriter, r *http.Request) (auth.TokenClaims, bool) {
	authorization := r.Header.Get("Authorization")
	if authorization == "" {
		writeJSON(w, http.StatusUnauthorized, map[string]string{"error": "missing authorization token"})
		return auth.TokenClaims{}, false
	}

	token := strings.TrimSpace(strings.TrimPrefix(authorization, "Bearer "))
	claims, ok := s.authenticateToken(token)
	if !ok {
		writeJSON(w, http.StatusUnauthorized, map[string]string{"error": "invalid token"})
		return auth.TokenClaims{}, false
	}
	return claims, true
}

func (s *Server) issueToken(user *store.User) (string, error) {
	if s.sessions != nil {
		token, _, err := s.sessions.Create(user.ID, user.Email, user.Role, 24*time.Hour)
		return token, err
	}
	return auth.GenerateToken(user.ID, user.Email, user.Role, s.config.JWTSecret), nil
}

func (s *Server) authenticateToken(token string) (auth.TokenClaims, bool) {
	if s.sessions != nil {
		claims, ok, err := s.sessions.Get(token)
		if err != nil || !ok {
			return auth.TokenClaims{}, false
		}
		return auth.TokenClaims{UserID: claims.UserID, Email: claims.Email, Role: claims.Role, Exp: claims.Exp}, true
	}
	if revoked, _ := s.revoker.IsRevoked(token); revoked {
		return auth.TokenClaims{}, false
	}
	return auth.ValidateToken(token, s.config.JWTSecret)
}

func (s *Server) requireAdmin(w http.ResponseWriter, r *http.Request) (auth.TokenClaims, bool) {
	claims, ok := s.requireAuth(w, r)
	if !ok {
		return claims, false
	}
	if claims.Role != "admin" {
		writeJSON(w, http.StatusForbidden, map[string]string{"error": "admin access required"})
		return claims, false
	}
	return claims, true
}

// canPreviewUnpublished lets an invitation's owner view it through the
// public read endpoints before it's published, so the dashboard preview
// page can reuse the same public rendering path for drafts.
func (s *Server) canPreviewUnpublished(r *http.Request, invitation *store.Invitation) bool {
	authorization := r.Header.Get("Authorization")
	if authorization == "" {
		return false
	}
	token := strings.TrimSpace(strings.TrimPrefix(authorization, "Bearer "))
	claims, ok := s.authenticateToken(token)
	return ok && claims.UserID == invitation.UserID
}

func (s *Server) handlePublicInvitation(w http.ResponseWriter, r *http.Request) {
	parts := strings.TrimPrefix(r.URL.Path, "/api/public/invitation/")
	if strings.HasSuffix(parts, "/rsvp") {
		s.handlePublicRSVP(w, r, strings.TrimSuffix(parts, "/rsvp"))
		return
	}
	if strings.HasSuffix(parts, "/wishes") {
		s.handlePublicWishes(w, r, strings.TrimSuffix(parts, "/wishes"))
		return
	}
	if strings.HasSuffix(parts, "/gifts") {
		invitationSlug := strings.TrimSuffix(parts, "/gifts")
		invitation, exists := s.store.FindInvitationBySlug(invitationSlug)
		if !exists || (!invitation.Published && !s.canPreviewUnpublished(r, invitation)) {
			writeJSON(w, http.StatusNotFound, map[string]string{"error": "invitation not found"})
			return
		}
		if r.Method != http.MethodGet {
			writeJSON(w, http.StatusMethodNotAllowed, map[string]string{"error": "method not allowed"})
			return
		}
		writeJSON(w, http.StatusOK, map[string]any{"items": s.store.ListActiveGifts(invitation.ID)})
		return
	}
	if strings.HasSuffix(parts, "/gift-transactions") {
		invitationSlug := strings.TrimSuffix(parts, "/gift-transactions")
		invitation, exists := s.store.FindInvitationBySlug(invitationSlug)
		if !exists || !invitation.Published {
			writeJSON(w, http.StatusNotFound, map[string]string{"error": "invitation not found"})
			return
		}
		if r.Method != http.MethodPost {
			writeJSON(w, http.StatusMethodNotAllowed, map[string]string{"error": "method not allowed"})
			return
		}
		var payload struct {
			GuestID    string  `json:"guest_id"`
			SenderName string  `json:"sender_name"`
			Message    string  `json:"message"`
			Amount     float64 `json:"amount"`
		}
		if json.NewDecoder(r.Body).Decode(&payload) != nil {
			writeJSON(w, http.StatusBadRequest, map[string]string{"error": "invalid payload"})
			return
		}
		tx, err := s.gifts.Create(invitation.ID, payload.GuestID, "dummy", payload.SenderName, payload.Message, payload.Amount)
		if err != nil {
			status := http.StatusBadRequest
			if errors.Is(err, giftservice.ErrNotFound) {
				status = http.StatusNotFound
			}
			writeJSON(w, status, map[string]string{"error": err.Error()})
			return
		}
		writeJSON(w, http.StatusCreated, tx)
		return
	}
	for _, resource := range []string{"gallery", "stories", "settings"} {
		if strings.HasSuffix(parts, "/"+resource) {
			s.handlePublicContent(w, r, strings.TrimSuffix(parts, "/"+resource), resource)
			return
		}
	}
	if r.Method != http.MethodGet {
		writeJSON(w, http.StatusMethodNotAllowed, map[string]string{"error": "method not allowed"})
		return
	}
	if parts == "" {
		writeJSON(w, http.StatusBadRequest, map[string]string{"error": "missing invitation slug"})
		return
	}
	invitation, exists := s.store.FindInvitationBySlug(parts)
	if !exists {
		invitation, exists = s.store.FindInvitationByCustomDomain(strings.ToLower(parts))
	}
	if !exists || (!invitation.Published && !s.canPreviewUnpublished(r, invitation)) {
		writeJSON(w, http.StatusNotFound, map[string]string{"error": "invitation not found"})
		return
	}
	watermark := true
	if plan, err := s.store.GetUserPlan(invitation.UserID); err == nil {
		watermark = plan.HasWatermark
	}
	writeJSON(w, http.StatusOK, map[string]any{
		"id":          invitation.ID,
		"slug":        invitation.Slug,
		"title":       invitation.Title,
		"watermark":   watermark,
		"template_id": invitation.TemplateID,
		"status":      map[string]bool{"published": invitation.Published},
		"couple": map[string]any{
			"groom_name": invitation.Couple.GroomName,
			"bride_name": invitation.Couple.BrideName,
		},
		"event": map[string]any{
			"title":    invitation.Event.Title,
			"venue":    invitation.Event.Venue,
			"date":     invitation.Event.Date,
			"maps_url": invitation.Event.MapsURL,
		},
		"sections": []string{"cover", "couple", "story", "event", "countdown", "location", "gallery", "rsvp", "wishes", "gift", "closing"},
	})
}

func (s *Server) handlePublicCurrent(w http.ResponseWriter, r *http.Request) {
	host := r.Host
	if parsed, _, err := net.SplitHostPort(host); err == nil {
		host = parsed
	}
	host = strings.ToLower(strings.TrimSpace(host))
	invitation, exists := s.store.FindInvitationByCustomDomain(host)
	if !exists {
		writeJSON(w, http.StatusNotFound, map[string]string{"error": "custom domain not found"})
		return
	}
	r2 := r.Clone(r.Context())
	r2.URL.Path = "/api/public/invitation/" + invitation.Slug
	s.handlePublicInvitation(w, r2)
}

func writeJSON(w http.ResponseWriter, status int, payload any) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(status)
	if w.Header().Get("X-API-Version") == "v1" {
		if status >= 400 {
			if fields, ok := payload.(map[string]string); ok {
				message := fields["error"]
				_ = json.NewEncoder(w).Encode(map[string]any{"error": map[string]any{"code": http.StatusText(status), "message": message}})
				return
			}
		}
		_ = json.NewEncoder(w).Encode(map[string]any{"data": payload, "meta": map[string]any{"request_id": w.Header().Get("X-Request-ID")}})
		return
	}
	_ = json.NewEncoder(w).Encode(payload)
}
