import type { InvitationData } from "./types";

export function CoupleSection({ data }: { data: InvitationData }) {
  return (
    <section id="couple" className="invitation-section couple-section" aria-labelledby="couple-title">
      <div className="section-mark">Together, in this season</div>
      <div className="couple-grid">
        <div>
          <p className="section-label">The two of us</p>
          <h2 id="couple-title">A home is a person, and we found ours in each other.</h2>
        </div>
        <div className="couple-note">
          <p>{data.couple.note}</p>
          <div className="signature">{data.couple.bride} + {data.couple.groom}</div>
        </div>
      </div>
    </section>
  );
}
