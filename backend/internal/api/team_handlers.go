package api

import (
	"bytes"
	"context"
	"crypto/rand"
	"encoding/hex"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"net/mail"
	"sort"
	"strings"
	"time"

	"yukakad/internal/auth"
	"yukakad/internal/store"
)

// Team roles per invitation. The owner can do everything; members get a fixed set of permissions.
//
//	editor        Keluarga / editor: edit the invitation and manage guests, no money or team.
//	organizer     WO / vendor: everything an editor can, plus hari-H (check-in, buku buwuh, doorprize, photos).
//	receptionist  Penerima tamu: check-in, log envelopes, venue screen.
const (
	permView          = "view"
	permContent       = "content"
	permGuests        = "guests"       // manage guests, RSVP, wishes, broadcast
	permGuestList     = "guest_list"   // read the guest list (check-in lookup)
	permCheckIn       = "checkin"      // check guests in
	permLedgerRead    = "ledger_read"  // see the buku buwuh
	permLedgerWrite   = "ledger_write" // add entries to the buku buwuh
	permHariH         = "hari_h"       // doorprize setup/draw, guest-photo moderation
	permLive          = "live"         // venue screen feed
	ownerOnly         = ""             // money, team, domains, deleting, duplicating
	defaultTeamLimit  = 15             // used when the owner's plan can't be read
	inviteValidity    = 7 * 24 * time.Hour
	roleEditor        = "editor"
	roleOrganizer     = "organizer"
	roleReceptionist  = "receptionist"
	accessRoleOwner   = "owner"
	memberStatusOpen  = "pending"
	memberStatusReady = "active"
)

var rolePermissions = map[string][]string{
	roleEditor:       {permView, permContent, permGuests, permGuestList, permLedgerRead, permLive},
	roleOrganizer:    {permView, permContent, permGuests, permGuestList, permCheckIn, permLedgerRead, permLedgerWrite, permHariH, permLive},
	roleReceptionist: {permView, permGuestList, permCheckIn, permLedgerWrite, permLive},
}

func roleAllows(role, perm string) bool {
	for _, p := range rolePermissions[role] {
		if p == perm {
			return true
		}
	}
	return false
}

// routedResources are the sub-resource names the invitation router dispatches on.
var routedResources = map[string]bool{
	"settings": true, "stories": true, "gallery": true, "template": true, "events": true, "media": true, "guests": true,
	"rsvps": true, "wishes": true, "broadcast": true, "ledger": true, "live": true, "doorprize": true, "guest-photos": true,
	"gift-wallet": true, "gift-payouts": true, "gift-transactions": true, "gifts": true, "domains": true, "team": true,
	"publish": true, "duplicate": true, "preview-token": true,
}

// requiredPermission maps /api/invitations/{id}/<sub> + method to the permission a member needs.
// Anything not listed is owner-only, so new endpoints are private until they are added here.
func requiredPermission(sub, method string) string {
	read := method == http.MethodGet || method == http.MethodHead
	parts := strings.Split(strings.Trim(sub, "/"), "/")
	head := parts[0]
	// The router also matches some resources by suffix/substring (gift-wallet, rsvps, domains, …). A path that
	// names a second resource after the first one is ambiguous, so only the owner may use it — otherwise a
	// member could prefix an allowed resource ("settings/x/gift-wallet") to reach an owner-only handler.
	for _, part := range parts[1:] {
		if routedResources[part] {
			return ownerOnly
		}
	}
	switch head {
	case "":
		if read {
			return permView
		}
		if method == http.MethodPut || method == http.MethodPatch {
			return permContent
		}
		return ownerOnly
	case "settings", "stories", "gallery", "template", "events", "media":
		if read {
			return permView
		}
		return permContent
	case "guests":
		if len(parts) == 3 && parts[2] == "check-in" && method == http.MethodPost {
			return permCheckIn
		}
		if read {
			return permGuestList
		}
		return permGuests
	case "rsvps", "wishes", "broadcast":
		return permGuests
	case "ledger":
		if read {
			return permLedgerRead
		}
		if method == http.MethodPost && len(parts) == 1 {
			return permLedgerWrite
		}
		return permLedgerRead + "+" + permLedgerWrite // edit/delete existing lines
	case "live":
		if read {
			return permLive
		}
	case "doorprize":
		if read {
			return permLive
		}
		return permHariH
	case "guest-photos":
		return permHariH
	case "preview-token":
		return permView
	}
	return ownerOnly
}

