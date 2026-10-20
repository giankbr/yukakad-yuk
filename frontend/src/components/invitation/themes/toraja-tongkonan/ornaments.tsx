/* eslint-disable @next/next/no-img-element -- painted decorative art is served as static WebP, no next/image needed */
// Ornaments for "Toraja Tongkonan": linocut relief print + matte gouache raster art (rendered for Rawuh with
// /tmp/pen/art/themes/toraja-tongkonan.py): a tongkonan house with its upswept saddle roof and stacked buffalo
// horns, a pa' barre allo sun disc, the roof alone as a card crown and a pa' tedong buffalo-head marker.
import s from "./styles.module.css";

const ART = "/themes/art/toraja-tongkonan";
type Load = { eager?: boolean };
const loading = (eager?: boolean) => eager ? { loading: "eager" as const, fetchPriority: "high" as const } : { loading: "lazy" as const };

/** Pa' barre allo — the rising-sun carving. `rays` adds the slowly turning ray ring; `initial` shows a monogram. */
export function BarreAllo({ className, initial, rays, eager }: { className?: string; initial?: string; rays?: boolean } & Load) {
  return (
    <span className={className ? `${s.sun} ${className}` : s.sun} aria-hidden="true">
      {rays && <img className={s.rays} src={`${ART}/rays.webp`} alt="" width={520} height={520} {...loading(eager)} data-nolightbox />}
      <img className={rays ? s.sunDisc : s.sunFull} src={`${ART}/${initial ? "plate" : "sun"}.webp`} alt="" width={300} height={300} {...loading(eager)} data-nolightbox />
      {initial && <span className={s.sunText}>{initial}</span>}
    </span>
  );
}

/** Tongkonan house, front view. */
export function Tongkonan({ className, eager }: { className?: string } & Load) {
  return <img className={className} src={`${ART}/house.webp`} alt="" aria-hidden width={500} height={403} {...loading(eager)} data-nolightbox />;
}

/** Upswept roof alone — used to crown cards. */
export function Roof({ className, tone = "red" }: { className?: string; tone?: "red" | "black" }) {
  return <img className={className} src={`${ART}/roof-${tone}.webp`} alt="" aria-hidden width={600} height={128} loading="lazy" data-nolightbox />;
}

/** Pa' tedong — stylised buffalo head used as a marker. */
export function Tedong({ className, tone = "red" }: { className?: string; tone?: "red" | "black" | "yellow" }) {
  return <img className={className} src={`${ART}/tedong-${tone}.webp`} alt="" aria-hidden width={96} height={74} loading="lazy" data-nolightbox />;
}
