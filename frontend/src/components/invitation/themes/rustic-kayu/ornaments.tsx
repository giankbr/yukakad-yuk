// Original rustic ornaments for "Rustic Kayu": baby's breath sprays, twine bow and twine line (drawn for Rawuh).

/** Tiny flower heads of the baby's breath spray: [x, y, r]. */
const BLOOMS: Array<[number, number, number]> = [
  [22, 18, 3.2], [30, 12, 2.6], [16, 26, 2.4], [38, 20, 3], [44, 12, 2.4], [52, 22, 2.8], [60, 14, 3.1], [66, 24, 2.4],
  [74, 16, 2.7], [82, 26, 2.2], [26, 34, 2.2], [48, 32, 2.5], [70, 34, 2.3], [34, 6, 2], [56, 6, 2.2], [88, 18, 2.1], [12, 16, 2],
];

/** Baby's breath spray (viewBox 100×120), stems meet at the bottom center. */
export function BabysBreath({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 100 120" aria-hidden="true" focusable="false">
      <g fill="none" stroke="#8d9a6e" strokeWidth="1" strokeLinecap="round">
        <path pathLength="1" className="stem" d="M50 118C49 90 40 60 22 18" />
        <path pathLength="1" className="stem" d="M50 118C51 88 58 58 60 14" />
        <path pathLength="1" className="stem" d="M50 118C52 92 66 62 82 26" />
        <path pathLength="1" className="stem" d="M41 66C36 50 30 36 16 26M44 74C42 56 44 40 38 20M30 38L30 12M56 60C52 44 50 34 48 32M58 40L52 22M63 54C68 42 72 36 74 16M66 44L70 34M75 34L88 18M24 30L12 16M44 30L34 6M60 30L56 6M72 40L66 24M54 44L44 12" strokeWidth=".7" />
      </g>
      <g className="blooms">
        {BLOOMS.map(([x, y, r], i) => (
          <g key={i} transform={`translate(${x} ${y})`}>
            <circle r={r} fill="#fffdf6" stroke="#d9d2c2" strokeWidth=".5" />
            <circle r={r * .32} fill="#e8e0cc" />
          </g>
        ))}
      </g>
      <g fill="#a3ad84">
        <path d="M47 92C42 88 40 84 41 80C45 83 47 87 47 92Z" />
        <path d="M53 86C58 82 60 78 59 74C55 77 53 81 53 86Z" />
      </g>
    </svg>
  );
}

/** Twine bow (viewBox 80×40). */
export function Bow({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 80 40" aria-hidden="true" focusable="false">
      <g fill="none" stroke="#a9834f" strokeWidth="2.2" strokeLinecap="round">
        <path d="M40 18C30 4 12 6 14 16C16 26 32 22 40 18Z" />
        <path d="M40 18C50 4 68 6 66 16C64 26 48 22 40 18Z" />
        <path d="M38 20C34 28 28 34 22 38M42 20C46 28 52 34 58 38" />
      </g>
      <g fill="none" stroke="#c9a676" strokeWidth=".7" strokeDasharray="1.6 2">
        <path d="M40 18C30 4 12 6 14 16M40 18C50 4 68 6 66 16" />
      </g>
      <circle cx="40" cy="19" r="4" fill="#a9834f" />
    </svg>
  );
}

/** Wavy twine divider (viewBox 220×20). */
export function Twine({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 220 20" aria-hidden="true" focusable="false">
      <path pathLength="1" className="twine" d="M2 10C22 2 38 18 58 10S94 2 110 10S146 18 162 10S198 2 218 10" fill="none" stroke="#a9834f" strokeWidth="1.6" strokeLinecap="round" />
      <path d="M2 10C22 2 38 18 58 10S94 2 110 10S146 18 162 10S198 2 218 10" fill="none" stroke="#d5b98b" strokeWidth=".6" strokeDasharray="2 3" />
      <circle cx="110" cy="10" r="3.4" fill="#fffdf6" stroke="#d9d2c2" strokeWidth=".6" />
      <circle cx="104" cy="6" r="2.2" fill="#fffdf6" stroke="#d9d2c2" strokeWidth=".5" />
      <circle cx="116" cy="6" r="2.4" fill="#fffdf6" stroke="#d9d2c2" strokeWidth=".5" />
    </svg>
  );
}
