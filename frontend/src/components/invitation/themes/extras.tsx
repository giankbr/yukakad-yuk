"use client";
// Optional "extra" sections shared by every Rawuh theme (quote, livestream, dress code, rundown, FAQ, …).
// Themes drop <Extras slot="…" /> where each group fits their layout; the blocks read the invitation from
// <InvitationProvider> and style themselves from the surrounding colour (currentColor) plus the theme's
// --t-* tokens, so they look native on light and dark themes alike.
import { createContext, useContext, useEffect, useMemo, useState, type ReactNode } from "react";
import QRCode from "qrcode";
import type { InvitationData, InvitationExtras, OnlineGift, WishlistItem } from "../types";
import x from "./extras.module.css";

const API = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8080";
const TZ = "Asia/Jakarta";

type Ctx = { data: InvitationData; slug: string; guestToken?: string; demo?: boolean };
const InvitationContext = createContext<Ctx | null>(null);

export function InvitationProvider({ children, ...value }: Ctx & { children: ReactNode }) {
  return <InvitationContext.Provider value={value}>{children}</InvitationContext.Provider>;
}

export function useInvitation() {
  return useContext(InvitationContext);
}

/** Section data only when it is filled in and not switched off. */
function on<K extends keyof InvitationExtras>(extras: InvitationExtras | undefined, key: K): InvitationExtras[K] | undefined {
  const value = extras?.[key] as ({ enabled?: boolean } & Record<string, unknown>) | undefined;
  if (!value || value.enabled === false) return undefined;
  return value as InvitationExtras[K];
}

/* ── Dates ──────────────────────────────────────────────────────── */

function toDate(value?: string) {
  if (!value) return undefined;
  const date = new Date(value);
  return Number.isNaN(date.getTime()) ? undefined : date;
}

function fmt(value: string | undefined, options: Intl.DateTimeFormatOptions) {
  const date = toDate(value);
  return date ? new Intl.DateTimeFormat("id-ID", { timeZone: TZ, ...options }).format(date) : value ?? "";
}

/** Last moment of the celebration: latest event start + 1 day (falls back to the main date). */
function eventsOver(data: InvitationData, now = Date.now()) {
  const times = [data.date, ...data.events.map(event => event.date)].map(value => toDate(value)?.getTime()).filter((t): t is number => Boolean(t));
  if (!times.length) return false;
  return now > Math.max(...times) + 24 * 60 * 60 * 1000;
}

/** Thank-you mode: forced on/off from the dashboard, or automatic once the event is over. */
export function useThankYou() {
  const ctx = useInvitation();
  const [over, setOver] = useState(false);
  const mode = ctx?.data.extras?.thankYou?.mode ?? "auto";
  // Evaluated after mount so server and client markup agree.
  useEffect(() => {
    if (!ctx || mode !== "auto") return;
    const timer = setTimeout(() => setOver(eventsOver(ctx.data)), 0);
    return () => clearTimeout(timer);
  }, [ctx, mode]);
  if (!ctx) return { active: false, message: "" };
  const active = mode === "on" || (mode === "auto" && over);
  return {
    active,
    message: ctx.data.extras?.thankYou?.message?.trim()
      || "Terima kasih atas doa, kehadiran, dan kasih sayang yang kalian berikan di hari bahagia kami.",
  };
}

/** Event start/end in UTC calendar format (YYYYMMDDTHHMMSSZ). */
function eventRange(event: InvitationData["events"][number]) {
  const start = toDate(event.date);
  if (!start) return undefined;
  let end = new Date(start.getTime() + 2 * 60 * 60 * 1000);
  // "08.00 – 10.00 WIB" → end at 10.00 on the same (WIB) day.
  const times = Array.from(event.time?.matchAll(/(\d{1,2})[.:](\d{2})/g) ?? []);
  if (times.length >= 2) {
    const [, hh, mm] = times[1];
    const wibMidnight = new Date(`${new Intl.DateTimeFormat("en-CA", { timeZone: TZ }).format(start)}T00:00:00+07:00`);
    const candidate = new Date(wibMidnight.getTime() + (Number(hh) * 60 + Number(mm)) * 60 * 1000);
    if (candidate > start) end = candidate;
  }
  const stamp = (date: Date) => date.toISOString().replace(/[-:]/g, "").replace(/\.\d{3}/, "");
  return { start: stamp(start), end: stamp(end) };
}

