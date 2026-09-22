package rsvp

import (
	"errors"
	"testing"
	"yukakad/internal/store"
)

func TestSubmitUpsertsGuestResponse(t *testing.T) {
	data := store.NewMemoryStore()
	inv, _ := data.CreateInvitation("user-1", "alya-rizky", "Alya & Rizky")
	guest, _ := data.CreateGuest(inv.ID, "Budi", "0812", "friend")
	svc := NewService(data)
	first, err := svc.Submit(inv.ID, "", guest.Token, "yes", 2, "See you")
	if err != nil {
		t.Fatal(err)
	}
	second, err := svc.Submit(inv.ID, guest.ID, "", "no", 1, "Sorry")
	if err != nil || first.ID != second.ID || second.AttendeesCount != 0 {
		t.Fatalf("unexpected upsert: %+v %v", second, err)
	}
	if _, err := svc.Submit(inv.ID, "", "bad-token", "yes", 1, ""); !errors.Is(err, ErrNotFound) {
		t.Fatalf("expected token error, got %v", err)
	}
}
