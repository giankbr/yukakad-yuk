/* eslint-disable @next/next/no-img-element -- painted decorative art is served as static WebP, no next/image needed */
// Ornaments for "Dayak Borneo": woodcut/linocut print + gouache raster art (rendered for Rawuh with
// /tmp/pen/art/themes/dayak-borneo.py): a perched burung enggang (hornbill) split into branch, tail and body so it
// can perch and sway, a mirrored sulur (vine scroll) divider and a talawang-shield monogram plate.
import s from "./styles.module.css";

const ART = "/themes/art/dayak-borneo";
const loading = (eager?: boolean) => eager ? { loading: "eager" as const, fetchPriority: "high" as const } : { loading: "lazy" as const };

/** Burung enggang, perched, facing right. */
export function Enggang({ className, eager }: { className?: string; eager?: boolean }) {
  const img = (name: string, cls?: string) => (
    <img className={cls ? `${s.birdLayer} ${cls}` : s.birdLayer} src={`${ART}/enggang-${name}.webp`} alt="" width={528} height={330} {...loading(eager)} data-nolightbox />
  );
  return (
    <span className={className ? `${s.birdBox} ${className}` : s.birdBox} aria-hidden="true">
      {img("branch")}
      <span className={s.bird}>
        {img("tail", s.tail)}
        {img("body")}
      </span>
    </span>
  );
}

/** Sulur — mirrored vine scroll with spiral hooks, used as a section divider; it unrolls from the centre. */
export function Sulur({ className, tone = "tosca" }: { className?: string; tone?: "tosca" | "kuning" }) {
  return <img className={className ? `${s.draw} ${className}` : s.draw} src={`${ART}/sulur-${tone}.webp`} alt="" aria-hidden width={330} height={68} loading="lazy" data-nolightbox />;
}

/** Talawang shield face with a monogram, used when there is no photo. */
export function Talawang({ className, initial }: { className?: string; initial: string }) {
  return (
    <span className={className ? `${s.talawang} ${className}` : s.talawang} aria-hidden="true">
      <img src={`${ART}/talawang.webp`} alt="" width={300} height={500} loading="lazy" data-nolightbox />
      <span>{initial}</span>
    </span>
  );
}
