"use client";
// Theme "Bugis Bosara" — adat Bugis-Makassar: warna baju bodo, lipa' sabbe kotak-kotak, bosara, dan walasuji.
import { useEffect, useRef, useState } from "react";
import {
  DATE_TBA, DietaryField, Extras, GuestCount, Lucide, Photo, ThemeShell, Tick, coupleLabel, dateParts, formatDate, giftInfo, guestLabel,
  mapsHref, storyItems, toDate, useCopy, useCountdown, useMusic, useRsvp, useThankYou, useWishes, type Attendance, type ThemeProps,
} from "../kit";
import { tableLabel } from "../extras";
import type { InvitationData } from "../../types";
import { celebrate } from "@/lib/celebrate";
import { ic } from "./icons";
import { bosaraBase, bosaraDefs, bosaraLid, divider, jewel } from "./ornaments";
import s from "./styles.module.css";

const FONTS = ["Playfair Display:ital,wght@0,400;0,600;1,400;1,600", "Jost:wght@400;500;600"];
const DEMO_WISHES = [
  { id: "w1", name: "Andi Nurul Fadhilah", attendance: "yes" as Attendance, message: "Selamat Tenri & Fadli! Semoga menjadi keluarga sakinah, mawaddah, warahmah, dan selalu dalam lindungan Allah SWT." },
  { id: "w2", name: "Kak Ilham & Kak Rahma", attendance: "maybe" as Attendance, message: "Barakallahu lakuma. Semoga langgeng sampai tua, rezekinya lancar terus." },
];
const ATTEND: Record<Attendance, string> = { yes: "Hadir", maybe: "Insyaallah", no: "Berhalangan" };

const Svg = ({ html, box, className }: { html: string; box: string; className?: string }) => (
  <svg className={className} viewBox={box} aria-hidden="true" focusable="false" dangerouslySetInnerHTML={{ __html: html }} />
);

function Bosara({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 160 170" aria-hidden="true" focusable="false">
      <defs dangerouslySetInnerHTML={{ __html: bosaraDefs }} />
      <g dangerouslySetInnerHTML={{ __html: bosaraBase }} />
      <g className={s.lid} dangerouslySetInnerHTML={{ __html: bosaraLid }} />
    </svg>
  );
}

