package api

import (
	"bytes"
	"io"
	"net/http"
	"regexp"

	mediaservice "yukakad/internal/media"
)

var uploadFolderPattern = regexp.MustCompile(`^[a-z0-9-]{1,30}$`)

// POST /api/admin/uploads (multipart: file, folder)
// Stores an image for site content (team photos, product images) and returns its URL.
func (s *Server) handleAdminUploads(w http.ResponseWriter, r *http.Request) {
	if _, ok := s.requireAdmin(w, r); !ok {
		return
	}
	if r.Method != http.MethodPost {
		writeJSON(w, http.StatusMethodNotAllowed, map[string]string{"error": "method not allowed"})
		return
	}
	if s.photoStore == nil {
		writeJSON(w, http.StatusServiceUnavailable, map[string]string{"error": "object storage is not configured"})
		return
	}
	r.Body = http.MaxBytesReader(w, r.Body, 10<<20)
	if err := r.ParseMultipartForm(10 << 20); err != nil {
		writeJSON(w, http.StatusRequestEntityTooLarge, map[string]string{"error": "file too large"})
		return
	}
	folder := r.FormValue("folder")
	if folder != "" && !uploadFolderPattern.MatchString(folder) {
		writeJSON(w, http.StatusBadRequest, map[string]string{"error": "invalid folder"})
		return
	}
	file, _, err := r.FormFile("file")
	if err != nil {
		writeJSON(w, http.StatusBadRequest, map[string]string{"error": "file is required"})
		return
	}
	defer file.Close()
	data, err := io.ReadAll(file)
	if err != nil {
		writeJSON(w, http.StatusBadRequest, map[string]string{"error": "could not read file"})
		return
	}
	contentType := mediaservice.DetectContentType(data)
	if contentType != "image/jpeg" && contentType != "image/png" && contentType != "image/webp" {
		writeJSON(w, http.StatusBadRequest, map[string]string{"error": "image must be jpeg, png, or webp"})
		return
	}
	url, err := s.photoStore.Upload(r.Context(), adminUploadKey(folder, randomID()), bytes.NewReader(data), int64(len(data)), contentType)
	if err != nil {
		writeJSON(w, http.StatusBadGateway, map[string]string{"error": err.Error()})
		return
	}
	writeJSON(w, http.StatusOK, map[string]string{"url": url})
}

// adminUploadKey keeps admin uploads under site/ ("site/<id>", or "site/<folder>/<id>" when a folder is given).
func adminUploadKey(folder, id string) string {
	if folder == "" || folder == "site" {
		return "site/" + id
	}
	return "site/" + folder + "/" + id
}
