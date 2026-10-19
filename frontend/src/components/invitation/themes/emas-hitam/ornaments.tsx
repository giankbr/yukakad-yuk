// Original art-deco ornaments for "Emas Hitam" (drawn for Rawuh). Strokes use currentColor / the gold gradient.
import { useId } from "react";

function Gold({ id }: { id: string }) {
  return (
    <defs>
      <linearGradient id={id} x1="0" y1="0" x2="1" y2="1">
        <stop offset="0" stopColor="#9c7a3c" />
        <stop offset=".45" stopColor="#f1d999" />
        <stop offset=".7" stopColor="#c9a159" />
        <stop offset="1" stopColor="#8d6a2e" />
      </linearGradient>
    </defs>
  );
}

/** Sunburst fan (viewBox 240×124): stepped arcs + rays radiating from the bottom center. */
export function Fan({ className }: { className?: string }) {
  const id = useId().replace(/:/g, "");
  const rays = Array.from({ length: 13 }, (_, i) => -90 + (i - 6) * 13);
  return (
    <svg className={className} viewBox="0 0 240 124" aria-hidden="true" focusable="false">
      <Gold id={id} />
      <g fill="none" stroke={`url(#${id})`} strokeLinecap="round">
        {[110, 92, 74].map((r, i) => <path key={r} pathLength="1" className="arc" d={`M${120 - r} 120A${r} ${r} 0 0 1 ${120 + r} 120`} strokeWidth={i === 0 ? 1.6 : 1} />)}
        {rays.map((a, i) => {
          const rad = (a * Math.PI) / 180;
          const inner = 30, outer = i % 2 ? 70 : 88;
          return <path key={a} pathLength="1" className="ray" d={`M${(120 + inner * Math.cos(rad)).toFixed(1)} ${(120 + inner * Math.sin(rad)).toFixed(1)}L${(120 + outer * Math.cos(rad)).toFixed(1)} ${(120 + outer * Math.sin(rad)).toFixed(1)}`} strokeWidth="1" />;
        })}
        <path pathLength="1" className="arc" d="M96 120A24 24 0 0 1 144 120" strokeWidth="1.4" />
      </g>
      <path d="M120 98L128 120H112Z" fill={`url(#${id})`} />
      <path d="M4 120H236" stroke={`url(#${id})`} strokeWidth="1.2" />
    </svg>
  );
}

/** Stepped art-deco corner (viewBox 60×60, top-left orientation; rotate via CSS for the others). */
export function Corner({ className }: { className?: string }) {
  const id = useId().replace(/:/g, "");
  return (
    <svg className={className} viewBox="0 0 60 60" aria-hidden="true" focusable="false">
      <Gold id={id} />
      <g fill="none" stroke={`url(#${id})`} strokeWidth="1.2">
        <path d="M2 58V14H14V2H58" />
        <path d="M8 58V20H20V8H58" opacity=".6" />
        <path d="M14 26H26V14" opacity=".8" />
      </g>
      <rect x="23" y="23" width="6" height="6" transform="rotate(45 26 26)" fill={`url(#${id})`} />
    </svg>
  );
}

/** Divider: line, chevrons and a diamond (viewBox 200×16). */
export function Rule({ className }: { className?: string }) {
  const id = useId().replace(/:/g, "");
  return (
    <svg className={className} viewBox="0 0 200 16" aria-hidden="true" focusable="false">
      <Gold id={id} />
      <g stroke={`url(#${id})`} strokeWidth="1" fill="none">
        <path className="line" d="M4 8H78" />
        <path className="line" d="M122 8H196" />
        <path d="M82 3L87 8L82 13M118 3L113 8L118 13" />
      </g>
      <path d="M100 1L107 8L100 15L93 8Z" fill={`url(#${id})`} />
    </svg>
  );
}
