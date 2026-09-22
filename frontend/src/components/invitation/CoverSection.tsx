import type { InvitationData } from "./types";

export function CoverSection({ data }: { data: InvitationData }) {
  return (
    <section className="invitation-cover" aria-labelledby="invitation-title">
      <div className="cover-image" role="img" aria-label="A quiet wedding portrait" />
      <div className="cover-copy">
        <p className="cover-kicker">{data.guestName ? `Dear ${data.guestName}` : "A small note from us"}</p>
        <h1 id="invitation-title">
          {data.couple.bride}
          <span>&</span>
          {data.couple.groom}
        </h1>
        <p className="cover-date">{data.date}</p>
        <a className="cover-link" href="#couple">Open our story <span aria-hidden="true">↓</span></a>
      </div>
    </section>
  );
}
