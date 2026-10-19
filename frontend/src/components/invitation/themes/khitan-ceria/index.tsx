"use client";
// Theme "Khitan Ceria" — khitanan anak yang ceria: stiker bergaris tebal, bendera segitiga berayun, dan jagoan kecil berpeci yang melambai.
import { useEffect, useRef, useState } from "react";
import {
  DietaryField, Extras, GuestCount, Icon, Photo, ThemeShell, Tick, dateParts, formatDate, giftInfo, guestLabel, icons,
  mapsHref, storyItems, toDate, useCopy, useCountdown, DATE_TBA, useRsvp, useThankYou, useWishes, type Attendance, type ThemeProps, type Wish,
} from "../kit";
import { tableLabel } from "../extras";
import { celebrate, toast } from "@/lib/celebrate";
import s from "./styles.module.css";

const FONTS = ["Poppins:wght@600;700;800", "Figtree:wght@400;500;600;700;800", "Amiri:wght@400;700"];
const ATTEND: Record<Attendance, string> = { yes: "Hadir", maybe: "Ragu", no: "Berhalangan" };
const DEMO_WISHES: Wish[] = [
  { id: "w1", name: "Om Bayu", attendance: "yes", message: "Selamat ya jagoan! Semoga Rafa jadi anak saleh, pintar, dan berbakti sama ayah ibu." },
  { id: "w2", name: "Bu Guru Aminah", attendance: "maybe", message: "Barakallahu fiik, Rafa. Semoga makin rajin mengaji dan salat ya, Nak." },
];
const COLORS = ["#ff7a59", "#ffc93c", "#12a594", "#4cc3ff", "#a77bf3"];
const STAR = "M12 2.5l2.6 5.6 6.1.7-4.5 4.2 1.2 6-5.4-3-5.4 3 1.2-6L3.3 8.8l6.1-.7z";
const WALLET = ["M19 7V4a1 1 0 0 0-1-1H5a2 2 0 0 0 0 4h15a1 1 0 0 1 1 1v4h-3a2 2 0 0 0 0 4h3a1 1 0 0 0 1-1v-2a1 1 0 0 0-1-1", "M3 5v14a2 2 0 0 0 2 2h15a1 1 0 0 0 1-1v-4"];
const BANK = ["M3 22h18", "M6 18v-7", "M10 18v-7", "M14 18v-7", "M18 18v-7", "M12 2l8 5H4z"];

/** Triangle bunting along a sagging string; each flag flutters from its top edge. */
function Bunting({ flags = 9, className }: { flags?: number; className?: string }) {
  const points = Array.from({ length: flags }, (_, i) => {
    const t = (i + 0.5) / flags;
    return { x: 390 * t, y: (1 - t) * (1 - t) * 6 + 2 * (1 - t) * t * 46 + t * t * 6 };
  });
  return (
    <svg className={`${s.bunting} ${className ?? ""}`} viewBox="0 0 390 70" preserveAspectRatio="xMidYMin slice" aria-hidden="true" focusable="false">
      <path d="M-4 6Q195 86 394 6" fill="none" stroke="#17324d" strokeWidth="2" />
      {points.map((p, i) => (
        <g key={i} className={s.flag} style={{ transformOrigin: `${p.x}px ${p.y}px`, animationDelay: `${-i * 0.37}s` }}>
          <path d={`M${p.x - 15} ${p.y}L${p.x + 15} ${p.y}L${p.x} ${p.y + 32}z`} fill={COLORS[i % COLORS.length]} stroke="#17324d" strokeWidth="2" strokeLinejoin="round" />
        </g>
      ))}
    </svg>
  );
}

