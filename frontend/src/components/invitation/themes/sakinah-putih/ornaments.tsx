// Painted ornaments for "Sakinah Putih" (rendered by /tmp/pen/art/themes/sakinah-putih.py): a glazed sage
// watercolour rosette, a leafy vine divider and a jasmine & olive corner spray for the cover.

export const ART = "/themes/art/sakinah-putih";

type ArtProps = { className?: string; eager?: boolean };

function Art({ src, w, h, className, eager, flip }: ArtProps & { src: string; w: number; h: number; flip?: boolean }) {
  return (
    // eslint-disable-next-line @next/next/no-img-element -- static decorative art, sized by CSS
    <img src={`${ART}/${src}`} alt="" aria-hidden width={w} height={h} className={className} data-nolightbox draggable={false}
      loading={eager ? "eager" : "lazy"} fetchPriority={eager ? "high" : undefined} decoding="async" style={flip ? { scale: "-1 1" } : undefined} />
  );
}

/** Eight translucent sage petals glazed over each other, a dotted ring and a warm heart. */
export function Bloom(props: ArtProps) {
  return <Art src="bloom.webp" w={240} h={239} {...props} />;
}

/** Horizontal watercolour vine with paired leaves and a jasmine bud in the middle. */
export function Vine({ flip, ...props }: ArtProps & { flip?: boolean }) {
  return <Art src="vine.webp" w={360} h={45} flip={flip} {...props} />;
}

/** Jasmine & olive spray for the cover corners (top-left oriented; rotate via CSS). */
export function Spray(props: ArtProps) {
  return <Art src="corner.webp" w={460} h={460} {...props} />;
}
