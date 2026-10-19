"use client";
// Theme "Ultah Balon" — pesta ulang tahun anak: balon yang bisa diletuskan, bendera segitiga, kue berlilin, stiker warna-warni.
import { useEffect, useRef, useState, type CSSProperties, type FormEvent } from "react";
import {
  DietaryField, Extras, GuestCount, Lucide, Photo, ThemeShell, Tick, dateParts, formatDate, giftInfo, guestLabel, mapsHref,
  storyItems, toDate, useCopy, useCountdown, DATE_TBA, sentSummary, useRsvp, useThankYou, useWishes, type Attendance, type ThemeProps, type Wish,
} from "../kit";
import type { InvitationData } from "../../types";
import { tableLabel } from "../extras";
import { celebrate, toast } from "@/lib/celebrate";
import { ic } from "./icons";
import s from "./styles.module.css";

const FONTS = ["Nunito:wght@400;600;700;800;900", "Caveat:wght@600;700"];
const COLORS = ["#ff6b6b", "#ffc93c", "#4ecdc4", "#8e7dff", "#ff9f43"];
const ATTEND: Record<Attendance, string> = { yes: "Hadir", maybe: "Masih ragu", no: "Berhalangan" };
const DEMO_WISHES: Wish[] = [
  { id: "w1", name: "Naura & Mama", attendance: "yes", message: "Selamat ulang tahun Arka! Semoga makin pintar, sehat, dan jadi anak yang sholeh. Sampai ketemu di pesta!" },
  { id: "w2", name: "Om Bayu", attendance: "maybe", message: "Happy birthday jagoan! Tetap ceria dan rajin belajar ya." },
];

/* ── Helpers ───────────────────────────────────────────────── */

const jakarta = (d: Date) => new Intl.DateTimeFormat("en-CA", { timeZone: "Asia/Jakarta", year: "numeric", month: "2-digit", day: "2-digit" }).format(d).split("-").map(Number);

/** Age the child turns on the party date (0 when either date is missing). */
function ageAt(birth?: string, at?: string) {
  const b = toDate(birth), a = toDate(at);
  if (!b || !a) return 0;
  const [by, bm, bd] = jakarta(b);
  const [ay, am, ad] = jakarta(a);
  const age = ay - by - (am < bm || (am === bm && ad < bd) ? 1 : 0);
  return age > 0 && age < 120 ? age : 0;
}

function celebrant(data: InvitationData) {
  const child = data.extras?.child?.enabled !== false && data.extras?.child?.name?.trim() ? data.extras.child : undefined;
  const bride = data.couple.bride?.trim() ?? "";
  const groom = data.couple.groom?.trim() ?? "";
  const short = child?.nickname?.trim() || child?.name.trim() || (groom ? `${bride} & ${groom}` : bride) || "Si Kecil";
  const full = child?.name.trim() || [data.couple.brideFull?.trim() || bride, groom ? data.couple.groomFull?.trim() || groom : ""].filter(Boolean).join(" & ") || short;
  return {
    short, full,
    parents: child?.parents?.trim() || data.couple.brideParents?.trim() || "",
    photo: child?.photo || data.couple.bridePhoto,
    birth: child?.birthDate,
    meaning: child?.meaning,
    age: ageAt(child?.birthDate, data.date),
  };
}

function chipDate(value?: string) {
  const p = dateParts(value);
  return p.day ? `${p.weekday}, ${p.day} ${p.month} ${p.year}` : DATE_TBA;
}

function calendarHref(title: string, data: InvitationData) {
  const start = toDate(data.events[0]?.date ?? data.date);
  if (!start) return undefined;
  const stamp = (d: Date) => d.toISOString().replace(/[-:]|\.\d{3}/g, "");
  const params = new URLSearchParams({ action: "TEMPLATE", text: title, dates: `${stamp(start)}/${stamp(new Date(start.getTime() + 3 * 3600e3))}`, location: [data.place, data.address].filter(Boolean).join(", ") });
  return `https://calendar.google.com/calendar/render?${params.toString()}`;
}

