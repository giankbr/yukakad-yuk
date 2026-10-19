package api

import (
	"bytes"
	"encoding/csv"
	"errors"
	"fmt"
	"io"
	"strings"
)

type guestRow struct{ name, phone, category, table string }

// parseGuestCSV reads name,phone,category,table rows. The delimiter is detected from the first line, so files
// saved by Indonesian Excel (semicolon) work as well as comma or tab separated ones. A header row is skipped.
func parseGuestCSV(body io.Reader) ([]guestRow, error) {
	data, err := io.ReadAll(body)
	if err != nil {
		return nil, errors.New("File terlalu besar (maksimal 2 MB)")
	}
	data = bytes.TrimPrefix(data, []byte("\xef\xbb\xbf")) // UTF-8 BOM from Excel
	firstLine, _, _ := bytes.Cut(data, []byte("\n"))
	reader := csv.NewReader(bytes.NewReader(data))
	reader.FieldsPerRecord = -1
	reader.TrimLeadingSpace = true
	reader.LazyQuotes = true
	switch {
	case bytes.Count(firstLine, []byte(";")) > bytes.Count(firstLine, []byte(",")):
		reader.Comma = ';'
	case bytes.Count(firstLine, []byte("\t")) > bytes.Count(firstLine, []byte(",")):
		reader.Comma = '\t'
	}
	rows := make([]guestRow, 0)
	for line := 1; ; line++ {
		record, err := reader.Read()
		if err == io.EOF {
			break
		}
		if err != nil {
			return nil, fmt.Errorf("Baris %d tidak bisa dibaca. Pastikan formatnya CSV (nama, telepon, kategori, meja)", line)
		}
		cell := func(i int) string {
			if i < len(record) {
				return strings.TrimSpace(record[i])
			}
			return ""
		}
		name := cell(0)
		if name == "" {
			continue
		}
		if line == 1 && (strings.EqualFold(name, "name") || strings.EqualFold(name, "nama")) {
			continue
		}
		category := cell(2)
		if category == "" {
			category = "family"
		}
		rows = append(rows, guestRow{name: name, phone: cell(1), category: category, table: cell(3)})
	}
	if len(rows) == 0 {
		return nil, errors.New("File tidak berisi tamu")
	}
	if len(rows) > 5000 {
		return nil, errors.New("Maksimal 5.000 tamu per file")
	}
	return rows, nil
}
