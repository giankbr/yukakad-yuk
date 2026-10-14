"use client";
// Theme "Malam Rimba" — elegan gelap, dedaunan rimba, aksen emas dan bingkai lengkung.
import { useState, type FormEvent } from "react";
import {
  Lucide, Photo, ThemeShell, coupleLabel, dateParts, giftInfo, guestLabel,
  mapsHref, storyItems, toDate, useCopy, useCountdown, useRsvp, useWishes,
  type Attendance, type ThemeProps, type Wish,
} from "../kit";
import { ic } from "./icons";
import s from "./styles.module.css";

const FONTS = ["Playfair Display:ital,wght@0,400;1,400", "Cinzel:wght@400;700", "Cormorant Garamond:ital,wght@0,400;0,600;0,700;1,400"];
const FOREST = "/themes/img/a51.webp";
const ATTEND: Record<Attendance, string> = { yes: "Hadir", maybe: "Ragu", no: "Berhalangan" };
const DEMO_CAPTIONS = ["Rumah Kaca, Dago", "Cincin", "Malam di Rimba"];
const DEMO_WISHES: Wish[] = [
  { id: "w1", name: "Raka", message: "Selamat Kirana & Arsen! Undangannya gelap-gelap elegan.", attendance: "yes" },
  { id: "w2", name: "Tante Yuni", message: "Semoga rumah tangganya rindang seperti rimba.", attendance: "yes" },
];

function Head({ id, children }: { id: string; children: string }) {
  return (
    <div className={s.head}>
      <h2 id={id}>{children}</h2>
      <span className={s.divider} aria-hidden><i /><b /><i /></span>
    </div>
  );
}

/** "Sabtu · 12 Desember 2026" */
function dotDate(value?: string) {
  const p = dateParts(value);
  return p.day ? `${p.weekday} · ${p.day} ${p.month} ${p.year}` : (value ?? "");
}

/** Father's family name from "Putri dari Bapak Hendra Gunawan & Ibu Sinta" → "Gunawan". */
function familyName(parents?: string) {
  const match = parents?.match(/(?:Bapak|Bpk\.?|Bp\.?)\s+([^&,]+)/i);
  return match ? match[1].trim().split(/\s+/).pop() : undefined;
}

function city(address?: string) {
  const parts = (address ?? "").split(",").map(part => part.trim()).filter(Boolean);
  return parts.length > 1 ? parts[parts.length - 1] : "";
}

function calendarHref(title: string, start?: string, location?: string) {
  const date = toDate(start);
  if (!date) return undefined;
  const stamp = (d: Date) => d.toISOString().replace(/[-:]/g, "").replace(/\.\d{3}/, "");
  const end = new Date(date.getTime() + 3 * 3600e3);
  const params = new URLSearchParams({ action: "TEMPLATE", text: title, dates: `${stamp(date)}/${stamp(end)}`, location: location ?? "" });
  return `https://calendar.google.com/calendar/render?${params.toString()}`;
}

