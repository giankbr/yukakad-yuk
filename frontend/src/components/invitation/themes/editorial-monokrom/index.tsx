"use client";
// Theme "Editorial Monokrom" — undangan bergaya majalah hitam-putih: masthead, tipografi raksasa, garis tegas, kolom & keterangan foto.
import { useEffect, useRef, useState } from "react";
import {
  DATE_TBA, DietaryField, Extras, GuestCount, Icon, Photo, ThemeShell, Tick, coupleLabel, dateParts, formatDate, giftInfo, guestLabel, icons,
  mapsHref, sentSummary, storyItems, useCopy, useCountdown, useRsvp, useThankYou, useWishes, type Attendance, type ThemeProps, type Wish,
} from "../kit";
import { tableLabel } from "../extras";
import { celebrate } from "@/lib/celebrate";
import s from "./styles.module.css";

const FONTS = ["Bebas Neue", "Playfair Display:ital,wght@0,400;0,600;0,700;1,400;1,600", "Inter:wght@400;500;600;700"];
const ATTEND: Record<Attendance, string> = { yes: "Hadir", maybe: "Ragu", no: "Berhalangan" };
const DEMO_WISHES: Wish[] = [
  { id: "w1", name: "Laras, Bandung", attendance: "yes", message: "Edisi paling ditunggu tahun ini. Selamat Saskia & Raka, semoga setiap babak berikutnya lebih indah." },
  { id: "w2", name: "Tim Studio Serambi", attendance: "yes", message: "Dari meja gambar ke pelaminan. Bahagia selalu, kalian berdua!" },
];
const pad = (n: number) => String(n).padStart(2, "0");
const arrowUpRight = ["M7 7h10v10", "M7 17 17 7"];

/** "12.06.2027" */
function dotted(value?: string) {
  const p = dateParts(value);
  if (!p.day) return "";
  const month = new Intl.DateTimeFormat("en", { timeZone: "Asia/Jakarta", month: "numeric" }).format(new Date(value as string));
  return `${pad(Number(p.day))}.${pad(Number(month))}.${p.year}`;
}

function plainName(guest?: string) {
  if (!guest || guest === "Tamu Undangan") return "";
  return guest.replace(/^(bapak|ibu|bpk\.?|sdr\.?|sdri\.?|saudara|saudari)\s+/i, "").replace(/\s*(&|dan)\s*keluarga$/i, "").trim();
}

function familyName(parents?: string) {
  const match = /(?:Bapak|Bpk\.?)\s+([^&\n,]+)/i.exec(parents ?? "");
  return match?.[1].trim().split(/\s+/).pop();
}

const ART = "/themes/art/editorial-monokrom";

/** Linocut accent (decorative): never opens the photo lightbox. */
function Print({ src, className, width, height }: { src: string; className?: string; width: number; height: number }) {
  return (
    // eslint-disable-next-line @next/next/no-img-element -- static decorative print
    <img src={`${ART}/${src}.webp`} alt="" aria-hidden className={className} width={width} height={height} data-nolightbox loading="lazy" decoding="async" draggable={false} />
  );
}

function Head({ id, no, kicker, title }: { id: string; no: string; kicker: string; title: string }) {
  return (
    <div className={s.head}>
      <div className={s.headMeta}><span>{kicker}</span><span>p. {no}</span></div>
      <span className={s.rule} aria-hidden />
      <h2 id={id}>{title}</h2>
    </div>
  );
}

function Ticker({ text }: { text: string }) {
  const items = Array.from({ length: 6 }, (_, index) => <span key={index}>{text}<b aria-hidden>✦</b></span>);
  return (
    <div className={s.ticker} aria-label={text}>
      <div className={s.tickerTrack} aria-hidden>{items}{items}</div>
    </div>
  );
}

