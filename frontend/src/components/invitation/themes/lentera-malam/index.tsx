"use client";
// Theme "Lentera Malam" — langit malam biru tua, lentera bergantungan yang berayun pelan dan bulan sabit keemasan.
import { useEffect, useRef, useState } from "react";
import {
  DietaryField, Extras, GuestCount, Icon, Photo, ThemeShell, Tick, coupleLabel, dateParts, formatDate, giftInfo, guestLabel, icons,
  mapsHref, storyItems, useCopy, useCountdown, DATE_TBA, useRsvp, useThankYou, useWishes, type Attendance, type ThemeProps, type Wish,
} from "../kit";
import { tableLabel } from "../extras";
import { celebrate } from "@/lib/celebrate";
import s from "./styles.module.css";

const FONTS = ["Playfair Display:ital,wght@0,500;0,600;0,700;1,500;1,600", "Mulish:wght@400;500;600;700", "Amiri:wght@400;700"];
const ATTEND: Record<Attendance, string> = { yes: "Hadir", maybe: "Ragu", no: "Berhalangan" };
const DEMO_WISHES: Wish[] = [
  { id: "w1", name: "Ustadzah Maryam", attendance: "yes", message: "Barakallahu lakuma wa baraka 'alaikuma wa jama'a bainakuma fi khair. Semoga menjadi keluarga sakinah, mawaddah, warahmah." },
  { id: "w2", name: "Rizky & Nadia", attendance: "yes", message: "Selamat Hamzah & Khadijah! Semoga rumah kalian selalu terang oleh iman dan kasih sayang." },
];
const WALLET = ["M19 7V4a1 1 0 0 0-1-1H5a2 2 0 0 0 0 4h15a1 1 0 0 1 1 1v4h-3a2 2 0 0 0 0 4h3a1 1 0 0 0 1-1v-2a1 1 0 0 0-1-1", "M3 5v14a2 2 0 0 0 2 2h15a1 1 0 0 0 1-1v-4"];
const BANK = ["M3 22h18", "M6 18v-7", "M10 18v-7", "M14 18v-7", "M18 18v-7", "M12 2l8 5H4z"];

/** One hanging lantern (fanous): a string, a domed cap, glowing arched windows and a tassel. */
function Lantern({ className, string = 40 }: { className?: string; string?: number }) {
  return (
    <span className={`${s.lantern} ${className ?? ""}`} style={{ ["--string" as string]: `${string}px` }} aria-hidden>
      <svg viewBox="0 0 40 92" width="40" height="92" focusable="false">
        <circle cx="20" cy="4" r="3" fill="none" stroke="currentColor" strokeWidth="1.4" />
        <path d="M20 7v4" stroke="currentColor" strokeWidth="1.4" />
        <path d="M11 22c1-7 5-11 9-11s8 4 9 11z" fill="currentColor" />
        <rect x="9" y="21" width="22" height="4" rx="1.5" fill="currentColor" />
        <path className={s.glass} d="M10.5 25 8 52c4 5 8 7 12 7s8-2 12-7l-2.5-27z" />
        <path d="M10.5 25 8 52c4 5 8 7 12 7s8-2 12-7l-2.5-27z" fill="none" stroke="currentColor" strokeWidth="1.4" />
        <path className={s.window} d="M14.5 48V33c0-3 2.5-5.5 5.5-7.5 3 2 5.5 4.5 5.5 7.5v15z" />
        <path d="M20 26v22M14.5 38h11" stroke="currentColor" strokeWidth=".9" opacity=".7" />
        <path d="M13 56l7 9 7-9" fill="currentColor" />
        <path d="M20 65v14" stroke="currentColor" strokeWidth="1.4" />
        <circle cx="20" cy="82" r="2.4" fill="currentColor" />
      </svg>
    </span>
  );
}

