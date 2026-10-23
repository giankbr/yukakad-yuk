"use client";
/* Shared building blocks for Rawuh invitation themes.
 *
 * Every theme is a client component `(props: ThemeProps) => JSX` that renders:
 *   1. a cover ("Kepada Yth. …") shown first, with a button that calls `open()`
 *   2. the main one-page invitation
 * using <ThemeShell>. Data comes from `props.data` (real invitation or the theme's demo data).
 * Interactive pieces (RSVP, wishes, countdown, copy) use the hooks below so all themes behave the same.
 */
import { useCallback, useEffect, useId, useMemo, useRef, useState, type CSSProperties, type ReactNode } from "react";
import type { GiftMethod, InvitationData } from "../types";
import kit from "./kit.module.css";
import { autoReveal, revealChildren } from "@/lib/reveal";
import { celebrate, toast } from "@/lib/celebrate";
import { DietaryField, ReadingAids, ThankYouBanner, useInvitation, useThankYou } from "./extras";
import { Ambient, FEEDBACK_EVENT, Lightbox, MusicChip, ScrollProgress, Toaster, boop, enhanceCover, enhanceMain, feedback, leaveCover, useLightbox } from "./motion-layer";
import { motionOf } from "./motion";
import { themeMood } from "./mood";
import { OPEN_EVENT, useMusic } from "./music";

export type ThemeProps = {
  data: InvitationData;
  slug: string;
  guestToken?: string;
  /** Demo/preview: forms don't post, sample wishes are shown. */
  demo?: boolean;
  /** Render straight to the main page (used for previews/screenshots: `?open=1`). */
  skipCover?: boolean;
};

export { OPEN_EVENT, useMusic } from "./music";

const API = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8080";

/* ── Shell + cover gate ─────────────────────────────────────────── */

/**
 * Mobile-first frame. On wide screens the invitation is centered in a phone-width column.
 * `cover` receives `open`; the main content is rendered underneath and revealed after opening.
 */
