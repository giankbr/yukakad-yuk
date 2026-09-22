package api

import (
	"net"
	"net/http"
	"strings"
	"time"
)

func (s *Server) securityHeadersMiddleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		if strings.HasPrefix(r.URL.Path, "/api/") && !strings.HasPrefix(r.URL.Path, "/api/v1/") {
			w.Header().Set("Deprecation", "true")
			w.Header().Set("Sunset", "Wed, 30 Jun 2027 00:00:00 GMT")
			w.Header().Add("Link", "</api/v1>; rel=\"successor-version\"")
		}
		w.Header().Set("X-Content-Type-Options", "nosniff")
		w.Header().Set("X-Frame-Options", "DENY")
		w.Header().Set("Referrer-Policy", "no-referrer")
		w.Header().Set("Content-Security-Policy", "default-src 'none'")
		next.ServeHTTP(w, r)
	})
}

func (s *Server) corsMiddleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		if origin := s.config.FrontendOrigin; origin != "" {
			w.Header().Set("Access-Control-Allow-Origin", origin)
			w.Header().Set("Vary", "Origin")
		}
		w.Header().Set("Access-Control-Allow-Methods", "GET, POST, PUT, PATCH, DELETE, OPTIONS")
		w.Header().Set("Access-Control-Allow-Headers", "Content-Type, Authorization")
		if r.Method == http.MethodOptions {
			w.WriteHeader(http.StatusNoContent)
			return
		}
		next.ServeHTTP(w, r)
	})
}

func (s *Server) rateLimitMiddleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		if !s.allowRate(w, "global:"+clientIP(r), 120, time.Minute) {
			return
		}
		next.ServeHTTP(w, r)
	})
}

// allowRate checks the limiter and fails closed when Redis is unavailable.
// Authentication and public write endpoints must not bypass protection during
// an infrastructure failure.
func (s *Server) allowRate(w http.ResponseWriter, key string, limit int, window time.Duration) bool {
	allowed, err := s.limiter.Allow(key, limit, window)
	if err != nil {
		writeJSON(w, http.StatusServiceUnavailable, map[string]string{"error": "rate limit service unavailable"})
		return false
	}
	if !allowed {
		writeJSON(w, http.StatusTooManyRequests, map[string]string{"error": "rate limit exceeded, please try again later"})
	}
	return allowed
}

func clientIP(r *http.Request) string {
	if fwd := r.Header.Get("X-Forwarded-For"); fwd != "" {
		return strings.TrimSpace(strings.Split(fwd, ",")[0])
	}
	host, _, err := net.SplitHostPort(r.RemoteAddr)
	if err != nil {
		return r.RemoteAddr
	}
	return host
}
