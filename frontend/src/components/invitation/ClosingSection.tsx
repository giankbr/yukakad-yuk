import type { InvitationData } from "./types";

export function ClosingSection({ data }: { data: InvitationData }) {
  return (
    <section className="invitation-section" aria-labelledby="closing-title">
      <p className="section-label">Thank you</p>
      <h2 id="closing-title">See you soon.</h2>
      <p style={{ maxWidth: "34rem", color: "var(--muted)", lineHeight: 1.7, marginTop: "1rem" }}>{data.couple.note}</p>
      <p className="signature">{data.couple.bride} &amp; {data.couple.groom}</p>
    </section>
  );
}
