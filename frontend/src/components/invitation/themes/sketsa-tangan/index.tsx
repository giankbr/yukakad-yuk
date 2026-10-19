"use client";
// Theme "Sketsa Tangan" — line art di atas kertas krem, foto ala scrapbook dengan selotip.
import { useEffect, useRef, useState, type FormEvent } from "react";
import {
  DietaryField, Extras, GuestCount, Lucide, Photo, ThemeShell, Tick, coupleLabel, formatDate, giftInfo, guestLabel,
  mapsHref, storyItems, toDate, useCopy, useCountdown, sentSummary, DATE_TBA, useRsvp, useThankYou, useWishes,
  type Attendance, type ThemeProps, type Wish,
} from "../kit";
import { celebrate } from "@/lib/celebrate";
import { ic } from "./icons";
import s from "./styles.module.css";

const FONTS = ["Caveat:wght@400;700", "Nunito:ital,wght@0,400;0,600;0,700;1,400"];
const ART = "/themes/img/a53.webp";
const ATTEND: Record<Attendance, string> = { yes: "Hadir", maybe: "Ragu", no: "Berhalangan" };
const DEMO_WISHES: Wish[] = [
  { id: "w1", name: "Dimas", message: "Akhirnyaaa! Selamat Tara & Gilang, lucu banget undangannya.", attendance: "yes" },
  { id: "w2", name: "Bu Guru Ani", message: "Selamat ya, dulu satu bangku sekarang satu rumah.", attendance: "yes" },
];

function Head({ id, children }: { id: string; children: string }) {
  return (
    <div className={s.head}>
      <h2 id={id}>{children}</h2>
      <svg className={s.squiggle} viewBox="0 0 120 14" aria-hidden focusable="false">
        <path d="M3 8 C 12 3, 19 12, 29 7 S 47 2, 57 7 S 76 12, 86 7 S 105 2, 117 7" pathLength={1} />
      </svg>
    </div>
  );
}

/** Father's family name from "anak Bapak Kusuma & Ibu Wati" → "Kusuma". */
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