export function ThemeShell({ cover, children, background = "#f4f4f4", width = 430, skipCover = false, className, style, fonts }: {
  cover: (open: () => void) => ReactNode;
  children: ReactNode;
  /** Page background around the phone column on desktop. */
  background?: string;
  width?: number;
  skipCover?: boolean;
  className?: string;
  style?: CSSProperties;
  /** Google Fonts families, e.g. ["Nunito Sans:wght@400;600;700;800"]. */
  fonts?: string[];
}) {
  const [opened, setOpened] = useState(skipCover);
  const [coverMounted, setCoverMounted] = useState(!skipCover);
  const coverRef = useRef<HTMLDivElement>(null);
  const mainRef = useRef<HTMLDivElement>(null);
  const themeId = useInvitation()?.theme;
  const motion = motionOf(themeId);
  const mood = themeMood(themeId);
  const lightbox = useLightbox(mainRef, opened);
  // Cover: stagger its content in on first paint, then add the Ken Burns photo + breathing open button.
  useEffect(() => {
    const root = coverRef.current?.firstElementChild;
    if (root instanceof HTMLElement) revealChildren(root, motion === "elegant" ? { stagger: 140, delay: 200 } : motion === "crisp" ? { stagger: 50, delay: 60 } : { stagger: 80, delay: 120 });
    return enhanceCover(coverRef.current);
  }, [motion]);
  // Main page: scroll-reveal every section once the invitation is open.
  useEffect(() => {
    if (!opened || !mainRef.current) return;
    const main = mainRef.current;
    const stop = autoReveal(main, motion === "elegant" ? { stagger: 110 } : motion === "crisp" ? { stagger: 40, maxStagger: 4 } : { stagger: 65 });
    const parallax = enhanceMain(main);
    return () => { stop(); parallax(); };
  }, [opened, motion]);
  const open = useCallback(() => {
    // `open` is handed to the theme's cover during render, so it finds the cover and page through the DOM, not refs.
    const button = document.activeElement instanceof HTMLElement ? document.activeElement : null;
    const dialog = button?.closest<HTMLElement>('[aria-label="Sampul undangan"]') ?? document.querySelector<HTMLElement>('[aria-label="Sampul undangan"]');
    const main = dialog?.parentElement?.querySelector<HTMLElement>(":scope > [data-invitation-main]") ?? null;
    setOpened(true);
    window.scrollTo({ top: 0 });
    // Let the cover leave in the theme's own way (doors, iris, curtain, pop) before unmounting it.
    setTimeout(() => setCoverMounted(false), leaveCover(mood.cover, dialog, main));
    if (mood.burst && button && dialog?.contains(button)) celebrate(button);
    // Opening the cover is a user gesture, so background music may start now (see <MusicPlayer>).
    window.dispatchEvent(new Event(OPEN_EVENT));
  }, [mood]);
  // RSVP / wish accepted: a theme-flavoured burst from the submit button (celebrate() skips repeats).
  useEffect(() => {
    const onFeedback = (event: Event) => {
      const from = (event as CustomEvent<{ from: HTMLElement | null }>).detail?.from;
      celebrate(from && mainRef.current?.contains(from) ? from : mainRef.current);
    };
    window.addEventListener(FEEDBACK_EVENT, onFeedback);
    return () => window.removeEventListener(FEEDBACK_EVENT, onFeedback);
  }, []);
  // Deep links from table QR cards (e.g. #extra-foto-tamu) open the invitation straight to that section.
  useEffect(() => {
    const hash = window.location.hash;
    if (!/^#extra-[\w-]+$/.test(hash)) return;
    const timer = setTimeout(() => {
      open();
      setTimeout(() => document.querySelector(hash)?.scrollIntoView({ block: "start" }), 700);
    }, 0);
    return () => clearTimeout(timer);
  }, [open]);
  useEffect(() => {
    if (opened) return;
    const previous = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    return () => { document.body.style.overflow = previous; };
  }, [opened]);
  const fontHref = fonts?.length ? `https://fonts.googleapis.com/css2?${fonts.map(f => `family=${f.replace(/ /g, "+")}`).join("&")}&display=swap` : undefined;
  return (
    <div style={{ minHeight: "100dvh", background, display: "flex", justifyContent: "center" }}>
      {/* Fonts are scoped to the invitation route. */}
      {fontHref && <link rel="stylesheet" href={fontHref} />}
      <div className={className} data-motion={motion} style={{ position: "relative", width: "100%", maxWidth: width, minHeight: "100dvh", overflowX: "clip", ...style }}>
        {coverMounted && (
          <div role="dialog" aria-modal="true" aria-label="Sampul undangan" className={opened && mood.cover === "lift" ? kit.coverLeave : undefined}
            style={{ position: "fixed", inset: 0, zIndex: 50, display: "flex", justifyContent: "center", background: opened ? "transparent" : background, overflowY: "auto", pointerEvents: opened ? "none" : undefined }}>
            <div ref={coverRef} style={{ position: "relative", width: "100%", maxWidth: width, minHeight: "100dvh" }}>{cover(open)}</div>
          </div>
        )}
        <div ref={mainRef} data-invitation-main aria-hidden={!opened} style={opened ? undefined : { visibility: "hidden", height: "100dvh", overflow: "hidden" }}><ThankYouBanner />{children}</div>
        {opened && <ReadingAids />}
        {opened && <ScrollProgress width={width} />}
        {opened && <Ambient kind={mood.ambient} width={width} />}
        <Toaster />
        <MusicChip />
        {lightbox.state && <Lightbox {...lightbox.state} onClose={lightbox.close} onIndex={lightbox.setIndex} />}
      </div>
    </div>
  );
}

/* ── Formatting ─────────────────────────────────────────────────── */

const TZ = "Asia/Jakarta";

export function toDate(value?: string) {
  if (!value) return undefined;
  const date = new Date(value);
  return Number.isNaN(date.getTime()) ? undefined : date;
}

/** Placeholder shown wherever a date is missing or can't be parsed. */
export const DATE_TBA = "Tanggal menyusul";

/** Format a date in Indonesian; returns "Tanggal menyusul" when it isn't a valid date. */
export function formatDate(value: string | undefined, options: Intl.DateTimeFormatOptions = { weekday: "long", day: "numeric", month: "long", year: "numeric" }) {
  const date = toDate(value);
  if (!date) return DATE_TBA;
  return new Intl.DateTimeFormat("id-ID", { timeZone: TZ, ...options }).format(date);
}

/** Pieces for calendar-style blocks: { day: "20", month: "Juni", monthShort: "JUN", year: "2026", weekday: "Sabtu", weekdayShort: "SAB" } */
export function dateParts(value?: string) {
  const date = toDate(value);
  if (!date) return { day: "", month: "", monthShort: "", year: "", weekday: "", weekdayShort: "" };
  const part = (o: Intl.DateTimeFormatOptions) => new Intl.DateTimeFormat("id-ID", { timeZone: TZ, ...o }).format(date);
  return {
    day: part({ day: "numeric" }),
    month: part({ month: "long" }),
    monthShort: part({ month: "short" }).replace(".", "").toUpperCase(),
    year: part({ year: "numeric" }),
    weekday: part({ weekday: "long" }),
    weekdayShort: part({ weekday: "short" }).replace(".", "").toUpperCase(),
  };
}

export function guestLabel(data: InvitationData, fallback = "Tamu Undangan") {
  return data.guestName?.trim() || fallback;
}

export function coupleLabel(data: InvitationData, joiner = " & ") {
  const groom = data.couple.groom?.trim();
  return groom ? `${data.couple.bride}${joiner}${groom}` : data.couple.bride;
}

/** Initials like "R&B". */
export function coupleInitials(data: InvitationData, joiner = "&") {
  const groom = data.couple.groom?.trim();
  return (groom ? `${data.couple.bride.slice(0, 1)}${joiner}${groom.slice(0, 1)}` : data.couple.bride.slice(0, 1)).toUpperCase();
}

export function safeUrl(url?: string) {
  return url && /^https?:\/\//i.test(url) ? url : undefined;
}

/** Maps link for an event (falls back to the invitation's main maps link, then a search). */
export function mapsHref(data: InvitationData, event?: InvitationData["events"][number]) {
  const direct = safeUrl(event?.mapsUrl) ?? safeUrl(data.mapsUrl);
  if (direct) return direct;
  const query = [event?.venue ?? data.place, event?.address ?? data.address].filter(Boolean).join(", ");
  return query ? `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(query)}` : undefined;
}

/** Story timeline: real `stories`, else the single `story`. */
export function storyItems(data: InvitationData) {
  if (data.stories?.length) return data.stories;
  return data.story?.body ? [{ title: data.story.title, body: data.story.body }] : [];
}

/** Normalised gift line for display + copy. */
export function giftInfo(gift: GiftMethod) {
  switch (gift.type) {
    case "bank": return { kind: "Transfer bank", title: gift.bank_name ?? "Bank", number: gift.account_number ?? "", holder: gift.account_name ?? "", copy: gift.account_number };
    case "ewallet": return { kind: "E-wallet", title: (gift.ewallet_provider ?? "E-wallet").replace(/^\w/, c => c.toUpperCase()), number: gift.ewallet_number ?? "", holder: gift.account_name ?? "", copy: gift.ewallet_number };
    case "qris": return { kind: "QRIS", title: "QRIS", number: "", holder: "", copy: undefined, image: gift.qris_image_url };
    case "address": return { kind: "Kirim kado", title: "Alamat kado", number: gift.address ?? "", holder: "", copy: gift.address };
  }
}

/* ── Countdown ──────────────────────────────────────────────────── */

export function useCountdown(value?: string) {
  const target = toDate(value)?.getTime();
  const [now, setNow] = useState<number | null>(null);
  useEffect(() => {
    if (!target) return;
    const tick = () => setNow(Date.now());
    tick();
    const id = setInterval(tick, 1000);
    return () => clearInterval(id);
  }, [target]);
  return useMemo(() => {
    // No (valid) date yet: render nothing in the digits; themes may hide the block via `valid`.
    if (!target) return { days: "", hours: "", minutes: "", seconds: "", done: false, ready: false, valid: false };
    if (now === null) return { days: "--", hours: "--", minutes: "--", seconds: "--", done: false, ready: false, valid: true };
    const diff = Math.max(0, target - now);
    const pad = (n: number) => String(n).padStart(2, "0");
    return {
      days: pad(Math.floor(diff / 86400000)),
      hours: pad(Math.floor(diff / 3600000) % 24),
      minutes: pad(Math.floor(diff / 60000) % 60),
      seconds: pad(Math.floor(diff / 1000) % 60),
      done: diff === 0,
      ready: true,
      valid: true,
    };
  }, [target, now]);
}

/** A countdown digit that rolls in whenever its value changes: <Tick value={countdown.seconds} />. */
export function Tick({ value, className, style }: { value: string | number; className?: string; style?: CSSProperties }) {
  return <span className={className} style={{ display: "inline-block", overflow: "hidden", verticalAlign: "bottom", ...style }}><span key={value} className={kit.tick}>{value}</span></span>;
}

/* ── RSVP ───────────────────────────────────────────────────────── */

export type Attendance = "yes" | "no" | "maybe";
export type RsvpInput = { name: string; attendance: Attendance; guests?: number; message?: string; diet?: string };

export function useRsvp({ slug, guestToken, demo }: Pick<ThemeProps, "slug" | "guestToken" | "demo">) {
  /** `closed`: the couple switched on thank-you mode, the backend no longer accepts RSVPs (409 rsvp_closed). */
  const [status, setStatus] = useState<"idle" | "sending" | "sent" | "error" | "closed">("idle");
  const submit = useCallback(async (input: RsvpInput) => {
    if (status === "sending") return;
    if (demo) { feedback("rsvp"); setStatus("sent"); return; }
    setStatus("sending");
    try {
      const response = await fetch(`${API}/api/public/invitation/${encodeURIComponent(slug)}/rsvp`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          guest_token: guestToken,
          attendance: input.attendance,
          attendees_count: Math.min(10, Math.max(1, input.guests ?? 1)),
          message: `${input.name}: ${input.message ?? ""}${input.diet ? ` [Catatan makanan: ${input.diet}]` : ""}`.trim(),
        }),
      });
      if (response.ok) { feedback("rsvp"); setStatus("sent"); return; }
      if (response.status === 409) {
        const body = await response.json().catch(() => null) as { code?: string } | null;
        if (body?.code === "rsvp_closed") { setStatus("closed"); return; }
      }
      setStatus("error");
    } catch {
      setStatus("error");
    }
  }, [demo, guestToken, slug, status]);
  return { submit, status, reset: () => setStatus("idle") };
}

