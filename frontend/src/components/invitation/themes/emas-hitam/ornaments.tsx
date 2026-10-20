// Pressed gold-foil art-deco pieces for "Emas Hitam" (rendered for Rawuh with /tmp/pen/art/themes/emas-hitam.py).
import s from "./styles.module.css";

const ART = "/themes/art/emas-hitam";

type ArtProps = { className?: string; eager?: boolean };

/** Sunburst fan (460×232). A glint sweeps across the foil (masked to the art) once it is revealed. */
export function Fan({ className, eager = false }: ArtProps) {
  return (
    <span className={`${s.fan} ${className ?? ""}`} aria-hidden>
      {/* eslint-disable-next-line @next/next/no-img-element -- static decorative theme art */}
      <img src={`${ART}/fan.webp`} alt="" width={460} height={232} loading={eager ? "eager" : "lazy"} fetchPriority={eager ? "high" : undefined} decoding="async" data-nolightbox />
    </span>
  );
}

/** Stepped art-deco corner (150×150, top-left orientation; rotate via CSS for the others). */
export function Corner({ className }: ArtProps) {
  return (
    // eslint-disable-next-line @next/next/no-img-element -- static decorative theme art
    <img className={className} src={`${ART}/corner.webp`} alt="" aria-hidden width={150} height={150} decoding="async" data-nolightbox />
  );
}

/** Divider: tapered foil lines, chevrons and a double diamond (420×33). */
export function Rule({ className }: ArtProps) {
  return (
    // eslint-disable-next-line @next/next/no-img-element -- static decorative theme art
    <img className={`${s.ruleArt} ${className ?? ""}`} src={`${ART}/rule.webp`} alt="" aria-hidden width={420} height={33} loading="lazy" decoding="async" data-nolightbox />
  );
}
