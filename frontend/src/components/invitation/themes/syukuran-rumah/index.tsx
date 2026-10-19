"use client";
// Theme "Syukuran Rumah" — tasyakuran rumah baru: kertas hangat, terakota & sage, bingkai pintu melengkung, ilustrasi rumah yang tergambar sendiri.
import { useEffect, useRef, useState, type FormEvent } from "react";
import {
  DietaryField, Extras, GuestCount, Lucide, Photo, ThemeShell, Tick, dateParts, formatDate, giftInfo, guestLabel, mapsHref,
  storyItems, toDate, useCopy, useCountdown, DATE_TBA, sentSummary, useRsvp, useThankYou, useWishes, type Attendance, type ThemeProps, type Wish,
} from "../kit";
import type { InvitationData } from "../../types";
import { tableLabel } from "../extras";
import { celebrate } from "@/lib/celebrate";
import { ic } from "./icons";
import s from "./styles.module.css";

const FONTS = ["Lora:ital,wght@0,400;0,500;0,600;0,700;1,400;1,500", "Mulish:wght@400;600;700;800", "Amiri:wght@400;700"];
const ATTEND: Record<Attendance, string> = { yes: "Hadir", maybe: "Ragu", no: "Berhalangan" };
const DEMO_WISHES: Wish[] = [
  { id: "w1", name: "Bu Ningsih (tetangga C3/10)", attendance: "yes", message: "Selamat datang di Griya Asri! Semoga rumahnya penuh berkah, betah, dan selalu ramai tawa anak-anak." },
  { id: "w2", name: "Mas Andri & Mbak Tika", attendance: "yes", message: "Barakallah, akhirnya punya istana sendiri. Semoga menjadi baiti jannati." },
];

/* ── Helpers ───────────────────────────────────────────────── */

function hostNames(data: InvitationData) {
  const a = data.couple.bride?.trim() ?? "";
  const b = data.couple.groom?.trim() ?? "";
  const short = [a, b].filter(Boolean).join(" & ");
  const full = [data.couple.brideFull?.trim() || a, b ? data.couple.groomFull?.trim() || b : ""].filter(Boolean);
  return { family: short ? `Keluarga ${short}` : "Keluarga Kami", full, initials: [a, b].filter(Boolean).map(n => n.slice(0, 1).toUpperCase()).join("") || "K" };
}

/** "… Blok C3 No. 12 …" → "C3/12"; "… No. 7 …" → "7". */
function houseNumber(address?: string) {
  if (!address) return "";
  const block = /\bBlok\s+([A-Z0-9-]+)/i.exec(address)?.[1];
  const no = /\b(?:No\.?|Nomor)\s*([0-9]+[A-Z]?)/i.exec(address)?.[1];
  return [block?.toUpperCase(), no].filter(Boolean).join("/");
}

function calendarHref(title: string, data: InvitationData) {
  const start = toDate(data.events[0]?.date ?? data.date);
  if (!start) return undefined;
  const last = toDate(data.events[data.events.length - 1]?.date) ?? start;
  const stamp = (d: Date) => d.toISOString().replace(/[-:]|\.\d{3}/g, "");
  const params = new URLSearchParams({ action: "TEMPLATE", text: title, dates: `${stamp(start)}/${stamp(new Date(Math.max(start.getTime(), last.getTime()) + 3 * 3600e3))}`, location: [data.place, data.address].filter(Boolean).join(", ") });
  return `https://calendar.google.com/calendar/render?${params.toString()}`;
}

function plainName(guest?: string) {
  if (!guest || guest === "Tamu Undangan") return "";
  return guest.replace(/^(bapak|ibu|bpk\.?|sdr\.?)\s+/i, "").replace(/\s*(&|dan)\s*keluarga$/i, "").trim();
}

function timeOf(value?: string) {
  const date = toDate(value);
  return date ? new Intl.DateTimeFormat("id-ID", { timeZone: "Asia/Jakarta", hour: "2-digit", minute: "2-digit" }).format(date).replace(":", ".") : "";
}

/* ── Ornaments ─────────────────────────────────────────────── */