/** Original flat illustration: a smiling boy in peci and baju koko, waving. */
function Boy({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 220 220" aria-hidden="true" focusable="false">
      <circle cx="110" cy="118" r="96" fill="#dff7ee" />
      <g stroke="#17324d" strokeWidth="3.5" strokeLinejoin="round" strokeLinecap="round">
        <path d="M58 220c0-50 20-74 52-74s52 24 52 74z" fill="#fff" />
        <path d="M110 148v72" fill="none" />
        <path d="M96 148l14 16 14-16" fill="#12a594" />
        <circle cx="110" cy="180" r="2.6" fill="#17324d" />
        <circle cx="110" cy="198" r="2.6" fill="#17324d" />
        <path d="M70 176c-6 14-8 28-8 44" fill="none" />
        <g className={s.wave}>
          <path d="M152 170c14-10 26-30 30-54" fill="none" stroke="#17324d" strokeWidth="22" />
          <path d="M152 170c14-10 26-30 30-54" fill="none" stroke="#fff" strokeWidth="15" />
          <circle cx="183" cy="106" r="12" fill="#f5c9a0" />
        </g>
        <circle cx="72" cy="104" r="9" fill="#f5c9a0" />
        <circle cx="148" cy="104" r="9" fill="#f5c9a0" />
        <circle cx="110" cy="100" r="40" fill="#f5c9a0" />
        <path d="M70 84c-2-30 14-40 40-40s42 10 40 40z" fill="#17324d" />
      </g>
      <path d="M74 72h72" stroke="#ffc93c" strokeWidth="3" />
      <circle cx="95" cy="104" r="4.4" fill="#17324d" />
      <circle cx="125" cy="104" r="4.4" fill="#17324d" />
      <circle cx="96.5" cy="102.5" r="1.4" fill="#fff" />
      <circle cx="126.5" cy="102.5" r="1.4" fill="#fff" />
      <path d="M97 118q13 12 26 0" fill="none" stroke="#17324d" strokeWidth="3.5" strokeLinecap="round" />
      <circle cx="84" cy="116" r="6" fill="#ff7a59" opacity=".35" />
      <circle cx="136" cy="116" r="6" fill="#ff7a59" opacity=".35" />
      <path className={s.chestStar} d="M84 168l3 6.4 7 .8-5.2 4.8 1.4 6.9-6.2-3.5-6.2 3.5 1.4-6.9-5.2-4.8 7-.8z" fill="#ffc93c" stroke="#17324d" strokeWidth="2" strokeLinejoin="round" />
    </svg>
  );
}

function Confetti({ count = 12, seed = 1 }: { count?: number; seed?: number }) {
  return (
    <div className={s.confetti} aria-hidden>
      {Array.from({ length: count }, (_, i) => {
        const n = (i + 3) * 29 * seed;
        const kind = n % 3;
        return <i key={i} data-kind={kind} style={{ left: `${(n * 13) % 96}%`, top: `${(n * 17) % 92}%`, background: kind === 2 ? "none" : COLORS[n % COLORS.length], color: COLORS[n % COLORS.length], rotate: `${(n * 23) % 180}deg`, animationDelay: `${(n % 7) * 0.5}s` }} />;
      })}
    </div>
  );
}

function Head({ id, tag, title, color = 0 }: { id: string; tag?: string; title: string; color?: number }) {
  return (
    <div className={s.head}>
      {tag && <p className={s.tag} style={{ background: COLORS[color % COLORS.length] }}>{tag}</p>}
      <h2 id={id}>{title}</h2>
    </div>
  );
}

/** The opening extras without the shared child card — this theme draws the child's profile itself. */
function OpeningExtras() {
  return <Extras slot="opening" without={["quote", "child"]} />;
}

/** "Muhammad Rafa Alfarizi" → "Rafa", "Naura Kamila" → "Naura" */
function shortName(name: string) {
  const words = name.trim().split(/\s+/);
  return /^(muhammad|muh\.?|moh\.?|m\.)$/i.test(words[0]) && words[1] ? words[1] : words[0];
}

function plainName(guest?: string) {
  if (!guest || guest === "Tamu Undangan") return "";
  return guest.replace(/^(bapak|ibu|bpk\.?|sdr\.?|saudara|saudari|om|tante)\s+/i, "").replace(/\s*(&|dan)\s*keluarga$/i, "").trim();
}

function parentNames(parents?: string) {
  const value = parents?.trim();
  if (!value) return "";
  const match = /\b(?:dari|of)\s+(.+)$/i.exec(value);
  return (match ? match[1] : value).trim();
}

/** Whole years between the birth date and the celebration. */
function ageAt(birth?: string, at?: string) {
  const born = toDate(birth);
  const day = toDate(at) ?? new Date();
  if (!born) return 0;
  let years = day.getFullYear() - born.getFullYear();
  if (day.getMonth() < born.getMonth() || (day.getMonth() === born.getMonth() && day.getDate() < born.getDate())) years -= 1;
  return years > 0 && years < 30 ? years : 0;
}

