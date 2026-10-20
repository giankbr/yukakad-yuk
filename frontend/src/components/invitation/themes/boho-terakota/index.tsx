"use client";
// Theme "Boho Terakota" — terakota hangat, rumput pampas yang bergoyang, lengkung pelangi bohemian dan jendela lengkung.
import { useEffect, useRef, useState, type CSSProperties } from "react";
import {
  DietaryField, Extras, GuestCount, Lucide, Photo, ThemeShell, Tick, coupleLabel, dateParts, formatDate, giftInfo, guestLabel,
  mapsHref, storyItems, useCopy, useCountdown, useMusic, DATE_TBA, useRsvp, useThankYou, useWishes, type Attendance, type ThemeProps, type Wish,
} from "../kit";
import { tableLabel } from "../extras";
import type { InvitationData } from "../../types";
import { celebrate } from "@/lib/celebrate";
import { ic } from "./icons";
import s from "./styles.module.css";

const FONTS = ["DM Serif Display:ital@0;1", "Josefin Sans:wght@300;400;600", "Sacramento"];
const ATTEND: Record<Attendance, string> = { yes: "Hadir", maybe: "Ragu", no: "Berhalangan" };
const DEMO_WISHES: Wish[] = [
  { id: "w1", name: "Tari & Bagas", attendance: "yes", message: "Selamat Nayla & Raka! Semoga cinta kalian tumbuh subur seperti kebun yang kalian rawat bersama." },
  { id: "w2", name: "Mas Yoga", attendance: "yes", message: "Barakallahu lakuma wa baraka 'alaikuma. Ditunggu di garden party-nya!" },
];

const ART = "/themes/art/boho-terakota";

/** Decorative painted image (never opens the photo lightbox). */
function Art({ src, className, style, w, h, eager }: { src: string; className?: string; style?: CSSProperties; w: number; h: number; eager?: boolean }) {
  return (
    // eslint-disable-next-line @next/next/no-img-element -- static painted ornament
    <img src={`${ART}/${src}.webp`} alt="" aria-hidden width={w} height={h} className={className} style={style} data-nolightbox
      loading={eager ? "eager" : "lazy"} fetchPriority={eager ? "high" : undefined} decoding="async" draggable={false} />
  );
}

/** Three gouache pampas plumes, each swaying on its own from the base. */
function Pampas({ className, flip, eager }: { className?: string; flip?: boolean; eager?: boolean }) {
  return (
    <span className={`${s.pampas} ${className ?? ""}`} aria-hidden="true" style={flip ? { scale: "-1 1" } : undefined}>
      {[{ x: 0, r: -16, o: 1, src: "pampas-a" }, { x: 22, r: -4, o: .9, src: "pampas-b" }, { x: 40, r: 8, o: .8, src: "pampas-a" }].map((sprig, index) => (
        <Art key={index} src={sprig.src} className={s.sprig} w={150} h={300} eager={eager}
          style={{ left: `${sprig.x}%`, opacity: sprig.o, "--r0": `${sprig.r}deg`, animationDelay: `${index * -1.7}s` } as CSSProperties} />
      ))}
    </span>
  );
}

/** Gouache boho rainbow; unveiled when revealed. */
function Rainbow({ className, eager }: { className?: string; eager?: boolean }) {
  return <Art src="rainbow" className={`${s.rainbow} ${className ?? ""}`} w={400} h={200} eager={eager} />;
}

function Sun({ className, blush, eager }: { className?: string; blush?: boolean; eager?: boolean }) {
  return <Art src={blush ? "sun-blush" : "sun"} className={`${s.sun} ${className ?? ""}`} w={180} h={180} eager={eager} />;
}

function Head({ id, kicker, title }: { id: string; kicker: string; title: string }) {
  return (
    <div className={s.head}>
      <p className={s.script}>{kicker}</p>
      <h2 id={id}>{title}</h2>
      <span className={s.dots} aria-hidden><i /><i /><i /></span>
    </div>
  );
}

function father(parents?: string) {
  const match = /(?:Bapak|Bpk\.?)\s+(?:H\.\s*)?([^&\n]+?)\s*(?:&|\n|$)/i.exec(parents ?? "");
  return match?.[1].trim();
}

function plainName(guest?: string) {
  if (!guest || guest === "Tamu Undangan") return "";
  return guest.replace(/^(bapak|ibu|bpk\.?|sdr\.?|saudara|saudari|mbak|mas)\s+/i, "").replace(/\s*(&|dan)\s*(keluarga|partner)$/i, "").trim();
}

