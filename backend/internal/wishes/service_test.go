package wishes

import (
	"errors"
	"testing"
	"yukakad/internal/store"
)

func TestWishModerationRequiresOwnerAndValidStatus(t *testing.T) {
	data := store.NewMemoryStore()
	inv, _ := data.CreateInvitation("user-1", "alya-rizky", "Alya & Rizky")
	wish, _ := data.CreateWish(inv.ID, "", "Budi", "Selamat")
	svc := NewService(data)
	if _, err := svc.Moderate("user-2", inv.ID, wish.ID, "published"); !errors.Is(err, ErrNotFound) {
		t.Fatalf("expected ownership error, got %v", err)
	}
	if _, err := svc.Moderate("user-1", inv.ID, wish.ID, "unknown"); !errors.Is(err, ErrInvalid) {
		t.Fatalf("expected status error, got %v", err)
	}
	updated, err := svc.Moderate("user-1", inv.ID, wish.ID, "published")
	if err != nil || updated.Status != "published" {
		t.Fatalf("moderation failed: %+v %v", updated, err)
	}
}