/** "Kirim semangat" — a decorative cheer counter with a little star burst. */
function Cheer({ name }: { name: string }) {
  const [count, setCount] = useState(0);
  const [bursts, setBursts] = useState<number[]>([]);
  const tap = () => {
    const id = Date.now();
    setCount(value => value + 1);
    setBursts(list => [...list.slice(-4), id]);
    window.setTimeout(() => setBursts(list => list.filter(item => item !== id)), 900);
    if (count === 0) toast(`Semangat terkirim untuk ${name}!`);
  };
  return (
    <button type="button" className={count > 0 ? `${s.cheer} ${s.cheerOn}` : s.cheer} onClick={tap} aria-label={`Kirim semangat untuk ${name}`}>
      <svg key={count} className={s.cheerStar} viewBox="0 0 24 24" aria-hidden="true"><path d={STAR} /></svg>
      <span>Kirim semangat</span>
      {count > 0 && <b aria-hidden><Tick value={count} /></b>}
      {bursts.map(id => <span key={id} className={s.burst} aria-hidden><i /><i /><i /><i /><i /><i /></span>)}
    </button>
  );
}

export default function KhitanCeriaTheme({ data, slug, guestToken, demo, skipCover }: ThemeProps) {
  const label = data.eventLabel ?? "Khitanan";
  const child = data.extras?.child?.enabled !== false && data.extras?.child?.name?.trim() ? data.extras.child : undefined;
  const kids = child
    ? [{ name: child.name, nick: child.nickname || shortName(child.name), birth: child.birthDate, meaning: child.meaning, parents: child.parents || data.couple.brideParents, photo: child.photo }]
    : [
      { name: data.couple.brideFull || data.couple.bride, nick: data.couple.bride, birth: undefined, meaning: undefined, parents: data.couple.brideParents, photo: data.couple.bridePhoto },
      ...(data.couple.groom?.trim() ? [{ name: data.couple.groomFull || data.couple.groom, nick: data.couple.groom, birth: undefined, meaning: undefined, parents: data.couple.groomParents, photo: data.couple.groomPhoto }] : []),
    ];
  const nick = kids.map(kid => kid.nick).filter(Boolean).join(" & ") || "Jagoan Kecil";
  const parents = parentNames(kids[0]?.parents);
  const countdown = useCountdown(data.date);
  const rsvp = useRsvp({ slug, guestToken, demo });
  const wishes = useWishes({ slug, guestToken, demo, seed: DEMO_WISHES });
  const thanks = useThankYou();
  const rsvpClosed = thanks.active || rsvp.status === "closed";
  const { copy, copied } = useCopy();
  const [attendance, setAttendance] = useState<Attendance>("yes");
  const stories = storyItems(data);
  const table = tableLabel(data.guestTable);
  const quote = data.extras?.quote?.enabled !== false && data.extras?.quote?.text ? data.extras.quote : { text: "Kemudian Kami wahyukan kepadamu (Muhammad), ‘Ikutilah agama Ibrahim yang lurus.’", source: "QS. An-Nahl: 123" };
  const sentRef = useRef<HTMLDivElement>(null);
  useEffect(() => { if (wishes.status === "sent") celebrate(sentRef.current); }, [wishes.status]);

  return (
    <ThemeShell
      fonts={FONTS}
      background="#dff7ee"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Confetti count={14} seed={2} />
          <Bunting />
          <div className={s.coverStack}>
            <p className={s.tag} style={{ background: "#ff7a59" }}>Undangan {label}</p>
            <Boy className={s.coverBoy} />
            <h1 className={s.coverName}>{nick}</h1>
            {child && child.name !== nick && <p className={s.coverFull}>{child.name}</p>}
            <p className={s.coverDate}><Icon d={icons.calendar} size={15} strokeWidth={2.6} />{formatDate(data.date)}</p>
          </div>
          <div className={s.kepada}>
            <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
            <strong>{guestLabel(data)}</strong>
            {table && <span className={s.table}>{table}</span>}
          </div>
          <button type="button" className={s.btn} onClick={open}><Icon d={icons.mailOpen} size={17} strokeWidth={2.6} />Buka Undangan</button>
        </section>
      )}
    >
      <main className={s.main}>
        <header className={s.hero}>
          <Bunting />
          <Confetti count={10} seed={5} />
          <p className={s.arabic} lang="ar" dir="rtl">بِسْمِ اللّٰهِ الرَّحْمٰنِ الرَّحِيْمِ</p>
          <p className={s.heroKicker}>Tasyakuran {label}</p>
          <h1 className={s.heroName}>{kids.map(kid => kid.name).join(" & ")}</h1>
          <p className={s.heroDate}>{formatDate(data.date)}</p>
        </header>

        <section className={s.section} aria-labelledby="kc-salam">
          <h2 id="kc-salam" className={s.salam}>Assalamu&rsquo;alaikum Warahmatullahi Wabarakatuh</h2>
          <p className={s.lead}>Dengan memohon rahmat dan ridha Allah Subhanahu wa Ta&rsquo;ala, kami mengundang Bapak/Ibu/Saudara/i serta teman-teman untuk hadir pada tasyakuran {label.toLowerCase()} putra kami.</p>
          <figure className={s.quote}>
            <span className={s.quoteMark} aria-hidden>&ldquo;</span>
            <blockquote>{quote.text}</blockquote>
            {quote.source && <figcaption>{quote.source}</figcaption>}
          </figure>
        </section>

        <OpeningExtras />

        <section className={`${s.section} ${s.mint}`} aria-labelledby="kc-kid">
          <Confetti count={8} seed={7} />
          <Head id="kc-kid" tag="Kenalan dulu" title={kids.length > 1 ? "Jagoan-Jagoan Kita" : "Jagoan Kita"} color={1} />
          {kids.map((kid, index) => {
            const age = ageAt(kid.birth, data.date);
            return (
              <article key={index} className={s.kid}>
                <div className={s.kidArt}>
                  {kid.photo ? <Photo src={kid.photo} alt={`Foto ${kid.nick}`} className={s.kidPhoto} /> : <Boy className={s.kidBoy} />}
                  {age > 0 && <span className={s.ageBadge}><b>{age}</b>tahun</span>}
                </div>
                <h3>{kid.name}</h3>
                {kid.nick && kid.nick !== kid.name && <p className={s.nick}>Panggilannya <b>{kid.nick}</b></p>}
                {kid.birth && <p className={s.born}><Icon d={icons.star} size={14} strokeWidth={2.4} />Lahir {formatDate(kid.birth, { day: "numeric", month: "long", year: "numeric" })}</p>}
                {kid.meaning && <div className={s.meaning}><small>Arti nama</small><p>{kid.meaning}</p></div>}
                {kid.parents && <p className={s.parents}>{kid.parents}</p>}
              </article>
            );
          })}
          <Cheer name={nick} />
        </section>

        <section className={s.section} aria-labelledby="kc-doa">
          <Head id="kc-doa" tag="Doa kami" title="Harapan untuk Si Jagoan" color={2} />
          <div className={s.doa}>
            <p className={s.arabic} lang="ar" dir="rtl">رَبِّ هَبْ لِيْ مِنَ الصّٰلِحِيْنَ</p>
            <p className={s.translit}>&ldquo;Ya Tuhanku, anugerahkanlah kepadaku (anak) yang termasuk orang-orang saleh.&rdquo;</p>
            <cite>QS. As-Saffat: 100 — doa Nabi Ibrahim</cite>
          </div>
          <ol className={s.hopes}>
            {["Tumbuh menjadi anak saleh yang cinta Al-Qur'an", "Sehat, kuat, dan cepat pulih", "Berbakti kepada ayah dan ibu", "Berani dan jujur dalam kebaikan"].map((hope, index) => (
              <li key={hope} style={{ ["--c" as string]: COLORS[index % COLORS.length] }}><b>{index + 1}</b><span>{hope}</span></li>
            ))}
          </ol>
        </section>

        <section className={`${s.section} ${s.sun}`} aria-labelledby="kc-count">
          <Head id="kc-count" tag="Tinggal sebentar lagi" title="Hitung Mundur" color={0} />
          {countdown.valid ? (
            <div className={s.count} role="timer" aria-label={`${countdown.days} hari ${countdown.hours} jam ${countdown.minutes} menit lagi`}>
              {[[countdown.days, "Hari"], [countdown.hours, "Jam"], [countdown.minutes, "Menit"], [countdown.seconds, "Detik"]].map(([value, unit], index) => (
                <div key={unit} className={s.countBox} style={{ ["--c" as string]: COLORS[(index + 2) % COLORS.length] }}><b><Tick value={value} /></b><small>{unit}</small></div>
              ))}
            </div>
          ) : <p className={s.tba}>{DATE_TBA}</p>}
        </section>

        <section className={s.section} aria-labelledby="kc-events">
          <Head id="kc-events" tag="Catat ya" title="Acaranya Kapan?" color={3} />
          <div className={s.events}>
            {data.events.map((event, index) => {
              const href = mapsHref(data, event);
              const day = dateParts(event.date || data.date);
              return (
                <article key={event.name + index} className={s.event} style={{ ["--c" as string]: COLORS[(index * 2 + 2) % COLORS.length] }}>
                  <div className={s.eventTop}>
                    <span className={s.eventDay}>{day.day ? <><b>{day.day}</b>{day.monthShort}</> : "TBA"}</span>
                    <h3>{event.name}</h3>
                  </div>
                  <p><Icon d={icons.calendar} size={15} strokeWidth={2.4} />{formatDate(event.date || data.date)}</p>
                  {event.time && <p><Icon d={icons.clock} size={15} strokeWidth={2.4} />{event.time}</p>}
                  <p className={s.venue}><Icon d={icons.mapPin} size={15} strokeWidth={2.4} /><span><strong>{event.venue}</strong>{event.address && <small>{event.address}</small>}</span></p>
                  {href && <a className={s.btnSm} href={href} target="_blank" rel="noreferrer">Buka Peta<Icon d={icons.arrowRight} size={15} strokeWidth={2.6} /></a>}
                </article>
              );
            })}
          </div>
        </section>

        <Extras slot="event" />

        {stories.length > 0 && (
          <section className={`${s.section} ${s.mint}`} aria-labelledby="kc-story">
            <Head id="kc-story" tag="Cerita" title="Perjalanan Si Jagoan" color={4} />
            <ol className={s.timeline}>
              {stories.map((story, index) => (
                <li key={index} style={{ ["--c" as string]: COLORS[index % COLORS.length] }}>
                  {story.date && <small>{story.date}</small>}
                  <h3>{story.title}</h3>
                  {story.body && <p>{story.body}</p>}
                  {story.image && <Photo src={story.image} alt={story.title} className={s.storyImg} />}
                </li>
              ))}
            </ol>
          </section>
        )}

        {data.gallery.length > 0 && (
          <section className={s.section} aria-labelledby="kc-gallery">
            <Head id="kc-gallery" tag="Foto" title="Galeri Ceria" color={1} />
            <div className={s.gallery}>
              {data.gallery.map((src, index) => <div key={src + index} className={s.shot}><Photo src={src} alt={`Foto galeri ${index + 1}`} /></div>)}
            </div>
          </section>
        )}

        <Extras slot="story" />
        <Extras slot="end" />

        {data.gifts.length > 0 && (
          <section className={`${s.section} ${s.mint}`} aria-labelledby="kc-gift">
            <Head id="kc-gift" tag="Tanda sayang" title={`Hadiah untuk ${nick}`} color={0} />
            <p className={s.lead}>Doa dan kehadiran Anda sudah membuat kami bahagia. Bila ingin memberi hadiah, dapat melalui:</p>
            <div className={s.gifts}>
              {data.gifts.map((gift, index) => {
                const info = giftInfo(gift);
                const on = Boolean(info.copy && copied === info.copy);
                return (
                  <div key={gift.id} className={on ? `${s.gift} ${s.giftOn}` : s.gift} style={{ ["--c" as string]: COLORS[(index + 1) % COLORS.length] }}>
                    <span className={s.giftIcon}><Icon d={gift.type === "bank" ? BANK : gift.type === "address" ? icons.gift : WALLET} size={20} strokeWidth={2.4} /></span>
                    <div className={s.giftText}>
                      <small>{info.kind}</small>
                      <strong>{info.title}</strong>
                      {info.number && <span className={s.giftNumber}>{info.number}</span>}
                      {info.holder && <span>a.n. {info.holder}</span>}
                      {info.image && <Photo src={info.image} alt="Kode QRIS" className={s.qris} />}
                    </div>
                    {info.copy && (
                      <button type="button" className={on ? `${s.copy} ${s.copyOn}` : s.copy} onClick={() => copy(info.copy)} aria-label={on ? "Tersalin" : `Salin ${info.title}`}>
                        <Icon key={on ? "on" : "off"} d={on ? icons.check : icons.copy} size={16} strokeWidth={2.6} />{on ? "Oke!" : "Salin"}
                      </button>
                    )}
                  </div>
                );
              })}
            </div>
          </section>
        )}

        <section className={s.section} aria-labelledby="kc-wishes">
          <Head id="kc-wishes" tag="Konfirmasi & doa" title="Datang, Ya!" color={2} />
          {wishes.status === "sent" ? (
            <div ref={sentRef} className={`${s.form} ${s.sentBox}`} role="status">
              <svg className={s.sentStar} viewBox="0 0 24 24" aria-hidden="true"><path d={STAR} /></svg>
              <strong>Terima kasih banyak!</strong>
              <p>{demo ? "Ini pratinjau — ucapan hanya tampil di daftar." : wishes.pending ? "Doamu akan tampil setelah disetujui keluarga." : rsvp.status === "sent" ? "Konfirmasi dan doamu sudah kami terima." : "Doamu sudah kami terima."}</p>
              <button type="button" className={s.btn} onClick={() => { wishes.reset(); rsvp.reset(); }}>Tulis Lagi</button>
            </div>
          ) : (
            <form className={s.form} onSubmit={event => {
              event.preventDefault();
              const form = new FormData(event.currentTarget);
              const name = String(form.get("name") ?? "").trim();
              const message = String(form.get("message") ?? "").trim();
              const guests = attendance === "no" ? 1 : Number(form.get("guests") ?? 1) || 1;
              if (!name || !message) return;
              void wishes.send(name, message);
              if (!rsvpClosed && rsvp.status !== "sent") void rsvp.submit({ name, attendance, guests, message, diet: String(form.get("diet") ?? "").trim() || undefined });
            }}>
              <label className={s.field}><span>Nama</span><input name="name" required maxLength={100} defaultValue={plainName(data.guestName)} placeholder="Nama kamu" autoComplete="name" /></label>
              {rsvpClosed ? (
                <div className={s.closed} role="status"><strong>Konfirmasi kehadiran sudah ditutup</strong><p>Terima kasih atas doa dan perhatiannya. Doa untuk {nick} masih bisa dikirim lewat form ini.</p></div>
              ) : (
                <div className={s.field}>
                  <span>Kehadiran</span>
                  <div className={s.choices} role="radiogroup" aria-label="Kehadiran">
                    {(["yes", "maybe", "no"] as Attendance[]).map(value => (
                      <button key={value} type="button" role="radio" aria-checked={attendance === value} className={attendance === value ? s.choiceOn : undefined} onClick={() => setAttendance(value)}>{ATTEND[value]}</button>
                    ))}
                  </div>
                </div>
              )}
              {!rsvpClosed && attendance !== "no" && <GuestCount label="Jumlah tamu" className={s.guests} buttonClassName={s.step} />}
              {!rsvpClosed && attendance !== "no" && <DietaryField className={s.field} />}
              <label className={s.field}><span>Doa &amp; ucapan</span><textarea name="message" required maxLength={500} rows={3} placeholder={`Tulis doa untuk ${nick}…`} /></label>
              {(wishes.status === "error" || rsvp.status === "error") && <p className={s.error} role="alert">Belum terkirim. Periksa koneksi lalu coba lagi.</p>}
              <button type="submit" className={s.btn} disabled={wishes.status === "sending"}>{wishes.status === "sending" ? "Mengirim…" : "Kirim"}</button>
            </form>
          )}
          <div className={s.wishes}>
            {wishes.wishes.length === 0 && <p className={s.empty}>Belum ada doa. Jadilah yang pertama mendoakan {nick}.</p>}
            {wishes.wishes.slice(0, 12).map((wish, index) => (
              <article key={wish.id} className={s.wish} style={{ ["--c" as string]: COLORS[index % COLORS.length] }}>
                <span className={s.avatar} aria-hidden>{wish.name.trim().slice(0, 1).toUpperCase()}</span>
                <div>
                  <p className={s.wishHead}><strong>{wish.name}</strong>{wish.attendance && <small>{ATTEND[wish.attendance]}</small>}</p>
                  <p>{wish.message}</p>
                </div>
              </article>
            ))}
          </div>
        </section>

        <footer className={s.closing}>
          <Confetti count={10} seed={9} />
          <p className={s.lead}>Atas kehadiran dan doa restu Bapak/Ibu/Saudara/i, kami ucapkan terima kasih. Jazakumullahu khairan.</p>
          <p className={s.salamEnd}>Wassalamu&rsquo;alaikum Warahmatullahi Wabarakatuh</p>
          <p className={s.tag} style={{ background: "#12a594" }}>Kami yang berbahagia</p>
          <p className={s.closingNames}>{parents || `Keluarga ${nick}`}</p>
          <a href="/" target="_blank" rel="noreferrer" className={s.made}>dibuat dengan ♥ di Rawuh</a>
          <Bunting className={s.buntingBottom} />
        </footer>
      </main>
    </ThemeShell>
  );
}
