package api

import (
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"testing"
	"yukakad/internal/config"
)

func TestWeddingTemplateSelectionReachesPublicInvitation(t *testing.T) {
	server := NewServer(config.Config{Environment: "test", JWTSecret: "test-secret"})
	user, err := server.store.CreateUser("Couple", "templates@example.com", "hash")
	if err != nil {
		t.Fatal(err)
	}
	invitation, err := server.store.CreateInvitation(user.ID, "template-preview", "Our wedding")
	if err != nil {
		t.Fatal(err)
	}
	invitation.Published = true
	for _, id := range []string{"alyra", "weddings", "veloria"} {
		t.Run(id, func(t *testing.T) {
			if err := server.store.AssignTemplate(invitation.ID, id); err != nil {
				t.Fatal(err)
			}
			recorder := httptest.NewRecorder()
			server.handlePublicInvitation(recorder, httptest.NewRequest(http.MethodGet, "/api/public/invitation/template-preview", nil))
			if recorder.Code != http.StatusOK {
				t.Fatalf("status %d: %s", recorder.Code, recorder.Body.String())
			}
			var body struct {
				TemplateID string `json:"template_id"`
			}
			if err := json.Unmarshal(recorder.Body.Bytes(), &body); err != nil {
				t.Fatal(err)
			}
			if body.TemplateID != id {
				t.Fatalf("selected %s, public renderer received %s", id, body.TemplateID)
			}
		})
	}
}
