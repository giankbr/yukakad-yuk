"use client";
// Optional "extra" sections shared by every Rawuh theme (quote, livestream, dress code, rundown, FAQ, …).
// Themes drop <Extras slot="…" /> where each group fits their layout; the blocks read the invitation from
// <InvitationProvider> and style themselves from the surrounding colour (currentColor) plus the theme's
// --t-* tokens, so they look native on light and dark themes alike.
import { createContext, useContext, useEffect, useMemo, useState, type ReactNode } from "react";
import { createPortal } from "react-dom";
import QRCode from "qrcode";
import type { InvitationData, InvitationExtras, OnlineGift, WishlistItem } from "../types";
import x from "./extras.module.css";

const API = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8080";
const TZ = "Asia/Jakarta";

type Ctx = { data: InvitationData; slug: string; guestToken?: string; demo?: boolean; /** Theme id, drives the motion personality. */ theme?: string };
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
  text: "M4 7V4h16v3M9 20h6M12 4v16",
  speaker: "M11 5 6 9H2v6h4l5 4V5ZM15.5 8.5a5 5 0 0 1 0 7M19 5a10 10 0 0 1 0 14",
  stop: "M6 6h12v12H6z",
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

function WishlistBlock({ wishlist, slug, demo, guestName, online, funds }: { wishlist: NonNullable<InvitationExtras["wishlist"]>; slug: string; demo?: boolean; guestName?: string; online?: OnlineGift; funds?: Record<string, number> }) {
  const [items, setItems] = useState<WishlistItem[]>(() => wishlist.items?.filter(item => item.name?.trim()) ?? []);
  const [claiming, setClaiming] = useState<string | null>(null);
  const [error, setError] = useState("");
  const [chipIn, setChipIn] = useState<string | null>(null);
  const [chipAmount, setChipAmount] = useState(100000);
  const [chipName, setChipName] = useState(guestName && guestName !== "Tamu Undangan" ? guestName : "");
  const [paying, setPaying] = useState(false);
  const knownName = guestName && guestName !== "Tamu Undangan" ? guestName : "";
  const [claimOpen, setClaimOpen] = useState<string | null>(null);
  const [claimName, setClaimName] = useState(knownName);
  const [claimError, setClaimError] = useState("");
  if (!items.length) return null;


  function openClaim(item: WishlistItem) {
    setClaimOpen(item.id);
    setClaimName(current => current || knownName);
    setClaimError("");
    setError("");
  }

  async function claim(event: React.FormEvent, item: WishlistItem) {
    event.preventDefault();
    const name = claimName.trim().slice(0, 60);
    if (!name) { setClaimError("Isi nama kamu dulu."); return; }
    setClaimError("");
    setError("");
    setClaiming(item.id);
    try {
      if (!demo) {
        const response = await fetch(`${API}/api/public/invitation/${encodeURIComponent(slug)}/wishlist/claim`, {
          method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ item_id: item.id, name }),
        });
        if (response.status === 409) {
          setClaimOpen(null);
          setError(`${item.name} sudah dipilih tamu lain.`);
          setItems(current => current.map(entry => entry.id === item.id ? { ...entry, claimed_by: entry.claimed_by || "tamu lain" } : entry));
          return;
        }
        if (!response.ok) throw new Error();
      }
      setItems(current => current.map(entry => entry.id === item.id ? { ...entry, claimed_by: name } : entry));
      setClaimOpen(null);
    } catch {
      setClaimError("Belum tersimpan. Periksa koneksi lalu coba lagi.");
    } finally {
      setClaiming(null);
    }
  }

  async function contribute(event: React.FormEvent, item: WishlistItem) {
    event.preventDefault();
    if (!chipName.trim()) { setError("Isi nama kamu dulu."); return; }
    if (online && (chipAmount < online.minAmount || chipAmount > online.maxAmount)) { setError(`Nominal minimal ${rupiah(online.minAmount)}.`); return; }
    setError("");
    if (demo) { setChipIn(null); return; }
    setPaying(true);
    const failure = await startOnlinePayment(slug, { sender_name: chipName.trim().slice(0, 80), amount: chipAmount, wishlist_item_id: item.id, message: `Patungan ${item.name}` });
    if (failure) { setError(failure); setPaying(false); }
  }

  return (
    <Block id="extra-wishlist" title="Wishlist kado" eyebrow="Kalau ingin memberi">
      <p className={x.body}>{wishlist.note || "Tandai kado yang akan kamu berikan supaya tidak ada yang dobel."}</p>
      <ul className={x.list}>
        {items.map(item => {
          const href = /^https?:\/\//i.test(item.url ?? "") ? item.url : undefined;
          const image = /^https?:\/\//i.test(item.image ?? "") || item.image?.startsWith("/") ? item.image : undefined;
          const fundable = Boolean(item.fund && item.target && online);
          if (fundable) {
            const collected = funds?.[item.id] ?? 0;
            const percent = Math.min(100, Math.round((collected / item.target!) * 100));
            return (
              <li key={item.id} className={`${x.card} ${x.fundCard}`}>
                <div className={x.fundTop}>
                  {/* eslint-disable-next-line @next/next/no-img-element */}
                  {image ? <img className={x.thumb} src={image} alt="" loading="lazy" /> : <span className={x.icon}><Glyph d={ICONS.gift} /></span>}
                  <div className={x.cardText}>
                    <strong>{href ? <a href={href} target="_blank" rel="noreferrer">{item.name}</a> : item.name}</strong>
                    <small>Patungan · {rupiah(collected)} dari {rupiah(item.target!)}</small>
                  </div>
                  {percent >= 100
                    ? <span className={x.done}><Glyph d={ICONS.check} size={14} /> Terkumpul</span>
                    : <button type="button" className={x.chip} onClick={() => setChipIn(chipIn === item.id ? null : item.id)}>Ikut patungan</button>}
                </div>
                <div className={x.progress} role="progressbar" aria-valuemin={0} aria-valuemax={100} aria-valuenow={percent} aria-label={`${percent}% terkumpul`}><i style={{ width: `${percent}%` }} /></div>
                {chipIn === item.id && (
                  <form className={x.giftForm} onSubmit={e => contribute(e, item)}>
                    <div className={x.presets} role="group" aria-label="Nominal patungan">
                      {[50000, 100000, 250000, 500000].map(value => <button key={value} type="button" className={x.chip} aria-pressed={chipAmount === value} onClick={() => setChipAmount(value)}>{rupiah(value)}</button>)}
                    </div>
                    <label className={x.field}><span>Nama kamu</span><input value={chipName} maxLength={80} onChange={e => setChipName(e.target.value)} /></label>
                    <button type="submit" className={x.button} disabled={paying}>{paying ? "Membuka pembayaran…" : `Patungan ${rupiah(chipAmount)}`}</button>
                  </form>
                )}
              </li>
            );
          }
          const open = claimOpen === item.id && !item.claimed_by;
          const busy = claiming === item.id;
          return (
            <li key={item.id} className={`${x.card} ${x.fundCard}`} data-claimed={item.claimed_by ? "" : undefined}>
              <div className={x.fundTop}>
                {/* eslint-disable-next-line @next/next/no-img-element */}
                {image ? <img className={x.thumb} src={image} alt="" loading="lazy" /> : <span className={x.icon}><Glyph d={ICONS.gift} /></span>}
                <div className={x.cardText}>
                  <strong>{href ? <a href={href} target="_blank" rel="noreferrer">{item.name}</a> : item.name}</strong>
                  <small>{item.claimed_by ? `Dipilih oleh ${item.claimed_by}` : item.price || "Belum ada yang memilih"}</small>
                </div>
                {item.claimed_by
                  ? <span className={x.done}><Glyph d={ICONS.check} size={14} /> Dipilih</span>
                  : !open && <button type="button" className={x.chip} disabled={claiming !== null} onClick={() => openClaim(item)}>Saya belikan</button>}
              </div>
              {open && (
                <form className={x.giftForm} onSubmit={e => claim(e, item)} aria-label={`Pilih ${item.name}`}>
                  <label className={x.field}><span>Nama kamu</span>
                    <input value={claimName} maxLength={60} required autoComplete="name" autoFocus placeholder="Nama kamu" disabled={busy}
                      onChange={e => setClaimName(e.target.value)} />
                  </label>
                  <p className={x.muted}>Namamu akan terlihat oleh tamu lain supaya kado tidak dobel.</p>
                  {claimError && <p className={x.error} role="alert">{claimError}</p>}
                  <div className={x.claimActions}>
                    <button type="button" className={x.chip} disabled={busy} onClick={() => { setClaimOpen(null); setClaimError(""); }}>Batal</button>
                    <button type="submit" className={x.button} disabled={busy}>{busy ? "Menyimpan…" : "Simpan"}</button>
                  </div>
                </form>
              )}
            </li>
          );
        })}
      </ul>
      {error && <p className={x.error} role="alert">{error}</p>}
    </Block>
  );
}

