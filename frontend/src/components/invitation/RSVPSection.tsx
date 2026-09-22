"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";

export async function sendRSVP(slug: string, body: { guest_token?: string; attendance: FormDataEntryValue | null; attendees_count: number; message: string }) {
  const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8080"}/api/public/invitation/${encodeURIComponent(slug)}/rsvp`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) });
  if (!response.ok) throw new Error("RSVP not saved");
}

export function RSVPSection({ slug, guestToken, demo = false }: { slug: string; guestToken?: string; demo?: boolean }) {
  const [sent, setSent] = useState(false);
  const [error, setError] = useState("");
  const [pending, setPending] = useState(false);
  return (
    <section className="invitation-section rsvp-section" aria-labelledby="rsvp-title">
      <div><p className="section-label">Save us a seat</p><h2 id="rsvp-title">Will you be there?</h2><p className="rsvp-intro">A quick note helps us prepare the right amount of joy.</p></div>
      {sent ? <p className="rsvp-success" role="status">{demo ? "Preview berhasil. Jawaban contoh tidak dikirim." : "Thank you. Your answer has been saved."}</p> : <form className="rsvp-form" onSubmit={async (event) => {
        event.preventDefault();
        if (pending) return;
        setError("");
        if (demo) { setSent(true); return; }
        const form = new FormData(event.currentTarget);
        setPending(true);
        try {
          await sendRSVP(slug, { guest_token: guestToken, attendance: form.get("attendance"), attendees_count: 1, message: `${form.get("name")}: ${form.get("message") ?? ""}` });
          setSent(true);
        } catch { setError("We could not save your answer. Please check your connection and try again."); }
        finally { setPending(false); }
      }}>
        <label>Name<input required name="name" maxLength={100} autoComplete="name" placeholder="Your name" /></label>
        <label>Attendance<select name="attendance" defaultValue="yes"><option value="yes">I&apos;ll be there</option><option value="maybe">I&apos;m still checking</option><option value="no">I&apos;m sending love from afar</option></select></label>
        <label>Message<textarea name="message" maxLength={850} rows={3} placeholder="A note for the couple (optional)" /></label>
        <Button type="submit" disabled={pending} className="bg-[var(--ink)] text-[var(--paper)] hover:bg-[var(--accent)]">{pending ? "Sending…" : "Send RSVP"}</Button>
        {error && <p className="form-error" role="alert">{error}</p>}
      </form>}
    </section>
  );
}
