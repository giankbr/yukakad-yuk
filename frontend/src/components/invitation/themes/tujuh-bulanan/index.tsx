"use client";
// Theme "Tujuh Bulanan" — syukuran mitoni: gading-merah muda, janur yang bergoyang, bokor kembang setaman, kelopak yang berguguran.
import { useEffect, useRef, useState, type CSSProperties, type FormEvent } from "react";
import {
  DietaryField, Extras, GuestCount, Lucide, Photo, ThemeShell, Tick, dateParts, formatDate, giftInfo, guestLabel, mapsHref,
  storyItems, toDate, useCopy, useCountdown, DATE_TBA, sentSummary, useRsvp, useThankYou, useWishes, type Attendance, type ThemeProps, type Wish,
} from "../kit";
import type { InvitationData } from "../../types";
import { tableLabel } from "../extras";
import { celebrate } from "@/lib/celebrate";
import { ic } from "./icons";
import s from "./styles.module.css";

const FONTS = ["Marcellus", "EB Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500", "Amiri:wght@400;700"];
const ATTEND: Record<Attendance, string> = { yes: "Hadir", maybe: "Ragu", no: "Berhalangan" };
const DEMO_WISHES: Wish[] = [
  { id: "w1", name: "Bude Narti", attendance: "yes", message: "Semoga Sekar sehat selalu, lancar sampai persalinan, dan dedek lahir sempurna menjadi anak yang sholeh-sholehah." },
  { id: "w2", name: "Rina & Yoga", attendance: "maybe", message: "Barakallah! Ikut bahagia menanti si kecil. Sehat-sehat ya ibu dan bayi." },
];
const RITES = [
  { title: "Siraman", body: "Calon ibu dimandikan oleh tujuh sesepuh dengan air kembang setaman, lambang menyucikan diri menyambut kelahiran." },
  { title: "Brojolan", body: "Sepasang cengkir gading diluncurkan dari balik kain, dengan harapan persalinan lancar dan bayi lahir dengan mudah." },
  { title: "Ganti tujuh busana", body: "Tujuh kain batik dicoba bergantian hingga yang sederhana dipilih, simbol kesahajaan dan kebaikan budi." },
  { title: "Dodol rujak & dawet", body: "Calon ibu menjual rujak dan dawet yang dibayar dengan kreweng, sebagai harapan rezeki yang mengalir." },
];
const HOPES = [
  "Semoga calon ibu senantiasa sehat, kuat, dan tenang hingga hari persalinan.",
  "Semoga si kecil tumbuh sempurna dan lahir dengan selamat.",
  "Semoga kelak menjadi anak yang sholeh-sholehah, berbakti, dan membawa kebaikan.",
];

/* ── Helpers ───────────────────────────────────────────────── */

function people(data: InvitationData) {
  return [
    { role: "Calon Ibu", short: data.couple.bride?.trim() ?? "", full: data.couple.brideFull?.trim(), parents: data.couple.brideParents?.trim(), photo: data.couple.bridePhoto },
    { role: "Calon Ayah", short: data.couple.groom?.trim() ?? "", full: data.couple.groomFull?.trim(), parents: data.couple.groomParents?.trim(), photo: data.couple.groomPhoto },
  ].filter(p => p.short || p.full).map(p => ({ ...p, short: p.short || p.full || "", full: p.full || p.short }));
}

function calendarHref(title: string, data: InvitationData) {
  const start = toDate(data.events[0]?.date ?? data.date);
  if (!start) return undefined;
  const last = toDate(data.events[data.events.length - 1]?.date) ?? start;
  const stamp = (d: Date) => d.toISOString().replace(/[-:]|\.\d{3}/g, "");
  const params = new URLSearchParams({ action: "TEMPLATE", text: title, dates: `${stamp(start)}/${stamp(new Date(Math.max(start.getTime(), last.getTime()) + 2 * 3600e3))}`, location: [data.place, data.address].filter(Boolean).join(", ") });
  return `https://calendar.google.com/calendar/render?${params.toString()}`;
}

function plainName(guest?: string) {
  if (!guest || guest === "Tamu Undangan") return "";
  return guest.replace(/^(bapak|ibu|bpk\.?|sdr\.?)\s+/i, "").replace(/\s*(&|dan)\s*keluarga$/i, "").trim();
}

/* ── Ornaments ─────────────────────────────────────────────── */

const ART = "/themes/art/tujuh-bulanan";
const PETAL_KINDS = ["rose", "white", "yellow"];