function Head({ id, kicker, title }: { id: string; kicker?: string; title: string }) {
  return (
    <div className={s.head}>
      {kicker && <p className={s.eyebrow}>{kicker}</p>}
      <h2 id={id}>{title}</h2>
      <Svg html={divider} box="0 0 160 24" className={s.divider} />
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
  const end = new Date(start.getTime() + 3 * 3600e3);
  const fmt = (d: Date) => d.toISOString().replace(/[-:]|\.\d{3}/g, "");
  const params = new URLSearchParams({
    action: "TEMPLATE", text: `${data.eventLabel ?? "Pernikahan"} ${coupleLabel(data)}`, dates: `${fmt(start)}/${fmt(end)}`,
    location: [data.place, data.address].filter(Boolean).join(", "),
  });
  return `https://calendar.google.com/calendar/render?${params.toString()}`;
}

export default function BugisBosaraTheme({ data, slug, guestToken, demo, skipCover }: ThemeProps) {
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
    { role: "Mempelai Wanita", nick: data.couple.bride, name: data.couple.brideFull ?? data.couple.bride, parents: data.couple.brideParents, photo: data.couple.bridePhoto },
    { role: "Mempelai Pria", nick: data.couple.groom, name: data.couple.groomFull ?? data.couple.groom, parents: data.couple.groomParents, photo: data.couple.groomPhoto },
  ];

  return (
    <ThemeShell
      fonts={FONTS}
      background="#5c0b2d"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.sheen} aria-hidden />
          <div className={s.panel}>
            <div className={s.panelInner}>
              <Bosara className={s.bosara} />
              <p className={s.salam}>Tabe&apos;</p>
              <p className={s.kicker}>Undangan {label}</p>
              <h1 className={s.coverNames}><span>{data.couple.bride}</span><em>&amp;</em><span>{data.couple.groom}</span></h1>
              <Svg html={divider} box="0 0 160 24" className={s.divider} />
              <p className={s.coverDate}>{formatDate(data.date)}</p>
              <div className={s.guest}>
                <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
                <strong>{guestLabel(data)}</strong>
                {table && <span className={s.table}>{table}</span>}
              </div>
            </div>
          </div>
          <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#7d0f3d" />Buka Undangan</button>
        </section>
      )}
    >
      <main className={s.main}>
        <header className={s.hero}>
          <div className={s.sheen} aria-hidden />
          <div className={s.heroFrame}><Photo src={hero} alt={`Foto ${couple}`} /></div>
          <p className={s.heroKicker}>The Wedding of</p>
          <h1 className={s.heroNames}>{data.couple.bride} <em>&amp;</em> {data.couple.groom}</h1>
          <p className={s.heroDate}>{parts.day ? `${parts.weekday}, ${parts.day} ${parts.month} ${parts.year}` : DATE_TBA}</p>
        </header>

        <section className={s.salamBlock} aria-label="Salam pembuka">
          <p className={s.arabic} lang="ar" dir="rtl">بِسْمِ اللّٰهِ الرَّحْمٰنِ الرَّحِيْمِ</p>
          <p className={s.salamTitle}>Tabe&apos;</p>
          <p className={s.salamSub}>Assalamu&apos;alaikum Warahmatullahi Wabarakatuh</p>
          <p className={s.intro}>Dengan memohon rahmat dan ridha Allah SWT, kami bermaksud menyelenggarakan {label.toLowerCase()} putra-putri kami. Merupakan kehormatan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.</p>
        </section>

        <Extras slot="opening" />

        <section className={`${s.section} ${s.couple}`} aria-labelledby="bg-couple">
          <Head id="bg-couple" kicker="Sulapa Eppa" title="Kedua Mempelai" />
          {people.map((person, index) => (
            <div key={person.role} className={s.personWrap}>
              {index === 1 && <p className={s.amp} aria-hidden>&amp;</p>}
              <article className={s.person}>
                <div className={s.ring}>
                  {person.photo ? <Photo src={person.photo} alt={person.name} /> : <span className={s.monogram} aria-hidden>{person.nick.slice(0, 1)}</span>}
                </div>
                <p className={s.role}>{person.role}</p>
                <h3>{person.name}</h3>
                {person.parents && <p className={s.parents}>{person.parents}</p>}
              </article>
            </div>
          ))}
        </section>

        <section className={`${s.section} ${s.countBand}`} aria-labelledby="bg-count">
          <div className={s.sheen} aria-hidden />
          <Head id="bg-count" kicker="Hari Baik" title="Menghitung Hari" />
          {countdown.valid ? (
            <div className={s.count} role="timer" aria-label={`${countdown.days} hari ${countdown.hours} jam ${countdown.minutes} menit lagi`}>
              {[[countdown.days, "Hari"], [countdown.hours, "Jam"], [countdown.minutes, "Menit"], [countdown.seconds, "Detik"]].map(([value, unit]) => (
                <div key={unit}><b><Tick value={value} /></b><small>{unit}</small></div>
              ))}
            </div>
          ) : <p className={s.countTba}>{DATE_TBA}</p>}
          {calendar && <a className={s.ghostBtn} href={calendar} target="_blank" rel="noreferrer"><Lucide icon={ic.calendarPlus} size={15} color="#f7dc8c" />Simpan ke Kalender</a>}
        </section>

        <section className={`${s.section} ${s.events}`} aria-labelledby="bg-events">
          <Head id="bg-events" kicker="Rangkaian Adat" title="Acara Pernikahan" />
          {data.events.map((event, index) => {
            const maps = mapsHref(data, event);
            return (
              <article key={event.name + index} className={s.event}>
                <div className={s.eventBand}><h3>{event.name}</h3><Svg html={jewel} box="0 0 24 24" /></div>
                <p className={s.meta}><Lucide icon={ic.calendarPlus} size={15} color="#c2185b" /><span>{formatDate(event.date || data.date)}</span></p>
                {event.time && <p className={s.meta}><Lucide icon={ic.clock} size={15} color="#c2185b" /><span>{event.time}</span></p>}
                {(event.venue || event.address) && (
                  <div className={s.venue}>
                    {event.venue && <strong>{event.venue}</strong>}
                    {event.address && <p>{event.address}</p>}
                  </div>
                )}
                {maps && <a className={s.mapBtn} href={maps} target="_blank" rel="noreferrer"><Lucide icon={ic.mapPin} size={14} color="#fff8ef" />Lihat Lokasi</a>}
              </article>
            );
          })}
        </section>

        <Extras slot="event" without={["calendar"]} />

        {stories.length > 0 && (
          <section className={`${s.section} ${s.story}`} aria-labelledby="bg-story">
            <Head id="bg-story" kicker="Perjalanan" title="Kisah Kami" />
            <ol className={s.timeline}>
              {stories.map((story, index) => (
                <li key={index}>
                  <Svg html={jewel} box="0 0 24 24" className={s.node} />
                  {story.date && <small>{story.date}</small>}
                  <h3>{story.title}</h3>
                  {story.body && <p>{story.body}</p>}
                  {story.image && <Photo src={story.image} alt={story.title} className={s.storyImg} />}
                </li>
              ))}
            </ol>
          </section>
        )}

        <Extras slot="story" />

        {data.gallery.length > 0 && (
          <section className={`${s.section} ${s.gallery}`} aria-labelledby="bg-gallery">
            <Head id="bg-gallery" kicker="Galeri" title="Momen Kami" />
            <div className={s.grid}>
              {gallery.map((src, index) => <Photo key={src + index} src={src} alt={`Foto galeri ${index + 1}`} className={s.shot} />)}
            </div>
          </section>
        )}

        <section className={`${s.section} ${s.wishes}`} aria-labelledby="bg-wishes">
          <Head id="bg-wishes" kicker="Doa Restu" title="Ucapan & Kehadiran" />
          {wishes.status === "sent" ? (
            <div ref={sentRef} className={`${s.form} ${s.sentBox}`} role="status">
              <Bosara className={s.sentIcon} />
              <p className={s.sent}>Terima kasih — doa dan ucapan Anda sudah terkirim.</p>
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
              <label className={s.field}><span>Ucapan &amp; Doa</span><textarea name="message" required maxLength={500} rows={3} placeholder="Tuliskan doa restu untuk kedua mempelai…" /></label>
              {rsvpClosed ? <div className={s.closed} role="status"><strong>Konfirmasi kehadiran sudah ditutup</strong><p>Terima kasih atas doa dan perhatiannya. Ucapan masih bisa dikirim lewat form ini.</p></div> : (
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

        {data.gifts.length > 0 && (
          <section className={`${s.section} ${s.gifts}`} aria-labelledby="bg-gift">
            <Head id="bg-gift" kicker="Passolo'" title="Tanda Kasih" />
            <p className={s.intro}>Doa restu Anda adalah hadiah terindah. Bagi yang ingin menitipkan passolo&apos; atau tanda kasih, dapat melalui:</p>
            {data.gifts.map(gift => {
              const info = giftInfo(gift);
              const isCopied = !!info.copy && copied === info.copy;
              const title = gift.type === "bank" ? (/^bank/i.test(info.title) ? info.title : `Bank ${info.title}`) : gift.type === "address" ? "Kirim Kado" : info.title;
              const icon = gift.type === "bank" ? ic.landmark : gift.type === "address" ? ic.gift : gift.type === "qris" ? ic.qrCode : ic.wallet;
              return (
                <div key={gift.id} className={isCopied ? `${s.gift} ${s.giftCopied}` : s.gift}>
                  <span className={s.giftIcon}><Lucide icon={icon} size={20} color="#fff8ef" /></span>
                  <h3>{title}</h3>
                  {info.number && <strong className={s.giftNo}>{info.number}</strong>}
                  {info.holder && <small>a.n. {info.holder}</small>}
                  {info.image && <Photo src={info.image} alt="Kode QRIS" className={s.qris} />}
                  {info.copy && (
                    <button type="button" className={isCopied ? `${s.copy} ${s.copyOn}` : s.copy} onClick={() => copy(info.copy)}>
                      <Lucide key={isCopied ? "on" : "off"} icon={isCopied ? ic.check : ic.copy} size={14} color={isCopied ? "#ffffff" : "#c2185b"} />
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
          <div className={s.sheen} aria-hidden />
          <Bosara className={s.closingBosara} />
          <p className={s.thanks}>Kurru&apos; Sumange&apos;</p>
          <p className={s.thanksSub}>Terima Kasih</p>
          <p className={s.closingText}>Merupakan kebahagiaan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu kepada kedua mempelai.</p>
          <p className={s.family}>Kami yang berbahagia<br />Keluarga Besar {families || couple}</p>
          <a href="/" target="_blank" rel="noreferrer" className={s.made}>dibuat dengan ♥ di Rawuh</a>
        </footer>
      </main>

      {music.visible && !music.failed && (
        <button type="button" className={music.playing ? `${s.music} ${s.musicOn}` : s.music} onClick={music.toggle} aria-pressed={music.playing} aria-label={music.playing ? "Matikan musik" : "Putar musik"}>
          <Lucide icon={ic.music} size={18} color="#f7dc8c" />
        </button>
      )}
    </ThemeShell>
  );
}