function plainName(guest?: string) {
  if (!guest || guest === "Tamu Undangan") return "";
  return guest.replace(/\s*(&|dan)\s*keluarga$/i, "").trim();
}

/* ── Ornaments ─────────────────────────────────────────────── */

function BalloonArt({ color, className }: { color: string; className?: string }) {
  return (
    <svg className={className} viewBox="0 0 60 104" aria-hidden="true" focusable="false">
      <path d="M30 70c-6 8 6 14 0 22s5 10 1 12" fill="none" stroke="#2d2a4a" strokeOpacity=".45" strokeWidth="1.4" strokeLinecap="round" />
      <path d="M30 3c15 0 25 12 25 28 0 18-13 35-25 37C18 66 5 49 5 31 5 15 15 3 30 3z" fill={color} />
      <path d="M30 3c15 0 25 12 25 28 0 18-13 35-25 37" fill="none" stroke="#000" strokeOpacity=".08" strokeWidth="6" />
      <ellipse cx="19" cy="20" rx="4.5" ry="9" fill="#fff" fillOpacity=".45" transform="rotate(-22 19 20)" />
      <path d="M25.5 67.5 30 73l4.5-5.5z" fill={color} />
    </svg>
  );
}

/** Tap a balloon to pop it (purely decorative; it grows back after a moment). */
function Balloons({ count = 5, className }: { count?: number; className?: string }) {
  const [popped, setPopped] = useState<number[]>([]);
  const [total, setTotal] = useState(0);
  const pop = (index: number, element: HTMLElement) => {
    if (popped.includes(index)) return;
    setPopped(list => [...list, index]);
    setTotal(value => value + 1);
    celebrate(element);
    navigator.vibrate?.(12);
    if (total === 0) toast("Dor! Balonnya meletus");
    window.setTimeout(() => setPopped(list => list.filter(item => item !== index)), 2600);
  };
  return (
    <div className={`${s.balloons} ${className ?? ""}`} data-noreveal>
      {Array.from({ length: count }, (_, index) => (
        <button key={index} type="button" className={`${s.balloon} ${popped.includes(index) ? s.popped : ""}`} style={{ "--i": index } as CSSProperties}
          onClick={event => pop(index, event.currentTarget)} aria-label="Letuskan balon">
          <span className={s.bob}><BalloonArt color={COLORS[index % COLORS.length]} /></span>
          <span className={s.burst} aria-hidden><i /><i /><i /><i /><i /><i /></span>
        </button>
      ))}
    </div>
  );
}

function Bunting({ flags = 11 }: { flags?: number }) {
  const w = 360 / flags;
  return (
    <svg className={s.bunting} viewBox="0 0 360 46" preserveAspectRatio="none" aria-hidden="true" focusable="false">
      <path d="M0 6 Q180 30 360 6" fill="none" stroke="#2d2a4a" strokeWidth="1.6" />
      {Array.from({ length: flags }, (_, i) => {
        const x = i * w + 3;
        const sag = (t: number) => 6 + 24 * 4 * (t / 360) * (1 - t / 360) * 0.98;
        const y1 = sag(x), y2 = sag(x + w - 6);
        return <path key={i} d={`M${x} ${y1} L${x + w - 6} ${y2} L${x + (w - 6) / 2} ${(y1 + y2) / 2 + 18} Z`} fill={COLORS[i % COLORS.length]} stroke="#2d2a4a" strokeWidth="1.2" strokeLinejoin="round" />;
      })}
    </svg>
  );
}

