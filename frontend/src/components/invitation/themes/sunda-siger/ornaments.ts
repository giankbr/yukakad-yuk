// Original ornaments for "Sunda Siger": siger crown, melati (jasmine) blooms & strands, Mega Mendung clouds.
// Drawn for Rawuh — inspired by the motifs, not traced from any artwork.

const GOLD = "<linearGradient id=\"sgGold\" x1=\"0\" x2=\"0\" y1=\"0\" y2=\"1\"><stop offset=\"0\" stop-color=\"#f6e2a4\"/><stop offset=\".5\" stop-color=\"#cfa94f\"/><stop offset=\"1\" stop-color=\"#8d6c22\"/></linearGradient>";

function bloom(x: number, y: number, r: number, fill = "#fffaf0", center = "#e3c56f") {
  let petals = "";
  for (let i = 0; i < 5; i += 1) petals += `<ellipse cx="0" cy="${-r * .62}" rx="${r * .42}" ry="${r * .62}" transform="rotate(${i * 72})"/>`;
  return `<g transform="translate(${x} ${y})" fill="${fill}" stroke="#cdbf95" stroke-width=".6">${petals}<circle r="${r * .26}" fill="${center}" stroke="none"/></g>`;
}

/** Siger — the Sundanese bridal crown, with five kembang goyang pins. viewBox 0 0 200 120. */
export const siger = `<defs>${GOLD}</defs>
<g stroke="#8d6c22" stroke-width="1.1" fill="none">
  <path d="M100 24V6M79 31 70 13M121 31l9-18M58 46 44 30M142 46l14-16"/>
</g>
${bloom(100, 6, 7, "url(#sgGold)", "#1d4a33")}${bloom(70, 13, 6, "url(#sgGold)", "#1d4a33")}${bloom(130, 13, 6, "url(#sgGold)", "#1d4a33")}${bloom(44, 30, 5.4, "url(#sgGold)", "#1d4a33")}${bloom(156, 30, 5.4, "url(#sgGold)", "#1d4a33")}
<path d="M24 101C32 62 63 35 100 22c37 13 68 40 76 79-44-15-108-15-152 0Z" fill="url(#sgGold)" stroke="#8d6c22" stroke-width="1.2"/>
<g fill="none" stroke="#6b5016" stroke-width="1.2" opacity=".85">
  <path d="M40 95c9-28 31-49 60-60 29 11 51 32 60 60"/>
  <path d="M58 91c8-19 23-33 42-41 19 8 34 22 42 41"/>
  <path d="M76 88c6-11 14-19 24-24 10 5 18 13 24 24"/>
</g>
<g fill="#fff6d8" opacity=".9"><circle cx="100" cy="30" r="2"/><circle cx="66" cy="52" r="1.8"/><circle cx="134" cy="52" r="1.8"/><circle cx="48" cy="72" r="1.6"/><circle cx="152" cy="72" r="1.6"/><circle cx="84" cy="42" r="1.6"/><circle cx="116" cy="42" r="1.6"/></g>
<path d="M100 56c7 6 9 13 0 22-9-9-7-16 0-22Z" fill="#1d4a33" stroke="#f6e2a4" stroke-width="1.2"/>
<path d="M20 101c46-16 114-16 160 0l-2 10c-45-14-111-14-156 0Z" fill="url(#sgGold)" stroke="#8d6c22" stroke-width="1.1"/>
<g fill="#1d4a33"><circle cx="40" cy="103" r="1.8"/><circle cx="60" cy="99" r="1.8"/><circle cx="80" cy="97" r="1.8"/><circle cx="100" cy="96.5" r="2.2"/><circle cx="120" cy="97" r="1.8"/><circle cx="140" cy="99" r="1.8"/><circle cx="160" cy="103" r="1.8"/></g>`;

/** Single melati bloom, viewBox -12 -12 24 24. */
export const melati = bloom(0, 0, 11);

/** Roncean melati — a hanging jasmine strand. viewBox 0 0 24 220. */
export const ronce = (() => {
  let parts = "<path d=\"M12 0V214\" stroke=\"#cdbf95\" stroke-width=\"1\"/>";
  for (let y = 14; y < 214; y += 14) {
    parts += (y / 14) % 3 === 0 ? bloom(12, y, 6.5) : `<ellipse cx="12" cy="${y}" rx="3.4" ry="5.6" fill="#fffaf0" stroke="#cdbf95" stroke-width=".6"/>`;
  }
  return parts + bloom(12, 214, 7.5);
})();

/** Mega Mendung cloud: stacked strokes give the banded, layered outline. viewBox 0 0 200 110. */
const CLOUD = "M24 96c-14 0-16-20-2-24-6-17 15-28 28-18 4-24 38-28 48-6 13-19 47-14 46 10 18-8 39 4 32 22 17 1 20 16 4 16Z";
export function megaMendung(colors: [string, string, string, string, string]) {
  const [a, b, c, d, e] = colors;
  return `<g stroke-linejoin="round"><path d="${CLOUD}" fill="${a}" stroke="${a}" stroke-width="22"/><path d="${CLOUD}" fill="none" stroke="${b}" stroke-width="16"/><path d="${CLOUD}" fill="none" stroke="${c}" stroke-width="10"/><path d="${CLOUD}" fill="none" stroke="${d}" stroke-width="5"/><path d="${CLOUD}" fill="none" stroke="${e}" stroke-width="1.4"/></g>`;
}

export const cloudDark = megaMendung(["#123323", "#1b4430", "#24573e", "#2f6b4c", "#d9bd6c"]);
export const cloudLight = megaMendung(["#e7ecdf", "#dbe4d2", "#cddbc4", "#bcd0b3", "#c9a54e"]);

/** Small divider: two leaf strokes and a melati in the middle. viewBox 0 0 160 24. */
export const divider = `<g fill="none" stroke="#c9a54e" stroke-width="1.2" stroke-linecap="round"><path d="M4 12h52M104 12h52"/><path d="M56 12c6-7 12-8 18-4M104 12c-6-7-12-8-18-4M56 12c6 7 12 8 18 4M104 12c-6 7-12 8-18 4"/></g>${bloom(80, 12, 9)}`;
