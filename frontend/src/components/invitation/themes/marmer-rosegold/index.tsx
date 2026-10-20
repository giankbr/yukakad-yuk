"use client";
// Theme "Marmer Rose Gold" — marmer putih modern, garis tipis rose gold, bingkai geometris dan kilau foil.
import {
  Extras, Lucide, Photo, RsvpForm, Sheet, ThemeShell, Tick, WishForm, coupleLabel, dateParts, formatDate, giftInfo, guestLabel,
  mapsHref, storyItems, useCopy, useCountdown, useMusic, DATE_TBA, useRsvp, useSheets, useThankYou, useWishes,
  type Attendance, type ThemeProps, type ThemeTint, type Wish,
} from "../kit";
import { tableLabel } from "../extras";
import type { InvitationData } from "../../types";
import { ic } from "./icons";
import s from "./styles.module.css";

const FONTS = ["Italiana", "Jost:wght@300;400;500"];
const ATTEND: Record<Attendance, string> = { yes: "Hadir", maybe: "Ragu", no: "Berhalangan" };
const DEMO_WISHES: Wish[] = [
  { id: "w1", name: "Clarissa Wijaya", attendance: "yes", message: "Selamat Alesha & Damar! Semoga pernikahan kalian seindah dan sekokoh marmer, berkilau sepanjang usia." },
  { id: "w2", name: "Om Freddy & Tante Lina", attendance: "yes", message: "Selamat menempuh hidup baru. Semoga selalu saling menguatkan dalam suka dan duka." },
];
const tint: ThemeTint = {
  "--t-accent": "#b5736f", "--t-accent-ink": "#ffffff", "--t-bg": "#fbfaf8", "--t-ink": "#2e2a2b", "--t-muted": "#8a8183",
  "--t-line": "#e7dcd6", "--t-field": "#ffffff", "--t-radius": "2px", "--t-font": "Jost, system-ui, sans-serif",
};

const ART = "/themes/art/marmer-rosegold";

/** Decorative painted/foil image (never opens the photo lightbox). */
function Art({ src, className, w, h, eager }: { src: string; className?: string; w: number; h: number; eager?: boolean }) {
  return (
    // eslint-disable-next-line @next/next/no-img-element -- static painted ornament
    <img src={`${ART}/${src}.webp`} alt="" aria-hidden width={w} height={h} className={className} data-nolightbox
      loading={eager ? "eager" : "lazy"} fetchPriority={eager ? "high" : undefined} decoding="async" draggable={false} />
  );
}

function Head({ id, kicker, title, light }: { id: string; kicker: string; title: string; light?: boolean }) {
  return (
    <div className={`${s.head} ${light ? s.headLight : ""}`}>
      <p className={s.kicker}>{kicker}</p>
      <h2 id={id}>{title}</h2>
      <Art src="rule" className={s.rule} w={210} h={16} />
    </div>
  );
}

/** "Bapak Ir. Hendra Gunawan & Ibu Sinta" → "Hendra Gunawan" */
function father(parents?: string) {
  const match = /(?:Bapak|Bpk\.?)\s+(?:Ir\.|Dr\.|H\.|Drs\.|Prof\.)?\s*([^&\n]+?)\s*(?:&|\n|$)/i.exec(parents ?? "");
  return match?.[1].trim();
}

function islamic(data: InvitationData) {
  return data.events.some(event => /akad|ijab|walimah/i.test(event.name)) || /\bQS\b|Q\.S\./.test(data.extras?.quote?.source ?? "");
}

function dotted(value?: string) {
  const date = value ? new Date(value) : undefined;
  if (!date || Number.isNaN(date.getTime())) return DATE_TBA;
  const part = (o: Intl.DateTimeFormatOptions) => new Intl.DateTimeFormat("id-ID", { timeZone: "Asia/Jakarta", ...o }).format(date);
  return `${part({ day: "2-digit" })} · ${part({ month: "2-digit" })} · ${part({ year: "numeric" })}`;
}

