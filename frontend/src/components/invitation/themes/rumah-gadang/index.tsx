"use client";
// Theme "Rumah Gadang" — undangan adat Minang: merah marun, emas, songket (design: Undangan — Tema Rumah Gadang (Sari & Fadli)).
import { useState, type FormEvent } from "react";
import {
  DietaryField, Extras, GuestCount, Lucide, Photo, ThemeShell, dateParts, giftInfo, guestLabel, mapsHref, storyItems,
  toDate, useCopy, useCountdown, useRsvp, useWishes, type Attendance, type ThemeProps, type Wish,
} from "../kit";
import type { GiftMethod, InvitationData } from "../../types";
import { ic } from "./icons";
import s from "./styles.module.css";

const FONTS = ["Cormorant Garamond:ital,wght@0,400;0,600;0,700;1,400", "Cinzel:wght@400;700"];
const DEMO_WISHES: Wish[] = [
  { id: "w1", name: "Uda Rizal", message: "Selamat berumah tangga, Sari & Fadli! Semoga samawa.", attendance: "yes" },
  { id: "w2", name: "Etek Nurma", message: "Barakallah. Semoga lancar sampai hari H.", attendance: "yes" },
];
const ATTEND: Record<Attendance, string> = { yes: "Hadir", maybe: "Ragu", no: "Berhalangan" };

function lastPart(address: string) {
  const parts = address.split(",").map(part => part.trim()).filter(Boolean);
  return parts[parts.length - 1] ?? "";
}

/** "Putri dari Bapak Rusli Chaniago & Ibu …" → "Chaniago" (family name for the closing line). */
function familyName(parents?: string) {
  const match = parents?.match(/(?:Bapak|Bpk\.?|Bp\.?)\s+([^&]+)/i);
  const words = match?.[1].trim().split(/\s+/) ?? [];
  return words[words.length - 1];
}

function longDay(value?: string) {
  const p = dateParts(value);
  return p.day ? `${p.weekday} · ${p.day} ${p.month} ${p.year}`.toUpperCase() : (value ?? "").toUpperCase();
}

function calendarHref(data: InvitationData) {
  const start = toDate(data.date);
  if (!start) return undefined;
  const end = new Date(start.getTime() + 4 * 3600e3);
  const fmt = (d: Date) => d.toISOString().replace(/[-:]/g, "").replace(/\.\d{3}/, "");
  const params = new URLSearchParams({
    action: "TEMPLATE",
    text: `${data.eventLabel ?? "Pernikahan"} ${data.couple.bride} & ${data.couple.groom}`,
    dates: `${fmt(start)}/${fmt(end)}`,
    location: [data.place, data.address].filter(Boolean).join(", "),
  });
  return `https://calendar.google.com/calendar/render?${params.toString()}`;
}

function giftIcon(gift: GiftMethod) {
  return gift.type === "bank" ? ic.landmark : gift.type === "ewallet" ? ic.wallet : gift.type === "qris" ? ic.qrCode : ic.gift;
}

function Divider() {
  return <span className={s.divider} aria-hidden><i /><b /><i /></span>;
}

function Head({ id, children }: { id: string; children: string }) {
  return <div className={s.head}><h2 id={id}>{children}</h2><Divider /></div>;
}

