package api

import (
	"encoding/json"
	"errors"
	"net/http"
	"net/url"
	"strings"
	"time"

	domainservice "yukakad/internal/domains"
	"yukakad/internal/store"
)

// domainView adds the DNS records the couple has to create.
func (s *Server) domainView(item *store.CustomDomain) map[string]any {
	return map[string]any{
		"id": item.ID, "domain": item.Domain, "status": item.Status, "verified_at": item.VerifiedAt, "created_at": item.CreatedAt,
		"txt_name": domainservice.TXTName(item.Domain), "txt_value": domainservice.TXTValue(item.VerificationToken),
		"cname_target": s.domains.Target,
	}
}

func domainError(err error) (int, map[string]string) {
	switch {
	case errors.Is(err, domainservice.ErrNotAllowed):
		return http.StatusForbidden, map[string]string{"error": err.Error(), "code": "plan_required"}
	case errors.Is(err, domainservice.ErrNotFound):
		return http.StatusNotFound, map[string]string{"error": err.Error()}
	case errors.Is(err, domainservice.ErrTaken):
		return http.StatusConflict, map[string]string{"error": err.Error()}
	case errors.Is(err, domainservice.ErrInvalid), errors.Is(err, domainservice.ErrLimit), errors.Is(err, domainservice.ErrReserved):
		return http.StatusBadRequest, map[string]string{"error": err.Error()}
	}
	return http.StatusServiceUnavailable, map[string]string{"error": "Domain belum bisa diproses. Coba lagi nanti."}
}

// /api/invitations/{id}/domains[/{domainID}[/verify]] — owner only (see requiredPermission).
func (s *Server) handleCustomDomains(w http.ResponseWriter, r *http.Request, invitationID string) {
	claims, ok := s.requireAuth(w, r)
	if !ok {
		return
	}
	base := "/api/invitations/" + invitationID + "/domains"
	id := strings.Trim(strings.TrimPrefix(r.URL.Path, base), "/")
	switch {
	case r.Method == http.MethodGet && id == "":
		items, err := s.domains.List(claims.UserID, invitationID)
		if err != nil {
			status, body := domainError(err)
			writeJSON(w, status, body)
			return
		}
		views := make([]map[string]any, 0, len(items))
		for _, item := range items {
			views = append(views, s.domainView(item))
		}
		allowed, _ := s.billing.Allows(claims.UserID, "custom_domain")
		writeJSON(w, http.StatusOK, map[string]any{"items": views, "cname_target": s.domains.Target, "allowed": allowed})
	case r.Method == http.MethodPost && id == "":
		var payload struct {
			Domain string `json:"domain"`
		}
		if json.NewDecoder(http.MaxBytesReader(w, r.Body, 4096)).Decode(&payload) != nil {
			writeJSON(w, http.StatusBadRequest, map[string]string{"error": "invalid payload"})
			return
		}
		item, err := s.domains.Create(claims.UserID, invitationID, payload.Domain)
		if err != nil {
			status, body := domainError(err)
			writeJSON(w, status, body)
			return
		}
		_ = s.store.CreateAuditLog(claims.UserID, invitationID, "domain.create", map[string]any{"domain": item.Domain})
		writeJSON(w, http.StatusCreated, s.domainView(item))
	case r.Method == http.MethodPost && strings.HasSuffix(id, "/verify"):
		if !s.allowRate(w, "domain-verify:"+claims.UserID, 20, 10*time.Minute) {
			return
		}
		item, check, err := s.domains.Verify(r.Context(), claims.UserID, invitationID, strings.TrimSuffix(id, "/verify"))
		if err != nil {
			status, body := domainError(err)
			writeJSON(w, status, body)
			return
		}
		writeJSON(w, http.StatusOK, map[string]any{"domain": s.domainView(item), "check": check})
	case r.Method == http.MethodDelete && id != "" && !strings.Contains(id, "/"):
		if err := s.domains.Delete(claims.UserID, invitationID, id); err != nil {
			status, body := domainError(err)
			writeJSON(w, status, body)
			return
		}
		writeJSON(w, http.StatusOK, map[string]bool{"deleted": true})
	default:
		writeJSON(w, http.StatusMethodNotAllowed, map[string]string{"error": "method not allowed"})
	}
}

// GET /api/public/domain/{host} — which published invitation a verified custom domain shows.
// Used by the Next.js server, which receives the guest's Host header.
func (s *Server) handlePublicDomain(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodGet {
		writeJSON(w, http.StatusMethodNotAllowed, map[string]string{"error": "method not allowed"})
		return
	}
	host := domainservice.Normalize(strings.TrimPrefix(r.URL.Path, "/api/public/domain/"))
	invitation, ok := s.store.FindInvitationByCustomDomain(host)
	if !ok || !invitation.Published {
		writeJSON(w, http.StatusNotFound, map[string]string{"error": "Domain tidak terhubung ke undangan"})
		return
	}
	writeJSON(w, http.StatusOK, map[string]string{"slug": invitation.Slug, "domain": host})
}

// GET /api/public/domain-check?domain=x — 200 when x is a verified custom domain. Point the TLS proxy's
// on-demand certificate "ask" hook here (e.g. Caddy on_demand_tls) so certificates are only issued for them.
func (s *Server) handleDomainCheck(w http.ResponseWriter, r *http.Request) {
	host := domainservice.Normalize(r.URL.Query().Get("domain"))
	if _, ok := s.store.FindInvitationByCustomDomain(host); !ok {
		writeJSON(w, http.StatusNotFound, map[string]string{"error": "unknown domain"})
		return
	}
	writeJSON(w, http.StatusOK, map[string]string{"domain": host})
}

// verifiedDomainOrigin reports whether origin is https://<verified custom domain>.
func (s *Server) verifiedDomainOrigin(origin string) bool {
	parsed, err := url.Parse(origin)
	if err != nil || parsed.Host == "" || (parsed.Scheme != "https" && parsed.Scheme != "http") {
		return false
	}
	_, ok := s.store.FindInvitationByCustomDomain(domainservice.Normalize(parsed.Host))
	return ok
}
