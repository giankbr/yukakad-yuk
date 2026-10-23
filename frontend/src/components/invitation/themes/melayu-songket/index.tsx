"use client";
// Theme "Melayu Songket" — adat Melayu kuning-hijau: bidang songket bertabur bunga, tepi kain pucuk rebung,
// medalion bunga cengkih dan awan larat, dibuka dengan pantun. Ornamen digambar sendiri untuk Rawuh.
import { useEffect, useRef, useState } from "react";
import {
  DietaryField, Extras, GuestCount, Lucide, Photo, ThemeShell, Tick, coupleLabel, dateParts, formatDate, giftInfo, guestLabel,
  mapsHref, storyItems, toDate, useCopy, useCountdown, useMusic, DATE_TBA, useRsvp, useThankYou, useWishes,
  type Attendance, type ThemeProps, type Wish,
} from "../kit";
import { tableLabel } from "../extras";
import type { InvitationData } from "../../types";
import { celebrate } from "@/lib/celebrate";
import { ic } from "./icons";
import { AwanLarat, Medallion, Rebung } from "./ornaments";
import s from "./styles.module.css";

const FONTS = ["Marcellus", "EB Garamond:ital,wght@0,400;0,500;0,600;0,700;1,400;1,500"];
const ATTEND: Record<Attendance, string> = { yes: "Hadir", maybe: "Ragu", no: "Berhalangan" };
const DEMO_WISHES: Wish[] = [
  { id: "w1", name: "Mak Long Rosnah", attendance: "yes", message: "Selamat menempuh hidup baru, Aisyah dan Fadhil. Semoga berkekalan hingga ke anak cucu, menjadi keluarga sakinah mawaddah warahmah." },
  { id: "w2", name: "Wan Hafiz", attendance: "maybe", message: "Selamat pengantin baru, sahabat! Semoga dimudahkan segala urusan dan dilimpahi berkah." },
];
const QUOTE = { text: "Dan segala sesuatu Kami ciptakan berpasang-pasangan agar kamu mengingat (kebesaran Allah).", source: "QS. Adz-Dzariyat: 49" };
const PANTUN_OPEN = ["Sirih berlipat sirih pinang,", "Sirih dari Pulau Mutiara;", "Pemanis kata selamat datang,", "Awal Bismillah pembuka bicara."];
const PANTUN_CLOSE = ["Kalau ada jarum yang patah,", "Jangan disimpan di dalam peti;", "Kalau ada silap dan salah,", "Jangan disimpan di dalam hati."];

function Head({ id, kicker, title, light }: { id: string; kicker?: string; title: string; light?: boolean }) {
  return (
    <div className={light ? `${s.head} ${s.headLight}` : s.head}>
      {kicker && <p className={s.kicker}>{kicker}</p>}
      <h2 id={id}>{title}</h2>
      <AwanLarat className={s.awan} />
    </div>
  );
}

function father(parents?: string) {
  const match = /(?:Bapak|Bpk\.?)\s+([^&\n]+?)\s*(?:&|\n|$)/i.exec(parents ?? "");
  return match?.[1].trim();
}

function plainName(guest?: string) {
  if (!guest || guest === "Tamu Undangan") return "";
  return guest.replace(/^(bapak|ibu|bpk\.?|sdr\.?|saudara|saudari)\s+/i, "").replace(/\s*(&|dan)\s*keluarga$/i, "").trim();
}

function calendarHref(data: InvitationData) {
  const start = toDate(data.date) ?? toDate(data.events[0]?.date);
  if (!start) return undefined;
  const lastStart = toDate(data.events[data.events.length - 1]?.date) ?? start;
  const end = new Date(Math.max(start.getTime(), lastStart.getTime()) + 3 * 3600e3);
  const fmt = (d: Date) => d.toISOString().replace(/[-:]|\.\d{3}/g, "");
  const params = new URLSearchParams({
    action: "TEMPLATE", text: `${data.eventLabel ?? "Pernikahan"} ${coupleLabel(data)}`, dates: `${fmt(start)}/${fmt(end)}`,
    location: [data.place, data.address].filter(Boolean).join(", "),
  });
  return `https://calendar.google.com/calendar/render?${params.toString()}`;
}

