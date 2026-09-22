package api

import "testing"

func TestAllowedCORSOrigin(t *testing.T) {
	configured := "http://localhost:3000,http://localhost:3001"
	cases := []struct {
		request string
		want    string
	}{
		{"http://localhost:3000", "http://localhost:3000"},
		{"http://localhost:3001", "http://localhost:3001"},
		{"http://localhost:4000", ""},
		{"", ""},
	}
	for _, tc := range cases {
		if got := allowedCORSOrigin(configured, tc.request); got != tc.want {
			t.Fatalf("origin %q: got %q want %q", tc.request, got, tc.want)
		}
	}
}