/** Uncontrolled helper: read a <form> into RsvpInput (fields: name, attendance, guests, message). */
export function readRsvpForm(form: HTMLFormElement): RsvpInput {
  const data = new FormData(form);
  const attendance = String(data.get("attendance") ?? "yes");
  return {
    name: String(data.get("name") ?? "").trim(),
    attendance: attendance === "no" || attendance === "maybe" ? attendance : "yes",
    guests: Number(data.get("guests") ?? 1) || 1,
    message: String(data.get("message") ?? "").trim(),
    diet: String(data.get("diet") ?? "").trim() || undefined,
  };
}

/* ── Wishes ─────────────────────────────────────────────────────── */

export type Wish = { id: string; name: string; message: string; created_at?: string; attendance?: Attendance };

/** Published wishes (live) — in demo mode returns `seed` and accepts local submissions. */
export function useWishes({ slug, guestToken, demo, seed = [] }: Pick<ThemeProps, "slug" | "guestToken" | "demo"> & { seed?: Wish[] }) {
  const [wishes, setWishes] = useState<Wish[]>(demo ? seed : []);
  const [status, setStatus] = useState<"idle" | "sending" | "sent" | "error">("idle");
  /** The last sent wish waits for the couple's approval before it's shown (moderation on). */
  const [pending, setPending] = useState(false);
  useEffect(() => {
    if (demo) return;
    let alive = true;
    fetch(`${API}/api/public/invitation/${encodeURIComponent(slug)}/wishes`)
      .then(r => (r.ok ? r.json() : { items: [] }))
      .then((body: { items?: Wish[] }) => { if (alive) setWishes(body.items ?? []); })
      .catch(() => undefined);
    return () => { alive = false; };
  }, [demo, slug]);
  const send = useCallback(async (name: string, message: string) => {
    if (!name.trim() || !message.trim()) return;
    if (demo) {
      setWishes(list => [{ id: `local-${Date.now()}`, name, message, created_at: new Date().toISOString() }, ...list]);
      setPending(false);
      feedback("wish");
      setStatus("sent");
      return;
    }
    setStatus("sending");
    try {
      const response = await fetch(`${API}/api/public/invitation/${encodeURIComponent(slug)}/wishes`, {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ guest_token: guestToken, name, message }),
      });
      if (!response.ok) { setStatus("error"); return; }
      // The backend answers with the stored wish; status "pending" means it's held for moderation.
      const wish = await response.json().catch(() => null) as (Wish & { status?: string }) | null;
      const published = wish?.status === "published";
      setPending(!published);
      if (published && wish?.id) setWishes(list => [{ id: wish.id, name: wish.name ?? name, message: wish.message ?? message, created_at: wish.created_at }, ...list.filter(item => item.id !== wish.id)]);
      feedback("wish");
      setStatus("sent");
    } catch {
      setStatus("error");
    }
  }, [demo, guestToken, slug]);
  return {
    wishes, send, status, pending,
    /** Confirmation line after sending (live mode). */
    sentNote: pending ? "Ucapanmu akan tampil setelah disetujui oleh mempelai." : "Terima kasih atas doa dan ucapannya.",
    reset: () => setStatus("idle"),
  };
}

