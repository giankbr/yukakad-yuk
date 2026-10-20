/* eslint-disable @next/next/no-img-element -- painted decorative art is served as static WebP, no next/image needed */
// Ornaments for "Palembang Aesan": pressed gold-foil raster art with ruby accents (rendered for Rawuh with
// /tmp/pen/art/themes/palembang-aesan.py): a fan crown inspired by the karsuhun of aesan gede with five trembling
// kembang goyang pins (separate layers so they sway), a songket-limar diamond and a lotus-bud corner.
import s from "./styles.module.css";

const ART = "/themes/art/palembang-aesan";
const PINS = [-60, -30, 0, 30, 60];
const loading = (eager?: boolean) => eager ? { loading: "eager" as const, fetchPriority: "high" as const } : { loading: "lazy" as const };

/** Fan crown (karsuhun-inspired) with five kembang goyang that sway on their stems. */
export function Crown({ className, eager }: { className?: string; eager?: boolean }) {
  return (
    <span className={className ? `${s.crown} ${className}` : s.crown} aria-hidden="true">
      {PINS.map((deg, index) => (
        <span key={deg} className={s.pinArm} style={{ rotate: `${deg}deg` }}>
          <img className={s.goyang} style={{ animationDelay: `${index * 0.45}s` }} src={`${ART}/goyang.webp`} alt="" width={57} height={120} {...loading(eager)} data-nolightbox />
        </span>
      ))}
      <img className={s.crownBase} src={`${ART}/crown.webp`} alt="" width={576} height={384} {...loading(eager)} data-nolightbox />
    </span>
  );
}

/** Songket-limar diamond made of dots, used as a divider jewel. */
export function Limar({ className, tone = "gold" }: { className?: string; tone?: "gold" | "red" }) {
  return <img className={className} src={`${ART}/limar-${tone}.webp`} alt="" aria-hidden width={72} height={66} loading="lazy" data-nolightbox />;
}

/** Lotus-bud corner (bunga teratai) for framed blocks. */
export function Corner({ className }: { className?: string }) {
  return <img className={className} src={`${ART}/corner.webp`} alt="" aria-hidden width={120} height={120} loading="eager" data-nolightbox />;
}
