"use client";
// Theme "Betawi Ondel" — adat Betawi yang meriah: ondel-ondel, kembang kelapa, lisplang gigi balang, dan pantun.
import { useEffect, useRef, useState } from "react";
import {
  DATE_TBA, DietaryField, Extras, GuestCount, Lucide, Photo, ThemeShell, Tick, coupleLabel, dateParts, formatDate, giftInfo, guestLabel,
  mapsHref, storyItems, toDate, useCopy, useCountdown, useMusic, useRsvp, useThankYou, useWishes, type Attendance, type ThemeProps,
} from "../kit";
import { tableLabel } from "../extras";
import type { InvitationData } from "../../types";
import { celebrate } from "@/lib/celebrate";
import { ic } from "./icons";
import { burst, kembangPot, ondelFemale, ondelMale, rosette } from "./ornaments";
import s from "./styles.module.css";

const FONTS = ["Bebas Neue", "Plus Jakarta Sans:ital,wght@0,400;0,600;0,700;0,800;1,400", "Great Vibes"];
const DEMO_WISHES = [
  { id: "w1", name: "Mpok Hasanah", attendance: "yes" as Attendance, message: "Selamet ye Aini & Rizky! Moga jadi keluarga sakinah, rezekinya ngalir terus, cepet dapet momongan. Aamiin." },
  { id: "w2", name: "Bang Udin Sanggar Silat", attendance: "yes" as Attendance, message: "Siap jaga palang pintu! Barakallah, moga langgeng ampe kakek-nenek." },
];
const ATTEND: Record<Attendance, string> = { yes: "Dateng", maybe: "Insyaallah", no: "Kagak bisa" };

const Svg = ({ html, box, className }: { html: string; box: string; className?: string }) => (
  <svg className={className} viewBox={box} aria-hidden="true" focusable="false" dangerouslySetInnerHTML={{ __html: html }} />
);
const Balang = ({ up }: { up?: boolean }) => <span className={up ? `${s.balang} ${s.balangUp}` : s.balang} aria-hidden />;

function Head({ id, kicker, title }: { id: string; kicker?: string; title: string }) {
  return (
    <div className={s.head}>
      {kicker && <p className={s.eyebrow}>{kicker}</p>}
      <h2 id={id}>{title}</h2>
      <span className={s.headRule} aria-hidden><i /><i /><i /><i /></span>
    </div>
  );
}

function father(parents?: string) {
  const match = /(?:Bapak|Bpk\.?)\s+([^&\n]+?)\s*(?:&|\n|$)/i.exec(parents ?? "");
  return match?.[1].trim();
}