function googleCalendarHref(data: InvitationData, event: InvitationData["events"][number]) {
  const range = eventRange(event);
  if (!range) return undefined;
  const params = new URLSearchParams({
    action: "TEMPLATE",
    text: `${event.name} · ${data.couple.bride} & ${data.couple.groom}`,
    dates: `${range.start}/${range.end}`,
    location: [event.venue, event.address].filter(Boolean).join(", "),
    details: "Undangan dari Rawuh",
    ctz: TZ,
  });
  return `https://calendar.google.com/calendar/render?${params}`;
}

function downloadIcs(data: InvitationData, event: InvitationData["events"][number]) {
  const range = eventRange(event);
  if (!range) return;
  const escape = (value: string) => value.replace(/[\\,;]/g, match => `\\${match}`).replace(/\n/g, "\\n");
  const ics = [
    "BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//Rawuh//Undangan//ID", "BEGIN:VEVENT",
    `UID:${range.start}-${Math.random().toString(36).slice(2)}@rawuh.id`,
    `DTSTAMP:${new Date().toISOString().replace(/[-:]/g, "").replace(/\.\d{3}/, "")}`,
    `DTSTART:${range.start}`, `DTEND:${range.end}`,
    `SUMMARY:${escape(`${event.name} · ${data.couple.bride} & ${data.couple.groom}`)}`,
    `LOCATION:${escape([event.venue, event.address].filter(Boolean).join(", "))}`,
    "END:VEVENT", "END:VCALENDAR",
  ].join("\r\n");
  const url = URL.createObjectURL(new Blob([ics], { type: "text/calendar;charset=utf-8" }));
  const link = Object.assign(document.createElement("a"), { href: url, download: `${event.name.toLowerCase().replace(/\s+/g, "-")}.ics` });
  link.click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}

/* ── Small UI pieces ───────────────────────────────────────────── */

const ICONS = {
  calendar: "M8 2v4M16 2v4M3 10h18M5 4h14a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2Z",
  play: "M8 5v14l11-7Z",
  live: "M4.9 19.1a10 10 0 0 1 0-14.2M7.8 16.2a6 6 0 0 1 0-8.4M16.2 7.8a6 6 0 0 1 0 8.4M19.1 4.9a10 10 0 0 1 0 14.2M12 12h.01",
  shirt: "M20.4 6.6 16 4a4 4 0 0 1-8 0L3.6 6.6a1 1 0 0 0-.5 1.2l1.4 4.2a1 1 0 0 0 1.2.6L8 12v8a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1v-8l2.3.6a1 1 0 0 0 1.2-.6l1.4-4.2a1 1 0 0 0-.5-1.2Z",
  gift: "M20 12v9H4v-9M2 7h20v5H2zM12 22V7M12 7H7.5a2.5 2.5 0 0 1 0-5C11 2 12 7 12 7ZM12 7h4.5a2.5 2.5 0 0 0 0-5C13 2 12 7 12 7Z",
  pin: "M20 10c0 5-8 12-8 12s-8-7-8-12a8 8 0 0 1 16 0ZM12 13a3 3 0 1 0 0-6 3 3 0 0 0 0 6Z",
  check: "M20 6 9 17l-5-5",
  link: "M7 17 17 7M8 7h9v9",
  heart: "M19 14c1.5-1.5 3-3.2 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.8 0-3 .5-4.5 2-1.5-1.5-2.7-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4 3 5.5l7 7Z",
};

function Glyph({ d, size = 16 }: { d: string; size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.8} strokeLinecap="round" strokeLinejoin="round" aria-hidden="true" focusable="false">
      <path d={d} />
    </svg>
  );
}

function Block({ id, title, eyebrow, children, className }: { id: string; title: string; eyebrow?: string; children: ReactNode; className?: string }) {
  return (
    <section className={`${x.block} ${className ?? ""}`} aria-labelledby={id}>
      {eyebrow && <p className={x.eyebrow}>{eyebrow}</p>}
      <h2 id={id} className={x.title}>{title}</h2>
      {children}
    </section>
  );
}

