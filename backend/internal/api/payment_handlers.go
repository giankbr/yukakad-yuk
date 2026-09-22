package api

import (
	"net/http"
	"strings"
)

func (s *Server) handleDummyPayment(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		writeJSON(w, http.StatusMethodNotAllowed, map[string]string{"error": "method not allowed"})
		return
	}
	reference := strings.Trim(strings.TrimPrefix(r.URL.Path, "/api/payments/dummy/"), "/")
	if reference == "" {
		writeJSON(w, http.StatusBadRequest, map[string]string{"error": "payment reference is required"})
		return
	}
	tx, err := s.gifts.ConfirmDummy(reference)
	if err != nil {
		writeJSON(w, http.StatusNotFound, map[string]string{"error": err.Error()})
		return
	}
	writeJSON(w, http.StatusOK, tx)
}