/** Line-art house with lit windows and potted plants (240×170). */
function House({ animate, className }: { animate?: boolean; className?: string }) {
  return (
    <svg className={`${s.house} ${animate ? s.animate : ""} ${className ?? ""}`} viewBox="0 0 240 170" aria-hidden="true" focusable="false">
      <rect className={s.glow} x="67" y="103" width="26" height="24" rx="1" />
      <rect className={s.glow} x="147" y="103" width="26" height="24" rx="1" />
      <circle className={s.glow} cx="120" cy="70" r="7" />
      <g className={s.sway}>
        <path className={s.leaf} d="M30 146c-6-12-12-16-14-26 8 3 13 11 14 26z" />
        <path className={s.leafDark} d="M31 146c2-14 7-22 15-26-1 10-7 17-15 26z" />
        <path className={s.leaf} d="M31 146c-1-16 1-26 6-34 3 10 1 22-6 34z" />
      </g>
      <path className={s.pot} d="M21 145h21l-3 15H24z" />
      <g className={s.sway}>
        <circle className={s.leaf} cx="214" cy="112" r="16" />
        <circle className={s.leafDark} cx="204" cy="124" r="10" />
        <circle className={s.leaf} cx="224" cy="126" r="10" />
      </g>
      <path className={s.draw} pathLength={1} d="M214 160v-36" />
      <path className={s.draw} pathLength={1} d="M6 160h228" />
      <path className={s.draw} pathLength={1} d="M50 160V88h140v72" />
      <path className={s.draw} pathLength={1} d="M36 92 120 36l84 56" />
      <path className={`${s.draw} ${s.soft}`} pathLength={1} d="M60 87 120 47l60 40" />
      <path className={s.draw} pathLength={1} d="M158 60V40h14v30" />
      <path className={s.draw} pathLength={1} d="M106 160v-38a14 14 0 0 1 28 0v38" />
      <path className={s.draw} pathLength={1} d="M66 102h28v26H66z" />
      <path className={s.draw} pathLength={1} d="M146 102h28v26h-28z" />
      <path className={`${s.draw} ${s.soft}`} pathLength={1} d="M80 102v26M66 115h28M160 102v26M146 115h28" />
      <path className={s.draw} pathLength={1} d="M128 70a8 8 0 1 1-16 0 8 8 0 1 1 16 0" />
      <path className={`${s.draw} ${s.soft}`} pathLength={1} d="M98 160h44M62 132h36M142 132h36" />
      <circle cx="128" cy="142" r="1.8" fill="currentColor" />
    </svg>
  );
}

function Roof() {
  return <svg className={s.roof} viewBox="0 0 46 18" aria-hidden="true"><path d="M2 16 23 3l21 13" fill="none" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round" /><circle cx="23" cy="11" r="2" fill="currentColor" /></svg>;
}

function Head({ id, eyebrow, children }: { id: string; eyebrow?: string; children: string }) {
  return (
    <div className={s.head}>
      <Roof />
      {eyebrow && <p className={s.eyebrow}>{eyebrow}</p>}
      <h2 id={id}>{children}</h2>
    </div>
  );
}

/* ── Theme ─────────────────────────────────────────────────── */

