package store

import (
	"encoding/json"
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
	// PasswordChangedAt is when the password was last changed/reset (tokens issued earlier are invalid).
	PasswordChangedAt(userID string) (time.Time, bool)
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
	SetGuestTable(id, table string) (*Guest, error)
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
	CreateLedgerEntry(LedgerEntry) (*LedgerEntry, error)
	ListLedger(invitationID string) []*LedgerEntry
	UpdateLedgerEntry(LedgerEntry) (*LedgerEntry, error)
	DeleteLedgerEntry(invitationID, id string) error
	CreateGuestPhoto(GuestPhoto) (*GuestPhoto, error)
	ListGuestPhotos(invitationID, status string) []*GuestPhoto
	UpdateGuestPhotoStatus(invitationID, id, status string) (*GuestPhoto, error)
	GetPrivateData(invitationID, key string) map[string]any
	SetPrivateData(invitationID, key string, data map[string]any) error
	CreateMember(Member) (*Member, error)
	ListMembers(invitationID string) []*Member
	FindMember(id string) (*Member, bool)
	FindMemberByTokenHash(hash string) (*Member, bool)
	FindMembership(invitationID, userID string) (*Member, bool)
	ListMembershipsByUser(userID string) []*Member
	UpdateMember(Member) (*Member, error)
	DeleteMember(id string) error
	CreateGiftPayout(GiftPayout) (*GiftPayout, error)
	ListGiftPayouts(invitationID string) []*GiftPayout
	ListAllGiftPayouts(status string) []*GiftPayout
	FindGiftPayout(id string) (*GiftPayout, bool)
	UpdateGiftPayout(id, status, note string) (*GiftPayout, error)
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
	// ActivateSubscription marks it active from now until endsAt (nil = no expiry).
	ActivateSubscription(id string, endsAt *time.Time) (*Subscription, error)
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
	DeleteCustomDomain(id, userID string) error
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
	SavePlan(plan Plan) (*Plan, error)
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
	UpdateStory(id, title, content, date, image string) (map[string]any, error)
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
	Table        string     `json:"table"`
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
	Purpose          string    `json:"purpose,omitempty"` // e.g. "wishlist:<item id>" for a crowdfunded gift
	CreatedAt        time.Time `json:"created_at"`
}

// Member is someone the owner invited to help with one invitation, with a limited role.
type Member struct {
	ID           string     `json:"id"`
	InvitationID string     `json:"invitation_id"`
	UserID       string     `json:"user_id,omitempty"`
	Email        string     `json:"email,omitempty"`
	Role         string     `json:"role"`   // editor, organizer, receptionist
	Status       string     `json:"status"` // pending, active
	TokenHash    string     `json:"-"`
	InvitedBy    string     `json:"invited_by,omitempty"`
	ExpiresAt    *time.Time `json:"expires_at,omitempty"`
	CreatedAt    time.Time  `json:"created_at"`
	AcceptedAt   *time.Time `json:"accepted_at,omitempty"`
}

// LedgerEntry is one line of the "buku buwuh": who gave what, so the family can reciprocate later.
type LedgerEntry struct {
	ID           string    `json:"id"`
	InvitationID string    `json:"invitation_id"`
	GuestID      string    `json:"guest_id,omitempty"`
	Name         string    `json:"name"`
	Kind         string    `json:"kind"` // cash, transfer, kado, online
	Amount       float64   `json:"amount"`
	Item         string    `json:"item,omitempty"`
	Note         string    `json:"note,omitempty"`
	RecordedBy   string    `json:"recorded_by,omitempty"`
	CreatedAt    time.Time `json:"created_at"`
}

// GuestPhoto is a photo uploaded by a guest from the invitation (scan QR on the table).
type GuestPhoto struct {
	ID           string    `json:"id"`
	InvitationID string    `json:"invitation_id"`
	GuestID      string    `json:"guest_id,omitempty"`
	UploaderName string    `json:"uploader_name,omitempty"`
	URL          string    `json:"url"`
	Status       string    `json:"status"` // approved, pending, hidden
	CreatedAt    time.Time `json:"created_at"`
}

// GiftPayout is a couple's request to withdraw online envelopes held by Rawuh.
type GiftPayout struct {
	ID            string     `json:"id"`
	InvitationID  string     `json:"invitation_id"`
	UserID        string     `json:"user_id"`
	Amount        float64    `json:"amount"`
	BankName      string     `json:"bank_name"`
	AccountNumber string     `json:"account_number"`
	AccountName   string     `json:"account_name"`
	Status        string     `json:"status"` // requested, paid, rejected
	Note          string     `json:"note,omitempty"`
	CreatedAt     time.Time  `json:"created_at"`
	ProcessedAt   *time.Time `json:"processed_at,omitempty"`
}

type Plan struct {
	ID                      string  `json:"id"`
	Name                    string  `json:"name"`
	MaxGuests               int     `json:"max_guests"`
	MaxTeamMembers          int     `json:"max_team_members"` // 0 = unlimited
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
	passwordChanged  map[string]time.Time
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
	giftPayouts      map[string]*GiftPayout
	ledger           map[string]*LedgerEntry
	members          map[string]*Member
	guestPhotos      map[string]*GuestPhoto
	private          map[string]map[string]any
	seq              int
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
		giftPayouts:      make(map[string]*GiftPayout),
		ledger:           make(map[string]*LedgerEntry),
		members:          make(map[string]*Member),
		guestPhotos:      make(map[string]*GuestPhoto),
		private:          make(map[string]map[string]any),
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
	if s.passwordChanged == nil {
		s.passwordChanged = map[string]time.Time{}
	}
	s.passwordChanged[id] = time.Now()
	return nil
}

func (s *MemoryStore) PasswordChangedAt(userID string) (time.Time, bool) {
	s.mu.RLock()
	defer s.mu.RUnlock()
	at, ok := s.passwordChanged[userID]
	return at, ok
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
	if guest.CheckedInAt == nil { // keep the first check-in time
		now := time.Now().UTC()
		guest.CheckedInAt = &now
		guest.CheckedInBy = &actorUserID
	}
	return guest, nil
}

func (s *MemoryStore) FindGuestByID(id string) (*Guest, bool) {
	s.mu.RLock()
	defer s.mu.RUnlock()
	guest, ok := s.guests[id]
	return guest, ok
}

func (s *MemoryStore) SetGuestTable(id, table string) (*Guest, error) {
	s.mu.Lock()
	defer s.mu.Unlock()
	guest, ok := s.guests[id]
	if !ok {
		return nil, fmt.Errorf("guest not found")
	}
	guest.Table = table
	return guest, nil
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
	sort.Slice(items, func(i, j int) bool { return items[i].CreatedAt.After(items[j].CreatedAt) })
	return items
}

func (s *MemoryStore) nextID(prefix string) string {
	s.seq++
	return fmt.Sprintf("%s-%d", prefix, s.seq)
}

func (s *MemoryStore) CreateMember(m Member) (*Member, error) {
	s.mu.Lock()
	defer s.mu.Unlock()
	if _, ok := s.invitations[m.InvitationID]; !ok {
		return nil, fmt.Errorf("invitation not found")
	}
	for _, existing := range s.members {
		if m.UserID != "" && existing.InvitationID == m.InvitationID && existing.UserID == m.UserID {
			return nil, fmt.Errorf("already a member")
		}
	}
	m.ID = s.nextID("member")
	m.CreatedAt = time.Now().UTC()
	s.members[m.ID] = &m
	out := m
	return &out, nil
}

func (s *MemoryStore) findMembers(keep func(*Member) bool) []*Member {
	s.mu.RLock()
	defer s.mu.RUnlock()
	items := make([]*Member, 0)
	for _, m := range s.members {
		if keep(m) {
			out := *m
			items = append(items, &out)
		}
	}
	sort.Slice(items, func(i, j int) bool { return items[i].CreatedAt.Before(items[j].CreatedAt) })
	return items
}

func (s *MemoryStore) ListMembers(invitationID string) []*Member {
	return s.findMembers(func(m *Member) bool { return m.InvitationID == invitationID })
}

func (s *MemoryStore) FindMember(id string) (*Member, bool) {
	items := s.findMembers(func(m *Member) bool { return m.ID == id })
	if len(items) == 0 {
		return nil, false
	}
	return items[0], true
}

func (s *MemoryStore) FindMemberByTokenHash(hash string) (*Member, bool) {
	items := s.findMembers(func(m *Member) bool { return hash != "" && m.TokenHash == hash })
	if len(items) == 0 {
		return nil, false
	}
	return items[0], true
}

func (s *MemoryStore) FindMembership(invitationID, userID string) (*Member, bool) {
	items := s.findMembers(func(m *Member) bool {
		return m.InvitationID == invitationID && userID != "" && m.UserID == userID && m.Status == "active"
	})
	if len(items) == 0 {
		return nil, false
	}
	return items[0], true
}

func (s *MemoryStore) ListMembershipsByUser(userID string) []*Member {
	return s.findMembers(func(m *Member) bool { return userID != "" && m.UserID == userID && m.Status == "active" })
}

func (s *MemoryStore) UpdateMember(m Member) (*Member, error) {
	s.mu.Lock()
	defer s.mu.Unlock()
	current, ok := s.members[m.ID]
	if !ok {
		return nil, fmt.Errorf("member not found")
	}
	for _, existing := range s.members {
		if m.UserID != "" && existing.ID != m.ID && existing.InvitationID == current.InvitationID && existing.UserID == m.UserID {
			return nil, fmt.Errorf("already a member")
		}
	}
	current.UserID, current.Email, current.Role, current.Status = m.UserID, m.Email, m.Role, m.Status
	current.TokenHash, current.ExpiresAt, current.AcceptedAt = m.TokenHash, m.ExpiresAt, m.AcceptedAt
	out := *current
	return &out, nil
}

func (s *MemoryStore) DeleteMember(id string) error {
	s.mu.Lock()
	defer s.mu.Unlock()
	if _, ok := s.members[id]; !ok {
		return fmt.Errorf("member not found")
	}
	delete(s.members, id)
	return nil
}

func (s *MemoryStore) CreateLedgerEntry(e LedgerEntry) (*LedgerEntry, error) {
	s.mu.Lock()
	defer s.mu.Unlock()
	if _, ok := s.invitations[e.InvitationID]; !ok {
		return nil, fmt.Errorf("invitation not found")
	}
	e.ID = s.nextID("ledger")
	e.CreatedAt = time.Now().UTC()
	s.ledger[e.ID] = &e
	out := e
	return &out, nil
}

func (s *MemoryStore) ListLedger(invitationID string) []*LedgerEntry {
	s.mu.RLock()
	defer s.mu.RUnlock()
	items := make([]*LedgerEntry, 0)
	for _, e := range s.ledger {
		if e.InvitationID == invitationID {
			out := *e
			items = append(items, &out)
		}
	}
	sort.Slice(items, func(i, j int) bool { return items[i].CreatedAt.After(items[j].CreatedAt) })
	return items
}

func (s *MemoryStore) UpdateLedgerEntry(e LedgerEntry) (*LedgerEntry, error) {
	s.mu.Lock()
	defer s.mu.Unlock()
	current, ok := s.ledger[e.ID]
	if !ok || current.InvitationID != e.InvitationID {
		return nil, fmt.Errorf("ledger entry not found")
	}
	current.Name, current.Kind, current.Amount, current.Item, current.Note = e.Name, e.Kind, e.Amount, e.Item, e.Note
	out := *current
	return &out, nil
}

func (s *MemoryStore) DeleteLedgerEntry(invitationID, id string) error {
	s.mu.Lock()
	defer s.mu.Unlock()
	current, ok := s.ledger[id]
	if !ok || current.InvitationID != invitationID {
		return fmt.Errorf("ledger entry not found")
	}
	delete(s.ledger, id)
	return nil
}

func (s *MemoryStore) CreateGuestPhoto(p GuestPhoto) (*GuestPhoto, error) {
	s.mu.Lock()
	defer s.mu.Unlock()
	if _, ok := s.invitations[p.InvitationID]; !ok {
		return nil, fmt.Errorf("invitation not found")
	}
	p.ID = s.nextID("photo")
	p.CreatedAt = time.Now().UTC()
	s.guestPhotos[p.ID] = &p
	out := p
	return &out, nil
}

func (s *MemoryStore) ListGuestPhotos(invitationID, status string) []*GuestPhoto {
	s.mu.RLock()
	defer s.mu.RUnlock()
	items := make([]*GuestPhoto, 0)
	for _, p := range s.guestPhotos {
		if p.InvitationID == invitationID && (status == "" || p.Status == status) {
			out := *p
			items = append(items, &out)
		}
	}
	sort.Slice(items, func(i, j int) bool { return items[i].CreatedAt.After(items[j].CreatedAt) })
	return items
}

func (s *MemoryStore) UpdateGuestPhotoStatus(invitationID, id, status string) (*GuestPhoto, error) {
	s.mu.Lock()
	defer s.mu.Unlock()
	p, ok := s.guestPhotos[id]
	if !ok || p.InvitationID != invitationID {
		return nil, fmt.Errorf("photo not found")
	}
	p.Status = status
	out := *p
	return &out, nil
}

func (s *MemoryStore) GetPrivateData(invitationID, key string) map[string]any {
	s.mu.RLock()
	defer s.mu.RUnlock()
	raw, _ := json.Marshal(s.private[invitationID+"/"+key])
	out := map[string]any{}
	_ = json.Unmarshal(raw, &out)
	return out
}

func (s *MemoryStore) SetPrivateData(invitationID, key string, data map[string]any) error {
	raw, err := json.Marshal(data)
	if err != nil {
		return err
	}
	stored := map[string]any{}
	_ = json.Unmarshal(raw, &stored)
	s.mu.Lock()
	defer s.mu.Unlock()
	s.private[invitationID+"/"+key] = stored
	return nil
}

func (s *MemoryStore) CreateGiftPayout(p GiftPayout) (*GiftPayout, error) {
	s.mu.Lock()
	defer s.mu.Unlock()
	if _, ok := s.invitations[p.InvitationID]; !ok {
		return nil, fmt.Errorf("invitation not found")
	}
	p.ID = fmt.Sprintf("payout-%d", len(s.giftPayouts)+1)
	p.CreatedAt = time.Now().UTC()
	if p.Status == "" {
		p.Status = "requested"
	}
	s.giftPayouts[p.ID] = &p
	out := p
	return &out, nil
}

func (s *MemoryStore) listPayouts(keep func(*GiftPayout) bool) []*GiftPayout {
	s.mu.RLock()
	defer s.mu.RUnlock()
	items := make([]*GiftPayout, 0)
	for _, p := range s.giftPayouts {
		if keep(p) {
			out := *p
			items = append(items, &out)
		}
	}
	sort.Slice(items, func(i, j int) bool { return items[i].CreatedAt.After(items[j].CreatedAt) })
	return items
}

func (s *MemoryStore) ListGiftPayouts(invitationID string) []*GiftPayout {
	return s.listPayouts(func(p *GiftPayout) bool { return p.InvitationID == invitationID })
}

func (s *MemoryStore) ListAllGiftPayouts(status string) []*GiftPayout {
	return s.listPayouts(func(p *GiftPayout) bool { return status == "" || p.Status == status })
}

func (s *MemoryStore) FindGiftPayout(id string) (*GiftPayout, bool) {
	s.mu.RLock()
	defer s.mu.RUnlock()
	p, ok := s.giftPayouts[id]
	if !ok {
		return nil, false
	}
	out := *p
	return &out, true
}

