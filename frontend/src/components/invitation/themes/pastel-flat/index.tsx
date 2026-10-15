"use client";
// Theme "Pastel Flat" — ilustrasi flat lucu, palet pink-pastel, kartu membulat.
import { Fragment, useEffect, useRef, useState, type FormEvent } from "react";
import {
  DietaryField, Extras, GuestCount, Lucide, Photo, ThemeShell, Tick, coupleLabel, dateParts, giftInfo, guestLabel,
  mapsHref, storyItems, toDate, useCopy, useCountdown, useRsvp, useWishes,
  type Attendance, type ThemeProps, type Wish,
} from "../kit";
import { celebrate, toast } from "@/lib/celebrate";
import { ic } from "./icons";
import s from "./styles.module.css";

const FONTS = ["Poppins:ital,wght@0,400;0,600;0,700;0,800;1,400"];
const ART = "/themes/img/a57.webp";
const ATTEND: Record<Attendance, string> = { yes: "Hadir", maybe: "Ragu", no: "Berhalangan" };
const DEMO_LABELS = ["Piknik", "Kue", "Sepeda"];
const DEMO_WISHES: Wish[] = [
  { id: "w1", name: "Vina", message: "Mira!!! Selamat ya sayang, gemes banget temanya.", attendance: "yes" },
  { id: "w2", name: "Pak Budi", message: "Selamat Mira & Bagas. Bahagia selalu.", attendance: "yes" },
];

/** The little heart between the couple cards: tap to send love (purely decorative, local state only). */
function LoveButton() {
  const [count, setCount] = useState(0);
  const [bursts, setBursts] = useState<number[]>([]);
  const onTap = () => {
    const id = Date.now();
    setCount(value => value + 1);
    setBursts(list => [...list.slice(-5), id]);
    window.setTimeout(() => setBursts(list => list.filter(item => item !== id)), 1100);
    if (count === 0) toast("Cinta terkirim untuk kedua mempelai");
  };
  return (
    <button type="button" className={`${s.heart} ${count > 0 ? s.heartOn : ""}`} onClick={onTap} aria-label="Kirim cinta untuk mempelai">
      <span key={count} className={s.heartIcon} aria-hidden>♥</span>
      {count > 0 && <span className={s.heartCount} aria-hidden><Tick value={count} /></span>}
      {bursts.map(id => (
        <span key={id} className={s.heartBurst} aria-hidden><i>♥</i><i>♥</i><i>♥</i><i>♥</i><i>♥</i></span>
      ))}
    </button>
  );
}

function Head({ id, children }: { id: string; children: string }) {
  return (
    <div className={s.head}>
      <h2 id={id}>{children}</h2>
      <span className={s.divider} aria-hidden><i /><b /><i /></span>
    </div>
  );
}

/** "MINGGU · 14 FEBRUARI 2027" */
function dotDate(value?: string) {
  const p = dateParts(value);
  return (p.day ? `${p.weekday} · ${p.day} ${p.month} ${p.year}` : (value ?? "")).toUpperCase();
}

/** Father's name from "Putri Bapak Anton & Ibu Rini" → "Anton". */
function familyName(parents?: string) {
  const match = parents?.match(/(?:Bapak|Bpk\.?|Bp\.?)\s+([^&,]+)/i);
  return match ? match[1].trim().split(/\s+/).pop() : undefined;
}

function calendarHref(title: string, start?: string, location?: string) {
  const date = toDate(start);
  if (!date) return undefined;
  const stamp = (d: Date) => d.toISOString().replace(/[-:]/g, "").replace(/\.\d{3}/, "");
  const end = new Date(date.getTime() + 3 * 3600e3);
  const params = new URLSearchParams({ action: "TEMPLATE", text: title, dates: `${stamp(date)}/${stamp(end)}`, location: location ?? "" });
  return `https://calendar.google.com/calendar/render?${params.toString()}`;
}

