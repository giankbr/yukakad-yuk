// Original ornaments for "Dayak Borneo": a perched burung enggang (hornbill) with a curling casque and banded tail,
// a mirrored sulur (vine scroll) that draws itself, and a talawang-shield monogram. Drawn for Rawuh.
import s from "./styles.module.css";

/** Burung enggang, perched, facing right. */
export function Enggang({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 240 150" aria-hidden="true" focusable="false">
      <g className={s.bird}>
        {/* tail feathers with white-black bands */}
        <g className={s.tail}>
          <path d="M78 98 C 54 104 28 114 4 132 C 30 126 56 116 80 108 Z" fill="#f4efe3" stroke="#0c1412" strokeWidth="1" />
          <path d="M76 104 C 54 114 34 126 16 144 C 40 134 60 122 82 110 Z" fill="#f4efe3" stroke="#0c1412" strokeWidth="1" />
          <path d="M60 106 L 50 112 M44 112 L 34 119 M28 118 L 20 124 M58 117 L 50 124 M44 125 L 36 132" stroke="#0c1412" strokeWidth="3" />
        </g>
        {/* body */}
        <path d="M70 94 C 80 70 122 62 150 72 C 164 77 170 88 162 100 C 150 114 108 120 84 112 C 72 108 66 102 70 94 Z" fill="#0c1412" stroke="#f4efe3" strokeWidth="1.6" />
        {/* wing with sulur carving */}
        <path d="M86 94 C 102 78 132 72 154 80 C 140 94 114 104 86 104 Z" fill="#173a32" stroke="#f0b429" strokeWidth="1.2" />
        <path d="M100 96 C 104 88 114 86 118 92 C 120 96 114 98 112 94 M124 90 C 128 82 138 82 140 88 C 141 92 136 93 135 90" fill="none" stroke="#f0b429" strokeWidth="1.2" strokeLinecap="round" />
        {/* neck & head */}
        <path d="M146 74 C 152 60 168 52 180 58 C 188 62 189 74 182 80 C 174 86 162 86 156 84 Z" fill="#0c1412" stroke="#f4efe3" strokeWidth="1.6" />
        {/* beak and upturned casque */}
        <path d="M181 63 C 200 60 222 70 234 92 C 218 82 200 77 183 77 Z" fill="#f0b429" stroke="#0c1412" strokeWidth="1" />
        <path d="M176 58 C 184 42 210 40 226 54 C 228 60 222 62 218 56 C 208 50 194 52 184 64 Z" fill="#c8322a" stroke="#0c1412" strokeWidth="1" />
        <path d="M218 56 C 222 50 228 50 230 54" fill="none" stroke="#c8322a" strokeWidth="2.4" strokeLinecap="round" />
        <circle cx="174" cy="66" r="3.2" fill="#f4efe3" />
        <circle cx="174.6" cy="66" r="1.6" fill="#0c1412" />
        {/* feet on a branch */}
        <path d="M118 114 v10 M132 112 v12" stroke="#f0b429" strokeWidth="2.4" strokeLinecap="round" />
      </g>
      <path d="M40 126 C 90 122 160 122 214 128" fill="none" stroke="#f4efe3" strokeWidth="2.4" strokeLinecap="round" />
      <path d="M186 127 C 196 120 204 120 210 114 M70 124 C 62 118 58 112 60 106" fill="none" stroke="#f4efe3" strokeWidth="1.4" strokeLinecap="round" />
    </svg>
  );
}

/** Sulur — mirrored vine scroll with spiral hooks, used as a section divider. */
export function Sulur({ className }: { className?: string }) {
  const half = "M8 20 C 20 20 24 7 36 7 C 48 7 52 21 44 25 C 38 28 33 22 37 19 M14 21 C 25 23 29 34 41 34 C 51 34 55 27 51 23 M44 25 C 56 31 64 23 70 13 C 66 12 63 15 62 19";
  return (
    <svg className={className} viewBox="0 0 150 40" aria-hidden="true" focusable="false">
      <g fill="none" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round">
        <path className={s.draw} d={half} transform="translate(75 0)" />
        <path className={s.draw} d={half} transform="translate(75 0) scale(-1 1)" />
      </g>
      <path d="M75 12 L82 20 L75 28 L68 20 Z" fill="currentColor" />
      <circle cx="75" cy="20" r="2" fill="#c8322a" />
    </svg>
  );
}

/** Talawang shield face with a monogram, used when there is no photo. */
export function Talawang({ className, initial }: { className?: string; initial: string }) {
  return (
    <svg className={className} viewBox="0 0 120 200" aria-hidden="true" focusable="false">
      <path d="M60 4 L116 30 V170 L60 196 L4 170 V30 Z" fill="#10221e" stroke="#f0b429" strokeWidth="2" />
      <path d="M60 16 L106 37 V163 L60 184 L14 163 V37 Z" fill="none" stroke="#f4efe3" strokeWidth="1" strokeDasharray="3 4" />
      {[-1, 1].map(dir => (
        <g key={dir} transform={`translate(60 100) scale(${dir} 1)`} fill="none" stroke="#c8322a" strokeWidth="2" strokeLinecap="round">
          <path d="M6 -44 C 30 -44 36 -66 24 -72 C 16 -76 12 -66 18 -64" />
          <path d="M6 44 C 30 44 36 66 24 72 C 16 76 12 66 18 64" />
        </g>
      ))}
      <text x="60" y="114" textAnchor="middle" fill="#f4efe3" fontFamily="'DM Serif Display', serif" fontSize="44">{initial}</text>
    </svg>
  );
}
