package store

import (
	"fmt"
	"sort"
	"strings"
	"sync"
	"time"
)

type Store interface {
	CreateUser(string, string, string) (*User, error)
	FindUserByEmail(string) (*User, bool)
	FindUserByID(string) (*User, bool)
	UpdateUser(string, string) (*User, error)
	UpdatePassword(string, string) error
	CreatePasswordResetToken(userID, tokenHash string, expiresAt time.Time) error
	ConsumePasswordResetToken(tokenHash string) (string, error)
	CreateInvitation(string, string, string) (*Invitation, error)
	ListInvitationsByUser(string) []*Invitation
	FindInvitationBySlug(string) (*Invitation, bool)
	FindInvitationByID(string) (*Invitation, bool)
	UpdateInvitation(string, string, string, bool, Couple, Event) (*Invitation, error)
	DeleteInvitation(string) error
	CreateGuest(string, string, string, string) (*Guest, error)
	ListGuests(string) []*Guest
	UpdateGuest(string, string, string, string) (*Guest, error)
	DeleteGuest(string) error
	CheckInGuest(id, actorUserID string) (*Guest, error)
	FindGuestByToken(invitationID, token string) (*Guest, bool)
	FindGuestByID(id string) (*Guest, bool)
	CreateRSVP(string, string, string, int, string) (*RSVP, error)
	UpsertRSVP(string, string, string, int, string) (*RSVP, error)
	ListRSVPs(string) []*RSVP
	RSVPSummary(string) map[string]int
	CreateWish(string, string, string, string) (*Wish, error)
	ListPublishedWishes(string) []*Wish
	ListWishes(string) []*Wish
	UpdateWishStatus(string, string) (*Wish, error)
	CreateGift(string, Gift) (*Gift, error)
	ListActiveGifts(string) []*Gift
	ListGifts(string) []*Gift
	SetGiftActive(id string, active bool) (*Gift, error)
	CreateGiftTransaction(GiftTransaction) (*GiftTransaction, error)
	ListGiftTransactions(invitationID string) []*GiftTransaction
	FindGiftTransactionByReference(reference string) (*GiftTransaction, bool)
	UpdateGiftTransactionStatus(id, status, reference string) (*GiftTransaction, error)
	ListTemplates() []*Template
	ListTemplatesAdmin() []*Template
	FindTemplate(id string) (*Template, bool)
	FindTemplateBySlug(slug string) (*Template, bool)
	CreateTemplate(Template) (*Template, error)
	UpdateTemplate(Template) (*Template, error)
	DeleteTemplate(id string) error
	SeedTemplates()
	AssignTemplate(string, string) error
	SeedPlans()
	SetUserPlan(userID, planID string) error
	GetUserPlan(userID string) (*Plan, error)
	CreateSubscription(Subscription) (*Subscription, error)
	FindSubscriptionByReference(reference string) (*Subscription, bool)
	GetActiveSubscription(userID string) (*Subscription, error)
	UpdateSubscriptionStatus(id, status string) (*Subscription, error)
	CancelActiveSubscriptions(userID string) error
	ListSubscriptions(userID string) []*Subscription
	CreateInvoice(Invoice) (*Invoice, error)
	ListInvoices(userID string) []*Invoice
	GetUserEntitlement(userID, feature string) (*Entitlement, bool)
	SetUserEntitlement(Entitlement) error
	CreateCustomDomain(CustomDomain) (*CustomDomain, error)
	ListCustomDomains(invitationID string) []*CustomDomain
	FindInvitationByCustomDomain(domain string) (*Invitation, bool)
	VerifyCustomDomain(id, userID, token string) (*CustomDomain, error)
	CreateAuditLog(userID, invitationID, action string, metadata map[string]any) error
	GetSettings(string) map[string]any
	UpdateSettings(string, map[string]any) map[string]any
	CreateStory(string, string, string) (map[string]any, error)
	ListStories(string) []map[string]any
	CreateGallery(string, string, string) (map[string]any, error)
	ListGallery(string) []map[string]any
	CreateBroadcastLog(invitationID, guestID, message, status string) (map[string]any, error)
	ListBroadcastLogs(string) []map[string]any
	LatestBroadcastLogForGuest(invitationID, guestID string) (map[string]any, bool)
	UpdateBroadcastLogStatus(id, status string) (map[string]any, error)
	CreateMedia(string, string, string, string, int64) (map[string]any, error)
	ListMedia(string) []map[string]any
	FindMedia(string) (map[string]any, bool)
	DeleteMedia(string) error
	UpdateUserRole(id, role string) (*User, error)
	ListPlans() []*Plan
	GetSiteContent(section string) map[string]any
	UpdateSiteContent(section string, data map[string]any) map[string]any
	ListFeatures() []map[string]any
	CreateFeature(title, description, icon string) (map[string]any, error)
	DeleteFeature(id string) error
	ListTestimonials() []map[string]any
	CreateTestimonial(name, role, quote, avatarURL string) (map[string]any, error)
	DeleteTestimonial(id string) error
	UpdateFeature(id, title, description, icon string) (map[string]any, error)
	UpdateTestimonial(id, name, role, quote, avatarURL string) (map[string]any, error)
	// Multi-event management
	CreateInvitationEvent(invitationID string, ev InvitationEvent) (*InvitationEvent, error)
	ListInvitationEvents(invitationID string) []*InvitationEvent
	UpdateInvitationEvent(id string, ev InvitationEvent) (*InvitationEvent, error)
	DeleteInvitationEvent(id string) error
	// Content item deletes
	DeleteGalleryItem(id string) error
	FindGalleryItem(id string) (map[string]any, bool)
	DeleteStoryItem(id string) error
	// Admin
	AdminListUsers() []*User
	AdminStats() map[string]any
	// SaaS operations
	DuplicateInvitation(sourceID, newSlug, newTitle, userID string) (*Invitation, error)
	BulkDeleteGuests(invitationID string, guestIDs []string) error
	ListGuestsFiltered(invitationID, search, category string) []*Guest
	UpdateUserAvatar(userID, avatarURL string) (*User, error)
}

type User struct {
	ID        string    `json:"id"`
	Name      string    `json:"name"`
	Email     string    `json:"email"`
	Password  string    `json:"-"`
	Role      string    `json:"role"`
	Avatar    string    `json:"avatar,omitempty"`
	CreatedAt time.Time `json:"created_at"`
}

type Couple struct {
	GroomName     string `json:"groom_name"`
	BrideName     string `json:"bride_name"`
	GroomNickname string `json:"groom_nickname,omitempty"`
	BrideNickname string `json:"bride_nickname,omitempty"`
	GroomPhoto    string `json:"groom_photo,omitempty"`
	BridePhoto    string `json:"bride_photo,omitempty"`
	GroomParents  string `json:"groom_parents,omitempty"`
	BrideParents  string `json:"bride_parents,omitempty"`
}

type Event struct {
	Title     string `json:"title"`
	Type      string `json:"type,omitempty"`
	Date      string `json:"date,omitempty"`
	StartTime string `json:"start_time,omitempty"`
	EndTime   string `json:"end_time,omitempty"`
	Venue     string `json:"venue,omitempty"`
	Address   string `json:"address,omitempty"`
	MapsURL   string `json:"maps_url,omitempty"`
}

type Invitation struct {
	ID          string     `json:"id"`
	UserID      string     `json:"user_id"`
	Slug        string     `json:"slug"`
	Title       string     `json:"title"`
	Published   bool       `json:"published"`
	TemplateID  string     `json:"template_id,omitempty"`
	Couple      Couple     `json:"couple"`
	Event       Event      `json:"event"`
	PublishedAt *time.Time `json:"published_at,omitempty"`
	UpdatedAt   time.Time  `json:"updated_at"`
	CreatedAt   time.Time  `json:"created_at"`
}

