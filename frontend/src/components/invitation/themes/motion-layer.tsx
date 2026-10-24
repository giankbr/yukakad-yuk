"use client";
// Shared motion + micro-interaction layer for every invitation theme, mounted by <ThemeShell>:
//   <Toaster>        transient "Disalin ✓" style messages (see toast() in lib/celebrate)
//   <ScrollProgress> thin accent bar showing how far the guest has read
//   <Lightbox>       tap any photo in the invitation to view the photo set full screen (swipe / arrows / Esc)
//   enhanceCover / enhanceMain: Ken Burns on the cover photo, a breathing open button, opening-photo parallax.
import { useCallback, useEffect, useRef, useState, type CSSProperties } from "react";
import { createPortal } from "react-dom";
import { TOAST_EVENT } from "@/lib/celebrate";
import m from "./motion-layer.module.css";
import type { AmbientKind, CoverExit } from "./mood";

const reduced = () => typeof window !== "undefined" && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

/* ── Toast ──────────────────────────────────────────────────────── */

export function Toaster() {
  const [message, setMessage] = useState<{ text: string; id: number } | null>(null);
  useEffect(() => {
    let timer: number | undefined;
    const onToast = (event: Event) => {
      const text = String((event as CustomEvent).detail ?? "");
      if (!text) return;
      setMessage({ text, id: Date.now() });
      window.clearTimeout(timer);
      timer = window.setTimeout(() => setMessage(null), 1900);
    };
    window.addEventListener(TOAST_EVENT, onToast);
    return () => { window.removeEventListener(TOAST_EVENT, onToast); window.clearTimeout(timer); };
  }, []);
  return (
    <div className={m.toastSlot} role="status" aria-live="polite">
      {message && (
        <span key={message.id} className={m.toast}>
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true"><path d="M20 6 9 17l-5-5" /></svg>
          {message.text}
        </span>
      )}
    </div>
  );
}

/* ── Reading progress ───────────────────────────────────────────── */

export function ScrollProgress({ width }: { width: number }) {
  const bar = useRef<HTMLDivElement>(null);
  useEffect(() => {
    let frame = 0;
    const update = () => {
      frame = 0;
      const max = document.documentElement.scrollHeight - window.innerHeight;
      const progress = max > 0 ? Math.min(1, Math.max(0, window.scrollY / max)) : 0;
      if (bar.current) {
        bar.current.style.transform = `scaleX(${progress})`;
        bar.current.style.opacity = progress > 0.01 ? "1" : "0";
      }
    };
    const onScroll = () => { if (!frame) frame = requestAnimationFrame(update); };
    update();
    window.addEventListener("scroll", onScroll, { passive: true });
    window.addEventListener("resize", onScroll);
    return () => { window.removeEventListener("scroll", onScroll); window.removeEventListener("resize", onScroll); cancelAnimationFrame(frame); };
  }, []);
  return <div className={m.progress} style={{ maxWidth: width } as CSSProperties} aria-hidden><div ref={bar} className={m.progressBar} /></div>;
}

/* ── Lightbox ───────────────────────────────────────────────────── */

const SKIP = "a, button, [role='button'], label, summary, [data-nolightbox], [role='dialog']";

function zoomable(img: HTMLImageElement) {
  if (img.closest(SKIP)) return false;
  const rect = img.getBoundingClientRect();
  return rect.width >= 72 && rect.height >= 72 && Boolean(img.currentSrc || img.src);
}

/** The photo set an image belongs to: the nearest ancestor (≤5 levels) holding 2+ zoomable photos, else itself. */
function groupOf(img: HTMLImageElement, root: HTMLElement) {
  let node: HTMLElement | null = img.parentElement;
  for (let depth = 0; node && node !== root && depth < 5; depth++, node = node.parentElement) {
    const imgs = Array.from(node.querySelectorAll("img")).filter(zoomable);
    if (imgs.length >= 2) return imgs;
  }
  return [img];
}

type Shot = { src: string; alt: string };