/* ── Reading aids (mode orang tua) ─────────────────────────────────── */

const EASY_KEY = "rawuh_easy_read";

function speechText(data: InvitationData) {
  const parts = [`${data.eventLabel || "Undangan"} ${data.couple.bride} dan ${data.couple.groom}.`];
  if (data.guestName && data.guestName !== "Tamu Undangan") parts.push(`Kepada yang terhormat, ${data.guestName}.`);
  if (data.couple.note) parts.push(data.couple.note);
  for (const event of data.events) {
    const when = fmt(event.date, { weekday: "long", day: "numeric", month: "long", year: "numeric" });
    parts.push(`${event.name}: ${when || ""}${event.time ? `, pukul ${event.time.replace(/\./g, " lewat ").replace("WIB", "Waktu Indonesia Barat")}` : ""}. Bertempat di ${event.venue}${event.address ? `, ${event.address}` : ""}.`);
  }
  parts.push("Merupakan suatu kehormatan apabila Bapak, Ibu, dan Saudara berkenan hadir. Terima kasih.");
  return parts.join(" ");
}

/** Floating "Aa" (bigger text) and "Dengarkan" (read the key details aloud) for older guests. */
export function ReadingAids() {
  const ctx = useInvitation();
  const [big, setBig] = useState(false);
  const [speaking, setSpeaking] = useState(false);
  const [canSpeak, setCanSpeak] = useState(false);

  useEffect(() => {
    const timer = setTimeout(() => {
      setCanSpeak(typeof window !== "undefined" && "speechSynthesis" in window);
      try { setBig(localStorage.getItem(EASY_KEY) === "1"); } catch { /* storage unavailable */ }
    }, 0);
    return () => { clearTimeout(timer); window.speechSynthesis?.cancel(); };
  }, []);
  useEffect(() => {
    if (big) document.documentElement.dataset.easyRead = "1";
    else delete document.documentElement.dataset.easyRead;
    try { localStorage.setItem(EASY_KEY, big ? "1" : "0"); } catch { /* storage unavailable */ }
  }, [big]);

  if (!ctx || ctx.data.extras?.easyRead?.enabled === false) return null;

  function toggleSpeech() {
    const synth = window.speechSynthesis;
    if (speaking) { synth.cancel(); setSpeaking(false); return; }
    const utterance = new SpeechSynthesisUtterance(speechText(ctx!.data));
    utterance.lang = "id-ID";
    utterance.rate = 0.9;
    const voice = synth.getVoices().find(v => v.lang?.toLowerCase().startsWith("id"));
    if (voice) utterance.voice = voice;
    utterance.onend = () => setSpeaking(false);
    utterance.onerror = () => setSpeaking(false);
    synth.cancel();
    synth.speak(utterance);
    setSpeaking(true);
  }

  return (
    <div className={x.aids} role="group" aria-label="Bantuan membaca">
      <button type="button" aria-pressed={big} onClick={() => setBig(!big)} aria-label={big ? "Tulisan normal" : "Perbesar tulisan"} title={big ? "Tulisan normal" : "Perbesar tulisan"}><span aria-hidden className={x.aidsText}>A<small>A</small></span></button>
      {canSpeak && <button type="button" aria-pressed={speaking} onClick={toggleSpeech} aria-label={speaking ? "Berhenti membacakan" : "Bacakan undangan"} title={speaking ? "Berhenti membacakan" : "Bacakan undangan"}><Glyph d={speaking ? ICONS.stop : ICONS.speaker} size={18} /></button>}
    </div>
  );
}