type Guest struct {
	ID           string     `json:"id"`
	InvitationID string     `json:"invitation_id"`
	Name         string     `json:"name"`
	Phone        string     `json:"phone,omitempty"`
	Category     string     `json:"category"`
	Token        string     `json:"token"`
	CheckedInAt  *time.Time `json:"checked_in_at,omitempty"`
	CheckedInBy  *string    `json:"checked_in_by,omitempty"`
	CreatedAt    time.Time  `json:"created_at"`
}

type RSVP struct {
	ID             string    `json:"id"`
	InvitationID   string    `json:"invitation_id"`
	GuestID        string    `json:"guest_id,omitempty"`
	Attendance     string    `json:"attendance"`
	AttendeesCount int       `json:"attendees_count"`
	Message        string    `json:"message,omitempty"`
	SubmittedAt    time.Time `json:"submitted_at"`
}

type Wish struct {
	ID           string    `json:"id"`
	InvitationID string    `json:"invitation_id"`
	GuestID      string    `json:"guest_id,omitempty"`
	Name         string    `json:"name"`
	Message      string    `json:"message"`
	Status       string    `json:"status"`
	CreatedAt    time.Time `json:"created_at"`
}

type Gift struct {
	ID              string    `json:"id"`
	InvitationID    string    `json:"invitation_id"`
	Type            string    `json:"type"`
	BankName        string    `json:"bank_name,omitempty"`
	AccountNumber   string    `json:"account_number,omitempty"`
	AccountName     string    `json:"account_name,omitempty"`
	EwalletProvider string    `json:"ewallet_provider,omitempty"`
	EwalletNumber   string    `json:"ewallet_number,omitempty"`
	QRISImageURL    string    `json:"qris_image_url,omitempty"`
	Address         string    `json:"address,omitempty"`
	Active          bool      `json:"is_active"`
	CreatedAt       time.Time `json:"created_at"`
}

type GiftTransaction struct {
	ID               string    `json:"id"`
	InvitationID     string    `json:"invitation_id"`
	GuestID          string    `json:"guest_id,omitempty"`
	Gateway          string    `json:"gateway"`
	GatewayReference string    `json:"gateway_reference_id,omitempty"`
	Amount           float64   `json:"amount"`
	Status           string    `json:"status"`
	SenderName       string    `json:"sender_name,omitempty"`
	Message          string    `json:"message,omitempty"`
	PaymentURL       string    `json:"payment_url,omitempty"`
	CreatedAt        time.Time `json:"created_at"`
}

type Plan struct {
	ID                      string  `json:"id"`
	Name                    string  `json:"name"`
	MaxGuests               int     `json:"max_guests"`
	HasWatermark            bool    `json:"has_watermark"`
	CustomDomainAllowed     bool    `json:"custom_domain_allowed"`
	PaymentGatewayAllowed   bool    `json:"payment_gateway_allowed"`
	PremiumTemplatesAllowed bool    `json:"premium_templates_allowed"`
	Price                   float64 `json:"price"`
	DurationDays            *int    `json:"duration_days,omitempty"`
}

type Subscription struct {
	ID                string     `json:"id"`
	UserID            string     `json:"user_id"`
	PlanID            string     `json:"plan_id"`
	Status            string     `json:"status"`
	Provider          string     `json:"provider"`
	ProviderReference string     `json:"provider_reference,omitempty"`
	StartedAt         time.Time  `json:"started_at"`
	EndsAt            *time.Time `json:"ends_at,omitempty"`
}

type CustomDomain struct {
	ID                string     `json:"id"`
	UserID            string     `json:"user_id"`
	InvitationID      string     `json:"invitation_id"`
	Domain            string     `json:"domain"`
	VerificationToken string     `json:"verification_token,omitempty"`
	Status            string     `json:"status"`
	VerifiedAt        *time.Time `json:"verified_at,omitempty"`
	CreatedAt         time.Time  `json:"created_at"`
}

type Entitlement struct {
	UserID    string     `json:"user_id"`
	Feature   string     `json:"feature"`
	Enabled   bool       `json:"enabled"`
	ExpiresAt *time.Time `json:"expires_at,omitempty"`
}

type Invoice struct {
	ID             string     `json:"id"`
	UserID         string     `json:"user_id"`
	SubscriptionID string     `json:"subscription_id"`
	InvoiceNumber  string     `json:"invoice_number"`
	Amount         float64    `json:"amount"`
	Status         string     `json:"status"`
	IssuedAt       time.Time  `json:"issued_at"`
	PaidAt         *time.Time `json:"paid_at,omitempty"`
}

type Template struct {
	ID            string    `json:"id"`
	Name          string    `json:"name"`
	Slug          string    `json:"slug"`
	Description   string    `json:"description,omitempty"`
	EventType     string    `json:"event_type"`
	Category      string    `json:"category"`
	Tags          []string  `json:"tags,omitempty"`
	PreviewImage  string    `json:"preview_image,omitempty"`
	PreviewURL    string    `json:"preview_url,omitempty"`
	Premium       bool      `json:"is_premium"`
	Price         float64   `json:"price"`
	Tier          string    `json:"tier"`
	SupportsPhoto bool      `json:"supports_photo"`
	SupportsMusic bool      `json:"supports_music"`
	SupportsRSVP  bool      `json:"supports_rsvp"`
	SupportsGift  bool      `json:"supports_gift"`
	SortOrder     int       `json:"sort_order"`
	Status        string    `json:"status"`
	CreatedAt     time.Time `json:"created_at,omitempty"`
	UpdatedAt     time.Time `json:"updated_at,omitempty"`
}

type InvitationEvent struct {
	ID           string    `json:"id"`
	InvitationID string    `json:"invitation_id"`
	Title        string    `json:"title"`
	Type         string    `json:"type"`
	Date         string    `json:"date"`
	StartTime    string    `json:"start_time,omitempty"`
	EndTime      string    `json:"end_time,omitempty"`
	Venue        string    `json:"venue"`
	Address      string    `json:"address,omitempty"`
	MapsURL      string    `json:"maps_url,omitempty"`
	Latitude     float64   `json:"latitude,omitempty"`
	Longitude    float64   `json:"longitude,omitempty"`
	SortOrder    int       `json:"sort_order"`
	CreatedAt    time.Time `json:"created_at"`
}

type MemoryStore struct {
	mu               sync.RWMutex
	users            map[string]*User
	invitations      map[string]*Invitation
	guests           map[string]*Guest
	rsvps            map[string]*RSVP
	wishes           map[string]*Wish
	gifts            map[string]*Gift
	templates        map[string]*Template
	settings         map[string]map[string]any
	stories          map[string][]map[string]any
	gallery          map[string][]map[string]any
	broadcasts       map[string][]map[string]any
	media            map[string][]map[string]any
	plans            map[string]*Plan
	userPlans        map[string]string
	auditLogs        []map[string]any
	siteContent      map[string]map[string]any
	features         map[string]map[string]any
	testimonials     map[string]map[string]any
	invitationEvents map[string][]*InvitationEvent
	passwordResets   map[string]passwordReset
	giftTransactions map[string]*GiftTransaction
	subscriptions    map[string]*Subscription
	customDomains    map[string]*CustomDomain
	entitlements     map[string]Entitlement
	invoices         map[string]*Invoice
}

type passwordReset struct {
	userID    string
	expiresAt time.Time
	used      bool
}