export default function SyukuranRumahTheme({ data, slug, guestToken, demo, skipCover }: ThemeProps) {
  const hosts = hostNames(data);
  const label = data.eventLabel?.trim() || "Tasyakuran Rumah Baru";
  const parts = dateParts(data.date);
  const longDate = formatDate(data.date);
  const countdown = useCountdown(data.date);
  const rsvp = useRsvp({ slug, guestToken, demo });
  const wishes = useWishes({ slug, guestToken, demo, seed: DEMO_WISHES });
  const thanks = useThankYou();
  const rsvpClosed = thanks.active || rsvp.status === "closed";
  const { copy, copied } = useCopy();
  const stories = storyItems(data);
  const gallery = data.gallery.filter(Boolean);
  const [attendance, setAttendance] = useState<Attendance>("yes");
  const maps = mapsHref(data);
  const calendar = calendarHref(`${label} ${hosts.family}`, data);
  const table = tableLabel(data.guestTable);
  const number = houseNumber(data.address);
  const notes = [data.couple.brideParents, data.couple.groomParents].map(v => v?.trim()).filter(Boolean);
  const photos = [data.couple.bridePhoto, data.couple.groomPhoto].filter(Boolean) as string[];
  const sending = rsvp.status === "sending" || wishes.status === "sending";
  const sent = rsvp.status === "sent" || wishes.status === "sent";
  const sentRef = useRef<HTMLDivElement>(null);
  useEffect(() => { if (sent) celebrate(sentRef.current); }, [sent]);

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
      background="#e9dfcc"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.door}>
            <House animate />
            <p className={s.coverKicker}>Undangan</p>
            <h1 className={s.coverTitle}>{label}</h1>
            <p className={s.coverFamily}>{hosts.family}</p>
            <p className={s.coverDate}>{longDate}</p>
          </div>
          <div className={s.kepada}>
            <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
            <strong>{guestLabel(data)}</strong>
            {table && <span className={s.table}>{table}</span>}
          </div>
          <button type="button" className={s.btn} onClick={open}><Lucide icon={ic.mailOpen} size={16} />Buka Undangan</button>
        </section>
      )}
    >
      <main className={s.page}>
        <header className={s.hero}>
          <div className={s.heroArch}><House animate /></div>
          <span className={s.heroGround} aria-hidden />
          <p className={s.bismillah} lang="ar">بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ</p>
          <p className={s.heroKicker}>Undangan</p>
          <h1 className={s.heroTitle}>{label}</h1>
          <p className={s.heroFamily}>{hosts.family}</p>
          <p className={s.heroDate}>{parts.day ? `${parts.weekday} · ${parts.day} ${parts.month} ${parts.year}` : DATE_TBA}</p>
        </header>

        <section className={`${s.section} ${s.alt}`} aria-label="Salam pembuka">
          <p className={s.salam}>Assalamu&apos;alaikum Warahmatullahi Wabarakatuh</p>
          <p className={s.lead}>{data.couple.note?.trim() || "Dengan memohon rahmat dan ridha Allah SWT, kami bermaksud menyelenggarakan tasyakuran atas rumah baru kami."} Kami mengharap kehadiran Bapak/Ibu/Saudara/i untuk turut mendoakan keberkahan rumah ini.</p>
          <figure className={s.doa}>
            <p className={s.arabic} lang="ar">رَبِّ أَنْزِلْنِي مُنْزَلًا مُبَارَكًا وَأَنْتَ خَيْرُ الْمُنْزِلِينَ</p>
            <figcaption>
              <p className={s.doaText}>“Ya Tuhanku, tempatkanlah aku pada tempat yang diberkahi, dan Engkaulah sebaik-baik pemberi tempat.”</p>
              <cite className={s.doaSrc}>QS. Al-Mu&apos;minun: 29</cite>
            </figcaption>
          </figure>
        </section>

        <Extras slot="opening" />

        <section className={s.section} aria-labelledby="sr-hosts">
          <Head id="sr-hosts" eyebrow="Tuan rumah">Yang Berbahagia</Head>
          <article className={s.hosts}>
            {photos.length > 0 ? (
              <div className={s.hostPhotos}>{photos.map((src, index) => <Photo key={src + index} src={src} alt={hosts.full[index] ?? hosts.family} className={s.hostPhoto} />)}</div>
            ) : <span className={s.monogram} aria-hidden>{hosts.initials}</span>}
            <div className={s.host}>
              <p className={s.eyebrow}>{hosts.family}</p>
              {hosts.full.map((name, index) => (
                <div key={name + index}>
                  {index > 0 && <p className={s.amp} aria-hidden>&amp;</p>}
                  <h3>{name}</h3>
                </div>
              ))}
              {notes.map((note, index) => <p key={index}>{note}</p>)}
            </div>
          </article>
        </section>

        <section className={`${s.section} ${s.alt}`} aria-labelledby="sr-address">
          <Head id="sr-address" eyebrow="Alamat rumah baru">Mampir ke Rumah Kami</Head>
          <div className={s.address}>
            <span className={s.plaque}>
              <small>Nomor</small>
              {number ? <b>{number}</b> : <Lucide icon={ic.mapPin} size={30} />}
            </span>
            <strong>{data.place || hosts.family}</strong>
            {data.address && <p>{data.address}</p>}
            {maps && <a className={s.btn} href={maps} target="_blank" rel="noreferrer"><Lucide icon={ic.mapPin} size={15} />Buka di Google Maps</a>}
          </div>
        </section>

        <section className={s.section} aria-labelledby="sr-count">
          <Head id="sr-count" eyebrow="Menuju hari syukur">Hitung Mundur</Head>
          {countdown.valid ? (
            <>
              <div className={s.window} role="timer" aria-label={`${countdown.days} hari ${countdown.hours} jam ${countdown.minutes} menit lagi`}>
                {([["Hari", countdown.days], ["Jam", countdown.hours], ["Menit", countdown.minutes], ["Detik", countdown.seconds]] as const).map(([unit, value]) => (
                  <div key={unit} className={s.pane}><b><Tick value={value} /></b><small>{unit}</small></div>
                ))}
              </div>
              <span className={s.sill} aria-hidden />
            </>
          ) : <p className={s.tba}>{DATE_TBA}</p>}
          {calendar && <a className={`${s.btn} ${s.btnLine}`} href={calendar} target="_blank" rel="noreferrer"><Lucide icon={ic.calendarPlus} size={15} />Simpan ke Kalender</a>}
        </section>

        <section className={`${s.section} ${s.alt}`} aria-labelledby="sr-events">
          <Head id="sr-events" eyebrow="Susunan acara">Waktu &amp; Tempat</Head>
          <div className={s.events}>
            {data.events.map((event, index) => {
              const when = event.date || data.date;
              const href = mapsHref(data, event);
              return (
                <article key={event.name + index} className={s.event}>
                  <div className={s.eventTime}><b>{timeOf(when) || dateParts(when).day || "–"}</b><small>{timeOf(when) ? "WIB" : dateParts(when).monthShort}</small></div>
                  <div className={s.eventBody}>
                    <h3>{event.name}</h3>
                    <p>{formatDate(when)}{event.time ? ` · ${event.time}` : ""}</p>
                    {event.venue && <strong>{event.venue}</strong>}
                    {event.address && <p>{event.address}</p>}
                    {href && <a className={s.mapLink} href={href} target="_blank" rel="noreferrer"><Lucide icon={ic.mapPin} size={13} />Petunjuk arah</a>}
                  </div>
                </article>
              );
            })}
          </div>
        </section>

        <Extras slot="event" without={["calendar"]} />

        {stories.length > 0 && (
          <section className={s.section} aria-labelledby="sr-story">
            <Head id="sr-story" eyebrow="Dari kontrakan ke rumah sendiri">{data.story?.title?.trim() || "Cerita Rumah Ini"}</Head>
            <ol className={s.timeline}>
              {stories.map((story, index) => (
                <li key={story.title + index}>
                  <span className={s.brick}><Lucide icon={index === stories.length - 1 ? ic.mailOpen : ic.sparkles} size={18} /></span>
                  <div>
                    {story.date && <small>{story.date}</small>}
                    <h3>{story.title}</h3>
                    {story.body && <p>{story.body}</p>}
                    {story.image && <Photo src={story.image} alt={story.title} className={s.storyImg} />}
                  </div>
                </li>
              ))}
            </ol>
          </section>
        )}

        {gallery.length > 0 && (
          <section className={`${s.section} ${s.alt}`} aria-labelledby="sr-gallery">
            <Head id="sr-gallery" eyebrow="Sudut-sudut rumah">Galeri</Head>
            <div className={s.gallery}>{gallery.map((src, index) => <Photo key={src + index} src={src} alt={`Foto ${index + 1}`} />)}</div>
          </section>
        )}

        <Extras slot="story" />

        <Extras slot="end" />

        <section className={`${s.section} ${s.alt}`} aria-labelledby="sr-rsvp">
          <Head id="sr-rsvp" eyebrow="Konfirmasi kehadiran">Doa &amp; Ucapan</Head>
          <div className={s.formCard}>
            {sent ? (
              <div ref={sentRef} className={s.sent} role="status">
                <span className={s.sentIcon}><Lucide icon={ic.check} size={22} strokeWidth={2.4} /></span>
                <strong>Jazakumullah khairan</strong>
                <p>{demo ? "Ini pratinjau — jawaban contoh tidak dikirim." : sentSummary(rsvp, wishes)}</p>
                <button type="button" className={`${s.btn} ${s.btnLine}`} onClick={() => { rsvp.reset(); wishes.reset(); }}>Tulis lagi</button>
              </div>
            ) : (
              <form className={s.form} onSubmit={onSubmit}>
                <label className={s.field}><span>Nama</span><input name="name" required maxLength={100} placeholder="Nama Anda" autoComplete="name" defaultValue={plainName(data.guestName)} /></label>
                <label className={s.field}><span>Doa untuk rumah ini</span><textarea name="message" required={rsvpClosed} maxLength={500} rows={3} placeholder="Tuliskan doa & ucapan…" /></label>
                {rsvpClosed ? (
                  <div className={s.closed} role="status"><strong>Konfirmasi kehadiran sudah ditutup</strong><p>Acara telah berlangsung. Terima kasih atas doa dan kehadirannya. Doa &amp; ucapan masih bisa dikirim lewat form ini.</p></div>
                ) : (
                  <fieldset className={s.choices}>
                    <legend className={s.srOnly}>Kehadiran</legend>
                    {(Object.keys(ATTEND) as Attendance[]).map(key => (
                      <label key={key} className={attendance === key ? s.chosen : undefined}>
                        <input type="radio" name="attendance" value={key} checked={attendance === key} onChange={() => setAttendance(key)} />{ATTEND[key]}
                      </label>
                    ))}
                  </fieldset>
                )}
                {!rsvpClosed && attendance !== "no" && <GuestCount label="Jumlah tamu" className={s.guests} buttonClassName={s.step} />}
                {!rsvpClosed && attendance !== "no" && <DietaryField className={s.field} />}
                {(rsvp.status === "error" || wishes.status === "error") && <p className={s.error} role="alert">Belum terkirim. Periksa koneksi lalu coba lagi.</p>}
                <button type="submit" className={`${s.btn} ${s.submit}`} disabled={sending}>{sending ? "Mengirim…" : "Kirim Doa & Konfirmasi"}</button>
              </form>
            )}
          </div>
          {wishes.wishes.length === 0 && <p className={s.empty}>Belum ada doa. Jadilah yang pertama mendoakan.</p>}
          <div className={s.wishes}>
            {wishes.wishes.slice(0, 10).map(wish => (
              <article key={wish.id} className={s.wish}>
                <div><strong>{wish.name}</strong>{wish.attendance && <small>{ATTEND[wish.attendance]}</small>}</div>
                <p>{wish.message}</p>
              </article>
            ))}
          </div>
        </section>

        {data.gifts.length > 0 && (
          <section className={s.section} aria-labelledby="sr-gift">
            <Head id="sr-gift" eyebrow="Tanda kasih">Hadiah</Head>
            <p className={s.lead}>Doa dan kehadiran Anda adalah hadiah terbaik. Bagi yang ingin memberi tanda kasih, dapat melalui:</p>
            {data.gifts.map(gift => {
              const info = giftInfo(gift);
              const on = Boolean(info.copy) && copied === info.copy;
              const icon = gift.type === "bank" ? ic.landmark : gift.type === "ewallet" ? ic.wallet : gift.type === "qris" ? ic.qrCode : ic.gift;
              return (
                <div key={gift.id} className={`${s.gift} ${on ? s.giftOn : ""}`}>
                  <span className={s.giftIcon}><Lucide icon={icon} size={20} /></span>
                  <div className={s.giftText}>
                    <small>{info.kind}</small>
                    <strong>{gift.type === "address" ? "Kirim ke rumah baru" : info.title}</strong>
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
          <House />
          <h2>Terima Kasih</h2>
          <p>Merupakan kebahagiaan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu untuk rumah baru kami.</p>
          <p className={s.wassalam}>Wassalamu&apos;alaikum Warahmatullahi Wabarakatuh</p>
          <strong>{hosts.family}</strong>
          <a href="/" target="_blank" rel="noreferrer" className={s.made}>dibuat dengan ♥ di Rawuh</a>
        </footer>
      </main>
    </ThemeShell>
  );
}
