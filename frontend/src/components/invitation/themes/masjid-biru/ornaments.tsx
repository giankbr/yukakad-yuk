// Painted ornaments for "Masjid Biru" (rendered by /tmp/pen/art/themes/masjid-biru.py): a layered mosque skyline
// (watercolour haze + gouache silhouette with lit windows), brass lanterns, a glowing crescent and a gold star.

export const ART = "/themes/art/masjid-biru";

type ArtProps = { className?: string; eager?: boolean };

function Art({ src, w, h, className, eager }: ArtProps & { src: string; w: number; h: number }) {
  return (
    // eslint-disable-next-line @next/next/no-img-element -- static decorative art, sized by CSS
    <img src={`${ART}/${src}`} alt="" aria-hidden width={w} height={h} className={className} data-nolightbox draggable={false}
      loading={eager ? "eager" : "lazy"} fetchPriority={eager ? "high" : undefined} decoding="async" />
  );
}

/** Mosque skyline: central dome, two side domes, minarets and a hazy distant city behind. */
export function Skyline(props: ArtProps) {
  return <Art src="skyline.webp" w={780} h={320} {...props} />;
}

/** A hanging lantern: the outer <span> swings (CSS); the string length is `drop` px; the glow flickers via ::after. */
export function Lantern({ className, drop = 60, eager }: ArtProps & { drop?: number }) {
  return (
    <span className={className} aria-hidden style={{ ["--drop" as string]: `${drop}px` }} data-lantern>
      <i data-string />
      <Art src="lantern.webp" w={128} h={196} eager={eager} />
    </span>
  );
}

export function Crescent(props: ArtProps) {
  return <Art src="moon.webp" w={200} h={200} {...props} />;
}

/** Small eight-point gold star. */
export function Star8(props: ArtProps) {
  return <Art src="star.webp" w={88} h={88} {...props} />;
}

/** Chalky interlocking eight-point star tile (transparent, seamless 180px), used as a faint repeating background. */
export const TILE = `url("${ART}/tile.webp")`;