/* ── Guest photos ("Foto dari tamu") ───────────────────────────────── */

type GuestPhoto = { id: string; url: string; uploader_name?: string };

/** Downscale big phone photos before upload so they go through quickly on venue Wi-Fi. */
async function shrinkImage(file: File, max = 2000): Promise<Blob> {
  try {
    const bitmap = await createImageBitmap(file);
    const scale = Math.min(1, max / Math.max(bitmap.width, bitmap.height));
    if (scale === 1 && file.size < 2_500_000) return file;
    const canvas = document.createElement("canvas");
    canvas.width = Math.round(bitmap.width * scale);
    canvas.height = Math.round(bitmap.height * scale);
    canvas.getContext("2d")?.drawImage(bitmap, 0, 0, canvas.width, canvas.height);
    return await new Promise<Blob>((resolve) => canvas.toBlob((blob) => resolve(blob ?? file), "image/jpeg", 0.85));
  } catch {
    return file;
  }
}

function GuestPhotosBlock({ slug, demo, guestToken, guestName }: { slug: string; demo?: boolean; guestToken?: string; guestName?: string }) {
  const [photos, setPhotos] = useState<GuestPhoto[]>([]);
  const [name, setName] = useState(guestName && guestName !== "Tamu Undangan" ? guestName : "");
  const [sending, setSending] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    if (demo) return;
    let cancelled = false;
    fetch(`${API}/api/public/invitation/${encodeURIComponent(slug)}/photos`)
      .then(r => r.json())
      .then((body: { items?: GuestPhoto[] }) => { if (!cancelled) setPhotos(body.items ?? []); })
      .catch(() => undefined);
    return () => { cancelled = true; };
  }, [slug, demo]);

  async function upload(files: FileList | null) {
    if (!files?.length) return;
    setError("");
    setMessage("");
    if (demo) { setMessage("Demo: foto tidak benar-benar diunggah."); return; }
    setSending(true);
    let sent = 0;
    let pending = 0;
    try {
      for (const file of Array.from(files).slice(0, 5)) {
        const form = new FormData();
        form.append("file", await shrinkImage(file), "foto.jpg");
        form.append("name", name.trim().slice(0, 60));
        if (guestToken) form.append("guest", guestToken);
        const response = await fetch(`${API}/api/public/invitation/${encodeURIComponent(slug)}/photos`, { method: "POST", body: form });
        const body = await response.json() as { id?: string; url?: string; status?: string; error?: string };
        if (!response.ok) throw new Error(body.error);
        sent++;
        if (body.status === "approved" && body.id && body.url) setPhotos(current => [{ id: body.id!, url: body.url!, uploader_name: name.trim() }, ...current]);
        else pending++;
      }
      setMessage(pending ? `${sent} foto terkirim. Tampil setelah disetujui mempelai.` : `${sent} foto terkirim. Terima kasih!`);
    } catch (err) {
      setError(err instanceof Error && err.message ? err.message : "Foto belum terkirim. Coba lagi.");
      if (sent) setMessage(`${sent} foto terkirim.`);
    } finally {
      setSending(false);
    }
  }

  return (
    <Block id="extra-foto-tamu" title="Foto dari tamu" eyebrow="Bagikan momen">
      <p className={x.body}>Punya foto seru hari ini? Kirim di sini — langsung tampil di undangan dan layar acara.</p>
      <div className={x.giftForm}>
        <label className={x.field}><span>Nama kamu (opsional)</span><input value={name} maxLength={60} onChange={e => setName(e.target.value)} placeholder="Nama kamu" /></label>
        <label className={x.button} style={{ opacity: sending ? 0.7 : 1 }}>
          {sending ? "Mengirim…" : "Kirim foto"}
          <input type="file" accept="image/*" multiple hidden disabled={sending} onChange={e => { void upload(e.target.files); e.target.value = ""; }} />
        </label>
        {message && <p className={x.muted} role="status">{message}</p>}
        {error && <p className={x.error} role="alert">{error}</p>}
      </div>
      {photos.length > 0 && (
        <ul className={x.photoGrid}>
          {photos.slice(0, 30).map(photo => (
            <li key={photo.id}>
              {/* eslint-disable-next-line @next/next/no-img-element */}
              <a href={photo.url} target="_blank" rel="noreferrer"><img src={photo.url} alt={`Foto dari ${photo.uploader_name || "tamu"}`} loading="lazy" /></a>
            </li>
          ))}
        </ul>
      )}
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

/** Create an online envelope and send the guest to Mayar; returns an error message on failure. */
async function startOnlinePayment(slug: string, payload: { sender_name: string; message?: string; amount: number; wishlist_item_id?: string }): Promise<string | null> {
  try {
    const url = new URL(window.location.href);
    url.searchParams.set("amplop", "selesai");
    url.hash = "";
    const response = await fetch(`${API}/api/public/invitation/${encodeURIComponent(slug)}/gift-transactions`, {
      method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ ...payload, return_url: url.href }),
    });
    const body = await response.json() as { reference?: string; payment_url?: string; error?: string };
    if (!response.ok || !body.payment_url || !body.reference) return body.error || "Pembayaran belum bisa dibuka. Coba lagi sebentar lagi.";
    const target = new URL(body.payment_url, window.location.origin);
    const trusted = target.origin === window.location.origin || (target.protocol === "https:" && PAYMENT_HOSTS.some(p => p.test(target.hostname)));
    if (!trusted) return "Alamat pembayaran tidak valid.";
    storeRef(slug, body.reference);
    window.location.assign(target.href);
    return null;
  } catch {
    return "Pembayaran belum bisa dibuka. Coba lagi sebentar lagi.";
  }
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
    const failure = await startOnlinePayment(slug, { sender_name: name.trim().slice(0, 80), message: message.trim().slice(0, 500), amount });
    if (failure) { setError(failure); setSending(false); }
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
  without?: Array<"calendar" | "quote" | "child">;
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
        return <>{quote && !without.includes("quote") && <QuoteBlock quote={quote} />}{child && !without.includes("child") && <ChildBlock child={child} label={data.eventLabel} />}</>;
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
          {e?.guestPhotos?.enabled && <GuestPhotosBlock slug={slug} demo={demo} guestToken={guestToken} guestName={data.guestName} />}
          {data.onlineGift && <OnlineGiftBlock gift={data.onlineGift} slug={slug} demo={demo} guestName={data.guestName} />}
          {wishlist && <WishlistBlock wishlist={wishlist} slug={slug} demo={demo} guestName={data.guestName} online={data.onlineGift} funds={data.wishlistFunds} />}
          {faq && <FaqBlock faq={faq} />}
        </>;
    }
  }, [ctx, slot, without]);
  if (!content) return null;
  return <div className={`${x.slot} ${className ?? ""}`} data-extras={slot}>{content}</div>;
}