func NewMemoryStore() *MemoryStore {
	return &MemoryStore{
		users:            make(map[string]*User),
		invitations:      make(map[string]*Invitation),
		guests:           make(map[string]*Guest),
		rsvps:            make(map[string]*RSVP),
		wishes:           make(map[string]*Wish),
		gifts:            make(map[string]*Gift),
		templates:        make(map[string]*Template),
		settings:         make(map[string]map[string]any),
		stories:          make(map[string][]map[string]any),
		gallery:          make(map[string][]map[string]any),
		broadcasts:       make(map[string][]map[string]any),
		media:            make(map[string][]map[string]any),
		plans:            make(map[string]*Plan),
		userPlans:        make(map[string]string),
		siteContent:      make(map[string]map[string]any),
		features:         make(map[string]map[string]any),
		testimonials:     make(map[string]map[string]any),
		invitationEvents: make(map[string][]*InvitationEvent),
		passwordResets:   make(map[string]passwordReset),
		giftTransactions: make(map[string]*GiftTransaction),
		subscriptions:    make(map[string]*Subscription),
		customDomains:    make(map[string]*CustomDomain),
		entitlements:     make(map[string]Entitlement),
		invoices:         make(map[string]*Invoice),
	}
}

func (s *MemoryStore) CreateUser(name, email, password string) (*User, error) {
	s.mu.Lock()
	defer s.mu.Unlock()

	for _, user := range s.users {
		if user.Email == email {
			return nil, fmt.Errorf("email already exists")
		}
	}

	user := &User{
		ID:        fmt.Sprintf("user-%d", len(s.users)+1),
		Name:      name,
		Email:     email,
		Password:  password,
		Role:      "user",
		CreatedAt: time.Now().UTC(),
	}
	s.users[user.ID] = user
	return user, nil
}

func (s *MemoryStore) FindUserByEmail(email string) (*User, bool) {
	s.mu.RLock()
	defer s.mu.RUnlock()
	for _, user := range s.users {
		if user.Email == email {
			return user, true
		}
	}
	return nil, false
}

func (s *MemoryStore) FindUserByID(id string) (*User, bool) {
	s.mu.RLock()
	defer s.mu.RUnlock()
	user, ok := s.users[id]
	return user, ok
}

func (s *MemoryStore) UpdateUser(id, name string) (*User, error) {
	s.mu.Lock()
	defer s.mu.Unlock()
	user, ok := s.users[id]
	if !ok {
		return nil, fmt.Errorf("user not found")
	}
	if name != "" {
		user.Name = name
	}
	return user, nil
}

func (s *MemoryStore) UpdatePassword(id, password string) error {
	s.mu.Lock()
	defer s.mu.Unlock()
	user, ok := s.users[id]
	if !ok {
		return fmt.Errorf("user not found")
	}
	user.Password = password
	return nil
}

func (s *MemoryStore) CreatePasswordResetToken(userID, tokenHash string, expiresAt time.Time) error {
	s.mu.Lock()
	defer s.mu.Unlock()
	if _, ok := s.users[userID]; !ok {
		return fmt.Errorf("user not found")
	}
	s.passwordResets[tokenHash] = passwordReset{userID: userID, expiresAt: expiresAt}
	return nil
}

func (s *MemoryStore) ConsumePasswordResetToken(tokenHash string) (string, error) {
	s.mu.Lock()
	defer s.mu.Unlock()
	reset, ok := s.passwordResets[tokenHash]
	if !ok || reset.used || !time.Now().Before(reset.expiresAt) {
		return "", fmt.Errorf("invalid or expired reset token")
	}
	reset.used = true
	s.passwordResets[tokenHash] = reset
	return reset.userID, nil
}

func (s *MemoryStore) CreateInvitation(userID, slug, title string) (*Invitation, error) {
	s.mu.Lock()
	defer s.mu.Unlock()

	for _, invitation := range s.invitations {
		if invitation.Slug == slug {
			return nil, fmt.Errorf("slug already exists")
		}
	}

	invitation := &Invitation{
		ID:        fmt.Sprintf("inv-%d", len(s.invitations)+1),
		UserID:    userID,
		Slug:      slug,
		Title:     title,
		Published: false,
		CreatedAt: time.Now().UTC(),
	}
	s.invitations[invitation.ID] = invitation
	return invitation, nil
}

func (s *MemoryStore) ListInvitationsByUser(userID string) []*Invitation {
	s.mu.RLock()
	defer s.mu.RUnlock()

	items := make([]*Invitation, 0)
	for _, invitation := range s.invitations {
		if invitation.UserID == userID {
			items = append(items, invitation)
		}
	}
	return items
}

func (s *MemoryStore) FindInvitationBySlug(slug string) (*Invitation, bool) {
	s.mu.RLock()
	defer s.mu.RUnlock()
	for _, invitation := range s.invitations {
		if invitation.Slug == slug {
			return invitation, true
		}
	}
	return nil, false
}

func (s *MemoryStore) FindInvitationByID(id string) (*Invitation, bool) {
	s.mu.RLock()
	defer s.mu.RUnlock()

	invitation, ok := s.invitations[id]
	if !ok {
		return nil, false
	}
	return invitation, true
}

func (s *MemoryStore) UpdateInvitation(id string, slug string, title string, published bool, couple Couple, event Event) (*Invitation, error) {
	s.mu.Lock()
	defer s.mu.Unlock()

	invitation, ok := s.invitations[id]
	if !ok {
		return nil, fmt.Errorf("invitation not found")
	}

	if slug != "" {
		for _, other := range s.invitations {
			if other.ID != id && other.Slug == slug {
				return nil, fmt.Errorf("slug already exists")
			}
		}
		invitation.Slug = slug
	}
	if title != "" {
		invitation.Title = title
	}
	invitation.Published = published
	invitation.Couple = couple
	invitation.Event = event

	return invitation, nil
}

func (s *MemoryStore) DeleteInvitation(id string) error {
	s.mu.Lock()
	defer s.mu.Unlock()
	if _, ok := s.invitations[id]; !ok {
		return fmt.Errorf("invitation not found")
	}
	delete(s.invitations, id)
	for guestID, guest := range s.guests {
		if guest.InvitationID == id {
			delete(s.guests, guestID)
		}
	}
	for rsvpID, rsvp := range s.rsvps {
		if rsvp.InvitationID == id {
			delete(s.rsvps, rsvpID)
		}
	}
	for wishID, wish := range s.wishes {
		if wish.InvitationID == id {
			delete(s.wishes, wishID)
		}
	}
	for giftID, gift := range s.gifts {
		if gift.InvitationID == id {
			delete(s.gifts, giftID)
		}
	}
	return nil
}

func (s *MemoryStore) CreateGuest(invitationID, name, phone, category string) (*Guest, error) {
	s.mu.Lock()
	defer s.mu.Unlock()
	if _, ok := s.invitations[invitationID]; !ok {
		return nil, fmt.Errorf("invitation not found")
	}
	guest := &Guest{
		ID:           fmt.Sprintf("guest-%d", len(s.guests)+1),
		InvitationID: invitationID,
		Name:         name,
		Phone:        phone,
		Category:     category,
		Token:        fmt.Sprintf("guest-token-%d", len(s.guests)+1),
		CreatedAt:    time.Now().UTC(),
	}
	s.guests[guest.ID] = guest
	return guest, nil
}

func (s *MemoryStore) ListGuests(invitationID string) []*Guest {
	s.mu.RLock()
	defer s.mu.RUnlock()
	items := make([]*Guest, 0)
	for _, guest := range s.guests {
		if guest.InvitationID == invitationID {
			items = append(items, guest)
		}
	}
	return items
}

func (s *MemoryStore) UpdateGuest(id, name, phone, category string) (*Guest, error) {
	s.mu.Lock()
	defer s.mu.Unlock()
	guest, ok := s.guests[id]
	if !ok {
		return nil, fmt.Errorf("guest not found")
	}
	if name != "" {
		guest.Name = name
	}
	guest.Phone, guest.Category = phone, category
	return guest, nil
}