type actingKey struct{}

// acting carries the owner identity a permitted member acts as for one request.
type acting struct {
	tokenUserID string // the member who sent the request
	ownerID     string
	role        string
}

func actingFrom(r *http.Request) (acting, bool) {
	a, ok := r.Context().Value(actingKey{}).(acting)
	return a, ok
}

// actorID is the person who really made the request (a member, or the owner).
func actorID(r *http.Request, fallback string) string {
	if a, ok := actingFrom(r); ok {
		return a.tokenUserID
	}
	return fallback
}

// gateInvitation authorises team members on /api/invitations/{id}/... before the regular handlers run.
// Owners and unrelated users pass through unchanged (handlers keep their own owner checks). A member with
// the right permission continues as the owner for this request only; otherwise they get 403.
func (s *Server) gateInvitation(w http.ResponseWriter, r *http.Request) (*http.Request, bool) {
	path := strings.TrimPrefix(r.URL.Path, "/api/invitations/")
	invitationID, sub, _ := strings.Cut(path, "/")
	if invitationID == "" || sub == "team" || strings.HasPrefix(sub, "team/") {
		return r, true
	}
	token := strings.TrimSpace(strings.TrimPrefix(r.Header.Get("Authorization"), "Bearer "))
	if token == "" {
		return r, true
	}
	claims, ok := s.authenticateToken(token)
	if !ok {
		return r, true
	}
	invitation, exists := s.store.FindInvitationByID(invitationID)
	if !exists || invitation.UserID == claims.UserID {
		return r, true
	}
	member, isMember := s.store.FindMembership(invitation.ID, claims.UserID)
	if !isMember {
		return r, true
	}
	need := requiredPermission(sub, r.Method)
	allowed := need != ownerOnly
	for _, perm := range strings.Split(need, "+") {
		if !roleAllows(member.Role, perm) {
			allowed = false
		}
	}
	if !allowed {
		writeJSON(w, http.StatusForbidden, map[string]string{"error": "peranmu di undangan ini tidak bisa melakukan ini", "role": member.Role})
		return r, false
	}
	// Members may edit content but never the link or publish state.
	if sub == "" && (r.Method == http.MethodPut || r.Method == http.MethodPatch) {
		var payload map[string]any
		body, _ := io.ReadAll(io.LimitReader(r.Body, 1<<20))
		if json.Unmarshal(body, &payload) != nil {
			writeJSON(w, http.StatusBadRequest, map[string]string{"error": "invalid payload"})
			return r, false
		}
		payload["slug"], payload["published"] = invitation.Slug, invitation.Published
		body, _ = json.Marshal(payload)
		r.Body = io.NopCloser(bytes.NewReader(body))
		r.ContentLength = int64(len(body))
	}
	ctx := context.WithValue(r.Context(), actingKey{}, acting{tokenUserID: claims.UserID, ownerID: invitation.UserID, role: member.Role})
	return r.WithContext(ctx), true
}

// accessFor describes what the requester can do on an invitation (for the dashboard to hide menus).
func (s *Server) accessFor(invitation *store.Invitation, userID string) (string, []string) {
	if invitation.UserID == userID {
		return accessRoleOwner, []string{"*"}
	}
	if member, ok := s.store.FindMembership(invitation.ID, userID); ok {
		return member.Role, rolePermissions[member.Role]
	}
	return "", nil
}

func newInviteToken() (string, string) {
	buf := make([]byte, 24)
	_, _ = rand.Read(buf)
	token := hex.EncodeToString(buf)
	return token, auth.HashOpaqueToken(token)
}

