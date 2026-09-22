import type { InvitationData } from "./types";

export function GallerySection({ data }: { data: InvitationData }) {
  return (
    <section className="invitation-section gallery-section" aria-labelledby="gallery-title">
      <div className="gallery-heading"><p className="section-label">Somewhere between then and now</p><h2 id="gallery-title">Frames we keep coming back to.</h2></div>
      <div className="gallery-strip">
        {data.gallery.map((image, index) => <img key={image} src={image} alt={`A moment from the couple's story ${index + 1}`} />)}
      </div>
    </section>
  );
}