/** Confirmation line for themes with a combined RSVP + wish form (live mode). */
export function sentSummary(rsvp: ReturnType<typeof useRsvp>, wishes: ReturnType<typeof useWishes>) {
  const rsvpSent = rsvp.status === "sent";
  const wishSent = wishes.status === "sent";
  if (rsvpSent && wishSent) return wishes.pending ? "Konfirmasi kehadiranmu sudah kami terima. Ucapanmu akan tampil setelah disetujui oleh mempelai." : "Konfirmasi dan ucapanmu sudah kami terima.";
  if (rsvpSent) return "Konfirmasi kehadiranmu sudah kami terima.";
  return wishes.sentNote;
}

/** "2 jam lalu" style relative time. */
export function timeAgo(value?: string) {
  const date = toDate(value);
  if (!date) return "";
  const minutes = Math.round((Date.now() - date.getTime()) / 60000);
  if (minutes < 1) return "baru saja";
  if (minutes < 60) return `${minutes} menit lalu`;
  const hours = Math.round(minutes / 60);
  if (hours < 24) return `${hours} jam lalu`;
  const days = Math.round(hours / 24);
  if (days < 30) return `${days} hari lalu`;
  return formatDate(value, { day: "numeric", month: "short", year: "numeric" });
}

/* ── Copy to clipboard ──────────────────────────────────────────── */