func (s *Server) inviteURL(token string) string {
	return strings.TrimRight(s.config.FrontendOrigin, "/") + "/gabung/" + token
}

type memberView struct {
	*store.Member
	Name string `json:"name,omitempty"`
}

func (s *Server) memberViews(invitationID string) []memberView {
	out := []memberView{}
	for _, m := range s.store.ListMembers(invitationID) {
		view := memberView{Member: m}
		if m.UserID != "" {
			if user, ok := s.store.FindUserByID(m.UserID); ok {
				view.Name = user.Name
				if view.Email == "" {
					view.Email = user.Email
				}
			}
		}
		out = append(out, view)
	}
	return out
}

// GET/POST /api/invitations/{id}/team, PATCH/DELETE /api/invitations/{id}/team/{memberId},
// POST /api/invitations/{id}/team/{memberId}/link, DELETE /api/invitations/{id}/team/me (leave)
func (s *Server) handleTeam(w http.ResponseWriter, r *http.Request, invitationID, rest string) {
	claims, ok := s.requireAuth(w, r)
	if !ok {
		return
	}
	invitation, exists := s.store.FindInvitationByID(invitationID)
	if !exists {
		writeJSON(w, http.StatusNotFound, map[string]string{"error": "invitation not found"})
		return
	}
	if rest == "me" && r.Method == http.MethodDelete {
		member, isMember := s.store.FindMembership(invitation.ID, claims.UserID)
		if !isMember {
			writeJSON(w, http.StatusNotFound, map[string]string{"error": "kamu bukan anggota tim undangan ini"})
			return
		}
		_ = s.store.DeleteMember(member.ID)
		writeJSON(w, http.StatusOK, map[string]bool{"left": true})
		return
	}
	if invitation.UserID != claims.UserID {
		writeJSON(w, http.StatusNotFound, map[string]string{"error": "invitation not found"})
		return
	}
	memberID, action, _ := strings.Cut(rest, "/")
	switch {
	case memberID == "" && r.Method == http.MethodGet:
		writeJSON(w, http.StatusOK, map[string]any{"items": s.memberViews(invitation.ID), "roles": rolePermissions, "limit": s.teamLimit(invitation.UserID)})
	case memberID == "" && r.Method == http.MethodPost:
		var payload struct {
			Email string `json:"email"`
			Role  string `json:"role"`
		}
		if json.NewDecoder(http.MaxBytesReader(w, r.Body, 4096)).Decode(&payload) != nil || rolePermissions[payload.Role] == nil {
			writeJSON(w, http.StatusBadRequest, map[string]string{"error": "pilih peran yang valid"})
			return
		}
		email := strings.ToLower(strings.TrimSpace(payload.Email))
		if email != "" {
			if _, err := mail.ParseAddress(email); err != nil || len(email) > 120 {
				writeJSON(w, http.StatusBadRequest, map[string]string{"error": "email tidak valid"})
				return
			}
			if owner, ok := s.store.FindUserByID(invitation.UserID); ok && strings.EqualFold(owner.Email, email) {
				writeJSON(w, http.StatusBadRequest, map[string]string{"error": "itu email pemilik undangan"})
				return
			}
		}
		members := s.store.ListMembers(invitation.ID)
		if limit := s.teamLimit(invitation.UserID); limit > 0 && len(members) >= limit {
			writeJSON(w, http.StatusConflict, map[string]string{"error": fmt.Sprintf("tim sudah penuh (paketmu maksimal %d orang)", limit), "code": "team_limit"})
			return
		}
		for _, m := range members {
			if email != "" && strings.EqualFold(m.Email, email) {
				writeJSON(w, http.StatusConflict, map[string]string{"error": "email ini sudah diundang"})
				return
			}
		}
		token, hash := newInviteToken()
		expires := time.Now().UTC().Add(inviteValidity)
		member, err := s.store.CreateMember(store.Member{InvitationID: invitation.ID, Email: email, Role: payload.Role, Status: memberStatusOpen, TokenHash: hash, InvitedBy: claims.UserID, ExpiresAt: &expires})
		if err != nil {
			writeJSON(w, http.StatusInternalServerError, map[string]string{"error": err.Error()})
			return
		}
		_ = s.store.CreateAuditLog(claims.UserID, invitation.ID, "team.invite", map[string]any{"member_id": member.ID, "role": member.Role})
		writeJSON(w, http.StatusCreated, map[string]any{"member": memberView{Member: member}, "invite_url": s.inviteURL(token)})
	case memberID != "" && action == "link" && r.Method == http.MethodPost:
		member, found := s.store.FindMember(memberID)
		if !found || member.InvitationID != invitation.ID || member.Status != memberStatusOpen {
			writeJSON(w, http.StatusNotFound, map[string]string{"error": "undangan tim tidak ditemukan atau sudah diterima"})
			return
		}
		token, hash := newInviteToken()
		expires := time.Now().UTC().Add(inviteValidity)
		member.TokenHash, member.ExpiresAt = hash, &expires
		if _, err := s.store.UpdateMember(*member); err != nil {
			writeJSON(w, http.StatusInternalServerError, map[string]string{"error": err.Error()})
			return
		}
		writeJSON(w, http.StatusOK, map[string]any{"invite_url": s.inviteURL(token), "expires_at": expires})
	case memberID != "" && action == "" && (r.Method == http.MethodPatch || r.Method == http.MethodPut):
		var payload struct {
			Role string `json:"role"`
		}
		if json.NewDecoder(http.MaxBytesReader(w, r.Body, 1024)).Decode(&payload) != nil || rolePermissions[payload.Role] == nil {
			writeJSON(w, http.StatusBadRequest, map[string]string{"error": "pilih peran yang valid"})
			return
		}
		member, found := s.store.FindMember(memberID)
		if !found || member.InvitationID != invitation.ID {
			writeJSON(w, http.StatusNotFound, map[string]string{"error": "anggota tidak ditemukan"})
			return
		}
		member.Role = payload.Role
		updated, err := s.store.UpdateMember(*member)
		if err != nil {
			writeJSON(w, http.StatusInternalServerError, map[string]string{"error": err.Error()})
			return
		}
		_ = s.store.CreateAuditLog(claims.UserID, invitation.ID, "team.role", map[string]any{"member_id": member.ID, "role": member.Role})
		writeJSON(w, http.StatusOK, memberView{Member: updated})
	case memberID != "" && action == "" && r.Method == http.MethodDelete:
		member, found := s.store.FindMember(memberID)
		if !found || member.InvitationID != invitation.ID {
			writeJSON(w, http.StatusNotFound, map[string]string{"error": "anggota tidak ditemukan"})
			return
		}
		_ = s.store.DeleteMember(member.ID)
		_ = s.store.CreateAuditLog(claims.UserID, invitation.ID, "team.remove", map[string]any{"member_id": member.ID})
		writeJSON(w, http.StatusOK, map[string]bool{"deleted": true})
	default:
		writeJSON(w, http.StatusMethodNotAllowed, map[string]string{"error": "method not allowed"})
	}
}