export function useLightbox(rootRef: React.RefObject<HTMLElement | null>, enabled: boolean) {
  const [state, setState] = useState<{ shots: Shot[]; index: number; from?: DOMRect } | null>(null);
  useEffect(() => {
    const root = rootRef.current;
    if (!root || !enabled) return;
    const onClick = (event: MouseEvent) => {
      const target = event.target as HTMLElement | null;
      const img = target?.closest("img");
      if (!(img instanceof HTMLImageElement) || !root.contains(img) || !zoomable(img)) return;
      const group = groupOf(img, root);
      setState({
        shots: group.map(item => ({ src: item.currentSrc || item.src, alt: item.alt })),
        index: Math.max(0, group.indexOf(img)),
        from: img.getBoundingClientRect(),
      });
    };
    const onOver = (event: MouseEvent) => {
      const img = (event.target as HTMLElement | null)?.closest("img");
      if (img instanceof HTMLImageElement && !img.style.cursor && zoomable(img)) img.style.cursor = "zoom-in";
    };
    root.addEventListener("click", onClick);
    root.addEventListener("mouseover", onOver);
    return () => { root.removeEventListener("click", onClick); root.removeEventListener("mouseover", onOver); };
  }, [rootRef, enabled]);
  const close = useCallback(() => setState(null), []);
  return { state, close, setIndex: (index: number) => setState(current => (current ? { ...current, index, from: undefined } : current)) };
}

export function Lightbox({ shots, index, from, onClose, onIndex }: { shots: Shot[]; index: number; from?: DOMRect; onClose: () => void; onIndex: (index: number) => void }) {
  const image = useRef<HTMLImageElement>(null);
  const drag = useRef<{ x: number; y: number; dx: number; dy: number } | null>(null);
  const [leaving, setLeaving] = useState(false);
  const count = shots.length;
  const go = useCallback((step: number) => { if (count > 1) onIndex((index + step + count) % count); }, [count, index, onIndex]);
  const close = useCallback(() => {
    if (reduced()) { onClose(); return; }
    setLeaving(true);
  }, [onClose]);

  useEffect(() => {
    const onKey = (event: KeyboardEvent) => {
      if (event.key === "Escape") close();
      if (event.key === "ArrowRight") go(1);
      if (event.key === "ArrowLeft") go(-1);
    };
    window.addEventListener("keydown", onKey);
    const previous = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    return () => { window.removeEventListener("keydown", onKey); document.body.style.overflow = previous; };
  }, [close, go]);

  // Open: grow the photo out of the thumbnail that was tapped (FLIP).
  useEffect(() => {
    const element = image.current;
    if (!element || !from || reduced()) return;
    const run = () => {
      const to = element.getBoundingClientRect();
      if (!to.width || !to.height) return;
      const scale = Math.max(from.width / to.width, from.height / to.height);
      const dx = from.left + from.width / 2 - (to.left + to.width / 2);
      const dy = from.top + from.height / 2 - (to.top + to.height / 2);
      element.animate([
        { transform: `translate(${dx}px, ${dy}px) scale(${scale})`, opacity: 0.6, borderRadius: "16px" },
        { transform: "none", opacity: 1, borderRadius: "4px" },
      ], { duration: 420, easing: "cubic-bezier(.2,.8,.2,1)" });
    };
    if (element.complete) run(); else element.addEventListener("load", run, { once: true });
  }, [from]);

  const shot = shots[index];
  if (!shot) return null;
  return createPortal(
    <div className={`${m.lightbox} ${leaving ? m.lightboxLeave : ""}`} role="dialog" aria-modal="true" aria-label="Foto"
      onAnimationEnd={event => { if (leaving && event.target === event.currentTarget) onClose(); }}
      onClick={event => { if (event.target === event.currentTarget) close(); }}
      onPointerDown={event => { drag.current = { x: event.clientX, y: event.clientY, dx: 0, dy: 0 }; }}
      onPointerMove={event => {
        const d = drag.current;
        if (!d || !image.current) return;
        d.dx = event.clientX - d.x; d.dy = event.clientY - d.y;
        image.current.style.translate = Math.abs(d.dy) > Math.abs(d.dx) ? `0 ${Math.max(0, d.dy)}px` : `${d.dx}px 0`;
      }}
      onPointerUp={() => {
        const d = drag.current;
        drag.current = null;
        if (image.current) image.current.style.translate = "";
        if (!d) return;
        if (d.dy > 110 && Math.abs(d.dy) > Math.abs(d.dx)) close();
        else if (d.dx < -60) go(1);
        else if (d.dx > 60) go(-1);
      }}
      onPointerCancel={() => { drag.current = null; if (image.current) image.current.style.translate = ""; }}>
      {/* eslint-disable-next-line @next/next/no-img-element -- user-supplied invitation photos */}
      <img key={shot.src} ref={image} src={shot.src} alt={shot.alt} className={m.lightboxImg} draggable={false} />
      <button type="button" className={m.lbClose} onClick={close} aria-label="Tutup foto">×</button>
      {count > 1 && (
        <>
          <button type="button" className={`${m.lbNav} ${m.lbPrev}`} onClick={() => go(-1)} aria-label="Foto sebelumnya">‹</button>
          <button type="button" className={`${m.lbNav} ${m.lbNext}`} onClick={() => go(1)} aria-label="Foto berikutnya">›</button>
          <div className={m.lbDots} aria-label={`Foto ${index + 1} dari ${count}`}>
            {shots.map((item, i) => <i key={item.src + i} data-on={i === index || undefined} />)}
          </div>
        </>
      )}
    </div>,
    document.body,
  );
}

