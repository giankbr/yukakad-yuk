"use client";
// Theme "Langit Navy" — pesta malam navy & emas: bulan sabit, bintang berkelip, rasi yang tergambar sendiri.
import { useId, type CSSProperties } from "react";
import {
  Extras, Lucide, Photo, RsvpForm, Sheet, ThemeShell, Tick, WishForm, coupleLabel, dateParts, formatDate, giftInfo, guestLabel,
  mapsHref, storyItems, useCopy, useCountdown, useMusic, DATE_TBA, useRsvp, useSheets, useThankYou, useWishes,
  type Attendance, type ThemeProps, type ThemeTint, type Wish,
} from "../kit";
import { tableLabel } from "../extras";
import type { InvitationData } from "../../types";
import { ic } from "./icons";
import s from "./styles.module.css";

const FONTS = ["Marcellus", "EB Garamond:ital,wght@0,400;0,500;1,400", "Parisienne"];
const ATTEND: Record<Attendance, string> = { yes: "Hadir", maybe: "Ragu", no: "Berhalangan" };
const DEMO_WISHES: Wish[] = [
  { id: "w1", name: "Kak Vania", attendance: "yes", message: "Selamat Gracia & Nael! Semoga kasih kalian bersinar terus seperti bintang yang tak pernah lelah menyala. Tuhan memberkati." },
  { id: "w2", name: "Tim Dev Lantai 12", attendance: "maybe", message: "Happy wedding, Nael! Semoga rumah tangganya selalu bebas bug dan penuh sukacita." },
];
const tint: ThemeTint = {
  "--t-accent": "#d6b46a", "--t-accent-ink": "#0b1630", "--t-bg": "#13254a", "--t-ink": "#f2eee3", "--t-muted": "#a9b3c9",
  "--t-line": "rgba(214, 180, 106, .35)", "--t-field": "#0f1f40", "--t-radius": "12px", "--t-font": "\"EB Garamond\", Georgia, serif",
};

function Star({ className, style }: { className?: string; style?: CSSProperties }) {
  return <svg className={className} style={style} viewBox="0 0 20 20" aria-hidden="true" focusable="false"><path d="M10 0c.7 5 4.3 8.6 10 10-5.7 1.4-9.3 5-10 10-.7-5-4.3-8.6-10-10C5.7 8.6 9.3 5 10 0z" /></svg>;
}

function Moon({ className }: { className?: string }) {
  const id = useId().replace(/:/g, "");
  return (
    <svg className={className} viewBox="0 0 120 120" aria-hidden="true" focusable="false">
      <defs>
        <radialGradient id={`lm${id}`} cx="40%" cy="38%" r="70%"><stop offset="0" stopColor="#fbefc8" /><stop offset=".7" stopColor="#e3c47f" /><stop offset="1" stopColor="#c59f55" /></radialGradient>
        <mask id={`lc${id}`}><rect width="120" height="120" fill="#fff" /><circle cx="78" cy="46" r="42" fill="#000" /></mask>
      </defs>
      <circle cx="60" cy="60" r="46" fill={`url(#lm${id})`} mask={`url(#lc${id})`} />
      <g fill="#c59f55" opacity=".35" mask={`url(#lc${id})`}><circle cx="34" cy="70" r="5" /><circle cx="46" cy="88" r="3" /><circle cx="28" cy="52" r="2.5" /></g>
    </svg>
  );
}

/** A small constellation whose lines draw themselves in. */
function Constellation({ className }: { className?: string }) {
  const points: Array<[number, number]> = [[8, 48], [46, 22], [92, 34], [128, 10], [170, 30], [206, 18]];
  return (
    <svg className={className} viewBox="0 0 214 60" aria-hidden="true" focusable="false">
      <polyline className={s.cLine} points={points.map(p => p.join(",")).join(" ")} pathLength="1" />
      {points.map(([x, y], index) => <circle key={index} cx={x} cy={y} r={index % 2 ? 2.2 : 3} className={s.cDot} style={{ animationDelay: `${index * 0.7}s` }} />)}
    </svg>
  );
}

function Head({ id, kicker, title }: { id: string; kicker: string; title: string }) {
  return (
    <div className={s.head}>
      <p className={s.kicker}><Star className={s.kStar} />{kicker}<Star className={s.kStar} /></p>
      <h2 id={id}>{title}</h2>
    </div>
  );
}

function father(parents?: string) {
  const match = /(?:Bapak|Bpk\.?)\s+([^&\n]+?)\s*(?:&|\n|$)/i.exec(parents ?? "");
  return match?.[1].trim();
}