export default function MelayuSongketTheme({ data, slug, guestToken, demo, skipCover }: ThemeProps) {
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
  const [first, ...rest] = data.gallery;
  const calendar = calendarHref(data);
  const table = tableLabel(data.guestTable);
  const quote = data.extras?.quote && data.extras.quote.enabled !== false && data.extras.quote.text ? data.extras.quote : QUOTE;
  const families = [father(data.couple.brideParents), father(data.couple.groomParents)].filter(Boolean).join(" & ");
  const initials = `${data.couple.bride.slice(0, 1)}${data.couple.groom ? ` ${data.couple.groom.slice(0, 1)}` : ""}`.toUpperCase();
  const sentRef = useRef<HTMLDivElement>(null);
  useEffect(() => { if (wishes.status === "sent") celebrate(sentRef.current); }, [wishes.status]);

  const people = [
    { role: "Pengantin Perempuan", name: data.couple.brideFull || data.couple.bride, short: data.couple.bride, parents: data.couple.brideParents, photo: data.couple.bridePhoto },
    { role: "Pengantin Laki-laki", name: data.couple.groomFull || data.couple.groom, short: data.couple.groom, parents: data.couple.groomParents, photo: data.couple.groomPhoto },
  ].filter(person => person.name);

  return (
    <ThemeShell
      fonts={FONTS}
      background="#062a1e"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.field} aria-hidden />
          <div className={`${s.band} ${s.bandTop}`} aria-hidden />
          <div className={`${s.band} ${s.bandBottom}`} aria-hidden />
          <p className={s.kicker}>Undangan Pernikahan</p>
          <Medallion className={s.coverMedal} eager />
          <h1 className={s.coverNames}>
            <span>{data.couple.bride}</span>
            {data.couple.groom && <><em>dengan</em><span>{data.couple.groom}</span></>}
          </h1>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.guest}>
            <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
            <strong>{guestLabel(data)}</strong>
            {table && <span className={s.table}>{table}</span>}
          </div>
          <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} />Buka Undangan</button>
        </section>
      )}
    >
      <main className={s.main}>
        <header className={s.opening}>
          <div className={s.field} aria-hidden />
          <div className={`${s.band} ${s.bandBottom}`} aria-hidden />
          <p className={s.kicker}>Walimatul &lsquo;Urs</p>
          <Medallion className={s.openMedal} initials={initials} />
          <h1>{couple}</h1>
          <p className={s.openDate}>{parts.day ? `${parts.weekday}, ${parts.day} ${parts.month} ${parts.year}` : DATE_TBA}</p>
        </header>

        <section className={s.salam} aria-labelledby="ml-salam">
          <h2 id="ml-salam" className={s.salamTitle}>Assalamu&rsquo;alaikum Warahmatullahi Wabarakatuh</h2>
          <div className={s.pantun} aria-label="Pantun pembuka">
            {PANTUN_OPEN.map(line => <p key={line}>{line}</p>)}
          </div>
          <p className={s.salamText}>Dengan segala hormat dan takzim, kami mengundang Bapak/Ibu, Datuk, Encik, dan Puan serta sanak saudara sekalian ke majelis {label.toLowerCase()} putera-puteri kami.</p>
          <figure className={s.quote}>
            <blockquote>&ldquo;{quote.text}&rdquo;</blockquote>
            {quote.source && <figcaption>{quote.source}</figcaption>}
          </figure>
        </section>

        <Extras slot="opening" without={["quote"]} />

        <section className={`${s.section} ${s.couple}`} aria-labelledby="ml-couple">
          <Head id="ml-couple" kicker="Raja Sehari" title="Kedua Mempelai" />
          <div className={people.length > 1 ? s.pair : `${s.pair} ${s.single}`}>
            {people.map(person => (
              <article key={person.role} className={s.person}>
                <div className={s.gerbang}>
                  <div className={s.gerbangIn}>
                    {person.photo ? <Photo src={person.photo} alt={person.name} /> : <span className={s.mono} aria-hidden>{person.short.slice(0, 1)}</span>}
                  </div>
                </div>
                <small className={s.role}>{person.role}</small>
                <h3>{person.name}</h3>
                {person.parents && <p>{person.parents}</p>}
              </article>
            ))}
          </div>
        </section>

        <section className={`${s.section} ${s.dark}`} aria-labelledby="ml-count">
          <div className={s.field} aria-hidden />
          <div className={`${s.band} ${s.bandTop}`} aria-hidden />
          <Head id="ml-count" kicker="Menanti Hari Baik" title="Hitung Mundur" light />
          {countdown.valid ? (
            <div className={s.count} role="timer" aria-label={`${countdown.days} hari ${countdown.hours} jam ${countdown.minutes} menit lagi`}>
              {[[countdown.days, "Hari"], [countdown.hours, "Jam"], [countdown.minutes, "Menit"], [countdown.seconds, "Detik"]].map(([value, unit]) => (
                <div key={unit}><b><Tick value={value} /></b><small>{unit}</small></div>
              ))}
            </div>
          ) : <p className={s.countTba}>{DATE_TBA}</p>}
          {calendar && <a className={s.ghostBtn} href={calendar} target="_blank" rel="noreferrer"><Lucide icon={ic.calendarPlus} size={15} />Simpan ke Kalender</a>}
        </section>

        <section className={s.section} aria-labelledby="ml-events">
          <Head id="ml-events" kicker="Susunan Acara" title="Rangkaian Acara" />
          {data.events.map((event, index) => {
            const maps = mapsHref(data, event);
            return (
              <article key={event.name + index} className={s.event}>
                <header className={s.kepala}><Rebung className={s.kepalaIcon} /><h3>{event.name}</h3><Rebung className={s.kepalaIcon} /></header>
                <div className={s.eventBody}>
                  <p className={s.eventDate}>{formatDate(event.date || data.date)}</p>
                  {event.time && <p className={s.eventTime}><Lucide icon={ic.calendarPlus} size={14} />{event.time}</p>}
                  {event.venue && <strong>{event.venue}</strong>}
                  {event.address && <p className={s.eventAddr}>{event.address}</p>}
                  {maps && <a className={s.mapBtn} href={maps} target="_blank" rel="noreferrer"><Lucide icon={ic.mapPin} size={14} />Lihat Peta</a>}
                </div>
              </article>
            );
          })}
        </section>

        <Extras slot="event" without={["calendar"]} />

        {stories.length > 0 && (
          <section className={`${s.section} ${s.story}`} aria-labelledby="ml-story">
            <Head id="ml-story" kicker="Dari Merisik ke Pelaminan" title="Kisah Kasih" />
            <ol className={s.timeline}>
              {stories.map((story, index) => (
                <li key={index}>
                  <span className={s.mark} aria-hidden><Rebung className={s.markIcon} /><b>{story.date ?? index + 1}</b></span>
                  <div className={s.storyText}>
                    <h3>{story.title}</h3>
                    {story.body && <p>{story.body}</p>}
                    {story.image && <Photo src={story.image} alt={story.title} className={s.storyImg} />}
                  </div>
                </li>
              ))}
            </ol>
          </section>
        )}

        {first && (
          <section className={`${s.section} ${s.gallery}`} aria-labelledby="ml-gallery">
            <Head id="ml-gallery" kicker="Kenangan" title="Galeri" />
            <div className={s.grid}>
              <div className={`${s.shot} ${s.shotWide}`}><Photo src={first} alt="Foto galeri 1" /></div>
              {rest.map((src, index) => <div key={src + index} className={s.shot}><Photo src={src} alt={`Foto galeri ${index + 2}`} /></div>)}
            </div>
          </section>
        )}

        <Extras slot="story" />

        <Extras slot="end" />

        {data.gifts.length > 0 && (
          <section className={`${s.section} ${s.gifts}`} aria-labelledby="ml-gift">
            <Head id="ml-gift" kicker="Tanda Kasih" title="Hadiah & Amplop" />
            <p className={s.intro}>Kehadiran dan doa restu sudah menjadi hadiah terindah. Bagi yang ingin memberi tanda kasih:</p>
            {data.gifts.map(gift => {
              const info = giftInfo(gift);
              const on = Boolean(info.copy) && copied === info.copy;
              const icon = gift.type === "bank" ? ic.landmark : gift.type === "address" ? ic.gift : gift.type === "qris" ? ic.qrCode : ic.wallet;
              const title = gift.type === "bank" ? (/^bank/i.test(info.title) ? info.title : `Bank ${info.title}`) : info.title;
              return (
                <div key={gift.id} className={on ? `${s.gift} ${s.giftOn}` : s.gift}>
                  <span className={s.giftIcon}><Lucide icon={icon} size={20} /></span>
                  <div>
                    <h3>{title}</h3>
                    {info.number && <strong>{info.number}</strong>}
                    {info.holder && <small>a.n. {info.holder}</small>}
                    {info.image && <Photo src={info.image} alt="Kode QRIS" className={s.qris} />}
                  </div>
                  {info.copy && (
                    <button type="button" className={on ? `${s.copy} ${s.copyOn}` : s.copy} onClick={() => copy(info.copy)} aria-label={on ? "Tersalin" : `Salin ${title}`}>
                      <Lucide key={on ? "on" : "off"} icon={on ? ic.check : ic.copy} size={14} />
                      <span>{on ? "Tersalin" : "Salin"}</span>
                    </button>
                  )}
                </div>
              );
            })}
          </section>
        )}

        <section className={`${s.section} ${s.wishes}`} aria-labelledby="ml-wishes">
          <Head id="ml-wishes" kicker={rsvpClosed ? "Doa Restu" : "Sudi Kiranya Hadir"} title="Ucapan & Kehadiran" />
          {wishes.status === "sent" ? (
            <div ref={sentRef} className={`${s.form} ${s.sentBox}`} role="status">
              <Rebung className={s.sentIcon} />
              <p className={s.sent}>Terima kasih, ucapan &amp; doa Anda sudah terkirim.</p>
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
              <label className={s.fieldRow}><span>Nama</span><input name="name" required maxLength={100} defaultValue={plainName(data.guestName)} placeholder="Nama Anda" autoComplete="name" /></label>
              <label className={s.fieldRow}><span>Ucapan &amp; doa</span><textarea name="message" required maxLength={500} rows={3} placeholder="Tuliskan ucapan dan doa restu…" /></label>
              {rsvpClosed ? (
                <div className={s.closed} role="status"><strong>Konfirmasi kehadiran sudah ditutup</strong><p>Terima kasih atas doa dan perhatiannya. Ucapan &amp; doa masih bisa dikirim lewat form ini.</p></div>
              ) : (
                <div className={s.choices} role="radiogroup" aria-label="Kehadiran">
                  {(["yes", "maybe", "no"] as Attendance[]).map(value => (
                    <button key={value} type="button" role="radio" aria-checked={attendance === value} className={attendance === value ? s.choiceOn : undefined} onClick={() => setAttendance(value)}>{ATTEND[value]}</button>
                  ))}
                </div>
              )}
              {!rsvpClosed && attendance !== "no" && <GuestCount label="Jumlah tamu" className={s.guests} labelClassName={s.fieldLabel} buttonClassName={s.step} />}
              {!rsvpClosed && attendance !== "no" && <DietaryField className={`${s.fieldRow} ${s.diet}`} />}
              {wishes.status === "error" && <p className={s.error} role="alert">Belum terkirim. Coba lagi sebentar lagi.</p>}
              <button type="submit" className={s.submit} disabled={wishes.status === "sending"}>{wishes.status === "sending" ? "Mengirim…" : "Kirim Ucapan"}</button>
            </form>
          )}
          {wishes.wishes.length === 0 && <p className={s.empty}>Belum ada ucapan. Jadilah yang pertama mendoakan.</p>}
          <div className={s.wishList}>
            {wishes.wishes.slice(0, 10).map(wish => (
              <article key={wish.id} className={s.wish}>
                <div><strong>{wish.name}</strong>{wish.attendance && <small>{ATTEND[wish.attendance]}</small>}</div>
                <p>{wish.message}</p>
              </article>
            ))}
          </div>
        </section>

        <footer className={s.closing}>
          <div className={s.field} aria-hidden />
          <div className={`${s.band} ${s.bandTop}`} aria-hidden />
          <Medallion className={s.closeMedal} />
          <p className={s.thanks}>Terima Kasih</p>
          <div className={`${s.pantun} ${s.pantunLight}`} aria-label="Pantun penutup">
            {PANTUN_CLOSE.map(line => <p key={line}>{line}</p>)}
          </div>
          <p className={s.wassalam}>Wassalamu&rsquo;alaikum Warahmatullahi Wabarakatuh</p>
          <p className={s.family}>Kami yang berbahagia,<br />Keluarga Besar {families || couple}</p>
          <a href="/" target="_blank" rel="noreferrer" className={s.made}>dibuat dengan ♥ di Rawuh</a>
        </footer>
      </main>

      {music.visible && !music.failed && (
        <button type="button" className={music.playing ? `${s.music} ${s.musicOn}` : s.music} onClick={music.toggle} aria-pressed={music.playing} {...music.attrs} aria-label={music.playing ? "Matikan musik" : "Putar musik"}>
          <Lucide icon={ic.music} size={18} />
        </button>
      )}
    </ThemeShell>
  );
}