/* ── Automatic flourishes ───────────────────────────────────────── */

function clipped(element: HTMLElement, levels = 4) {
  let node: HTMLElement | null = element.parentElement;
  for (let i = 0; node && i < levels; i++, node = node.parentElement) {
    const style = getComputedStyle(node);
    if (/(hidden|clip)/.test(style.overflow + style.overflowX + style.overflowY)) return true;
  }
  return false;
}

const CTA_TEXT = /buka|open|lihat|masuk|mulai|putar|play|tonton|undangan|terima|lanjut|cek|baca|naik|berangkat|check/i;

/** Cover: Ken Burns on the large photo and a breathing open button. Returns a cleanup. */
export function enhanceCover(cover: HTMLElement | null) {
  if (!cover || reduced()) return () => undefined;
  const area = window.innerWidth * window.innerHeight;
  for (const img of Array.from(cover.querySelectorAll("img"))) {
    const rect = img.getBoundingClientRect();
    if (rect.width * rect.height > area * 0.3 && !img.hasAttribute("data-reveal") && clipped(img) && getComputedStyle(img).animationName === "none") {
      img.setAttribute("data-kenburns", "");
    }
  }
  const buttons = Array.from(cover.querySelectorAll<HTMLButtonElement>("button")).filter(button => button.offsetParent !== null);
  const cta = buttons.find(button => CTA_TEXT.test(button.textContent ?? "")) ?? buttons[buttons.length - 1];
  const timer = window.setTimeout(() => {
    if (!cta || getComputedStyle(cta).animationName !== "none" && !cta.hasAttribute("data-reveal")) return;
    cta.removeAttribute("data-reveal");
    cta.removeAttribute("data-revealed");
    cta.setAttribute("data-cta", "");
  }, 1700);
  return () => window.clearTimeout(timer);
}