func (s *MemoryStore) DeleteGuest(id string) error {
	s.mu.Lock()
	defer s.mu.Unlock()
	if _, ok := s.guests[id]; !ok {
		return fmt.Errorf("guest not found")
	}
	delete(s.guests, id)
	for rsvpID, rsvp := range s.rsvps {
		if rsvp.GuestID == id {
			delete(s.rsvps, rsvpID)
		}
	}
	return nil
}

func (s *MemoryStore) CheckInGuest(id, actorUserID string) (*Guest, error) {
	s.mu.Lock()
	defer s.mu.Unlock()
	guest, ok := s.guests[id]
	if !ok {
		return nil, fmt.Errorf("guest not found")
	}
	now := time.Now().UTC()
	guest.CheckedInAt = &now
	guest.CheckedInBy = &actorUserID
	return guest, nil
}

func (s *MemoryStore) FindGuestByID(id string) (*Guest, bool) {
	s.mu.RLock()
	defer s.mu.RUnlock()
	guest, ok := s.guests[id]
	return guest, ok
}

func (s *MemoryStore) FindGuestByToken(invitationID, token string) (*Guest, bool) {
	s.mu.RLock()
	defer s.mu.RUnlock()
	for _, guest := range s.guests {
		if guest.InvitationID == invitationID && guest.Token == token {
			return guest, true
		}
	}
	return nil, false
}

func (s *MemoryStore) CreateRSVP(invitationID, guestID, attendance string, attendeesCount int, message string) (*RSVP, error) {
	s.mu.Lock()
	defer s.mu.Unlock()
	if _, ok := s.invitations[invitationID]; !ok {
		return nil, fmt.Errorf("invitation not found")
	}
	rsvp := &RSVP{
		ID:             fmt.Sprintf("rsvp-%d", len(s.rsvps)+1),
		InvitationID:   invitationID,
		GuestID:        guestID,
		Attendance:     attendance,
		AttendeesCount: attendeesCount,
		Message:        message,
		SubmittedAt:    time.Now().UTC(),
	}
	s.rsvps[rsvp.ID] = rsvp
	return rsvp, nil
}

func (s *MemoryStore) UpsertRSVP(invitationID, guestID, attendance string, attendeesCount int, message string) (*RSVP, error) {
	s.mu.Lock()
	defer s.mu.Unlock()
	if _, ok := s.invitations[invitationID]; !ok {
		return nil, fmt.Errorf("invitation not found")
	}
	if guestID != "" {
		for _, item := range s.rsvps {
			if item.InvitationID == invitationID && item.GuestID == guestID {
				item.Attendance, item.AttendeesCount, item.Message, item.SubmittedAt = attendance, attendeesCount, message, time.Now().UTC()
				return item, nil
			}
		}
	}
	rsvp := &RSVP{ID: fmt.Sprintf("rsvp-%d", len(s.rsvps)+1), InvitationID: invitationID, GuestID: guestID, Attendance: attendance, AttendeesCount: attendeesCount, Message: message, SubmittedAt: time.Now().UTC()}
	s.rsvps[rsvp.ID] = rsvp
	return rsvp, nil
}

func (s *MemoryStore) ListRSVPs(invitationID string) []*RSVP {
	s.mu.RLock()
	defer s.mu.RUnlock()
	items := make([]*RSVP, 0)
	for _, rsvp := range s.rsvps {
		if rsvp.InvitationID == invitationID {
			items = append(items, rsvp)
		}
	}
	return items
}

func (s *MemoryStore) RSVPSummary(invitationID string) map[string]int {
	s.mu.RLock()
	defer s.mu.RUnlock()
	summary := map[string]int{"yes": 0, "no": 0, "maybe": 0, "attendees": 0}
	for _, rsvp := range s.rsvps {
		if rsvp.InvitationID == invitationID {
			summary[rsvp.Attendance]++
			summary["attendees"] += rsvp.AttendeesCount
		}
	}
	return summary
}

func (s *MemoryStore) CreateWish(invitationID, guestID, name, message string) (*Wish, error) {
	s.mu.Lock()
	defer s.mu.Unlock()
	if _, ok := s.invitations[invitationID]; !ok {
		return nil, fmt.Errorf("invitation not found")
	}
	wish := &Wish{
		ID:           fmt.Sprintf("wish-%d", len(s.wishes)+1),
		InvitationID: invitationID,
		GuestID:      guestID,
		Name:         name,
		Message:      message,
		Status:       "pending",
		CreatedAt:    time.Now().UTC(),
	}
	s.wishes[wish.ID] = wish
	return wish, nil
}

func (s *MemoryStore) ListPublishedWishes(invitationID string) []*Wish {
	s.mu.RLock()
	defer s.mu.RUnlock()
	items := make([]*Wish, 0)
	for _, wish := range s.wishes {
		if wish.InvitationID == invitationID && wish.Status == "published" {
			items = append(items, wish)
		}
	}
	return items
}

func (s *MemoryStore) ListWishes(invitationID string) []*Wish {
	s.mu.RLock()
	defer s.mu.RUnlock()
	items := make([]*Wish, 0)
	for _, wish := range s.wishes {
		if wish.InvitationID == invitationID {
			items = append(items, wish)
		}
	}
	return items
}

func (s *MemoryStore) UpdateWishStatus(id, status string) (*Wish, error) {
	s.mu.Lock()
	defer s.mu.Unlock()
	wish, ok := s.wishes[id]
	if !ok {
		return nil, fmt.Errorf("wish not found")
	}
	if status != "pending" && status != "published" && status != "rejected" {
		return nil, fmt.Errorf("invalid wish status")
	}
	wish.Status = status
	return wish, nil
}

func (s *MemoryStore) CreateGift(invitationID string, gift Gift) (*Gift, error) {
	s.mu.Lock()
	defer s.mu.Unlock()
	if _, ok := s.invitations[invitationID]; !ok {
		return nil, fmt.Errorf("invitation not found")
	}
	gift.ID = fmt.Sprintf("gift-%d", len(s.gifts)+1)
	gift.InvitationID = invitationID
	gift.CreatedAt = time.Now().UTC()
	s.gifts[gift.ID] = &gift
	return &gift, nil
}

func (s *MemoryStore) ListActiveGifts(invitationID string) []*Gift {
	s.mu.RLock()
	defer s.mu.RUnlock()
	items := make([]*Gift, 0)
	for _, gift := range s.gifts {
		if gift.InvitationID == invitationID && gift.Active {
			items = append(items, gift)
		}
	}
	return items
}

func (s *MemoryStore) ListGifts(invitationID string) []*Gift {
	s.mu.RLock()
	defer s.mu.RUnlock()
	items := make([]*Gift, 0)
	for _, gift := range s.gifts {
		if gift.InvitationID == invitationID {
			items = append(items, gift)
		}
	}
	return items
}

func (s *MemoryStore) SetGiftActive(id string, active bool) (*Gift, error) {
	s.mu.Lock()
	defer s.mu.Unlock()
	gift, ok := s.gifts[id]
	if !ok {
		return nil, fmt.Errorf("gift not found")
	}
	gift.Active = active
	return gift, nil
}

func (s *MemoryStore) CreateGiftTransaction(tx GiftTransaction) (*GiftTransaction, error) {
	s.mu.Lock()
	defer s.mu.Unlock()
	if _, ok := s.invitations[tx.InvitationID]; !ok {
		return nil, fmt.Errorf("invitation not found")
	}
	tx.ID = fmt.Sprintf("gift-tx-%d", len(s.giftTransactions)+1)
	tx.CreatedAt = time.Now().UTC()
	s.giftTransactions[tx.ID] = &tx
	return &tx, nil
}

