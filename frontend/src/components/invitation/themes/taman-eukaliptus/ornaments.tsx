// Original eucalyptus ornaments for "Taman Eukaliptus" (drawn for Rawuh): silver-dollar leaves along a curved stem.

type Pt = [number, number];
const LEAF_TONES = ["#9fb4a4", "#87a293", "#b9c9b6", "#7b978a", "#a9bca2"];

function cubic(p: Pt[], t: number): { x: number; y: number; a: number } {
  const u = 1 - t;
  const x = u * u * u * p[0][0] + 3 * u * u * t * p[1][0] + 3 * u * t * t * p[2][0] + t * t * t * p[3][0];
  const y = u * u * u * p[0][1] + 3 * u * u * t * p[1][1] + 3 * u * t * t * p[2][1] + t * t * t * p[3][1];
  const dx = 3 * u * u * (p[1][0] - p[0][0]) + 6 * u * t * (p[2][0] - p[1][0]) + 3 * t * t * (p[3][0] - p[2][0]);
  const dy = 3 * u * u * (p[1][1] - p[0][1]) + 6 * u * t * (p[2][1] - p[1][1]) + 3 * t * t * (p[3][1] - p[2][1]);
  return { x, y, a: Math.atan2(dy, dx) };
}

const STEM: Pt[] = [[60, 2], [86, 80], [26, 160], [50, 254]];
const LEAVES = Array.from({ length: 13 }, (_, i) => {
  const t = 0.07 + i * 0.07;
  const { x, y, a } = cubic(STEM, t);
  const side = i % 2 ? 1 : -1;
  const size = 15 - i * 0.62;
  const off = size * 0.95;
  return {
    x: +(x + Math.cos(a + side * Math.PI / 2) * off).toFixed(1),
    y: +(y + Math.sin(a + side * Math.PI / 2) * off).toFixed(1),
    r: +size.toFixed(1),
    rot: +((a * 180) / Math.PI + side * 30).toFixed(1),
    fill: LEAF_TONES[i % LEAF_TONES.length],
    sx: +x.toFixed(1), sy: +y.toFixed(1),
  };
});

/** One hanging eucalyptus branch (viewBox 120×260, anchored at the top). */
export function Branch({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 120 260" aria-hidden="true" focusable="false">
      <path pathLength="1" className="stem" d={`M${STEM[0].join(" ")}C${STEM[1].join(" ")} ${STEM[2].join(" ")} ${STEM[3].join(" ")}`} fill="none" stroke="#6f8a76" strokeWidth="1.6" strokeLinecap="round" />
      {LEAVES.map((leaf, i) => (
        <g key={i} className="leaf" style={{ transformOrigin: `${leaf.sx}px ${leaf.sy}px`, animationDelay: `${i * 70}ms` }}>
          <path d={`M${leaf.sx} ${leaf.sy}L${leaf.x} ${leaf.y}`} stroke="#6f8a76" strokeWidth=".8" />
          <ellipse cx={leaf.x} cy={leaf.y} rx={leaf.r} ry={leaf.r * 0.86} transform={`rotate(${leaf.rot} ${leaf.x} ${leaf.y})`} fill={leaf.fill} opacity=".95" />
          <path d={`M${leaf.x - leaf.r * 0.55} ${leaf.y}H${leaf.x + leaf.r * 0.55}`} transform={`rotate(${leaf.rot} ${leaf.x} ${leaf.y})`} stroke="#ffffff" strokeOpacity=".35" strokeWidth=".7" />
        </g>
      ))}
    </svg>
  );
}

/** Small horizontal sprig for headings and labels (viewBox 120×36). */
export function Sprig({ className }: { className?: string }) {
  const leaves: Array<[number, number, number, string]> = [
    [24, 12, 7, LEAF_TONES[0]], [34, 25, 7.5, LEAF_TONES[1]], [48, 11, 8, LEAF_TONES[2]], [60, 25, 8, LEAF_TONES[3]],
    [72, 11, 7.5, LEAF_TONES[0]], [86, 24, 7, LEAF_TONES[4]], [97, 13, 6, LEAF_TONES[1]],
  ];
  return (
    <svg className={className} viewBox="0 0 120 36" aria-hidden="true" focusable="false">
      <path pathLength="1" className="stem" d="M8 20C40 16 80 22 112 16" fill="none" stroke="#6f8a76" strokeWidth="1.2" strokeLinecap="round" />
      {leaves.map(([x, y, r, fill], i) => <ellipse key={i} className="leaf" cx={x} cy={y} rx={r} ry={r * 0.82} fill={fill} style={{ transformOrigin: `${x}px 18px`, animationDelay: `${i * 80}ms` }} />)}
    </svg>
  );
}
