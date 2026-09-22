"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";

export function WishesSection({ slug, guestToken }: { slug: string; guestToken?: string }) {
  const [sent, setSent] = useState(false);
  const [error, setError] = useState("");
  return <section className="invitation-section wishes-section" aria-labelledby="wishes-title">
    <div className="wishes-heading"><p className="section-label">Leave a little light</p><h2 id="wishes-title">Your words will stay with us.</h2></div>
    {sent ? <p className="rsvp-success" role="status">Your wish is on its way. Thank you.</p> : <form className="wishes-form" onSubmit={async (event) => { event.preventDefault(); setError(""); const form = new FormData(event.currentTarget); const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8080"}/api/public/invitation/${slug}/wishes`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ guest_token: guestToken, name: form.get("name"), message: form.get("message") }), }); if (response.ok) setSent(true); else setError("Your wish could not be sent yet. Please try once more."); }}>
      <label>Name<input required name="name" placeholder="Your name" /></label>
      <label>Your wish<textarea required name="message" rows={4} placeholder="Write something warm..." /></label>
      <Button type="submit" className="border border-[var(--ink)] text-[var(--ink)] hover:bg-[var(--ink)] hover:text-[var(--paper)]">Leave a wish</Button>
      {error && <p className="form-error" role="alert">{error}</p>}
    </form>}
  </section>;
}
