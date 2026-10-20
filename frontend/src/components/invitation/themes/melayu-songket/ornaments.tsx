/* eslint-disable @next/next/no-img-element -- painted decorative art is served as static WebP, no next/image needed */
// Ornaments for "Melayu Songket": hand-painted gouache + pressed gold foil raster art (rendered for Rawuh with
// /tmp/pen/art/themes/melayu-songket.py): a bunga cengkih medallion ringed by pucuk rebung, an awan larat scroll
// divider and a tumpal marker.
import s from "./styles.module.css";

const ART = "/themes/art/melayu-songket";

/** Bunga cengkih (clove flower) medallion; the outer pucuk rebung ring turns slowly. */
export function Medallion({ className, initials, eager }: { className?: string; initials?: string; eager?: boolean }) {
  const load = eager ? { loading: "eager" as const, fetchPriority: "high" as const } : { loading: "lazy" as const };
  return (
    <span className={className ? `${s.medal} ${className}` : s.medal} aria-hidden="true">
      <img className={s.ring} src={`${ART}/ring.webp`} alt="" width={428} height={428} {...load} data-nolightbox />
      <img className={s.medalCore} src={`${ART}/${initials ? "plate" : "core"}.webp`} alt="" width={330} height={330} {...load} data-nolightbox />
      {initials && <span className={s.medalText}>{initials}</span>}
    </span>
  );
}

/** Awan larat (drifting cloud scroll) divider; it unrolls from the centre when revealed. */
export function AwanLarat({ className }: { className?: string }) {
  return <img className={className ? `${s.draw} ${className}` : s.draw} src={`${ART}/awan.webp`} alt="" aria-hidden width={280} height={49} loading="lazy" data-nolightbox />;
}

/** Small tumpal (pucuk rebung) triangle used as list/timeline markers. */
export function Rebung({ className }: { className?: string }) {
  return <img className={className} src={`${ART}/rebung.webp`} alt="" aria-hidden width={60} height={77} loading="lazy" data-nolightbox />;
}
