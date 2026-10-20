// Hand-painted rustic ornaments for "Rustic Kayu" (rendered for Rawuh with /tmp/pen/art/themes/rustic-kayu.py):
// gouache baby's breath on watercolour stems, a painted twine bow and a twine divider.
const ART = "/themes/art/rustic-kayu";

type ArtProps = { className?: string; eager?: boolean };

/** Baby's breath spray (260×336), stems meet at the bottom center. */
export function BabysBreath({ className, eager = false }: ArtProps) {
  return (
    // eslint-disable-next-line @next/next/no-img-element -- static decorative theme art
    <img className={className} src={`${ART}/spray.webp`} alt="" aria-hidden width={260} height={336}
      loading={eager ? "eager" : "lazy"} fetchPriority={eager ? "high" : undefined} decoding="async" data-nolightbox />
  );
}

/** Twine bow (170×110). */
export function Bow({ className, eager = false }: ArtProps) {
  return (
    // eslint-disable-next-line @next/next/no-img-element -- static decorative theme art
    <img className={className} src={`${ART}/bow.webp`} alt="" aria-hidden width={170} height={110} loading={eager ? "eager" : "lazy"} decoding="async" data-nolightbox />
  );
}

/** Wavy twine divider with a few florets (400×32). */
export function Twine({ className }: ArtProps) {
  return (
    // eslint-disable-next-line @next/next/no-img-element -- static decorative theme art
    <img className={className} src={`${ART}/twine.webp`} alt="" aria-hidden width={400} height={32} loading="lazy" decoding="async" data-nolightbox />
  );
}
