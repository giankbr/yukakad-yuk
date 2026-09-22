import type { InvitationData } from "./types";

export function EventSection({ data }: { data: InvitationData }) {
  return (
    <section className="invitation-section event-section" aria-labelledby="event-title">
      <div className="event-heading">
        <p className="section-label">Meet us there</p>
        <h2 id="event-title">The day, in two chapters.</h2>
        <p>{data.place}<br />{data.address}</p>
      </div>
      <div className="event-list">
        {data.events.map((event) => (
          <article className="event-row" key={event.name}>
            <div className="event-time"><span>{event.date}</span><strong>{event.time}</strong></div>
            <div><h3>{event.name}</h3><p>{event.venue}</p></div>
          </article>
        ))}
      </div>
    </section>
  );
}