/** Painted (watercolour) decorative image — never opens the photo lightbox. */
function Art({ name, w, h, className, eager }: { name: string; w: number; h: number; className?: string; eager?: boolean }) {
  return (
    // eslint-disable-next-line @next/next/no-img-element -- static painted ornament
    <img src={`${ART}/${name}.webp`} alt="" aria-hidden width={w} height={h} className={className} data-nolightbox
      loading={eager ? "eager" : "lazy"} fetchPriority={eager ? "high" : undefined} decoding="async" draggable={false} />
  );
}

/** Woven janur band with hanging strips (each strip sways on its own). */
function Janur({ eager }: { eager?: boolean }) {
  const strips: [number, number][] = [[22, 1], [52, 2], [82, 0], [308, 0], [338, 2], [368, 1]];
  return (
    <div className={s.janur} aria-hidden>
      {strips.map(([x, kind]) => <span key={x} className={`${s.strip} ${s[`strip${kind}`]}`} style={{ left: `${(x / 390) * 100}%` }} />)}
      <Art name="janur" w={780} h={47} className={s.janurBand} eager={eager} />
    </div>
  );
}

function Petals() {
  return <div className={s.petals} aria-hidden>{Array.from({ length: 11 }, (_, i) => <i key={i} style={{ "--i": i, backgroundImage: `url(${ART}/petal-${PETAL_KINDS[i % PETAL_KINDS.length]}.webp)` } as CSSProperties} />)}</div>;
}

function Bloom() {
  return <Art name="bloom" w={80} h={79} className={s.bloom} />;
}

/** Bokor (brass bowl) of kembang setaman: rose, melati, kenanga and kantil floating on rippling water. */
function Bokor({ className, eager }: { className?: string; eager?: boolean }) {
  return (
    <div className={`${s.bokor} ${className ?? ""}`} aria-hidden data-nolightbox>
      <Art name="bokor" w={420} h={290} eager={eager} />
      <span className={s.ripple} />
      <span className={s.ripple} />
      <span className={s.floaty} />
    </div>
  );
}

function Head({ id, eyebrow, children }: { id: string; eyebrow?: string; children: string }) {
  return (
    <div className={s.head}>
      <Bloom />
      {eyebrow && <p className={s.eyebrow}>{eyebrow}</p>}
      <h2 id={id}>{children}</h2>
    </div>
  );
}

/* ── Theme ─────────────────────────────────────────────────── */

