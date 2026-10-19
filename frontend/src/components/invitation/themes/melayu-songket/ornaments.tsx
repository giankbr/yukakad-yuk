// Original ornaments for "Melayu Songket": a bunga cengkih medallion ringed by pucuk rebung,
// an awan larat scroll divider, and a pointed "gerbang" outline. Drawn for Rawuh.
import s from "./styles.module.css";

const RING = Array.from({ length: 24 }, (_, i) => i * 15);
const PETALS = [0, 45, 90, 135, 180, 225, 270, 315];

/** Bunga cengkih (clove flower) medallion; the outer pucuk rebung ring turns slowly. */
export function Medallion({ className, initials }: { className?: string; initials?: string }) {
  return (
    <svg className={className} viewBox="0 0 200 200" aria-hidden="true" focusable="false">
      <g className={s.ring}>
        <circle cx="100" cy="100" r="96" fill="none" stroke="#e9b526" strokeWidth="1" />
        {RING.map(deg => (
          <path key={deg} transform={`rotate(${deg} 100 100)`} d="M93 6 L100 24 L107 6 Z" fill="#e9b526" opacity=".9" />
        ))}
        {RING.map(deg => <circle key={`d${deg}`} transform={`rotate(${deg + 7.5} 100 100)`} cx="100" cy="10" r="1.6" fill="#f6d670" />)}
      </g>
      <circle cx="100" cy="100" r="74" fill="#0b3f2d" stroke="#e9b526" strokeWidth="1.5" />
      <circle cx="100" cy="100" r="68" fill="none" stroke="#e9b526" strokeWidth=".6" strokeDasharray="2 4" />
      {initials ? (
        <text x="100" y="114" textAnchor="middle" fill="#f6d670" fontFamily="Marcellus, serif" fontSize="40" letterSpacing="2">{initials}</text>
      ) : (
        <g>
          {PETALS.map(deg => (
            <g key={deg} transform={`rotate(${deg} 100 100)`}>
              <path d="M100 100 C 88 82 90 60 100 46 C 110 60 112 82 100 100 Z" fill="#e9b526" />
              <path d="M100 92 C 95 80 96 66 100 58 C 104 66 105 80 100 92 Z" fill="#0b3f2d" />
            </g>
          ))}
          <circle cx="100" cy="100" r="10" fill="#f6d670" stroke="#0b3f2d" strokeWidth="2" />
          <circle cx="100" cy="100" r="3" fill="#a8322a" />
        </g>
      )}
    </svg>
  );
}

/** Awan larat (drifting cloud scroll) divider, mirrored around a small bud. */
export function AwanLarat({ className }: { className?: string }) {
  const half = "M6 12 C 18 12 22 3 32 3 C 42 3 45 13 38 16 C 33 18 30 12 34 10 M32 3 C 44 -1 54 6 60 12 M20 11 C 22 16 28 18 30 22 C 24 22 20 18 20 11 Z";
  return (
    <svg className={className} viewBox="0 0 132 26" aria-hidden="true" focusable="false">
      <g fill="none" stroke="currentColor" strokeWidth="1.3" strokeLinecap="round">
        <path className={s.draw} d={half} transform="translate(66 0) translate(0 0)" />
        <path className={s.draw} d={half} transform="translate(66 0) scale(-1 1)" />
      </g>
      <path d="M66 4 L71 12 L66 20 L61 12 Z" fill="currentColor" />
    </svg>
  );
}

/** Small tumpal (pucuk rebung) triangle used as list/timeline markers. */
export function Rebung({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 30" aria-hidden="true" focusable="false">
      <path d="M12 1 L23 29 H1 Z" fill="currentColor" />
      <path d="M12 10 L18 27 H6 Z" fill="#0b3f2d" />
      <path d="M12 18 L15 26 H9 Z" fill="currentColor" />
    </svg>
  );
}