/* ── Blocks ─────────────────────────────────────────────────────── */

function QuoteBlock({ quote }: { quote: NonNullable<InvitationExtras["quote"]> }) {
  if (!quote.text?.trim()) return null;
  return (
    <section className={`${x.block} ${x.quote}`} aria-label="Kutipan pembuka">
      <span className={x.quoteMark} aria-hidden>“</span>
      <blockquote>
        <p>{quote.text}</p>
        {quote.source && <cite>{quote.source}</cite>}
      </blockquote>
    </section>
  );
}

function ChildBlock({ child, label }: { child: NonNullable<InvitationExtras["child"]>; label?: string }) {
  if (!child.name?.trim()) return null;
  return (
    <Block id="extra-child" title={child.name} eyebrow={label ? `${label} untuk` : "Dengan penuh syukur"} className={x.center}>
      {child.photo && /^(https?:)?\//.test(child.photo) && (
        // eslint-disable-next-line @next/next/no-img-element
        <img className={x.childPhoto} src={child.photo} alt={`Foto ${child.nickname || child.name}`} loading="lazy" />
      )}
      {child.nickname && <p className={x.lead}>“{child.nickname}”</p>}
      {child.birthDate && <p className={x.muted}>Lahir {fmt(child.birthDate, { weekday: "long", day: "numeric", month: "long", year: "numeric" })}</p>}
      {child.meaning && <p className={x.body}>{child.meaning}</p>}
      {child.parents && <p className={x.muted}>{child.parents}</p>}
    </Block>
  );
}

function CalendarBlock({ data }: { data: InvitationData }) {
  const events = data.events.filter(event => toDate(event.date));
  if (!events.length) return null;
  return (
    <Block id="extra-calendar" title="Simpan tanggalnya" eyebrow="Jangan sampai lupa">
      <ul className={x.list}>
        {events.map(event => (
          <li key={event.name + event.date} className={`${x.card} ${x.calCard}`}>
            <span className={x.icon}><Glyph d={ICONS.calendar} /></span>
            <div className={x.cardText}>
              <strong>{event.name}</strong>
              <small>{fmt(event.date, { weekday: "long", day: "numeric", month: "long" })}{event.time ? ` · ${event.time}` : ""}</small>
            </div>
            <div className={x.actions}>
              <a className={x.chip} href={googleCalendarHref(data, event)} target="_blank" rel="noreferrer">Google</a>
              <button type="button" className={x.chip} onClick={() => downloadIcs(data, event)}>iPhone/Outlook</button>
            </div>
          </li>
        ))}
      </ul>
    </Block>
  );
}

function RundownBlock({ rundown }: { rundown: NonNullable<InvitationExtras["rundown"]> }) {
  const items = rundown.items?.filter(item => item.title?.trim()) ?? [];
  if (!items.length) return null;
  return (
    <Block id="extra-rundown" title="Susunan acara" eyebrow="Rundown">
      <ol className={x.timeline}>
        {items.map((item, index) => (
          <li key={index}>
            <time>{item.time}</time>
            <div><strong>{item.title}</strong>{item.note && <small>{item.note}</small>}</div>
          </li>
        ))}
      </ol>
    </Block>
  );
}

