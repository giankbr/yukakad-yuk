package webhooks

import "testing"

func TestSignature(t *testing.T) {
	body := []byte(`{"reference":"abc"}`)
	sig := Sign(body, "secret")
	if !Verify(body, sig, "secret") {
		t.Fatal("valid signature rejected")
	}
	if Verify([]byte(`{"reference":"other"}`), sig, "secret") {
		t.Fatal("tampered payload accepted")
	}
}
