// Original ornaments for "Masjid Biru": a domed skyline silhouette, hanging lanterns, a crescent and an eight-point star tile.

/** Mosque skyline: central dome flanked by two smaller domes and two minarets, with a few lit windows. */
export function Skyline({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 390 150" preserveAspectRatio="xMidYMax slice" aria-hidden focusable="false">
      <g fill="var(--sil, #060d22)">
        {/* minarets */}
        <path d="M44 150V44h4l6-26 6 26h4v106z" />
        <rect x="38" y="66" width="32" height="5" rx="1" />
        <rect x="41" y="96" width="26" height="4" rx="1" />
        <path d="M326 150V44h4l6-26 6 26h4v106z" />
        <rect x="320" y="66" width="32" height="5" rx="1" />
        <rect x="323" y="96" width="26" height="4" rx="1" />
        {/* side halls + domes */}
        <path d="M84 150v-50h52v50z" />
        <path d="M88 102c0-20 14-26 22-38 8 12 22 18 22 38z" />
        <path d="M254 150v-50h52v50z" />
        <path d="M258 102c0-20 14-26 22-38 8 12 22 18 22 38z" />
        {/* main hall + dome */}
        <path d="M128 150V86h134v64z" />
        <path d="M138 88c0-40 34-52 57-74 23 22 57 34 57 74z" />
        <rect x="193.5" y="2" width="3" height="14" />
        <rect y="140" width="390" height="10" />
      </g>
      <g fill="var(--lit, #e6b95c)" opacity=".85">
        <path d="M186 150v-24a9 9 0 0 1 18 0v24z" />
        <path d="M152 124v-12a5 5 0 0 1 10 0v12zM228 124v-12a5 5 0 0 1 10 0v12z" />
        <path d="M104 132v-12a5 5 0 0 1 10 0v12zM276 132v-12a5 5 0 0 1 10 0v12z" />
        <rect x="52" y="52" width="4" height="8" rx="2" /><rect x="334" y="52" width="4" height="8" rx="2" />
      </g>
      {/* finial crescent */}
      <path d="M199 4.5a5 5 0 1 1-5.4-3.8 4 4 0 1 0 5.4 3.8z" fill="var(--lit, #e6b95c)" />
    </svg>
  );
}

/** A hanging lantern; the outer <span> swings (CSS), the body glows. */
export function Lantern({ className, drop = 60 }: { className?: string; drop?: number }) {
  return (
    <span className={className} aria-hidden>
      <svg viewBox={`0 0 40 ${drop + 74}`} width="40" height={drop + 74} focusable="false">
        <line x1="20" y1="0" x2="20" y2={drop} stroke="currentColor" strokeWidth="1" opacity=".7" />
        <g transform={`translate(0 ${drop})`}>
          <circle cx="20" cy="3" r="3" fill="none" stroke="currentColor" strokeWidth="1.2" />
          <path d="M11 14 20 6l9 8z" fill="currentColor" />
          <path d="M10 15h20l-2 6H12z" fill="currentColor" />
          <path d="M12 21h16l3 18-3 16H12L9 39z" fill="var(--glow, #ffd98a)" opacity=".92" />
          <path d="M12 21h16l3 18-3 16H12L9 39zM20 21v34M9 39h22" fill="none" stroke="currentColor" strokeWidth="1.3" strokeLinejoin="round" />
          <path d="M12 55h16l-3 6H15z" fill="currentColor" />
          <path d="M20 61v8" stroke="currentColor" strokeWidth="1.4" />
          <circle cx="20" cy="71" r="2" fill="currentColor" />
        </g>
      </svg>
    </span>
  );
}

export function Crescent({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 60 60" aria-hidden focusable="false">
      <path d="M40 6a26 26 0 1 0 14 40A22 22 0 1 1 40 6z" fill="currentColor" />
    </svg>
  );
}

/** Small eight-point star (two squares). */
export function Star8({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="-12 -12 24 24" aria-hidden focusable="false">
      <g fill="currentColor"><rect x="-7.5" y="-7.5" width="15" height="15" /><rect x="-7.5" y="-7.5" width="15" height="15" transform="rotate(45)" /></g>
    </svg>
  );
}

/** Interlocking eight-point star tile (zellige-like), used as a faint repeating background. */
export const TILE = `url("data:image/svg+xml,${encodeURIComponent(
  "<svg xmlns='http://www.w3.org/2000/svg' width='60' height='60' viewBox='0 0 60 60'><g fill='none' stroke='#7fd0c8' stroke-width='.8'><path d='M30 12.4 35.1 17.6H42.4V24.9L47.6 30 42.4 35.1V42.4H35.1L30 47.6 24.9 42.4H17.6V35.1L12.4 30 17.6 24.9V17.6H24.9Z'/><circle cx='30' cy='30' r='5'/><path d='M0 0 12.4 12.4M60 0 47.6 12.4M0 60 12.4 47.6M60 60 47.6 47.6M30 0v12.4M30 47.6V60M0 30h12.4M47.6 30H60'/></g></svg>",
)}")`;