export default function TujuhBulananTheme({ data, slug, guestToken, demo, skipCover }: ThemeProps) {
  const pair = people(data);
  const names = pair.map(p => p.short).join(" & ") || "Keluarga Kami";
  const label = data.eventLabel?.trim() || "Syukuran Tujuh Bulanan";
  const parts = dateParts(data.date);
  const dotted = parts.day ? `${parts.weekday} · ${parts.day} ${parts.month} ${parts.year}` : DATE_TBA;
  const countdown = useCountdown(data.date);
  const rsvp = useRsvp({ slug, guestToken, demo });
  const wishes = useWishes({ slug, guestToken, demo, seed: DEMO_WISHES });
  const thanks = useThankYou();
  const rsvpClosed = thanks.active || rsvp.status === "closed";
  const { copy, copied } = useCopy();
  const stories = storyItems(data);
  const gallery = data.gallery.filter(Boolean);
  const [attendance, setAttendance] = useState<Attendance>("yes");
  const calendar = calendarHref(`${label} ${names}`, data);
  const table = tableLabel(data.guestTable);
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
      background="#efdcd5"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Petals />
          <Janur eager />
          <Bokor className={s.coverBokor} eager />
          <p className={s.coverKicker}>Tingkeban · Mitoni</p>
          <h1 className={s.coverTitle}>{label}</h1>
          <p className={s.coverNames}>{names}</p>
          <p className={s.coverDate}>{dotted.toUpperCase()}</p>
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
          <Petals />
          <Janur />
          <p className={s.heroKicker}>Tingkeban · Mitoni</p>
          <h1 className={s.heroTitle}>{label}</h1>
          <p className={s.heroNames}>{names}</p>
          <p className={s.heroDate}>{dotted.toUpperCase()}</p>
          <Bokor className={s.heroBokor} />
        </header>

        <section className={s.section} aria-label="Salam pembuka">
          <p className={s.salam}>Assalamu&apos;alaikum Warahmatullahi Wabarakatuh</p>
          <p className={s.lead}>{data.couple.note?.trim() || "Dengan memohon rahmat Allah SWT, kami bermaksud menyelenggarakan syukuran tujuh bulanan kandungan kami."} Kehadiran dan doa Bapak/Ibu/Saudara/i sangat kami harapkan.</p>
          <figure className={s.doa}>
            <p className={s.arabic} lang="ar">رَبِّ هَبْ لِي مِنْ لَدُنْكَ ذُرِّيَّةً طَيِّبَةً إِنَّكَ سَمِيعُ الدُّعَاءِ</p>
            <figcaption>
              <p className={s.doaText}>“Ya Tuhanku, berilah aku keturunan yang baik dari sisi-Mu. Sesungguhnya Engkau Maha Mendengar doa.”</p>
              <cite className={s.doaSrc}>QS. ALI &apos;IMRAN: 38</cite>
            </figcaption>
          </figure>
        </section>

        <Extras slot="opening" />

        <section className={`${s.section} ${s.blush}`} aria-labelledby="tb-parents">
          <Head id="tb-parents" eyebrow="Yang berbahagia">Calon Ayah &amp; Bunda</Head>
          <div className={s.parents}>
            {pair.map((person, index) => (
              <div key={person.role} className={s.person}>
                {index > 0 && <p className={s.amp} aria-hidden>&amp;</p>}
                <div className={s.oval}>{person.photo ? <Photo src={person.photo} alt={person.full} /> : <span aria-hidden>{person.short.slice(0, 1).toUpperCase()}</span>}</div>
                <p className={s.role}>{person.role}</p>
                <h3>{person.full}</h3>
                {person.parents && <p>{person.parents}</p>}
              </div>
            ))}
          </div>
        </section>

        <section className={s.section} aria-labelledby="tb-month">
          <Head id="tb-month" eyebrow="Usia kandungan">Tujuh Bulan Penantian</Head>
          <div className={s.month} role="img" aria-label="Usia kandungan tujuh dari sembilan bulan">
            <svg viewBox="0 0 100 100" aria-hidden="true">
              <circle className={s.track} cx="50" cy="50" r="44" pathLength={100} />
              <circle className={s.arc} cx="50" cy="50" r="44" pathLength={100} />
              {Array.from({ length: 9 }, (_, i) => <circle key={i} className={s.dot} cx={50 + 44 * Math.cos((i / 9) * 2 * Math.PI)} cy={50 + 44 * Math.sin((i / 9) * 2 * Math.PI)} r={i < 7 ? 2.2 : 1.4} opacity={i < 7 ? 1 : .35} />)}
            </svg>
            <div className={s.monthText}><b>7</b><small>dari 9 bulan</small></div>
          </div>
          {countdown.valid ? (
            <div className={s.count} role="timer" aria-label={`${countdown.days} hari ${countdown.hours} jam ${countdown.minutes} menit lagi`}>
              {([["Hari", countdown.days], ["Jam", countdown.hours], ["Menit", countdown.minutes], ["Detik", countdown.seconds]] as const).map(([unit, value]) => (
                <div key={unit}><b><Tick value={value} /></b><small>{unit}</small></div>
              ))}
            </div>
          ) : <p className={s.tba}>{DATE_TBA}</p>}
          {calendar && <a className={`${s.btn} ${s.btnSoft}`} href={calendar} target="_blank" rel="noreferrer"><Lucide icon={ic.calendarPlus} size={15} />Simpan ke Kalender</a>}
        </section>

        <section className={`${s.section} ${s.blush}`} aria-labelledby="tb-events">
          <Head id="tb-events" eyebrow="Waktu & tempat">Rangkaian Acara</Head>
          <div className={s.events}>
            {data.events.map((event, index) => {
              const href = mapsHref(data, event);
              return (
                <article key={event.name + index} className={s.event}>
                  <Bloom />
                  <h3>{event.name}</h3>
                  <p className={s.eventDate}>{formatDate(event.date || data.date)}</p>
                  {event.time && <p className={s.eventTime}>{event.time}</p>}
                  {event.venue && <strong>{event.venue}</strong>}
                  {event.address && <p>{event.address}</p>}
                  {href && <a className={s.mapLink} href={href} target="_blank" rel="noreferrer"><Lucide icon={ic.mapPin} size={13} />Petunjuk arah</a>}
                </article>
              );
            })}
          </div>
        </section>

        <Extras slot="event" without={["calendar"]} />

        <section className={s.section} aria-labelledby="tb-rites">
          <Head id="tb-rites" eyebrow="Adat Jawa">Makna Tingkeban</Head>
          <Art name="siraman" w={606} h={256} className={s.siraman} />
          <p className={s.lead}>Tingkeban digelar pada bulan ketujuh kehamilan anak pertama, dihiasi janur dan kembang setaman: mawar, melati, kenanga, dan kantil.</p>
          <ol className={s.rites}>
            {RITES.map((rite, index) => (
              <li key={rite.title} className={s.rite}>
                <span className={s.riteNo}>{index + 1}</span>
                <div><h3>{rite.title}</h3><p>{rite.body}</p></div>
              </li>
            ))}
          </ol>
        </section>

        {stories.length > 0 && (
          <section className={`${s.section} ${s.blush}`} aria-labelledby="tb-story">
            <Head id="tb-story" eyebrow="Cerita kami">{data.story?.title?.trim() && data.stories?.length ? data.story.title : "Menanti Buah Hati"}</Head>
            <ol className={s.timeline}>
              {stories.map((story, index) => (
                <li key={story.title + index}>
                  {story.date && <small>{story.date.toUpperCase()}</small>}
                  <h3>{story.title}</h3>
                  {story.body && <p>{story.body}</p>}
                  {story.image && <Photo src={story.image} alt={story.title} className={s.storyImg} />}
                </li>
              ))}
            </ol>
          </section>
        )}

        {gallery.length > 0 && (
          <section className={s.section} aria-labelledby="tb-gallery">
            <Head id="tb-gallery" eyebrow="Kenangan">Galeri</Head>
            <div className={s.gallery}>{gallery.map((src, index) => <Photo key={src + index} src={src} alt={`Foto ${index + 1}`} />)}</div>
          </section>
        )}

        <Extras slot="story" />

        <section className={s.section} aria-labelledby="tb-hopes">
          <Head id="tb-hopes" eyebrow="Doa & harapan">Untuk Ibu dan Bayi</Head>
          <ul className={s.hopes}>{HOPES.map(hope => <li key={hope}>{hope}</li>)}</ul>
        </section>

        <Extras slot="end" />

        <section className={`${s.section} ${s.blush}`} aria-labelledby="tb-rsvp">
          <Head id="tb-rsvp" eyebrow="Konfirmasi kehadiran">Doa &amp; Ucapan</Head>
          <div className={s.formCard}>
            {sent ? (
              <div ref={sentRef} className={s.sent} role="status">
                <span className={s.sentIcon}><Lucide icon={ic.check} size={22} strokeWidth={2.4} /></span>
                <strong>Matur nuwun</strong>
                <p>{demo ? "Ini pratinjau — jawaban contoh tidak dikirim." : sentSummary(rsvp, wishes)}</p>
                <button type="button" className={`${s.btn} ${s.btnSoft}`} onClick={() => { rsvp.reset(); wishes.reset(); }}>Tulis lagi</button>
              </div>
            ) : (
              <form className={s.form} onSubmit={onSubmit}>
                <label className={s.field}><span>Nama</span><input name="name" required maxLength={100} placeholder="Nama Anda" autoComplete="name" defaultValue={plainName(data.guestName)} /></label>
                <label className={s.field}><span>Doa untuk ibu &amp; bayi</span><textarea name="message" required={rsvpClosed} maxLength={500} rows={3} placeholder="Tuliskan doa terbaik Anda…" /></label>
                {rsvpClosed ? (
                  <div className={s.closed} role="status"><strong>Konfirmasi kehadiran sudah ditutup</strong><p>Acara telah berlangsung. Terima kasih atas doa dan perhatiannya. Doa masih bisa dikirim lewat form ini.</p></div>
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
                <button type="submit" className={`${s.btn} ${s.submit}`} disabled={sending}>{sending ? "Mengirim…" : "Kirim Doa"}</button>
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
          <section className={s.section} aria-labelledby="tb-gift">
            <Head id="tb-gift" eyebrow="Tanda kasih">Hadiah</Head>
            <p className={s.lead}>Doa restu Anda adalah hadiah terindah bagi kami dan si kecil. Bila berkenan memberi tanda kasih, dapat melalui:</p>
            {data.gifts.map(gift => {
              const info = giftInfo(gift);
              const on = Boolean(info.copy) && copied === info.copy;
              const icon = gift.type === "bank" ? ic.landmark : gift.type === "ewallet" ? ic.wallet : gift.type === "qris" ? ic.qrCode : ic.gift;
              return (
                <div key={gift.id} className={`${s.gift} ${on ? s.giftOn : ""}`}>
                  <span className={s.giftIcon}><Lucide icon={icon} size={20} /></span>
                  <div className={s.giftText}>
                    <small>{info.kind}</small>
                    <strong>{gift.type === "address" ? "Alamat kirim" : info.title}</strong>
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
          <Janur />
          <Bokor className={s.heroBokor} />
          <h2>Matur Nuwun</h2>
          <p>Merupakan kebahagiaan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan mendoakan keselamatan ibu dan bayi.</p>
          <p>Wassalamu&apos;alaikum Warahmatullahi Wabarakatuh</p>
          <strong>{names}</strong>
          <a href="/" target="_blank" rel="noreferrer" className={s.made}>dibuat dengan ♥ di Rawuh</a>
        </footer>
      </main>
    </ThemeShell>
  );
}
