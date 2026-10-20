// Painted ornaments for "Kaligrafi Emas" (rendered by /tmp/pen/art/themes/kaligrafi-emas.py): pressed gold-foil
// mihrab, a khatam rosette with an ochre/teal tezhip wash, a portrait crest and a small foil star. No calligraphic
// artwork — Arabic elsewhere is typeset text.

export const ART = "/themes/art/kaligrafi-emas";

type ArtProps = { className?: string; eager?: boolean };

function Art({ src, w, h, className, eager }: ArtProps & { src: string; w: number; h: number }) {
  return (
    // eslint-disable-next-line @next/next/no-img-element -- static decorative art, sized by CSS
    <img src={`${ART}/${src}`} alt="" aria-hidden width={w} height={h} className={className} data-nolightbox draggable={false}
      loading={eager ? "eager" : "lazy"} fetchPriority={eager ? "high" : undefined} decoding="async" />
  );
}

/** Khatam rosette: interlaced squares and eight-point stars in gold foil over an ochre wash with a teal heart. */
export function Rosette(props: ArtProps) {
  return <Art src="rosette.webp" w={240} h={240} {...props} />;
}

/** Small eight-point foil star used in dividers and bullets. */
export function Star(props: ArtProps) {
  return <Art src="star.webp" w={72} h={74} {...props} />;
}

/** Foil crest above an arched portrait. */
export function ArchCrest(props: ArtProps) {
  return <Art src="crest.webp" w={480} h={168} {...props} />;
}

/** Hand-inked gold lattice (transparent, seamless 176px tile) for faint backgrounds. */
export const LATTICE = `url("${ART}/lattice.webp")`;
