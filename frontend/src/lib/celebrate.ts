/**
 * Tiny dependency-free celebration bursts for invitation themes (RSVP sent, wish sent, …).
 * The flavour follows the theme's motion personality (data-motion on the invitation root):
 *   playful — confetti that pops up and tumbles down
 *   elegant — a few soft petals / sparkles drifting down
 *   crisp   — nothing (the check-mark animation is enough)
 * Colours come from the theme's --t-accent. No-op under prefers-reduced-motion.
 */
type Flavour = "playful" | "elegant" | "crisp";

function flavourOf(from: Element | null): Flavour {
  const value = from?.closest("[data-motion]")?.getAttribute("data-motion");
  return value === "playful" || value === "crisp" ? value : "elegant";
}

function accentOf(from: Element | null) {
  const root = from?.closest("[data-motion]") ?? from;
  const accent = root ? getComputedStyle(root).getPropertyValue("--t-accent").trim() : "";
  return accent || "#d4a24c";
}

// One burst per action: ThemeShell celebrates every accepted RSVP / wish, and some themes also celebrate on their own.
let lastBurst = 0;

export function celebrate(from: Element | null, origin?: { x: number; y: number }) {
  if (typeof window === "undefined" || window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
  const now = Date.now();
  if (now - lastBurst < 900) return;
  lastBurst = now;
  const flavour = flavourOf(from);
  if (flavour === "crisp") return;
  navigator.vibrate?.(flavour === "playful" ? [12, 40, 12] : 10);
  const accent = accentOf(from);
  const palette = flavour === "playful"
    ? [accent, "#ffd166", "#ef476f", "#06d6a0", "#118ab2", "#ffffff"]
    : [accent, `color-mix(in srgb, ${accent} 55%, #fff)`, "#fff7e6", `color-mix(in srgb, ${accent} 70%, #000)`];
  const rect = from?.getBoundingClientRect();
  const x = origin?.x ?? (rect ? rect.left + rect.width / 2 : window.innerWidth / 2);
  const y = origin?.y ?? (rect ? rect.top + Math.min(rect.height, 120) / 2 : window.innerHeight / 3);

  const layer = document.createElement("div");
  layer.setAttribute("aria-hidden", "true");
  Object.assign(layer.style, { position: "fixed", inset: "0", pointerEvents: "none", zIndex: "120", overflow: "hidden" });
  document.body.appendChild(layer);

  const count = flavour === "playful" ? 70 : 26;
  let longest = 0;
  for (let i = 0; i < count; i++) {
    const piece = document.createElement("i");
    const color = palette[i % palette.length];
    const size = flavour === "playful" ? 6 + Math.random() * 6 : 5 + Math.random() * 7;
    Object.assign(piece.style, {
      position: "absolute", left: `${x}px`, top: `${y}px`, width: `${size}px`, height: `${flavour === "playful" ? size * 0.45 : size}px`,
      background: color, borderRadius: flavour === "playful" ? "2px" : "60% 0 60% 0", opacity: "0",
      boxShadow: flavour === "elegant" ? `0 0 6px ${color}` : "none",
    });
    layer.appendChild(piece);
    const angle = flavour === "playful" ? -Math.PI / 2 + (Math.random() - 0.5) * Math.PI * 1.1 : Math.random() * Math.PI * 2;
    const power = flavour === "playful" ? 160 + Math.random() * 220 : 40 + Math.random() * 90;
    const dx = Math.cos(angle) * power;
    const dy = Math.sin(angle) * power;
    const fall = flavour === "playful" ? 380 + Math.random() * 260 : 180 + Math.random() * 160;
    const spin = (Math.random() - 0.5) * (flavour === "playful" ? 1440 : 540);
    const duration = flavour === "playful" ? 1300 + Math.random() * 900 : 2200 + Math.random() * 1400;
    longest = Math.max(longest, duration);
    piece.animate([
      { opacity: 1, transform: "translate(-50%, -50%) rotate(0deg) scale(.6)" },
      { opacity: 1, transform: `translate(calc(-50% + ${dx}px), calc(-50% + ${dy}px)) rotate(${spin * 0.5}deg) scale(1)`, offset: flavour === "playful" ? 0.3 : 0.25 },
      { opacity: 0, transform: `translate(calc(-50% + ${dx * 1.3 + (Math.random() - 0.5) * 60}px), calc(-50% + ${dy + fall}px)) rotate(${spin}deg) scale(.9)` },
    ], { duration, easing: "cubic-bezier(.2,.7,.3,1)", fill: "forwards" });
  }
  window.setTimeout(() => layer.remove(), longest + 100);
}

/** Small transient message ("Disalin ✓") shown by ThemeShell's toaster. */
export const TOAST_EVENT = "rawuh:toast";
export function toast(message: string) {
  if (typeof window === "undefined") return;
  window.dispatchEvent(new CustomEvent(TOAST_EVENT, { detail: message }));
}
