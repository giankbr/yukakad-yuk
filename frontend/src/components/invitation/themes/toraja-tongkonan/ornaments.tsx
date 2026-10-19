// Original ornaments for "Toraja Tongkonan": a tongkonan house with its upswept saddle roof, stacked buffalo
// horns on the front pillar and a carved red facade; a pa' barre allo sun disc; a buffalo-head marker. Drawn for Rawuh.
import s from "./styles.module.css";

const RAYS = Array.from({ length: 16 }, (_, i) => i * 22.5);

/** Pa' barre allo — the rising-sun carving: rays around concentric discs with a four-way cross. */
export function BarreAllo({ className, initial }: { className?: string; initial?: string }) {
  return (
    <svg className={className} viewBox="0 0 120 120" aria-hidden="true" focusable="false">
      <g className={s.rays}>
        {RAYS.map((deg, i) => (
          <path key={deg} transform={`rotate(${deg} 60 60)`} d="M54 4 L60 18 L66 4 Z" fill={i % 2 ? "#f3ece0" : "#e5a823"} />
        ))}
      </g>
      <circle cx="60" cy="60" r="42" fill="#16110f" stroke="#e5a823" strokeWidth="2" />
      <circle cx="60" cy="60" r="35" fill="#a3201b" />
      {initial ? (
        <>
          <circle cx="60" cy="60" r="27" fill="none" stroke="#f3ece0" strokeWidth="1" strokeDasharray="1.5 3.5" />
          <text x="60" y="71" textAnchor="middle" fill="#f3ece0" fontFamily="'Josefin Sans', sans-serif" fontSize="32" fontWeight="600">{initial}</text>
        </>
      ) : (
        <>
          {[0, 90, 180, 270].map(deg => (
            <path key={deg} transform={`rotate(${deg} 60 60)`} d="M60 60 C 52 50 52 36 60 28 C 68 36 68 50 60 60 Z" fill="#e5a823" />
          ))}
          {[45, 135, 225, 315].map(deg => <circle key={deg} transform={`rotate(${deg} 60 60)`} cx="60" cy="34" r="3" fill="#f3ece0" />)}
          <circle cx="60" cy="60" r="7" fill="#16110f" stroke="#f3ece0" strokeWidth="2" />
        </>
      )}
    </svg>
  );
}

/** Tongkonan house, front view. */
export function Tongkonan({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 240 200" aria-hidden="true" focusable="false">
      {/* saddle roof with bamboo layers */}
      <path d="M4 18 Q 60 72 120 72 Q 180 72 236 18 L 228 44 Q 180 96 120 96 Q 60 96 12 44 Z" fill="#16110f" stroke="#e5a823" strokeWidth="1.5" />
      <path d="M10 32 Q 62 84 120 84 Q 178 84 230 32" fill="none" stroke="#5a4232" strokeWidth="1.2" />
      <path d="M8 25 Q 61 78 120 78 Q 179 78 232 25" fill="none" stroke="#3a2a22" strokeWidth="1" />
      {/* carved facade, flaring outwards to the top */}
      <path d="M74 96 H166 L154 146 H86 Z" fill="#a3201b" stroke="#16110f" strokeWidth="1.5" />
      <path d="M80 110 H160" stroke="#16110f" strokeWidth="1.2" />
      <path d="M84 128 H156" stroke="#16110f" strokeWidth="1.2" />
      {Array.from({ length: 9 }, (_, i) => 82 + i * 9.5).map(x => <path key={x} d={`M${x} 110 L${x + 4.75} 102 L${x + 9.5} 110`} fill="none" stroke="#e5a823" strokeWidth="1.2" />)}
      {Array.from({ length: 8 }, (_, i) => 88 + i * 9).map(x => <circle key={x} cx={x + 4.5} cy="137" r="2" fill="#f3ece0" />)}
      <circle cx="100" cy="119" r="5" fill="none" stroke="#f3ece0" strokeWidth="1.4" />
      <circle cx="140" cy="119" r="5" fill="none" stroke="#f3ece0" strokeWidth="1.4" />
      {/* buffalo head carving (kabongo') at the centre of the facade */}
      <path d="M108 115 Q 102 108 98 112 Q 104 116 110 121 M132 115 Q 138 108 142 112 Q 136 116 130 121" fill="none" stroke="#f3ece0" strokeWidth="2" strokeLinecap="round" />
      <path d="M112 116 H128 L124 128 H116 Z" fill="#16110f" />
      {/* floor beam, stilts and the front pillar with stacked horns */}
      <rect x="80" y="146" width="80" height="6" fill="#16110f" />
      {[90, 104, 136, 150].map(x => <rect key={x} x={x - 2.5} y="152" width="5" height="34" fill="#16110f" />)}
      <rect x="117" y="96" width="6" height="90" fill="#16110f" />
      {[156, 164, 172, 180].map(y => (
        <path key={y} d={`M106 ${y - 4} Q 120 ${y + 4} 134 ${y - 4} Q 120 ${y + 8} 106 ${y - 4} Z`} fill="#f3ece0" stroke="#16110f" strokeWidth=".6" />
      ))}
      <path d="M40 188 H200" stroke="#e5a823" strokeWidth="1.5" />
      {/* the rooster at the gable tip */}
      <path d="M117 66 q 3 -8 8 -6 q -1 3 -4 4 l 3 4 z" fill="#e5a823" />
    </svg>
  );
}

/** Upswept roof alone — used to crown cards. */
export function Roof({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 200 40" preserveAspectRatio="none" aria-hidden="true" focusable="false">
      <path d="M2 2 Q 50 30 100 30 Q 150 30 198 2 L 192 16 Q 150 40 100 40 Q 50 40 8 16 Z" fill="currentColor" />
      <path d="M6 9 Q 52 35 100 35 Q 148 35 194 9" fill="none" stroke="#e5a823" strokeWidth="1" />
    </svg>
  );
}

/** Pa' tedong — stylised buffalo head used as a marker. */
export function Tedong({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 40 32" aria-hidden="true" focusable="false">
      <path d="M14 12 C 6 12 1 7 2 1 C 6 6 10 8 16 8 Z M26 12 C 34 12 39 7 38 1 C 34 6 30 8 24 8 Z" fill="currentColor" />
      <path d="M13 9 H27 L24 27 Q 20 31 16 27 Z" fill="currentColor" />
      <circle cx="17" cy="15" r="1.6" fill="#16110f" />
      <circle cx="23" cy="15" r="1.6" fill="#16110f" />
    </svg>
  );
}