func (s *MemoryStore) UpdateGiftPayout(id, status, note string) (*GiftPayout, error) {
	s.mu.Lock()
	defer s.mu.Unlock()
	p, ok := s.giftPayouts[id]
	if !ok {
		return nil, fmt.Errorf("payout not found")
	}
	now := time.Now().UTC()
	p.Status, p.Note, p.ProcessedAt = status, note, &now
	out := *p
	return &out, nil
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
		{ID: "marketplace", Name: "Marketplace", Slug: "marketplace", Category: "Belanja", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/marketplace.webp", PreviewURL: "/invitation/demo?template=marketplace", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 100},
		{ID: "oranye", Name: "Oranye", Slug: "oranye", Category: "Belanja", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/oranye.webp", PreviewURL: "/invitation/demo?template=oranye", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 101},
		{ID: "streaming", Name: "Streaming", Slug: "streaming", Category: "Hiburan", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/streaming.webp", PreviewURL: "/invitation/demo?template=streaming", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 102},
		{ID: "jawa", Name: "Jawa Keraton", Slug: "jawa", Category: "Adat Jawa", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/jawa.webp", PreviewURL: "/invitation/demo?template=jawa", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 103},
		{ID: "rumah-gadang", Name: "Rumah Gadang", Slug: "rumah-gadang", Category: "Adat Minang", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/rumah-gadang.webp", PreviewURL: "/invitation/demo?template=rumah-gadang", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 104},
		{ID: "bali-kuning", Name: "Bali Kuning", Slug: "bali-kuning", Category: "Adat Bali", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/bali-kuning.webp", PreviewURL: "/invitation/demo?template=bali-kuning", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 105},
		{ID: "syari-zamrud", Name: "Syari Zamrud", Slug: "syari-zamrud", Category: "Syari", EventType: "wedding", Tier: "free", Premium: false, PreviewImage: "/themes/previews/syari-zamrud.webp", PreviewURL: "/invitation/demo?template=syari-zamrud", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 106},
		{ID: "lavender-air", Name: "Lavender Air", Slug: "lavender-air", Category: "Cat Air", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/lavender-air.webp", PreviewURL: "/invitation/demo?template=lavender-air", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 107},
		{ID: "linen-putih", Name: "Linen Putih", Slug: "linen-putih", Category: "Minimalis", EventType: "wedding", Tier: "free", Premium: false, PreviewImage: "/themes/previews/linen-putih.webp", PreviewURL: "/invitation/demo?template=linen-putih", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 108},
		{ID: "sketsa-tangan", Name: "Sketsa Tangan", Slug: "sketsa-tangan", Category: "Gambar Tangan", EventType: "wedding", Tier: "free", Premium: false, PreviewImage: "/themes/previews/sketsa-tangan.webp", PreviewURL: "/invitation/demo?template=sketsa-tangan", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 109},
		{ID: "malam-rimba", Name: "Malam Rimba", Slug: "malam-rimba", Category: "Elegan", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/malam-rimba.webp", PreviewURL: "/invitation/demo?template=malam-rimba", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 110},
		{ID: "pastel-flat", Name: "Pastel Flat", Slug: "pastel-flat", Category: "Ilustrasi", EventType: "wedding", Tier: "free", Premium: false, PreviewImage: "/themes/previews/pastel-flat.webp", PreviewURL: "/invitation/demo?template=pastel-flat", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 111},
		{ID: "hijau-ojek", Name: "Hijau Ojek", Slug: "hijau-ojek", Category: "Aplikasi", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/hijau-ojek.webp", PreviewURL: "/invitation/demo?template=hijau-ojek", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 112},
		{ID: "pesan-antar", Name: "Pesan-Antar", Slug: "pesan-antar", Category: "Aplikasi", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/pesan-antar.webp", PreviewURL: "/invitation/demo?template=pesan-antar", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 113},
		{ID: "arena-legenda", Name: "Arena Legenda", Slug: "arena-legenda", Category: "Unik", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/arena-legenda.webp", PreviewURL: "/invitation/demo?template=arena-legenda", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 114},
		{ID: "kanal-video", Name: "Video", Slug: "kanal-video", Category: "Hiburan", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/kanal-video.webp", PreviewURL: "/invitation/demo?template=kanal-video", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 115},
		{ID: "repositori", Name: "Repositori", Slug: "repositori", Category: "Unik", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/repositori.webp", PreviewURL: "/invitation/demo?template=repositori", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 116},
		{ID: "pemutar-musik", Name: "Musik", Slug: "pemutar-musik", Category: "Hiburan", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/pemutar-musik.webp", PreviewURL: "/invitation/demo?template=pemutar-musik", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 117},
		{ID: "playlist", Name: "Playlist", Slug: "playlist", Category: "Hiburan", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/playlist.webp", PreviewURL: "/invitation/demo?template=playlist", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 118},
		{ID: "chat-hijau", Name: "Chat Hijau", Slug: "chat-hijau", Category: "Sosial Media", EventType: "wedding", Tier: "free", Premium: false, PreviewImage: "/themes/previews/chat-hijau.webp", PreviewURL: "/invitation/demo?template=chat-hijau", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 119},
		{ID: "feed-foto", Name: "Feed Foto", Slug: "feed-foto", Category: "Sosial Media", EventType: "wedding", Tier: "free", Premium: false, PreviewImage: "/themes/previews/feed-foto.webp", PreviewURL: "/invitation/demo?template=feed-foto", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 120},
		{ID: "video-vertikal", Name: "Video Vertikal", Slug: "video-vertikal", Category: "Sosial Media", EventType: "wedding", Tier: "free", Premium: false, PreviewImage: "/themes/previews/video-vertikal.webp", PreviewURL: "/invitation/demo?template=video-vertikal", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 121},
		{ID: "kencan", Name: "Kencan", Slug: "kencan", Category: "Sosial Media", EventType: "wedding", Tier: "free", Premium: false, PreviewImage: "/themes/previews/kencan.webp", PreviewURL: "/invitation/demo?template=kencan", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 122},
		{ID: "peta-rute", Name: "Peta", Slug: "peta-rute", Category: "Aplikasi", EventType: "wedding", Tier: "free", Premium: false, PreviewImage: "/themes/previews/peta-rute.webp", PreviewURL: "/invitation/demo?template=peta-rute", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 123},
		{ID: "surel", Name: "Surel", Slug: "surel", Category: "Aplikasi", EventType: "wedding", Tier: "free", Premium: false, PreviewImage: "/themes/previews/surel.webp", PreviewURL: "/invitation/demo?template=surel", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 124},
		{ID: "dokumen", Name: "Dokumen", Slug: "dokumen", Category: "Aplikasi", EventType: "wedding", Tier: "free", Premium: false, PreviewImage: "/themes/previews/dokumen.webp", PreviewURL: "/invitation/demo?template=dokumen", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 125},
		{ID: "rapat-video", Name: "Rapat Video", Slug: "rapat-video", Category: "Aplikasi", EventType: "wedding", Tier: "free", Premium: false, PreviewImage: "/themes/previews/rapat-video.webp", PreviewURL: "/invitation/demo?template=rapat-video", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 126},
		{ID: "boarding-pass", Name: "Boarding Pass", Slug: "boarding-pass", Category: "Perjalanan", EventType: "wedding", Tier: "free", Premium: false, PreviewImage: "/themes/previews/boarding-pass.webp", PreviewURL: "/invitation/demo?template=boarding-pass", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 127},
		{ID: "tiket-kereta", Name: "Tiket Kereta", Slug: "tiket-kereta", Category: "Perjalanan", EventType: "wedding", Tier: "free", Premium: false, PreviewImage: "/themes/previews/tiket-kereta.webp", PreviewURL: "/invitation/demo?template=tiket-kereta", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 128},
		{ID: "game-retro", Name: "Game Retro", Slug: "game-retro", Category: "Unik", EventType: "wedding", Tier: "free", Premium: false, PreviewImage: "/themes/previews/game-retro.webp", PreviewURL: "/invitation/demo?template=game-retro", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 129},
		{ID: "koran", Name: "Koran", Slug: "koran", Category: "Unik", EventType: "wedding", Tier: "free", Premium: false, PreviewImage: "/themes/previews/koran.webp", PreviewURL: "/invitation/demo?template=koran", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 130},
		{ID: "dompet-digital", Name: "Dompet Digital", Slug: "dompet-digital", Category: "Keuangan", EventType: "wedding", Tier: "free", Premium: false, PreviewImage: "/themes/previews/dompet-digital.webp", PreviewURL: "/invitation/demo?template=dompet-digital", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 131},
		{ID: "saku-biru", Name: "Saku Biru", Slug: "saku-biru", Category: "Keuangan", EventType: "wedding", Tier: "free", Premium: false, PreviewImage: "/themes/previews/saku-biru.webp", PreviewURL: "/invitation/demo?template=saku-biru", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 132},
		{ID: "poin-ungu", Name: "Poin Ungu", Slug: "poin-ungu", Category: "Keuangan", EventType: "wedding", Tier: "free", Premium: false, PreviewImage: "/themes/previews/poin-ungu.webp", PreviewURL: "/invitation/demo?template=poin-ungu", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 133},
		{ID: "kantong-oranye", Name: "Kantong Oranye", Slug: "kantong-oranye", Category: "Keuangan", EventType: "wedding", Tier: "free", Premium: false, PreviewImage: "/themes/previews/kantong-oranye.webp", PreviewURL: "/invitation/demo?template=kantong-oranye", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 134},
		{ID: "kursi-kereta", Name: "Kursi Kereta", Slug: "kursi-kereta", Category: "Perjalanan", EventType: "wedding", Tier: "free", Premium: false, PreviewImage: "/themes/previews/kursi-kereta.webp", PreviewURL: "/invitation/demo?template=kursi-kereta", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 135},
		{ID: "paket-liburan", Name: "Paket Liburan", Slug: "paket-liburan", Category: "Perjalanan", EventType: "wedding", Tier: "free", Premium: false, PreviewImage: "/themes/previews/paket-liburan.webp", PreviewURL: "/invitation/demo?template=paket-liburan", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 136},
		{ID: "rencana-perjalanan", Name: "Rencana Perjalanan", Slug: "rencana-perjalanan", Category: "Perjalanan", EventType: "wedding", Tier: "free", Premium: false, PreviewImage: "/themes/previews/rencana-perjalanan.webp", PreviewURL: "/invitation/demo?template=rencana-perjalanan", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 137},
		{ID: "mawar-blush", Name: "Mawar Blush", Slug: "mawar-blush", Description: "Bunga mawar cat air merah muda lembut dengan bingkai lengkung dan tulisan tangan.", Category: "Floral", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/mawar-blush.webp", PreviewURL: "/invitation/demo?template=mawar-blush", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 200},
		{ID: "emas-hitam", Name: "Emas Hitam", Slug: "emas-hitam", Description: "Mewah hitam-emas bergaya art deco dengan garis geometris berkilau.", Category: "Luxury", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/emas-hitam.webp", PreviewURL: "/invitation/demo?template=emas-hitam", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 201},
		{ID: "rustic-kayu", Name: "Rustic Kayu", Slug: "rustic-kayu", Description: "Kertas kraft, kayu hangat, dan rangkaian baby's breath bergaya pedesaan.", Category: "Rustic", EventType: "wedding", Tier: "free", Premium: false, PreviewImage: "/themes/previews/rustic-kayu.webp", PreviewURL: "/invitation/demo?template=rustic-kayu", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 202},
		{ID: "taman-eukaliptus", Name: "Taman Eukaliptus", Slug: "taman-eukaliptus", Description: "Hijau sage dengan daun eukaliptus untuk pesta taman yang segar.", Category: "Garden", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/taman-eukaliptus.webp", PreviewURL: "/invitation/demo?template=taman-eukaliptus", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 203},
		{ID: "surat-vintage", Name: "Surat Vintage", Slug: "surat-vintage", Description: "Surat lama bernuansa sepia lengkap dengan segel lilin dan perangko.", Category: "Vintage", EventType: "wedding", Tier: "free", Premium: false, PreviewImage: "/themes/previews/surat-vintage.webp", PreviewURL: "/invitation/demo?template=surat-vintage", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 204},
		{ID: "marmer-rosegold", Name: "Marmer Rose Gold", Slug: "marmer-rosegold", Description: "Marmer putih modern dengan aksen rose gold yang bersih dan mewah.", Category: "Luxury", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/marmer-rosegold.webp", PreviewURL: "/invitation/demo?template=marmer-rosegold", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 205},
		{ID: "langit-navy", Name: "Langit Navy", Slug: "langit-navy", Description: "Navy dan emas berhias bintang dan bulan untuk pesta malam.", Category: "Elegan", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/langit-navy.webp", PreviewURL: "/invitation/demo?template=langit-navy", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 206},
		{ID: "boho-terakota", Name: "Boho Terakota", Slug: "boho-terakota", Description: "Terakota hangat, rumput pampas, dan lengkungan bergaya bohemian.", Category: "Boho", EventType: "wedding", Tier: "free", Premium: false, PreviewImage: "/themes/previews/boho-terakota.webp", PreviewURL: "/invitation/demo?template=boho-terakota", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 207},
		{ID: "pantai-senja", Name: "Pantai Senja", Slug: "pantai-senja", Description: "Gradasi senja di tepi pantai dengan ombak dan nyiur melambai.", Category: "Pantai", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/pantai-senja.webp", PreviewURL: "/invitation/demo?template=pantai-senja", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 208},
		{ID: "editorial-monokrom", Name: "Editorial Monokrom", Slug: "editorial-monokrom", Description: "Tata letak majalah hitam-putih dengan tipografi besar yang tegas.", Category: "Minimalis", EventType: "wedding", Tier: "free", Premium: false, PreviewImage: "/themes/previews/editorial-monokrom.webp", PreviewURL: "/invitation/demo?template=editorial-monokrom", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 209},
		{ID: "kaligrafi-emas", Name: "Kaligrafi Emas", Slug: "kaligrafi-emas", Description: "Krem dan emas dengan lengkung mihrab dan ornamen geometris Islami.", Category: "Islami", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/kaligrafi-emas.webp", PreviewURL: "/invitation/demo?template=kaligrafi-emas", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 210},
		{ID: "masjid-biru", Name: "Masjid Biru", Slug: "masjid-biru", Description: "Biru tua berhias kubah, lentera, dan pola bintang delapan.", Category: "Islami", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/masjid-biru.webp", PreviewURL: "/invitation/demo?template=masjid-biru", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 211},
		{ID: "sakinah-putih", Name: "Sakinah Putih", Slug: "sakinah-putih", Description: "Syari putih-hijau lembut tanpa foto, penuh doa dan ayat.", Category: "Syari", EventType: "wedding", Tier: "free", Premium: false, PreviewImage: "/themes/previews/sakinah-putih.webp", PreviewURL: "/invitation/demo?template=sakinah-putih", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 212},
		{ID: "arabesque-marun", Name: "Arabesque Marun", Slug: "arabesque-marun", Description: "Marun dan emas dengan sulur arabesque yang anggun.", Category: "Islami", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/arabesque-marun.webp", PreviewURL: "/invitation/demo?template=arabesque-marun", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 213},
		{ID: "lentera-malam", Name: "Lentera Malam", Slug: "lentera-malam", Description: "Langit malam dengan lentera bergantungan dan bulan sabit.", Category: "Islami", EventType: "wedding", Tier: "free", Premium: false, PreviewImage: "/themes/previews/lentera-malam.webp", PreviewURL: "/invitation/demo?template=lentera-malam", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 214},
		{ID: "mihrab-pastel", Name: "Mihrab Pastel", Slug: "mihrab-pastel", Description: "Lengkung mihrab pastel tanpa foto, lembut dan bersahaja.", Category: "Syari", EventType: "wedding", Tier: "free", Premium: false, PreviewImage: "/themes/previews/mihrab-pastel.webp", PreviewURL: "/invitation/demo?template=mihrab-pastel", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 215},
		{ID: "sunda-siger", Name: "Sunda Siger", Slug: "sunda-siger", Description: "Adat Sunda hijau-emas dengan siger, melati, dan motif batik Mega Mendung.", Category: "Adat Sunda", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/sunda-siger.webp", PreviewURL: "/invitation/demo?template=sunda-siger", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 216},
		{ID: "batak-ulos", Name: "Batak Ulos", Slug: "batak-ulos", Description: "Adat Batak Toba merah-hitam-putih dengan motif gorga dan kain ulos.", Category: "Adat Batak", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/batak-ulos.webp", PreviewURL: "/invitation/demo?template=batak-ulos", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 217},
		{ID: "bugis-bosara", Name: "Bugis Bosara", Slug: "bugis-bosara", Description: "Adat Bugis-Makassar warna cerah dengan bosara dan sarung sutra.", Category: "Adat Bugis", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/bugis-bosara.webp", PreviewURL: "/invitation/demo?template=bugis-bosara", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 218},
		{ID: "betawi-ondel", Name: "Betawi Ondel", Slug: "betawi-ondel", Description: "Adat Betawi meriah dengan ondel-ondel, gigi balang, dan kembang kelapa.", Category: "Adat Betawi", EventType: "wedding", Tier: "free", Premium: false, PreviewImage: "/themes/previews/betawi-ondel.webp", PreviewURL: "/invitation/demo?template=betawi-ondel", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 219},
		{ID: "melayu-songket", Name: "Melayu Songket", Slug: "melayu-songket", Description: "Adat Melayu kuning-hijau dengan songket dan motif pucuk rebung.", Category: "Adat Melayu", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/melayu-songket.webp", PreviewURL: "/invitation/demo?template=melayu-songket", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 220},
		{ID: "toraja-tongkonan", Name: "Toraja Tongkonan", Slug: "toraja-tongkonan", Description: "Adat Toraja merah-hitam dengan atap tongkonan dan ukiran pa'ssura.", Category: "Adat Toraja", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/toraja-tongkonan.webp", PreviewURL: "/invitation/demo?template=toraja-tongkonan", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 221},
		{ID: "dayak-borneo", Name: "Dayak Borneo", Slug: "dayak-borneo", Description: "Adat Dayak dengan motif sulur khas Kalimantan dan burung enggang.", Category: "Adat Dayak", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/dayak-borneo.webp", PreviewURL: "/invitation/demo?template=dayak-borneo", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 222},
		{ID: "palembang-aesan", Name: "Palembang Aesan", Slug: "palembang-aesan", Description: "Adat Palembang merah-emas dengan aesan gede dan songket limar.", Category: "Adat Palembang", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/palembang-aesan.webp", PreviewURL: "/invitation/demo?template=palembang-aesan", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 223},
		{ID: "joglo-marun", Name: "Joglo Marun", Slug: "joglo-marun", Description: "Krem-marun dengan bingkai ukir gebyok, joglo samar, dan rangkaian bunga cat air yang rimbun.", Category: "Adat Jawa", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/joglo-marun.webp", PreviewURL: "/invitation/demo?template=joglo-marun", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 240},
		{ID: "kawung-biru", Name: "Kawung Biru", Slug: "kawung-biru", Description: "Biru nila bergaya toile: joglo, wayang, dan bingkai kawung dengan bunga lili dan anggrek.", Category: "Adat Jawa", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/kawung-biru.webp", PreviewURL: "/invitation/demo?template=kawung-biru", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 241},
		{ID: "gebyok-sogan", Name: "Gebyok Sogan", Slug: "gebyok-sogan", Description: "Krem dan cokelat sogan dengan gapura gebyok berukir, kembar mayang emas, dan kabut pegunungan.", Category: "Adat Jawa", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/gebyok-sogan.webp", PreviewURL: "/invitation/demo?template=gebyok-sogan", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 242},
		{ID: "busana-jawi", Name: "Busana Jawi", Slug: "busana-jawi", Description: "Foto penuh pasangan berbusana adat dengan tulisan putih elegan dan aksen batik parang emas.", Category: "Adat Jawa", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/busana-jawi.webp", PreviewURL: "/invitation/demo?template=busana-jawi", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 243},
		{ID: "wayang-mega", Name: "Wayang Mega", Slug: "wayang-mega", Description: "Tanpa foto: awan mega mendung, sepasang wayang kulit, dan pinggiran batik sogan.", Category: "Adat Jawa", EventType: "wedding", Tier: "free", Premium: false, PreviewImage: "/themes/previews/wayang-mega.webp", PreviewURL: "/invitation/demo?template=wayang-mega", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 244},
		{ID: "kereta-kencana", Name: "Kereta Kencana", Slug: "kereta-kencana", Description: "Kemegahan keraton Solo-Jogja: hijau tua dan emas, kereta kencana, payung agung, dan motif paes.", Category: "Adat Jawa", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/kereta-kencana.webp", PreviewURL: "/invitation/demo?template=kereta-kencana", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 245},
		{ID: "madura-sakera", Name: "Madura Sakera", Slug: "madura-sakera", Description: "Merah-hitam bergaris ala Sakera, keris, dan rumah tanean lanjang dengan batik tulis Madura yang berani.", Category: "Adat Madura", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/madura-sakera.webp", PreviewURL: "/invitation/demo?template=madura-sakera", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 300},
		{ID: "lampung-tapis", Name: "Lampung Tapis", Slug: "lampung-tapis", Description: "Kain tapis bersulam emas, siger Lampung bergerigi, dan motif kapal dari kain pelepai.", Category: "Adat Lampung", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/lampung-tapis.webp", PreviewURL: "/invitation/demo?template=lampung-tapis", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 301},
		{ID: "aceh-pintu", Name: "Aceh Pintu", Slug: "aceh-pintu", Description: "Motif pintu Aceh dan kerawang Gayo, merah-hijau-kuning keemasan, rumah Krong Bade.", Category: "Adat Aceh", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/aceh-pintu.webp", PreviewURL: "/invitation/demo?template=aceh-pintu", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 302},
		{ID: "papua-cendrawasih", Name: "Papua Cendrawasih", Slug: "papua-cendrawasih", Description: "Burung cendrawasih, ukiran garis Asmat, noken, dan warna tanah merah-oker yang hangat.", Category: "Adat Papua", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/papua-cendrawasih.webp", PreviewURL: "/invitation/demo?template=papua-cendrawasih", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 303},
		{ID: "ntt-tenun", Name: "Tenun NTT", Slug: "ntt-tenun", Description: "Tenun ikat Sumba nila-karat bermotif kuda dan rumah kerucut Mbaru Niang.", Category: "Adat NTT", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/ntt-tenun.webp", PreviewURL: "/invitation/demo?template=ntt-tenun", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 304},
		{ID: "banjar-sasirangan", Name: "Banjar Sasirangan", Slug: "banjar-sasirangan", Description: "Kain sasirangan jumputan, rumah Bubungan Tinggi, dan jukung di sungai Kalimantan.", Category: "Adat Banjar", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/banjar-sasirangan.webp", PreviewURL: "/invitation/demo?template=banjar-sasirangan", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 305},
		{ID: "zellige-hijau", Name: "Zellige Hijau", Slug: "zellige-hijau", Description: "Ubin zellige Maroko hijau toska-putih dengan lengkung riad dan air mancur taman.", Category: "Islami", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/zellige-hijau.webp", PreviewURL: "/invitation/demo?template=zellige-hijau", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 306},
		{ID: "andalusia-terakota", Name: "Andalusia Terakota", Slug: "andalusia-terakota", Description: "Lengkung muqarnas bergaya Andalusia, terakota dan biru kobalt dengan ubin bunga.", Category: "Islami", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/andalusia-terakota.webp", PreviewURL: "/invitation/demo?template=andalusia-terakota", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 307},
		{ID: "tasbih-mutiara", Name: "Tasbih Mutiara", Slug: "tasbih-mutiara", Description: "Tanpa foto: putih mutiara dan hijau sage, untaian mutiara, dan mawar cat air lembut.", Category: "Syari", EventType: "wedding", Tier: "free", Premium: false, PreviewImage: "/themes/previews/tasbih-mutiara.webp", PreviewURL: "/invitation/demo?template=tasbih-mutiara", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 308},
		{ID: "hijrah-senja", Name: "Hijrah Senja", Slug: "hijrah-senja", Description: "Gurun pasir saat senja, bulan sabit, lentera, dan kafilah unta yang dilukis hangat.", Category: "Islami", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/hijrah-senja.webp", PreviewURL: "/invitation/demo?template=hijrah-senja", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 309},
		{ID: "iznik-tulip", Name: "Iznik Tulip", Slug: "iznik-tulip", Description: "Keramik Iznik: tulip dan anyelir biru kobalt, toska, dan merah di atas putih.", Category: "Islami", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/iznik-tulip.webp", PreviewURL: "/invitation/demo?template=iznik-tulip", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 310},
		{ID: "taman-persia", Name: "Taman Persia", Slug: "taman-persia", Description: "Taman ala lukisan miniatur Persia: pohon cemara, delima, dan biru lapis berpadu emas.", Category: "Islami", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/taman-persia.webp", PreviewURL: "/invitation/demo?template=taman-persia", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 311},
		{ID: "deco-sampanye", Name: "Deco Sampanye", Slug: "deco-sampanye", Description: "Art deco sampanye dan hitam dengan geometri kipas berlapis emas ala 1920-an.", Category: "Luxury", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/deco-sampanye.webp", PreviewURL: "/invitation/demo?template=deco-sampanye", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 312},
		{ID: "terrazzo-modern", Name: "Terrazzo Modern", Slug: "terrazzo-modern", Description: "Terrazzo sage-terakota dengan bentuk geometris modern dan tipografi bersih.", Category: "Minimalis", EventType: "wedding", Tier: "free", Premium: false, PreviewImage: "/themes/previews/terrazzo-modern.webp", PreviewURL: "/invitation/demo?template=terrazzo-modern", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 313},
		{ID: "sakura-sumi", Name: "Sakura Sumi", Slug: "sakura-sumi", Description: "Bunga sakura bergaya lukisan tinta sumi-e di atas kertas washi yang tenang.", Category: "Floral", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/sakura-sumi.webp", PreviewURL: "/invitation/demo?template=sakura-sumi", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 314},
		{ID: "kebun-tropis", Name: "Kebun Tropis", Slug: "kebun-tropis", Description: "Daun pisang, bunga cendrawasih (strelitzia), dan warna tropis yang cerah.", Category: "Garden", EventType: "wedding", Tier: "free", Premium: false, PreviewImage: "/themes/previews/kebun-tropis.webp", PreviewURL: "/invitation/demo?template=kebun-tropis", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 315},
		{ID: "herbarium-klasik", Name: "Herbarium Klasik", Slug: "herbarium-klasik", Description: "Bunga kering bergaya lembar herbarium lengkap dengan label tulisan tangan.", Category: "Vintage", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/herbarium-klasik.webp", PreviewURL: "/invitation/demo?template=herbarium-klasik", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 316},
		{ID: "telaga-kabut", Name: "Telaga Kabut", Slug: "telaga-kabut", Description: "Telaga dan pegunungan berkabut cat air dalam nuansa hijau-biru yang sejuk.", Category: "Pemandangan", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/telaga-kabut.webp", PreviewURL: "/invitation/demo?template=telaga-kabut", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 317},
		{ID: "perak-kenangan", Name: "Perak Kenangan", Slug: "perak-kenangan", Description: "Ulang tahun pernikahan perak dan emas: kenangan, foto lama, dan rangkaian mawar.", Category: "Ulang Tahun Pernikahan", EventType: "syukuran", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/perak-kenangan.webp", PreviewURL: "/invitation/demo?template=perak-kenangan", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 318},
		{ID: "ultah-dino", Name: "Ultah Dino", Slug: "ultah-dino", Description: "Ulang tahun anak bersama dinosaurus lucu, gunung api kue, dan dedaunan purba.", Category: "Ulang Tahun", EventType: "ulang-tahun", Tier: "free", Premium: false, PreviewImage: "/themes/previews/ultah-dino.webp", PreviewURL: "/invitation/demo?template=ultah-dino", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 319},
		{ID: "baby-shower-awan", Name: "Baby Shower Awan", Slug: "baby-shower-awan", Description: "Baby shower pastel dengan awan, balon udara, dan bintang-bintang kecil.", Category: "Baby Shower", EventType: "syukuran", Tier: "free", Premium: false, PreviewImage: "/themes/previews/baby-shower-awan.webp", PreviewURL: "/invitation/demo?template=baby-shower-awan", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 320},
		{ID: "walimatus-safar", Name: "Walimatus Safar", Slug: "walimatus-safar", Description: "Walimatus safar haji/umrah: doa perjalanan, gurun, dan lentera dalam hijau-emas.", Category: "Syukuran", EventType: "syukuran", Tier: "free", Premium: false, PreviewImage: "/themes/previews/walimatus-safar.webp", PreviewURL: "/invitation/demo?template=walimatus-safar", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 321},
		{ID: "reuni-sekolah", Name: "Reuni Sekolah", Slug: "reuni-sekolah", Description: "Reuni sekolah bernuansa buku tulis, papan kapur, dan foto angkatan yang retro.", Category: "Reuni", EventType: "lainnya", Tier: "free", Premium: false, PreviewImage: "/themes/previews/reuni-sekolah.webp", PreviewURL: "/invitation/demo?template=reuni-sekolah", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 322},
		{ID: "sweet-seventeen", Name: "Sweet Seventeen", Slug: "sweet-seventeen", Description: "Pesta tujuh belas tahun: merah muda, mutiara, pita satin, dan kilau malam.", Category: "Ulang Tahun", EventType: "ulang-tahun", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/sweet-seventeen.webp", PreviewURL: "/invitation/demo?template=sweet-seventeen", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 323},
		{ID: "minahasa-kawanua", Name: "Minahasa Kawanua", Slug: "minahasa-kawanua", Description: "Kain bentenan, rumah panggung kayu Woloan, dan burung manguni dalam merah-hitam-emas.", Category: "Adat Minahasa", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/minahasa-kawanua.webp", PreviewURL: "/invitation/demo?template=minahasa-kawanua", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 330},
		{ID: "gorontalo-karawo", Name: "Gorontalo Karawo", Slug: "gorontalo-karawo", Description: "Sulaman kerawang karawo yang halus, warna lembut, dan rumah adat Dulohupa.", Category: "Adat Gorontalo", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/gorontalo-karawo.webp", PreviewURL: "/invitation/demo?template=gorontalo-karawo", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 331},
		{ID: "nias-omo", Name: "Nias Omo Sebua", Slug: "nias-omo", Description: "Rumah Omo Sebua berukir di atas tiang besar, emas dan merah-hitam khas Nias.", Category: "Adat Nias", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/nias-omo.webp", PreviewURL: "/invitation/demo?template=nias-omo", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 332},
		{ID: "sasak-lombok", Name: "Sasak Lombok", Slug: "sasak-lombok", Description: "Songket Sasak, lumbung padi beratap ilalang, dan pantai Lombok yang tenang.", Category: "Adat Sasak", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/sasak-lombok.webp", PreviewURL: "/invitation/demo?template=sasak-lombok", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 333},
		{ID: "mandar-sandeq", Name: "Mandar Sandeq", Slug: "mandar-sandeq", Description: "Perahu layar sandeq, sarung sutra lipaq saqbe, dan laut biru Sulawesi Barat.", Category: "Adat Mandar", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/mandar-sandeq.webp", PreviewURL: "/invitation/demo?template=mandar-sandeq", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 334},
		{ID: "jambi-angso", Name: "Jambi Angso Duo", Slug: "jambi-angso", Description: "Batik Jambi bermotif angso duo, rumah Kajang Leko, dan sungai Batanghari.", Category: "Adat Jambi", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/jambi-angso.webp", PreviewURL: "/invitation/demo?template=jambi-angso", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 335},
		{ID: "mashrabiya-kayu", Name: "Mashrabiya Kayu", Slug: "mashrabiya-kayu", Description: "Kisi-kisi kayu mashrabiya yang menyaring cahaya hangat menjadi pola bayangan.", Category: "Islami", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/mashrabiya-kayu.webp", PreviewURL: "/invitation/demo?template=mashrabiya-kayu", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 336},
		{ID: "mughal-marmer", Name: "Mughal Marmer", Slug: "mughal-marmer", Description: "Marmer putih bertatah batu bunga (pietra dura) dan lengkung Mughal yang anggun.", Category: "Islami", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/mughal-marmer.webp", PreviewURL: "/invitation/demo?template=mughal-marmer", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 337},
		{ID: "oasis-kurma", Name: "Oasis Kurma", Slug: "oasis-kurma", Description: "Oasis di siang hari: pohon kurma, kolam jernih, dan langit gurun yang cerah.", Category: "Islami", EventType: "wedding", Tier: "free", Premium: false, PreviewImage: "/themes/previews/oasis-kurma.webp", PreviewURL: "/invitation/demo?template=oasis-kurma", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 338},
		{ID: "masjid-tajug", Name: "Masjid Tajug", Slug: "masjid-tajug", Description: "Masjid kuno beratap tajug bersusun ala Nusantara dengan kayu jati dan halaman berpasir.", Category: "Islami", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/masjid-tajug.webp", PreviewURL: "/invitation/demo?template=masjid-tajug", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 339},
		{ID: "anyelir-syari", Name: "Anyelir Syari", Slug: "anyelir-syari", Description: "Tanpa foto: anyelir garis halus dalam mauve dan krem, lembut dan tenang.", Category: "Syari", EventType: "wedding", Tier: "free", Premium: false, PreviewImage: "/themes/previews/anyelir-syari.webp", PreviewURL: "/invitation/demo?template=anyelir-syari", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 340},
		{ID: "samarkand-biru", Name: "Samarkand Biru", Slug: "samarkand-biru", Description: "Kubah toska dan ubin Timurid ala Registan dengan langit biru yang dalam.", Category: "Islami", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/samarkand-biru.webp", PreviewURL: "/invitation/demo?template=samarkand-biru", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 341},
		{ID: "boho-pampas", Name: "Boho Pampas", Slug: "boho-pampas", Description: "Rumput pampas, lengkung rotan, dan warna netral hangat bergaya bohemian.", Category: "Boho", EventType: "wedding", Tier: "free", Premium: false, PreviewImage: "/themes/previews/boho-pampas.webp", PreviewURL: "/invitation/demo?template=boho-pampas", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 342},
		{ID: "hydrangea-biru", Name: "Hydrangea Biru", Slug: "hydrangea-biru", Description: "Bunga hortensia biru-ungu cat air yang rimbun dengan pita sutra.", Category: "Floral", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/hydrangea-biru.webp", PreviewURL: "/invitation/demo?template=hydrangea-biru", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 343},
		{ID: "riso-cetak", Name: "Riso Cetak", Slug: "riso-cetak", Description: "Cetak risograf dua warna dengan halftone, tekstur tinta, dan tata letak berani.", Category: "Modern", EventType: "wedding", Tier: "free", Premium: false, PreviewImage: "/themes/previews/riso-cetak.webp", PreviewURL: "/invitation/demo?template=riso-cetak", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 344},
		{ID: "kaca-patri", Name: "Kaca Patri", Slug: "kaca-patri", Description: "Kaca patri berwarna dengan garis timah ala art nouveau yang bercahaya.", Category: "Vintage", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/kaca-patri.webp", PreviewURL: "/invitation/demo?template=kaca-patri", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 345},
		{ID: "delft-biru", Name: "Delft Biru", Slug: "delft-biru", Description: "Ubin keramik Delft biru-putih bergaya warisan Hindia dengan bunga dan kincir.", Category: "Vintage", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/delft-biru.webp", PreviewURL: "/invitation/demo?template=delft-biru", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 346},
		{ID: "origami-bangau", Name: "Origami Bangau", Slug: "origami-bangau", Description: "Seribu bangau kertas origami dalam warna lembut di atas kertas bertekstur.", Category: "Modern", EventType: "wedding", Tier: "free", Premium: false, PreviewImage: "/themes/previews/origami-bangau.webp", PreviewURL: "/invitation/demo?template=origami-bangau", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 347},
		{ID: "ultah-antariksa", Name: "Ultah Antariksa", Slug: "ultah-antariksa", Description: "Ulang tahun anak bertema luar angkasa: roket, planet, dan bintang yang ramah.", Category: "Ulang Tahun", EventType: "ulang-tahun", Tier: "free", Premium: false, PreviewImage: "/themes/previews/ultah-antariksa.webp", PreviewURL: "/invitation/demo?template=ultah-antariksa", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 348},
		{ID: "aqiqah-domba", Name: "Aqiqah Domba", Slug: "aqiqah-domba", Description: "Aqiqah dengan domba lucu berbulu lembut, padang hijau, dan awan pastel.", Category: "Aqiqah", EventType: "aqiqah", Tier: "free", Premium: false, PreviewImage: "/themes/previews/aqiqah-domba.webp", PreviewURL: "/invitation/demo?template=aqiqah-domba", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 349},
		{ID: "khataman-quran", Name: "Khataman Quran", Slug: "khataman-quran", Description: "Syukuran khataman Al-Qur'an dengan rehal kayu, lentera, dan hijau-emas yang teduh.", Category: "Syukuran", EventType: "syukuran", Tier: "free", Premium: false, PreviewImage: "/themes/previews/khataman-quran.webp", PreviewURL: "/invitation/demo?template=khataman-quran", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 350},
		{ID: "tedak-siten", Name: "Tedak Siten", Slug: "tedak-siten", Description: "Upacara tedak siten: tangga tebu, jadah tujuh warna, dan kurungan berhias.", Category: "Syukuran", EventType: "syukuran", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/tedak-siten.webp", PreviewURL: "/invitation/demo?template=tedak-siten", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 351},
		{ID: "halal-bihalal", Name: "Halal Bihalal", Slug: "halal-bihalal", Description: "Halal bihalal keluarga: ketupat, lampu pelita, dan suasana Lebaran yang hangat.", Category: "Syukuran", EventType: "syukuran", Tier: "free", Premium: false, PreviewImage: "/themes/previews/halal-bihalal.webp", PreviewURL: "/invitation/demo?template=halal-bihalal", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 352},
		{ID: "purna-tugas", Name: "Purna Tugas", Slug: "purna-tugas", Description: "Syukuran purna tugas atau pensiun: perjalanan karier, buku kenangan, dan bunga.", Category: "Syukuran", EventType: "syukuran", Tier: "free", Premium: false, PreviewImage: "/themes/previews/purna-tugas.webp", PreviewURL: "/invitation/demo?template=purna-tugas", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 353},
		{ID: "bengkulu-rafflesia", Name: "Bengkulu Rafflesia", Slug: "bengkulu-rafflesia", Description: "Bunga rafflesia raksasa, rumah Bubungan Lima, dan pantai Panjang Bengkulu yang hangat.", Category: "Adat Bengkulu", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/bengkulu-rafflesia.webp", PreviewURL: "/invitation/demo?template=bengkulu-rafflesia", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 360},
		{ID: "maluku-tifa", Name: "Maluku Tifa", Slug: "maluku-tifa", Description: "Tifa berukir, tenun Tanimbar, cengkih, dan laut biru kepulauan Maluku.", Category: "Adat Maluku", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/maluku-tifa.webp", PreviewURL: "/invitation/demo?template=maluku-tifa", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 361},
		{ID: "sumbawa-samawa", Name: "Sumbawa Samawa", Slug: "sumbawa-samawa", Description: "Tenun kre alang berbenang emas dan istana kayu Dalam Loka yang megah.", Category: "Adat Sumbawa", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/sumbawa-samawa.webp", PreviewURL: "/invitation/demo?template=sumbawa-samawa", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 362},
		{ID: "peranakan-merah", Name: "Peranakan Merah", Slug: "peranakan-merah", Description: "Pernikahan Peranakan merah-emas: sulaman burung hong, peoni, dan kebaya encim.", Category: "Peranakan", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/peranakan-merah.webp", PreviewURL: "/invitation/demo?template=peranakan-merah", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 363},
		{ID: "osing-gajah-oling", Name: "Osing Gajah Oling", Slug: "osing-gajah-oling", Description: "Batik gajah oling Banyuwangi, rumah Osing, dan kebun kopi di kaki Ijen.", Category: "Adat Osing", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/osing-gajah-oling.webp", PreviewURL: "/invitation/demo?template=osing-gajah-oling", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 364},
		{ID: "buton-wolio", Name: "Buton Wolio", Slug: "buton-wolio", Description: "Benteng keraton Buton, istana Kamali, dan tenun Buton bergaris cerah.", Category: "Adat Buton", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/buton-wolio.webp", PreviewURL: "/invitation/demo?template=buton-wolio", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 365},
		{ID: "lampu-mosaik", Name: "Lampu Mosaik", Slug: "lampu-mosaik", Description: "Lampu gantung kaca mosaik warna-warni yang berpendar hangat di malam hari.", Category: "Islami", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/lampu-mosaik.webp", PreviewURL: "/invitation/demo?template=lampu-mosaik", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 366},
		{ID: "hadramaut-tanah", Name: "Hadramaut Tanah", Slug: "hadramaut-tanah", Description: "Rumah menara bata lumpur ala Hadramaut dengan lis putih dan langit senja gurun.", Category: "Islami", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/hadramaut-tanah.webp", PreviewURL: "/invitation/demo?template=hadramaut-tanah", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 367},
		{ID: "melati-syari", Name: "Melati Syari", Slug: "melati-syari", Description: "Tanpa foto: untaian melati putih dan daun hijau yang bersih dan tenang.", Category: "Syari", EventType: "wedding", Tier: "free", Premium: false, PreviewImage: "/themes/previews/melati-syari.webp", PreviewURL: "/invitation/demo?template=melati-syari", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 368},
		{ID: "kaftan-ottoman", Name: "Kaftan Ottoman", Slug: "kaftan-ottoman", Description: "Brokat sutra kaftan Utsmani merah tua dan emas dengan motif cintamani dan bunga.", Category: "Islami", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/kaftan-ottoman.webp", PreviewURL: "/invitation/demo?template=kaftan-ottoman", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 369},
		{ID: "istana-maimun", Name: "Istana Maimun", Slug: "istana-maimun", Description: "Kemegahan kesultanan Melayu Deli: kuning-emas, lengkung istana, dan ukiran Melayu.", Category: "Islami", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/istana-maimun.webp", PreviewURL: "/invitation/demo?template=istana-maimun", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 370},
		{ID: "langit-subuh", Name: "Langit Subuh", Slug: "langit-subuh", Description: "Langit subuh pastel dengan siluet menara dan cahaya pertama yang lembut.", Category: "Islami", EventType: "wedding", Tier: "free", Premium: false, PreviewImage: "/themes/previews/langit-subuh.webp", PreviewURL: "/invitation/demo?template=langit-subuh", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 371},
		{ID: "zaitun-tuscan", Name: "Zaitun Tuscan", Slug: "zaitun-tuscan", Description: "Ranting zaitun, terakota, dan vila pedesaan Tuscan di bawah matahari sore.", Category: "Rustic", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/zaitun-tuscan.webp", PreviewURL: "/invitation/demo?template=zaitun-tuscan", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 372},
		{ID: "santorini-putih", Name: "Santorini Putih", Slug: "santorini-putih", Description: "Dinding kapur putih, pintu biru, bugenvil, dan laut Aegea yang berkilau.", Category: "Pantai", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/santorini-putih.webp", PreviewURL: "/invitation/demo?template=santorini-putih", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 373},
		{ID: "neon-malam", Name: "Neon Malam", Slug: "neon-malam", Description: "Tulisan neon berpendar di dinding bata malam hari, modern dan meriah.", Category: "Modern", EventType: "wedding", Tier: "free", Premium: false, PreviewImage: "/themes/previews/neon-malam.webp", PreviewURL: "/invitation/demo?template=neon-malam", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 374},
		{ID: "marmer-ebru", Name: "Marmer Ebru", Slug: "marmer-ebru", Description: "Kertas marmer ebru dengan pusaran warna lembut dan aksen emas.", Category: "Modern", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/marmer-ebru.webp", PreviewURL: "/invitation/demo?template=marmer-ebru", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 375},
		{ID: "padang-liar", Name: "Padang Liar", Slug: "padang-liar", Description: "Padang bunga liar: cosmos, chamomile, dan rumput yang tertiup angin.", Category: "Garden", EventType: "wedding", Tier: "free", Premium: false, PreviewImage: "/themes/previews/padang-liar.webp", PreviewURL: "/invitation/demo?template=padang-liar", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 376},
		{ID: "batik-kontemporer", Name: "Batik Kontemporer", Slug: "batik-kontemporer", Description: "Batik gaya kontemporer berwarna berani dengan tata letak modern yang bersih.", Category: "Modern", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/batik-kontemporer.webp", PreviewURL: "/invitation/demo?template=batik-kontemporer", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 377},
		{ID: "ultah-unicorn", Name: "Ultah Unicorn", Slug: "ultah-unicorn", Description: "Ulang tahun anak bersama unicorn pastel, pelangi, dan awan permen kapas.", Category: "Ulang Tahun", EventType: "ulang-tahun", Tier: "free", Premium: false, PreviewImage: "/themes/previews/ultah-unicorn.webp", PreviewURL: "/invitation/demo?template=ultah-unicorn", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 378},
		{ID: "ultah-bola", Name: "Ultah Bola", Slug: "ultah-bola", Description: "Ulang tahun anak bertema sepak bola: lapangan hijau, bola, dan piala.", Category: "Ulang Tahun", EventType: "ulang-tahun", Tier: "free", Premium: false, PreviewImage: "/themes/previews/ultah-bola.webp", PreviewURL: "/invitation/demo?template=ultah-bola", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 379},
		{ID: "wisuda-tk", Name: "Wisuda TK", Slug: "wisuda-tk", Description: "Pelepasan TK dengan krayon, toga mini, dan gambar anak-anak yang ceria.", Category: "Wisuda", EventType: "wisuda", Tier: "free", Premium: false, PreviewImage: "/themes/previews/wisuda-tk.webp", PreviewURL: "/invitation/demo?template=wisuda-tk", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 380},
		{ID: "syukuran-kelahiran", Name: "Syukuran Kelahiran", Slug: "syukuran-kelahiran", Description: "Syukuran kelahiran bayi dengan mainan gantung, jejak kaki mungil, dan pastel lembut.", Category: "Syukuran", EventType: "syukuran", Tier: "free", Premium: false, PreviewImage: "/themes/previews/syukuran-kelahiran.webp", PreviewURL: "/invitation/demo?template=syukuran-kelahiran", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 381},
		{ID: "ultah-sepuh", Name: "Ultah Sepuh", Slug: "ultah-sepuh", Description: "Ulang tahun ke-60/70 yang anggun: emas, bunga, dan kenangan keluarga besar.", Category: "Ulang Tahun", EventType: "ulang-tahun", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/ultah-sepuh.webp", PreviewURL: "/invitation/demo?template=ultah-sepuh", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 382},
		{ID: "natal-keluarga", Name: "Natal Keluarga", Slug: "natal-keluarga", Description: "Perayaan Natal keluarga: pohon cemara, lilin, bintang, dan kehangatan rumah.", Category: "Natal", EventType: "lainnya", Tier: "free", Premium: false, PreviewImage: "/themes/previews/natal-keluarga.webp", PreviewURL: "/invitation/demo?template=natal-keluarga", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 383},
		{ID: "bali-gringsing", Name: "Bali Gringsing", Slug: "bali-gringsing", Description: "Tenun ikat ganda gringsing Tenganan, merah-hitam-krem, dan pura batu desa Bali Aga.", Category: "Adat Bali", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/bali-gringsing.webp", PreviewURL: "/invitation/demo?template=bali-gringsing", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 390},
		{ID: "doyo-benuaq", Name: "Doyo Benuaq", Slug: "doyo-benuaq", Description: "Tenun ulap doyo serat daun, rumah lamin panjang, dan hutan Mahakam.", Category: "Adat Dayak", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/doyo-benuaq.webp", PreviewURL: "/invitation/demo?template=doyo-benuaq", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 391},
		{ID: "riau-lancang", Name: "Riau Lancang Kuning", Slug: "riau-lancang", Description: "Perahu Lancang Kuning, selembayung, dan laut Riau dalam kuning-hijau Melayu.", Category: "Adat Melayu", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/riau-lancang.webp", PreviewURL: "/invitation/demo?template=riau-lancang", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 392},
		{ID: "flores-sikka", Name: "Flores Sikka", Slug: "flores-sikka", Description: "Tenun ikat Sikka Maumere, bukit Flores, dan danau Kelimutu tiga warna.", Category: "Adat NTT", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/flores-sikka.webp", PreviewURL: "/invitation/demo?template=flores-sikka", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 393},
		{ID: "cirebon-kasepuhan", Name: "Cirebon Kasepuhan", Slug: "cirebon-kasepuhan", Description: "Gerbang bata keraton Kasepuhan bertatah piring porselen dan taman sari.", Category: "Adat Cirebon", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/cirebon-kasepuhan.webp", PreviewURL: "/invitation/demo?template=cirebon-kasepuhan", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 394},
		{ID: "belitung-granit", Name: "Belitung Granit", Slug: "belitung-granit", Description: "Batu granit raksasa, mercusuar, dan laut jernih Belitung yang tenang.", Category: "Adat Melayu", EventType: "wedding", Tier: "free", Premium: false, PreviewImage: "/themes/previews/belitung-granit.webp", PreviewURL: "/invitation/demo?template=belitung-granit", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 395},
		{ID: "khatam-kayu", Name: "Khatam Kayu", Slug: "khatam-kayu", Description: "Pintu kayu berukir dengan tatahan khatam geometris dari kayu, tulang, dan logam.", Category: "Islami", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/khatam-kayu.webp", PreviewURL: "/invitation/demo?template=khatam-kayu", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 396},
		{ID: "masjid-terapung", Name: "Masjid Terapung", Slug: "masjid-terapung", Description: "Masjid di atas air saat senja dengan pantulan cahaya di laut yang tenang.", Category: "Islami", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/masjid-terapung.webp", PreviewURL: "/invitation/demo?template=masjid-terapung", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 397},
		{ID: "kilim-anatolia", Name: "Kilim Anatolia", Slug: "kilim-anatolia", Description: "Tenun kilim Anatolia: geometri berani merah bata, nila, dan kunyit.", Category: "Islami", EventType: "wedding", Tier: "free", Premium: false, PreviewImage: "/themes/previews/kilim-anatolia.webp", PreviewURL: "/invitation/demo?template=kilim-anatolia", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 398},
		{ID: "pualam-hitam", Name: "Pualam Hitam", Slug: "pualam-hitam", Description: "Pualam hitam bertatah emas geometris yang mewah dan tenang.", Category: "Islami", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/pualam-hitam.webp", PreviewURL: "/invitation/demo?template=pualam-hitam", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 399},
		{ID: "sulam-zamrud", Name: "Sulam Zamrud", Slug: "sulam-zamrud", Description: "Tanpa foto: sutra hijau zamrud bersulam benang emas berpola bunga dan bintang.", Category: "Syari", EventType: "wedding", Tier: "free", Premium: false, PreviewImage: "/themes/previews/sulam-zamrud.webp", PreviewURL: "/invitation/demo?template=sulam-zamrud", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 400},
		{ID: "mutiara-damaskus", Name: "Mutiara Damaskus", Slug: "mutiara-damaskus", Description: "Kayu bertatah kerang mutiara ala Damaskus dengan mawar damask yang lembut.", Category: "Islami", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/mutiara-damaskus.webp", PreviewURL: "/invitation/demo?template=mutiara-damaskus", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 401},
		{ID: "cyanotype-biru", Name: "Cyanotype Biru", Slug: "cyanotype-biru", Description: "Cetak cyanotype biru prusia: siluet daun dan bunga yang dijemur matahari.", Category: "Vintage", EventType: "wedding", Tier: "free", Premium: false, PreviewImage: "/themes/previews/cyanotype-biru.webp", PreviewURL: "/invitation/demo?template=cyanotype-biru", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 402},
		{ID: "shibori-indigo", Name: "Shibori Indigo", Slug: "shibori-indigo", Description: "Kain shibori celup indigo dengan pola ikat, lipat, dan jahit yang lembut.", Category: "Modern", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/shibori-indigo.webp", PreviewURL: "/invitation/demo?template=shibori-indigo", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 403},
		{ID: "karang-laut", Name: "Karang Laut", Slug: "karang-laut", Description: "Taman karang bawah laut cat air dengan cahaya yang menembus air biru.", Category: "Pantai", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/karang-laut.webp", PreviewURL: "/invitation/demo?template=karang-laut", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 404},
		{ID: "musim-gugur", Name: "Musim Gugur", Slug: "musim-gugur", Description: "Daun maple dan oak musim gugur dalam jingga, merah bata, dan emas.", Category: "Garden", EventType: "wedding", Tier: "free", Premium: false, PreviewImage: "/themes/previews/musim-gugur.webp", PreviewURL: "/invitation/demo?template=musim-gugur", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 405},
		{ID: "impasto-taman", Name: "Impasto Taman", Slug: "impasto-taman", Description: "Taman bunga bergaya lukisan cat minyak impresionis dengan sapuan tebal.", Category: "Floral", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/impasto-taman.webp", PreviewURL: "/invitation/demo?template=impasto-taman", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 406},
		{ID: "kebun-anggrek", Name: "Kebun Anggrek", Slug: "kebun-anggrek", Description: "Rumah kaca anggrek tropis: bulan, dendrobium, dan cahaya pagi yang lembap.", Category: "Floral", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/kebun-anggrek.webp", PreviewURL: "/invitation/demo?template=kebun-anggrek", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 407},
		{ID: "khitan-pangeran", Name: "Khitan Pangeran", Slug: "khitan-pangeran", Description: "Khitanan bertema pangeran kecil: mahkota, istana, dan biru-emas yang gagah.", Category: "Khitanan", EventType: "khitan", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/khitan-pangeran.webp", PreviewURL: "/invitation/demo?template=khitan-pangeran", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 408},
		{ID: "ultah-istana", Name: "Ultah Istana", Slug: "ultah-istana", Description: "Ulang tahun anak di istana dongeng: menara, bendera, dan taman bunga.", Category: "Ulang Tahun", EventType: "ulang-tahun", Tier: "free", Premium: false, PreviewImage: "/themes/previews/ultah-istana.webp", PreviewURL: "/invitation/demo?template=ultah-istana", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 409},
		{ID: "ultah-sirkus", Name: "Ultah Sirkus", Slug: "ultah-sirkus", Description: "Ulang tahun bertema sirkus: tenda bergaris, balon, dan atraksi yang ceria.", Category: "Ulang Tahun", EventType: "ulang-tahun", Tier: "free", Premium: false, PreviewImage: "/themes/previews/ultah-sirkus.webp", PreviewURL: "/invitation/demo?template=ultah-sirkus", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 410},
		{ID: "ultah-pertama", Name: "Ultah Pertama", Slug: "ultah-pertama", Description: "Ulang tahun pertama si kecil: boneka beruang, huruf balok, dan kue mungil.", Category: "Ulang Tahun", EventType: "ulang-tahun", Tier: "free", Premium: false, PreviewImage: "/themes/previews/ultah-pertama.webp", PreviewURL: "/invitation/demo?template=ultah-pertama", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 411},
		{ID: "pengajian-akbar", Name: "Pengajian Akbar", Slug: "pengajian-akbar", Description: "Undangan pengajian dan majelis taklim yang teduh dengan nuansa hijau dan emas.", Category: "Pengajian", EventType: "lainnya", Tier: "free", Premium: false, PreviewImage: "/themes/previews/pengajian-akbar.webp", PreviewURL: "/invitation/demo?template=pengajian-akbar", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 412},
		{ID: "peresmian-usaha", Name: "Peresmian Usaha", Slug: "peresmian-usaha", Description: "Peresmian usaha atau toko baru: pita gunting, papan bunga, dan konfeti.", Category: "Peresmian", EventType: "lainnya", Tier: "free", Premium: false, PreviewImage: "/themes/previews/peresmian-usaha.webp", PreviewURL: "/invitation/demo?template=peresmian-usaha", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 413},
		{ID: "rote-sasando", Name: "Rote Sasando", Slug: "rote-sasando", Description: "Sasando berdawai dari daun lontar, topi ti'i langga, dan pantai Nemberala Pulau Rote.", Category: "Adat NTT", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/rote-sasando.webp", PreviewURL: "/invitation/demo?template=rote-sasando", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 420},
		{ID: "ternate-gamalama", Name: "Ternate Gamalama", Slug: "ternate-gamalama", Description: "Kesultanan Ternate di kaki Gamalama, pala dan cengkih, serta laut biru Halmahera.", Category: "Adat Maluku Utara", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/ternate-gamalama.webp", PreviewURL: "/invitation/demo?template=ternate-gamalama", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 421},
		{ID: "pinisi-makassar", Name: "Pinisi Makassar", Slug: "pinisi-makassar", Description: "Kapal pinisi berlayar tujuh, pantai Losari saat senja, dan sarung sutra Makassar.", Category: "Adat Makassar", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/pinisi-makassar.webp", PreviewURL: "/invitation/demo?template=pinisi-makassar", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 422},
		{ID: "minang-pandai-sikek", Name: "Pandai Sikek", Slug: "minang-pandai-sikek", Description: "Songket Pandai Sikek bertabur benang emas, ngarai hijau, dan ukiran Minang.", Category: "Adat Minang", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/minang-pandai-sikek.webp", PreviewURL: "/invitation/demo?template=minang-pandai-sikek", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 423},
		{ID: "raja-ampat", Name: "Raja Ampat", Slug: "raja-ampat", Description: "Gugusan pulau karst Raja Ampat, laut toska jernih, dan langit Papua yang luas.", Category: "Adat Papua", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/raja-ampat.webp", PreviewURL: "/invitation/demo?template=raja-ampat", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 424},
		{ID: "karo-siwaluh", Name: "Karo Siwaluh", Slug: "karo-siwaluh", Description: "Rumah adat siwaluh jabu, uis Karo, dan dataran tinggi Berastagi di kaki Sinabung.", Category: "Adat Karo", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/karo-siwaluh.webp", PreviewURL: "/invitation/demo?template=karo-siwaluh", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 425},
		{ID: "fes-tembaga", Name: "Fes Tembaga", Slug: "fes-tembaga", Description: "Lentera tembaga berlubang, dinding tadelakt, dan cahaya hangat ala riad Fes.", Category: "Islami", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/fes-tembaga.webp", PreviewURL: "/invitation/demo?template=fes-tembaga", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 426},
		{ID: "mamluk-kairo", Name: "Mamluk Kairo", Slug: "mamluk-kairo", Description: "Batu ablaq bergaris, muqarnas, dan lampu kuningan ala Kairo era Mamluk.", Category: "Islami", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/mamluk-kairo.webp", PreviewURL: "/invitation/demo?template=mamluk-kairo", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 427},
		{ID: "bulan-bintang", Name: "Bulan Bintang", Slug: "bulan-bintang", Description: "Tanpa foto: bulan sabit dan bintang di langit pastel yang lembut dan tenang.", Category: "Syari", EventType: "wedding", Tier: "free", Premium: false, PreviewImage: "/themes/previews/bulan-bintang.webp", PreviewURL: "/invitation/demo?template=bulan-bintang", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 428},
		{ID: "garis-geometri", Name: "Garis Geometri", Slug: "garis-geometri", Description: "Geometri Islami bergaris tipis hitam-putih yang modern dan bersih.", Category: "Islami", EventType: "wedding", Tier: "free", Premium: false, PreviewImage: "/themes/previews/garis-geometri.webp", PreviewURL: "/invitation/demo?template=garis-geometri", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 429},
		{ID: "mawar-taif", Name: "Mawar Taif", Slug: "mawar-taif", Description: "Ladang mawar Taif merah muda, kelopak yang bertebaran, dan lembah berbatu.", Category: "Islami", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/mawar-taif.webp", PreviewURL: "/invitation/demo?template=mawar-taif", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 430},
		{ID: "pesantren-teduh", Name: "Pesantren Teduh", Slug: "pesantren-teduh", Description: "Halaman pesantren yang teduh: surau kayu, pohon kamboja, dan bedug di serambi.", Category: "Islami", EventType: "wedding", Tier: "free", Premium: false, PreviewImage: "/themes/previews/pesantren-teduh.webp", PreviewURL: "/invitation/demo?template=pesantren-teduh", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 431},
		{ID: "retro-70an", Name: "Retro 70an", Slug: "retro-70an", Description: "Gaya retro 70-an: matahari bergaris, jingga-cokelat, dan huruf yang groovy.", Category: "Retro", EventType: "wedding", Tier: "free", Premium: false, PreviewImage: "/themes/previews/retro-70an.webp", PreviewURL: "/invitation/demo?template=retro-70an", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 432},
		{ID: "merak-nouveau", Name: "Merak Nouveau", Slug: "merak-nouveau", Description: "Bulu merak dan garis lengkung art nouveau dalam toska, zamrud, dan emas.", Category: "Vintage", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/merak-nouveau.webp", PreviewURL: "/invitation/demo?template=merak-nouveau", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 433},
		{ID: "shan-shui", Name: "Shan Shui", Slug: "shan-shui", Description: "Lukisan tinta pegunungan ala shan shui dengan kabut, pinus, dan air terjun.", Category: "Floral", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/shan-shui.webp", PreviewURL: "/invitation/demo?template=shan-shui", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 434},
		{ID: "gurun-kaktus", Name: "Gurun Kaktus", Slug: "gurun-kaktus", Description: "Kaktus dan sukulen gurun dengan warna terakota dan senja yang hangat.", Category: "Boho", EventType: "wedding", Tier: "free", Premium: false, PreviewImage: "/themes/previews/gurun-kaktus.webp", PreviewURL: "/invitation/demo?template=gurun-kaktus", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 435},
		{ID: "kolase-kertas", Name: "Kolase Kertas", Slug: "kolase-kertas", Description: "Kolase potongan kertas berwarna dengan bentuk organik yang ceria.", Category: "Modern", EventType: "wedding", Tier: "free", Premium: false, PreviewImage: "/themes/previews/kolase-kertas.webp", PreviewURL: "/invitation/demo?template=kolase-kertas", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 436},
		{ID: "kebun-teh", Name: "Kebun Teh", Slug: "kebun-teh", Description: "Hamparan kebun teh Puncak yang hijau berundak dengan kabut pagi.", Category: "Pemandangan", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/kebun-teh.webp", PreviewURL: "/invitation/demo?template=kebun-teh", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 437},
		{ID: "ultah-truk", Name: "Ultah Truk", Slug: "ultah-truk", Description: "Ulang tahun anak bertema mobil dan truk konstruksi yang ramah.", Category: "Ulang Tahun", EventType: "ulang-tahun", Tier: "free", Premium: false, PreviewImage: "/themes/previews/ultah-truk.webp", PreviewURL: "/invitation/demo?template=ultah-truk", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 438},
		{ID: "ultah-safari", Name: "Ultah Safari", Slug: "ultah-safari", Description: "Ulang tahun bertema safari: jerapah, gajah, singa lucu di padang rumput.", Category: "Ulang Tahun", EventType: "ulang-tahun", Tier: "free", Premium: false, PreviewImage: "/themes/previews/ultah-safari.webp", PreviewURL: "/invitation/demo?template=ultah-safari", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 439},
		{ID: "ultah-samudra", Name: "Ultah Samudra", Slug: "ultah-samudra", Description: "Ulang tahun bawah laut: kapal selam kuning, ikan, dan gurita ramah.", Category: "Ulang Tahun", EventType: "ulang-tahun", Tier: "free", Premium: false, PreviewImage: "/themes/previews/ultah-samudra.webp", PreviewURL: "/invitation/demo?template=ultah-samudra", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 440},
		{ID: "bridal-shower", Name: "Bridal Shower", Slug: "bridal-shower", Description: "Bridal shower yang manis: sampanye merah muda, bunga, dan pita.", Category: "Bridal Shower", EventType: "lainnya", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/bridal-shower.webp", PreviewURL: "/invitation/demo?template=bridal-shower", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 441},
		{ID: "prom-perpisahan", Name: "Prom Perpisahan", Slug: "prom-perpisahan", Description: "Malam perpisahan SMA yang gemerlap dengan bola disko dan lampu panggung.", Category: "Perpisahan", EventType: "lainnya", Tier: "free", Premium: false, PreviewImage: "/themes/previews/prom-perpisahan.webp", PreviewURL: "/invitation/demo?template=prom-perpisahan", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 442},
		{ID: "pembaptisan", Name: "Pembaptisan", Slug: "pembaptisan", Description: "Undangan pembaptisan anak yang teduh: merpati, air, dan cahaya lembut.", Category: "Baptis", EventType: "lainnya", Tier: "free", Premium: false, PreviewImage: "/themes/previews/pembaptisan.webp", PreviewURL: "/invitation/demo?template=pembaptisan", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 443},
		{ID: "kutai-erau", Name: "Kutai Erau", Slug: "kutai-erau", Description: "Kemegahan Kesultanan Kutai Kartanegara: Mahakam, ukiran Kutai, dan kuning-hijau keraton.", Category: "Adat Kutai", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/kutai-erau.webp", PreviewURL: "/invitation/demo?template=kutai-erau", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 450},
		{ID: "bima-mbojo", Name: "Bima Mbojo", Slug: "bima-mbojo", Description: "Lumbung uma lengge, tenun tembe nggoli, dan teluk Bima yang tenang.", Category: "Adat Bima", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/bima-mbojo.webp", PreviewURL: "/invitation/demo?template=bima-mbojo", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 451},
		{ID: "simalungun-bolon", Name: "Simalungun Bolon", Slug: "simalungun-bolon", Description: "Rumah bolon Simalungun, kain hiou, dan Danau Toba dari sisi timur.", Category: "Adat Simalungun", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/simalungun-bolon.webp", PreviewURL: "/invitation/demo?template=simalungun-bolon", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 452},
		{ID: "mandailing-gordang", Name: "Mandailing Gordang", Slug: "mandailing-gordang", Description: "Bagas godang, gendang gordang sambilan, dan perbukitan Tapanuli Selatan.", Category: "Adat Mandailing", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/mandailing-gordang.webp", PreviewURL: "/invitation/demo?template=mandailing-gordang", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 453},
		{ID: "bromo-tengger", Name: "Bromo Tengger", Slug: "bromo-tengger", Description: "Lautan pasir Bromo saat fajar, bukit Teletubbies, dan kabut Tengger.", Category: "Adat Tengger", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/bromo-tengger.webp", PreviewURL: "/invitation/demo?template=bromo-tengger", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 454},
		{ID: "sentani-kayu", Name: "Sentani Kayu", Slug: "sentani-kayu", Description: "Lukisan kulit kayu kombouw Sentani dan danau berpulau di bawah Cycloop.", Category: "Adat Papua", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/sentani-kayu.webp", PreviewURL: "/invitation/demo?template=sentani-kayu", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 455},
		{ID: "zanzibar-pintu", Name: "Zanzibar Pintu", Slug: "zanzibar-pintu", Description: "Pintu kayu berukir Swahili bertabur paku kuningan dan perahu dhow di laut.", Category: "Islami", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/zanzibar-pintu.webp", PreviewURL: "/invitation/demo?template=zanzibar-pintu", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 456},
		{ID: "suzani-bukhara", Name: "Suzani Bukhara", Slug: "suzani-bukhara", Description: "Sulaman suzani Bukhara: medali bunga besar merah delima dan nila di kain krem.", Category: "Islami", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/suzani-bukhara.webp", PreviewURL: "/invitation/demo?template=suzani-bukhara", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 457},
		{ID: "tegel-kunci", Name: "Tegel Kunci", Slug: "tegel-kunci", Description: "Tegel kunci jadul bermotif bunga ala rumah lama Nusantara yang hangat.", Category: "Islami", EventType: "wedding", Tier: "free", Premium: false, PreviewImage: "/themes/previews/tegel-kunci.webp", PreviewURL: "/invitation/demo?template=tegel-kunci", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 458},
		{ID: "daun-embun", Name: "Daun Embun", Slug: "daun-embun", Description: "Tanpa foto: daun hijau segar berembun pagi yang bening dan menenangkan.", Category: "Syari", EventType: "wedding", Tier: "free", Premium: false, PreviewImage: "/themes/previews/daun-embun.webp", PreviewURL: "/invitation/demo?template=daun-embun", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 459},
		{ID: "chefchaouen-biru", Name: "Chefchaouen Biru", Slug: "chefchaouen-biru", Description: "Lorong biru Chefchaouen dengan tangga, pot bunga, dan pintu lengkung.", Category: "Islami", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/chefchaouen-biru.webp", PreviewURL: "/invitation/demo?template=chefchaouen-biru", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 460},
		{ID: "langgar-sawah", Name: "Langgar Sawah", Slug: "langgar-sawah", Description: "Langgar kayu kecil di tepi sawah hijau dengan pohon kelapa dan pematang.", Category: "Islami", EventType: "wedding", Tier: "free", Premium: false, PreviewImage: "/themes/previews/langgar-sawah.webp", PreviewURL: "/invitation/demo?template=langgar-sawah", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 461},
		{ID: "abstrak-sapuan", Name: "Abstrak Sapuan", Slug: "abstrak-sapuan", Description: "Sapuan kuas abstrak berwarna lembut ala lukisan kontemporer.", Category: "Modern", EventType: "wedding", Tier: "free", Premium: false, PreviewImage: "/themes/previews/abstrak-sapuan.webp", PreviewURL: "/invitation/demo?template=abstrak-sapuan", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 462},
		{ID: "kota-tua-batavia", Name: "Kota Tua Batavia", Slug: "kota-tua-batavia", Description: "Gedung-gedung kolonial Kota Tua, sepeda onthel, dan cahaya sore Batavia.", Category: "Vintage", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/kota-tua-batavia.webp", PreviewURL: "/invitation/demo?template=kota-tua-batavia", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 463},
		{ID: "balkon-paris", Name: "Balkon Paris", Slug: "balkon-paris", Description: "Balkon besi tempa Paris dengan lilac musim semi dan jendela krem.", Category: "Floral", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/balkon-paris.webp", PreviewURL: "/invitation/demo?template=balkon-paris", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 464},
		{ID: "lemon-amalfi", Name: "Lemon Amalfi", Slug: "lemon-amalfi", Description: "Lemon Amalfi, ubin majolika biru-kuning, dan pantai Mediterania yang cerah.", Category: "Garden", EventType: "wedding", Tier: "free", Premium: false, PreviewImage: "/themes/previews/lemon-amalfi.webp", PreviewURL: "/invitation/demo?template=lemon-amalfi", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 465},
		{ID: "hutan-bambu", Name: "Hutan Bambu", Slug: "hutan-bambu", Description: "Hutan bambu hijau yang menjulang dengan cahaya yang menembus celah daun.", Category: "Pemandangan", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/hutan-bambu.webp", PreviewURL: "/invitation/demo?template=hutan-bambu", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 466},
		{ID: "cahaya-lilin", Name: "Cahaya Lilin", Slug: "cahaya-lilin", Description: "Makan malam romantis bercahaya lilin: hangat, gelap, dan berkilau.", Category: "Elegan", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/cahaya-lilin.webp", PreviewURL: "/invitation/demo?template=cahaya-lilin", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 467},
		{ID: "ultah-balerina", Name: "Ultah Balerina", Slug: "ultah-balerina", Description: "Ulang tahun anak bertema balet: tutu, sepatu balet, dan panggung merah muda.", Category: "Ulang Tahun", EventType: "ulang-tahun", Tier: "free", Premium: false, PreviewImage: "/themes/previews/ultah-balerina.webp", PreviewURL: "/invitation/demo?template=ultah-balerina", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 468},
		{ID: "siraman-adat", Name: "Siraman Adat", Slug: "siraman-adat", Description: "Upacara siraman calon pengantin: kembang setaman, kendi, dan janur.", Category: "Siraman", EventType: "syukuran", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/siraman-adat.webp", PreviewURL: "/invitation/demo?template=siraman-adat", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 469},
		{ID: "tunangan-modern", Name: "Tunangan Modern", Slug: "tunangan-modern", Description: "Tunangan bergaya modern minimalis dengan cincin dan garis tipis.", Category: "Tunangan", EventType: "tunangan", Tier: "free", Premium: false, PreviewImage: "/themes/previews/tunangan-modern.webp", PreviewURL: "/invitation/demo?template=tunangan-modern", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 470},
		{ID: "pesta-kebun", Name: "Pesta Kebun", Slug: "pesta-kebun", Description: "Pesta ulang tahun dewasa di kebun: lampu gantung, meja panjang, dan bunga.", Category: "Ulang Tahun", EventType: "ulang-tahun", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/pesta-kebun.webp", PreviewURL: "/invitation/demo?template=pesta-kebun", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 471},
		{ID: "wisuda-santri", Name: "Wisuda Santri", Slug: "wisuda-santri", Description: "Wisuda santri dan khataman pesantren dengan nuansa hijau-putih yang teduh.", Category: "Wisuda", EventType: "wisuda", Tier: "free", Premium: false, PreviewImage: "/themes/previews/wisuda-santri.webp", PreviewURL: "/invitation/demo?template=wisuda-santri", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 472},
		{ID: "gender-reveal", Name: "Gender Reveal", Slug: "gender-reveal", Description: "Pesta tebak jenis kelamin bayi: balon biru dan merah muda yang ceria.", Category: "Syukuran", EventType: "syukuran", Tier: "free", Premium: false, PreviewImage: "/themes/previews/gender-reveal.webp", PreviewURL: "/invitation/demo?template=gender-reveal", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 473},
		{ID: "gayo-kerawang", Name: "Gayo Kerawang", Slug: "gayo-kerawang", Description: "Sulaman kerawang Gayo, kebun kopi dataran tinggi, dan Danau Lut Tawar berkabut.", Category: "Adat Gayo", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/gayo-kerawang.webp", PreviewURL: "/invitation/demo?template=gayo-kerawang", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 480},
		{ID: "kerinci-danau", Name: "Kerinci Danau", Slug: "kerinci-danau", Description: "Gunung Kerinci, Danau Kerinci, kebun teh lereng, dan ukiran rumah larik.", Category: "Adat Kerinci", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/kerinci-danau.webp", PreviewURL: "/invitation/demo?template=kerinci-danau", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 481},
		{ID: "priangan-kacapi", Name: "Priangan Kacapi", Slug: "priangan-kacapi", Description: "Kacapi suling, sawah terasering Priangan, dan anyaman bambu yang hangat.", Category: "Adat Sunda", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/priangan-kacapi.webp", PreviewURL: "/invitation/demo?template=priangan-kacapi", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 482},
		{ID: "sumba-hinggi", Name: "Sumba Hinggi", Slug: "sumba-hinggi", Description: "Kain hinggi Sumba, rumah beratap menara, padang sabana, dan kuda sandel.", Category: "Adat Sumba", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/sumba-hinggi.webp", PreviewURL: "/invitation/demo?template=sumba-hinggi", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 483},
		{ID: "kaili-souraja", Name: "Kaili Souraja", Slug: "kaili-souraja", Description: "Rumah Souraja, tenun Donggala, dan Teluk Palu di bawah lembah hijau.", Category: "Adat Kaili", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/kaili-souraja.webp", PreviewURL: "/invitation/demo?template=kaili-souraja", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 484},
		{ID: "tolaki-kendari", Name: "Tolaki Kendari", Slug: "tolaki-kendari", Description: "Tenun Tolaki merah-emas, rumah laika, dan Teluk Kendari saat senja.", Category: "Adat Tolaki", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/tolaki-kendari.webp", PreviewURL: "/invitation/demo?template=tolaki-kendari", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 485},
		{ID: "menara-kudus", Name: "Menara Kudus", Slug: "menara-kudus", Description: "Menara bata merah Kudus, gapura paduraksa, dan tegel hijau yang teduh.", Category: "Islami", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/menara-kudus.webp", PreviewURL: "/invitation/demo?template=menara-kudus", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 486},
		{ID: "sajadah-beludru", Name: "Sajadah Beludru", Slug: "sajadah-beludru", Description: "Motif sajadah beludru: relung mihrab, rumbai, dan bordir emas di merah anggur.", Category: "Islami", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/sajadah-beludru.webp", PreviewURL: "/invitation/demo?template=sajadah-beludru", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 487},
		{ID: "mezquita-cordoba", Name: "Mezquita Cordoba", Slug: "mezquita-cordoba", Description: "Lengkung bergaris merah-putih ala Cordoba, kolom berderet, dan cahaya keemasan.", Category: "Islami", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/mezquita-cordoba.webp", PreviewURL: "/invitation/demo?template=mezquita-cordoba", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 488},
		{ID: "sage-syari", Name: "Sage Syari", Slug: "sage-syari", Description: "Tanpa foto: hijau sage, daun kering, dan linen lembut yang tenang.", Category: "Syari", EventType: "wedding", Tier: "free", Premium: false, PreviewImage: "/themes/previews/sage-syari.webp", PreviewURL: "/invitation/demo?template=sage-syari", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 489},
		{ID: "girih-emas", Name: "Girih Emas", Slug: "girih-emas", Description: "Ubin girih Persia bergaris emas di biru malam yang dalam.", Category: "Islami", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/girih-emas.webp", PreviewURL: "/invitation/demo?template=girih-emas", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 490},
		{ID: "lengkung-putih", Name: "Lengkung Putih", Slug: "lengkung-putih", Description: "Lengkung gading berderet dengan garis emas tipis: syar'i, bersih, modern.", Category: "Syari", EventType: "wedding", Tier: "free", Premium: false, PreviewImage: "/themes/previews/lengkung-putih.webp", PreviewURL: "/invitation/demo?template=lengkung-putih", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 491},
		{ID: "kintsugi-emas", Name: "Kintsugi Emas", Slug: "kintsugi-emas", Description: "Keramik retak yang disatukan emas: lambang cinta yang makin indah dari waktu ke waktu.", Category: "Modern", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/kintsugi-emas.webp", PreviewURL: "/invitation/demo?template=kintsugi-emas", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 492},
		{ID: "aurora-utara", Name: "Aurora Utara", Slug: "aurora-utara", Description: "Cahaya aurora hijau-ungu di atas danau beku dan hutan pinus bersalju.", Category: "Pemandangan", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/aurora-utara.webp", PreviewURL: "/invitation/demo?template=aurora-utara", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 493},
		{ID: "ladang-tulip", Name: "Ladang Tulip", Slug: "ladang-tulip", Description: "Ladang tulip berwarna-warni, kincir angin, dan langit musim semi.", Category: "Floral", EventType: "wedding", Tier: "free", Premium: false, PreviewImage: "/themes/previews/ladang-tulip.webp", PreviewURL: "/invitation/demo?template=ladang-tulip", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 494},
		{ID: "perpustakaan-tua", Name: "Perpustakaan Tua", Slug: "perpustakaan-tua", Description: "Rak buku kayu, tangga perpustakaan, lampu meja hijau, dan kertas tua.", Category: "Vintage", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/perpustakaan-tua.webp", PreviewURL: "/invitation/demo?template=perpustakaan-tua", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 495},
		{ID: "film-analog", Name: "Film Analog", Slug: "film-analog", Description: "Gulungan film 35mm, cetak foto berbingkai, dan warna hangat kamera analog.", Category: "Retro", EventType: "wedding", Tier: "free", Premium: false, PreviewImage: "/themes/previews/film-analog.webp", PreviewURL: "/invitation/demo?template=film-analog", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 496},
		{ID: "opera-beludru", Name: "Opera Beludru", Slug: "opera-beludru", Description: "Tirai beludru merah, balkon opera bersepuh emas, dan lampu kristal.", Category: "Luxury", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/opera-beludru.webp", PreviewURL: "/invitation/demo?template=opera-beludru", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 497},
		{ID: "kawin-emas", Name: "Kawin Emas", Slug: "kawin-emas", Description: "Syukuran 50 tahun pernikahan: emas hangat, album kenangan, dan bunga krisan.", Category: "Ulang Tahun Pernikahan", EventType: "syukuran", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/kawin-emas.webp", PreviewURL: "/invitation/demo?template=kawin-emas", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 498},
		{ID: "ultah-kucing", Name: "Ultah Kucing", Slug: "ultah-kucing", Description: "Ulang tahun anak bertema kucing: bola benang, kardus, dan kue ikan.", Category: "Ulang Tahun", EventType: "ulang-tahun", Tier: "free", Premium: false, PreviewImage: "/themes/previews/ultah-kucing.webp", PreviewURL: "/invitation/demo?template=ultah-kucing", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 499},
		{ID: "ultah-melukis", Name: "Ultah Melukis", Slug: "ultah-melukis", Description: "Pesta ulang tahun melukis: palet warna, krayon, dan cipratan cat ceria.", Category: "Ulang Tahun", EventType: "ulang-tahun", Tier: "free", Premium: false, PreviewImage: "/themes/previews/ultah-melukis.webp", PreviewURL: "/invitation/demo?template=ultah-melukis", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 500},
		{ID: "lomba-17an", Name: "Lomba 17-an", Slug: "lomba-17an", Description: "Undangan lomba Agustusan warga: panjat pinang, balap karung, dan bendera merah putih.", Category: "Acara Warga", EventType: "lainnya", Tier: "free", Premium: false, PreviewImage: "/themes/previews/lomba-17an.webp", PreviewURL: "/invitation/demo?template=lomba-17an", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 501},
		{ID: "buka-bersama", Name: "Buka Bersama", Slug: "buka-bersama", Description: "Undangan bukber Ramadan: kurma, lentera, dan meja panjang menjelang magrib.", Category: "Buka Bersama", EventType: "lainnya", Tier: "free", Premium: false, PreviewImage: "/themes/previews/buka-bersama.webp", PreviewURL: "/invitation/demo?template=buka-bersama", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 502},
		{ID: "imlek-keluarga", Name: "Imlek Keluarga", Slug: "imlek-keluarga", Description: "Makan malam Imlek keluarga: lampion merah, bunga meihua, dan jeruk mandarin.", Category: "Imlek", EventType: "lainnya", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/imlek-keluarga.webp", PreviewURL: "/invitation/demo?template=imlek-keluarga", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 503},
		{ID: "pakpak-dairi", Name: "Pakpak Dairi", Slug: "pakpak-dairi", Description: "Rumah adat Pakpak, kain oles, dan perbukitan Dairi yang hijau berkabut.", Category: "Adat Pakpak", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/pakpak-dairi.webp", PreviewURL: "/invitation/demo?template=pakpak-dairi", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 504},
		{ID: "banten-surosowan", Name: "Banten Surosowan", Slug: "banten-surosowan", Description: "Reruntuhan Keraton Surosowan, menara Banten, dan batik Banten berwarna lembut.", Category: "Adat Banten", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/banten-surosowan.webp", PreviewURL: "/invitation/demo?template=banten-surosowan", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 505},
		{ID: "kotagede-perak", Name: "Kotagede Perak", Slug: "kotagede-perak", Description: "Kerajinan perak filigri Kotagede, gang rumah kalang, dan nuansa Mataram lama.", Category: "Adat Jawa", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/kotagede-perak.webp", PreviewURL: "/invitation/demo?template=kotagede-perak", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 506},
		{ID: "timor-tais", Name: "Timor Tais", Slug: "timor-tais", Description: "Kain tais Timor, rumah bulat ume kbubu, dan padang lontar di bawah langit biru.", Category: "Adat NTT", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/timor-tais.webp", PreviewURL: "/invitation/demo?template=timor-tais", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 507},
		{ID: "alor-moko", Name: "Alor Moko", Slug: "alor-moko", Description: "Moko perunggu Alor, tenun ikat, dan teluk biru jernih Kepulauan Alor.", Category: "Adat NTT", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/alor-moko.webp", PreviewURL: "/invitation/demo?template=alor-moko", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 508},
		{ID: "baliem-honai", Name: "Baliem Honai", Slug: "baliem-honai", Description: "Lembah Baliem, honai beratap jerami, dan noken anyaman di pegunungan Papua.", Category: "Adat Papua", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/baliem-honai.webp", PreviewURL: "/invitation/demo?template=baliem-honai", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 509},
		{ID: "riad-jeruk", Name: "Riad Jeruk", Slug: "riad-jeruk", Description: "Halaman riad Maroko dengan air mancur, pohon jeruk, dan ubin zellige lembut.", Category: "Islami", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/riad-jeruk.webp", PreviewURL: "/invitation/demo?template=riad-jeruk", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 510},
		{ID: "paisley-kashmir", Name: "Paisley Kashmir", Slug: "paisley-kashmir", Description: "Motif boteh selendang Kashmir yang halus dalam merah kunyit dan hijau.", Category: "Islami", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/paisley-kashmir.webp", PreviewURL: "/invitation/demo?template=paisley-kashmir", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 511},
		{ID: "mawar-debu", Name: "Mawar Debu", Slug: "mawar-debu", Description: "Tanpa foto: dusty rose lembut, mawar kering, dan pita satin yang anggun.", Category: "Syari", EventType: "wedding", Tier: "free", Premium: false, PreviewImage: "/themes/previews/mawar-debu.webp", PreviewURL: "/invitation/demo?template=mawar-debu", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 512},
		{ID: "ukir-jepara", Name: "Ukir Jepara", Slug: "ukir-jepara", Description: "Ukiran kayu jati Jepara bermotif sulur bunga, hangat dan megah.", Category: "Islami", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/ukir-jepara.webp", PreviewURL: "/invitation/demo?template=ukir-jepara", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 513},
		{ID: "ikat-adras", Name: "Ikat Adras", Slug: "ikat-adras", Description: "Kain ikat sutra adras Asia Tengah dengan motif awan berwarna berani.", Category: "Islami", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/ikat-adras.webp", PreviewURL: "/invitation/demo?template=ikat-adras", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 514},
		{ID: "safir-malam", Name: "Safir Malam", Slug: "safir-malam", Description: "Tanpa foto: biru safir dan perak dengan bintang geometri yang tenang.", Category: "Syari", EventType: "wedding", Tier: "free", Premium: false, PreviewImage: "/themes/previews/safir-malam.webp", PreviewURL: "/invitation/demo?template=safir-malam", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 515},
		{ID: "bauhaus-primer", Name: "Bauhaus Primer", Slug: "bauhaus-primer", Description: "Bentuk dasar lingkaran, segitiga, dan persegi dalam merah, kuning, biru.", Category: "Modern", EventType: "wedding", Tier: "free", Premium: false, PreviewImage: "/themes/previews/bauhaus-primer.webp", PreviewURL: "/invitation/demo?template=bauhaus-primer", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 516},
		{ID: "taman-zen", Name: "Taman Zen", Slug: "taman-zen", Description: "Taman batu Jepang: pasir bergaris, batu berlumut, dan maple merah.", Category: "Minimalis", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/taman-zen.webp", PreviewURL: "/invitation/demo?template=taman-zen", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 517},
		{ID: "pondok-inggris", Name: "Pondok Inggris", Slug: "pondok-inggris", Description: "Pondok batu bergaya Inggris dengan kebun bunga liar dan mawar merambat.", Category: "Garden", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/pondok-inggris.webp", PreviewURL: "/invitation/demo?template=pondok-inggris", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 518},
		{ID: "poster-wisata", Name: "Poster Wisata", Slug: "poster-wisata", Description: "Gaya poster wisata lawas dengan panorama Nusantara yang cerah.", Category: "Retro", EventType: "wedding", Tier: "free", Premium: false, PreviewImage: "/themes/previews/poster-wisata.webp", PreviewURL: "/invitation/demo?template=poster-wisata", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 519},
		{ID: "piringan-hitam", Name: "Piringan Hitam", Slug: "piringan-hitam", Description: "Piringan hitam, sampul album, dan nuansa klub jazz yang hangat.", Category: "Retro", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/piringan-hitam.webp", PreviewURL: "/invitation/demo?template=piringan-hitam", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 520},
		{ID: "kolam-teratai", Name: "Kolam Teratai", Slug: "kolam-teratai", Description: "Kolam teratai bergaya impresionis dengan jembatan kayu dan cahaya pagi.", Category: "Cat Air", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/kolam-teratai.webp", PreviewURL: "/invitation/demo?template=kolam-teratai", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 521},
		{ID: "ultah-robot", Name: "Ultah Robot", Slug: "ultah-robot", Description: "Ulang tahun anak bertema robot: roda gigi, lampu kedip, dan kue robot.", Category: "Ulang Tahun", EventType: "ulang-tahun", Tier: "free", Premium: false, PreviewImage: "/themes/previews/ultah-robot.webp", PreviewURL: "/invitation/demo?template=ultah-robot", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 522},
		{ID: "ultah-peri", Name: "Ultah Peri", Slug: "ultah-peri", Description: "Ulang tahun anak di hutan peri: jamur, kunang-kunang, dan bunga ajaib.", Category: "Ulang Tahun", EventType: "ulang-tahun", Tier: "free", Premium: false, PreviewImage: "/themes/previews/ultah-peri.webp", PreviewURL: "/invitation/demo?template=ultah-peri", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 523},
		{ID: "maulid-nabi", Name: "Maulid Nabi", Slug: "maulid-nabi", Description: "Undangan peringatan Maulid Nabi: lentera, hiasan janur, dan nuansa hijau-emas.", Category: "Pengajian", EventType: "lainnya", Tier: "free", Premium: false, PreviewImage: "/themes/previews/maulid-nabi.webp", PreviewURL: "/invitation/demo?template=maulid-nabi", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 524},
		{ID: "arisan-keluarga", Name: "Arisan Keluarga", Slug: "arisan-keluarga", Description: "Undangan arisan keluarga: kocokan, teh manis, dan kue-kue tradisional.", Category: "Arisan", EventType: "lainnya", Tier: "free", Premium: false, PreviewImage: "/themes/previews/arisan-keluarga.webp", PreviewURL: "/invitation/demo?template=arisan-keluarga", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 525},
		{ID: "peluncuran-buku", Name: "Peluncuran Buku", Slug: "peluncuran-buku", Description: "Undangan peluncuran buku: tumpukan buku, pena, dan panggung diskusi.", Category: "Peluncuran", EventType: "lainnya", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/peluncuran-buku.webp", PreviewURL: "/invitation/demo?template=peluncuran-buku", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 526},
		{ID: "paskah-keluarga", Name: "Paskah Keluarga", Slug: "paskah-keluarga", Description: "Ibadah dan syukuran Paskah keluarga: bunga lili, taman pagi, dan telur hias.", Category: "Paskah", EventType: "lainnya", Tier: "free", Premium: false, PreviewImage: "/themes/previews/paskah-keluarga.webp", PreviewURL: "/invitation/demo?template=paskah-keluarga", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 527},
		{ID: "tidore-kadato", Name: "Tidore Kadato", Slug: "tidore-kadato", Description: "Kadato Kie Kesultanan Tidore, kebun cengkeh, dan Gunung Kie Matubu di atas laut.", Category: "Adat Tidore", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/tidore-kadato.webp", PreviewURL: "/invitation/demo?template=tidore-kadato", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 528},
		{ID: "mamasa-banua", Name: "Mamasa Banua", Slug: "mamasa-banua", Description: "Banua Mamasa beratap perahu, ukiran kayu berwarna, dan lembah pinus Sulawesi Barat.", Category: "Adat Mamasa", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/mamasa-banua.webp", PreviewURL: "/invitation/demo?template=mamasa-banua", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 529},
		{ID: "muna-kaghati", Name: "Muna Kaghati", Slug: "muna-kaghati", Description: "Layang-layang daun kolope Muna, tenun Muna bergaris, dan pantai karang Sultra.", Category: "Adat Muna", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/muna-kaghati.webp", PreviewURL: "/invitation/demo?template=muna-kaghati", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 530},
		{ID: "bali-endek", Name: "Bali Endek", Slug: "bali-endek", Description: "Kain endek Bali, penjor janur, dan sawah Ubud yang hijau berundak.", Category: "Adat Bali", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/bali-endek.webp", PreviewURL: "/invitation/demo?template=bali-endek", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 531},
		{ID: "lasem-tiga-negeri", Name: "Lasem Tiga Negeri", Slug: "lasem-tiga-negeri", Description: "Batik tiga negeri Lasem merah-biru-sogan dan rumah tua pesisir Jawa.", Category: "Adat Jawa", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/lasem-tiga-negeri.webp", PreviewURL: "/invitation/demo?template=lasem-tiga-negeri", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 532},
		{ID: "sambas-lunggi", Name: "Sambas Lunggi", Slug: "sambas-lunggi", Description: "Kain lunggi Sambas bertabur benang emas dan Keraton Alwatzikhoebillah di tepi sungai.", Category: "Adat Melayu", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/sambas-lunggi.webp", PreviewURL: "/invitation/demo?template=sambas-lunggi", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 533},
		{ID: "muqarnas-putih", Name: "Muqarnas Putih", Slug: "muqarnas-putih", Description: "Kubah muqarnas putih bersarang lebah dengan cahaya lembut dari atas.", Category: "Islami", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/muqarnas-putih.webp", PreviewURL: "/invitation/demo?template=muqarnas-putih", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 534},
		{ID: "bordir-tasik", Name: "Bordir Tasik", Slug: "bordir-tasik", Description: "Bordir kerancang Tasikmalaya yang halus di atas kain putih dan hijau pupus.", Category: "Islami", EventType: "wedding", Tier: "free", Premium: false, PreviewImage: "/themes/previews/bordir-tasik.webp", PreviewURL: "/invitation/demo?template=bordir-tasik", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 535},
		{ID: "latte-syari", Name: "Latte Syari", Slug: "latte-syari", Description: "Tanpa foto: warna kopi susu, krem, dan garis lengkung yang hangat dan rapi.", Category: "Syari", EventType: "wedding", Tier: "free", Premium: false, PreviewImage: "/themes/previews/latte-syari.webp", PreviewURL: "/invitation/demo?template=latte-syari", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 536},
		{ID: "sanaa-qamariya", Name: "Sanaa Qamariya", Slug: "sanaa-qamariya", Description: "Rumah menara Sana'a berbingkai gipsum putih dan jendela kaca qamariya berwarna.", Category: "Islami", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/sanaa-qamariya.webp", PreviewURL: "/invitation/demo?template=sanaa-qamariya", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 537},
		{ID: "bata-persia", Name: "Bata Persia", Slug: "bata-persia", Description: "Pola susunan bata Persia dengan sisipan ubin pirus yang hangat dan megah.", Category: "Islami", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/bata-persia.webp", PreviewURL: "/invitation/demo?template=bata-persia", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 538},
		{ID: "kapas-syari", Name: "Kapas Syari", Slug: "kapas-syari", Description: "Bunga kapas, linen krem, dan nuansa putih gading yang lembut dan bersahaja.", Category: "Syari", EventType: "wedding", Tier: "free", Premium: false, PreviewImage: "/themes/previews/kapas-syari.webp", PreviewURL: "/invitation/demo?template=kapas-syari", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 539},
		{ID: "memphis-80an", Name: "Memphis 80an", Slug: "memphis-80an", Description: "Gaya Memphis 80-an: garis zigzag, konfeti geometri, dan warna pastel berani.", Category: "Retro", EventType: "wedding", Tier: "free", Premium: false, PreviewImage: "/themes/previews/memphis-80an.webp", PreviewURL: "/invitation/demo?template=memphis-80an", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 540},
		{ID: "pop-art", Name: "Pop Art", Slug: "pop-art", Description: "Pop art berani: titik halftone, balon kata, dan warna primer yang meriah.", Category: "Modern", EventType: "wedding", Tier: "free", Premium: false, PreviewImage: "/themes/previews/pop-art.webp", PreviewURL: "/invitation/demo?template=pop-art", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 541},
		{ID: "flora-gelap", Name: "Flora Gelap", Slug: "flora-gelap", Description: "Rangkaian bunga ala lukisan klasik Belanda di latar gelap yang dramatis.", Category: "Floral", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/flora-gelap.webp", PreviewURL: "/invitation/demo?template=flora-gelap", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 542},
		{ID: "linocut-bunga", Name: "Linocut Bunga", Slug: "linocut-bunga", Description: "Cetak cukil lino bunga liar dua warna dengan tekstur tinta yang jujur.", Category: "Gambar Tangan", EventType: "wedding", Tier: "free", Premium: false, PreviewImage: "/themes/previews/linocut-bunga.webp", PreviewURL: "/invitation/demo?template=linocut-bunga", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 543},
		{ID: "nautika-biru", Name: "Nautika Biru", Slug: "nautika-biru", Description: "Nuansa bahari: garis biru-putih, tali tambang, jangkar, dan kompas kuningan.", Category: "Pantai", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/nautika-biru.webp", PreviewURL: "/invitation/demo?template=nautika-biru", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 544},
		{ID: "bunga-matahari", Name: "Bunga Matahari", Slug: "bunga-matahari", Description: "Ladang bunga matahari keemasan di bawah langit musim panas.", Category: "Garden", EventType: "wedding", Tier: "free", Premium: false, PreviewImage: "/themes/previews/bunga-matahari.webp", PreviewURL: "/invitation/demo?template=bunga-matahari", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 545},
		{ID: "ultah-bajak-laut", Name: "Ultah Bajak Laut", Slug: "ultah-bajak-laut", Description: "Ulang tahun anak petualang bajak laut: kapal, peta harta, dan pulau rahasia.", Category: "Ulang Tahun", EventType: "ulang-tahun", Tier: "free", Premium: false, PreviewImage: "/themes/previews/ultah-bajak-laut.webp", PreviewURL: "/invitation/demo?template=ultah-bajak-laut", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 546},
		{ID: "ultah-koki", Name: "Ultah Koki", Slug: "ultah-koki", Description: "Pesta ulang tahun koki cilik: topi koki, adonan kue, dan dapur warna-warni.", Category: "Ulang Tahun", EventType: "ulang-tahun", Tier: "free", Premium: false, PreviewImage: "/themes/previews/ultah-koki.webp", PreviewURL: "/invitation/demo?template=ultah-koki", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 547},
		{ID: "haul-tahlil", Name: "Haul & Tahlil", Slug: "haul-tahlil", Description: "Undangan haul dan tahlil keluarga yang teduh: hijau tua, melati, dan tasbih.", Category: "Tahlilan", EventType: "lainnya", Tier: "free", Premium: false, PreviewImage: "/themes/previews/haul-tahlil.webp", PreviewURL: "/invitation/demo?template=haul-tahlil", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 548},
		{ID: "gathering-kantor", Name: "Gathering Kantor", Slug: "gathering-kantor", Description: "Undangan family gathering kantor: tenda, permainan tim, dan suasana outbound.", Category: "Gathering", EventType: "lainnya", Tier: "free", Premium: false, PreviewImage: "/themes/previews/gathering-kantor.webp", PreviewURL: "/invitation/demo?template=gathering-kantor", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 549},
		{ID: "malam-tahun-baru", Name: "Malam Tahun Baru", Slug: "malam-tahun-baru", Description: "Pesta malam tahun baru: kembang api, hitung mundur, dan kilau emas.", Category: "Tahun Baru", EventType: "lainnya", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/malam-tahun-baru.webp", PreviewURL: "/invitation/demo?template=malam-tahun-baru", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 550},
		{ID: "seminar-ilmiah", Name: "Seminar Ilmiah", Slug: "seminar-ilmiah", Description: "Undangan seminar dan diskusi ilmiah: rapi, modern, dan informatif.", Category: "Seminar", EventType: "lainnya", Tier: "free", Premium: false, PreviewImage: "/themes/previews/seminar-ilmiah.webp", PreviewURL: "/invitation/demo?template=seminar-ilmiah", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 551},
		{ID: "banyumas-batik", Name: "Banyumas Batik", Slug: "banyumas-batik", Description: "Batik Banyumasan sogan-hitam, Gunung Slamet, dan kebun kelapa Jawa Tengah barat.", Category: "Adat Jawa", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/banyumas-batik.webp", PreviewURL: "/invitation/demo?template=banyumas-batik", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 552},
		{ID: "minang-suntiang", Name: "Minang Suntiang", Slug: "minang-suntiang", Description: "Suntiang emas pengantin Minang yang bertingkat, beludru merah, dan songket.", Category: "Adat Minang", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/minang-suntiang.webp", PreviewURL: "/invitation/demo?template=minang-suntiang", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 553},
		{ID: "asmat-ukir", Name: "Asmat Ukir", Slug: "asmat-ukir", Description: "Ukiran kayu Asmat bermotif alam, sungai berawa, dan perahu lesung panjang.", Category: "Adat Papua", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/asmat-ukir.webp", PreviewURL: "/invitation/demo?template=asmat-ukir", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 554},
		{ID: "banda-neira", Name: "Banda Neira", Slug: "banda-neira", Description: "Pala Banda, rumah perkenier tua, dan Gunung Api di tengah laut biru.", Category: "Adat Maluku", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/banda-neira.webp", PreviewURL: "/invitation/demo?template=banda-neira", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 555},
		{ID: "manggarai-lingko", Name: "Manggarai Lingko", Slug: "manggarai-lingko", Description: "Sawah lingko berbentuk jaring laba-laba dan rumah kerucut mbaru niang.", Category: "Adat NTT", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/manggarai-lingko.webp", PreviewURL: "/invitation/demo?template=manggarai-lingko", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 556},
		{ID: "bajo-laut", Name: "Bajo Laut", Slug: "bajo-laut", Description: "Kampung panggung suku Bajo di atas laut tosca, perahu lepa, dan karang.", Category: "Adat Bajo", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/bajo-laut.webp", PreviewURL: "/invitation/demo?template=bajo-laut", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 557},
		{ID: "cheng-ho", Name: "Cheng Ho", Slug: "cheng-ho", Description: "Masjid bergaya Tionghoa merah-hijau dengan atap pagoda dan lampion.", Category: "Islami", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/cheng-ho.webp", PreviewURL: "/invitation/demo?template=cheng-ho", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 558},
		{ID: "dahlia-syari", Name: "Dahlia Syari", Slug: "dahlia-syari", Description: "Tanpa foto: bunga dahlia terakota dan krem yang anggun dan hangat.", Category: "Syari", EventType: "wedding", Tier: "free", Premium: false, PreviewImage: "/themes/previews/dahlia-syari.webp", PreviewURL: "/invitation/demo?template=dahlia-syari", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 559},
		{ID: "jali-merah", Name: "Jali Merah", Slug: "jali-merah", Description: "Kisi-kisi jali batu pasir merah ala Fatehpur Sikri dan cahaya yang menembus.", Category: "Islami", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/jali-merah.webp", PreviewURL: "/invitation/demo?template=jali-merah", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 560},
		{ID: "renda-putih", Name: "Renda Putih", Slug: "renda-putih", Description: "Renda putih halus berlapis di atas satin gading: bersih dan syar'i.", Category: "Syari", EventType: "wedding", Tier: "free", Premium: false, PreviewImage: "/themes/previews/renda-putih.webp", PreviewURL: "/invitation/demo?template=renda-putih", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 561},
		{ID: "kaca-cermin", Name: "Kaca Cermin", Slug: "kaca-cermin", Description: "Mozaik kaca cermin berkilau ala istana Persia yang memantulkan cahaya.", Category: "Islami", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/kaca-cermin.webp", PreviewURL: "/invitation/demo?template=kaca-cermin", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 562},
		{ID: "batik-syari", Name: "Batik Syari", Slug: "batik-syari", Description: "Batik parang pastel yang lembut dan modern untuk undangan syar'i.", Category: "Syari", EventType: "wedding", Tier: "free", Premium: false, PreviewImage: "/themes/previews/batik-syari.webp", PreviewURL: "/invitation/demo?template=batik-syari", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 563},
		{ID: "malakit-hijau", Name: "Malakit Hijau", Slug: "malakit-hijau", Description: "Batu malakit hijau berpita dengan aksen emas yang mewah.", Category: "Luxury", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/malakit-hijau.webp", PreviewURL: "/invitation/demo?template=malakit-hijau", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 564},
		{ID: "hujan-kota", Name: "Hujan Kota", Slug: "hujan-kota", Description: "Malam kota yang hujan, payung, dan pantulan lampu di jalan basah.", Category: "Modern", EventType: "wedding", Tier: "free", Premium: false, PreviewImage: "/themes/previews/hujan-kota.webp", PreviewURL: "/invitation/demo?template=hujan-kota", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 565},
		{ID: "pesawat-kertas", Name: "Pesawat Kertas", Slug: "pesawat-kertas", Description: "Pesawat kertas yang terbang di langit biru dengan jejak garis putus.", Category: "Ilustrasi", EventType: "wedding", Tier: "free", Premium: false, PreviewImage: "/themes/previews/pesawat-kertas.webp", PreviewURL: "/invitation/demo?template=pesawat-kertas", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 566},
		{ID: "peta-bintang", Name: "Peta Bintang", Slug: "peta-bintang", Description: "Peta rasi bintang di malam pernikahan dengan garis emas yang tipis.", Category: "Pemandangan", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/peta-bintang.webp", PreviewURL: "/invitation/demo?template=peta-bintang", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 567},
		{ID: "piknik-gingham", Name: "Piknik Gingham", Slug: "piknik-gingham", Description: "Piknik di taman: kain kotak-kotak, keranjang rotan, dan buah segar.", Category: "Garden", EventType: "wedding", Tier: "free", Premium: false, PreviewImage: "/themes/previews/piknik-gingham.webp", PreviewURL: "/invitation/demo?template=piknik-gingham", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 568},
		{ID: "kertas-quilling", Name: "Kertas Quilling", Slug: "kertas-quilling", Description: "Seni kertas quilling: gulungan kertas warna-warni membentuk bunga.", Category: "Unik", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/kertas-quilling.webp", PreviewURL: "/invitation/demo?template=kertas-quilling", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 569},
		{ID: "ultah-pahlawan", Name: "Ultah Pahlawan", Slug: "ultah-pahlawan", Description: "Ulang tahun anak bertema pahlawan super ciptaan sendiri: jubah dan kota.", Category: "Ulang Tahun", EventType: "ulang-tahun", Tier: "free", Premium: false, PreviewImage: "/themes/previews/ultah-pahlawan.webp", PreviewURL: "/invitation/demo?template=ultah-pahlawan", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 570},
		{ID: "ultah-kereta", Name: "Ultah Kereta", Slug: "ultah-kereta", Description: "Ulang tahun anak bertema kereta api: rel, stasiun, dan gerbong warna-warni.", Category: "Ulang Tahun", EventType: "ulang-tahun", Tier: "free", Premium: false, PreviewImage: "/themes/previews/ultah-kereta.webp", PreviewURL: "/invitation/demo?template=ultah-kereta", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 571},
		{ID: "pulang-haji", Name: "Pulang Haji", Slug: "pulang-haji", Description: "Syukuran kepulangan haji: nuansa putih-hijau, payung, dan doa mabrur.", Category: "Syukuran", EventType: "syukuran", Tier: "free", Premium: false, PreviewImage: "/themes/previews/pulang-haji.webp", PreviewURL: "/invitation/demo?template=pulang-haji", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 572},
		{ID: "kenduri-panen", Name: "Kenduri Panen", Slug: "kenduri-panen", Description: "Syukuran panen desa: padi menguning, tumpeng, dan lumbung kayu.", Category: "Syukuran", EventType: "syukuran", Tier: "free", Premium: false, PreviewImage: "/themes/previews/kenduri-panen.webp", PreviewURL: "/invitation/demo?template=kenduri-panen", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 573},
		{ID: "konser-amal", Name: "Konser Amal", Slug: "konser-amal", Description: "Undangan konser amal: panggung, lampu sorot, dan semangat berbagi.", Category: "Konser", EventType: "lainnya", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/konser-amal.webp", PreviewURL: "/invitation/demo?template=konser-amal", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 574},
		{ID: "pesta-piyama", Name: "Pesta Piyama", Slug: "pesta-piyama", Description: "Pesta menginap anak: piyama, bantal, tenda selimut, dan bintang malam.", Category: "Ulang Tahun", EventType: "ulang-tahun", Tier: "free", Premium: false, PreviewImage: "/themes/previews/pesta-piyama.webp", PreviewURL: "/invitation/demo?template=pesta-piyama", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 575},
		{ID: "baju-bodo", Name: "Baju Bodo", Slug: "baju-bodo", Description: "Baju bodo transparan berwarna cerah, sarung sutra Makassar, dan perhiasan emas.", Category: "Adat Makassar", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/baju-bodo.webp", PreviewURL: "/invitation/demo?template=baju-bodo", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 576},
		{ID: "gorga-toba", Name: "Gorga Toba", Slug: "gorga-toba", Description: "Ukiran gorga Batak Toba merah-putih-hitam dan Danau Toba dari Samosir.", Category: "Adat Batak", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/gorga-toba.webp", PreviewURL: "/invitation/demo?template=gorga-toba", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 577},
		{ID: "pua-kumbu", Name: "Pua Kumbu", Slug: "pua-kumbu", Description: "Tenun ikat pua kumbu Dayak Iban dan rumah betang di tepi sungai Kapuas.", Category: "Adat Dayak", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/pua-kumbu.webp", PreviewURL: "/invitation/demo?template=pua-kumbu", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 578},
		{ID: "pulau-penyengat", Name: "Pulau Penyengat", Slug: "pulau-penyengat", Description: "Masjid kuning Pulau Penyengat, perahu pompong, dan warisan Melayu Riau.", Category: "Adat Melayu", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/pulau-penyengat.webp", PreviewURL: "/invitation/demo?template=pulau-penyengat", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 579},
		{ID: "kelimutu-lio", Name: "Kelimutu Lio", Slug: "kelimutu-lio", Description: "Danau tiga warna Kelimutu dan tenun ikat Lio dari Ende, Flores.", Category: "Adat NTT", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/kelimutu-lio.webp", PreviewURL: "/invitation/demo?template=kelimutu-lio", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 580},
		{ID: "bangka-cual", Name: "Bangka Cual", Slug: "bangka-cual", Description: "Tenun cual Bangka bermotif bunga, pantai granit, dan rumah panggung Melayu.", Category: "Adat Melayu", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/bangka-cual.webp", PreviewURL: "/invitation/demo?template=bangka-cual", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 581},
		{ID: "karavanserai", Name: "Karavanserai", Slug: "karavanserai", Description: "Halaman karavanserai Jalur Sutra dengan iwan bata dan lampu tembaga.", Category: "Islami", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/karavanserai.webp", PreviewURL: "/invitation/demo?template=karavanserai", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 582},
		{ID: "wisteria-syari", Name: "Wisteria Syari", Slug: "wisteria-syari", Description: "Tanpa foto: untaian wisteria ungu lembut yang menjuntai di atas krem.", Category: "Syari", EventType: "wedding", Tier: "free", Premium: false, PreviewImage: "/themes/previews/wisteria-syari.webp", PreviewURL: "/invitation/demo?template=wisteria-syari", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 583},
		{ID: "brokat-emas", Name: "Brokat Emas", Slug: "brokat-emas", Description: "Kain brokat emas bertekstur dengan motif bunga tenun yang megah.", Category: "Islami", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/brokat-emas.webp", PreviewURL: "/invitation/demo?template=brokat-emas", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 584},
		{ID: "kristal-syari", Name: "Kristal Syari", Slug: "kristal-syari", Description: "Tanpa foto: kristal bening berkilau dan pelangi cahaya yang halus.", Category: "Syari", EventType: "wedding", Tier: "free", Premium: false, PreviewImage: "/themes/previews/kristal-syari.webp", PreviewURL: "/invitation/demo?template=kristal-syari", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 585},
		{ID: "mozaik-umayyah", Name: "Mozaik Umayyah", Slug: "mozaik-umayyah", Description: "Mozaik emas ala masjid Umayyah: pepohonan, sungai, dan istana tanpa figur.", Category: "Islami", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/mozaik-umayyah.webp", PreviewURL: "/invitation/demo?template=mozaik-umayyah", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 586},
		{ID: "zaitun-syari", Name: "Zaitun Syari", Slug: "zaitun-syari", Description: "Ranting zaitun hijau perak di atas kertas linen yang tenang dan syar'i.", Category: "Syari", EventType: "wedding", Tier: "free", Premium: false, PreviewImage: "/themes/previews/zaitun-syari.webp", PreviewURL: "/invitation/demo?template=zaitun-syari", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 587},
		{ID: "kabin-danau", Name: "Kabin Danau", Slug: "kabin-danau", Description: "Kabin kayu di tepi danau, kano, dan hutan pinus berkabut.", Category: "Rustic", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/kabin-danau.webp", PreviewURL: "/invitation/demo?template=kabin-danau", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 588},
		{ID: "alpen-chalet", Name: "Alpen Chalet", Slug: "alpen-chalet", Description: "Chalet kayu di pegunungan Alpen bersalju dengan padang bunga.", Category: "Pemandangan", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/alpen-chalet.webp", PreviewURL: "/invitation/demo?template=alpen-chalet", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 589},
		{ID: "geode-biru", Name: "Geode Biru", Slug: "geode-biru", Description: "Irisan batu geode biru dengan kristal dan tepian emas.", Category: "Luxury", EventType: "wedding", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/geode-biru.webp", PreviewURL: "/invitation/demo?template=geode-biru", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 590},
		{ID: "sabana-afrika", Name: "Sabana Afrika", Slug: "sabana-afrika", Description: "Sabana senja dengan pohon akasia dan langit jingga yang luas.", Category: "Pemandangan", EventType: "wedding", Tier: "free", Premium: false, PreviewImage: "/themes/previews/sabana-afrika.webp", PreviewURL: "/invitation/demo?template=sabana-afrika", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 591},
		{ID: "miami-deco", Name: "Miami Deco", Slug: "miami-deco", Description: "Hotel art deco pastel di tepi pantai, palem, dan neon lembut.", Category: "Retro", EventType: "wedding", Tier: "free", Premium: false, PreviewImage: "/themes/previews/miami-deco.webp", PreviewURL: "/invitation/demo?template=miami-deco", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 592},
		{ID: "letterpress", Name: "Letterpress", Slug: "letterpress", Description: "Cetak letterpress dengan huruf timah, tinta timbul, dan kertas tebal.", Category: "Minimalis", EventType: "wedding", Tier: "free", Premium: false, PreviewImage: "/themes/previews/letterpress.webp", PreviewURL: "/invitation/demo?template=letterpress", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 593},
		{ID: "ultah-balap", Name: "Ultah Balap", Slug: "ultah-balap", Description: "Ulang tahun anak bertema balap mobil: sirkuit, bendera kotak, dan piala.", Category: "Ulang Tahun", EventType: "ulang-tahun", Tier: "free", Premium: false, PreviewImage: "/themes/previews/ultah-balap.webp", PreviewURL: "/invitation/demo?template=ultah-balap", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 594},
		{ID: "ultah-putri-duyung", Name: "Ultah Putri Duyung", Slug: "ultah-putri-duyung", Description: "Ulang tahun anak bertema putri duyung: kerang, mutiara, dan ombak pastel.", Category: "Ulang Tahun", EventType: "ulang-tahun", Tier: "free", Premium: false, PreviewImage: "/themes/previews/ultah-putri-duyung.webp", PreviewURL: "/invitation/demo?template=ultah-putri-duyung", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 595},
		{ID: "ultah-pelangi", Name: "Ultah Pelangi", Slug: "ultah-pelangi", Description: "Ulang tahun anak penuh warna pelangi, awan, dan balon ceria.", Category: "Ulang Tahun", EventType: "ulang-tahun", Tier: "free", Premium: false, PreviewImage: "/themes/previews/ultah-pelangi.webp", PreviewURL: "/invitation/demo?template=ultah-pelangi", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 596},
		{ID: "dies-natalis", Name: "Dies Natalis", Slug: "dies-natalis", Description: "Undangan dies natalis kampus atau sekolah: rapi, megah, dan penuh kebanggaan.", Category: "Peresmian", EventType: "lainnya", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/dies-natalis.webp", PreviewURL: "/invitation/demo?template=dies-natalis", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 597},
		{ID: "pesta-teh", Name: "Pesta Teh", Slug: "pesta-teh", Description: "Pesta teh sore yang anggun: cangkir porselen, kue, dan bunga.", Category: "Ulang Tahun", EventType: "ulang-tahun", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/pesta-teh.webp", PreviewURL: "/invitation/demo?template=pesta-teh", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 598},
		{ID: "bakti-sosial", Name: "Bakti Sosial", Slug: "bakti-sosial", Description: "Undangan bakti sosial dan donor darah: hangat, peduli, dan bersemangat.", Category: "Bakti Sosial", EventType: "lainnya", Tier: "free", Premium: false, PreviewImage: "/themes/previews/bakti-sosial.webp", PreviewURL: "/invitation/demo?template=bakti-sosial", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 599},
		{ID: "khitan-ceria", Name: "Khitan Ceria", Slug: "khitan-ceria", Description: "Khitanan anak yang ceria dengan ilustrasi lucu dan warna segar.", Category: "Khitanan", EventType: "khitan", Tier: "free", Premium: false, PreviewImage: "/themes/previews/khitan-ceria.webp", PreviewURL: "/invitation/demo?template=khitan-ceria", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 224},
		{ID: "aqiqah-bintang", Name: "Aqiqah Bintang", Slug: "aqiqah-bintang", Description: "Aqiqah bayi bernuansa pastel dengan bintang, awan, dan bulan.", Category: "Aqiqah", EventType: "aqiqah", Tier: "free", Premium: false, PreviewImage: "/themes/previews/aqiqah-bintang.webp", PreviewURL: "/invitation/demo?template=aqiqah-bintang", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 225},
		{ID: "ultah-balon", Name: "Ultah Balon", Slug: "ultah-balon", Description: "Ulang tahun anak penuh balon, confetti, dan kue warna-warni.", Category: "Ulang Tahun", EventType: "ulang-tahun", Tier: "free", Premium: false, PreviewImage: "/themes/previews/ultah-balon.webp", PreviewURL: "/invitation/demo?template=ultah-balon", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 226},
		{ID: "ultah-gemerlap", Name: "Ultah Gemerlap", Slug: "ultah-gemerlap", Description: "Pesta ulang tahun dewasa yang gemerlap dengan nuansa malam dan emas.", Category: "Ulang Tahun", EventType: "ulang-tahun", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/ultah-gemerlap.webp", PreviewURL: "/invitation/demo?template=ultah-gemerlap", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 227},
		{ID: "syukuran-rumah", Name: "Syukuran Rumah", Slug: "syukuran-rumah", Description: "Tasyakuran rumah baru yang hangat dengan ilustrasi rumah dan tanaman.", Category: "Syukuran", EventType: "syukuran", Tier: "free", Premium: false, PreviewImage: "/themes/previews/syukuran-rumah.webp", PreviewURL: "/invitation/demo?template=syukuran-rumah", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 228},
		{ID: "lamaran-cincin", Name: "Lamaran Cincin", Slug: "lamaran-cincin", Description: "Lamaran dan tunangan dengan cincin, bunga, dan nuansa champagne.", Category: "Tunangan", EventType: "tunangan", Tier: "premium", Premium: true, PreviewImage: "/themes/previews/lamaran-cincin.webp", PreviewURL: "/invitation/demo?template=lamaran-cincin", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 229},
		{ID: "wisuda-toga", Name: "Wisuda Toga", Slug: "wisuda-toga", Description: "Syukuran wisuda dengan toga, ijazah, dan warna akademik.", Category: "Wisuda", EventType: "wisuda", Tier: "free", Premium: false, PreviewImage: "/themes/previews/wisuda-toga.webp", PreviewURL: "/invitation/demo?template=wisuda-toga", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 230},
		{ID: "tujuh-bulanan", Name: "Tujuh Bulanan", Slug: "tujuh-bulanan", Description: "Syukuran tujuh bulanan (mitoni) dengan kembang setaman dan janur.", Category: "Syukuran", EventType: "syukuran", Tier: "free", Premium: false, PreviewImage: "/themes/previews/tujuh-bulanan.webp", PreviewURL: "/invitation/demo?template=tujuh-bulanan", SupportsPhoto: true, SupportsRSVP: true, SupportsGift: true, Status: "active", SortOrder: 231},
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
		ID:             "free",
		Name:           "Free",
		MaxGuests:      50,
		MaxTeamMembers: 2,
		HasWatermark:   true,
	}
	s.plans["pro"] = &Plan{
		ID:                      "pro",
		Name:                    "Pro",
		MaxGuests:               500,
		MaxTeamMembers:          5,
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
		MaxTeamMembers:          15,
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

func (s *MemoryStore) ActivateSubscription(id string, endsAt *time.Time) (*Subscription, error) {
	s.mu.Lock()
	defer s.mu.Unlock()
	sub, ok := s.subscriptions[id]
	if !ok {
		return nil, fmt.Errorf("subscription not found")
	}
	sub.Status, sub.StartedAt, sub.EndsAt = "active", time.Now().UTC(), endsAt
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
	domain.ID = fmt.Sprintf("domain-%d", time.Now().UnixNano())
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

func (s *MemoryStore) DeleteCustomDomain(id, userID string) error {
	s.mu.Lock()
	defer s.mu.Unlock()
	item, ok := s.customDomains[id]
	if !ok || item.UserID != userID {
		return fmt.Errorf("domain not found")
	}
	delete(s.customDomains, id)
	return nil
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
	sort.Slice(items, func(i, j int) bool { return items[i].Price < items[j].Price })
	return items
}

// SavePlan creates or replaces a plan by ID.
func (s *MemoryStore) SavePlan(plan Plan) (*Plan, error) {
	s.mu.Lock()
	defer s.mu.Unlock()
	saved := plan
	s.plans[plan.ID] = &saved
	return &saved, nil
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

func (s *MemoryStore) UpdateStory(id, title, content, date, image string) (map[string]any, error) {
	s.mu.Lock()
	defer s.mu.Unlock()
	for _, items := range s.stories {
		for _, item := range items {
			if item["id"] == id {
				item["title"], item["content"], item["date"], item["image_url"] = title, content, date, image
				return item, nil
			}
		}
	}
	return nil, fmt.Errorf("story not found")
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