export default function EditorialMonokromTheme({ data, slug, guestToken, demo, skipCover }: ThemeProps) {
  const couple = coupleLabel(data);
  const label = data.eventLabel ?? "Pernikahan";
  const parts = dateParts(data.date);
  const stamp = dotted(data.date);
  const countdown = useCountdown(data.date);
  const rsvp = useRsvp({ slug, guestToken, demo });
  const wishes = useWishes({ slug, guestToken, demo, seed: DEMO_WISHES });
  const thanks = useThankYou();
  const rsvpClosed = thanks.active || rsvp.status === "closed";
  const { copy, copied } = useCopy();
  const [attendance, setAttendance] = useState<Attendance>("yes");
  const stories = storyItems(data);
  const coverPhoto = data.gallery[0] ?? data.couple.bridePhoto ?? data.couple.groomPhoto;
  const photos = data.gallery.length > 1 ? data.gallery.slice(1) : data.gallery;
  const table = tableLabel(data.guestTable);
  const families = [familyName(data.couple.brideParents), familyName(data.couple.groomParents)].filter(Boolean);
  const sentRef = useRef<HTMLDivElement>(null);
  const sent = wishes.status === "sent";
  useEffect(() => { if (sent) celebrate(sentRef.current); }, [sent]);
  const people = [
    { no: "01", role: "Sang Mempelai Wanita", nick: data.couple.bride, name: data.couple.brideFull || data.couple.bride, parents: data.couple.brideParents, photo: data.couple.bridePhoto },
    { no: "02", role: "Sang Mempelai Pria", nick: data.couple.groom, name: data.couple.groomFull || data.couple.groom, parents: data.couple.groomParents, photo: data.couple.groomPhoto },
  ];
  const issue = `Edisi ${label}`;

  return (
    <ThemeShell
      fonts={FONTS}
      background="#e9e9e6"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.mast}>
            <span>{issue}</span>
            <span>{parts.year ? `Vol. ${parts.year.slice(2)}` : "Vol. —"}</span>
          </div>
          <p className={s.coverBrand}>The Wedding</p>
          <div className={s.coverFrame}>
            <Photo src={coverPhoto} alt={`Foto ${couple}`} className={s.coverImg} />
            <span className={s.coverStamp}>{stamp || DATE_TBA}</span>
          </div>
          <h1 className={s.coverNames}><span>{data.couple.bride}</span><em>&amp;</em><span>{data.couple.groom}</span></h1>
          <div className={s.coverFoot}>
            <div className={s.to}>
              <small>Kepada Yth.</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}>Buka Undangan<Icon d={icons.arrowRight} size={16} /></button>
          </div>
        </section>
      )}
    >
      <main className={s.main}>
        <header className={s.masthead}>
          <div className={s.mast}><span>{issue}</span><span>{stamp || DATE_TBA}</span></div>
          <h1 className={s.bigNames}><span>{data.couple.bride}</span><span className={s.and}>dan</span><span>{data.couple.groom}</span></h1>
          <figure className={s.heroFig}>
            <Photo src={coverPhoto} alt={`Foto ${couple}`} className={s.heroImg} />
            <figcaption><b>Sampul.</b> {couple}, {parts.day ? `${parts.month} ${parts.year}` : "segera"}.</figcaption>
          </figure>
        </header>

        <Ticker text={`Save the date — ${stamp || DATE_TBA} — ${data.place || label}`} />

        <section className={s.section} aria-labelledby="em-letter">
          <Head id="em-letter" no="02" kicker="Catatan Pembuka" title="Kepada para pembaca terkasih" />
          <p className={s.salam}>Assalamu&apos;alaikum warahmatullahi wabarakatuh.</p>
          <p className={s.dropcap}>Dengan memohon rahmat dan ridha Allah SWT, kami mengundang Bapak/Ibu/Saudara/i untuk hadir dalam {label.toLowerCase()} kami. Halaman-halaman berikut memuat seluruh keterangan acara — semoga berkenan membacanya sampai habis.</p>
          {data.couple.note && <blockquote className={s.pull}>“{data.couple.note}”</blockquote>}
          <p className={s.sign}>— {couple}</p>
          <Print src="linocut-twig" className={s.twig} width={143} height={26} />
        </section>

        <Extras slot="opening" />

        <section className={s.section} aria-labelledby="em-profile">
          <Head id="em-profile" no="04" kicker="Profil" title="Dua nama di halaman ini" />
          {people.map(person => (
            <article key={person.no} className={s.profile}>
              <div className={s.profilePic}>
                {person.photo ? <Photo src={person.photo} alt={person.name} /> : <span className={s.mono} aria-hidden>{person.nick.slice(0, 1)}</span>}
                <span className={s.profileNo}>{person.no}</span>
              </div>
              <div className={s.profileText}>
                <small>{person.role}</small>
                <h3>{person.name}</h3>
                {person.parents && <p>{person.parents}</p>}
              </div>
            </article>
          ))}
        </section>

        <section className={`${s.section} ${s.black}`} aria-labelledby="em-count">
          <Head id="em-count" no="06" kicker="Tenggat" title="Hitung mundur" />
          {countdown.valid ? (
            <div className={s.count} role="timer" aria-label={`${countdown.days} hari ${countdown.hours} jam ${countdown.minutes} menit lagi`}>
              {[[countdown.days, "Hari"], [countdown.hours, "Jam"], [countdown.minutes, "Menit"], [countdown.seconds, "Detik"]].map(([value, unit]) => (
                <div key={unit}><b><Tick value={value} /></b><small>{unit}</small></div>
              ))}
            </div>
          ) : <p className={s.tba}>{DATE_TBA}</p>}
          <p className={s.countDate}>{formatDate(data.date)}</p>
        </section>

        <section className={s.section} aria-labelledby="em-agenda">
          <Head id="em-agenda" no="07" kicker="Agenda" title="Rangkaian acara" />
          <ol className={s.agenda}>
            {data.events.map((event, index) => {
              const p = dateParts(event.date || data.date);
              const maps = mapsHref(data, event);
              return (
                <li key={event.name + index} className={s.agendaRow}>
                  <div className={s.agendaDate}><b>{p.day || "—"}</b><small>{p.monthShort || "TBA"}</small></div>
                  <div className={s.agendaBody}>
                    <h3>{event.name}</h3>
                    <p className={s.agendaMeta}>{formatDate(event.date || data.date)}{event.time ? ` · ${event.time}` : ""}</p>
                    <strong>{event.venue}</strong>
                    {event.address && <p>{event.address}</p>}
                    {maps && <a className={s.link} href={maps} target="_blank" rel="noreferrer">Buka peta<Icon d={arrowUpRight} size={14} /></a>}
                  </div>
                </li>
              );
            })}
          </ol>
        </section>

        <Extras slot="event" />

        {stories.length > 0 && (
          <section className={s.section} aria-labelledby="em-story">
            <Head id="em-story" no="09" kicker="Kronologi" title="Bagaimana semua bermula" />
            <ol className={s.chrono}>
              {stories.map((story, index) => (
                <li key={index}>
                  <span className={s.year} aria-hidden={!story.date}>{story.date ?? pad(index + 1)}</span>
                  <div>
                    <h3>{story.title}</h3>
                    {story.body && <p>{story.body}</p>}
                    {story.image && <Photo src={story.image} alt={story.title} className={s.storyImg} />}
                  </div>
                </li>
              ))}
            </ol>
          </section>
        )}

        {photos.length > 0 && (
          <section className={s.section} aria-labelledby="em-gallery">
            <Head id="em-gallery" no="11" kicker="Portofolio" title="Galeri" />
            <div className={s.gallery}>
              {photos.map((src, index) => (
                <figure key={src + index} className={s.fig}>
                  <Photo src={src} alt={`Foto galeri ${index + 1}`} />
                  <figcaption>Fig. {index + 1}</figcaption>
                </figure>
              ))}
            </div>
          </section>
        )}

        <Extras slot="story" />

        <section className={s.section} aria-labelledby="em-rsvp">
          <Head id="em-rsvp" no="13" kicker="Formulir" title={rsvpClosed ? "Surat pembaca" : "Konfirmasi & ucapan"} />
          {sent ? (
            <div ref={sentRef} className={s.sentBox} role="status">
              <span className={s.sentMark} aria-hidden><Icon d={icons.check} size={22} strokeWidth={2.6} /></span>
              <strong>Diterima redaksi.</strong>
              <p>{demo ? "Ini pratinjau — ucapanmu hanya tampil di daftar." : sentSummary(rsvp, wishes)}</p>
              <button type="button" className={s.submit} onClick={() => { wishes.reset(); rsvp.reset(); }}>Tulis lagi</button>
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
              <label className={s.field}><span>Nama</span><input name="name" required maxLength={100} defaultValue={plainName(data.guestName)} placeholder="Nama lengkap" autoComplete="name" /></label>
              {rsvpClosed ? (
                <div className={s.closed} role="status"><strong>Konfirmasi kehadiran sudah ditutup.</strong><p>Terima kasih atas doa dan perhatiannya. Ucapan masih bisa dikirim lewat formulir ini.</p></div>
              ) : (
                <div className={s.field}>
                  <span>Kehadiran</span>
                  <div className={s.segment} role="radiogroup" aria-label="Kehadiran">
                    {(["yes", "maybe", "no"] as Attendance[]).map(value => (
                      <button key={value} type="button" role="radio" aria-checked={attendance === value} className={attendance === value ? s.segOn : undefined} onClick={() => setAttendance(value)}>{ATTEND[value]}</button>
                    ))}
                  </div>
                </div>
              )}
              {!rsvpClosed && attendance !== "no" && <GuestCount className={s.guests} labelClassName={s.guestsLabel} buttonClassName={s.step} />}
              {!rsvpClosed && attendance !== "no" && <DietaryField className={s.field} />}
              <label className={s.field}><span>Ucapan</span><textarea name="message" required maxLength={500} rows={3} placeholder="Tulis surat singkatmu…" /></label>
              {wishes.status === "error" && <p className={s.error} role="alert">Belum terkirim. Coba lagi sebentar lagi.</p>}
              <button type="submit" className={s.submit} disabled={wishes.status === "sending"}>{wishes.status === "sending" ? "Mengirim…" : "Kirim ke redaksi"}</button>
            </form>
          )}
          <div className={s.letters}>
            <p className={s.lettersHead}>Surat pembaca · {wishes.wishes.length}</p>
            {wishes.wishes.length === 0 && <p className={s.empty}>Belum ada surat. Jadilah yang pertama menulis.</p>}
            {wishes.wishes.slice(0, 12).map(wish => (
              <article key={wish.id} className={s.letter}>
                <p>“{wish.message}”</p>
                <div><strong>{wish.name}</strong>{wish.attendance && <small>{ATTEND[wish.attendance]}</small>}</div>
              </article>
            ))}
          </div>
        </section>

        {data.gifts.length > 0 && (
          <section className={s.section} aria-labelledby="em-gifts">
            <Head id="em-gifts" no="15" kicker="Kontribusi" title="Tanda kasih" />
            <p className={s.note}>Kehadiran dan doa Anda adalah hadiah utama. Bagi yang ingin memberi tanda kasih:</p>
            <div className={s.giftList}>
              {data.gifts.map((gift, index) => {
                const info = giftInfo(gift);
                const on = Boolean(info.copy) && copied === info.copy;
                return (
                  <div key={gift.id} className={on ? `${s.gift} ${s.giftOn}` : s.gift}>
                    <span className={s.giftNo}>{pad(index + 1)}</span>
                    <div className={s.giftText}>
                      <small>{info.kind}</small>
                      <h3>{info.title}</h3>
                      {info.number && <strong>{info.number}</strong>}
                      {info.holder && <p>a.n. {info.holder}</p>}
                      {info.image && <Photo src={info.image} alt="Kode QRIS" className={s.qris} />}
                    </div>
                    {info.copy && (
                      <button type="button" className={on ? `${s.copy} ${s.copyOn}` : s.copy} onClick={() => copy(info.copy)} aria-label={on ? "Tersalin" : `Salin ${info.title}`}>
                        <Icon key={on ? "on" : "off"} d={on ? icons.check : icons.copy} size={14} />{on ? "Tersalin" : "Salin"}
                      </button>
                    )}
                  </div>
                );
              })}
            </div>
          </section>
        )}

        <Extras slot="end" />

        <footer className={s.colophon}>
          <Print src="linocut-lily" className={s.lily} width={118} height={180} />
          <p className={s.fin}>Terima kasih.</p>
          <p className={s.finText}>{thanks.active ? thanks.message : "Kehadiran dan doa restu Anda melengkapi cerita kami. Sampai bertemu di hari bahagia."}</p>
          <dl className={s.credits}>
            <div><dt>Mempelai</dt><dd>{couple}</dd></div>
            {families.length > 0 && <div><dt>Keluarga</dt><dd>{families.map(name => `Kel. ${name}`).join(" & ")}</dd></div>}
            <div><dt>Terbit</dt><dd>{parts.day ? formatDate(data.date, { day: "numeric", month: "long", year: "numeric" }) : DATE_TBA}</dd></div>
          </dl>
          <span className={s.ruleThick} aria-hidden />
          <a href="/" target="_blank" rel="noreferrer" className={s.made}>dibuat dengan ♥ di Rawuh</a>
        </footer>
      </main>
    </ThemeShell>
  );
}