function DressCodeBlock({ dress }: { dress: NonNullable<InvitationExtras["dressCode"]> }) {
  if (!dress.note?.trim() && !dress.colors?.length) return null;
  const colors = (dress.colors ?? []).filter(color => /^#[0-9a-f]{3,8}$/i.test(color)).slice(0, 6);
  return (
    <Block id="extra-dress" title="Dress code" eyebrow="Busana" className={x.center}>
      {colors.length > 0 && (
        <div className={x.swatches} role="list" aria-label="Palet warna busana">
          {colors.map(color => <span key={color} role="listitem" style={{ background: color }} title={color} aria-label={`Warna ${color}`} />)}
        </div>
      )}
      {dress.note && <p className={x.body}>{dress.note}</p>}
    </Block>
  );
}

function LivestreamBlock({ live }: { live: NonNullable<InvitationExtras["livestream"]> }) {
  const url = /^https?:\/\//i.test(live.url ?? "") ? live.url : undefined;
  if (!url) return null;
  const platform = live.platform || (/youtu/i.test(url) ? "YouTube" : /instagram/i.test(url) ? "Instagram Live" : /zoom/i.test(url) ? "Zoom" : "Live streaming");
  return (
    <Block id="extra-live" title="Saksikan secara virtual" eyebrow="Live streaming" className={x.center}>
      <p className={x.body}>{live.note || "Tidak bisa hadir? Ikuti momen bahagia kami secara langsung."}</p>
      <div className={x.liveCard}>
        <span className={x.liveDot} aria-hidden><Glyph d={ICONS.live} size={18} /></span>
        <div className={x.cardText}>
          <strong>{platform}</strong>
          {live.startsAt && <small>{fmt(live.startsAt, { weekday: "long", day: "numeric", month: "long", hour: "2-digit", minute: "2-digit" })} WIB</small>}
        </div>
      </div>
      <a className={x.button} href={url} target="_blank" rel="noreferrer"><Glyph d={ICONS.play} /> Tonton siaran</a>
    </Block>
  );
}

/** "12" → "Meja 12"; free-form labels ("VIP A", "Meja Keluarga") are shown as written. */
export function tableLabel(table?: string) {
  const value = table?.trim();
  if (!value) return "";
  return /^\d/.test(value) ? `Meja ${value}` : value;
}

function GuestPassBlock({ pass, guestToken, guestName, guestTable, demo }: { pass: NonNullable<InvitationExtras["guestPass"]>; guestToken?: string; guestName?: string; guestTable?: string; demo?: boolean }) {
  const token = guestToken || (demo ? "demo-tamu" : undefined);
  const [src, setSrc] = useState("");
  useEffect(() => {
    if (!token) return;
    QRCode.toDataURL(`rawuh:${token}`, { width: 360, margin: 1 }).then(setSrc).catch(() => undefined);
  }, [token]);
  if (!token) return null;
  return (
    <Block id="extra-pass" title="Kartu masuk tamu" eyebrow="QR check-in" className={x.center}>
      <div className={x.pass}>
        {/* eslint-disable-next-line @next/next/no-img-element */}
        {src ? <img src={src} alt="Kode QR check-in" width={180} height={180} /> : <span className={x.qrPlaceholder} aria-hidden />}
        {guestName && <strong>{guestName}</strong>}
        {guestTable && <span className={x.table}>{tableLabel(guestTable)}</span>}
        <small>{pass.note || "Tunjukkan kode ini ke penerima tamu saat tiba di lokasi."}</small>
      </div>
    </Block>
  );
}

function videoEmbed(url: string) {
  const yt = url.match(/(?:youtube\.com\/(?:watch\?v=|shorts\/|embed\/)|youtu\.be\/)([\w-]{6,})/i);
  if (yt) return { kind: "iframe" as const, src: `https://www.youtube-nocookie.com/embed/${yt[1]}?rel=0` };
  const vimeo = url.match(/vimeo\.com\/(\d+)/i);
  if (vimeo) return { kind: "iframe" as const, src: `https://player.vimeo.com/video/${vimeo[1]}` };
  if (/\.(mp4|webm)(\?|$)/i.test(url)) return { kind: "video" as const, src: url };
  return { kind: "link" as const, src: url };
}

function VideoBlock({ video }: { video: NonNullable<InvitationExtras["video"]> }) {
  if (!/^https?:\/\//i.test(video.url ?? "")) return null;
  const embed = videoEmbed(video.url);
  return (
    <Block id="extra-video" title={video.title || "Video kami"} eyebrow="Film pendek" className={x.center}>
      {embed.kind === "iframe" && (
        <div className={x.video}><iframe src={embed.src} title={video.title || "Video undangan"} loading="lazy" allow="accelerometer; encrypted-media; picture-in-picture; fullscreen" allowFullScreen /></div>
      )}
      {embed.kind === "video" && <div className={x.video}><video src={embed.src} controls playsInline preload="metadata" /></div>}
      {embed.kind === "link" && <a className={x.button} href={embed.src} target="_blank" rel="noreferrer"><Glyph d={ICONS.play} /> Putar video</a>}
    </Block>
  );
}

function FamilyBlock({ family }: { family: NonNullable<InvitationExtras["family"]> }) {
  const names = family.names?.map(name => name.trim()).filter(Boolean) ?? [];
  if (!names.length) return null;
  return (
    <Block id="extra-family" title={family.title || "Turut mengundang"} className={x.center}>
      <ul className={x.family}>{names.map(name => <li key={name}>{name}</li>)}</ul>
    </Block>
  );
}

function TravelBlock({ travel }: { travel: NonNullable<InvitationExtras["travel"]> }) {
  const items = travel.items?.filter(item => item.name?.trim()) ?? [];
  if (!items.length && !travel.note?.trim()) return null;
  return (
    <Block id="extra-travel" title="Info tamu luar kota" eyebrow="Akomodasi & transportasi">
      {travel.note && <p className={x.body}>{travel.note}</p>}
      {items.length > 0 && (
        <ul className={x.list}>
          {items.map(item => {
            const href = /^https?:\/\//i.test(item.url ?? "") ? item.url : undefined;
            const inner = <>
              <span className={x.icon}><Glyph d={ICONS.pin} /></span>
              <div className={x.cardText}><strong>{item.name}</strong>{item.detail && <small>{item.detail}</small>}</div>
              {href && <span className={x.arrow}><Glyph d={ICONS.link} size={14} /></span>}
            </>;
            return <li key={item.name}>{href ? <a className={x.card} href={href} target="_blank" rel="noreferrer">{inner}</a> : <div className={x.card}>{inner}</div>}</li>;
          })}
        </ul>
      )}
    </Block>
  );
}

function WishlistBlock({ wishlist, slug, demo, guestName }: { wishlist: NonNullable<InvitationExtras["wishlist"]>; slug: string; demo?: boolean; guestName?: string }) {
  const [items, setItems] = useState<WishlistItem[]>(() => wishlist.items?.filter(item => item.name?.trim()) ?? []);
  const [claiming, setClaiming] = useState<string | null>(null);
  const [error, setError] = useState("");
  if (!items.length) return null;

  async function claim(item: WishlistItem) {
    const fallback = guestName && guestName !== "Tamu Undangan" ? guestName : "";
    const name = window.prompt("Nama kamu (agar kado tidak dobel):", fallback)?.trim();
    if (!name) return;
    setError("");
    setClaiming(item.id);
    try {
      if (!demo) {
        const response = await fetch(`${API}/api/public/invitation/${encodeURIComponent(slug)}/wishlist/claim`, {
          method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ item_id: item.id, name: name.slice(0, 60) }),
        });
        if (response.status === 409) {
          setError(`${item.name} sudah dipilih tamu lain.`);
          setItems(current => current.map(entry => entry.id === item.id ? { ...entry, claimed_by: entry.claimed_by || "tamu lain" } : entry));
          return;
        }
        if (!response.ok) throw new Error();
      }
      setItems(current => current.map(entry => entry.id === item.id ? { ...entry, claimed_by: name } : entry));
    } catch {
      setError("Belum tersimpan. Coba lagi sebentar lagi.");
    } finally {
      setClaiming(null);
    }
  }

  return (
    <Block id="extra-wishlist" title="Wishlist kado" eyebrow="Kalau ingin memberi">
      <p className={x.body}>{wishlist.note || "Tandai kado yang akan kamu berikan supaya tidak ada yang dobel."}</p>
      <ul className={x.list}>
        {items.map(item => {
          const href = /^https?:\/\//i.test(item.url ?? "") ? item.url : undefined;
          const image = /^https?:\/\//i.test(item.image ?? "") || item.image?.startsWith("/") ? item.image : undefined;
          return (
            <li key={item.id} className={x.card} data-claimed={item.claimed_by ? "" : undefined}>
              {/* eslint-disable-next-line @next/next/no-img-element */}
              {image ? <img className={x.thumb} src={image} alt="" loading="lazy" /> : <span className={x.icon}><Glyph d={ICONS.gift} /></span>}
              <div className={x.cardText}>
                <strong>{href ? <a href={href} target="_blank" rel="noreferrer">{item.name}</a> : item.name}</strong>
                <small>{item.claimed_by ? `Dipilih oleh ${item.claimed_by}` : item.price || "Belum ada yang memilih"}</small>
              </div>
              {item.claimed_by
                ? <span className={x.done}><Glyph d={ICONS.check} size={14} /> Dipilih</span>
                : <button type="button" className={x.chip} disabled={claiming !== null} onClick={() => claim(item)}>{claiming === item.id ? "Menyimpan…" : "Saya belikan"}</button>}
            </li>
          );
        })}
      </ul>
      {error && <p className={x.error} role="alert">{error}</p>}
    </Block>
  );
}

