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
