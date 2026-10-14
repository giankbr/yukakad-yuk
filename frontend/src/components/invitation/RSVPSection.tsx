"use client";

import { useRef, useState } from "react";
import { Button } from "@/components/ui/button";

export async function sendRSVP(slug: string, body: { guest_token?: string; attendance: FormDataEntryValue | null; attendees_count: number; message: string }) {
  const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8080"}/api/public/invitation/${encodeURIComponent(slug)}/rsvp`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) });
  if (!response.ok) throw new Error("RSVP not saved");
}

export function RSVPSection({ slug, guestToken, demo = false, locale = "en" }: { slug: string; guestToken?: string; demo?: boolean; locale?: "en" | "id" }) {
  const indonesian = locale === "id";
  const formRef = useRef<HTMLFormElement>(null);
  const [sent, setSent] = useState(false);
  const [error, setError] = useState("");
  const [pending, setPending] = useState(false);
  return (
    <section className="invitation-section rsvp-section" aria-labelledby="rsvp-title">
      <div><p className="section-label">Save us a seat</p><h2 id="rsvp-title">Will you be there?</h2><p className="rsvp-intro">A quick note helps us prepare the right amount of joy.</p></div>
      {sent ? <div className="rsvp-result"><p className="rsvp-success" role="status">{demo ? "Preview berhasil. Jawaban contoh tidak dikirim." : "Thank you. Your answer has been saved."}</p>{demo && <button type="button" className="rsvp-reset" onClick={() => { setSent(false); requestAnimationFrame(() => formRef.current?.querySelector<HTMLInputElement>('input[name="name"]')?.focus()); }}>{indonesian ? "Coba lagi" : "Try again"} ↻</button>}</div> : <form ref={formRef} className="rsvp-form" onSubmit={async (event) => {
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
        <label>{indonesian ? "Nama tamu" : "Name"}<input required name="name" maxLength={100} autoComplete="name" placeholder={indonesian ? "Nama kalian" : "Your name"} /></label>
        <label>{indonesian ? "Konfirmasi hadir" : "Attendance"}<select name="attendance" defaultValue="yes"><option value="yes">{indonesian ? "Hadir" : "I’ll be there"}</option><option value="maybe">{indonesian ? "Masih ragu" : "I’m still checking"}</option><option value="no">{indonesian ? "Tidak hadir" : "I’m sending love from afar"}</option></select></label>
        <label>{indonesian ? "Pesan untuk pasangan" : "Message"}<textarea name="message" maxLength={850} rows={3} placeholder={indonesian ? "Ucapan kalian (opsional)" : "A note for the couple (optional)"} /></label>
        <Button type="submit" disabled={pending} className="bg-[var(--ink)] text-[var(--paper)] hover:bg-[var(--accent)]">{pending ? (indonesian ? "Mengirim…" : "Sending…") : (indonesian ? "Kirim RSVP" : "Send RSVP")}</Button>
        {error && <p className="form-error" role="alert">{error}</p>}
      </form>}
    </section>
  );
}
