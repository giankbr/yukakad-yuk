// Original watercolor rose ornaments for "Mawar Blush" (drawn for Rawuh; no external artwork).
import { useId } from "react";

const PETAL = "M0 0C-17 -5 -21 -29 0 -37C21 -29 17 -5 0 0Z";
const LEAF = "M0 0C9 -9 29 -10 44 0C29 10 9 9 0 0Z";

type RoseProps = { x: number; y: number; r?: number; tone?: "blush" | "rose" | "peach"; turn?: number };

const TONES = {
  blush: ["#f6cfd0", "#eeb0b5", "#de8c96", "#c26878"],
  rose: ["#f1b8be", "#e2919c", "#cd6b7b", "#a84b5e"],
  peach: ["#f9dccc", "#f2bfa8", "#e59f86", "#c97a64"],
} as const;

/** One rose: three rings of petals around a swirled heart. Centered on (x, y), r ≈ outer radius. */
function Rose({ x, y, r = 40, tone = "blush", turn = 0 }: RoseProps) {
  const c = TONES[tone];
  const k = r / 40;
  return (
    <g transform={`translate(${x} ${y}) rotate(${turn}) scale(${k})`}>
      {[0, 60, 120, 180, 240, 300].map(a => <path key={`o${a}`} d={PETAL} transform={`rotate(${a})`} fill={c[0]} opacity=".9" />)}
      {[30, 102, 174, 246, 318].map(a => <path key={`m${a}`} d={PETAL} transform={`rotate(${a}) scale(.74)`} fill={c[1]} opacity=".85" />)}
      {[0, 90, 180, 270].map(a => <path key={`i${a}`} d={PETAL} transform={`rotate(${a + 45}) scale(.48)`} fill={c[2]} opacity=".85" />)}
      <circle r="7" fill={c[2]} />
      <path d="M-5 1C-5 -5 4 -6 5 0C6 5 -1 7 -3 3C-4 0 0 -2 1 0" fill="none" stroke={c[3]} strokeWidth="1.6" strokeLinecap="round" />
    </g>
  );
}

function Leaf({ x, y, turn, size = 1, dark }: { x: number; y: number; turn: number; size?: number; dark?: boolean }) {
  return (
    <g transform={`translate(${x} ${y}) rotate(${turn}) scale(${size})`}>
      <path d={LEAF} fill={dark ? "#8fa585" : "#b4c6a6"} opacity=".9" />
      <path d="M2 0C14 -1 28 -1 40 0" fill="none" stroke={dark ? "#6f8766" : "#93ab88"} strokeWidth=".9" />
    </g>
  );
}

function Bud({ x, y, turn = 0, tone = "rose" }: { x: number; y: number; turn?: number; tone?: keyof typeof TONES }) {
  const c = TONES[tone];
  return (
    <g transform={`translate(${x} ${y}) rotate(${turn})`}>
      <path d="M0 0C-2 -10 -1 -22 0 -30" fill="none" stroke="#93ab88" strokeWidth="1.2" />
      <path d="M0 -26C-7 -30 -7 -40 0 -45C7 -40 7 -30 0 -26Z" fill={c[1]} />
      <path d="M0 -26C-4 -31 -3 -38 0 -42" fill="none" stroke={c[3]} strokeWidth=".8" opacity=".6" />
      <path d="M0 -24C-6 -24 -9 -28 -8 -32C-4 -29 -2 -27 0 -24ZM0 -24C6 -24 9 -28 8 -32C4 -29 2 -27 0 -24Z" fill="#a9bd9b" />
    </g>
  );
}

/** Watercolor filter (soft bleeding edges) + a blurred wash. Ids are unique per instance. */
function Defs({ id }: { id: string }) {
  return (
    <defs>
      <filter id={`${id}w`} x="-10%" y="-10%" width="120%" height="120%">
        <feTurbulence type="fractalNoise" baseFrequency=".045" numOctaves="2" seed="7" />
        <feDisplacementMap in="SourceGraphic" scale="5" />
      </filter>
      <filter id={`${id}b`} x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="9" /></filter>
    </defs>
  );
}

/** Corner bouquet (viewBox 220×180), roses spilling toward the bottom-left; flip with CSS for other corners. */
export function Bouquet({ className }: { className?: string }) {
  const id = useId().replace(/:/g, "");
  return (
    <svg className={className} viewBox="0 0 220 180" aria-hidden="true" focusable="false">
      <Defs id={id} />
      <g filter={`url(#${id}b)`} opacity=".55">
        <circle cx="70" cy="70" r="46" fill="#f4c6c9" />
        <circle cx="140" cy="48" r="34" fill="#f8dcd3" />
        <circle cx="40" cy="128" r="30" fill="#dfe8d6" />
      </g>
      <g filter={`url(#${id}w)`}>
        <Leaf x={92} y={92} turn={18} size={1.2} dark />
        <Leaf x={70} y={60} turn={-150} size={1.1} />
        <Leaf x={130} y={62} turn={-28} size={1} />
        <Leaf x={58} y={104} turn={110} size={1.1} dark />
        <Leaf x={150} y={84} turn={8} size={.8} />
        <Bud x={172} y={70} turn={58} />
        <Bud x={40} y={150} turn={-150} tone="peach" />
        <Rose x={72} y={70} r={40} tone="blush" turn={10} />
        <Rose x={128} y={44} r={30} tone="peach" turn={-20} />
        <Rose x={104} y={104} r={26} tone="rose" turn={34} />
        <Rose x={34} y={112} r={20} tone="peach" turn={-8} />
      </g>
      <g fill="#e7a3ac" opacity=".7">
        <circle cx="186" cy="34" r="2.2" /><circle cx="196" cy="46" r="1.5" /><circle cx="20" cy="70" r="1.8" /><circle cx="160" cy="118" r="1.6" />
      </g>
    </svg>
  );
}

/** Small sprig: one rose + two leaves, for headings and timeline nodes (viewBox 80×60). */
export function Sprig({ className }: { className?: string }) {
  const id = useId().replace(/:/g, "");
  return (
    <svg className={className} viewBox="0 0 80 60" aria-hidden="true" focusable="false">
      <Defs id={id} />
      <g filter={`url(#${id}w)`}>
        <Leaf x={40} y={34} turn={-12} size={.7} dark />
        <Leaf x={40} y={34} turn={-168} size={.7} />
        <Rose x={40} y={30} r={17} tone="rose" />
      </g>
    </svg>
  );
}

/** Thin hand-drawn arch outline, drawn in with stroke-dashoffset (viewBox 300×420). */
export function ArchLine({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 300 420" preserveAspectRatio="none" aria-hidden="true" focusable="false">
      <path pathLength="1" d="M14 418V150C14 72 76 12 150 12S286 72 286 150V418" fill="none" stroke="currentColor" strokeWidth="1.4" vectorEffect="non-scaling-stroke" />
      <path pathLength="1" d="M26 418V154C26 82 82 26 150 26S274 82 274 154V418" fill="none" stroke="currentColor" strokeWidth=".8" opacity=".55" vectorEffect="non-scaling-stroke" />
    </svg>
  );
}

/** Loose falling petal (viewBox 20×20). */
export const PETAL_SVG = "M10 2C15 4 18 10 14 16C11 19 6 18 4 14C2 9 5 3 10 2Z";