func (s *MemoryStore) ListGiftTransactions(invitationID string) []*GiftTransaction {
	s.mu.RLock()
	defer s.mu.RUnlock()
	items := make([]*GiftTransaction, 0)
	for _, tx := range s.giftTransactions {
		if tx.InvitationID == invitationID {
			items = append(items, tx)
		}
	}
	return items
}

func (s *MemoryStore) FindGiftTransactionByReference(reference string) (*GiftTransaction, bool) {
	s.mu.RLock()
	defer s.mu.RUnlock()
	for _, tx := range s.giftTransactions {
		if tx.GatewayReference == reference {
			return tx, true
		}
	}
	return nil, false
}

func (s *MemoryStore) UpdateGiftTransactionStatus(id, status, reference string) (*GiftTransaction, error) {
	s.mu.Lock()
	defer s.mu.Unlock()
	tx, ok := s.giftTransactions[id]
	if !ok {
		return nil, fmt.Errorf("gift transaction not found")
	}
	tx.Status, tx.GatewayReference = status, reference
	return tx, nil
}

func (s *MemoryStore) ListTemplates() []*Template {
	s.mu.RLock()
	defer s.mu.RUnlock()
	items := make([]*Template, 0, len(s.templates))
	for _, template := range s.templates {
		if template.Status == "active" {
			items = append(items, template)
		}
	}
	return items
}

func (s *MemoryStore) ListTemplatesAdmin() []*Template {
	s.mu.RLock()
	defer s.mu.RUnlock()
	items := make([]*Template, 0, len(s.templates))
	for _, item := range s.templates {
		items = append(items, item)
	}
	sort.Slice(items, func(i, j int) bool { return items[i].SortOrder < items[j].SortOrder })
	return items
}

func (s *MemoryStore) FindTemplate(id string) (*Template, bool) {
	s.mu.RLock()
	defer s.mu.RUnlock()
	item, ok := s.templates[id]
	return item, ok
}

func (s *MemoryStore) FindTemplateBySlug(slug string) (*Template, bool) {
	s.mu.RLock()
	defer s.mu.RUnlock()
	for _, item := range s.templates {
		if item.Slug == slug {
			return item, true
		}
	}
	return nil, false
}

func (s *MemoryStore) CreateTemplate(item Template) (*Template, error) {
	s.mu.Lock()
	defer s.mu.Unlock()
	if item.ID == "" {
		item.ID = fmt.Sprintf("template-%d", len(s.templates)+1)
	}
	if _, ok := s.templates[item.ID]; ok {
		return nil, fmt.Errorf("template already exists")
	}
	if item.Status == "" {
		item.Status = "draft"
	}
	if item.Tier == "" {
		item.Tier = "free"
	}
	item.CreatedAt = time.Now().UTC()
	item.UpdatedAt = item.CreatedAt
	s.templates[item.ID] = &item
	return &item, nil
}

func (s *MemoryStore) UpdateTemplate(item Template) (*Template, error) {
	s.mu.Lock()
	defer s.mu.Unlock()
	current, ok := s.templates[item.ID]
	if !ok {
		return nil, fmt.Errorf("template not found")
	}
	item.CreatedAt = current.CreatedAt
	item.UpdatedAt = time.Now().UTC()
	s.templates[item.ID] = &item
	return &item, nil
}

func (s *MemoryStore) DeleteTemplate(id string) error {
	s.mu.Lock()
	defer s.mu.Unlock()
	if _, ok := s.templates[id]; !ok {
		return fmt.Errorf("template not found")
	}
	delete(s.templates, id)
	return nil
}

func (s *MemoryStore) SeedTemplates() {
	s.mu.Lock()
	defer s.mu.Unlock()
	if len(s.templates) > 0 {
		return
	}
	defaults := []*Template{
		{ID: "alyra", Name: "Alyra", Slug: "alyra", Category: "editorial", EventType: "wedding", Tier: "free", PreviewImage: "/templates/alyra-preview.png", PreviewURL: "/invitation/demo?template=alyra", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 1},
		{ID: "weddings", Name: "Weddings", Slug: "weddings", Category: "modern", EventType: "wedding", Tier: "free", PreviewImage: "/templates/weddings-preview.png", PreviewURL: "/invitation/demo?template=weddings", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 2},
		{ID: "veloria", Name: "Veloria", Slug: "veloria", Category: "editorial", EventType: "wedding", Tier: "free", PreviewImage: "/templates/veloria-preview.png", PreviewURL: "/invitation/demo?template=veloria", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 3},
		{ID: "classic", Name: "Classic", Slug: "classic", EventType: "wedding", Category: "elegant", Tags: []string{"minimal", "elegant"}, Tier: "free", SupportsPhoto: true, SupportsRSVP: true, Status: "active", SortOrder: 10},
		{ID: "botanical", Name: "Botanical", Slug: "botanical", EventType: "wedding", Category: "nature", Tags: []string{"floral", "garden"}, Tier: "free", SupportsPhoto: true, SupportsMusic: true, SupportsRSVP: true, Status: "active", SortOrder: 20},
		{ID: "minimal", Name: "Minimal", Slug: "minimal", EventType: "wedding", Category: "modern", Tags: []string{"minimal", "clean"}, Tier: "free", SupportsPhoto: true, SupportsRSVP: true, Status: "active", SortOrder: 30},
		{ID: "aksara", Name: "Aksara", Slug: "aksara", EventType: "wedding", Category: "premium", Tags: []string{"adat", "heritage"}, Tier: "premium", Premium: true, SupportsPhoto: true, SupportsMusic: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 40},
	}
	for _, template := range defaults {
		s.templates[template.ID] = template
	}
}

func (s *MemoryStore) AssignTemplate(invitationID, templateID string) error {
	s.mu.Lock()
	defer s.mu.Unlock()
	invitation, ok := s.invitations[invitationID]
	if !ok {
		return fmt.Errorf("invitation not found")
	}
	if _, ok := s.templates[templateID]; !ok {
		return fmt.Errorf("template not found")
	}
	invitation.TemplateID = templateID
	return nil
}

func (s *MemoryStore) GetSettings(invitationID string) map[string]any {
	s.mu.RLock()
	defer s.mu.RUnlock()
	settings := s.settings[invitationID]
	if settings == nil {
		return map[string]any{"theme": "classic", "primary_color": "#d97706", "secondary_color": "#f59e0b", "font": "poppins", "autoplay_music": false}
	}
	copy := map[string]any{}
	for key, value := range settings {
		copy[key] = value
	}
	return copy
}

func (s *MemoryStore) UpdateSettings(invitationID string, settings map[string]any) map[string]any {
	s.mu.Lock()
	defer s.mu.Unlock()
	if s.settings[invitationID] == nil {
		s.settings[invitationID] = map[string]any{}
	}
	for key, value := range settings {
		s.settings[invitationID][key] = value
	}
	return s.settings[invitationID]
}

func (s *MemoryStore) CreateStory(invitationID, title, content string) (map[string]any, error) {
	s.mu.Lock()
	defer s.mu.Unlock()
	if _, ok := s.invitations[invitationID]; !ok {
		return nil, fmt.Errorf("invitation not found")
	}
	story := map[string]any{"id": fmt.Sprintf("story-%d", len(s.stories[invitationID])+1), "invitation_id": invitationID, "title": title, "content": content, "sort_order": len(s.stories[invitationID])}
	s.stories[invitationID] = append(s.stories[invitationID], story)
	return story, nil
}

func (s *MemoryStore) ListStories(invitationID string) []map[string]any {
	s.mu.RLock()
	defer s.mu.RUnlock()
	return append([]map[string]any{}, s.stories[invitationID]...)
}

