// Painted ornaments for "Arabesque Marun" (rendered by /tmp/pen/art/themes/arabesque-marun.py): pressed gold-foil
// arabesque with wine-red enamel inlay — corner scrolls, a lobed medallion, a divider scroll and a multifoil
// portrait frame. Simple hand-drawn geometry, no calligraphy.

export const ART = "/themes/art/arabesque-marun";

type ArtProps = { className?: string; eager?: boolean };

function Art({ src, w, h, className, eager }: ArtProps & { src: string; w: number; h: number }) {
  return (
    // eslint-disable-next-line @next/next/no-img-element -- static decorative art, sized by CSS
    <img src={`${ART}/${src}`} alt="" aria-hidden width={w} height={h} className={className} data-nolightbox draggable={false}
      loading={eager ? "eager" : "lazy"} fetchPriority={eager ? "high" : undefined} decoding="async" />
  );
}

/** Corner arabesque (bottom-left oriented; rotate via CSS for other corners). */
export function Corner(props: ArtProps) {
  return <Art src="corner.webp" w={264} h={264} {...props} />;
}

/** Lobed medallion: eight enamelled palmette lobes around a foil star. */
export function Medallion(props: ArtProps) {
  return <Art src="medallion.webp" w={260} h={260} {...props} />;
}

/** Horizontal divider: two mirrored foil scrolls meeting at an enamelled palmette. */
export function Scroll(props: ArtProps) {
  return <Art src="scroll.webp" w={320} h={43} {...props} />;
}

/** Multifoil arch (210×280) used to clip portraits. */
export const FOIL = "M0 280V106A30 30 0 0 1 30 62A35 35 0 0 1 68 27A40 40 0 0 1 105 0A40 40 0 0 1 142 27A35 35 0 0 1 180 62A30 30 0 0 1 210 106V280Z";

/** Double foil outline with an enamel band around the multifoil arch (234×304, drawn 12px outside the clip). */
export function FoilOutline(props: ArtProps) {
  return <Art src="frame.webp" w={468} h={608} {...props} />;
}

/** Faint inked arabesque damask tile (transparent, seamless 160px). */
export const DAMASK = `url("${ART}/damask.webp")`;