/** Main page: slow parallax on the opening photo. Returns a cleanup. */
export function enhanceMain(main: HTMLElement | null) {
  if (!main || reduced()) return () => undefined;
  const column = main.getBoundingClientRect().width;
  const img = Array.from(main.querySelectorAll("img")).find(item => {
    const rect = item.getBoundingClientRect();
    return rect.top + window.scrollY < window.innerHeight * 1.1 && rect.width >= column * 0.8 && rect.height >= 200;
  });
  if (!img || img.closest("[data-reveal]") === img || img.hasAttribute("data-reveal") || !clipped(img) || getComputedStyle(img).animationName !== "none") return () => undefined;
  img.setAttribute("data-parallax", "");
  let frame = 0;
  const update = () => {
    frame = 0;
    const rect = img.getBoundingClientRect();
    if (rect.bottom < 0 || rect.top > window.innerHeight) return;
    const shift = Math.min(rect.height * 0.055, Math.max(0, window.scrollY * 0.12));
    img.style.setProperty("--py", `${shift.toFixed(1)}px`);
  };
  const onScroll = () => { if (!frame) frame = requestAnimationFrame(update); };
  window.addEventListener("scroll", onScroll, { passive: true });
  update();
  return () => { window.removeEventListener("scroll", onScroll); cancelAnimationFrame(frame); img.removeAttribute("data-parallax"); };
}

/* ── Cover exit ─────────────────────────────────────────────────── */

const SPLIT_CLOSED = "polygon(0% 0%, 50% 0%, 50% 100%, 50% 100%, 50% 0%, 100% 0%, 100% 100%, 0% 100%)";
const SPLIT_OPEN = "polygon(0% 0%, 0% 0%, 0% 100%, 100% 100%, 100% 0%, 100% 0%, 100% 100%, 0% 100%)";

/**
 * Plays the cover's leave transition and resolves with how long to keep the cover mounted (ms).
 * `lift` is the CSS class fallback (kit.coverLeave); the others animate the cover and/or reveal the main page.
 */
export function leaveCover(exit: CoverExit, cover: HTMLElement | null, main: HTMLElement | null): number {
  if (reduced()) return 0;
  if (!cover || exit === "lift") return 650;
  const ease = "cubic-bezier(.65, 0, .35, 1)";
  if (exit === "doors") {
    // Two halves part from the middle, like gebyok / palace doors.
    cover.animate([{ clipPath: SPLIT_CLOSED }, { clipPath: SPLIT_OPEN }], { duration: 1000, easing: ease, fill: "forwards" });
    cover.animate([{ opacity: 1 }, { opacity: 1, offset: 0.7 }, { opacity: 0 }], { duration: 1000, fill: "forwards" });
    return 1000;
  }
  if (exit === "iris") {
    // The page opens from the centre in a widening circle while the cover dissolves.
    main?.animate([{ clipPath: "circle(0% at 50% 50vh)" }, { clipPath: "circle(150vmax at 50% 50vh)" }], { duration: 1100, easing: "cubic-bezier(.5, 0, .2, 1)" });
    cover.animate([{ opacity: 1, filter: "blur(0px)" }, { opacity: 0, filter: "blur(6px)" }], { duration: 700, delay: 120, easing: "ease-out", fill: "forwards" });
    return 900;
  }
  if (exit === "rise") {
    // A curtain pulled up.
    cover.animate([{ translate: "0 0" }, { translate: "0 -100%" }], { duration: 900, easing: ease, fill: "forwards" });
    return 900;
  }
  // pop: a quick spring zoom-out, paired with confetti from the button.
  cover.animate([{ opacity: 1, scale: 1 }, { opacity: 0, scale: 1.12 }], { duration: 480, easing: "cubic-bezier(.34, 1.56, .64, 1)", fill: "forwards" });
  return 480;
}

/* ── Ambient particles ──────────────────────────────────────────── */

type Particle = { x: number; y: number; vx: number; vy: number; size: number; spin: number; angle: number; phase: number; hue: number; life: number };

const AMBIENT_COUNT: Record<Exclude<AmbientKind, "none">, number> = { petals: 14, gold: 26, glow: 10, leaves: 10, confetti: 18, sparkle: 14 };