export default function PastelFlatTheme({ data, slug, guestToken, demo, skipCover }: ThemeProps) {
  const couple = coupleLabel(data);
  const label = data.eventLabel ?? "Pernikahan";
  const date = dotDate(data.date);
  const countdown = useCountdown(data.date);
  const rsvp = useRsvp({ slug, guestToken, demo });
  const wishes = useWishes({ slug, guestToken, demo, seed: DEMO_WISHES });
  const { copy, copied } = useCopy();
  const stories = storyItems(data);
  const gallery = data.gallery;
  // 4+ photos: three circles + one wide photo + the rest behind a toggle; fewer: wide photo first.
  const circles = gallery.length >= 4 ? gallery.slice(0, 3) : gallery.slice(1);
  const big = gallery.length >= 4 ? gallery[3] : gallery[0];
  const extra = gallery.length >= 4 ? gallery.slice(4) : [];
  const [showAll, setShowAll] = useState(false);
  const [attendance, setAttendance] = useState<Attendance>("yes");
  const maps = mapsHref(data, data.events[data.events.length - 1]);
  const calendar = calendarHref(`${label} ${couple}`, data.events[0]?.date ?? data.date, [data.place, data.address].filter(Boolean).join(", "));
  const families = [familyName(data.couple.brideParents) ?? data.couple.bride, familyName(data.couple.groomParents) ?? data.couple.groom];
  const sending = rsvp.status === "sending" || wishes.status === "sending";
  const sent = rsvp.status === "sent" || wishes.status === "sent";
  const sentRef = useRef<HTMLDivElement>(null);
  useEffect(() => { if (sent) celebrate(sentRef.current); }, [sent]);
  const pillTone = [undefined, s.pillBlue, s.pillYellow];

  const people = [
    { key: "bride", role: "Pengantin Wanita", tone: undefined, name: data.couple.brideFull ?? data.couple.bride, parents: data.couple.brideParents, photo: data.couple.bridePhoto ?? gallery[1] },
    { key: "groom", role: "Pengantin Pria", tone: s.pillBlue, name: data.couple.groomFull ?? data.couple.groom, parents: data.couple.groomParents, photo: data.couple.groomPhoto ?? gallery[2] },
  ];

  const onSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const form = new FormData(event.currentTarget);
    const name = String(form.get("name") ?? "").trim();
    const message = String(form.get("message") ?? "").trim();
    const guests = attendance === "no" ? 1 : Number(form.get("guests")) || 1;
    if (!name) return;
    void rsvp.submit({ name, attendance, guests, message, diet: String(form.get("diet") ?? "").trim() || undefined });
    if (message) void wishes.send(name, message);
  };

  return (
    <ThemeShell
      fonts={FONTS}
      background="#fbd9d6"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.coverBg} aria-hidden><Photo src={ART} /></div>
          <div className={s.confetti} aria-hidden><i /><i /><i /><i /><i /><i /></div>
          <div className={s.coverContent}>
            <p className={s.coverKicker}>Simpan tanggalnya</p>
            <h1 className={s.coverNames}>{couple}</h1>
            <p className={s.coverDate}>{date}</p>
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
          <div className={s.openingBg} aria-hidden><Photo src={ART} /></div>
          <div className={s.openingText}>
            <p className={s.openingKicker}>{label}</p>
            <h1>{couple}</h1>
            <p className={s.openingDate}>{date}</p>
          </div>
        </section>

        {data.couple.note && <p className={s.quote}>“{data.couple.note.replace(/^[“"]|[”"]$/g, "")}”</p>}

        <Extras slot="opening" />

        <section className={`${s.band} ${s.alt}`} aria-labelledby="pf-couple">
          <Head id="pf-couple">Mempelai</Head>
          <p className={`${s.lead} ${s.small}`}>Yeay! Kami mau nikah dan kamu diundang. Kenalan dulu sama kami:</p>
          {people.map((person, index) => (
            <Fragment key={person.key}>
              {index > 0 && <LoveButton />}
              <article className={`${s.person} ${index % 2 ? s.personRight : ""}`}>
                <Photo src={person.photo} alt={person.name} className={s.personPhoto} />
                <div className={s.personText}>
                  <span className={`${s.pill} ${person.tone ?? ""}`}>{person.role}</span>
                  <h3>{person.name}</h3>
                  {person.parents && <p>{person.parents}</p>}
                </div>
              </article>
            </Fragment>
          ))}
        </section>

        <section className={s.band} aria-labelledby="pf-count">
          <Head id="pf-count">Menuju Hari Bahagia</Head>
          <div className={s.count} role="timer" aria-label={`${countdown.days} hari ${countdown.hours} jam ${countdown.minutes} menit lagi`}>
            {([["Hari", countdown.days], ["Jam", countdown.hours], ["Menit", countdown.minutes], ["Detik", countdown.seconds]] as const).map(([unit, value]) => (
              <div key={unit} className={s.countBox}><b><Tick value={value} /></b><small>{unit}</small></div>
            ))}
          </div>
          {calendar && <a className={s.btn} href={calendar} target="_blank" rel="noreferrer"><Lucide icon={ic.calendarPlus} size={15} />Simpan ke Kalender</a>}
        </section>

        <section className={`${s.band} ${s.alt}`} aria-labelledby="pf-events">
          <Head id="pf-events">Rangkaian Acara</Head>
          {data.events.map((event, index) => (
            <article key={event.name + index} className={`${s.card} ${s.event}`}>
              <span className={s.iconDot}><Lucide icon={index === 0 ? ic.heartHandshake : ic.partyPopper} size={18} /></span>
              <h3>{event.name}</h3>
              <p className={s.eventDate}>{dotDate(event.date || data.date)}</p>
              {event.time && <b>{event.time}</b>}
              <strong>{event.venue}</strong>
              {event.address && <p className={s.eventAddr}>{event.address}</p>}
            </article>
          ))}
          {maps && <a className={s.btn} href={maps} target="_blank" rel="noreferrer"><Lucide icon={ic.mapPin} size={15} />Lihat Lokasi di Maps</a>}
        </section>

        <Extras slot="event" without={["calendar"]} />

        {stories.length > 0 && (
          <section className={s.band} aria-labelledby="pf-story">
            <Head id="pf-story">Kisah Kami</Head>
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
          <section className={`${s.band} ${s.alt}`} aria-labelledby="pf-gallery">
            <Head id="pf-gallery">Galeri</Head>
            {circles.length > 0 && (
              <div className={s.circles} data-count={circles.length}>
                {circles.map((src, index) => {
                  const caption = demo ? DEMO_LABELS[index] : undefined;
                  return (
                    <figure key={src + index} className={s.circle}>
                      <Photo src={src} alt={caption ?? `Foto ${index + 1}`} className={s.circleImg} />
                      {caption && <figcaption className={`${s.pill} ${pillTone[index] ?? ""}`}>{caption}</figcaption>}
                    </figure>
                  );
                })}
              </div>
            )}
            {big && (
              <div className={s.big}>
                <Photo src={big} alt={`Foto bersama ${couple}`} />
                {extra.length > 0 && (
                  <button type="button" className={s.more} aria-expanded={showAll} onClick={() => setShowAll(value => !value)}>
                    {showAll ? "Sembunyikan foto" : `Lihat ${extra.length} foto lainnya`}
                    <Lucide icon={ic.chevronDown} size={14} className={s.moreIcon} />
                  </button>
                )}
              </div>
            )}
            {showAll && extra.length > 0 && (
              <div className={s.grid}>
                {extra.map((src, index) => <Photo key={src + index} src={src} alt={`Foto ${index + 5} dari ${gallery.length}`} />)}
              </div>
            )}
          </section>
        )}

        <Extras slot="story" />

        <Extras slot="end" />

        {data.gifts.length > 0 && (
          <section className={s.band} aria-labelledby="pf-gift">
            <Head id="pf-gift">Kirim Kado</Head>
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
                    <button type="button" className={`${s.copy} ${copied === info.copy ? s.copied : ""}`} onClick={() => copy(info.copy)} aria-label={copied === info.copy ? "Tersalin" : `Salin ${info.title}`}>
                      <Lucide icon={copied === info.copy ? ic.check : ic.copy} size={16} />
                    </button>
                  )}
                </div>
              );
            })}
          </section>
        )}

        <section className={`${s.band} ${s.alt}`} aria-labelledby="pf-wish">
          <Head id="pf-wish">Ucapan &amp; RSVP</Head>
          <div className={`${s.card} ${s.formCard}`}>
            {sent ? (
              <div ref={sentRef} className={s.sent} role="status">
                <span className={s.iconDot}><Lucide icon={ic.check} size={18} /></span>
                <strong>Yeay, terima kasih!</strong>
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
                {attendance !== "no" && <GuestCount label="Jumlah tamu" className={s.guests} labelClassName={s.guestsLabel} buttonClassName={s.step} />}
                {attendance !== "no" && <DietaryField className={s.field} />}
                {(rsvp.status === "error" || wishes.status === "error") && <p className={s.error} role="alert">Belum terkirim. Periksa koneksi lalu coba lagi.</p>}
                <button type="submit" className={`${s.btn} ${s.submit}`} disabled={sending}>{sending ? "Mengirim…" : "Kirim Ucapan"}</button>
              </form>
            )}
          </div>
          {wishes.wishes.length === 0 && <p className={s.lead}>Belum ada ucapan. Jadilah yang pertama!</p>}
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
          <strong>Keluarga {families[0]} &amp; {families[1]}</strong>
          <a href="/" target="_blank" rel="noreferrer">dibuat dengan ♥ di Rawuh</a>
        </footer>
      </main>
    </ThemeShell>
  );
}
