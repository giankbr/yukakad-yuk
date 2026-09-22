import type { InvitationData } from "./types";

export function LocationSection({ data }: { data: InvitationData }) {
  const link = data.mapsUrl || `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(data.address || data.place)}`;

  return (
    <section className="invitation-section" aria-labelledby="location-title">
      <p className="section-label">Find your way</p>
      <h2 id="location-title">{data.place}</h2>
      <p style={{ color: "var(--muted)", marginTop: ".75rem" }}>{data.address}</p>
      <a className="cover-link" href={link} target="_blank" rel="noreferrer">
        Open in Google Maps <span aria-hidden="true">↗</span>
      </a>
    </section>
  );
}
