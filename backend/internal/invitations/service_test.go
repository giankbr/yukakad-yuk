package invitations

import (
	"errors"
	"testing"
	"yukakad/internal/store"
)

func TestCreateAndOwnership(t *testing.T) {
	data := store.NewMemoryStore()
	svc := NewService(data)
	inv, err := svc.Create("user-1", "alya-rizky", "Alya & Rizky")
	if err != nil {
		t.Fatalf("create: %v", err)
	}
	if _, err := svc.Owned("user-2", inv.ID); !errors.Is(err, ErrNotFound) {
		t.Fatalf("expected hidden invitation, got %v", err)
	}
	if _, err := svc.Create("user-1", "bad slug", "Title"); !errors.Is(err, ErrInvalid) {
		t.Fatalf("expected invalid slug, got %v", err)
	}
}

func TestDuplicateDefaultsToDraft(t *testing.T) {
	data := store.NewMemoryStore()
	svc := NewService(data)
	_, err := svc.Create("user-1", "alya-rizky", "Alya & Rizky")
	if err != nil {
		t.Fatal(err)
	}
	source, _ := data.FindInvitationBySlug("alya-rizky")
	copy, err := svc.Duplicate("user-1", source.ID, "", "")
	if err != nil {
		t.Fatalf("duplicate: %v", err)
	}
	if copy.Slug != "alya-rizky-copy" || copy.Published {
		t.Fatalf("unexpected copy: %+v", copy)
	}
}