export function useCopy() {
  const [copied, setCopied] = useState<string | null>(null);
  const copy = useCallback(async (value?: string) => {
    if (!value) return;
    try {
      const button = document.activeElement;
      await navigator.clipboard.writeText(value);
      boop(button);
      setCopied(value);
      toast("Disalin");
      navigator.vibrate?.(8);
      setTimeout(() => setCopied(current => (current === value ? null : current)), 2000);
    } catch { /* clipboard blocked: the value is still visible */ }
  }, []);
  return { copy, copied };
}

/* ── Small helpers ──────────────────────────────────────────────── */

/** Photo with graceful empty state; `src` may be user-supplied. */
export function Photo({ src, alt = "", className, style }: { src?: string; alt?: string; className?: string; style?: CSSProperties }) {
  if (!src) return <div className={className} style={{ background: "linear-gradient(135deg,#e7e2da,#cfc7bb)", ...style }} role={alt ? "img" : undefined} aria-label={alt || undefined} />;
  // eslint-disable-next-line @next/next/no-img-element -- invitation photos can be user-supplied URLs
  return <img src={src} alt={alt} className={className} style={{ objectFit: "cover", display: "block", ...style }} loading="lazy" />;
}

/** Inline lucide-style icon from a raw path list (keeps themes free of icon dependencies). */
export function Icon({ d, size = 16, stroke = "currentColor", strokeWidth = 2, fill = "none", style, className }: {
  d: string | string[]; size?: number; stroke?: string; strokeWidth?: number; fill?: string; style?: CSSProperties; className?: string;
}) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill={fill} stroke={stroke} strokeWidth={strokeWidth} strokeLinecap="round" strokeLinejoin="round" aria-hidden="true" focusable="false" style={{ flexShrink: 0, ...style }} className={className}>
      {(Array.isArray(d) ? d : [d]).map((path, index) => <path key={index} d={path} />)}
    </svg>
  );
}

/** Lucide icon paths used across themes (copy more from lucide.dev as needed). */
export const icons = {
  mail: ["M22 7l-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7", "M4 4h16a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2z"],
  mailOpen: ["M21.2 8.4c.5.38.8.97.8 1.6v10a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V10a2 2 0 0 1 .8-1.6l8-6a2 2 0 0 1 2.4 0l8 6Z", "m22 10-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 10"],
  mapPin: ["M20 10c0 4.99-5.54 10.19-7.4 11.8a1 1 0 0 1-1.2 0C9.54 20.19 4 14.99 4 10a8 8 0 0 1 16 0", "M12 7a3 3 0 1 0 0 6 3 3 0 1 0 0-6z"],
  calendar: ["M8 2v4", "M16 2v4", "M3 10h18", "M5 4h14a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2z"],
  clock: ["M12 2a10 10 0 1 0 0 20 10 10 0 1 0 0-20z", "M12 6v6l4 2"],
  copy: ["M10 8h10a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2H10a2 2 0 0 1-2-2V10a2 2 0 0 1 2-2z", "M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2"],
  check: "M20 6 9 17l-5-5",
  heart: "M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z",
  gift: ["M3 8h18v4H3z", "M12 8v13", "M19 12v7a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2v-7", "M7.5 8a2.5 2.5 0 0 1 0-5A4.8 8 0 0 1 12 8a4.8 8 0 0 1 4.5-5 2.5 2.5 0 0 1 0 5"],
  play: "M6 3l14 9-14 9V3z",
  send: ["m22 2-7 20-4-9-9-4Z", "M22 2 11 13"],
  star: "M11.5 2.3a.5.5 0 0 1 1 0l2.3 4.7a2 2 0 0 0 1.6 1.2l5.2.7a.5.5 0 0 1 .3.9l-3.8 3.7a2 2 0 0 0-.6 1.9l.9 5.1a.5.5 0 0 1-.8.6l-4.6-2.4a2 2 0 0 0-2 0l-4.6 2.4a.5.5 0 0 1-.8-.6l.9-5.1a2 2 0 0 0-.6-1.9L2.2 9.8a.5.5 0 0 1 .3-.9l5.2-.7a2 2 0 0 0 1.6-1.2z",
  chevronRight: "m9 18 6-6-6-6",
  arrowRight: ["M5 12h14", "m12 5 7 7-7 7"],
  messageCircle: "M7.9 20A9 9 0 1 0 4 16.1L2 22Z",
  users: ["M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2", "M9 3a4 4 0 1 0 0 8 4 4 0 1 0 0-8z", "M22 21v-2a4 4 0 0 0-3-3.87", "M16 3.13a4 4 0 0 1 0 7.75"],
};

