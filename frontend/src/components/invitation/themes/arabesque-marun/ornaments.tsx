// Original arabesque ornaments for "Arabesque Marun": scrolling vines with spirals and split palmettes,
// a lobed medallion and a multifoil (cusped) arch frame. Simple hand-drawn geometry, no calligraphy.

/** One half of the corner scroll; mirrored across the corner diagonal to make it symmetric. */
const HALF = (
  <>
    <path pathLength={1} d="M6 94C8 60 26 32 62 14" />
    <path pathLength={1} d="M22 56C10 50 10 34 22 30C32 27 38 38 30 43C26 45 22 42 24 38" />
    <path pathLength={1} d="M44 26C40 14 50 6 58 9C65 12 63 21 57 21" />
    <path pathLength={1} d="M14 76C24 72 30 64 30 54" />
  </>
);
const LEAVES = (
  <>
    <path d="M62 14c4-6 12-8 18-5-5 1-9 4-11 9-2-3-4-4-7-4z" />
    <path d="M30 54c-6-2-8-8-6-13 2 4 5 6 9 6-2 2-3 4-3 7z" />
    <path d="M14 76c-6 0-10-4-10-9 3 3 6 4 10 3-1 2-1 4 0 6z" />
  </>
);

/** Corner arabesque (bottom-left oriented; rotate via CSS for other corners). */
export function Corner({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 100 100" aria-hidden focusable="false">
      <g fill="none" stroke="currentColor" strokeWidth="1.3" strokeLinecap="round">
        {HALF}
        <g transform="matrix(0 -1 -1 0 100 100)">{HALF}</g>
      </g>
      <g fill="currentColor">
        {LEAVES}
        <g transform="matrix(0 -1 -1 0 100 100)">{LEAVES}</g>
        <circle cx="6" cy="94" r="3" />
      </g>
    </svg>
  );
}

/** Lobed medallion: eight palmette lobes around a star, used on the cover and as a monogram ground. */
export function Medallion({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="-50 -50 100 100" aria-hidden focusable="false">
      <g fill="none" stroke="currentColor" strokeWidth="1">
        {Array.from({ length: 8 }, (_, i) => (
          <path key={i} transform={`rotate(${i * 45})`} d="M0-20C6-26 6-36 0-44C-6-36-6-26 0-20ZM0-30C10-30 16-38 14-46M0-30C-10-30-16-38-14-46" />
        ))}
        <circle r="20" />
        <circle r="47" strokeWidth=".6" strokeDasharray="1 3" />
      </g>
      <g fill="currentColor">
        <path d="M0-12 3.5-3.5 12 0 3.5 3.5 0 12-3.5 3.5-12 0-3.5-3.5Z" />
      </g>
    </svg>
  );
}

/** Horizontal divider: two mirrored scrolls meeting at a palmette. */
export function Scroll({ className }: { className?: string }) {
  const side = (
    <>
      <path pathLength={1} d="M58 12C46 12 40 4 30 4S14 12 22 16C28 19 32 12 27 10" />
      <path pathLength={1} d="M58 12C50 18 42 20 34 19" />
      <path pathLength={1} d="M30 4C20 4 8 8 2 12" />
    </>
  );
  return (
    <svg className={className} viewBox="0 0 140 24" aria-hidden focusable="false">
      <g fill="none" stroke="currentColor" strokeWidth="1.1" strokeLinecap="round">
        {side}
        <g transform="matrix(-1 0 0 1 140 0)">{side}</g>
      </g>
      <path d="M70 3c5 4 6 10 0 18-6-8-5-14 0-18z" fill="currentColor" />
      <circle cx="61" cy="12" r="1.6" fill="currentColor" /><circle cx="79" cy="12" r="1.6" fill="currentColor" />
    </svg>
  );
}

/** Multifoil arch (210×280) used to clip portraits, and its outline. */
export const FOIL = "M0 280V106A30 30 0 0 1 30 62A35 35 0 0 1 68 27A40 40 0 0 1 105 0A40 40 0 0 1 142 27A35 35 0 0 1 180 62A30 30 0 0 1 210 106V280Z";

export function FoilOutline({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="-12 -12 234 304" aria-hidden focusable="false">
      <path d={FOIL} fill="none" stroke="currentColor" strokeWidth="1.2" transform="translate(-6 -6) scale(1.057 1.043)" />
      <path d={FOIL} fill="none" stroke="currentColor" strokeWidth=".6" opacity=".7" transform="translate(-11 -11) scale(1.105 1.079)" />
    </svg>
  );
}

/** Faint arabesque damask tile for backgrounds. */
export const DAMASK = `url("data:image/svg+xml,${encodeURIComponent(
  "<svg xmlns='http://www.w3.org/2000/svg' width='80' height='80' viewBox='0 0 80 80'><g fill='none' stroke='#d6b06a' stroke-width='.8' stroke-linecap='round'><path d='M40 8C52 20 52 32 40 40C28 32 28 20 40 8Z'/><path d='M40 72C52 60 52 48 40 40C28 48 28 60 40 72Z'/><path d='M40 40C30 46 18 44 14 36C11 30 18 26 22 30'/><path d='M40 40C50 34 62 36 66 44C69 50 62 54 58 50'/><path d='M0 0C8 4 12 10 10 18M80 80C72 76 68 70 70 62M80 0C72 4 68 10 70 18M0 80C8 76 12 70 10 62'/></g></svg>",
)}")`;