export default function SketsaTanganTheme({ data, slug, guestToken, demo, skipCover }: ThemeProps) {
  const couple = coupleLabel(data);
  const label = data.eventLabel ?? "Pernikahan";
  const longDate = formatDate(data.date);
  const countdown = useCountdown(data.date);
  const rsvp = useRsvp({ slug, guestToken, demo });
  const wishes = useWishes({ slug, guestToken, demo, seed: DEMO_WISHES });
  const thanks = useThankYou();
  // Thank-you mode (or the server already closed RSVPs): only wishes can still be sent.
  const rsvpClosed = thanks.active || rsvp.status === "closed";
  const { copy, copied } = useCopy();
  const stories = storyItems(data);
  const gallery = data.gallery;
  const scrap = gallery.slice(0, 3);
  const [attendance, setAttendance] = useState<Attendance>("yes");
  const maps = mapsHref(data, data.events[data.events.length - 1]);
  const calendar = calendarHref(`${label} ${couple}`, data.events[0]?.date ?? data.date, [data.place, data.address].filter(Boolean).join(", "));
  const families = [familyName(data.couple.brideParents) ?? data.couple.bride, familyName(data.couple.groomParents) ?? data.couple.groom];
  const sending = rsvp.status === "sending" || wishes.status === "sending";
  const sent = rsvp.status === "sent" || wishes.status === "sent";
  const sentRef = useRef<HTMLDivElement>(null);
  useEffect(() => { if (sent) celebrate(sentRef.current); }, [sent]);

  const people = [
    { key: "bride", name: data.couple.brideFull ?? data.couple.bride, parents: data.couple.brideParents, photo: data.couple.bridePhoto ?? gallery[1] },
    { key: "groom", name: data.couple.groomFull ?? data.couple.groom, parents: data.couple.groomParents, photo: data.couple.groomPhoto ?? gallery[2] },
  ];

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
      background="#e4ddcf"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.coverBg} aria-hidden><Photo src={ART} /></div>
          <svg className={s.frame} aria-hidden focusable="false"><rect x="0.5" y="0.5" pathLength={1} /></svg>
          <div className={s.coverContent}>
            <p className={s.coverKicker}>kami akan menikah!</p>
            <h1 className={s.coverNames}>{data.couple.bride} &amp; {data.couple.groom}</h1>
            <p className={s.coverDate}>{longDate}</p>
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
            <p className={s.openingDate}>{longDate}</p>
          </div>
        </section>

        {data.couple.note && <p className={s.quote}>“{data.couple.note.replace(/^[“"]|[”"]$/g, "")}”</p>}

        <Extras slot="opening" />

        <section className={`${s.band} ${s.alt}`} aria-labelledby="st-couple">
          <Head id="st-couple">Mempelai</Head>
          <p className={s.lead}>Halo! Kami mau menikah, dan rasanya nggak lengkap tanpa kamu. Kenalin dulu:</p>
          <div className={`${s.scrap} ${s.couple}`}>
            {people.map(person => (
              <article key={person.key} className={`${s.polaroid} ${s.person}`}>
                <Photo src={person.photo} alt={person.name} className={s.personPhoto} />
                <h3>{person.name}</h3>
                {person.parents && <p>{person.parents}</p>}
              </article>
            ))}
            <span className={`${s.tape} ${s.tapeA}`} aria-hidden />
            <span className={`${s.tape} ${s.tapeB}`} aria-hidden />
            <span className={s.amp} aria-hidden>&amp;</span>
            <span className={`${s.scribble} ${s.iniKami}`} aria-hidden>↙ ini kami</span>
          </div>
        </section>

        <section className={s.band} aria-labelledby="st-count">
          <Head id="st-count">Menuju Hari Bahagia</Head>
          {countdown.valid ? (
            <div className={s.count} role="timer" aria-label={`${countdown.days} hari ${countdown.hours} jam ${countdown.minutes} menit lagi`}>
              {([["Hari", countdown.days], ["Jam", countdown.hours], ["Menit", countdown.minutes], ["Detik", countdown.seconds]] as const).map(([unit, value]) => (
                <div key={unit} className={s.countBox}><b><Tick value={value} /></b><small>{unit}</small></div>
              ))}
            </div>
          ) : <p className={s.countTba}>{DATE_TBA}</p>}
          {calendar && <a className={s.btn} href={calendar} target="_blank" rel="noreferrer"><Lucide icon={ic.calendarPlus} size={15} />Simpan ke Kalender</a>}
        </section>

        <section className={`${s.band} ${s.alt}`} aria-labelledby="st-events">
          <Head id="st-events">Rangkaian Acara</Head>
          {data.events.map((event, index) => (
            <article key={event.name + index} className={`${s.card} ${s.event}`}>
              <span className={s.iconDot}><Lucide icon={index === 0 ? ic.heartHandshake : ic.partyPopper} size={18} /></span>
              <h3>{event.name}</h3>
              <p className={s.eventDate}>{formatDate(event.date || data.date)}</p>
              {event.time && <b>{event.time}</b>}
              <strong>{event.venue}</strong>
              {event.address && <p className={s.eventAddr}>{event.address}</p>}
            </article>
          ))}
          {maps && <a className={s.btn} href={maps} target="_blank" rel="noreferrer"><Lucide icon={ic.mapPin} size={15} />Lihat Lokasi di Maps</a>}
        </section>

        <Extras slot="event" without={["calendar"]} />

        {stories.length > 0 && (
          <section className={s.band} aria-labelledby="st-story">
            <Head id="st-story">Kisah Kami</Head>
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
          <section className={`${s.band} ${s.alt}`} aria-labelledby="st-gallery">
            <Head id="st-gallery">Galeri</Head>
            <div className={`${s.scrap} ${s.galleryScrap}`} data-count={scrap.length}>
              {scrap.map((src, index) => (
                <div key={src + index} className={`${s.polaroid} ${s.snap}`}>
                  <Photo src={src} alt={`Foto ${index + 1} dari ${gallery.length}`} />
                </div>
              ))}
              {scrap.map((src, index) => <span key={`tape-${index}`} className={`${s.tape} ${[s.tape1, s.tape2, s.tape3][index]}`} aria-hidden />)}
              <span className={`${s.scribble} ${s.coret}`} aria-hidden>coret-coret kenangan</span>
            </div>
            {gallery.length > 3 && (
              <div className={s.more}>
                {gallery.slice(3).map((src, index) => (
                  <div key={src + index} className={s.snap}><Photo src={src} alt={`Foto ${index + 4} dari ${gallery.length}`} /></div>
                ))}
              </div>
            )}
          </section>
        )}

        <Extras slot="story" />

        <Extras slot="end" />

        {data.gifts.length > 0 && (
          <section className={s.band} aria-labelledby="st-gift">
            <Head id="st-gift">Kirim Kado</Head>
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

        <section className={`${s.band} ${s.alt}`} aria-labelledby="st-wish">
          <Head id="st-wish">Ucapan &amp; RSVP</Head>
          <div className={`${s.card} ${s.formCard}`}>
            {sent ? (
              <div ref={sentRef} className={s.sent} role="status">
                <span className={s.iconDot}><Lucide icon={ic.check} size={18} /></span>
                <strong>Makasih ya!</strong>
                <p>{demo ? "Ini pratinjau — jawaban contoh tidak dikirim." : sentSummary(rsvp, wishes)}</p>
                <button type="button" className={s.btn} onClick={() => { rsvp.reset(); wishes.reset(); }}>Tulis lagi</button>
              </div>
            ) : (
              <form className={s.form} onSubmit={onSubmit}>
                <label className={s.field}>Nama
                  <input name="name" required maxLength={100} placeholder="Nama Anda" autoComplete="name"
                    defaultValue={data.guestName && data.guestName !== "Tamu Undangan" ? data.guestName : ""} />
                </label>
                <label className={s.field}>Ucapan
                  <textarea name="message" required={rsvpClosed} maxLength={500} rows={3} placeholder="Tulis doa & ucapan…" />
                </label>
                {rsvpClosed ? <div className={s.closed} role="status"><strong>Konfirmasi kehadiran sudah ditutup</strong><p>Terima kasih atas doa dan perhatiannya. Ucapan &amp; doa masih bisa dikirim lewat form ini.</p></div> : (
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
                {!rsvpClosed && attendance !== "no" && <GuestCount label="Jumlah tamu" className={s.guests} labelClassName={s.guestsLabel} buttonClassName={s.step} />}
                {!rsvpClosed && attendance !== "no" && <DietaryField className={s.field} />}
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
