// Original ornaments for "Palembang Aesan": a fan crown inspired by the karsuhun of aesan gede with
// trembling kembang goyang pins, a songket-limar diamond, and a lotus-bud corner. Drawn for Rawuh.
import s from "./styles.module.css";

const PETALS = [-72, -54, -36, -18, 0, 18, 36, 54, 72];

/** Fan crown (karsuhun-inspired) with five kembang goyang that sway on their stems. */
export function Crown({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 240 160" aria-hidden="true" focusable="false">
      <defs>
        <linearGradient id="pl-gold" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stopColor="#f6dc95" />
          <stop offset=".55" stopColor="#d6a548" />
          <stop offset="1" stopColor="#9c6d22" />
        </linearGradient>
      </defs>
      {/* kembang goyang: thin springs topped by small blossoms */}
      {[-60, -30, 0, 30, 60].map((deg, index) => (
        <g key={deg} transform={`translate(120 132) rotate(${deg})`}>
          <g className={s.goyang} style={{ animationDelay: `${index * 0.45}s` }}>
            <path d="M0 -78 C 3 -88 -3 -96 0 -106" fill="none" stroke="#d6a548" strokeWidth="1.2" />
            {[0, 72, 144, 216, 288].map(r => <ellipse key={r} cx="0" cy="-113" rx="2.6" ry="5.2" fill="url(#pl-gold)" transform={`rotate(${r} 0 -108)`} />)}
            <circle cx="0" cy="-108" r="2.2" fill="#9b1520" />
          </g>
        </g>
      ))}
      {/* outer fan */}
      {PETALS.map(deg => (
        <g key={deg} transform={`translate(120 132) rotate(${deg})`}>
          <path d={`M0 0 C -9 -22 -8 ${-50 - (72 - Math.abs(deg)) / 4} 0 ${-70 - (72 - Math.abs(deg)) / 3} C 8 ${-50 - (72 - Math.abs(deg)) / 4} 9 -22 0 0 Z`} fill="url(#pl-gold)" stroke="#7a4f14" strokeWidth=".6" />
          <path d={`M0 -10 L0 ${-58 - (72 - Math.abs(deg)) / 3.4}`} stroke="#9c6d22" strokeWidth=".8" />
          <circle cx="0" cy={-40 - (72 - Math.abs(deg)) / 5} r="2" fill="#9b1520" />
        </g>
      ))}
      {/* inner fan of small leaves */}
      {[-60, -40, -20, 0, 20, 40, 60].map(deg => (
        <path key={deg} transform={`translate(120 132) rotate(${deg})`} d="M0 0 C -6 -12 -5 -26 0 -34 C 5 -26 6 -12 0 0 Z" fill="#f6dc95" stroke="#9c6d22" strokeWidth=".6" />
      ))}
      {/* jewelled base band */}
      <path d="M44 130 Q120 110 196 130 L192 148 Q120 128 48 148 Z" fill="url(#pl-gold)" stroke="#7a4f14" strokeWidth=".8" />
      {[60, 80, 100, 120, 140, 160, 180].map((x, i) => <circle key={x} cx={x} cy={129 + Math.abs(120 - x) / 9 - 6 + (i === 3 ? 0 : 0)} r={i === 3 ? 4 : 2.4} fill={i === 3 ? "#9b1520" : "#fbf3e2"} stroke="#7a4f14" strokeWidth=".5" />)}
      {/* hanging tassels (rumbai) */}
      {[52, 70, 88, 106, 134, 152, 170, 188].map(x => <path key={x} d={`M${x} ${146 - Math.abs(120 - x) / 10} v8`} stroke="#d6a548" strokeWidth="1.4" strokeLinecap="round" />)}
    </svg>
  );
}

/** Songket-limar diamond made of dots, used as a divider jewel. */
export function Limar({ className }: { className?: string }) {
  const dots = [[12, 1], [17, 6], [22, 11], [17, 16], [12, 21], [7, 16], [2, 11], [7, 6]];
  return (
    <svg className={className} viewBox="0 0 24 22" aria-hidden="true" focusable="false">
      {dots.map(([x, y]) => <circle key={`${x}-${y}`} cx={x} cy={y} r="1.5" fill="currentColor" />)}
      <path d="M12 7 L16 11 L12 15 L8 11 Z" fill="currentColor" />
    </svg>
  );
}

/** Lotus-bud corner (bunga teratai) for framed blocks. */
export function Corner({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 48 48" aria-hidden="true" focusable="false">
      <path d="M2 46 V20 M2 46 H28" stroke="currentColor" strokeWidth="1.2" fill="none" />
      <path d="M8 40 C 8 26 16 16 26 12 C 22 20 20 30 8 40 Z" fill="currentColor" opacity=".85" />
      <path d="M8 40 C 18 38 28 32 34 22 C 26 24 16 30 8 40 Z" fill="currentColor" opacity=".55" />
      <circle cx="30" cy="10" r="2" fill="currentColor" />
      <circle cx="38" cy="18" r="1.4" fill="currentColor" />
    </svg>
  );
}
