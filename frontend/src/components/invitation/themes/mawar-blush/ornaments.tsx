// Hand-painted watercolour roses for "Mawar Blush" (rendered for Rawuh with /tmp/pen/art/themes/mawar-blush.py).
const ART = "/themes/art/mawar-blush";

type ArtProps = { className?: string; eager?: boolean };

/** Corner bouquet (520×453): roses spilling toward the bottom-left; flip with CSS `scale` for other corners. */
export function Bouquet({ className, eager = false }: ArtProps) {
  return (
    // eslint-disable-next-line @next/next/no-img-element -- static decorative theme art
    <img className={className} src={`${ART}/bouquet.webp`} alt="" aria-hidden width={520} height={453}
      loading={eager ? "eager" : "lazy"} fetchPriority={eager ? "high" : undefined} decoding="async" data-nolightbox />
  );
}

/** Small sprig (220×161): one rose + leaves, for headings and timeline nodes. */
export function Sprig({ className }: ArtProps) {
  return (
    // eslint-disable-next-line @next/next/no-img-element -- static decorative theme art
    <img className={className} src={`${ART}/sprig.webp`} alt="" aria-hidden width={220} height={161} loading="lazy" decoding="async" data-nolightbox />
  );
}

/** Thin hand-drawn arch outline, drawn in with stroke-dashoffset (viewBox 300×420). Functional line, kept as SVG. */
export function ArchLine({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 300 420" preserveAspectRatio="none" aria-hidden="true" focusable="false">
      <path pathLength="1" d="M14 418V150C14 72 76 12 150 12S286 72 286 150V418" fill="none" stroke="currentColor" strokeWidth="1.4" vectorEffect="non-scaling-stroke" />
      <path pathLength="1" d="M26 418V154C26 82 82 26 150 26S274 82 274 154V418" fill="none" stroke="currentColor" strokeWidth=".8" opacity=".55" vectorEffect="non-scaling-stroke" />
    </svg>
  );
}

/** One painted falling petal (48×41). */
export function Petal() {
  // eslint-disable-next-line @next/next/no-img-element -- static decorative theme art
  return <img src={`${ART}/petal.webp`} alt="" aria-hidden width={48} height={41} loading="lazy" decoding="async" data-nolightbox />;
}