function islamic(data: InvitationData) {
  return data.events.some(event => /akad|ijab|walimah/i.test(event.name)) || /\bQS\b|Q\.S\./.test(data.extras?.quote?.source ?? "");
}

export default function BohoTerakotaTheme({ data, slug, guestToken, demo, skipCover }: ThemeProps) {
  const couple = coupleLabel(data);
  const label = data.eventLabel ?? "Pernikahan";
  const parts = dateParts(data.date);
  const countdown = useCountdown(data.date);
  const rsvp = useRsvp({ slug, guestToken, demo });
  const wishes = useWishes({ slug, guestToken, demo, seed: DEMO_WISHES });
  const thanks = useThankYou();
  const rsvpClosed = thanks.active || rsvp.status === "closed";
  const { copy, copied } = useCopy();
  const music = useMusic(data.music);
  const [attendance, setAttendance] = useState<Attendance>("yes");
  const stories = storyItems(data);
  const gallery = data.gallery;
  const coverPhoto = gallery[0];
  const feature = gallery[1] ?? gallery[0];
  const table = tableLabel(data.guestTable);
  const quote = data.extras?.quote && data.extras.quote.enabled !== false ? data.extras.quote : undefined;
  const muslim = islamic(data);
  const families = [father(data.couple.brideParents), father(data.couple.groomParents)].filter(Boolean);
  const sentRef = useRef<HTMLDivElement>(null);
  useEffect(() => { if (wishes.status === "sent") celebrate(sentRef.current); }, [wishes.status]);
  const people = [
    { key: "bride", short: data.couple.bride, name: data.couple.brideFull ?? data.couple.bride, parents: data.couple.brideParents, photo: data.couple.bridePhoto },
    { key: "groom", short: data.couple.groom, name: data.couple.groomFull ?? data.couple.groom, parents: data.couple.groomParents, photo: data.couple.groomPhoto },
  ].filter(person => person.short || person.name);

  return (
    <ThemeShell
      fonts={FONTS}
      background="#e9d6c2"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.coverArch}>
            <Sun className={s.coverSun} eager />
            <div className={s.archWindow}>{coverPhoto ? <Photo src={coverPhoto} alt={`Foto ${couple}`} /> : <Rainbow className={s.archRainbow} eager />}</div>
            <Pampas className={s.pampasL} eager />
            <Pampas className={s.pampasR} flip eager />
          </div>
          <p className={s.label}>The Wedding of</p>
          <h1 className={s.coverNames}>{data.couple.bride}{data.couple.groom && <><em>&amp;</em>{data.couple.groom}</>}</h1>
          <p className={s.coverDate}>{parts.day ? `${parts.weekday} · ${parts.day} ${parts.month} ${parts.year}` : DATE_TBA}</p>
          <div className={s.guest}>
            <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
            <strong>{guestLabel(data)}</strong>
            {table && <span>{table}</span>}
          </div>
          <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#fff6ec" />Buka Undangan</button>
        </section>
      )}
    >
      <main className={s.main}>
        <header className={s.hero} data-reveal-block>
          <Rainbow className={s.heroRainbow} />
          <p className={s.label}>{label}</p>
          <h1 className={s.heroNames}>{data.couple.bride}{data.couple.groom && <><em>&amp;</em>{data.couple.groom}</>}</h1>
          <p className={s.heroDate}>{formatDate(data.date)}</p>
          {feature && <div className={s.heroPhoto}><Photo src={feature} alt={`Foto ${couple}`} /></div>}
        </header>

        <section className={s.opening} aria-label="Pembuka">
          <Sun className={s.openSun} blush />
          <p className={s.salam}>{muslim ? "Assalamu'alaikum Warahmatullahi Wabarakatuh" : "Salam hangat untuk Anda"}</p>
          {quote ? (
            <blockquote className={s.quote}><p>“{quote.text}”</p>{quote.source && <cite>{quote.source}</cite>}</blockquote>
          ) : data.couple.note ? <p className={s.quote}>{data.couple.note}</p> : null}
        </section>

        <Extras slot="opening" without={["quote"]} />

        <section className={s.section} aria-labelledby="bt-couple">
          <Head id="bt-couple" kicker="dengan bahagia" title="Kedua Mempelai" />
          <p className={s.intro}>Dengan memohon rahmat Tuhan Yang Maha Kuasa, kami bermaksud menyelenggarakan {label.toLowerCase()} kami:</p>
          <div className={`${s.people} ${people.length === 1 ? s.peopleOne : ""}`}>
            {people.map(person => (
              <article key={person.key} className={s.person}>
                <div className={s.portrait}>{person.photo ? <Photo src={person.photo} alt={person.name} /> : <span className={s.initial} aria-hidden>{person.short.charAt(0).toUpperCase()}</span>}</div>
                <p className={s.script}>{person.short}</p>
                <h3>{person.name}</h3>
                {person.parents && <p className={s.parents}>{person.parents}</p>}
              </article>
            ))}
          </div>
        </section>

        <section className={`${s.section} ${s.terra}`} aria-labelledby="bt-count">
          <Head id="bt-count" kicker="hitung mundur" title="Menuju Hari Bahagia" />
          {countdown.valid ? (
            <div className={s.count} role="timer" aria-label={`${countdown.days} hari ${countdown.hours} jam ${countdown.minutes} menit lagi`}>
              {[[countdown.days, "Hari"], [countdown.hours, "Jam"], [countdown.minutes, "Menit"], [countdown.seconds, "Detik"]].map(([value, unit]) => (
                <div key={unit}><b><Tick value={value} /></b><small>{unit}</small></div>
              ))}
            </div>
          ) : <p className={s.countTba}>{DATE_TBA}</p>}
          <Pampas className={s.bandPampas} />
        </section>

        <section className={s.section} aria-labelledby="bt-events">
          <Head id="bt-events" kicker="kapan & di mana" title="Rangkaian Acara" />
          <div className={s.events}>
            {data.events.map((event, index) => {
              const maps = mapsHref(data, event);
              const p = dateParts(event.date || data.date);
              return (
                <article key={event.name + index} className={s.event}>
                  <span className={s.eventDay} aria-hidden><b>{p.day || "—"}</b><small>{p.monthShort || "TBA"}</small></span>
                  <h3>{event.name}</h3>
                  <p className={s.when}>{formatDate(event.date || data.date)}</p>
                  {event.time && <p className={s.time}><Lucide icon={ic.clock3} size={14} />{event.time}</p>}
                  <p className={s.venue}>{event.venue}</p>
                  {event.address && <p className={s.addr}>{event.address}</p>}
                  {maps && <a className={s.btn} href={maps} target="_blank" rel="noreferrer"><Lucide icon={ic.mapPin} size={15} />Lihat Peta</a>}
                </article>
              );
            })}
          </div>
        </section>

        <Extras slot="event" />

        {stories.length > 0 && (
          <section className={s.section} aria-labelledby="bt-story">
            <Head id="bt-story" kicker="cerita kami" title="Kisah Cinta" />
            <ol className={`${s.story} ${stories.length === 1 ? s.storyOne : ""}`} data-noreveal={stories.length > 1 ? "" : undefined}>
              {stories.map((story, index) => (
                <li key={index}>
                  {story.image ? <Photo src={story.image} alt={story.title} className={s.storyImg} /> : <span className={s.storyNum} aria-hidden>{index + 1}</span>}
                  {story.date && <p className={s.label}>{story.date}</p>}
                  <h3>{story.title}</h3>
                  {story.body && <p>{story.body}</p>}
                </li>
              ))}
            </ol>
            {stories.length > 1 && <p className={s.swipe} aria-hidden>geser untuk membaca &rarr;</p>}
          </section>
        )}

        {gallery.length > 0 && (
          <section className={s.section} aria-labelledby="bt-gallery">
            <Head id="bt-gallery" kicker="kenangan" title="Galeri Foto" />
            <div className={s.gallery}>
              {gallery.slice(0, 9).map((src, index) => <div key={src + index} className={s.tile}><Photo src={src} alt={`Foto galeri ${index + 1}`} /></div>)}
            </div>
          </section>
        )}

        <Extras slot="story" />

        <Extras slot="end" />

        {data.gifts.length > 0 && (
          <section className={s.section} aria-labelledby="bt-gift">
            <Head id="bt-gift" kicker="tanda kasih" title="Amplop & Kado" />
            <p className={s.intro}>Doa restu Anda adalah karunia terindah. Bila berkenan berbagi tanda kasih, dapat melalui:</p>
            <div className={s.gifts}>
              {data.gifts.map(gift => {
                const info = giftInfo(gift);
                const on = Boolean(info.copy) && copied === info.copy;
                const icon = gift.type === "bank" ? ic.landmark : gift.type === "address" ? ic.gift : gift.type === "qris" ? ic.qrCode : ic.wallet;
                return (
                  <article key={gift.id} className={`${s.gift} ${on ? s.giftOn : ""}`}>
                    <span className={s.giftIcon}><Lucide icon={icon} size={20} /></span>
                    <p className={s.label}>{info.kind}</p>
                    <h3>{info.title}</h3>
                    {info.number && <p className={gift.type === "address" ? s.giftAddr : s.giftNo}>{info.number}</p>}
                    {info.holder && <p className={s.giftName}>a.n. {info.holder}</p>}
                    {info.image && <Photo src={info.image} alt="Kode QRIS" className={s.qris} />}
                    {info.copy && (
                      <button type="button" className={s.copyBtn} onClick={() => copy(info.copy)} aria-label={on ? "Tersalin" : `Salin ${info.title}`}>
                        <Lucide key={on ? "on" : "off"} icon={on ? ic.check : ic.copy} size={14} />{on ? "Tersalin" : "Salin"}
                      </button>
                    )}
                  </article>
                );
              })}
            </div>
          </section>
        )}

        <section className={s.section} aria-labelledby="bt-rsvp">
          <Head id="bt-rsvp" kicker="kabari kami" title="Kehadiran & Ucapan" />
          {wishes.status === "sent" ? (
            <div ref={sentRef} className={`${s.form} ${s.sentBox}`} role="status">
              <Sun className={s.sentSun} />
              <p className={s.sent}>Terima kasih! Ucapan dan doa Anda sudah kami terima dengan hangat.</p>
              {!demo && wishes.pending && <p className={s.sentNote}>Ucapan akan tampil setelah disetujui oleh mempelai.</p>}
              {demo && <p className={s.sentNote}>Ini pratinjau, ucapan hanya tampil di daftar.</p>}
              <button type="button" className={s.submit} onClick={() => { wishes.reset(); rsvp.reset(); }}>Tulis Lagi</button>
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
              if (!rsvpClosed && rsvp.status !== "sent") void rsvp.submit({ name, attendance, guests, diet: String(form.get("diet") ?? "").trim() || undefined });
            }}>
              <label className={s.field}><span>Nama</span><input name="name" required maxLength={100} defaultValue={plainName(data.guestName)} placeholder="Nama Anda" autoComplete="name" /></label>
              <label className={s.field}><span>Ucapan & doa</span><textarea name="message" required maxLength={500} rows={3} placeholder="Tuliskan ucapan hangat…" /></label>
              {rsvpClosed ? (
                <div className={s.closed} role="status"><strong>Konfirmasi kehadiran sudah ditutup</strong><p>Terima kasih atas doa dan perhatiannya. Ucapan masih bisa dikirim lewat form ini.</p></div>
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
              {wishes.status === "error" && <p className={s.error} role="alert">Belum terkirim. Coba lagi sebentar lagi.</p>}
              <button type="submit" className={s.submit} disabled={wishes.status === "sending"}><Lucide icon={ic.send} size={15} />{wishes.status === "sending" ? "Mengirim…" : "Kirim Ucapan"}</button>
            </form>
          )}
          <div className={s.wishes}>
            {wishes.wishes.length === 0 && <p className={s.empty}>Belum ada ucapan. Jadilah yang pertama.</p>}
            {wishes.wishes.slice(0, 10).map(wish => (
              <article key={wish.id} className={s.wish}>
                <span className={s.avatar} aria-hidden>{wish.name.trim().charAt(0).toUpperCase()}</span>
                <div>
                  <div className={s.wishHead}><strong>{wish.name}</strong>{wish.attendance && <small>{ATTEND[wish.attendance]}</small>}</div>
                  <p>{wish.message}</p>
                </div>
              </article>
            ))}
          </div>
        </section>

        <footer className={s.closing}>
          <div className={s.closingArt} aria-hidden>
            <Rainbow className={s.closingRainbow} />
            <Pampas className={s.closingPampasL} />
            <Pampas className={s.closingPampasR} flip />
          </div>
          <p className={s.script}>terima kasih</p>
          <p className={s.closingText}>Kehadiran dan doa restu Anda akan melengkapi kebahagiaan kami di hari istimewa ini.</p>
          {muslim && <p className={s.salamEnd}>Wassalamu&apos;alaikum Warahmatullahi Wabarakatuh</p>}
          <p className={s.closingNames}>{couple}</p>
          {families.length > 0 && <p className={s.family}>beserta keluarga besar<br />Bapak {families.join(" & Bapak ")}</p>}
          <a href="/" target="_blank" rel="noreferrer" className={s.made}>dibuat dengan ♥ di Rawuh</a>
        </footer>
      </main>

      {music.visible && !music.failed && (
        <button type="button" className={`${s.music} ${music.playing ? s.musicOn : ""}`} onClick={music.toggle} aria-pressed={music.playing} aria-label={music.playing ? "Matikan musik" : "Putar musik"}>
          <Lucide icon={ic.music} size={17} color="#fff6ec" />
        </button>
      )}
    </ThemeShell>
  );
}