/* ── Online envelope (paid through Rawuh / Mayar) ──────────────────── */

const rupiah = (value: number) => `Rp${Math.round(value).toLocaleString("id-ID")}`;
const PRESETS = [50000, 100000, 200000, 500000];
const GIFT_REF_KEY = "rawuh_gift_ref";
const PAYMENT_HOSTS = [/\.myr\.id$/, /(^|\.)mayar\.id$/, /(^|\.)mayar\.io$/];

function storeRef(slug: string, ref: string) {
  try { sessionStorage.setItem(GIFT_REF_KEY, JSON.stringify({ slug, ref })); } catch { /* storage unavailable */ }
}
function readRef(slug: string): string | null {
  try {
    const saved = JSON.parse(sessionStorage.getItem(GIFT_REF_KEY) ?? "null") as { slug?: string; ref?: string } | null;
    return saved?.slug === slug && saved.ref ? saved.ref : null;
  } catch { return null; }
}

function OnlineGiftBlock({ gift, slug, demo, guestName }: { gift: OnlineGift; slug: string; demo?: boolean; guestName?: string }) {
  const [preset, setPreset] = useState<number | null>(PRESETS[1]);
  const [custom, setCustom] = useState("");
  const [name, setName] = useState(guestName && guestName !== "Tamu Undangan" ? guestName : "");
  const [message, setMessage] = useState("");
  const [sending, setSending] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState<{ state: "checking" | "confirmed" | "pending" | "failed"; amount?: number } | null>(null);

  // Back from Mayar (?amplop=selesai): confirm the payment we started in this tab.
  useEffect(() => {
    if (demo || new URLSearchParams(window.location.search).get("amplop") !== "selesai") return;
    const ref = readRef(slug);
    if (!ref) return;
    let cancelled = false;
    const run = async () => {
      setResult({ state: "checking" });
      for (let attempt = 0; attempt < 6 && !cancelled; attempt++) {
        if (attempt) await new Promise(resolve => setTimeout(resolve, 2500));
        try {
          const response = await fetch(`${API}/api/public/gift-transactions/${encodeURIComponent(ref)}/verify`, { method: "POST" });
          const body = await response.json() as { status?: string; amount?: number };
          if (body.status === "confirmed") { if (!cancelled) setResult({ state: "confirmed", amount: body.amount }); return; }
          if (body.status === "failed") { if (!cancelled) setResult({ state: "failed" }); return; }
        } catch { /* retry */ }
      }
      if (!cancelled) setResult({ state: "pending" });
    };
    void run();
    document.getElementById("extra-amplop")?.scrollIntoView({ block: "center" });
    return () => { cancelled = true; };
  }, [slug, demo]);

  const amount = preset ?? Number(custom.replace(/\D/g, ""));
  const valid = amount >= gift.minAmount && amount <= gift.maxAmount && name.trim().length > 0;

  async function send(event: React.FormEvent) {
    event.preventDefault();
    if (!valid) {
      setError(name.trim() ? `Nominal antara ${rupiah(gift.minAmount)} dan ${rupiah(gift.maxAmount)}.` : "Isi nama kamu dulu.");
      return;
    }
    setError("");
    if (demo) { setResult({ state: "confirmed", amount }); return; }
    setSending(true);
    try {
      const url = new URL(window.location.href);
      url.searchParams.set("amplop", "selesai");
      url.hash = "";
      const response = await fetch(`${API}/api/public/invitation/${encodeURIComponent(slug)}/gift-transactions`, {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ sender_name: name.trim().slice(0, 80), message: message.trim().slice(0, 500), amount, return_url: url.href }),
      });
      const body = await response.json() as { reference?: string; payment_url?: string; error?: string };
      if (!response.ok || !body.payment_url || !body.reference) throw new Error(body.error);
      const target = new URL(body.payment_url, window.location.origin);
      const trusted = target.origin === window.location.origin || (target.protocol === "https:" && PAYMENT_HOSTS.some(p => p.test(target.hostname)));
      if (!trusted) throw new Error();
      storeRef(slug, body.reference);
      window.location.assign(target.href);
    } catch {
      setError("Pembayaran belum bisa dibuka. Coba lagi sebentar lagi.");
      setSending(false);
    }
  }

  if (result && result.state !== "checking") {
    return (
      <Block id="extra-amplop" title={result.state === "confirmed" ? "Terima kasih 🤍" : result.state === "failed" ? "Pembayaran dibatalkan" : "Menunggu pembayaran"} eyebrow="Amplop online" className={x.center}>
        <p className={x.body}>
          {result.state === "confirmed"
            ? `Amplop${result.amount ? ` ${rupiah(result.amount)}` : ""} sudah kami terima dan akan diteruskan ke kedua mempelai.${demo ? " (Demo — tidak ada pembayaran.)" : ""}`
            : result.state === "failed"
              ? "Pembayaran kedaluwarsa atau dibatalkan. Kamu bisa mencoba lagi."
              : "Kalau kamu sudah membayar, konfirmasinya biasanya masuk dalam beberapa menit. Tidak perlu membayar ulang."}
        </p>
        {result.state !== "confirmed" && <button type="button" className={x.chip} onClick={() => setResult(null)}>Kirim amplop lagi</button>}
      </Block>
    );
  }

  return (
    <Block id="extra-amplop" title="Kirim amplop online" eyebrow="Tanda kasih">
      <p className={x.body}>{gift.note?.trim() || "Bayar lewat QRIS, transfer bank, atau e-wallet. Amplop diteruskan Rawuh ke kedua mempelai."}</p>
      {result?.state === "checking" ? <p className={x.muted} role="status">Memeriksa pembayaranmu…</p> : (
        <form className={x.giftForm} onSubmit={send}>
          <div className={x.presets} role="group" aria-label="Nominal">
            {PRESETS.filter(value => value >= gift.minAmount && value <= gift.maxAmount).map(value => (
              <button key={value} type="button" className={x.chip} aria-pressed={preset === value} onClick={() => { setPreset(value); setCustom(""); }}>{rupiah(value)}</button>
            ))}
            <button type="button" className={x.chip} aria-pressed={preset === null} onClick={() => setPreset(null)}>Lainnya</button>
          </div>
          {preset === null && (
            <label className={x.field}><span>Nominal (Rp)</span>
              <input inputMode="numeric" autoFocus value={custom} placeholder={String(gift.minAmount)} onChange={e => setCustom(e.target.value.replace(/[^\d.]/g, ""))} />
            </label>
          )}
          <label className={x.field}><span>Nama pengirim</span><input value={name} maxLength={80} onChange={e => setName(e.target.value)} placeholder="Nama kamu" /></label>
          <label className={x.field}><span>Ucapan (opsional)</span><textarea rows={2} maxLength={500} value={message} onChange={e => setMessage(e.target.value)} /></label>
          {error && <p className={x.error} role="alert">{error}</p>}
          <button type="submit" className={x.button} disabled={sending}>{sending ? "Membuka pembayaran…" : `Kirim ${amount >= gift.minAmount ? rupiah(amount) : "amplop"}`}</button>
          <p className={x.muted}>Pembayaran diproses aman oleh Mayar.</p>
        </form>
      )}
    </Block>
  );
}