// GET /api/team-invites/{token} — preview; POST /api/team-invites/{token}/accept — join (requires login).
func (s *Server) handleTeamInvite(w http.ResponseWriter, r *http.Request) {
	rest := strings.Trim(strings.TrimPrefix(r.URL.Path, "/api/team-invites/"), "/")
	token, action, _ := strings.Cut(rest, "/")
	if !s.allowRate(w, "team-invite:"+clientIP(r), 30, time.Minute) {
		return
	}
	member, found := s.store.FindMemberByTokenHash(auth.HashOpaqueToken(token))
	if token == "" || !found || member.Status != memberStatusOpen {
		writeJSON(w, http.StatusNotFound, map[string]string{"error": "link undangan tim tidak berlaku atau sudah dipakai"})
		return
	}
	if member.ExpiresAt != nil && time.Now().After(*member.ExpiresAt) {
		writeJSON(w, http.StatusGone, map[string]string{"error": "link undangan tim sudah kedaluwarsa, minta link baru ke pemilik undangan"})
		return
	}
	invitation, exists := s.store.FindInvitationByID(member.InvitationID)
	if !exists {
		writeJSON(w, http.StatusNotFound, map[string]string{"error": "undangan tidak ditemukan"})
		return
	}
	switch {
	case action == "" && r.Method == http.MethodGet:
		inviter := ""
		if owner, ok := s.store.FindUserByID(invitation.UserID); ok {
			inviter = owner.Name
		}
		writeJSON(w, http.StatusOK, map[string]any{
			"invitation": map[string]any{"id": invitation.ID, "title": invitation.Title, "couple": invitation.Couple},
			"role":       member.Role, "permissions": rolePermissions[member.Role], "email": member.Email, "inviter": inviter, "expires_at": member.ExpiresAt,
		})
	case action == "accept" && r.Method == http.MethodPost:
		claims, ok := s.requireAuth(w, r)
		if !ok {
			return
		}
		if claims.UserID == invitation.UserID {
			writeJSON(w, http.StatusBadRequest, map[string]string{"error": "kamu pemilik undangan ini"})
			return
		}
		if _, already := s.store.FindMembership(invitation.ID, claims.UserID); already {
			writeJSON(w, http.StatusConflict, map[string]string{"error": "kamu sudah ada di tim undangan ini"})
			return
		}
		now := time.Now().UTC()
		member.UserID, member.Status, member.TokenHash, member.AcceptedAt = claims.UserID, memberStatusReady, "", &now
		if member.Email == "" {
			member.Email = claims.Email
		}
		updated, err := s.store.UpdateMember(*member)
		if err != nil {
			writeJSON(w, http.StatusConflict, map[string]string{"error": err.Error()})
			return
		}
		_ = s.store.CreateAuditLog(claims.UserID, invitation.ID, "team.join", map[string]any{"member_id": updated.ID, "role": updated.Role})
		writeJSON(w, http.StatusOK, map[string]any{"invitation_id": invitation.ID, "role": updated.Role})
	default:
		writeJSON(w, http.StatusMethodNotAllowed, map[string]string{"error": "method not allowed"})
	}
}

