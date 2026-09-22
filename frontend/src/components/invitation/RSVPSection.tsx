"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";

export function RSVPSection({ slug, guestToken }: { slug: string; guestToken?: string }) {
  const [sent, setSent] = useState(false);
  const [error, setError] = useState("");
  return (
    <section className="invitation-section rsvp-section" aria-labelledby="rsvp-title">
      <div><p className="section-label">Save us a seat</p><h2 id="rsvp-title">Will you be there?</h2><p className="rsvp-intro">A quick note helps us prepare the right amount of joy.</p></div>
      {sent ? <p className="rsvp-success" role="status">Thank you. We&apos;ll keep your answer close.</p> : <form className="rsvp-form" onSubmit={async (event) => { event.preventDefault(); setError(""); const form = new FormData(event.currentTarget); const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8080"}/api/public/invitation/${slug}/rsvp`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ guest_token: guestToken, attendance: form.get("attendance"), attendees_count: 1, message: form.get("message") }), }); if (response.ok) setSent(true); else setError("We could not save your answer. Please try once more."); }}>
        <label>Name<input required name="name" placeholder="Your name" /></label>
        <label>Attendance<select name="attendance" defaultValue="yes"><option value="yes">I&apos;ll be there</option><option value="maybe">I&apos;m still checking</option><option value="no">I&apos;m sending love from afar</option></select></label>
        <label>Message<textarea name="message" rows={3} placeholder="A note for the couple (optional)" /></label>
        <Button type="submit" className="bg-[var(--ink)] text-[var(--paper)] hover:bg-[var(--accent)]">Send RSVP</Button>
        {error && <p className="form-error" role="alert">{error}</p>}
      </form>}
    </section>
  );
}