function Cake({ candles }: { candles: number }) {
  const n = Math.max(1, Math.min(candles || 1, 9));
  const gap = 96 / (n + 1);
  return (
    <svg className={s.cake} viewBox="0 0 160 150" aria-hidden="true" focusable="false">
      <ellipse cx="80" cy="140" rx="70" ry="7" fill="#2d2a4a" opacity=".12" />
      <rect x="18" y="86" width="124" height="50" rx="10" fill="#ff8fa3" stroke="#2d2a4a" strokeWidth="2.4" />
      <path d="M18 100c10 10 20 10 31 0s20-10 31 0 20 10 31 0 20-10 31 0" fill="none" stroke="#fff" strokeWidth="5" strokeLinecap="round" />
      <rect x="32" y="54" width="96" height="36" rx="9" fill="#ffe08a" stroke="#2d2a4a" strokeWidth="2.4" />
      <path d="M32 66c8 8 16 8 24 0s16-8 24 0 16 8 24 0 16-8 24 0" fill="none" stroke="#fff" strokeWidth="4" strokeLinecap="round" />
      {[40, 62, 84, 106, 124].map((x, i) => <circle key={x} cx={x} cy={i % 2 ? 124 : 118} r="3" fill={COLORS[(i + 2) % COLORS.length]} />)}
      {Array.from({ length: n }, (_, i) => {
        const x = 32 + gap * (i + 1);
        return (
          <g key={i}>
            <rect x={x - 3} y="30" width="6" height="25" rx="2" fill={COLORS[i % COLORS.length]} stroke="#2d2a4a" strokeWidth="1.6" />
            <path className={s.flame} style={{ animationDelay: `${-i * 0.23}s` }} d={`M${x} 14c4 5 5 8 5 10a5 5 0 0 1-10 0c0-2 1-5 5-10z`} fill="#ffb627" stroke="#2d2a4a" strokeWidth="1.2" />
          </g>
        );
      })}
    </svg>
  );
}

function Confetti() {
  return <div className={s.confetti} aria-hidden>{Array.from({ length: 14 }, (_, i) => <i key={i} style={{ "--i": i, background: COLORS[i % COLORS.length] } as CSSProperties} />)}</div>;
}

function Head({ id, kicker, children }: { id: string; kicker?: string; children: string }) {
  return (
    <div className={s.head}>
      {kicker && <p className={s.kicker}>{kicker}</p>}
      <h2 id={id}>{children}</h2>
      <span className={s.squiggle} aria-hidden><svg viewBox="0 0 80 10"><path d="M2 5c6-6 10 6 16 0s10 6 16 0 10 6 16 0 10 6 16 0 8 4 12 0" fill="none" stroke="currentColor" strokeWidth="3" strokeLinecap="round" /></svg></span>
    </div>
  );
}

/* ── Theme ─────────────────────────────────────────────────── */