// sharedInvitations lists invitations the user helps with, newest membership first.
func (s *Server) sharedInvitations(userID string) []map[string]any {
	items := []map[string]any{}
	memberships := s.store.ListMembershipsByUser(userID)
	sort.Slice(memberships, func(i, j int) bool { return memberships[i].CreatedAt.After(memberships[j].CreatedAt) })
	for _, m := range memberships {
		invitation, ok := s.store.FindInvitationByID(m.InvitationID)
		if !ok {
			continue
		}
		owner := ""
		if user, found := s.store.FindUserByID(invitation.UserID); found {
			owner = user.Name
		}
		items = append(items, map[string]any{
			"id": invitation.ID, "slug": invitation.Slug, "title": invitation.Title, "published": invitation.Published,
			"template_id": invitation.TemplateID, "couple": invitation.Couple, "event": invitation.Event,
			"created_at": invitation.CreatedAt, "role": m.Role, "owner_name": owner,
		})
	}
	return items
}

func (s *Server) accessView(r *http.Request, invitation *store.Invitation, userID string) map[string]any {
	if a, ok := actingFrom(r); ok {
		return map[string]any{"role": a.role, "permissions": rolePermissions[a.role]}
	}
	role, perms := s.accessFor(invitation, userID)
	return map[string]any{"role": role, "permissions": perms}
}

// teamLimit is how many members the owner's plan allows per invitation (0 = unlimited).
func (s *Server) teamLimit(ownerID string) int {
	plan, err := s.store.GetUserPlan(ownerID)
	if err != nil || plan == nil {
		return defaultTeamLimit
	}
	return plan.MaxTeamMembers
}