function islamic(data: InvitationData) {
  return data.events.some(event => /akad|ijab|walimah/i.test(event.name)) || /\bQS\b|Q\.S\./.test(data.extras?.quote?.source ?? "");
}

export default function LangitNavyTheme({ data, slug, guestToken, demo, skipCover }: ThemeProps) {
  const couple = coupleLabel(data);
  const label = data.eventLabel ?? "Pernikahan";
  const parts = dateParts(data.date);
  const countdown = useCountdown(data.date);
  const rsvp = useRsvp({ slug, guestToken, demo });
  const wishes = useWishes({ slug, guestToken, demo, seed: DEMO_WISHES });
  const thanks = useThankYou();
  const rsvpClosed = thanks.active || rsvp.status === "closed";
  const sheets = useSheets();
  const { copy, copied } = useCopy();
  const music = useMusic(data.music);
  const stories = storyItems(data);
  const gallery = data.gallery;
  const hero = gallery[0];
  const table = tableLabel(data.guestTable);
  const quote = data.extras?.quote && data.extras.quote.enabled !== false ? data.extras.quote : undefined;
  const muslim = islamic(data);
  const families = [father(data.couple.brideParents), father(data.couple.groomParents)].filter(Boolean);
  const people = [
    { key: "bride", short: data.couple.bride, name: data.couple.brideFull ?? data.couple.bride, parents: data.couple.brideParents, photo: data.couple.bridePhoto },
    { key: "groom", short: data.couple.groom, name: data.couple.groomFull ?? data.couple.groom, parents: data.couple.groomParents, photo: data.couple.groomPhoto },
  ].filter(person => person.short || person.name);

  return (
    <ThemeShell
      fonts={FONTS}
      background="#070f22"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.sky} aria-hidden>
            {[[8, 14, 12], [84, 10, 9], [72, 30, 6], [16, 44, 7], [90, 58, 11], [6, 74, 8], [60, 86, 6], [30, 92, 10]].map(([x, y, size], index) => (
              <Star key={index} className={s.twinkle} style={{ left: `${x}%`, top: `${y}%`, width: size, animationDelay: `${index * 0.6}s` }} />
            ))}
          </div>
          <div className={s.moonWrap}><Moon className={s.moon} /></div>
          <p className={s.kicker}>The Wedding of</p>
          <h1 className={s.coverNames}><span>{data.couple.bride}</span>{data.couple.groom && <><em>&amp;</em><span>{data.couple.groom}</span></>}</h1>
          <Constellation className={s.coverConst} />
          <p className={s.coverDate}>{parts.day ? `${parts.weekday}, ${parts.day} ${parts.month} ${parts.year}` : DATE_TBA}</p>
          <div className={s.guest}>
            <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
            <strong>{guestLabel(data)}</strong>
            {table && <span>{table}</span>}
          </div>
          <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.moonStar} size={16} color="#0b1630" />Buka Undangan</button>
        </section>
      )}
    >
      <main className={s.main}>
        <header className={s.hero} data-reveal-block>
          <div className={s.orbit}>
            <span className={s.orbitRing} aria-hidden><i /></span>
            <div className={s.heroCircle}>{hero ? <Photo src={hero} alt={`Foto ${couple}`} /> : <Moon className={s.heroMoon} />}</div>
          </div>
          <p className={s.kicker}>{label}</p>
          <h1 className={s.heroNames}>{couple}</h1>
          <p className={s.heroDate}>{formatDate(data.date)}</p>
        </header>

        <section className={s.opening} aria-label="Pembuka">
          <Moon className={s.smallMoon} />
          <p className={s.salam}>{muslim ? "Assalamu'alaikum Warahmatullahi Wabarakatuh" : "Salam sejahtera dalam kasih Tuhan"}</p>
          {quote ? (
            <blockquote className={s.quote}><p>“{quote.text}”</p>{quote.source && <cite>{quote.source}</cite>}</blockquote>
          ) : data.couple.note ? <p className={s.quote}>{data.couple.note}</p> : null}
        </section>

        <Extras slot="opening" without={["quote"]} />

        <section className={s.section} aria-labelledby="ln-couple">
          <Head id="ln-couple" kicker="Mempelai" title="Dua Bintang, Satu Langit" />
          <p className={s.intro}>Dengan penuh sukacita, kami mengundang Bapak/Ibu/Saudara/i untuk hadir dalam {label.toLowerCase()} kami:</p>
          <div className={s.people}>
            {people.map((person, index) => (
              <div key={person.key} className={s.personWrap}>
                {index === 1 && <p className={s.amp} aria-hidden>&amp;</p>}
                <article className={s.person}>
                  <div className={s.orbitSmall}>
                    <span className={s.orbitRing} aria-hidden><i /></span>
                    <div className={s.portrait}>{person.photo ? <Photo src={person.photo} alt={person.name} /> : <span className={s.initial} aria-hidden>{person.short.charAt(0).toUpperCase()}</span>}</div>
                  </div>
                  <p className={s.script}>{person.short}</p>
                  <h3>{person.name}</h3>
                  {person.parents && <p className={s.parents}>{person.parents}</p>}
                </article>
              </div>
            ))}
          </div>
        </section>

        <section className={`${s.section} ${s.band}`} aria-labelledby="ln-count">
          <Head id="ln-count" kicker="Menghitung Malam" title="Menuju Hari Bahagia" />
          {countdown.valid ? (
            <div className={s.count} role="timer" aria-label={`${countdown.days} hari ${countdown.hours} jam ${countdown.minutes} menit lagi`}>
              {[[countdown.days, "Hari"], [countdown.hours, "Jam"], [countdown.minutes, "Menit"], [countdown.seconds, "Detik"]].map(([value, unit]) => (
                <div key={unit}>
                  <span className={s.phase}><b><Tick value={value} /></b></span>
                  <small>{unit}</small>
                </div>
              ))}
            </div>
          ) : <p className={s.countTba}>{DATE_TBA}</p>}
        </section>

        <section className={s.section} aria-labelledby="ln-events">
          <Head id="ln-events" kicker="Waktu & Tempat" title="Rangkaian Acara" />
          <div className={s.events}>
            {data.events.map((event, index) => {
              const maps = mapsHref(data, event);
              return (
                <article key={event.name + index} className={s.event}>
                  <Star className={s.eventStar} />
                  <h3>{event.name}</h3>
                  <p className={s.when}>{formatDate(event.date || data.date)}</p>
                  {event.time && <p className={s.time}><Lucide icon={ic.clock3} size={14} />{event.time}</p>}
                  <span className={s.sep} aria-hidden />
                  <p className={s.venue}>{event.venue}</p>
                  {event.address && <p className={s.addr}>{event.address}</p>}
                  {maps && <a className={s.goldBtn} href={maps} target="_blank" rel="noreferrer"><Lucide icon={ic.mapPin} size={15} />Buka Peta</a>}
                </article>
              );
            })}
          </div>
        </section>

        <Extras slot="event" />

        {stories.length > 0 && (
          <section className={s.section} aria-labelledby="ln-story">
            <Head id="ln-story" kicker="Rasi Kisah Kami" title="Perjalanan Cinta" />
            <ol className={s.story}>
              {stories.map((story, index) => (
                <li key={index}>
                  <span className={s.node} aria-hidden><Star className={s.nodeStar} /><i /></span>
                  <div>
                    {story.date && <p className={s.storyDate}>{story.date}</p>}
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
          <section className={s.section} aria-labelledby="ln-gallery">
            <Head id="ln-gallery" kicker="Galeri" title="Momen di Bawah Langit" />
            <div className={s.gallery}>
              {gallery.slice(0, 9).map((src, index) => <div key={src + index} className={s.tile}><Photo src={src} alt={`Foto galeri ${index + 1}`} /></div>)}
            </div>
          </section>
        )}

        <Extras slot="story" />

        <Extras slot="end" />

        {data.gifts.length > 0 && (
          <section className={s.section} aria-labelledby="ln-gift">
            <Head id="ln-gift" kicker="Tanda Kasih" title="Kado Pernikahan" />
            <p className={s.intro}>Doa dan kehadiran Anda adalah hadiah terindah. Bila ingin memberi tanda kasih, dapat melalui:</p>
            <div className={s.gifts}>
              {data.gifts.map(gift => {
                const info = giftInfo(gift);
                const on = Boolean(info.copy) && copied === info.copy;
                const icon = gift.type === "bank" ? ic.landmark : gift.type === "address" ? ic.gift : gift.type === "qris" ? ic.qrCode : ic.wallet;
                return (
                  <article key={gift.id} className={`${s.gift} ${on ? s.giftOn : ""}`}>
                    <span className={s.giftIcon}><Lucide icon={icon} size={19} /></span>
                    <div className={s.giftBody}>
                      <small>{info.kind}</small>
                      <h3>{info.title}</h3>
                      {info.number && <p className={s.giftNo}>{info.number}</p>}
                      {info.holder && <p className={s.giftName}>a.n. {info.holder}</p>}
                      {info.image && <Photo src={info.image} alt="Kode QRIS" className={s.qris} />}
                    </div>
                    {info.copy && (
                      <button type="button" className={s.copyBtn} onClick={() => copy(info.copy)} aria-label={on ? "Tersalin" : `Salin ${info.title}`}>
                        <Lucide key={on ? "on" : "off"} icon={on ? ic.check : ic.copy} size={15} />
                      </button>
                    )}
                  </article>
                );
              })}
            </div>
          </section>
        )}

        <section className={s.section} aria-labelledby="ln-rsvp">
          <Head id="ln-rsvp" kicker="RSVP" title="Kirim Doa ke Langit" />
          <div className={s.rsvp}>
            <Constellation className={s.rsvpConst} />
            {rsvpClosed ? (
              <div className={s.closed} role="status"><strong>Konfirmasi kehadiran sudah ditutup</strong><p>Terima kasih atas doa dan perhatiannya. Ucapan masih dapat dikirim.</p></div>
            ) : rsvp.status === "sent" ? (
              <p className={s.done}><Lucide icon={ic.check} size={16} />Terima kasih, konfirmasi Anda sudah kami terima.</p>
            ) : (
              <>
                <p className={s.intro}>Apakah Anda dapat hadir merayakan malam bahagia kami?</p>
                <div className={s.quick}>
                  {(["yes", "maybe", "no"] as Attendance[]).map(value => (
                    <button key={value} type="button" onClick={() => sheets.openRsvp(value)}>{ATTEND[value]}</button>
                  ))}
                </div>
              </>
            )}
            <button type="button" className={s.goldBtn} onClick={sheets.openWish}><Lucide icon={ic.sparkles} size={15} />Tulis Ucapan &amp; Doa</button>
          </div>
          <div className={s.wishes}>
            {wishes.wishes.length === 0 && <p className={s.empty}>Belum ada ucapan. Jadilah bintang pertama.</p>}
            {wishes.wishes.slice(0, 10).map(wish => (
              <article key={wish.id} className={s.wish}>
                <Star className={s.wishStar} />
                <div>
                  <div className={s.wishHead}><strong>{wish.name}</strong>{wish.attendance && <small>{ATTEND[wish.attendance]}</small>}</div>
                  <p>{wish.message}</p>
                </div>
              </article>
            ))}
          </div>
        </section>

        <footer className={s.closing}>
          <div className={s.closingSky} aria-hidden>
            <Moon className={s.closingMoon} />
            <Star className={s.twinkle} style={{ left: "18%", top: "20%", width: 10 }} />
            <Star className={s.twinkle} style={{ left: "78%", top: "64%", width: 8, animationDelay: "1.4s" }} />
            <Star className={s.twinkle} style={{ left: "70%", top: "10%", width: 6, animationDelay: "2.6s" }} />
          </div>
          <p className={s.kicker}>Terima Kasih</p>
          <p className={s.closingText}>Merupakan sukacita bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.</p>
          {muslim && <p className={s.salamEnd}>Wassalamu&apos;alaikum Warahmatullahi Wabarakatuh</p>}
          <p className={s.closingNames}>{couple}</p>
          {families.length > 0 && <p className={s.family}>beserta keluarga besar<br />Bapak {families.join(" & Bapak ")}</p>}
          <a href="/" target="_blank" rel="noreferrer" className={s.made}>dibuat dengan ♥ di Rawuh</a>
        </footer>
      </main>

      {music.visible && !music.failed && (
        <button type="button" className={`${s.music} ${music.playing ? s.musicOn : ""}`} onClick={music.toggle} aria-pressed={music.playing} aria-label={music.playing ? "Matikan musik" : "Putar musik"}>
          <Lucide icon={ic.music} size={17} />
        </button>
      )}

      <Sheet open={sheets.sheet === "rsvp"} onClose={sheets.close} title="Konfirmasi Kehadiran" tint={tint}>
        <RsvpForm key={sheets.attendance} rsvp={rsvp} guestName={data.guestName} demo={demo} initialAttendance={sheets.attendance} />
      </Sheet>
      <Sheet open={sheets.sheet === "wish"} onClose={sheets.close} title="Ucapan & Doa" tint={tint}>
        <WishForm wishes={wishes} guestName={data.guestName} demo={demo} submitLabel="Kirim Doa" />
      </Sheet>
    </ThemeShell>
  );
}