function Lanterns({ variant = "row" }: { variant?: "row" | "cover" | "pair" }) {
  if (variant === "pair") return <div className={s.lanternPair} aria-hidden><Lantern className={s.lanternSmall} string={8} /><Lantern string={20} /><Lantern className={s.lanternSmall} string={8} /></div>;
  if (variant === "cover") {
    return (
      <div className={s.coverLanterns} aria-hidden>
        <Lantern string={70} /><Lantern className={s.lanternSmall} string={130} /><Lantern string={34} /><Lantern className={s.lanternSmall} string={96} />
      </div>
    );
  }
  return <div className={s.lanternRow} aria-hidden><Lantern className={s.lanternSmall} string={10} /><Lantern string={26} /><Lantern className={s.lanternSmall} string={10} /></div>;
}

function Moon({ className }: { className?: string }) {
  return <span className={`${s.moon} ${className ?? ""}`} aria-hidden><i /></span>;
}

/** Four-point twinkling stars, positioned by CSS custom properties. */
function Stars({ count = 9, seed = 1 }: { count?: number; seed?: number }) {
  const list = Array.from({ length: count }, (_, i) => {
    const n = (i + 1) * 37 * seed;
    return { x: (n * 13) % 100, y: (n * 7) % 92, size: 6 + (n % 3) * 3, delay: (n % 5) * 0.9 };
  });
  return (
    <div className={s.stars} aria-hidden>
      {list.map((star, index) => (
        <svg key={index} viewBox="0 0 10 10" style={{ left: `${star.x}%`, top: `${star.y}%`, width: star.size, height: star.size, animationDelay: `${star.delay}s` }}>
          <path d="M5 0c.4 3 1.6 4.6 5 5-3.4.4-4.6 2-5 5-.4-3-1.6-4.6-5-5 3.4-.4 4.6-2 5-5z" fill="currentColor" />
        </svg>
      ))}
    </div>
  );
}

function Head({ id, kicker, title }: { id: string; kicker?: string; title: string }) {
  return (
    <div className={s.head}>
      {kicker && <p className={s.kicker}>{kicker}</p>}
      <h2 id={id}>{title}</h2>
      <span className={s.rule} aria-hidden><i /><b /><i /></span>
    </div>
  );
}

function initials(name: string) {
  return name.replace(/^(dr|drs|h|hj|ir)\.?\s+/i, "").slice(0, 1).toUpperCase() || "·";
}

function plainName(guest?: string) {
  if (!guest || guest === "Tamu Undangan") return "";
  return guest.replace(/^(bapak|ibu|bpk\.?|sdr\.?|saudara|saudari)\s+/i, "").replace(/\s*(&|dan)\s*keluarga$/i, "").trim();
}

/** "Putri kedua dari Bapak H. Syamsul Arifin & Ibu …" → "H. Syamsul Arifin" */
function father(parents?: string) {
  const match = /(?:Bapak|Bpk\.?)\s+([^&\n]+?)\s*(?:&|\n|$)/i.exec(parents ?? "");
  return match?.[1].trim();
}