/** Banner shown at the top of the page in thank-you mode (rendered by ThemeShell). */
/** Years since the main event when today is its anniversary (Jakarta time), else 0. */
function anniversaryYears(date?: string) {
  const event = toDate(date);
  if (!event) return 0;
  const parts = (d: Date) => new Intl.DateTimeFormat("en-CA", { timeZone: TZ, year: "numeric", month: "2-digit", day: "2-digit" }).format(d).split("-").map(Number);
  const [ey, em, ed] = parts(event);
  const [ty, tm, td] = parts(new Date());
  return tm === em && td === ed && ty > ey ? ty - ey : 0;
}

type Recap = { checked_in: number; attending: number; wishes: number; photos: number };

export function ThankYouBanner() {
  const thanks = useThankYou();
  const ctx = useInvitation();
  const [recap, setRecap] = useState<Recap | null>(null);
  const [years, setYears] = useState(0);
  const [playing, setPlaying] = useState(false);
  const active = thanks.active && Boolean(ctx);
  const slug = ctx?.slug;
  const demo = ctx?.demo;
  const date = ctx?.data.date;
  useEffect(() => {
    if (!active) return;
    const timer = setTimeout(() => setYears(anniversaryYears(date)), 0);
    if (!slug || demo) return () => clearTimeout(timer);
    let cancelled = false;
    fetch(`${API}/api/public/invitation/${encodeURIComponent(slug)}/recap`).then(r => r.json()).then((body: Recap) => { if (!cancelled) setRecap(body); }).catch(() => undefined);
    return () => { cancelled = true; clearTimeout(timer); };
  }, [active, slug, demo, date]);
  if (!thanks.active || !ctx) return null;
  const guests = Math.max(recap?.checked_in ?? 0, recap?.attending ?? 0);
  const stats = [
    guests ? `${guests.toLocaleString("id-ID")} tamu hadir` : "",
    recap?.wishes ? `${recap.wishes.toLocaleString("id-ID")} ucapan & doa` : "",
    recap?.photos ? `${recap.photos.toLocaleString("id-ID")} foto dari tamu` : "",
  ].filter(Boolean);
  return (
    <section className={x.thanks} aria-label={years ? "Hari jadi pernikahan" : "Ucapan terima kasih"}>
      <span className={x.thanksIcon} aria-hidden><Glyph d={ICONS.heart} size={18} /></span>
      <p className={x.eyebrow}>{years ? `Hari jadi ke-${years}` : "Acara telah berlangsung"}</p>
      <h2 className={x.title}>{years ? `${years} tahun bersama` : "Terima kasih"}</h2>
      <p className={x.body}>{years ? "Hari ini, tepat di tanggal yang sama, kalian hadir merayakan awal cerita kami. Terima kasih masih menjadi bagian darinya." : thanks.message}</p>
      <p className={x.muted}>— {ctx.data.couple.bride} &amp; {ctx.data.couple.groom}</p>
      {stats.length > 0 && <ul className={x.recap}>{stats.map(item => <li key={item}>{item}</li>)}</ul>}
      <button type="button" className={x.button} onClick={() => setPlaying(true)}><Glyph d={ICONS.play} size={14} /> Putar kenangan</button>
      {playing && createPortal(<MemoriesPlayer onClose={() => setPlaying(false)} />, document.body)}
    </section>
  );
}