/* ── Sheets: RSVP + wishes (shared behaviour, tinted per theme via CSS vars) ── */

export type ThemeTint = {
  "--t-accent"?: string; "--t-accent-ink"?: string; "--t-bg"?: string; "--t-ink"?: string; "--t-muted"?: string;
  "--t-line"?: string; "--t-field"?: string; "--t-radius"?: string; "--t-font"?: string;
};

export function Sheet({ open, onClose, title, tint, children }: { open: boolean; onClose: () => void; title: string; tint?: ThemeTint; children: ReactNode }) {
  // Stay mounted while the closing animation plays (adjusting state during render, no effect needed).
  const [shown, setShown] = useState(open);
  if (open && !shown) setShown(true);
  const leaving = shown && !open;
  const sheet = useRef<HTMLDivElement>(null);
  const backdrop = useRef<HTMLDivElement>(null);
  const drag = useRef<{ y: number; dy: number; t: number } | null>(null);
  useEffect(() => {
    if (!open) return;
    const onKey = (event: KeyboardEvent) => { if (event.key === "Escape") onClose(); };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [open, onClose]);
  if (!shown) return null;
  const release = () => {
    const state = drag.current;
    drag.current = null;
    const element = sheet.current;
    if (!state || !element) return;
    const fast = state.dy / Math.max(1, Date.now() - state.t) > 0.6;
    element.style.transition = "translate 260ms cubic-bezier(.2, .8, .2, 1)";
    if (backdrop.current) backdrop.current.style.opacity = "";
    if (state.dy > 120 || (fast && state.dy > 40)) onClose();
    else element.style.translate = "";
  };
  return (
    <div ref={backdrop} className={`${kit.backdrop} ${leaving ? kit.backdropLeave : ""}`} style={tint as CSSProperties}
      onClick={event => { if (event.target === event.currentTarget) onClose(); }}
      onAnimationEnd={event => { if (leaving && event.target === event.currentTarget) setShown(false); }}>
      <div ref={sheet} className={`${kit.sheet} ${leaving ? kit.sheetLeave : ""}`} role="dialog" aria-modal="true" aria-label={title}
        onTouchStart={event => {
          if ((sheet.current?.scrollTop ?? 0) > 0) return;
          drag.current = { y: event.touches[0].clientY, dy: 0, t: Date.now() };
          if (sheet.current) sheet.current.style.transition = "none";
        }}
        onTouchMove={event => {
          const state = drag.current;
          if (!state || !sheet.current) return;
          state.dy = Math.max(0, event.touches[0].clientY - state.y);
          if (state.dy > 0 && sheet.current.scrollTop <= 0) {
            sheet.current.style.translate = `0 ${state.dy}px`;
            if (backdrop.current) backdrop.current.style.opacity = String(Math.max(0.35, 1 - state.dy / 500));
          }
        }}
        onTouchEnd={release} onTouchCancel={release}>
        <div className={kit.grip} aria-hidden />
        <div className={kit.head}><h2>{title}</h2><button type="button" className={kit.close} onClick={onClose} aria-label="Tutup">×</button></div>
        {children}
      </div>
    </div>
  );
}

/** Fires a theme-flavoured celebration once when `when` turns true. */
function useCelebrate(when: boolean) {
  const ref = useRef<HTMLSpanElement>(null);
  useEffect(() => { if (when) celebrate(ref.current); }, [when]);
  return ref;
}

/** RSVP form (name, attendance, guest count, message). Use inside <Sheet> or inline. */
export function RsvpForm({ rsvp, guestName, demo, labels, initialAttendance = "yes" }: {
  rsvp: ReturnType<typeof useRsvp>; guestName?: string; demo?: boolean; initialAttendance?: Attendance;
  labels?: { submit?: string; yes?: string; maybe?: string; no?: string; success?: string };
}) {
  const [guests, setGuests] = useState(1);
  const thanks = useThankYou();
  const party = useCelebrate(rsvp.status === "sent");
  if (thanks.active || rsvp.status === "closed") {
    return (
      <div className={kit.state} role="status">
        <span className={kit.badge}><Icon d={icons.heart} size={24} strokeWidth={2.4} /></span>
        <strong>Konfirmasi kehadiran sudah ditutup</strong>
        <p>Acara telah berlangsung. Terima kasih atas doa dan perhatiannya.</p>
      </div>
    );
  }
  if (rsvp.status === "sent") {
    return (
      <div className={kit.state} role="status">
        <span ref={party} className={`${kit.badge} ${kit.badgePop}`}><Icon d={icons.check} size={26} strokeWidth={3} className={kit.draw} /></span>
        <strong>{labels?.success ?? "Terima kasih!"}</strong>
        <p>{demo ? "Ini pratinjau — jawaban contoh tidak dikirim." : "Konfirmasi kehadiranmu sudah kami terima."}</p>
      </div>
    );
  }
  return (
    <form className={kit.form} onSubmit={event => { event.preventDefault(); void rsvp.submit({ ...readRsvpForm(event.currentTarget), guests }); }}>
      <label className={kit.field}>Nama<input name="name" required maxLength={100} defaultValue={guestName && guestName !== "Tamu Undangan" ? guestName : ""} placeholder="Nama kamu" autoComplete="name" /></label>
      <fieldset className={kit.field} style={{ border: 0, margin: 0, padding: 0 }}>
        <legend style={{ marginBottom: 6 }}>Kehadiran</legend>
        <div className={kit.choices}>
          <label><input type="radio" name="attendance" value="yes" defaultChecked={initialAttendance === "yes"} />{labels?.yes ?? "Hadir"}</label>
          <label><input type="radio" name="attendance" value="maybe" defaultChecked={initialAttendance === "maybe"} />{labels?.maybe ?? "Ragu"}</label>
          <label><input type="radio" name="attendance" value="no" defaultChecked={initialAttendance === "no"} />{labels?.no ?? "Berhalangan"}</label>
        </div>
      </fieldset>
      <div className={kit.field}>
        <span id="rsvp-guests">Jumlah tamu</span>
        <div className={kit.stepper} role="group" aria-labelledby="rsvp-guests">
          <button type="button" onClick={() => setGuests(g => Math.max(1, g - 1))} aria-label="Kurangi">−</button>
          <output aria-live="polite">{guests}</output>
          <button type="button" onClick={() => setGuests(g => Math.min(10, g + 1))} aria-label="Tambah">+</button>
        </div>
      </div>
      <DietaryField className={kit.field} />
      <label className={kit.field}>Pesan (opsional)<textarea name="message" maxLength={500} rows={3} placeholder="Tulis doa atau pesan…" /></label>
      {rsvp.status === "error" && <p className={kit.error} role="alert">Belum terkirim. Periksa koneksi lalu coba lagi.</p>}
      <button type="submit" className={kit.submit} disabled={rsvp.status === "sending"}>{rsvp.status === "sending" ? "Mengirim…" : labels?.submit ?? "Kirim Konfirmasi"}</button>
    </form>
  );
}

/** Wish form (name + message). */
export function WishForm({ wishes, guestName, demo, submitLabel }: { wishes: ReturnType<typeof useWishes>; guestName?: string; demo?: boolean; submitLabel?: string }) {
  const party = useCelebrate(wishes.status === "sent");
  if (wishes.status === "sent") {
    return (
      <div className={kit.state} role="status">
        <span ref={party} className={`${kit.badge} ${kit.badgePop}`}><Icon d={icons.heart} size={24} strokeWidth={2.4} /></span>
        <strong>Ucapan terkirim</strong>
        <p>{demo ? "Ucapanmu muncul di daftar (pratinjau)." : wishes.sentNote}</p>
        <button type="button" className={kit.submit} style={{ minWidth: 180 }} onClick={wishes.reset}>Tulis lagi</button>
      </div>
    );
  }
  return (
    <form className={kit.form} onSubmit={event => {
      event.preventDefault();
      const form = new FormData(event.currentTarget);
      void wishes.send(String(form.get("name") ?? "").trim(), String(form.get("message") ?? "").trim());
    }}>
      <label className={kit.field}>Nama<input name="name" required maxLength={100} defaultValue={guestName && guestName !== "Tamu Undangan" ? guestName : ""} placeholder="Nama kamu" autoComplete="name" /></label>
      <label className={kit.field}>Ucapan & doa<textarea name="message" required maxLength={500} rows={4} placeholder="Tulis ucapan terbaikmu…" /></label>
      {wishes.status === "error" && <p className={kit.error} role="alert">Belum terkirim. Coba lagi sebentar lagi.</p>}
      <button type="submit" className={kit.submit} disabled={wishes.status === "sending"}>{wishes.status === "sending" ? "Mengirim…" : submitLabel ?? "Kirim Ucapan"}</button>
    </form>
  );
}

/** Convenience: state for the two sheets most themes need. */
export function useSheets() {
  const [sheet, setSheet] = useState<null | "rsvp" | "wish">(null);
  const [attendance, setAttendance] = useState<Attendance>("yes");
  return {
    sheet,
    /** Answer to preselect in <RsvpForm initialAttendance={sheets.attendance} key={sheets.attendance} />. */
    attendance,
    openRsvp: (answer?: Attendance | unknown) => {
      setAttendance(answer === "no" || answer === "maybe" ? answer : "yes");
      setSheet("rsvp");
    },
    openWish: () => setSheet("wish"),
    close: () => setSheet(null),
  };
}

/**
 * Guest-count stepper for inline RSVP forms. Renders a hidden `guests` input, so
 * `readRsvpForm(form)` picks the value up automatically. Style it via `className`/`buttonClassName`.
 */
export function GuestCount({ label = "Jumlah tamu", max = 10, className, buttonClassName, labelClassName, style }: {
  label?: string; max?: number; className?: string; buttonClassName?: string; labelClassName?: string; style?: CSSProperties;
}) {
  const [count, setCount] = useState(1);
  const id = useId();
  const button: CSSProperties = { width: 36, height: 36, display: "grid", placeItems: "center", border: "1px solid currentColor", borderRadius: 999, background: "transparent", color: "inherit", font: "inherit", fontSize: 18, lineHeight: 1, cursor: "pointer", opacity: 0.85 };
  return (
    <div className={className} style={{ display: "flex", alignItems: "center", justifyContent: "space-between", gap: 12, ...style }}>
      <span id={id} className={labelClassName}>{label}</span>
      <span role="group" aria-labelledby={id} style={{ display: "flex", alignItems: "center", gap: 10 }}>
        <button type="button" className={buttonClassName} style={buttonClassName ? undefined : button} onClick={() => setCount(c => Math.max(1, c - 1))} aria-label="Kurangi jumlah tamu">−</button>
        <output aria-live="polite" style={{ minWidth: 24, textAlign: "center", fontWeight: 700, fontVariantNumeric: "tabular-nums" }}>{count}</output>
        <button type="button" className={buttonClassName} style={buttonClassName ? undefined : button} onClick={() => setCount(c => Math.min(max, c + 1))} aria-label="Tambah jumlah tamu">+</button>
      </span>
      <input type="hidden" name="guests" value={count} />
    </div>
  );
}

/** Generic floating music toggle, rendered by the invitation page; hides itself when the theme has its own player. */
export function MusicPlayer({ music, accent = "rgba(17,16,16,.72)" }: { music?: InvitationData["music"]; accent?: string }) {
  const player = useMusic(music, { generic: true });
  // A broken track: drop the toggle instead of offering a button that does nothing.
  if (!player.visible || player.failed || player.ownedByTheme) return null;
  return (
    <button type="button" onClick={player.toggle} aria-pressed={player.playing} {...player.attrs} aria-label={player.playing ? "Jeda musik" : "Putar musik"}
      style={{ position: "fixed", right: "max(14px, calc(50% - 215px + 14px))", bottom: 104, zIndex: 60, width: 44, height: 44, display: "grid", placeItems: "center", border: "1px solid rgba(255,255,255,.35)", borderRadius: 999, background: accent, color: "#fff", boxShadow: "0 8px 24px rgba(0,0,0,.25)", backdropFilter: "blur(8px)", cursor: "pointer" }}>
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
        <path d="M9 18V5l12-2v13" /><circle cx="6" cy="18" r="3" /><circle cx="18" cy="16" r="3" />{!player.playing && <path d="M2 2l20 20" />}
      </svg>
    </button>
  );
}

/** Render a lucide icon from its inner SVG markup (generated per theme into `icons.ts`). */
export function Lucide({ icon, size = 16, color = "currentColor", strokeWidth = 2, style, className }: {
  icon: string; size?: number; color?: string; strokeWidth?: number; style?: CSSProperties; className?: string;
}) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth={strokeWidth} strokeLinecap="round" strokeLinejoin="round"
      aria-hidden="true" focusable="false" style={{ flexShrink: 0, display: "block", ...style }} className={className}
      dangerouslySetInnerHTML={{ __html: icon }} />
  );
}

export { Extras, DietaryField, InvitationProvider, useInvitation, useThankYou } from "./extras";