func (s *MemoryStore) CreateGallery(invitationID, imageURL, caption string) (map[string]any, error) {
	s.mu.Lock()
	defer s.mu.Unlock()
	if _, ok := s.invitations[invitationID]; !ok {
		return nil, fmt.Errorf("invitation not found")
	}
	image := map[string]any{"id": fmt.Sprintf("media-%d", len(s.gallery[invitationID])+1), "invitation_id": invitationID, "image_url": imageURL, "caption": caption, "sort_order": len(s.gallery[invitationID])}
	s.gallery[invitationID] = append(s.gallery[invitationID], image)
	return image, nil
}

func (s *MemoryStore) ListGallery(invitationID string) []map[string]any {
	s.mu.RLock()
	defer s.mu.RUnlock()
	return append([]map[string]any{}, s.gallery[invitationID]...)
}

func (s *MemoryStore) CreateBroadcastLog(invitationID, guestID, message, status string) (map[string]any, error) {
	s.mu.Lock()
	defer s.mu.Unlock()
	if _, ok := s.invitations[invitationID]; !ok {
		return nil, fmt.Errorf("invitation not found")
	}
	log := map[string]any{"id": fmt.Sprintf("broadcast-%d", len(s.broadcasts[invitationID])+1), "invitation_id": invitationID, "guest_id": guestID, "channel": "whatsapp", "status": status, "message": message}
	s.broadcasts[invitationID] = append(s.broadcasts[invitationID], log)
	return log, nil
}

func (s *MemoryStore) ListBroadcastLogs(invitationID string) []map[string]any {
	s.mu.RLock()
	defer s.mu.RUnlock()
	return append([]map[string]any{}, s.broadcasts[invitationID]...)
}

func (s *MemoryStore) LatestBroadcastLogForGuest(invitationID, guestID string) (map[string]any, bool) {
	s.mu.RLock()
	defer s.mu.RUnlock()
	var latest map[string]any
	for _, log := range s.broadcasts[invitationID] {
		if log["guest_id"] == guestID {
			latest = log
		}
	}
	return latest, latest != nil
}

func (s *MemoryStore) UpdateBroadcastLogStatus(id, status string) (map[string]any, error) {
	s.mu.Lock()
	defer s.mu.Unlock()
	for _, logs := range s.broadcasts {
		for _, log := range logs {
			if log["id"] == id {
				log["status"] = status
				if status == "sent" {
					log["sent_at"] = time.Now().UTC()
				}
				return log, nil
			}
		}
	}
	return nil, fmt.Errorf("broadcast log not found")
}

func (s *MemoryStore) CreateMedia(invitationID, mediaType, path, mime string, size int64) (map[string]any, error) {
	s.mu.Lock()
	defer s.mu.Unlock()
	if _, ok := s.invitations[invitationID]; !ok {
		return nil, fmt.Errorf("invitation not found")
	}
	item := map[string]any{"id": fmt.Sprintf("media-%d", len(s.media[invitationID])+1), "invitation_id": invitationID, "type": mediaType, "path": path, "mime_type": mime, "size_bytes": size}
	s.media[invitationID] = append(s.media[invitationID], item)
	return item, nil
}

func (s *MemoryStore) ListMedia(invitationID string) []map[string]any {
	s.mu.RLock()
	defer s.mu.RUnlock()
	return append([]map[string]any{}, s.media[invitationID]...)
}

func (s *MemoryStore) FindMedia(id string) (map[string]any, bool) {
	s.mu.RLock()
	defer s.mu.RUnlock()
	for _, items := range s.media {
		for _, item := range items {
			if item["id"] == id {
				return item, true
			}
		}
	}
	return nil, false
}

func (s *MemoryStore) DeleteMedia(id string) error {
	s.mu.Lock()
	defer s.mu.Unlock()
	for invitationID, items := range s.media {
		for i, item := range items {
			if item["id"] == id {
				s.media[invitationID] = append(items[:i], items[i+1:]...)
				return nil
			}
		}
	}
	return fmt.Errorf("media not found")
}

func (s *MemoryStore) SeedPlans() {
	s.mu.Lock()
	defer s.mu.Unlock()
	if len(s.plans) > 0 {
		return
	}
	durationDays := 30
	s.plans["free"] = &Plan{
		ID:           "free",
		Name:         "Free",
		MaxGuests:    50,
		HasWatermark: true,
	}
	s.plans["pro"] = &Plan{
		ID:                      "pro",
		Name:                    "Pro",
		MaxGuests:               500,
		HasWatermark:            false,
		CustomDomainAllowed:     false,
		PremiumTemplatesAllowed: true,
		Price:                   99000,
		DurationDays:            &durationDays,
	}
	s.plans["premium"] = &Plan{
		ID:                      "premium",
		Name:                    "Premium",
		MaxGuests:               2000,
		HasWatermark:            false,
		CustomDomainAllowed:     true,
		PaymentGatewayAllowed:   true,
		PremiumTemplatesAllowed: true,
		Price:                   249000,
		DurationDays:            &durationDays,
	}
}

func (s *MemoryStore) SetUserPlan(userID, planID string) error {
	s.mu.Lock()
	defer s.mu.Unlock()
	if _, ok := s.users[userID]; !ok {
		return fmt.Errorf("user not found")
	}
	if _, ok := s.plans[planID]; !ok {
		return fmt.Errorf("plan not found")
	}
	s.userPlans[userID] = planID
	return nil
}

func (s *MemoryStore) GetUserPlan(userID string) (*Plan, error) {
	s.mu.RLock()
	defer s.mu.RUnlock()
	planID, ok := s.userPlans[userID]
	if !ok {
		planID = "free"
	}
	plan, ok := s.plans[planID]
	if !ok {
		return nil, fmt.Errorf("plan not found")
	}
	return plan, nil
}

func (s *MemoryStore) CreateSubscription(sub Subscription) (*Subscription, error) {
	s.mu.Lock()
	defer s.mu.Unlock()
	if _, ok := s.users[sub.UserID]; !ok {
		return nil, fmt.Errorf("user not found")
	}
	if _, ok := s.plans[sub.PlanID]; !ok {
		return nil, fmt.Errorf("plan not found")
	}
	sub.ID = fmt.Sprintf("sub-%d", len(s.subscriptions)+1)
	sub.StartedAt = time.Now().UTC()
	s.subscriptions[sub.ID] = &sub
	return &sub, nil
}

func (s *MemoryStore) FindSubscriptionByReference(reference string) (*Subscription, bool) {
	s.mu.RLock()
	defer s.mu.RUnlock()
	for _, sub := range s.subscriptions {
		if sub.ProviderReference == reference {
			return sub, true
		}
	}
	return nil, false
}

func (s *MemoryStore) GetActiveSubscription(userID string) (*Subscription, error) {
	s.mu.RLock()
	defer s.mu.RUnlock()
	for _, sub := range s.subscriptions {
		if sub.UserID == userID && sub.Status == "active" {
			return sub, nil
		}
	}
	return nil, fmt.Errorf("active subscription not found")
}

func (s *MemoryStore) UpdateSubscriptionStatus(id, status string) (*Subscription, error) {
	s.mu.Lock()
	defer s.mu.Unlock()
	sub, ok := s.subscriptions[id]
	if !ok {
		return nil, fmt.Errorf("subscription not found")
	}
	sub.Status = status
	return sub, nil
}

func (s *MemoryStore) CancelActiveSubscriptions(userID string) error {
	s.mu.Lock()
	defer s.mu.Unlock()
	for _, sub := range s.subscriptions {
		if sub.UserID == userID && sub.Status == "active" {
			sub.Status = "cancelled"
		}
	}
	return nil
}

func (s *MemoryStore) ListSubscriptions(userID string) []*Subscription {
	s.mu.RLock()
	defer s.mu.RUnlock()
	items := make([]*Subscription, 0)
	for _, sub := range s.subscriptions {
		if sub.UserID == userID {
			items = append(items, sub)
		}
	}
	sort.Slice(items, func(i, j int) bool { return items[i].StartedAt.After(items[j].StartedAt) })
	return items
}