export default function UltahBalonTheme({ data, slug, guestToken, demo, skipCover }: ThemeProps) {
  const who = celebrant(data);
  const label = data.eventLabel?.trim() || "Ulang Tahun";
  const ageText = who.age ? `ke-${who.age}` : "";
  const countdown = useCountdown(data.date);
  const rsvp = useRsvp({ slug, guestToken, demo });
  const wishes = useWishes({ slug, guestToken, demo, seed: DEMO_WISHES });
  const thanks = useThankYou();
  const rsvpClosed = thanks.active || rsvp.status === "closed";
  const { copy, copied } = useCopy();
  const stories = storyItems(data);
  const gallery = data.gallery.filter(Boolean);
  const [attendance, setAttendance] = useState<Attendance>("yes");
  const maps = mapsHref(data, data.events[0]);
  const calendar = calendarHref(`${label} ${who.short}`, data);
  const table = tableLabel(data.guestTable);
  const sending = rsvp.status === "sending" || wishes.status === "sending";
  const sent = rsvp.status === "sent" || wishes.status === "sent";
  const sentRef = useRef<HTMLDivElement>(null);
  useEffect(() => { if (sent) celebrate(sentRef.current); }, [sent]);
  const initial = who.short.slice(0, 1).toUpperCase();

  const onSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const form = new FormData(event.currentTarget);
    const name = String(form.get("name") ?? "").trim();
    const message = String(form.get("message") ?? "").trim();
    const guests = attendance === "no" ? 1 : Number(form.get("guests")) || 1;
    if (!name) return;
    if (!rsvpClosed) void rsvp.submit({ name, attendance, guests, message, diet: String(form.get("diet") ?? "").trim() || undefined });
    if (message) void wishes.send(name, message);
  };

  return (
    <ThemeShell
      fonts={FONTS}
      background="#ffe9c7"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Confetti />
          <Bunting />
          <Balloons className={s.coverBalloons} />
          <div className={s.coverBody}>
            <p className={s.coverKicker}>Undangan {label}</p>
            <h1 className={s.coverName}>{who.short}</h1>
            {ageText && <span className={s.ageSticker}><small>yang</small><b>{ageText.replace("ke-", "")}</b><small>tahun</small></span>}
            <p className={s.coverDate}><Lucide icon={ic.calendarPlus} size={15} />{chipDate(data.date)}</p>
            <div className={s.kepada}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.btn} onClick={open}><Lucide icon={ic.mailOpen} size={16} />Buka Undangan</button>
            <p className={s.hint}>psst… balonnya bisa diletuskan</p>
          </div>
        </section>
      )}
    >
      <main className={s.page}>
        <header className={s.hero}>
          <Bunting />
          <div className={s.heroArt}>
            <Balloons count={3} className={s.heroBalloons} />
            <Cake candles={who.age} />
          </div>
          <p className={s.script}>Hore, ada pesta!</p>
          <h1 className={s.heroName}>{who.short}</h1>
          <p className={s.heroLine}>{label}{ageText ? ` ${ageText}` : ""}</p>
          <p className={s.chip}><Lucide icon={ic.calendarPlus} size={14} />{chipDate(data.date)}</p>
        </header>

        <section className={s.band} aria-label="Salam pembuka">
          <div className={s.note}>
            <p className={s.hello}>Halo teman-teman, Om, dan Tante!</p>
            <p>{data.couple.note?.trim() || `Dengan penuh sukacita kami mengundang kamu untuk merayakan ${label.toLowerCase()} ${who.short}. Datang, bermain, dan bergembira bersama kami, ya!`}</p>
          </div>
        </section>

        <Extras slot="opening" without={["child"]} />

        <section className={`${s.band} ${s.tint}`} aria-labelledby="ub-who">
          <Head id="ub-who" kicker="Yang berulang tahun">Si Bintang Pesta</Head>
          <article className={s.star}>
            <div className={s.avatar}>
              {who.photo ? <Photo src={who.photo} alt={`Foto ${who.short}`} /> : <span aria-hidden>{initial}</span>}
              {ageText && <b className={s.avatarAge}>{who.age}</b>}
            </div>
            <h3>{who.full}</h3>
            {who.short !== who.full && <p className={s.nick}>panggil aku <b>{who.short}</b></p>}
            {who.birth && toDate(who.birth) && <p className={s.meta}>Lahir {formatDate(who.birth)}</p>}
            {ageText && <p className={s.turns}>berulang tahun {ageText}</p>}
            {who.meaning && <p className={s.meta}>{who.meaning}</p>}
            {who.parents && <p className={s.parents}>{who.parents}</p>}
          </article>
        </section>

        <section className={s.band} aria-labelledby="ub-count">
          <Head id="ub-count" kicker="Hitung mundur">Sebentar Lagi!</Head>
          {countdown.valid ? (
            <div className={s.count} role="timer" aria-label={`${countdown.days} hari ${countdown.hours} jam ${countdown.minutes} menit lagi`}>
              {([["Hari", countdown.days], ["Jam", countdown.hours], ["Menit", countdown.minutes], ["Detik", countdown.seconds]] as const).map(([unit, value], index) => (
                <div key={unit} className={s.countBlob} style={{ "--c": COLORS[index] } as CSSProperties}><b><Tick value={value} /></b><small>{unit}</small></div>
              ))}
            </div>
          ) : <p className={s.tba}>{DATE_TBA}</p>}
          {calendar && <a className={`${s.btn} ${s.btnGhost}`} href={calendar} target="_blank" rel="noreferrer"><Lucide icon={ic.calendarPlus} size={15} />Simpan ke Kalender</a>}
        </section>

        <section className={`${s.band} ${s.tint}`} aria-labelledby="ub-events">
          <Head id="ub-events" kicker="Catat ya">Waktu &amp; Tempat</Head>
          {data.events.map((event, index) => (
            <article key={event.name + index} className={s.ticket} style={{ "--c": COLORS[(index + 2) % COLORS.length] } as CSSProperties}>
              <div className={s.ticketTab}>
                <b>{dateParts(event.date || data.date).day || "?"}</b>
                <small>{dateParts(event.date || data.date).monthShort || "TBA"}</small>
              </div>
              <div className={s.ticketBody}>
                <h3>{event.name}</h3>
                <p className={s.ticketDate}>{formatDate(event.date || data.date)}</p>
                {event.time && <p className={s.ticketRow}><Lucide icon={ic.clock} size={14} />{event.time}</p>}
                {event.venue && <strong>{event.venue}</strong>}
                {event.address && <p className={s.ticketAddr}>{event.address}</p>}
                {mapsHref(data, event) && <a className={s.mapLink} href={mapsHref(data, event)} target="_blank" rel="noreferrer"><Lucide icon={ic.mapPin} size={14} />Petunjuk arah</a>}
              </div>
            </article>
          ))}
          {data.events.length === 0 && maps && <a className={s.btn} href={maps} target="_blank" rel="noreferrer"><Lucide icon={ic.mapPin} size={15} />Lihat Lokasi</a>}
        </section>

        <Extras slot="event" without={["calendar"]} />

        {stories.length > 0 && (
          <section className={s.band} aria-labelledby="ub-story">
            <Head id="ub-story" kicker="Tumbuh setiap hari">{`Cerita ${who.short}`}</Head>
            <ol className={s.stories}>
              {stories.map((story, index) => (
                <li key={story.title + index} className={s.storyCard} style={{ "--c": COLORS[index % COLORS.length] } as CSSProperties}>
                  <span className={s.storyYear}>{story.date || index + 1}</span>
                  <h3>{story.title}</h3>
                  {story.body && <p>{story.body}</p>}
                  {story.image && <Photo src={story.image} alt={story.title} className={s.storyImg} />}
                </li>
              ))}
            </ol>
          </section>
        )}

        {gallery.length > 0 && (
          <section className={`${s.band} ${s.tint}`} aria-labelledby="ub-gallery">
            <Head id="ub-gallery" kicker="Momen lucu">Galeri</Head>
            <div className={s.gallery}>
              {gallery.map((src, index) => <Photo key={src + index} src={src} alt={`Foto ${index + 1}`} className={s.polaroid} />)}
            </div>
          </section>
        )}

        <Extras slot="story" />

        <section className={`${s.band} ${s.wishBand}`} aria-label="Harapan">
          <div className={s.hope}>
            <Lucide icon={ic.sparkles} size={22} />
            <p>Semoga {who.short} tumbuh sehat, ceria, berbakti kepada orang tua, dan selalu dikelilingi kasih sayang.</p>
          </div>
        </section>

        <Extras slot="end" />

        <section className={s.band} aria-labelledby="ub-rsvp">
          <Head id="ub-rsvp" kicker="Kamu datang, kan?">RSVP &amp; Ucapan</Head>
          <div className={s.card}>
            {sent ? (
              <div ref={sentRef} className={s.sent} role="status">
                <span className={s.sentBadge}><Lucide icon={ic.check} size={22} strokeWidth={3} /></span>
                <strong>Yeay, terima kasih!</strong>
                <p>{demo ? "Ini pratinjau — jawaban contoh tidak dikirim." : sentSummary(rsvp, wishes)}</p>
                <button type="button" className={`${s.btn} ${s.btnGhost}`} onClick={() => { rsvp.reset(); wishes.reset(); }}>Tulis lagi</button>
              </div>
            ) : (
              <form className={s.form} onSubmit={onSubmit}>
                <label className={s.field}><span>Nama</span>
                  <input name="name" required maxLength={100} placeholder="Nama kamu" autoComplete="name" defaultValue={plainName(data.guestName)} />
                </label>
                <label className={s.field}><span>Ucapan untuk {who.short}</span>
                  <textarea name="message" required={rsvpClosed} maxLength={500} rows={3} placeholder="Tulis doa & ucapan ulang tahun…" />
                </label>
                {rsvpClosed ? (
                  <div className={s.closed} role="status"><strong>Konfirmasi kehadiran sudah ditutup</strong><p>Pestanya sudah selesai. Terima kasih! Ucapan &amp; doa masih bisa dikirim lewat form ini.</p></div>
                ) : (
                  <fieldset className={s.choices}>
                    <legend className={s.srOnly}>Kehadiran</legend>
                    {(Object.keys(ATTEND) as Attendance[]).map(key => (
                      <label key={key} className={attendance === key ? s.chosen : undefined}>
                        <input type="radio" name="attendance" value={key} checked={attendance === key} onChange={() => setAttendance(key)} />
                        {ATTEND[key]}
                      </label>
                    ))}
                  </fieldset>
                )}
                {!rsvpClosed && attendance !== "no" && <GuestCount label="Jumlah tamu" className={s.guests} buttonClassName={s.step} />}
                {!rsvpClosed && attendance !== "no" && <DietaryField className={s.field} />}
                {(rsvp.status === "error" || wishes.status === "error") && <p className={s.error} role="alert">Belum terkirim. Periksa koneksi lalu coba lagi.</p>}
                <button type="submit" className={`${s.btn} ${s.submit}`} disabled={sending}>{sending ? "Mengirim…" : "Kirim"}</button>
              </form>
            )}
          </div>
          {wishes.wishes.length === 0 && <p className={s.empty}>Belum ada ucapan. Jadilah yang pertama!</p>}
          <div className={s.wishes}>
            {wishes.wishes.slice(0, 10).map((wish, index) => (
              <article key={wish.id} className={s.wish} style={{ "--c": COLORS[index % COLORS.length] } as CSSProperties}>
                <div><strong>{wish.name}</strong>{wish.attendance && <small>{ATTEND[wish.attendance]}</small>}</div>
                <p>{wish.message}</p>
              </article>
            ))}
          </div>
        </section>

        {data.gifts.length > 0 && (
          <section className={`${s.band} ${s.tint}`} aria-labelledby="ub-gift">
            <Head id="ub-gift" kicker="Kado">Kirim Hadiah</Head>
            <p className={s.lead}>Kehadiran dan doamu sudah jadi kado terbaik. Bila ingin mengirim hadiah, bisa lewat:</p>
            {data.gifts.map(gift => {
              const info = giftInfo(gift);
              const on = Boolean(info.copy) && copied === info.copy;
              const icon = gift.type === "bank" ? ic.landmark : gift.type === "ewallet" ? ic.wallet : gift.type === "qris" ? ic.qrCode : ic.gift;
              return (
                <div key={gift.id} className={`${s.gift} ${on ? s.giftOn : ""}`}>
                  <span className={s.giftIcon}><Lucide icon={icon} size={20} /></span>
                  <div className={s.giftText}>
                    <small>{info.kind}</small>
                    <strong>{gift.type === "address" ? "Alamat kado" : info.title}</strong>
                    {info.number && <span className={s.giftNumber}>{info.number}</span>}
                    {info.holder && <span>a.n. {info.holder}</span>}
                    {info.image && <Photo src={info.image} alt="Kode QRIS" className={s.qris} />}
                  </div>
                  {info.copy && (
                    <button type="button" className={`${s.copy} ${on ? s.copyOn : ""}`} onClick={() => copy(info.copy)} aria-label={on ? "Tersalin" : `Salin ${info.title}`}>
                      <Lucide key={on ? "on" : "off"} icon={on ? ic.check : ic.copy} size={16} />
                    </button>
                  )}
                </div>
              );
            })}
          </section>
        )}

        <footer className={s.closing}>
          <Balloons count={3} className={s.footBalloons} />
          <h2>Terima Kasih!</h2>
          <p>Sampai jumpa di pesta {who.short}. Kehadiranmu membuat hari ini makin seru.</p>
          <p className={s.from}>Dengan sayang,<br /><strong>{who.parents ? who.parents.replace(/^(putra|putri|anak)[^,]*?dari\s+/i, "") : `Keluarga ${who.short}`}</strong></p>
          <a href="/" target="_blank" rel="noreferrer" className={s.made}>dibuat dengan ♥ di Rawuh</a>
        </footer>
      </main>
    </ThemeShell>
  );
}
