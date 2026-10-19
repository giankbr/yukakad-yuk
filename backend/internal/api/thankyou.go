package api

import (
	"time"

	"yukakad/internal/store"
)

// thankYouActive mirrors the frontend's useThankYou: sections_config.thankYou.mode "on" forces it, "off"
// disables it, and "auto" (default) turns it on one day after the latest event.
func (s *Server) thankYouActive(invitation *store.Invitation) bool {
	sections, _ := s.store.GetSettings(invitation.ID)["sections_config"].(map[string]any)
	mode := "auto"
	if cfg, ok := sections["thankYou"].(map[string]any); ok {
		if value, ok := cfg["mode"].(string); ok && value != "" {
			mode = value
		}
	}
	switch mode {
	case "on":
		return true
	case "off":
		return false
	}
	jakarta := time.FixedZone("WIB", 7*3600)
	var latest time.Time
	consider := func(date, start string) {
		day, err := time.ParseInLocation("2006-01-02", date, jakarta)
		if err != nil {
			return
		}
		if clock, err := time.Parse("15:04", start); err == nil {
			day = day.Add(time.Duration(clock.Hour())*time.Hour + time.Duration(clock.Minute())*time.Minute)
		}
		if day.After(latest) {
			latest = day
		}
	}
	consider(invitation.Event.Date, invitation.Event.StartTime)
	for _, event := range s.store.ListInvitationEvents(invitation.ID) {
		consider(event.Date, event.StartTime)
	}
	return !latest.IsZero() && time.Now().After(latest.Add(24*time.Hour))
}
