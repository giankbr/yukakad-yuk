// Motion personality per theme. ThemeShell sets `data-motion` on the invitation root and globals.css maps it to
// easing / duration / distance tokens (--m-*), so reveals, presses, sheets and celebrations feel like the theme:
//   elegant — classic & adat themes: slow, soft, blur-in, no overshoot
//   playful — app & social themes: springy overshoot, pop-in, confetti
//   crisp   — document / productivity themes: short, precise, no bounce
export type MotionStyle = "elegant" | "playful" | "crisp";

const ELEGANT = new Set([
  "jawa", "rumah-gadang", "bali-kuning", "syari-zamrud", "lavender-air", "linen-putih", "sketsa-tangan", "malam-rimba",
]);
const CRISP = new Set(["dokumen", "surel", "koran", "repositori", "rapat-video", "peta-rute", "rencana-perjalanan"]);

export function motionOf(themeId?: string): MotionStyle {
  if (!themeId) return "elegant";
  if (ELEGANT.has(themeId)) return "elegant";
  if (CRISP.has(themeId)) return "crisp";
  return "playful";
}