function plainName(guest?: string) {
  if (!guest || guest === "Tamu Undangan") return "";
  return guest.replace(/^(bapak|ibu|bpk\.?|sdr\.?|saudara|saudari|bang|mpok)\s+/i, "").replace(/\s*(&|dan)\s*keluarga$/i, "").trim();
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

export default function BetawiOndelTheme({ data, slug, guestToken, demo, skipCover }: ThemeProps) {
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
  const hero = data.gallery[0];
  const gallery = data.gallery.length > 1 ? data.gallery.slice(1) : data.gallery;
  const calendar = calendarHref(data);
  const table = tableLabel(data.guestTable);
  const families = [father(data.couple.brideParents), father(data.couple.groomParents)].filter(Boolean).join(" & ");
  const sentRef = useRef<HTMLDivElement>(null);
  useEffect(() => { if (wishes.status === "sent") celebrate(sentRef.current); }, [wishes.status]);
  const people = [
    { role: "None", nick: data.couple.bride, name: data.couple.brideFull ?? data.couple.bride, parents: data.couple.brideParents, photo: data.couple.bridePhoto },
    { role: "Abang", nick: data.couple.groom, name: data.couple.groomFull ?? data.couple.groom, parents: data.couple.groomParents, photo: data.couple.groomPhoto },
  ];

  return (
    <ThemeShell
      fonts={FONTS}
      background="#9e1820"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Balang />
          <div className={s.coverTop}>
            <p className={s.kicker}>Undangan {label}</p>
            <p className={s.coverSalam}>Assalamu&apos;alaikum, nyok pade dateng!</p>
            <h1 className={s.coverNames}><span>{data.couple.bride}</span><em>&amp;</em><span>{data.couple.groom}</span></h1>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
          </div>
          <div className={s.stage} aria-hidden>
            <Svg html={ondelMale} box="0 0 120 250" className={s.ondel} />
            <Svg html={kembangPot} box="0 0 120 130" className={s.pot} />
            <Svg html={ondelFemale} box="0 0 120 250" className={s.ondel} />
          </div>
          <div className={s.guest}>
            <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
            <strong>{guestLabel(data)}</strong>
            {table && <span className={s.table}>{table}</span>}
          </div>
          <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={18} color="#fffaf0" />Buka Undangan</button>
        </section>
      )}
    >
      <main className={s.main}>
        <header className={s.hero}>
          <Balang />
          <div className={s.heroPhoto}>
            <Photo src={hero} alt={`Foto ${couple}`} />
            {parts.day && <span className={s.heroTag}><span><b>{parts.day}</b>{parts.monthShort} {parts.year}</span></span>}
          </div>
          <p className={s.heroKicker}>Kawinan</p>
          <h1 className={s.heroNames}>{data.couple.bride} <em>&amp;</em> {data.couple.groom}</h1>
          <p className={s.heroDate}>{parts.day ? `${parts.weekday}, ${parts.day} ${parts.month} ${parts.year}` : DATE_TBA}</p>
        </header>

        <section className={s.salamBlock} aria-label="Salam pembuka">
          <p className={s.arabic} lang="ar" dir="rtl">بِسْمِ اللّٰهِ الرَّحْمٰنِ الرَّحِيْمِ</p>
          <p className={s.salamTitle}>Assalamu&apos;alaikum Wr. Wb.</p>
          <div className={s.pantun}>
            <p>Jalan-jalan ke Kota Tua,<br />jangan lupa mampir ke Setu Babakan.<br />Dateng ye ke hari bahagia kite berdua,<br />doa restu abang none kami harapkan.</p>
          </div>
          <p className={s.intro}>Dengan memohon rahmat dan ridha Allah SWT, kami bermaksud menyelenggarakan {label.toLowerCase()} putra-putri kami. Kehadiran Bapak/Ibu/Saudara/i menjadi kebahagiaan bagi kami sekeluarga.</p>
        </section>

        <Extras slot="opening" />

        <section className={`${s.section} ${s.couple}`} aria-labelledby="bw-couple">
          <Head id="bw-couple" kicker="Abang & None" title="Kedua Mempelai" />
          {people.map((person, index) => (
            <div key={person.role} className={s.personWrap}>
              {index === 1 && <p className={s.amp} aria-hidden>&amp;</p>}
              <article className={s.person}>
                <div className={s.medal}>
                  <Svg html={burst} box="0 0 120 120" />
                  <div className={s.medalFace}>{person.photo ? <Photo src={person.photo} alt={person.name} /> : <span aria-hidden>{person.nick.slice(0, 1)}</span>}</div>
                </div>
                <p className={s.role}>{person.role}</p>
                <h3 className={s.nick}>{person.nick}</h3>
                <p className={s.fullName}>{person.name}</p>
                {person.parents && <p className={s.parents}>{person.parents}</p>}
              </article>
            </div>
          ))}
        </section>

        <section className={`${s.section} ${s.countBand}`} aria-labelledby="bw-count">
          <Balang />
          <Head id="bw-count" kicker="Itung Hari" title="Kagak Lama Lagi" />
          {countdown.valid ? (
            <div className={s.count} role="timer" aria-label={`${countdown.days} hari ${countdown.hours} jam ${countdown.minutes} menit lagi`}>
              {[[countdown.days, "Hari"], [countdown.hours, "Jam"], [countdown.minutes, "Menit"], [countdown.seconds, "Detik"]].map(([value, unit]) => (
                <div key={unit}><b><Tick value={value} /></b><small>{unit}</small></div>
              ))}
            </div>
          ) : <p className={s.countTba}>{DATE_TBA}</p>}
          {calendar && <a className={s.ghostBtn} href={calendar} target="_blank" rel="noreferrer"><Lucide icon={ic.calendarPlus} size={15} color="#2a1a14" />Simpan ke Kalender</a>}
        </section>

        <section className={`${s.section} ${s.events}`} aria-labelledby="bw-events">
          <Head id="bw-events" kicker="Rangkaian Acara" title="Hari Bahagia" />
          {data.events.map((event, index) => {
            const maps = mapsHref(data, event);
            return (
              <article key={event.name + index} className={s.event}>
                <div className={s.eventHead}><span className={s.eventNo} aria-hidden>{index + 1}</span><h3>{event.name}</h3></div>
                <Balang />
                <p className={s.meta}><Lucide icon={ic.calendarPlus} size={15} color="#d1262f" /><span>{formatDate(event.date || data.date)}</span></p>
                {event.time && <p className={s.meta}><Lucide icon={ic.clock} size={15} color="#d1262f" /><span>{event.time}</span></p>}
                {(event.venue || event.address) && (
                  <div className={s.venue}>
                    {event.venue && <strong>{event.venue}</strong>}
                    {event.address && <p>{event.address}</p>}
                  </div>
                )}
                {maps && <a className={s.mapBtn} href={maps} target="_blank" rel="noreferrer"><Lucide icon={ic.mapPin} size={14} color="#fffaf0" />Liat Peta</a>}
              </article>
            );
          })}
        </section>

        <Extras slot="event" without={["calendar"]} />

        {stories.length > 0 && (
          <section className={`${s.section} ${s.story}`} aria-labelledby="bw-story">
            <Head id="bw-story" kicker="Cerite Kite" title="Kisah Kami" />
            <ol className={s.timeline}>
              {stories.map((story, index) => (
                <li key={index}>
                  <span className={s.rail} aria-hidden><Svg html={rosette} box="0 0 24 24" /><i /></span>
                  <div className={s.storyBody}>
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

        <Extras slot="story" />

        {data.gallery.length > 0 && (
          <section className={`${s.section} ${s.gallery}`} aria-labelledby="bw-gallery">
            <Head id="bw-gallery" kicker="Galeri" title="Potret Kite" />
            <div className={s.polaroids}>
              {gallery.map((src, index) => <div key={src + index} className={s.polaroid}><Photo src={src} alt={`Foto galeri ${index + 1}`} /></div>)}
            </div>
          </section>
        )}

        <section className={`${s.section} ${s.wishes}`} aria-labelledby="bw-wishes">
          <Head id="bw-wishes" kicker="Doa & Kehadiran" title="Kirim Ucapan" />
          {wishes.status === "sent" ? (
            <div ref={sentRef} className={`${s.form} ${s.sentBox}`} role="status">
              <Svg html={kembangPot} box="0 0 120 130" className={`${s.pot} ${s.sentIcon}`} />
              <p className={s.sent}>Makasih banyak ye! Ucapan ente udah terkirim.</p>
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
              <label className={s.field}><span>Ucapan &amp; Doa</span><textarea name="message" required maxLength={500} rows={3} placeholder="Tulis doa restu buat abang & none…" /></label>
              {rsvpClosed ? <div className={s.closed} role="status"><strong>Konfirmasi kehadiran sudah ditutup</strong><p>Makasih atas doa dan perhatiannya. Ucapan masih bisa dikirim lewat form ini.</p></div> : (
                <div className={s.choices} role="radiogroup" aria-label="Kehadiran">
                  {(["yes", "maybe", "no"] as Attendance[]).map(value => (
                    <button key={value} type="button" role="radio" aria-checked={attendance === value} className={attendance === value ? s.choiceOn : undefined} onClick={() => setAttendance(value)}>{ATTEND[value]}</button>
                  ))}
                </div>
              )}
              {!rsvpClosed && attendance !== "no" && <GuestCount label="Jumlah tamu" className={s.guests} labelClassName={s.guestsLabel} buttonClassName={s.step} />}
              {!rsvpClosed && attendance !== "no" && <DietaryField className={`${s.field} ${s.diet}`} />}
              {wishes.status === "error" && <p className={s.error} role="alert">Belum terkirim. Coba lagi sebentar lagi.</p>}
              <button type="submit" className={s.submit} disabled={wishes.status === "sending"}>{wishes.status === "sending" ? "Mengirim…" : "Kirim Ucapan"}</button>
            </form>
          )}
          {wishes.wishes.length === 0 && <p className={s.empty}>Belum ada ucapan. Jadi yang pertama, nyok!</p>}
          <div className={s.wishList}>
            {wishes.wishes.slice(0, 10).map(wish => (
              <article key={wish.id} className={s.wish}>
                <div><strong>{wish.name}</strong>{wish.attendance && <small>{ATTEND[wish.attendance]}</small>}</div>
                <p>{wish.message}</p>
              </article>
            ))}
          </div>
        </section>

        {data.gifts.length > 0 && (
          <section className={`${s.section} ${s.gifts}`} aria-labelledby="bw-gift">
            <Head id="bw-gift" kicker="Amplop Digital" title="Tanda Kasih" />
            <p className={s.intro}>Doa restu Anda sudah lebih dari cukup. Kalau mau ngasih tanda kasih, bisa lewat:</p>
            {data.gifts.map(gift => {
              const info = giftInfo(gift);
              const isCopied = !!info.copy && copied === info.copy;
              const title = gift.type === "bank" ? (/^bank/i.test(info.title) ? info.title : `Bank ${info.title}`) : gift.type === "address" ? "Kirim Kado" : info.title;
              const icon = gift.type === "bank" ? ic.landmark : gift.type === "address" ? ic.gift : gift.type === "qris" ? ic.qrCode : ic.wallet;
              return (
                <div key={gift.id} className={isCopied ? `${s.gift} ${s.giftCopied}` : s.gift}>
                  <div className={s.giftTop}><span><Lucide icon={icon} size={18} color="#2a1a14" /></span><h3>{title}</h3></div>
                  {info.number && <strong className={s.giftNo}>{info.number}</strong>}
                  {info.holder && <small>a.n. {info.holder}</small>}
                  {info.image && <Photo src={info.image} alt="Kode QRIS" className={s.qris} />}
                  {info.copy && (
                    <button type="button" className={isCopied ? `${s.copy} ${s.copyOn}` : s.copy} onClick={() => copy(info.copy)}>
                      <Lucide key={isCopied ? "on" : "off"} icon={isCopied ? ic.check : ic.copy} size={14} color="#2a1a14" />
                      {isCopied ? "Tersalin" : gift.type === "address" ? "Salin Alamat" : "Salin Nomor"}
                    </button>
                  )}
                </div>
              );
            })}
          </section>
        )}

        <Extras slot="end" />

        <footer className={s.closing}>
          <Balang />
          <div className={s.closingStage} aria-hidden>
            <Svg html={ondelMale} box="0 0 120 250" className={s.ondel} />
            <Svg html={kembangPot} box="0 0 120 130" className={s.pot} />
            <Svg html={ondelFemale} box="0 0 120 250" className={s.ondel} />
          </div>
          <p className={s.thanks}>Makasih Banyak Ye!</p>
          <p className={s.closingText}>Atas kehadiran dan doa restu Bapak/Ibu/Saudara/i, kami sekeluarga mengucapkan terima kasih.</p>
          <p className={s.family}>Keluarga Besar<br />{families || couple}</p>
          <p className={s.closingNames}>{couple}</p>
          <a href="/" target="_blank" rel="noreferrer" className={s.made}>dibuat dengan ♥ di Rawuh</a>
        </footer>
      </main>

      {music.visible && !music.failed && (
        <button type="button" className={music.playing ? `${s.music} ${s.musicOn}` : s.music} onClick={music.toggle} aria-pressed={music.playing} aria-label={music.playing ? "Matikan musik" : "Putar musik"}>
          <Lucide icon={ic.music} size={18} color="#2a1a14" />
        </button>
      )}
    </ThemeShell>
  );
}
