"use client";
// Theme "Mihrab Pastel" — syari tanpa foto: lengkung mihrab berlapis warna pastel, bintang delapan, tipografi lembut.
import { useEffect, useRef, useState, type ReactNode } from "react";
import {
  DietaryField, Extras, GuestCount, Icon, Photo, ThemeShell, Tick, coupleLabel, dateParts, formatDate, giftInfo, guestLabel, icons,
  mapsHref, storyItems, useCopy, useCountdown, DATE_TBA, useRsvp, useThankYou, useWishes, type Attendance, type ThemeProps, type Wish,
} from "../kit";
import { tableLabel } from "../extras";
import { celebrate } from "@/lib/celebrate";
import s from "./styles.module.css";

const FONTS = ["Cormorant Garamond:ital,wght@0,500;0,600;0,700;1,500;1,600", "Nunito Sans:wght@400;600;700", "Amiri:wght@400;700"];
const ATTEND: Record<Attendance, string> = { yes: "Hadir", maybe: "Ragu", no: "Berhalangan" };
const DEMO_WISHES: Wish[] = [
  { id: "w1", name: "Ummu Salamah", attendance: "yes", message: "Barakallahu lakuma. Semoga Allah himpunkan kalian dalam kebaikan hingga ke surga-Nya." },
  { id: "w2", name: "Teman halaqah Aisyah", attendance: "maybe", message: "Masya Allah, ikut bahagia. Semoga menjadi keluarga yang saling menguatkan dalam ketaatan." },
];
const POINTED = "M0 100V72C0 36 118 28 150 3c32 25 150 33 150 69v28";
const WALLET = ["M19 7V4a1 1 0 0 0-1-1H5a2 2 0 0 0 0 4h15a1 1 0 0 1 1 1v4h-3a2 2 0 0 0 0 4h3a1 1 0 0 0 1-1v-2a1 1 0 0 0-1-1", "M3 5v14a2 2 0 0 0 2 2h15a1 1 0 0 0 1-1v-4"];
const BANK = ["M3 22h18", "M6 18v-7", "M10 18v-7", "M14 18v-7", "M18 18v-7", "M12 2l8 5H4z"];

const ART = "/themes/art/mihrab-pastel";

/** Eight-point rosette, painted in watercolour (two overlapping squares + ring). */
function Star8({ className, eager = false }: { className?: string; eager?: boolean }) {
  // eslint-disable-next-line @next/next/no-img-element -- static decorative theme art
  return <img className={className} src={`${ART}/star.webp`} alt="" aria-hidden width={88} height={88} loading={eager ? "eager" : "lazy"} data-nolightbox />;
}

/** A card shaped like a mihrab niche: a painted-wash pointed cap (masked) on top of a washed body. */
function Mihrab({ children, tone = "cream", className }: { children: ReactNode; tone?: "cream" | "sage" | "rose" | "lilac"; className?: string }) {
  return (
    <div className={`${s.mihrab} ${s[tone]} ${className ?? ""}`}>
      <div className={s.cap} aria-hidden>
        <span className={s.capWash} />
        <svg viewBox="0 0 300 100" preserveAspectRatio="none" focusable="false">
          <path d={POINTED} className={s.capLine} pathLength={1} />
        </svg>
      </div>
      <Star8 className={s.apex} />
      <div className={s.body}>{children}</div>
    </div>
  );
}

/** Cover illustration: three nested mihrab arches painted in sage, blush and cream watercolour. */
function Arches() {
  // eslint-disable-next-line @next/next/no-img-element -- static decorative theme art
  return <img className={s.arches} src={`${ART}/arches.webp`} alt="" aria-hidden width={640} height={884} loading="eager" fetchPriority="high" data-nolightbox />;
}

function Head({ id, kicker, title }: { id: string; kicker?: string; title: string }) {
  return (
    <div className={s.head}>
      {kicker && <p className={s.kicker}>{kicker}</p>}
      <h2 id={id}>{title}</h2>
      <span className={s.rule} aria-hidden><i /><Star8 /><i /></span>
    </div>
  );
}