function spawn(kind: Exclude<AmbientKind, "none">, w: number, h: number, initial: boolean): Particle {
  const rising = kind === "glow" || kind === "gold";
  const falling = kind === "petals" || kind === "leaves" || kind === "confetti";
  const y = initial ? Math.random() * h : falling ? -20 : rising ? h + 20 : Math.random() * h;
  const sizes = { petals: [7, 12], gold: [1.2, 2.6], glow: [10, 22], leaves: [8, 13], confetti: [4, 7], sparkle: [4, 8] }[kind];
  return {
    x: Math.random() * w, y,
    vx: (Math.random() - 0.5) * 0.25,
    vy: falling ? 0.35 + Math.random() * 0.45 : rising ? -(0.12 + Math.random() * 0.3) : 0,
    size: sizes[0] + Math.random() * (sizes[1] - sizes[0]),
    spin: (Math.random() - 0.5) * 0.03, angle: Math.random() * Math.PI * 2,
    phase: Math.random() * Math.PI * 2, hue: Math.random(), life: kind === "sparkle" ? Math.random() * 1 : 1,
  };
}

/**
 * A few slow particles drifting over the invitation (petals, gold dust, glowing lights, leaves, confetti, sparkles),
 * tinted by the theme's --t-accent. Off under prefers-reduced-motion, in easy-read mode and while the tab is hidden.
 */
