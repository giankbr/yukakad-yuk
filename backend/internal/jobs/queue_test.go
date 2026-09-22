package jobs

import (
	"encoding/json"
	"testing"
	"time"
)

func TestJobPayloadRoundTrip(t *testing.T) {
	payload, _ := json.Marshal(map[string]string{"email": "a@example.com"})
	job := Job{ID: "job-1", Type: "password_reset", Payload: payload, CreatedAt: time.Now().UTC()}
	encoded, err := json.Marshal(job)
	if err != nil {
		t.Fatal(err)
	}
	var decoded Job
	if err := json.Unmarshal(encoded, &decoded); err != nil {
		t.Fatal(err)
	}
	if decoded.Type != job.Type || string(decoded.Payload) != string(job.Payload) {
		t.Fatalf("round trip mismatch: %+v", decoded)
	}
}