export default function RumahGadangTheme({ data, slug, guestToken, demo, skipCover }: ThemeProps) {
  const couple = `${data.couple.bride} & ${data.couple.groom}`;
  const day = longDay(data.date);
  const city = lastPart(data.address);
  const countdown = useCountdown(data.date);
  const rsvp = useRsvp({ slug, guestToken, demo });
  const wishes = useWishes({ slug, guestToken, demo, seed: DEMO_WISHES });
  const { copy, copied } = useCopy();
  const stories = storyItems(data);
  const hero = data.gallery[0];
  const gallery = data.gallery.length > 3 ? data.gallery.slice(1) : data.gallery;
  const [main, ...rest] = gallery;
  const side = rest.slice(0, 2);
  const extra = rest.slice(2);
  const coverLabel = data.events[data.events.length - 1]?.name ?? data.eventLabel ?? "Pernikahan";
  const families = [familyName(data.couple.brideParents) ?? data.couple.bride, familyName(data.couple.groomParents) ?? data.couple.groom];
  const calendar = calendarHref(data);
  const maps = mapsHref(data, data.events[data.events.length - 1]);
  const [attendance, setAttendance] = useState<Attendance>("yes");
  const guestDefault = data.guestName && data.guestName !== "Tamu Undangan" ? data.guestName : "";

  const people = [
    { name: data.couple.brideFull ?? data.couple.bride, parents: data.couple.brideParents, photo: data.couple.bridePhoto ?? data.gallery[1] },
    { name: data.couple.groomFull ?? data.couple.groom, parents: data.couple.groomParents, photo: data.couple.groomPhoto ?? data.gallery[2] },
  ];

  const onSend = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const form = new FormData(event.currentTarget);
    const name = String(form.get("name") ?? "").trim();
    const message = String(form.get("message") ?? "").trim();
    const guests = attendance === "no" ? 1 : Number(form.get("guests") ?? 1) || 1;
    if (!name || !message) return;
    void rsvp.submit({ name, attendance, guests, message, diet: String(form.get("diet") ?? "").trim() || undefined });
    void wishes.send(name, message);
  };

  return (
    <ThemeShell
      fonts={FONTS}
      background="#2a0509"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.coverBg} aria-hidden><Photo src={hero} /></div>
          <div className={s.coverBorder} aria-hidden />
          <div className={s.coverContent}>
            <p className={s.kicker}>{coverLabel.toUpperCase()}</p>
            <h1 className={s.coverNames}>{couple}</h1>
            <p className={s.coverDate}>{[day, city.toUpperCase()].filter(Boolean).join(" · ")}</p>
            <div className={s.kepada}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
            </div>
            <button type="button" className={s.pill} onClick={open}><Lucide icon={ic.mailOpen} size={15} />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <main className={s.page}>
        <section className={s.opening} aria-label="Pembuka">
          <Photo src={hero} alt={`Foto ${couple}`} className={s.openingImg} />
          <div className={s.openingText}>
            <p className={s.kickerSm}>{(data.eventLabel ?? "Pernikahan").toUpperCase()}</p>
            <h1>{couple}</h1>
            <p className={s.openingDate}>{day}</p>
          </div>
        </section>

        {data.couple.note && <blockquote className={s.quote}>“{data.couple.note}”</blockquote>}

        <Extras slot="opening" />

        <section className={`${s.section} ${s.alt}`} aria-labelledby="rg-couple">
          <Head id="rg-couple">Mempelai</Head>
          <p className={s.lead}>Dengan memohon rahmat Allah SWT, kami bermaksud menyelenggarakan pernikahan putra-putri kami:</p>
          <div className={s.pair}>
            {people.map((person, index) => (
              <div key={index} className={s.pairCell}>
                {index === 1 && <span className={s.amp} aria-hidden>&amp;</span>}
                <article className={s.person}>
                  <div className={s.arch}><Photo src={person.photo} alt={person.name} /></div>
                  <h3>{person.name}</h3>
                  {person.parents && <p>{person.parents}</p>}
                </article>
              </div>
            ))}
          </div>
        </section>

        <section className={s.section} aria-labelledby="rg-count">
          <Head id="rg-count">Menuju Hari Bahagia</Head>
          <div className={s.count} role="timer" aria-label={`${countdown.days} hari ${countdown.hours} jam ${countdown.minutes} menit ${countdown.seconds} detik lagi`}>
            {([[countdown.days, "Hari"], [countdown.hours, "Jam"], [countdown.minutes, "Menit"], [countdown.seconds, "Detik"]] as const).map(([value, label]) => (
              <div key={label} className={s.countBox} aria-hidden><b>{value}</b><span>{label}</span></div>
            ))}
          </div>
          {calendar && <a className={s.pill} href={calendar} target="_blank" rel="noreferrer"><Lucide icon={ic.calendarPlus} size={15} />Simpan ke Kalender</a>}
        </section>

        <section className={`${s.section} ${s.alt}`} aria-labelledby="rg-events">
          <Head id="rg-events">Rangkaian Acara</Head>
          {data.events.map((event, index) => (
            <article key={event.name + index} className={s.event}>
              <span className={s.iconDot}><Lucide icon={index === 0 ? ic.heartHandshake : ic.partyPopper} size={18} /></span>
              <h3>{event.name.toUpperCase()}</h3>
              <p className={s.eventDate}>{longDay(event.date)}</p>
              <p className={s.eventTime}>{event.time}</p>
              <p className={s.eventVenue}>{event.venue}</p>
              {event.address && <p className={s.eventAddr}>{event.address}</p>}
            </article>
          ))}
          {maps && <a className={s.pill} href={maps} target="_blank" rel="noreferrer"><Lucide icon={ic.mapPin} size={15} />Lihat Lokasi di Maps</a>}
        </section>

        <Extras slot="event" without={["calendar"]} />

        {stories.length > 0 && (
          <section className={s.section} aria-labelledby="rg-story">
            <Head id="rg-story">Kisah Kami</Head>
            <ol className={s.stories}>
              {stories.map((story, index) => (
                <li key={story.title + index} className={s.story}>
                  <span className={s.year}>{story.date ?? String(index + 1).padStart(2, "0")}</span>
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

        {main && (
          <section className={`${s.section} ${s.alt}`} aria-labelledby="rg-gallery">
            <Head id="rg-gallery">Galeri</Head>
            <div className={s.masonry}>
              <div className={`${s.frame} ${s.tall}`}><Photo src={main} alt="Foto galeri 1" /></div>
              {side.length > 0 && (
                <div className={s.stack}>
                  {side.map((src, index) => <div key={src + index} className={s.frame}><Photo src={src} alt={`Foto galeri ${index + 2}`} /></div>)}
                </div>
              )}
            </div>
            {extra.length > 0 && (
              <div className={s.more}>
                {extra.map((src, index) => <div key={src + index} className={s.frame}><Photo src={src} alt={`Foto galeri ${index + 4}`} /></div>)}
              </div>
            )}
            {demo && <p className={s.caption}>“Bukittinggi, tempat semuanya bermula.”</p>}
          </section>
        )}

        <Extras slot="story" />

        <Extras slot="end" />

        {data.gifts.length > 0 && (
          <section className={s.section} aria-labelledby="rg-gift">
            <Head id="rg-gift">Kirim Kado</Head>
            <p className={s.lead}>Doa restu Anda adalah hadiah terindah. Jika ingin memberi tanda kasih, dapat melalui:</p>
            {data.gifts.map(gift => {
              const info = giftInfo(gift);
              const [line1, ...line2] = gift.type === "address" ? info.number.split(",") : [info.number];
              const sub = gift.type === "address" ? line2.join(",").trim() : info.holder ? `a.n. ${info.holder}` : "";
              return (
                <div key={gift.id} className={s.gift}>
                  <span className={s.iconDot}><Lucide icon={giftIcon(gift)} size={18} /></span>
                  <div className={s.giftText}>
                    <small>{gift.type === "address" ? "Kirim Kado" : info.title}</small>
                    {line1 && <strong>{line1.trim()}</strong>}
                    {sub && <span>{sub}</span>}
                    {info.image && <Photo src={info.image} alt="Kode QRIS" className={s.qris} />}
                  </div>
                  {info.copy && (
                    <button type="button" className={s.copy} onClick={() => copy(info.copy)} aria-label={copied === info.copy ? "Tersalin" : `Salin ${gift.type === "address" ? "alamat" : "nomor"}`}>
                      <Lucide icon={copied === info.copy ? ic.check : ic.copy} size={16} />
                    </button>
                  )}
                </div>
              );
            })}
          </section>
        )}

        <section className={`${s.section} ${s.alt}`} aria-labelledby="rg-wish">
          <Head id="rg-wish">Ucapan &amp; RSVP</Head>
          {wishes.status === "sent" ? (
            <div className={s.card} role="status">
              <p className={s.sent}>Terima kasih! {demo ? "Ini pratinjau — ucapanmu muncul di daftar." : "Ucapan dan konfirmasimu sudah kami terima."}</p>
              <button type="button" className={s.pillWide} onClick={() => { wishes.reset(); rsvp.reset(); }}>Tulis Lagi</button>
            </div>
          ) : (
            <form className={s.card} onSubmit={onSend}>
              <label className={s.field}><span>Nama</span><input name="name" required maxLength={100} defaultValue={guestDefault} placeholder="Nama Anda" autoComplete="name" /></label>
              <label className={s.field}><span>Ucapan</span><textarea name="message" required maxLength={500} rows={3} placeholder="Tulis doa & ucapan…" /></label>
              <fieldset className={s.choices}>
                <legend className={s.srOnly}>Kehadiran</legend>
                {(["yes", "maybe", "no"] as const).map(value => (
                  <label key={value} className={attendance === value ? s.on : undefined}>
                    <input type="radio" name="attendance" value={value} checked={attendance === value} onChange={() => setAttendance(value)} />
                    {ATTEND[value]}
                  </label>
                ))}
              </fieldset>
              {attendance !== "no" && <GuestCount label="Jumlah tamu" className={s.guests} labelClassName={s.guestsLabel} buttonClassName={s.step} />}
              {attendance !== "no" && <DietaryField className={`${s.field} ${s.diet}`} />}
              {wishes.status === "error" && <p className={s.error} role="alert">Belum terkirim. Periksa koneksi lalu coba lagi.</p>}
              <button type="submit" className={s.pillWide} disabled={wishes.status === "sending"}>{wishes.status === "sending" ? "Mengirim…" : "Kirim Ucapan"}</button>
            </form>
          )}
          {wishes.wishes.slice(0, 8).map(wish => (
            <article key={wish.id} className={s.wish}>
              <div><strong>{wish.name}</strong>{wish.attendance && <span>{ATTEND[wish.attendance]}</span>}</div>
              <p>{wish.message}</p>
            </article>
          ))}
        </section>

        <footer className={s.closing}>
          <h2>Terima Kasih</h2>
          <p>Merupakan suatu kehormatan dan kebahagiaan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir.</p>
          <p className={s.families}>KELUARGA BESAR<br />{families.join(" & ").toUpperCase()}</p>
          <a href="/" target="_blank" rel="noreferrer" className={s.credit}>dibuat dengan ♥ di Rawuh</a>
        </footer>
      </main>

    </ThemeShell>
  );
}