export function Ambient({ kind, width }: { kind: AmbientKind; width: number }) {
  const canvas = useRef<HTMLCanvasElement>(null);
  useEffect(() => {
    const element = canvas.current;
    if (kind === "none" || !element || reduced()) return;
    const ctx = element.getContext("2d");
    if (!ctx) return;
    const root = element.closest("[data-motion]") ?? document.documentElement;
    const accent = getComputedStyle(root).getPropertyValue("--t-accent").trim() || "#d4a24c";
    const palette = kind === "confetti"
      ? [accent, "#ffd166", "#ef476f", "#06d6a0", "#118ab2"]
      : kind === "leaves" ? [accent, "#7a9a5b", "#a3b56b", "#c58b4e"]
      : kind === "petals" ? [accent, "#f4b6c2", "#f9d5dc", "#ffffff"]
      : kind === "glow" ? [accent, "#fff3c4"]
      : [accent, "#f6d87a", "#ffffff"];
    const dpr = Math.min(2, window.devicePixelRatio || 1);
    let w = 0, h = 0;
    const resize = () => {
      w = element.clientWidth; h = element.clientHeight;
      element.width = Math.round(w * dpr); element.height = Math.round(h * dpr);
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    };
    resize();
    const count = AMBIENT_COUNT[kind];
    const particles = Array.from({ length: count }, () => spawn(kind, w, h, true));
    let frame = 0, last = performance.now(), running = true;
    const draw = (now: number) => {
      frame = requestAnimationFrame(draw);
      const dt = Math.min(48, now - last) / 16.7;
      last = now;
      ctx.clearRect(0, 0, w, h);
      if (document.documentElement.dataset.easyRead === "1") return;
      for (let i = 0; i < particles.length; i++) {
        const p = particles[i];
        p.phase += 0.012 * dt;
        p.angle += p.spin * dt;
        p.x += (p.vx + Math.sin(p.phase) * (kind === "petals" || kind === "leaves" ? 0.35 : 0.12)) * dt;
        p.y += p.vy * dt;
        if (kind === "sparkle") p.life -= 0.004 * dt;
        const out = p.y > h + 30 || p.y < -30 || p.x < -30 || p.x > w + 30 || p.life <= 0;
        if (out) { particles[i] = spawn(kind, w, h, false); continue; }
        // Fade in/out near the top and bottom so particles never pop.
        const edge = Math.min(1, Math.min(p.y + 30, h + 30 - p.y) / 120);
        const color = palette[Math.floor(p.hue * palette.length) % palette.length];
        ctx.save();
        ctx.translate(p.x, p.y);
        ctx.rotate(p.angle);
        ctx.fillStyle = color;
        if (kind === "petals") {
          ctx.globalAlpha = 0.55 * edge;
          ctx.beginPath();
          ctx.ellipse(0, 0, p.size * 0.55, p.size * Math.abs(Math.cos(p.phase * 1.6)) * 0.32 + p.size * 0.12, 0, 0, Math.PI * 2);
          ctx.fill();
        } else if (kind === "leaves") {
          ctx.globalAlpha = 0.5 * edge;
          const s = p.size;
          ctx.beginPath();
          ctx.moveTo(-s / 2, 0);
          ctx.quadraticCurveTo(0, -s * 0.42, s / 2, 0);
          ctx.quadraticCurveTo(0, s * 0.42, -s / 2, 0);
          ctx.fill();
        } else if (kind === "confetti") {
          ctx.globalAlpha = 0.6 * edge;
          ctx.scale(1, Math.cos(p.phase * 2.2));
          ctx.fillRect(-p.size / 2, -p.size * 0.22, p.size, p.size * 0.44);
        } else if (kind === "glow") {
          const twinkle = 0.55 + Math.sin(p.phase * 1.7) * 0.25;
          const gradient = ctx.createRadialGradient(0, 0, 0, 0, 0, p.size);
          gradient.addColorStop(0, color);
          gradient.addColorStop(1, "transparent");
          ctx.globalAlpha = 0.32 * twinkle * edge;
          ctx.fillStyle = gradient;
          ctx.beginPath();
          ctx.arc(0, 0, p.size, 0, Math.PI * 2);
          ctx.fill();
        } else if (kind === "gold") {
          ctx.globalAlpha = (0.35 + Math.sin(p.phase * 2.3) * 0.3) * edge;
          ctx.shadowColor = color;
          ctx.shadowBlur = 6;
          ctx.beginPath();
          ctx.arc(0, 0, p.size, 0, Math.PI * 2);
          ctx.fill();
        } else {
          // sparkle: a four-point star that fades in and out once.
          const life = Math.max(0, p.life);
          ctx.globalAlpha = Math.sin(life * Math.PI) * 0.7;
          const s = p.size;
          ctx.beginPath();
          ctx.moveTo(0, -s); ctx.quadraticCurveTo(0, 0, s, 0); ctx.quadraticCurveTo(0, 0, 0, s);
          ctx.quadraticCurveTo(0, 0, -s, 0); ctx.quadraticCurveTo(0, 0, 0, -s);
          ctx.fill();
        }
        ctx.restore();
      }
    };
    const onVisibility = () => {
      if (document.hidden && running) { running = false; cancelAnimationFrame(frame); }
      else if (!document.hidden && !running) { running = true; last = performance.now(); frame = requestAnimationFrame(draw); }
    };
    frame = requestAnimationFrame(draw);
    window.addEventListener("resize", resize);
    document.addEventListener("visibilitychange", onVisibility);
    return () => { cancelAnimationFrame(frame); window.removeEventListener("resize", resize); document.removeEventListener("visibilitychange", onVisibility); };
  }, [kind]);
  if (kind === "none") return null;
  return <canvas ref={canvas} className={m.ambient} style={{ "--col": `${width}px` } as CSSProperties} aria-hidden="true" />;
}

/* ── Action feedback ────────────────────────────────────────────── */

/** Fired by useRsvp / useWishes when a guest's RSVP or wish has been accepted. */
export const FEEDBACK_EVENT = "rawuh:feedback";
export function feedback(kind: "rsvp" | "wish") {
  if (typeof window === "undefined") return;
  // The submit button that's still focused is where the celebration bursts from.
  const from = document.activeElement instanceof HTMLElement && document.activeElement !== document.body ? document.activeElement : null;
  window.dispatchEvent(new CustomEvent(FEEDBACK_EVENT, { detail: { kind, from } }));
}

/** A springy "boop" on the element the guest just tapped (copy buttons and the like). */
export function boop(element: Element | null) {
  if (!(element instanceof HTMLElement) || reduced() || typeof element.animate !== "function") return;
  element.animate([{ scale: "1" }, { scale: "1.12" }, { scale: "0.97" }, { scale: "1" }], { duration: 420, easing: "cubic-bezier(.34, 1.56, .64, 1)" });
}
