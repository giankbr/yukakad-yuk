// Original ornaments for "Batak Ulos": Rumah Bolon, gorga spirals (simeol-meol) and ipon-ipon teeth, in the
// three gorga colours — red, white, black. Drawn for Rawuh, inspired by the motifs, not traced from any artwork.

/** Rumah Bolon (Batak Toba house) with saddle roof and a gorga gable. viewBox 0 0 220 160. */
export const rumahBolon = `
<path d="M4 10c44 30 76 42 106 42S172 40 216 10l-22 80c-40 9-128 9-168 0Z" fill="#15100e" stroke="#f4efe6" stroke-width="1.5"/>
<g stroke="#f4efe6" stroke-width=".8" opacity=".35"><path d="M30 34 40 86M52 44l6 46M76 50l3 42M110 52v40M144 50l-3 42M168 44l-6 46M190 34l-10 52"/></g>
<path d="M58 90 110 56l52 34Z" fill="#b3261e" stroke="#f4efe6" stroke-width="1.5"/>
<g fill="none" stroke="#f4efe6" stroke-width="1.6" stroke-linecap="round">
  <path d="M110 86c-12 0-16-8-12-13s11-3 11 2-6 5-6 1"/><path d="M110 86c12 0 16-8 12-13s-11-3-11 2 6 5 6 1"/>
  <path d="M84 86c-4-6 0-12 6-11"/><path d="M136 86c4-6 0-12-6-11"/>
</g>
<circle cx="110" cy="68" r="3" fill="#f4efe6"/>
<rect x="42" y="90" width="136" height="30" fill="#b3261e" stroke="#f4efe6" stroke-width="1.5"/>
<path d="M42 96h136M42 114h136" stroke="#15100e" stroke-width="2"/>
<polyline points="42,105 50,99 58,105 66,99 74,105 82,99 90,105 98,99 106,105 114,99 122,105 130,99 138,105 146,99 154,105 162,99 170,105 178,99" fill="none" stroke="#f4efe6" stroke-width="1.4"/>
<g fill="#f4efe6"><circle cx="50" cy="109" r="1.4"/><circle cx="66" cy="109" r="1.4"/><circle cx="82" cy="109" r="1.4"/><circle cx="98" cy="109" r="1.4"/><circle cx="114" cy="109" r="1.4"/><circle cx="130" cy="109" r="1.4"/><circle cx="146" cy="109" r="1.4"/><circle cx="162" cy="109" r="1.4"/></g>
<g stroke="#f4efe6" stroke-width="3" stroke-linecap="round"><path d="M52 120v34M84 120v34M136 120v34M168 120v34"/></g>
<path d="M98 120l-6 34M122 120l6 34M95 132h30M93 144h34" stroke="#f4efe6" stroke-width="1.6" fill="none"/>
<path d="M0 154h220" stroke="#f4efe6" stroke-width="1.5" opacity=".6"/>`;

/** A single gorga spiral pair, used as timeline node / bullets. viewBox 0 0 40 40. */
export const spiral = `<g fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round">
<path d="M4 20c0-9 8-14 15-11s7 11 1 12-6-6-2-6"/><path d="M36 20c0 9-8 14-15 11s-7-11-1-12 6 6 2 6"/></g>`;

/** Diamond (lozenge) gorga frame with ipon-ipon teeth, for monograms. viewBox 0 0 200 200. */
export const lozenge = `
<path d="M100 4 196 100 100 196 4 100Z" fill="#15100e" stroke="#b3261e" stroke-width="3"/>
<path d="M100 20 180 100 100 180 20 100Z" fill="none" stroke="#f4efe6" stroke-width="1.2"/>
<g fill="#b3261e">
  <path d="M100 20 108 28 100 36 92 28Z"/><path d="M100 180 108 172 100 164 92 172Z"/><path d="M20 100 28 92 36 100 28 108Z"/><path d="M180 100 172 92 164 100 172 108Z"/>
</g>
<g fill="none" stroke="#f4efe6" stroke-width="1.6" stroke-linecap="round" opacity=".9">
  <path d="M60 60c-8-8-2-18 6-14s2 12-3 8"/><path d="M140 60c8-8 2-18-6-14s-2 12 3 8"/>
  <path d="M60 140c-8 8-2 18 6 14s2-12-3-8"/><path d="M140 140c8 8 2 18-6 14s-2-12 3-8"/>
</g>`;
