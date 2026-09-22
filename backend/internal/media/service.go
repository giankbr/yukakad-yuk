package media

import (
	"bytes"
	"context"
	"crypto/rand"
	"encoding/hex"
	"errors"
	"fmt"
	"net/http"
	"strings"

	"yukakad/internal/storage"
	"yukakad/internal/store"
)

var (
	ErrNotFound = errors.New("media not found")
	ErrInvalid  = errors.New("invalid media")
)

const MaxUploadSize int64 = 10 << 20

var allowedTypes = map[string]bool{"image/jpeg": true, "image/png": true, "image/webp": true, "audio/mpeg": true}

type Service struct {
	store   store.Store
	storage *storage.Client
}

func NewService(dataStore store.Store, objectStorage *storage.Client) *Service {
	return &Service{store: dataStore, storage: objectStorage}
}

func (s *Service) Upload(ctx context.Context, ownerID, invitationID, mediaType, contentType string, data []byte) (map[string]any, error) {
	invitation, ok := s.store.FindInvitationByID(invitationID)
	if !ok || invitation.UserID != ownerID {
		return nil, ErrNotFound
	}
	if s.storage == nil || !allowedTypes[contentType] || len(data) == 0 || int64(len(data)) > MaxUploadSize {
		return nil, ErrInvalid
	}
	mediaType = strings.TrimSpace(mediaType)
	if mediaType == "" {
		mediaType = "gallery"
	}
	if mediaType != "gallery" && mediaType != "cover" && mediaType != "music" && mediaType != "qris" {
		return nil, ErrInvalid
	}
	key := fmt.Sprintf("invitations/%s/%s/%s", invitationID, mediaType, randomID())
	publicURL, err := s.storage.Upload(ctx, key, bytes.NewReader(data), int64(len(data)), contentType)
	if err != nil {
		return nil, fmt.Errorf("upload media: %w", err)
	}
	item, err := s.store.CreateMedia(invitationID, mediaType, publicURL, contentType, int64(len(data)))
	if err != nil {
		_ = s.storage.DeleteURL(ctx, publicURL)
		return nil, fmt.Errorf("save media: %w", err)
	}
	return item, nil
}

func (s *Service) Delete(ctx context.Context, ownerID, mediaID string) error {
	item, ok := s.store.FindMedia(mediaID)
	if !ok {
		return ErrNotFound
	}
	invitation, ok := s.store.FindInvitationByID(item["invitation_id"].(string))
	if !ok || invitation.UserID != ownerID {
		return ErrNotFound
	}
	if s.storage == nil {
		return ErrInvalid
	}
	if err := s.storage.DeleteURL(ctx, item["path"].(string)); err != nil {
		return fmt.Errorf("delete media object: %w", err)
	}
	if err := s.store.DeleteMedia(mediaID); err != nil {
		return fmt.Errorf("delete media record: %w", err)
	}
	return nil
}

func randomID() string {
	b := make([]byte, 16)
	_, _ = rand.Read(b)
	return hex.EncodeToString(b)
}

func DetectContentType(data []byte) string { return http.DetectContentType(data) }