func (s *MemoryStore) CreateInvoice(invoice Invoice) (*Invoice, error) {
	s.mu.Lock()
	defer s.mu.Unlock()
	if _, ok := s.users[invoice.UserID]; !ok {
		return nil, fmt.Errorf("user not found")
	}
	invoice.ID = fmt.Sprintf("invoice-%d", len(s.invoices)+1)
	invoice.IssuedAt = time.Now().UTC()
	s.invoices[invoice.ID] = &invoice
	return &invoice, nil
}

func (s *MemoryStore) ListInvoices(userID string) []*Invoice {
	s.mu.RLock()
	defer s.mu.RUnlock()
	items := make([]*Invoice, 0)
	for _, invoice := range s.invoices {
		if invoice.UserID == userID {
			items = append(items, invoice)
		}
	}
	sort.Slice(items, func(i, j int) bool { return items[i].IssuedAt.After(items[j].IssuedAt) })
	return items
}

func (s *MemoryStore) GetUserEntitlement(userID, feature string) (*Entitlement, bool) {
	s.mu.RLock()
	defer s.mu.RUnlock()
	item, ok := s.entitlements[userID+":"+feature]
	if !ok || (item.ExpiresAt != nil && !time.Now().Before(*item.ExpiresAt)) {
		return nil, false
	}
	return &item, true
}

func (s *MemoryStore) SetUserEntitlement(item Entitlement) error {
	s.mu.Lock()
	defer s.mu.Unlock()
	if _, ok := s.users[item.UserID]; !ok {
		return fmt.Errorf("user not found")
	}
	s.entitlements[item.UserID+":"+item.Feature] = item
	return nil
}

func (s *MemoryStore) CreateCustomDomain(domain CustomDomain) (*CustomDomain, error) {
	s.mu.Lock()
	defer s.mu.Unlock()
	for _, item := range s.customDomains {
		if item.Domain == domain.Domain {
			return nil, fmt.Errorf("domain already exists")
		}
	}
	domain.ID = fmt.Sprintf("domain-%d", len(s.customDomains)+1)
	domain.CreatedAt = time.Now().UTC()
	domain.Status = "pending"
	s.customDomains[domain.ID] = &domain
	return &domain, nil
}

func (s *MemoryStore) ListCustomDomains(invitationID string) []*CustomDomain {
	s.mu.RLock()
	defer s.mu.RUnlock()
	items := make([]*CustomDomain, 0)
	for _, item := range s.customDomains {
		if item.InvitationID == invitationID {
			items = append(items, item)
		}
	}
	return items
}

func (s *MemoryStore) FindInvitationByCustomDomain(domain string) (*Invitation, bool) {
	s.mu.RLock()
	defer s.mu.RUnlock()
	for _, item := range s.customDomains {
		if item.Domain == domain && item.Status == "verified" {
			inv, ok := s.invitations[item.InvitationID]
			return inv, ok
		}
	}
	return nil, false
}

func (s *MemoryStore) VerifyCustomDomain(id, userID, token string) (*CustomDomain, error) {
	s.mu.Lock()
	defer s.mu.Unlock()
	item, ok := s.customDomains[id]
	if !ok || item.UserID != userID {
		return nil, fmt.Errorf("domain not found")
	}
	if item.VerificationToken != token {
		return nil, fmt.Errorf("invalid verification token")
	}
	now := time.Now().UTC()
	item.Status, item.VerifiedAt = "verified", &now
	return item, nil
}

func (s *MemoryStore) CreateAuditLog(userID, invitationID, action string, metadata map[string]any) error {
	s.mu.Lock()
	defer s.mu.Unlock()
	s.auditLogs = append(s.auditLogs, map[string]any{
		"id":            fmt.Sprintf("audit-%d", len(s.auditLogs)+1),
		"user_id":       userID,
		"invitation_id": invitationID,
		"action":        action,
		"metadata":      metadata,
		"created_at":    time.Now().UTC(),
	})
	return nil
}

func (s *MemoryStore) UpdateUserRole(id, role string) (*User, error) {
	s.mu.Lock()
	defer s.mu.Unlock()
	user, ok := s.users[id]
	if !ok {
		return nil, fmt.Errorf("user not found")
	}
	user.Role = role
	return user, nil
}

func (s *MemoryStore) ListPlans() []*Plan {
	s.mu.RLock()
	defer s.mu.RUnlock()
	items := make([]*Plan, 0, len(s.plans))
	for _, plan := range s.plans {
		items = append(items, plan)
	}
	return items
}

func (s *MemoryStore) GetSiteContent(section string) map[string]any {
	s.mu.RLock()
	defer s.mu.RUnlock()
	content := s.siteContent[section]
	if content == nil {
		return map[string]any{}
	}
	copy := map[string]any{}
	for key, value := range content {
		copy[key] = value
	}
	return copy
}

func (s *MemoryStore) UpdateSiteContent(section string, data map[string]any) map[string]any {
	s.mu.Lock()
	defer s.mu.Unlock()
	if s.siteContent[section] == nil {
		s.siteContent[section] = map[string]any{}
	}
	for key, value := range data {
		s.siteContent[section][key] = value
	}
	return s.siteContent[section]
}

func (s *MemoryStore) ListFeatures() []map[string]any {
	s.mu.RLock()
	defer s.mu.RUnlock()
	items := make([]map[string]any, 0, len(s.features))
	for _, feature := range s.features {
		items = append(items, feature)
	}
	return items
}

func (s *MemoryStore) CreateFeature(title, description, icon string) (map[string]any, error) {
	s.mu.Lock()
	defer s.mu.Unlock()
	feature := map[string]any{
		"id":          fmt.Sprintf("feature-%d", len(s.features)+1),
		"title":       title,
		"description": description,
		"icon":        icon,
		"sort_order":  len(s.features),
	}
	s.features[feature["id"].(string)] = feature
	return feature, nil
}

func (s *MemoryStore) DeleteFeature(id string) error {
	s.mu.Lock()
	defer s.mu.Unlock()
	if _, ok := s.features[id]; !ok {
		return fmt.Errorf("feature not found")
	}
	delete(s.features, id)
	return nil
}

func (s *MemoryStore) ListTestimonials() []map[string]any {
	s.mu.RLock()
	defer s.mu.RUnlock()
	items := make([]map[string]any, 0, len(s.testimonials))
	for _, testimonial := range s.testimonials {
		items = append(items, testimonial)
	}
	return items
}

func (s *MemoryStore) CreateTestimonial(name, role, quote, avatarURL string) (map[string]any, error) {
	s.mu.Lock()
	defer s.mu.Unlock()
	testimonial := map[string]any{
		"id":         fmt.Sprintf("testimonial-%d", len(s.testimonials)+1),
		"name":       name,
		"role":       role,
		"quote":      quote,
		"avatar_url": avatarURL,
		"sort_order": len(s.testimonials),
	}
	s.testimonials[testimonial["id"].(string)] = testimonial
	return testimonial, nil
}

func (s *MemoryStore) DeleteTestimonial(id string) error {
	s.mu.Lock()
	defer s.mu.Unlock()
	if _, ok := s.testimonials[id]; !ok {
		return fmt.Errorf("testimonial not found")
	}
	delete(s.testimonials, id)
	return nil
}

func (s *MemoryStore) UpdateFeature(id, title, description, icon string) (map[string]any, error) {
	s.mu.Lock()
	defer s.mu.Unlock()
	f, ok := s.features[id]
	if !ok {
		return nil, fmt.Errorf("feature not found")
	}
	if title != "" {
		f["title"] = title
	}
	if description != "" {
		f["description"] = description
	}
	f["icon"] = icon
	return f, nil
}