export default function LenteraMalamTheme({ data, slug, guestToken, demo, skipCover }: ThemeProps) {
  const couple = coupleLabel(data);
  const label = data.eventLabel ?? "Pernikahan";
  const parts = dateParts(data.date);
  const countdown = useCountdown(data.date);
  const rsvp = useRsvp({ slug, guestToken, demo });
  const wishes = useWishes({ slug, guestToken, demo, seed: DEMO_WISHES });
  const thanks = useThankYou();
  const rsvpClosed = thanks.active || rsvp.status === "closed";
  const { copy, copied } = useCopy();
  const [attendance, setAttendance] = useState<Attendance>("yes");
  const stories = storyItems(data);
  const table = tableLabel(data.guestTable);
  const quote = data.extras?.quote?.enabled !== false && data.extras?.quote?.text ? data.extras.quote : { text: "Dan di antara tanda-tanda kekuasaan-Nya ialah Dia menciptakan untukmu pasangan dari jenismu sendiri, supaya kamu merasa tenteram kepadanya.", source: "QS. Ar-Rum: 21" };
  const hero = data.gallery[0];
  const gallery = data.gallery;
  const families = [father(data.couple.brideParents), father(data.couple.groomParents)].filter(Boolean).join(" & ");
  const sentRef = useRef<HTMLDivElement>(null);
  useEffect(() => { if (wishes.status === "sent") celebrate(sentRef.current); }, [wishes.status]);
  const people = [
    { role: "Mempelai Wanita", name: data.couple.brideFull || data.couple.bride, short: data.couple.bride, parents: data.couple.brideParents, photo: data.couple.bridePhoto },
    { role: "Mempelai Pria", name: data.couple.groomFull || data.couple.groom, short: data.couple.groom, parents: data.couple.groomParents, photo: data.couple.groomPhoto },
  ];

  return (
    <ThemeShell
      fonts={FONTS}
      background="#090f24"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.sky} aria-hidden><Stars count={14} seed={3} /></div>
          <Lanterns variant="cover" />
          <Moon className={s.coverMoon} />
          <div className={s.coverContent}>
            <p className={s.bismillah} lang="ar" dir="rtl">بِسْمِ اللّٰهِ الرَّحْمٰنِ الرَّحِيْمِ</p>
            <p className={s.kicker}>Walimatul &lsquo;Urs</p>
            <h1 className={s.coverNames}><span>{data.couple.bride}</span><em>&amp;</em><span>{data.couple.groom}</span></h1>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
          </div>
          <div className={s.kepada}>
            <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
            <strong>{guestLabel(data)}</strong>
            {table && <span className={s.table}>{table}</span>}
          </div>
          <button type="button" className={s.openBtn} onClick={open}><Icon d={icons.mailOpen} size={16} />Buka Undangan</button>
          <div className={s.horizon} aria-hidden />
        </section>
      )}
    >
      <main className={s.main}>
        <header className={s.hero}>
          <div className={s.sky} aria-hidden><Stars count={10} seed={5} /></div>
          <Lanterns variant="row" />
          <div className={s.heroArch}>
            {hero ? <Photo src={hero} alt={`Foto ${couple}`} className={s.heroImg} /> : <div className={s.heroEmpty} aria-hidden><Moon /></div>}
          </div>
          <p className={s.kicker}>The Wedding of</p>
          <h1 className={s.heroNames}>{couple}</h1>
          {parts.day ? <p className={s.heroDate}><span>{parts.weekday}</span><b>{parts.day}</b><span>{parts.month} {parts.year}</span></p> : <p className={s.heroDate}><span>{DATE_TBA}</span></p>}
        </header>

        <section className={s.salam} aria-labelledby="lm-salam">
          <h2 id="lm-salam" className={s.salamTitle}>Assalamu&rsquo;alaikum Warahmatullahi Wabarakatuh</h2>
          <p className={s.lead}>Dengan memohon rahmat dan ridha Allah Subhanahu wa Ta&rsquo;ala, kami bermaksud menyelenggarakan {label.toLowerCase()} putra-putri kami. Merupakan suatu kehormatan apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.</p>
          <figure className={s.quote}>
            <Lanterns variant="pair" />
            <blockquote>&ldquo;{quote.text}&rdquo;</blockquote>
            {quote.source && <figcaption>{quote.source}</figcaption>}
          </figure>
        </section>

        <Extras slot="opening" without={["quote"]} />

        <section className={s.section} aria-labelledby="lm-couple">
          <Head id="lm-couple" kicker="Bismillah, kami yang berbahagia" title="Kedua Mempelai" />
          <div className={s.people}>
            {people.map((person, index) => (
              <article key={index} className={s.person}>
                <div className={s.portrait}>
                  {person.photo ? <Photo src={person.photo} alt={person.name} /> : <span className={s.monogram} aria-hidden>{initials(person.short)}</span>}
                </div>
                <small>{person.role}</small>
                <h3>{person.name}</h3>
                {person.parents && <p>{person.parents}</p>}
                {index === 0 && <span className={s.amp} aria-hidden>&amp;</span>}
              </article>
            ))}
          </div>
        </section>

        <section className={`${s.section} ${s.deep}`} aria-labelledby="lm-count">
          <Stars count={8} seed={7} />
          <Head id="lm-count" kicker="Menuju hari bahagia" title="Menghitung Malam" />
          {countdown.valid ? (
            <div className={s.count} role="timer" aria-label={`${countdown.days} hari ${countdown.hours} jam ${countdown.minutes} menit lagi`}>
              {[[countdown.days, "Hari"], [countdown.hours, "Jam"], [countdown.minutes, "Menit"], [countdown.seconds, "Detik"]].map(([value, unit]) => (
                <div key={unit} className={s.countBox}><b><Tick value={value} /></b><small>{unit}</small></div>
              ))}
            </div>
          ) : <p className={s.tba}>{DATE_TBA}</p>}
        </section>

        <section className={s.section} aria-labelledby="lm-events">
          <Head id="lm-events" kicker="Waktu & tempat" title="Rangkaian Acara" />
          <div className={s.events}>
            {data.events.map((event, index) => {
              const href = mapsHref(data, event);
              return (
                <article key={event.name + index} className={s.event}>
                  <Lantern className={s.eventLantern} string={14} />
                  <h3>{event.name}</h3>
                  <p className={s.eventDate}><Icon d={icons.calendar} size={14} />{formatDate(event.date || data.date)}</p>
                  {event.time && <p className={s.eventTime}><Icon d={icons.clock} size={14} />{event.time}</p>}
                  <span className={s.rule} aria-hidden><i /><b /><i /></span>
                  <strong>{event.venue}</strong>
                  {event.address && <p className={s.eventAddr}>{event.address}</p>}
                  {href && <a className={s.ghost} href={href} target="_blank" rel="noreferrer"><Icon d={icons.mapPin} size={15} />Petunjuk Lokasi</a>}
                </article>
              );
            })}
          </div>
        </section>

        <Extras slot="event" />

        {stories.length > 0 && (
          <section className={`${s.section} ${s.deep}`} aria-labelledby="lm-story">
            <Head id="lm-story" kicker="Bagaimana Allah mempertemukan" title="Kisah Kami" />
            <ol className={s.timeline}>
              {stories.map((story, index) => (
                <li key={index}>
                  <span className={s.node} aria-hidden><svg viewBox="0 0 10 10"><path d="M5 0c.4 3 1.6 4.6 5 5-3.4.4-4.6 2-5 5-.4-3-1.6-4.6-5-5 3.4-.4 4.6-2 5-5z" fill="currentColor" /></svg></span>
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
          <section className={s.section} aria-labelledby="lm-gallery">
            <Head id="lm-gallery" kicker="Sekilas kenangan" title="Galeri" />
            <div className={s.gallery}>
              {gallery.map((src, index) => <div key={src + index} className={s.frame}><Photo src={src} alt={`Foto galeri ${index + 1}`} /></div>)}
            </div>
          </section>
        )}

        <Extras slot="story" />
        <Extras slot="end" />

        {data.gifts.length > 0 && (
          <section className={`${s.section} ${s.deep}`} aria-labelledby="lm-gift">
            <Head id="lm-gift" kicker="Tanda kasih" title="Amplop Digital" />
            <p className={s.lead}>Doa restu Anda adalah hadiah terindah. Bila berkenan memberi tanda kasih, dapat melalui:</p>
            <div className={s.gifts}>
              {data.gifts.map(gift => {
                const info = giftInfo(gift);
                const on = Boolean(info.copy && copied === info.copy);
                return (
                  <div key={gift.id} className={on ? `${s.gift} ${s.giftOn}` : s.gift}>
                    <span className={s.giftIcon}><Icon d={gift.type === "bank" ? BANK : gift.type === "address" ? icons.gift : WALLET} size={18} /></span>
                    <div className={s.giftText}>
                      <small>{info.kind}</small>
                      <strong>{info.title}</strong>
                      {info.number && <span className={s.giftNumber}>{info.number}</span>}
                      {info.holder && <span>a.n. {info.holder}</span>}
                      {info.image && <Photo src={info.image} alt="Kode QRIS" className={s.qris} />}
                    </div>
                    {info.copy && (
                      <button type="button" className={on ? `${s.copy} ${s.copyOn}` : s.copy} onClick={() => copy(info.copy)} aria-label={on ? "Tersalin" : `Salin ${info.title}`}>
                        <Icon key={on ? "on" : "off"} d={on ? icons.check : icons.copy} size={15} />
                      </button>
                    )}
                  </div>
                );
              })}
            </div>
          </section>
        )}

        <section className={s.section} aria-labelledby="lm-wishes">
          <Head id="lm-wishes" kicker="Konfirmasi & doa" title="Doa untuk Kami" />
          {wishes.status === "sent" ? (
            <div ref={sentRef} className={`${s.form} ${s.sentBox}`} role="status">
              <span className={s.sentMoon} aria-hidden><Moon /></span>
              <strong>Jazakumullahu khairan</strong>
              <p>{demo ? "Ini pratinjau — ucapan hanya tampil di daftar." : wishes.pending ? "Ucapan Anda akan tampil setelah disetujui oleh mempelai." : rsvp.status === "sent" ? "Konfirmasi dan doa Anda sudah kami terima." : "Doa Anda sudah kami terima."}</p>
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
              if (!rsvpClosed && rsvp.status !== "sent") void rsvp.submit({ name, attendance, guests, message, diet: String(form.get("diet") ?? "").trim() || undefined });
            }}>
              <label className={s.field}><span>Nama</span><input name="name" required maxLength={100} defaultValue={plainName(data.guestName)} placeholder="Nama Anda" autoComplete="name" /></label>
              {rsvpClosed ? (
                <div className={s.closed} role="status"><strong>Konfirmasi kehadiran sudah ditutup</strong><p>Terima kasih atas doa dan perhatiannya. Doa &amp; ucapan masih bisa dikirim lewat form ini.</p></div>
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
              <label className={s.field}><span>Doa &amp; ucapan</span><textarea name="message" required maxLength={500} rows={3} placeholder="Tuliskan doa terbaik Anda…" /></label>
              {(wishes.status === "error" || rsvp.status === "error") && <p className={s.error} role="alert">Belum terkirim. Periksa koneksi lalu coba lagi.</p>}
              <button type="submit" className={s.submit} disabled={wishes.status === "sending"}>{wishes.status === "sending" ? "Mengirim…" : "Kirim Doa"}</button>
            </form>
          )}
          <div className={s.wishes}>
            {wishes.wishes.length === 0 && <p className={s.empty}>Belum ada ucapan. Jadilah yang pertama mendoakan.</p>}
            {wishes.wishes.slice(0, 12).map(wish => (
              <article key={wish.id} className={s.wish}>
                <div><strong>{wish.name}</strong>{wish.attendance && <small>{ATTEND[wish.attendance]}</small>}</div>
                <p>{wish.message}</p>
              </article>
            ))}
          </div>
        </section>

        <footer className={s.closing}>
          <Stars count={10} seed={11} />
          <Moon className={s.closingMoon} />
          <p className={s.closingText}>Merupakan kebahagiaan dan kehormatan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.</p>
          <p className={s.salamEnd}>Wassalamu&rsquo;alaikum Warahmatullahi Wabarakatuh</p>
          <p className={s.familyLabel}>Kami yang berbahagia</p>
          <p className={s.closingNames}>{couple}</p>
          {families && <p className={s.families}>Keluarga Bapak {families}</p>}
          <Lanterns variant="row" />
          <a href="/" target="_blank" rel="noreferrer" className={s.made}>dibuat dengan ♥ di Rawuh</a>
        </footer>
      </main>
    </ThemeShell>
  );
}