export default function MarmerRoseGoldTheme({ data, slug, guestToken, demo, skipCover }: ThemeProps) {
  const couple = coupleLabel(data);
  const label = data.eventLabel ?? "Pernikahan";
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
  const mono = `${data.couple.bride?.charAt(0) ?? ""}${data.couple.groom ? data.couple.groom.charAt(0) : ""}`.toUpperCase();

  const people = [
    { key: "bride", role: "Mempelai Wanita", short: data.couple.bride, name: data.couple.brideFull ?? data.couple.bride, parents: data.couple.brideParents, photo: data.couple.bridePhoto },
    { key: "groom", role: "Mempelai Pria", short: data.couple.groom, name: data.couple.groomFull ?? data.couple.groom, parents: data.couple.groomParents, photo: data.couple.groomPhoto },
  ].filter(person => person.short || person.name);

  return (
    <ThemeShell
      fonts={FONTS}
      background="#e9e4df"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.stage}>
          <Art src="frame" className={s.coverFrame} w={600} h={940} eager />
          <div className={s.coverInner}>
            <p className={s.kicker}>The Wedding of</p>
            <h1 className={s.coverNames}><span className={s.foil}>{data.couple.bride}</span>{data.couple.groom && <><em className={s.foil}>&amp;</em><span className={s.foil}>{data.couple.groom}</span></>}</h1>
            <p className={s.coverDate}>{dotted(data.date)}</p>
          </div>
          </div>
          <div className={s.guest}>
            <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
            <strong>{guestLabel(data)}</strong>
            {table && <span>{table}</span>}
          </div>
          <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#fff" />Buka Undangan</button>
        </section>
      )}
    >
      <main className={s.main}>
        <header className={s.hero} data-reveal-block>
          <div className={s.heroPhoto}>
            {hero ? <Photo src={hero} alt={`Foto ${couple}`} className={s.heroImg} /> : <div className={s.heroMono} aria-hidden><span className={s.foil}>{mono}</span></div>}
          </div>
          <div className={s.heroCard}>
            <p className={s.kicker}>{label}</p>
            <h1><span className={s.foil}>{couple}</span></h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
          </div>
        </header>

        <section className={s.opening} aria-label="Pembuka">
          <p className={s.salam}>{muslim ? "Assalamu'alaikum Warahmatullahi Wabarakatuh" : "Salam sejahtera bagi kita semua"}</p>
          {quote ? (
            <blockquote className={s.quote}><span aria-hidden>“</span><p>{quote.text}</p>{quote.source && <cite>{quote.source}</cite>}</blockquote>
          ) : (
            <p className={s.lead}>{data.couple.note}</p>
          )}
        </section>

        <Extras slot="opening" without={["quote"]} />

        <section className={s.section} aria-labelledby="mr-couple">
          <Head id="mr-couple" kicker="Bride & Groom" title="Mempelai" />
          <p className={s.intro}>Dengan memohon rahmat dan ridha Tuhan Yang Maha Esa, kami bermaksud menyelenggarakan {label.toLowerCase()} putra-putri kami:</p>
          <div className={s.people}>
            {people.map((person, index) => (
              <article key={person.key} className={`${s.person} ${index % 2 ? s.personAlt : ""}`}>
                <div className={s.portrait}>
                  {person.photo ? <Photo src={person.photo} alt={person.name} /> : <div className={s.portraitMono} aria-hidden><span className={s.foil}>{person.short.charAt(0).toUpperCase()}</span></div>}
                </div>
                <div className={s.personText}>
                  <p className={s.kicker}>{person.role}</p>
                  <h3>{person.name}</h3>
                  {person.parents && <p>{person.parents}</p>}
                </div>
              </article>
            ))}
          </div>
        </section>

        <section className={`${s.section} ${s.dark}`} aria-labelledby="mr-count">
          <Head id="mr-count" kicker="Save the Date" title="Menuju Hari Bahagia" light />
          {countdown.valid ? (
            <div className={s.count} role="timer" aria-label={`${countdown.days} hari ${countdown.hours} jam ${countdown.minutes} menit lagi`}>
              {[[countdown.days, "Hari"], [countdown.hours, "Jam"], [countdown.minutes, "Menit"], [countdown.seconds, "Detik"]].map(([value, unit]) => (
                <div key={unit}><b><Tick value={value} /></b><small>{unit}</small></div>
              ))}
            </div>
          ) : <p className={s.countTba}>{DATE_TBA}</p>}
          <p className={s.countDate}>{dotted(data.date)}</p>
        </section>

        <section className={s.section} aria-labelledby="mr-events">
          <Head id="mr-events" kicker="Wedding Day" title="Rangkaian Acara" />
          <div className={s.events}>
            {data.events.map((event, index) => {
              const p = dateParts(event.date || data.date);
              const maps = mapsHref(data, event);
              return (
                <article key={event.name + index} className={s.event}>
                  <div className={s.eventDate} aria-hidden>
                    <b className={s.foil}>{p.day || "—"}</b>
                    <small>{p.monthShort || "TBA"}</small>
                    <small>{p.year}</small>
                  </div>
                  <div className={s.eventBody}>
                    <h3>{event.name}</h3>
                    <p className={s.eventWhen}>{formatDate(event.date || data.date, { weekday: "long", day: "numeric", month: "long" })}{event.time ? ` · ${event.time}` : ""}</p>
                    <p className={s.venue}>{event.venue}</p>
                    {event.address && <p className={s.addr}>{event.address}</p>}
                    {maps && <a className={s.link} href={maps} target="_blank" rel="noreferrer"><Lucide icon={ic.mapPin} size={14} />Lihat Lokasi</a>}
                  </div>
                </article>
              );
            })}
          </div>
        </section>

        <Extras slot="event" />

        {stories.length > 0 && (
          <section className={s.section} aria-labelledby="mr-story">
            <Head id="mr-story" kicker="Our Story" title="Kisah Kami" />
            <ol className={s.story}>
              {stories.map((story, index) => (
                <li key={index}>
                  <span className={s.num} aria-hidden>{String(index + 1).padStart(2, "0")}</span>
                  <div>
                    {story.date && <p className={s.kicker}>{story.date}</p>}
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
          <section className={s.section} aria-labelledby="mr-gallery">
            <Head id="mr-gallery" kicker="Gallery" title="Galeri" />
            <div className={s.gallery}>
              {gallery.slice(0, 9).map((src, index) => (
                <div key={src + index} className={s.tile}><Photo src={src} alt={`Foto galeri ${index + 1}`} /></div>
              ))}
            </div>
          </section>
        )}

        <Extras slot="story" />

        <Extras slot="end" />

        {data.gifts.length > 0 && (
          <section className={s.section} aria-labelledby="mr-gift">
            <Head id="mr-gift" kicker="Wedding Gift" title="Tanda Kasih" />
            <p className={s.intro}>Kehadiran dan doa Anda adalah hadiah terbaik. Namun bila ingin memberi tanda kasih, dapat melalui:</p>
            <div className={s.cards}>
              {data.gifts.map(gift => {
                const info = giftInfo(gift);
                const on = Boolean(info.copy) && copied === info.copy;
                const metal = gift.type === "bank" || gift.type === "ewallet";
                return (
                  <article key={gift.id} className={`${metal ? s.card : s.cardPlain} ${on ? s.cardOn : ""}`}>
                    <div className={s.cardTop}>
                      <span>{info.kind}</span>
                      <b>{info.title}</b>
                    </div>
                    {metal && <span className={s.chip} aria-hidden />}
                    {info.number && <p className={s.cardNo}>{info.number}</p>}
                    {info.image && <Photo src={info.image} alt="Kode QRIS" className={s.qris} />}
                    <div className={s.cardFoot}>
                      <span>{info.holder ? info.holder : gift.type === "address" ? "Alamat pengiriman" : ""}</span>
                      {info.copy && (
                        <button type="button" className={s.copyBtn} onClick={() => copy(info.copy)} aria-label={on ? "Tersalin" : `Salin ${info.title}`}>
                          <Lucide key={on ? "on" : "off"} icon={on ? ic.check : ic.copy} size={14} />{on ? "Tersalin" : "Salin"}
                        </button>
                      )}
                    </div>
                  </article>
                );
              })}
            </div>
          </section>
        )}

        <section className={s.section} aria-labelledby="mr-rsvp">
          <Head id="mr-rsvp" kicker="RSVP" title="Kehadiran & Ucapan" />
          <div className={s.rsvpCard}>
            {rsvpClosed ? (
              <div className={s.closed} role="status"><strong>Konfirmasi kehadiran sudah ditutup</strong><p>Terima kasih atas doa dan perhatiannya. Ucapan masih dapat dikirim.</p></div>
            ) : rsvp.status === "sent" ? (
              <p className={s.done}><Lucide icon={ic.check} size={16} />Konfirmasi kehadiran Anda sudah kami terima.</p>
            ) : (
              <>
                <p className={s.intro}>Mohon konfirmasi kehadiran Anda agar kami dapat menyiapkan tempat terbaik.</p>
                <div className={s.quick}>
                  {(["yes", "maybe", "no"] as Attendance[]).map(value => (
                    <button key={value} type="button" onClick={() => sheets.openRsvp(value)}>{ATTEND[value]}</button>
                  ))}
                </div>
              </>
            )}
            <button type="button" className={s.primary} onClick={sheets.openWish}><Lucide icon={ic.penLine} size={15} color="#fff" />Tulis Ucapan</button>
          </div>
          <div className={s.wishes}>
            {wishes.wishes.length === 0 && <p className={s.empty}>Belum ada ucapan. Jadilah yang pertama.</p>}
            {wishes.wishes.slice(0, 10).map(wish => (
              <article key={wish.id} className={s.wish}>
                <p>{wish.message}</p>
                <div><strong>{wish.name}</strong>{wish.attendance && <small>{ATTEND[wish.attendance]}</small>}</div>
              </article>
            ))}
          </div>
        </section>

        <footer className={s.closing}>
          <div className={s.mono} aria-hidden>
            <Art src="ring" className={s.monoRing} w={296} h={296} />
            <span className={s.foil}>{mono}</span>
          </div>
          <p className={s.kicker}>Thank You</p>
          <h2 className={s.thanks}>Terima Kasih</h2>
          <p className={s.closingText}>Merupakan kehormatan dan kebahagiaan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.</p>
          {muslim && <p className={s.salamEnd}>Wassalamu&apos;alaikum Warahmatullahi Wabarakatuh</p>}
          <p className={s.family}>Kami yang berbahagia,<br /><b>{couple}</b>{families.length > 0 && <><br />beserta keluarga besar Bapak {families.join(" & Bapak ")}</>}</p>
          <a href="/" target="_blank" rel="noreferrer" className={s.made}>dibuat dengan ♥ di Rawuh</a>
        </footer>
      </main>

      {music.visible && !music.failed && (
        <button type="button" className={`${s.music} ${music.playing ? s.musicOn : ""}`} onClick={music.toggle} aria-pressed={music.playing} aria-label={music.playing ? "Matikan musik" : "Putar musik"}>
          <Lucide icon={ic.music} size={17} color="#fff" />
        </button>
      )}

      <Sheet open={sheets.sheet === "rsvp"} onClose={sheets.close} title="Konfirmasi Kehadiran" tint={tint}>
        <RsvpForm key={sheets.attendance} rsvp={rsvp} guestName={data.guestName} demo={demo} initialAttendance={sheets.attendance} />
      </Sheet>
      <Sheet open={sheets.sheet === "wish"} onClose={sheets.close} title="Ucapan & Doa" tint={tint}>
        <WishForm wishes={wishes} guestName={data.guestName} demo={demo} />
      </Sheet>
    </ThemeShell>
  );
}