func (s *MemoryStore) UpdateTestimonial(id, name, role, quote, avatarURL string) (map[string]any, error) {
	s.mu.Lock()
	defer s.mu.Unlock()
	t, ok := s.testimonials[id]
	if !ok {
		return nil, fmt.Errorf("testimonial not found")
	}
	if name != "" {
		t["name"] = name
	}
	if quote != "" {
		t["quote"] = quote
	}
	t["role"] = role
	t["avatar_url"] = avatarURL
	return t, nil
}

func (s *MemoryStore) CreateInvitationEvent(invitationID string, ev InvitationEvent) (*InvitationEvent, error) {
	s.mu.Lock()
	defer s.mu.Unlock()
	ev.ID = fmt.Sprintf("ev-%d", time.Now().UnixNano())
	ev.InvitationID = invitationID
	ev.CreatedAt = time.Now()
	s.invitationEvents[invitationID] = append(s.invitationEvents[invitationID], &ev)
	return &ev, nil
}

func (s *MemoryStore) ListInvitationEvents(invitationID string) []*InvitationEvent {
	s.mu.RLock()
	defer s.mu.RUnlock()
	items := s.invitationEvents[invitationID]
	if items == nil {
		return []*InvitationEvent{}
	}
	result := make([]*InvitationEvent, len(items))
	copy(result, items)
	sort.Slice(result, func(i, j int) bool {
		return result[i].SortOrder < result[j].SortOrder
	})
	return result
}

func (s *MemoryStore) UpdateInvitationEvent(id string, ev InvitationEvent) (*InvitationEvent, error) {
	s.mu.Lock()
	defer s.mu.Unlock()
	for _, events := range s.invitationEvents {
		for i, e := range events {
			if e.ID == id {
				ev.ID = id
				ev.InvitationID = e.InvitationID
				ev.CreatedAt = e.CreatedAt
				events[i] = &ev
				return &ev, nil
			}
		}
	}
	return nil, fmt.Errorf("event not found")
}

func (s *MemoryStore) DeleteInvitationEvent(id string) error {
	s.mu.Lock()
	defer s.mu.Unlock()
	for invID, events := range s.invitationEvents {
		for i, e := range events {
			if e.ID == id {
				s.invitationEvents[invID] = append(events[:i], events[i+1:]...)
				return nil
			}
		}
	}
	return fmt.Errorf("event not found")
}

func (s *MemoryStore) DeleteGalleryItem(id string) error {
	s.mu.Lock()
	defer s.mu.Unlock()
	for invID, items := range s.gallery {
		for i, item := range items {
			if item["id"] == id {
				s.gallery[invID] = append(items[:i], items[i+1:]...)
				return nil
			}
		}
	}
	return fmt.Errorf("gallery item not found")
}

func (s *MemoryStore) FindGalleryItem(id string) (map[string]any, bool) {
	s.mu.RLock()
	defer s.mu.RUnlock()
	for _, items := range s.gallery {
		for _, item := range items {
			if item["id"] == id {
				return item, true
			}
		}
	}
	return nil, false
}

func (s *MemoryStore) DeleteStoryItem(id string) error {
	s.mu.Lock()
	defer s.mu.Unlock()
	for invID, items := range s.stories {
		for i, item := range items {
			if item["id"] == id {
				s.stories[invID] = append(items[:i], items[i+1:]...)
				return nil
			}
		}
	}
	return fmt.Errorf("story not found")
}

func (s *MemoryStore) AdminListUsers() []*User {
	s.mu.RLock()
	defer s.mu.RUnlock()
	items := make([]*User, 0, len(s.users))
	for _, u := range s.users {
		items = append(items, u)
	}
	sort.Slice(items, func(i, j int) bool {
		return items[i].CreatedAt.After(items[j].CreatedAt)
	})
	return items
}

func (s *MemoryStore) AdminStats() map[string]any {
	s.mu.RLock()
	defer s.mu.RUnlock()
	published := 0
	for _, inv := range s.invitations {
		if inv.Published {
			published++
		}
	}
	return map[string]any{
		"total_users":           len(s.users),
		"total_invitations":     len(s.invitations),
		"published_invitations": published,
		"total_guests":          len(s.guests),
		"total_rsvps":           len(s.rsvps),
		"total_wishes":          len(s.wishes),
	}
}

func (s *MemoryStore) DuplicateInvitation(sourceID, newSlug, newTitle, userID string) (*Invitation, error) {
	s.mu.Lock()
	defer s.mu.Unlock()
	src, ok := s.invitations[sourceID]
	if !ok {
		return nil, fmt.Errorf("invitation not found")
	}
	for _, inv := range s.invitations {
		if inv.Slug == newSlug {
			return nil, fmt.Errorf("slug already taken")
		}
	}
	newID := fmt.Sprintf("inv-%d", time.Now().UnixNano())
	now := time.Now()
	newInv := &Invitation{
		ID:         newID,
		UserID:     userID,
		Slug:       newSlug,
		Title:      newTitle,
		Published:  false,
		TemplateID: src.TemplateID,
		Couple:     src.Couple,
		Event:      src.Event,
		UpdatedAt:  now,
		CreatedAt:  now,
	}
	s.invitations[newID] = newInv
	if srcSettings, ok := s.settings[sourceID]; ok {
		newSettings := make(map[string]any, len(srcSettings))
		for k, v := range srcSettings {
			newSettings[k] = v
		}
		s.settings[newID] = newSettings
	}
	if srcStories, ok := s.stories[sourceID]; ok {
		newStories := make([]map[string]any, len(srcStories))
		copy(newStories, srcStories)
		s.stories[newID] = newStories
	}
	if srcGallery, ok := s.gallery[sourceID]; ok {
		newGallery := make([]map[string]any, len(srcGallery))
		copy(newGallery, srcGallery)
		s.gallery[newID] = newGallery
	}
	for _, gift := range s.gifts {
		if gift.InvitationID == sourceID {
			g := *gift
			g.ID = fmt.Sprintf("gift-%d", time.Now().UnixNano())
			g.InvitationID = newID
			g.CreatedAt = now
			s.gifts[g.ID] = &g
		}
	}
	return newInv, nil
}

func (s *MemoryStore) BulkDeleteGuests(invitationID string, guestIDs []string) error {
	s.mu.Lock()
	defer s.mu.Unlock()
	idSet := make(map[string]bool, len(guestIDs))
	for _, id := range guestIDs {
		idSet[id] = true
	}
	for id, guest := range s.guests {
		if guest.InvitationID == invitationID && idSet[id] {
			delete(s.guests, id)
		}
	}
	return nil
}

func (s *MemoryStore) ListGuestsFiltered(invitationID, search, category string) []*Guest {
	s.mu.RLock()
	defer s.mu.RUnlock()
	searchLower := strings.ToLower(search)
	items := make([]*Guest, 0)
	for _, g := range s.guests {
		if g.InvitationID != invitationID {
			continue
		}
		if category != "" && g.Category != category {
			continue
		}
		if search != "" {
			if !strings.Contains(strings.ToLower(g.Name), searchLower) &&
				!strings.Contains(g.Phone, search) {
				continue
			}
		}
		items = append(items, g)
	}
	sort.Slice(items, func(i, j int) bool {
		return items[i].CreatedAt.After(items[j].CreatedAt)
	})
	return items
}

func (s *MemoryStore) UpdateUserAvatar(userID, avatarURL string) (*User, error) {
	s.mu.Lock()
	defer s.mu.Unlock()
	user, ok := s.users[userID]
	if !ok {
		return nil, fmt.Errorf("user not found")
	}
	user.Avatar = avatarURL
	return user, nil
}