type Slide = { kind: "photo"; url: string; caption?: string } | { kind: "wish"; text: string; name: string };

/** Fullscreen slideshow of the gallery, guest photos and wishes — a keepsake to replay after the event. */
function MemoriesPlayer({ onClose }: { onClose: () => void }) {
  const ctx = useInvitation()!;
  const [slides, setSlides] = useState<Slide[] | null>(null);
  const [index, setIndex] = useState(0);
  const [paused, setPaused] = useState(false);
  useEffect(() => {
    let cancelled = false;
    const base = `${API}/api/public/invitation/${encodeURIComponent(ctx.slug)}`;
    const get = (path: string) => (ctx.demo ? Promise.resolve({ items: [] }) : fetch(base + path).then(r => r.json()).catch(() => ({ items: [] })));
    Promise.all([get("/photos"), get("/wishes")]).then(([photos, wishes]: [{ items?: { url: string; uploader_name?: string }[] }, { items?: { name: string; message: string }[] }]) => {
      if (cancelled) return;
      const pics: Slide[] = [
        ...ctx.data.gallery.map(url => ({ kind: "photo" as const, url })),
        ...(photos.items ?? []).map(p => ({ kind: "photo" as const, url: p.url, caption: p.uploader_name ? `Foto dari ${p.uploader_name}` : undefined })),
      ];
      const words: Slide[] = (wishes.items ?? []).filter(w => w.message?.trim()).map(w => ({ kind: "wish" as const, text: w.message, name: w.name }));
      // Interleave photos and wishes so it plays like a short film.
      const mixed: Slide[] = [];
      for (let i = 0; i < Math.max(pics.length, words.length); i++) {
        if (pics[i]) mixed.push(pics[i]);
        if (words[i]) mixed.push(words[i]);
      }
      setSlides(mixed.length ? mixed : [{ kind: "wish", text: "Terima kasih atas doa dan kehadiranmu.", name: `${ctx.data.couple.bride} & ${ctx.data.couple.groom}` }]);
    });
    return () => { cancelled = true; };
  }, [ctx]);
  useEffect(() => {
    if (!slides || paused) return;
    const timer = setTimeout(() => setIndex(i => (i + 1) % slides.length), slides[index]?.kind === "wish" ? 6500 : 4500);
    return () => clearTimeout(timer);
  }, [slides, index, paused]);
  useEffect(() => {
    const onKey = (event: KeyboardEvent) => {
      if (event.key === "Escape") onClose();
      if (event.key === "ArrowRight" && slides) setIndex(i => (i + 1) % slides.length);
      if (event.key === "ArrowLeft" && slides) setIndex(i => (i - 1 + slides.length) % slides.length);
      if (event.key === " ") { event.preventDefault(); setPaused(p => !p); }
    };
    window.addEventListener("keydown", onKey);
    const previous = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    return () => { window.removeEventListener("keydown", onKey); document.body.style.overflow = previous; };
  }, [onClose, slides]);
  const slide = slides?.[index];
  return (
    <div className={x.player} role="dialog" aria-modal="true" aria-label="Putar kenangan" onClick={() => setPaused(p => !p)}>
      {slide?.kind === "photo" && (
        <figure key={index} className={x.playerPhoto}>
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img src={slide.url} alt="" />
          {slide.caption && <figcaption>{slide.caption}</figcaption>}
        </figure>
      )}
      {slide?.kind === "wish" && (
        <blockquote key={index} className={x.playerWish}><p>{slide.text}</p><cite>— {slide.name}</cite></blockquote>
      )}
      {!slides && <p className={x.muted}>Menyiapkan kenangan…</p>}
      <div className={x.playerBar} onClick={event => event.stopPropagation()}>
        <span>{ctx.data.couple.bride} &amp; {ctx.data.couple.groom}{slides ? ` · ${index + 1}/${slides.length}` : ""}{paused ? " · dijeda" : ""}</span>
        <button type="button" className={x.chip} onClick={onClose}>Tutup</button>
      </div>
      {slides && <div className={x.playerProgress} aria-hidden><i style={{ width: `${((index + 1) / slides.length) * 100}%` }} /></div>}
    </div>
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