function initial(name: string) {
  return name.replace(/^(ust|dr|drs|h|hj|ir)\.?\s+/i, "").slice(0, 1).toUpperCase() || "·";
}

function plainName(guest?: string) {
  if (!guest || guest === "Tamu Undangan") return "";
  return guest.replace(/^(bapak|ibu|bpk\.?|sdr\.?|saudara|saudari)\s+/i, "").replace(/\s*(&|dan)\s*keluarga$/i, "").trim();
}

export default function MihrabPastelTheme({ data, slug, guestToken, demo, skipCover }: ThemeProps) {
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
  const stories = storyItems(data).map(story => ({ ...story, image: undefined }));
  const table = tableLabel(data.guestTable);
  const quote = data.extras?.quote?.enabled !== false && data.extras?.quote?.text ? data.extras.quote : { text: "Dan segala sesuatu Kami ciptakan berpasang-pasangan agar kamu mengingat (kebesaran Allah).", source: "QS. Adz-Dzariyat: 49" };
  const sentRef = useRef<HTMLDivElement>(null);
  useEffect(() => { if (wishes.status === "sent") celebrate(sentRef.current); }, [wishes.status]);
  const people = [
    { role: "Mempelai Wanita", name: data.couple.brideFull || data.couple.bride, short: data.couple.bride, parents: data.couple.brideParents, tone: "rose" as const },
    { role: "Mempelai Pria", name: data.couple.groomFull || data.couple.groom, short: data.couple.groom, parents: data.couple.groomParents, tone: "sage" as const },
  ];
  const tones = ["sage", "rose", "lilac", "cream"] as const;

  return (
    <ThemeShell
      fonts={FONTS}
      background="#efe8dc"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.pattern} aria-hidden />
          <div className={s.coverArch}>
            <Arches />
            <div className={s.coverContent}>
              <p className={s.bismillah} lang="ar" dir="rtl">بِسْمِ اللّٰهِ الرَّحْمٰنِ الرَّحِيْمِ</p>
              <p className={s.kicker}>Undangan {label}</p>
              <h1 className={s.coverNames}><span>{data.couple.bride}</span><em>&amp;</em><span>{data.couple.groom}</span></h1>
              <p className={s.coverDate}>{formatDate(data.date)}</p>
            </div>
          </div>
          <div className={s.kepada}>
            <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
            <strong>{guestLabel(data)}</strong>
            {table && <span className={s.table}>{table}</span>}
          </div>
          <button type="button" className={s.btn} onClick={open}><Icon d={icons.mailOpen} size={16} />Buka Undangan</button>
        </section>
      )}
    >
      <main className={s.main}>
        <header className={s.hero}>
          <div className={s.pattern} aria-hidden />
          <Mihrab tone="sage" className={s.heroArch}>
            <p className={s.arabicSm} lang="ar" dir="rtl">وَلِيْمَةُ الْعُرْسِ</p>
            <p className={s.kicker}>Walimatul &lsquo;Urs</p>
            <h1 className={s.heroNames}><span>{data.couple.bride}</span><em>&amp;</em><span>{data.couple.groom}</span></h1>
            {parts.day ? (
              <p className={s.heroDate}><span>{parts.weekday}</span><b>{parts.day}</b><span>{parts.month} {parts.year}</span></p>
            ) : <p className={s.heroDate}><span>{DATE_TBA}</span></p>}
          </Mihrab>
        </header>

        <section className={s.section} aria-labelledby="mp-salam">
          <p className={s.arabic} lang="ar" dir="rtl">السَّلَامُ عَلَيْكُمْ وَرَحْمَةُ اللّٰهِ وَبَرَكَاتُهُ</p>
          <h2 id="mp-salam" className={s.salam}>Assalamu&rsquo;alaikum Warahmatullahi Wabarakatuh</h2>
          <p className={s.lead}>Dengan memohon rahmat dan ridha Allah Subhanahu wa Ta&rsquo;ala, kami mengundang Bapak/Ibu/Saudara/i untuk menghadiri {label.toLowerCase()} kami yang insya Allah diselenggarakan dengan sederhana.</p>
          <Mihrab tone="cream" className={s.quote}>
            <blockquote>&ldquo;{quote.text}&rdquo;</blockquote>
            {quote.source && <cite>{quote.source}</cite>}
          </Mihrab>
        </section>

        <Extras slot="opening" without={["quote"]} />

        <section className={s.section} aria-labelledby="mp-couple">
          <Head id="mp-couple" kicker="Dengan izin Allah" title="Kedua Mempelai" />
          <div className={s.people}>
            {people.map((person, index) => (
              <article key={index} className={s.person}>
                <Mihrab tone={person.tone} className={s.niche}><span className={s.initial} aria-hidden>{initial(person.short)}</span></Mihrab>
                <small>{person.role}</small>
                <h3>{person.name}</h3>
                {person.parents && <p>{person.parents}</p>}
              </article>
            ))}
          </div>
        </section>

        <section className={`${s.section} ${s.tint}`} aria-labelledby="mp-count">
          <Head id="mp-count" kicker="Insya Allah" title="Menuju Hari Akad" />
          {countdown.valid ? (
            <div className={s.count} role="timer" aria-label={`${countdown.days} hari ${countdown.hours} jam ${countdown.minutes} menit lagi`}>
              {[[countdown.days, "Hari"], [countdown.hours, "Jam"], [countdown.minutes, "Menit"], [countdown.seconds, "Detik"]].map(([value, unit], index) => (
                <div key={unit} className={`${s.countBox} ${s[tones[index]]}`}><b><Tick value={value} /></b><small>{unit}</small></div>
              ))}
            </div>
          ) : <p className={s.tba}>{DATE_TBA}</p>}
        </section>

        <section className={s.section} aria-labelledby="mp-events">
          <Head id="mp-events" kicker="Waktu & tempat" title="Rangkaian Acara" />
          <div className={s.events}>
            {data.events.map((event, index) => {
              const href = mapsHref(data, event);
              return (
                <Mihrab key={event.name + index} tone={tones[index % 3]} className={s.event}>
                  <h3>{event.name}</h3>
                  <p className={s.eventDate}>{formatDate(event.date || data.date)}</p>
                  {event.time && <p className={s.eventTime}><Icon d={icons.clock} size={14} />{event.time}</p>}
                  <span className={s.dash} aria-hidden />
                  <strong>{event.venue}</strong>
                  {event.address && <p className={s.eventAddr}>{event.address}</p>}
                  {href && <a className={s.btnGhost} href={href} target="_blank" rel="noreferrer"><Icon d={icons.mapPin} size={15} />Buka Peta</a>}
                </Mihrab>
              );
            })}
          </div>
        </section>

        <Extras slot="event" />

        {stories.length > 0 && (
          <section className={`${s.section} ${s.tint}`} aria-labelledby="mp-story">
            <Head id="mp-story" kicker="Atas takdir-Nya" title="Perjalanan Kami" />
            <ol className={s.timeline}>
              {stories.map((story, index) => (
                <li key={index}>
                  <span className={s.bullet} aria-hidden><Star8 /></span>
                  <div>
                    {story.date && <small>{story.date}</small>}
                    <h3>{story.title}</h3>
                    {story.body && <p>{story.body}</p>}
                  </div>
                </li>
              ))}
            </ol>
          </section>
        )}

        <section className={s.section} aria-labelledby="mp-doa">
          <Head id="mp-doa" kicker="Doa untuk pengantin" title="Barakallahu Lakuma" />
          <Mihrab tone="lilac" className={s.doa}>
            <p className={s.arabic} lang="ar" dir="rtl">بَارَكَ اللّٰهُ لَكُمَا وَبَارَكَ عَلَيْكُمَا وَجَمَعَ بَيْنَكُمَا فِيْ خَيْرٍ</p>
            <p className={s.translit}>Barakallahu lakuma wa baraka &lsquo;alaikuma wa jama&lsquo;a bainakuma fi khair.</p>
            <p className={s.lead}>&ldquo;Semoga Allah memberkahi kalian berdua, melimpahkan keberkahan atas kalian, dan menghimpun kalian dalam kebaikan.&rdquo;</p>
            <cite>HR. Abu Dawud & Tirmidzi</cite>
          </Mihrab>
        </section>

        <Extras slot="story" />
        <Extras slot="end" />

        {data.gifts.length > 0 && (
          <section className={`${s.section} ${s.tint}`} aria-labelledby="mp-gift">
            <Head id="mp-gift" kicker="Tanda kasih" title="Hadiah & Amplop" />
            <p className={s.lead}>Kehadiran dan doa Anda sudah lebih dari cukup. Bagi yang ingin memberi tanda kasih, dapat melalui:</p>
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
                        <span>{on ? "Tersalin" : "Salin"}</span>
                      </button>
                    )}
                  </div>
                );
              })}
            </div>
          </section>
        )}

        <section className={s.section} aria-labelledby="mp-wishes">
          <Head id="mp-wishes" kicker="Konfirmasi & doa" title="Kehadiran & Doa" />
          {wishes.status === "sent" ? (
            <div ref={sentRef} className={`${s.form} ${s.sentBox}`} role="status">
              <Star8 className={s.sentStar} />
              <strong>Jazakumullahu khairan</strong>
              <p>{demo ? "Ini pratinjau — ucapan hanya tampil di daftar." : wishes.pending ? "Doa Anda akan tampil setelah disetujui oleh mempelai." : rsvp.status === "sent" ? "Konfirmasi dan doa Anda sudah kami terima." : "Doa Anda sudah kami terima."}</p>
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
              <label className={s.field}><span>Nama</span><input name="name" required maxLength={100} defaultValue={plainName(data.guestName)} placeholder="Nama Anda" autoComplete="name" /></label>
              {rsvpClosed ? (
                <div className={s.closed} role="status"><strong>Konfirmasi kehadiran sudah ditutup</strong><p>Terima kasih atas doa dan perhatiannya. Doa masih bisa dikirim lewat form ini.</p></div>
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
              <label className={s.field}><span>Doa &amp; ucapan</span><textarea name="message" required maxLength={500} rows={3} placeholder="Tuliskan doa untuk kedua mempelai…" /></label>
              {(wishes.status === "error" || rsvp.status === "error") && <p className={s.error} role="alert">Belum terkirim. Periksa koneksi lalu coba lagi.</p>}
              <button type="submit" className={s.btn} disabled={wishes.status === "sending"}>{wishes.status === "sending" ? "Mengirim…" : "Kirim Doa"}</button>
            </form>
          )}
          <div className={s.wishes}>
            {wishes.wishes.length === 0 && <p className={s.empty}>Belum ada doa. Jadilah yang pertama mendoakan.</p>}
            {wishes.wishes.slice(0, 12).map(wish => (
              <article key={wish.id} className={s.wish}>
                <span className={s.wishInitial} aria-hidden>{initial(wish.name)}</span>
                <div>
                  <p className={s.wishHead}><strong>{wish.name}</strong>{wish.attendance && <small>{ATTEND[wish.attendance]}</small>}</p>
                  <p>{wish.message}</p>
                </div>
              </article>
            ))}
          </div>
        </section>

        <footer className={s.closing}>
          <div className={s.pattern} aria-hidden />
          <Mihrab tone="rose" className={s.closingArch}>
            <p className={s.lead}>Merupakan kebahagiaan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan mendoakan.</p>
            <p className={s.salamEnd}>Wassalamu&rsquo;alaikum Warahmatullahi Wabarakatuh</p>
            <p className={s.kicker}>Kami yang berbahagia</p>
            <p className={s.closingNames}>{couple}</p>
            <p className={s.families}>beserta keluarga besar</p>
          </Mihrab>
          <a href="/" target="_blank" rel="noreferrer" className={s.made}>dibuat dengan ♥ di Rawuh</a>
        </footer>
      </main>
    </ThemeShell>
  );
}
