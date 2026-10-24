// Rawuh logo: a tiered joglo roof over a glowing doorway — the host welcoming guests ("rawuh" = to arrive).
// Geometry is shared with app/icon.svg and public/brand/*.svg; keep them in sync.

/** Gold of the doorway, the one accent of the mark. */
export const RAWUH_GOLD = "#e0a83b";

/** The joglo mark. `color` paints the house (currentColor by default), `door` the doorway. */
export function RawuhMark({ size = 24, color = "currentColor", door = RAWUH_GOLD, title }: {
  size?: number; color?: string; door?: string; title?: string;
}) {
  const small = size < 24;
  return (
    <svg width={size} height={size} viewBox="0 0 48 48" role={title ? "img" : undefined} aria-label={title} aria-hidden={title ? undefined : true} focusable="false">
      {/* Below 24px the top tier merges into one roof so the shape stays readable. */}
      {small
        ? <path d="M12 14h24l8 11H4z" fill={color} />
        : <><path d="M18 6.5h12l4.5 8H13.5z" fill={color} /><path d="M12 16.5h24l8 9H4z" fill={color} /></>}
      <path d={small ? "M10 27h28v15H10z" : "M10 28h28v14H10z"} fill={color} />
      <path d={small ? "M18.5 42v-7.5a5.5 5.5 0 0 1 11 0V42z" : "M19.5 42v-6.5a4.5 4.5 0 0 1 9 0V42z"} fill={door} />
    </svg>
  );
}

/** The mark on an indigo rounded tile (app icon look): used next to the "rawuh" wordmark in navigation. */
export function RawuhTile({ size = 32 }: { size?: number }) {
  return (
    <span aria-hidden="true" style={{ display: "inline-grid", flex: "none", placeItems: "center", width: size, height: size, borderRadius: Math.round(size * 0.28), background: "var(--rw-primary-fill, var(--rw-primary, #2e43b0))" }}>
      <RawuhMark size={Math.round(size * 0.72)} color="#fff" />
    </span>
  );
}
