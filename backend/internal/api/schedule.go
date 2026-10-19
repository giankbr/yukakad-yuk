package api

import (
	"regexp"
	"time"
)

var timePattern = regexp.MustCompile(`^([01]\d|2[0-3]):[0-5]\d(:[0-5]\d)?$`)

// validateSchedule checks an event's date (YYYY-MM-DD) and times (HH:MM); empty values are allowed.
// It returns an Indonesian error message, or "" when valid.
func validateSchedule(date, start, end string) string {
	if date != "" {
		if _, err := time.Parse("2006-01-02", date); err != nil {
			return "Tanggal acara tidak valid (format YYYY-MM-DD)"
		}
	}
	for _, value := range []string{start, end} {
		if value != "" && !timePattern.MatchString(value) {
			return "Jam acara tidak valid (format JJ:MM, 00:00–23:59)"
		}
	}
	if start != "" && end != "" && len(start) >= 5 && len(end) >= 5 && end[:5] < start[:5] {
		return "Jam selesai tidak boleh sebelum jam mulai"
	}
	return ""
}