export default function MalamRimbaTheme({ data, slug, guestToken, demo, skipCover }: ThemeProps) {
  const couple = coupleLabel(data);
  const label = data.eventLabel ?? "Pernikahan";
  const date = dotDate(data.date);
  const where = city(data.address);
  const countdown = useCountdown(data.date);
  const rsvp = useRsvp({ slug, guestToken, demo });
  const wishes = useWishes({ slug, guestToken, demo, seed: DEMO_WISHES });
  const { copy, copied } = useCopy();
  const stories = storyItems(data);
  const gallery = data.gallery;
  const [attendance, setAttendance] = useState<Attendance>("yes");
  const maps = mapsHref(data, data.events[data.events.length - 1]);
  const calendar = calendarHref(`${label} ${couple}`, data.events[0]?.date ?? data.date, [data.place, data.address].filter(Boolean).join(", "));
  const families = [familyName(data.couple.brideParents) ?? data.couple.bride, familyName(data.couple.groomParents) ?? data.couple.groom];
  const sending = rsvp.status === "sending" || wishes.status === "sending";
  const sent = rsvp.status === "sent" || wishes.status === "sent";

  const people = [
    { key: "bride", role: "Mempelai Wanita", name: data.couple.brideFull ?? data.couple.bride, parents: data.couple.brideParents, photo: data.couple.bridePhoto ?? gallery[1] },
    { key: "groom", role: "Mempelai Pria", name: data.couple.groomFull ?? data.couple.groom, parents: data.couple.groomParents, photo: data.couple.groomPhoto ?? gallery[2] },
  ];

  const onSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const form = new FormData(event.currentTarget);
    const name = String(form.get("name") ?? "").trim();
    const message = String(form.get("message") ?? "").trim();
    if (!name) return;
    void rsvp.submit({ name, attendance, guests: 1, message });
    if (message) void wishes.send(name, message);
  };

  return (
    <ThemeShell
      fonts={FONTS}
      background="#060806"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.coverBg} aria-hidden><Photo src={FOREST} /></div>
          <div className={s.arch} aria-hidden />
          <div className={s.coverContent}>
            <p className={s.coverKicker}>{label}</p>
            <h1 className={s.coverNames}>{couple}</h1>
            <p className={s.coverDate}>{[date, where].filter(Boolean).join(" · ")}</p>
            <div className={s.kepada}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
            </div>
            <button type="button" className={s.btn} onClick={open}><Lucide icon={ic.mailOpen} size={15} />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <main className={s.page}>
        <section className={s.opening} aria-label="Pembuka">
          <div className={s.openingBg} aria-hidden><Photo src={FOREST} /></div>
          <div className={s.openingText}>
            <p className={s.openingKicker}>{label}</p>
            <h1>{couple}</h1>
            <p className={s.openingDate}>{date}</p>
          </div>
        </section>

        {data.couple.note && <p className={s.quote}>“{data.couple.note.replace(/^[“"]|[”"]$/g, "")}”</p>}

        <section className={`${s.band} ${s.alt} ${s.bleed}`} aria-labelledby="mr-couple">
          <div className={s.headWrap}>
            <Head id="mr-couple">Mempelai</Head>
            <p className={s.lead}>Dengan penuh rasa syukur, kami mengundang Anda untuk hadir pada {label.toLowerCase()} kami:</p>
          </div>
          {people.map((person, index) => (
            <article key={person.key} className={`${s.portrait} ${index % 2 ? s.portraitRight : ""}`}>
              <Photo src={person.photo} alt={person.name} />
              <div className={s.portraitText}>
                <small>{person.role}</small>
                <h3>{person.name}</h3>
                {person.parents && <p>{person.parents}</p>}
              </div>
            </article>
          ))}
        </section>

        <section className={s.band} aria-labelledby="mr-count">
          <Head id="mr-count">Menuju Hari Bahagia</Head>
          <div className={s.count} role="timer" aria-label={`${countdown.days} hari ${countdown.hours} jam ${countdown.minutes} menit lagi`}>
            {([["Hari", countdown.days], ["Jam", countdown.hours], ["Menit", countdown.minutes], ["Detik", countdown.seconds]] as const).map(([unit, value]) => (
              <div key={unit} className={s.countBox}><b>{value}</b><small>{unit}</small></div>
            ))}
          </div>
          {calendar && <a className={s.btn} href={calendar} target="_blank" rel="noreferrer"><Lucide icon={ic.calendarPlus} size={15} />Simpan ke Kalender</a>}
        </section>

        <section className={`${s.band} ${s.alt}`} aria-labelledby="mr-events">
          <Head id="mr-events">Rangkaian Acara</Head>
          {data.events.map((event, index) => (
            <article key={event.name + index} className={`${s.card} ${s.event}`}>
              <span className={s.iconDot}><Lucide icon={index === 0 ? ic.heartHandshake : ic.partyPopper} size={18} /></span>
              <h3>{event.name}</h3>
              <p className={s.eventDate}>{dotDate(event.date || data.date).toUpperCase()}</p>
              {event.time && <b>{event.time}</b>}
              <strong>{event.venue}</strong>
              {event.address && <p className={s.eventAddr}>{event.address}</p>}
            </article>
          ))}
          {maps && <a className={s.btn} href={maps} target="_blank" rel="noreferrer"><Lucide icon={ic.mapPin} size={15} />Lihat Lokasi di Maps</a>}
        </section>

        {stories.length > 0 && (
          <section className={s.band} aria-labelledby="mr-story">
            <Head id="mr-story">Kisah Kami</Head>
            <ol className={s.stories}>
              {stories.map((story, index) => (
                <li key={story.title + index} className={s.story}>
                  <span className={s.year}>{story.date || String(index + 1).padStart(2, "0")}</span>
                  <div>
                    <h3>{story.title}</h3>
                    <p>{story.body}</p>
                    {story.image && <Photo src={story.image} alt={story.title} className={s.storyImg} />}
                  </div>
                </li>
              ))}
            </ol>
          </section>
        )}

        {gallery.length > 0 && (
          <section className={`${s.band} ${s.alt} ${s.bleed}`} aria-labelledby="mr-gallery">
            <div className={s.headWrap}><Head id="mr-gallery">Galeri</Head></div>
            <div className={s.galleryList}>
              {gallery.map((src, index) => {
                const caption = demo ? DEMO_CAPTIONS[index] : undefined;
                return (
                  <figure key={src + index} className={s.shot} style={{ margin: 0 }}>
                    <Photo src={src} alt={caption ?? `Foto ${index + 1} dari ${gallery.length}`} />
                    {caption && <span>{caption}</span>}
                    <b aria-hidden>{String(index + 1).padStart(2, "0")}</b>
                  </figure>
                );
              })}
            </div>
          </section>
        )}

        {data.gifts.length > 0 && (
          <section className={s.band} aria-labelledby="mr-gift">
            <Head id="mr-gift">Kirim Kado</Head>
            <p className={s.lead}>Doa restu Anda adalah hadiah terindah. Jika ingin memberi tanda kasih, dapat melalui:</p>
            {data.gifts.map(gift => {
              const info = giftInfo(gift);
              const [line, ...rest] = gift.type === "address" ? info.number.split(",") : [info.number];
              const sub = gift.type === "address" ? rest.join(",").trim() : info.holder ? `a.n. ${info.holder}` : "";
              const icon = gift.type === "bank" ? ic.landmark : gift.type === "ewallet" ? ic.wallet : gift.type === "qris" ? ic.qrCode : ic.gift;
              return (
                <div key={gift.id} className={`${s.card} ${s.gift}`}>
                  <span className={s.iconDot}><Lucide icon={icon} size={18} /></span>
                  <div className={s.giftText}>
                    <small>{gift.type === "address" ? "Kirim Kado" : info.title}</small>
                    {line && <strong>{line.trim()}</strong>}
                    {sub && <span>{sub}</span>}
                    {info.image && <Photo src={info.image} alt="Kode QRIS" className={s.qris} />}
                  </div>
                  {info.copy && (
                    <button type="button" className={s.copy} onClick={() => copy(info.copy)} aria-label={copied === info.copy ? "Tersalin" : `Salin ${info.title}`}>
                      <Lucide icon={copied === info.copy ? ic.check : ic.copy} size={16} />
                    </button>
                  )}
                </div>
              );
            })}
          </section>
        )}

        <section className={`${s.band} ${s.alt}`} aria-labelledby="mr-wish">
          <Head id="mr-wish">Ucapan &amp; RSVP</Head>
          <div className={`${s.card} ${s.formCard}`}>
            {sent ? (
              <div className={s.sent} role="status">
                <span className={s.iconDot}><Lucide icon={ic.check} size={18} /></span>
                <strong>Terima kasih</strong>
                <p>{demo ? "Ini pratinjau — jawaban contoh tidak dikirim." : "Konfirmasi dan ucapanmu sudah kami terima."}</p>
                <button type="button" className={s.btn} onClick={() => { rsvp.reset(); wishes.reset(); }}>Tulis lagi</button>
              </div>
            ) : (
              <form className={s.form} onSubmit={onSubmit}>
                <label className={s.field}>Nama
                  <input name="name" required maxLength={100} placeholder="Nama Anda" autoComplete="name"
                    defaultValue={data.guestName && data.guestName !== "Tamu Undangan" ? data.guestName : ""} />
                </label>
                <label className={s.field}>Ucapan
                  <textarea name="message" maxLength={500} rows={3} placeholder="Tulis doa & ucapan…" />
                </label>
                <fieldset className={s.choices}>
                  <legend className={s.srOnly}>Kehadiran</legend>
                  {(Object.keys(ATTEND) as Attendance[]).map(key => (
                    <label key={key} className={attendance === key ? s.chosen : undefined}>
                      <input type="radio" name="attendance" value={key} checked={attendance === key} onChange={() => setAttendance(key)} />
                      {ATTEND[key]}
                    </label>
                  ))}
                </fieldset>
                {(rsvp.status === "error" || wishes.status === "error") && <p className={s.error} role="alert">Belum terkirim. Periksa koneksi lalu coba lagi.</p>}
                <button type="submit" className={`${s.btn} ${s.submit}`} disabled={sending}>{sending ? "Mengirim…" : "Kirim Ucapan"}</button>
              </form>
            )}
          </div>
          {wishes.wishes.length === 0 && <p className={s.lead}>Belum ada ucapan. Jadilah yang pertama.</p>}
          {wishes.wishes.slice(0, 8).map(wish => (
            <article key={wish.id} className={`${s.card} ${s.wish}`}>
              <div><strong>{wish.name}</strong>{wish.attendance && <small>{ATTEND[wish.attendance]}</small>}</div>
              <p>{wish.message}</p>
            </article>
          ))}
        </section>

        <footer className={s.closing}>
          <h2>Terima Kasih</h2>
          <p>Merupakan suatu kehormatan dan kebahagiaan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir.</p>
          <strong>Keluarga Besar<br />{families[0]} &amp; {families[1]}</strong>
          <a href="/" target="_blank" rel="noreferrer">dibuat dengan ♥ di Rawuh</a>
        </footer>
      </main>
    </ThemeShell>
  );
}
