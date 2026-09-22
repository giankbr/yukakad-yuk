package db

import "time"

type User struct {
	ID        string    `json:"id"`
	Name      string    `json:"name"`
	Email     string    `json:"email"`
	Password  string    `json:"-"`
	CreatedAt time.Time `json:"created_at"`
}

type Invitation struct {
	ID        string    `json:"id"`
	UserID    string    `json:"user_id"`
	Slug      string    `json:"slug"`
	Title     string    `json:"title"`
	Status    string    `json:"status"`
	Published bool      `json:"published"`
	CreatedAt time.Time `json:"created_at"`
}

type Couple struct {
	InvitationID string `json:"invitation_id"`
	GroomName    string `json:"groom_name"`
	BrideName    string `json:"bride_name"`
}

type Event struct {
	InvitationID string `json:"invitation_id"`
	Title       string `json:"title"`
	Venue       string `json:"venue"`
	Date        string `json:"date"`
}

type Guest struct {
	ID              string    `json:"id"`
	InvitationID    string    `json:"invitation_id"`
	Name            string    `json:"name"`
	Phone           string    `json:"phone,omitempty"`
	Category        string    `json:"category"`
	InvitationToken string    `json:"invitation_token"`
	CreatedAt       time.Time `json:"created_at"`
}

type RSVP struct {
	ID             string    `json:"id"`
	InvitationID   string    `json:"invitation_id"`
	GuestID        string    `json:"guest_id,omitempty"`
	Attendance     string    `json:"attendance"`
	AttendeesCount int       `json:"attendees_count"`
	SubmittedAt    time.Time `json:"submitted_at"`
}

type Wish struct {
	ID          string    `json:"id"`
	InvitationID string    `json:"invitation_id"`
	GuestID     string    `json:"guest_id,omitempty"`
	Name        string    `json:"name"`
	Message     string    `json:"message"`
	Status      string    `json:"status"`
	CreatedAt   time.Time `json:"created_at"`
}