function FaqBlock({ faq }: { faq: NonNullable<InvitationExtras["faq"]> }) {
  const items = faq.items?.filter(item => item.q?.trim() && item.a?.trim()) ?? [];
  if (!items.length) return null;
  return (
    <Block id="extra-faq" title="Yang sering ditanyakan" eyebrow="FAQ">
      <div className={x.faq}>
        {items.map((item, index) => (
          <details key={index}>
            <summary>{item.q}</summary>
            <p>{item.a}</p>
          </details>
        ))}
      </div>
    </Block>
  );
}

/* ── Slots ──────────────────────────────────────────────────────── */

export type ExtrasSlot = "opening" | "event" | "story" | "end";

/**
 * Renders the extra sections that belong in one part of the page:
 * - opening: quote, child profile (after the hero / couple intro)
 * - event:   save-the-date, rundown, dress code, live streaming, guest QR (after the events)
 * - story:   video, turut mengundang (after the story / gallery)
 * - end:     travel info, wishlist, FAQ (before RSVP / wishes / closing)
 */
export function Extras({ slot, className, without = [] }: {
  slot: ExtrasSlot; className?: string;
  /** Blocks the theme already renders itself, e.g. ["calendar"] when it has its own save-the-date button. */
  without?: Array<"calendar" | "quote">;
}) {
  const ctx = useInvitation();
  const content = useMemo(() => {
    if (!ctx) return null;
    const { data, slug, guestToken, demo } = ctx;
    const e = data.extras;
    const quote = on(e, "quote"), child = on(e, "child"), rundown = on(e, "rundown"), dress = on(e, "dressCode");
    const live = on(e, "livestream"), pass = on(e, "guestPass"), video = on(e, "video"), family = on(e, "family");
    const travel = on(e, "travel"), wishlist = on(e, "wishlist"), faq = on(e, "faq");
    const calendar = e?.calendar?.enabled !== false && !without.includes("calendar");
    switch (slot) {
      case "opening":
        return <>{quote && !without.includes("quote") && <QuoteBlock quote={quote} />}{child && <ChildBlock child={child} label={data.eventLabel} />}</>;
      case "event":
        return <>
          {calendar && <CalendarBlock data={data} />}
          {rundown && <RundownBlock rundown={rundown} />}
          {dress && <DressCodeBlock dress={dress} />}
          {live && <LivestreamBlock live={live} />}
          {pass && <GuestPassBlock pass={pass} guestToken={guestToken} guestName={data.guestName} guestTable={data.guestTable} demo={demo} />}
        </>;
      case "story":
        return <>{video && <VideoBlock video={video} />}{family && <FamilyBlock family={family} />}</>;
      case "end":
        return <>
          {travel && <TravelBlock travel={travel} />}
          {data.onlineGift && <OnlineGiftBlock gift={data.onlineGift} slug={slug} demo={demo} guestName={data.guestName} />}
          {wishlist && <WishlistBlock wishlist={wishlist} slug={slug} demo={demo} guestName={data.guestName} />}
          {faq && <FaqBlock faq={faq} />}
        </>;
    }
  }, [ctx, slot, without]);
  if (!content) return null;
  return <div className={`${x.slot} ${className ?? ""}`} data-extras={slot}>{content}</div>;
}

