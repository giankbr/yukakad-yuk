// Hand-painted watercolour eucalyptus for "Taman Eukaliptus" (rendered for Rawuh with /tmp/pen/art/themes/taman-eukaliptus.py).
const ART = "/themes/art/taman-eukaliptus";

const BRANCH = { a: [195, 642], b: [177, 628] } as const;

/** One hanging silver-dollar eucalyptus branch, anchored at the top. Two painted variants so a garland never repeats. */
export function Branch({ className, variant = "a", eager = false }: { className?: string; variant?: keyof typeof BRANCH; eager?: boolean }) {
  const [w, h] = BRANCH[variant];
  return (
    // eslint-disable-next-line @next/next/no-img-element -- static decorative theme art
    <img className={className} src={`${ART}/branch-${variant}.webp`} alt="" aria-hidden width={w} height={h}
      loading={eager ? "eager" : "lazy"} fetchPriority={eager ? "high" : undefined} decoding="async" data-nolightbox />
  );
}

/** Small horizontal sprig for headings and labels (240×60). */
export function Sprig({ className }: { className?: string }) {
  return (
    // eslint-disable-next-line @next/next/no-img-element -- static decorative theme art
    <img className={className} src={`${ART}/sprig.webp`} alt="" aria-hidden width={240} height={60} loading="lazy" decoding="async" data-nolightbox />
  );
}
