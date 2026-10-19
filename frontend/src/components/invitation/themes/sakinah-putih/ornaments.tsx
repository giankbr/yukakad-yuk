// Original ornaments for "Sakinah Putih": a girih-like eight-petal rosette of interlaced circles and a leafy vine line.

/** Eight overlapping circles on a ring form soft petals; each petal is its own <circle> so CSS can bloom them in turn. */
export function Bloom({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="-50 -50 100 100" aria-hidden focusable="false">
      <g fill="none" stroke="currentColor" strokeWidth=".9">
        <circle r="46" strokeWidth=".6" />
        <circle r="44" strokeDasharray=".6 3.4" strokeLinecap="round" strokeWidth="1.4" />
        <g data-petals>
          {Array.from({ length: 8 }, (_, i) => (
            <circle key={i} r="16" cx="0" cy="-16" transform={`rotate(${i * 45})`} style={{ ["--i" as string]: i }} />
          ))}
        </g>
        <circle r="6" />
      </g>
      <circle r="2.2" fill="currentColor" />
    </svg>
  );
}

/** Horizontal vine with paired leaves; the stem uses pathLength=1 so it can draw itself. */
export function Vine({ className, flip }: { className?: string; flip?: boolean }) {
  const leaves = [30, 90, 150, 210];
  return (
    <svg className={className} viewBox="0 0 240 24" aria-hidden focusable="false" style={flip ? { scale: "-1 1" } : undefined}>
      <path pathLength={1} d="M2 12C22 2 40 22 60 12S100 2 120 12 160 22 180 12 220 2 238 12" fill="none" stroke="currentColor" strokeWidth="1" strokeLinecap="round" />
      <g fill="currentColor" opacity=".8">
        {leaves.map((x, i) => (
          <path key={x} d="M0 0C3-5 9-6 12-4 9 0 4 2 0 0Z" transform={`translate(${x} ${i % 2 ? 15 : 9}) rotate(${i % 2 ? 30 : -30})`} />
        ))}
      </g>
      <circle cx="120" cy="12" r="2.4" fill="currentColor" />
    </svg>
  );
}

/** Scalloped edge (row of half circles) as a repeating background. */
export const SCALLOP = `url("data:image/svg+xml,${encodeURIComponent(
  "<svg xmlns='http://www.w3.org/2000/svg' width='24' height='12' viewBox='0 0 24 12'><path d='M0 12a12 12 0 0 1 24 0z' fill='#e6f0e8'/></svg>",
)}")`;
