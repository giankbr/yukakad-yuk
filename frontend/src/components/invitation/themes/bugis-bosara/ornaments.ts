// Original ornaments for "Bugis Bosara": the bosara (lidded tray for wedding cakes), walasuji lattice and the
// sulapa eppa (four-sided) diamond. Drawn for Rawuh, inspired by the motifs, not traced from any artwork.

const GOLD = "<linearGradient id=\"bgGold\" x1=\"0\" x2=\"0\" y1=\"0\" y2=\"1\"><stop offset=\"0\" stop-color=\"#f7dc8c\"/><stop offset=\".55\" stop-color=\"#d4a532\"/><stop offset=\"1\" stop-color=\"#9b7414\"/></linearGradient>";

function scallops(x0: number, x1: number, y: number, r: number, fill: string) {
  let out = "";
  for (let x = x0 + r; x <= x1 - r + .1; x += r * 2) out += `<path d="M${x - r} ${y}a${r} ${r} 0 0 0 ${r * 2} 0Z" fill="${fill}"/>`;
  return out;
}

/** Gold gradient shared by the bosara parts. viewBox 0 0 160 170. */
export const bosaraDefs = GOLD;

/** Bosara lid (rendered in its own group so it can float). */
export const bosaraLid = `<path d="M22 104C26 58 50 30 80 20c30 10 54 38 58 84Z" fill="#c2185b" stroke="url(#bgGold)" stroke-width="2.4"/>
<path d="M36 100c4-34 20-56 44-66 24 10 40 32 44 66" fill="none" stroke="url(#bgGold)" stroke-width="1.4" stroke-dasharray="2 4" stroke-linecap="round"/>
<g fill="url(#bgGold)"><path d="M80 44 92 58 80 72 68 58Z"/><path d="M80 52 85 58 80 64 75 58Z" fill="#c2185b"/>
<path d="M54 74 62 83 54 92 46 83Z"/><path d="M106 74l8 9-8 9-8-9Z"/><path d="M80 80l7 8-7 8-7-8Z"/></g>
<g fill="#fff3d6" opacity=".9"><circle cx="64" cy="54" r="1.6"/><circle cx="96" cy="54" r="1.6"/><circle cx="44" cy="96" r="1.4"/><circle cx="116" cy="96" r="1.4"/><circle cx="80" cy="30" r="1.6"/></g>
<rect x="18" y="100" width="124" height="9" rx="2" fill="url(#bgGold)"/>
${scallops(18, 142, 109, 5.17, "url(#bgGold)")}
<circle cx="80" cy="16" r="6" fill="url(#bgGold)"/><circle cx="80" cy="16" r="2.4" fill="#0f7a5c"/>`;

/** Bosara bowl and stand. viewBox 0 0 160 170. */
export const bosaraBase = `
<path d="M26 114c8 22 30 34 54 34s46-12 54-34Z" fill="url(#bgGold)" stroke="#9b7414" stroke-width="1"/>
<path d="M40 122c10 12 24 18 40 18s30-6 40-18" fill="none" stroke="#9b7414" stroke-width="1"/>
<g fill="#0f7a5c"><circle cx="54" cy="128" r="2"/><circle cx="80" cy="134" r="2.4"/><circle cx="106" cy="128" r="2"/></g>
<path d="M60 148h40l8 14H52Z" fill="url(#bgGold)" stroke="#9b7414" stroke-width="1"/>
<rect x="46" y="160" width="68" height="6" rx="2" fill="#9b7414"/>`;

/** Sulapa eppa — the four-sided diamond, as divider jewel. viewBox 0 0 160 24. */
export const divider = `<g stroke="#d4a532" stroke-width="1.2" fill="none"><path d="M4 12h56M100 12h56"/></g>
<path d="M80 1 91 12 80 23 69 12Z" fill="#c2185b" stroke="#d4a532" stroke-width="1.4"/><path d="M80 7 85 12 80 17 75 12Z" fill="#d4a532"/>
<path d="M62 12 66 8 70 12 66 16Z" fill="#0f7a5c"/><path d="M90 12l4-4 4 4-4 4Z" fill="#0f7a5c"/>`;

/** Small sulapa eppa diamond (bullet / node). viewBox 0 0 24 24. */
export const jewel = `<path d="M12 1 23 12 12 23 1 12Z" fill="currentColor"/><path d="M12 6 18 12 12 18 6 12Z" fill="#f7dc8c"/><path d="M12 9.5 14.5 12 12 14.5 9.5 12Z" fill="currentColor"/>`;
