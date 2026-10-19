// Original ornaments for "Kaligrafi Emas": a pointed mihrab arch, an eight-fold khatam rosette and a star lattice.
// All drawn here as simple geometry (no calligraphic artwork); Arabic text elsewhere is typeset.

/** Points of a 16-vertex eight-point star (alternating outer/inner radius), centred on 0,0. */
function starPoints(outer: number, inner: number) {
  return Array.from({ length: 16 }, (_, i) => {
    const angle = (Math.PI / 8) * i - Math.PI / 2;
    const r = i % 2 === 0 ? outer : inner;
    return `${(Math.cos(angle) * r).toFixed(2)},${(Math.sin(angle) * r).toFixed(2)}`;
  }).join(" ");
}

const STAR_OUT = starPoints(46, 30);
const STAR_MID = starPoints(30, 19);

/** Khatam rosette: two interlaced squares, an inner eight-point star and a ring of petals. */
export function Rosette({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="-50 -50 100 100" aria-hidden focusable="false">
      <g fill="none" stroke="currentColor" strokeWidth="1" strokeLinejoin="round">
        <rect x="-32" y="-32" width="64" height="64" />
        <rect x="-32" y="-32" width="64" height="64" transform="rotate(45)" />
        <polygon points={STAR_OUT} strokeWidth=".8" />
        <polygon points={STAR_MID} />
        <circle r="12" />
        <circle r="48" strokeWidth=".6" strokeDasharray="1 3" />
      </g>
      <g fill="currentColor">
        {Array.from({ length: 8 }, (_, i) => <circle key={i} r="1.6" cx="0" cy="-39" transform={`rotate(${i * 45})`} />)}
        <circle r="3" />
      </g>
    </svg>
  );
}

/** Small eight-point star used in dividers and bullets. */
export function Star({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="-12 -12 24 24" aria-hidden focusable="false">
      <rect x="-7" y="-7" width="14" height="14" fill="currentColor" />
      <rect x="-7" y="-7" width="14" height="14" fill="currentColor" transform="rotate(45)" />
      <circle r="3" fill="var(--bg, #fff)" />
    </svg>
  );
}

/** Full-height pointed (mihrab) arch with a double line; stretches to its box. */
export function Mihrab({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 300 600" preserveAspectRatio="none" aria-hidden focusable="false">
      <g fill="none" stroke="currentColor" vectorEffect="non-scaling-stroke">
        <path vectorEffect="non-scaling-stroke" strokeWidth="1.4" d="M12 600V236C12 138 86 86 150 12C214 86 288 138 288 236V600" />
        <path vectorEffect="non-scaling-stroke" strokeWidth=".8" d="M24 600V240C24 146 94 100 150 30C206 100 276 146 276 240V600" />
      </g>
    </svg>
  );
}

/** Arch-topped frame for a portrait; children (the photo) are clipped by CSS. */
export function ArchCrest({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 120 40" aria-hidden focusable="false">
      <g fill="none" stroke="currentColor" strokeWidth="1">
        <path d="M2 38C24 38 40 26 60 4C80 26 96 38 118 38" />
        <path d="M18 38C34 36 46 28 60 14C74 28 86 36 102 38" strokeWidth=".7" />
      </g>
      <g fill="currentColor"><circle cx="60" cy="4" r="2.4" /><circle cx="2" cy="38" r="1.6" /><circle cx="118" cy="38" r="1.6" /></g>
    </svg>
  );
}

/** Lattice of eight-point stars as a tiling background (used at low opacity). */
export const LATTICE = `url("data:image/svg+xml,${encodeURIComponent(
  "<svg xmlns='http://www.w3.org/2000/svg' width='44' height='44' viewBox='0 0 44 44'><g fill='none' stroke='#b08a3e' stroke-width='.7'><rect x='13' y='13' width='18' height='18'/><path d='M22 9.3L34.7 22 22 34.7 9.3 22z'/><path d='M0 22h9.3M34.7 22H44M22 0v9.3M22 34.7V44'/></g></svg>",
)}")`;