/** Banner shown at the top of the page in thank-you mode (rendered by ThemeShell). */
export function ThankYouBanner() {
  const thanks = useThankYou();
  const ctx = useInvitation();
  if (!thanks.active || !ctx) return null;
  return (
    <section className={x.thanks} aria-label="Ucapan terima kasih">
      <span className={x.thanksIcon} aria-hidden><Glyph d={ICONS.heart} size={18} /></span>
      <p className={x.eyebrow}>Acara telah berlangsung</p>
      <h2 className={x.title}>Terima kasih</h2>
      <p className={x.body}>{thanks.message}</p>
      <p className={x.muted}>— {ctx.data.couple.bride} &amp; {ctx.data.couple.groom}</p>
    </section>
  );
}

/** Optional RSVP question; renders nothing unless enabled from the dashboard. */
export function DietaryField({ className, inputClassName }: { className?: string; inputClassName?: string }) {
  const ctx = useInvitation();
  const dietary = ctx?.data.extras?.rsvpDietary;
  if (!dietary || dietary.enabled === false) return null;
  return (
    <label className={className ?? x.dietary}>
      {dietary.label || "Alergi / pantangan makanan (opsional)"}
      <input name="diet" maxLength={120} placeholder="mis. alergi kacang, vegetarian" className={inputClassName} />
    </label>
  );
}
