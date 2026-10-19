// Original ornaments for "Betawi Ondel": ondel-ondel pair, kembang kelapa, and the gigi balang fascia.
// Drawn for Rawuh, inspired by the motifs, not traced from any artwork.

const PAPER = ["#d1262f", "#f4c430", "#157a4b", "#f07aa0", "#ffffff", "#ef7d22"];

/** Kembang kelapa — bamboo sticks with paper strips fanned out like a coconut flower. Centre at (cx, cy). */
function kembang(cx: number, cy: number, radius: number, count: number, spread = 150, start = -165) {
  let out = "";
  for (let i = 0; i < count; i += 1) {
    const angle = ((start + (spread * i) / (count - 1)) * Math.PI) / 180;
    const x = cx + Math.cos(angle) * radius;
    const y = cy + Math.sin(angle) * radius;
    const color = PAPER[i % PAPER.length];
    out += `<path d="M${cx} ${cy}L${x.toFixed(1)} ${y.toFixed(1)}" stroke="#8a6a3c" stroke-width="1"/>`;
    out += `<path d="M${x.toFixed(1)} ${y.toFixed(1)}l-3 7h6Z" fill="${color}" transform="rotate(${((angle * 180) / Math.PI + 90).toFixed(0)} ${x.toFixed(1)} ${y.toFixed(1)})"/>`;
    out += `<circle cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" r="2.6" fill="${color}" stroke="#fff" stroke-width=".6"/>`;
  }
  return out;
}

/** One ondel-ondel. `male` = red face with moustache, `female` = white face. viewBox 0 0 120 250. */
function ondel(male: boolean) {
  const face = male ? "#c8202b" : "#fbf4ea";
  const faceLine = male ? "#8d1219" : "#d8c9b5";
  const body = male ? "#1f2a2e" : "#c8202b";
  const trim = male ? "#f4c430" : "#f4c430";
  const sash = male ? "#d1262f" : "#157a4b";
  const motif = male ? "#f4c430" : "#fbf4ea";
  return `
<g class="kembang">${kembang(60, 54, 44, 13)}</g>
<path d="M30 64c0-20 14-30 30-30s30 10 30 30Z" fill="#1a1412"/>
<rect x="30" y="52" width="60" height="9" rx="3" fill="${trim}"/>
<g fill="#d1262f"><circle cx="40" cy="56.5" r="2"/><circle cx="60" cy="56.5" r="2.4"/><circle cx="80" cy="56.5" r="2"/></g>
<ellipse cx="60" cy="88" rx="27" ry="31" fill="${face}" stroke="${faceLine}" stroke-width="1.4"/>
<path d="M30 70c-6 10-6 30 0 44M90 70c6 10 6 30 0 44" stroke="#1a1412" stroke-width="7" stroke-linecap="round" fill="none"/>
${male
    ? `<g><ellipse cx="49" cy="82" rx="7" ry="6" fill="#fff"/><ellipse cx="71" cy="82" rx="7" ry="6" fill="#fff"/><circle cx="50" cy="82" r="3.2" fill="#1a1412"/><circle cx="70" cy="82" r="3.2" fill="#1a1412"/>
<path d="M40 72q9-6 17 0M63 72q8-6 17 0" stroke="#1a1412" stroke-width="3" fill="none" stroke-linecap="round"/>
<path d="M60 90v8" stroke="${faceLine}" stroke-width="2"/>
<path d="M44 104c6-6 12-2 16-2s10-4 16 2c-4 0-6 3-16 3s-12-3-16-3Z" fill="#1a1412"/>
<path d="M52 110q8 5 16 0" stroke="#fff" stroke-width="2" fill="none"/></g>`
    : `<g><path d="M43 82q6-5 12 0M65 82q6-5 12 0" stroke="#1a1412" stroke-width="2.4" fill="none" stroke-linecap="round"/>
<path d="M42 74q7-4 14-1M64 73q7-3 14 1" stroke="#1a1412" stroke-width="1.6" fill="none" stroke-linecap="round"/>
<path d="M60 88v8" stroke="${faceLine}" stroke-width="1.6"/>
<circle cx="44" cy="98" r="5" fill="#f07aa0" opacity=".5"/><circle cx="76" cy="98" r="5" fill="#f07aa0" opacity=".5"/>
<path d="M51 105q9 7 18 0q-9 3-18 0Z" fill="#c8202b"/><circle cx="60" cy="68" r="2.4" fill="#c8202b"/></g>`}
<path d="M32 118c-14 10-22 40-24 128h104c-2-88-10-118-24-128-8 6-18 9-28 9s-20-3-28-9Z" fill="${body}"/>
<path d="M8 236h104v10H8Z" fill="${trim}"/>
<g fill="${motif}" opacity=".85"><path d="M30 170l6-8 6 8-6 8Z"/><path d="M54 186l6-8 6 8-6 8Z"/><path d="M78 170l6-8 6 8-6 8Z"/><path d="M30 210l6-8 6 8-6 8Z"/><path d="M78 210l6-8 6 8-6 8Z"/><path d="M54 222l6-8 6 8-6 8Z"/></g>
<path d="M32 120c10 22 30 34 56 36l4 10c-30-2-54-16-66-40Z" fill="${sash}"/>
<path d="M36 120c8 6 16 9 24 9s16-3 24-9l3 8c-9 6-18 9-27 9s-18-3-27-9Z" fill="${trim}"/>`;
}

export const ondelMale = ondel(true);
export const ondelFemale = ondel(false);

/** Free-standing kembang kelapa in a pot (cover centrepiece). viewBox 0 0 120 130. */
export const kembangPot = `<path d="M60 128V48" stroke="#8a6a3c" stroke-width="2"/><g class="kembang">${kembang(60, 50, 46, 17, 300, -240)}</g>
<path d="M44 106h32l-4 22H48Z" fill="#157a4b"/><rect x="40" y="102" width="40" height="7" rx="2" fill="#f4c430"/>`;

/** Small rosette (kembang) bullet. viewBox 0 0 24 24. */
export const rosette = `<g>${kembang(12, 12, 9, 8, 315, -90)}</g><circle cx="12" cy="12" r="3" fill="#f4c430" stroke="#d1262f" stroke-width="1"/>`;

/** Full ring of kembang kelapa sticks, framing a portrait medallion. viewBox 0 0 120 120. */
export const burst = `<g class="kembang">${kembang(60, 60, 56, 24, 345, -90)}</g>`;
