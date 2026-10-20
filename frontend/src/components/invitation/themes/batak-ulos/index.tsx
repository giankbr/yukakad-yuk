"use client";
// Theme "Batak Ulos" — adat Batak Toba: gorga tiga warna (merah-putih-hitam), kain ulos berumbai, Rumah Bolon.
import { useEffect, useRef, useState } from "react";
import {
  DATE_TBA, DietaryField, Extras, GuestCount, Lucide, Photo, ThemeShell, Tick, coupleLabel, dateParts, formatDate, giftInfo, guestLabel,
  mapsHref, storyItems, toDate, useCopy, useCountdown, useMusic, useRsvp, useThankYou, useWishes, type Attendance, type ThemeProps,
} from "../kit";
import { tableLabel } from "../extras";
import type { InvitationData } from "../../types";
import { celebrate } from "@/lib/celebrate";
import { ic } from "./icons";
import s from "./styles.module.css";

const FONTS = ["DM Serif Display", "Josefin Sans:wght@400;600;700", "Lora:ital,wght@0,400;0,500;0,600;1,400"];
const DEMO_WISHES = [
  { id: "w1", name: "Inang Uda Lumbantobing", attendance: "yes" as Attendance, message: "Horas! Selamat Rotua & Daniel. Semoga diberkati hagabeon, hamoraon, dan hasangapon. Tuhan Yesus memberkati rumah tangga kalian." },
  { id: "w2", name: "Naposobulung HKBP", attendance: "yes" as Attendance, message: "Selamat menempuh hidup baru, kakak & abang! Kami tunggu di pesta, siap manortor." },
];
const ATTEND: Record<Attendance, string> = { yes: "Hadir", maybe: "Belum pasti", no: "Berhalangan" };

// Linocut-printed ornaments (rendered by /tmp/pen/art/themes/batak-ulos.py); woven ulos/gorga tiles live in the CSS.
const ART = { "spiral-red": [88, 67], "lozenge": [410, 411], "spiral-bone": [88, 69], "rumah-bolon": [440, 298] } as const;
const Art = ({ name, className, eager }: { name: keyof typeof ART; className?: string; eager?: boolean }) => (
  // eslint-disable-next-line @next/next/no-img-element -- decorative printed ornament, static asset
  <img src={`/themes/art/batak-ulos/${name}.webp`} alt="" aria-hidden width={ART[name][0]} height={ART[name][1]} className={className} data-nolightbox draggable={false}
    loading={eager ? "eager" : "lazy"} fetchPriority={eager ? "high" : undefined} decoding="async" />
);

function Head({ id, kicker, title }: { id: string; kicker?: string; title: string }) {
  return (
    <div className={s.head}>
      {kicker && <p className={s.eyebrow}>{kicker}</p>}
      <h2 id={id}>{title}</h2>
      <span className={s.headRule} aria-hidden><Art name="spiral-red" /></span>
    </div>
  );
}

/** "Bapak St. Jonggi Simanjuntak & Ibu …" → "Simanjuntak" (the marga, for "Keluarga Besar …"). */
function marga(parents?: string) {
  const match = /(?:Bapak|Bpk\.?|Amang)\s+([^&\n]+?)\s*(?:&|\n|$)/i.exec(parents ?? "");
  const words = match?.[1].trim().split(/\s+/) ?? [];
  return words.length > 1 ? words[words.length - 1] : words[0];
}

function plainName(guest?: string) {
  if (!guest || guest === "Tamu Undangan") return "";
  return guest.replace(/^(bapak|ibu|bpk\.?|sdr\.?|saudara|saudari|amang|inang)\s+/i, "").replace(/\s*(&|dan)\s*keluarga$/i, "").trim();
}

function calendarHref(data: InvitationData) {
  const start = toDate(data.date) ?? toDate(data.events[0]?.date);
  if (!start) return undefined;
  const end = new Date(start.getTime() + 6 * 3600e3);
  const fmt = (d: Date) => d.toISOString().replace(/[-:]|\.\d{3}/g, "");
  const params = new URLSearchParams({
    action: "TEMPLATE", text: `${data.eventLabel ?? "Pernikahan"} ${coupleLabel(data)}`, dates: `${fmt(start)}/${fmt(end)}`,
    location: [data.place, data.address].filter(Boolean).join(", "),
  });
  return `https://calendar.google.com/calendar/render?${params.toString()}`;
}

export default function BatakUlosTheme({ data, slug, guestToken, demo, skipCover }: ThemeProps) {
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
  const families = [marga(data.couple.brideParents), marga(data.couple.groomParents)].filter(Boolean).join(" & ");
  const sentRef = useRef<HTMLDivElement>(null);
  useEffect(() => { if (wishes.status === "sent") celebrate(sentRef.current); }, [wishes.status]);
  const people = [
    { role: "Boru", nick: data.couple.bride, name: data.couple.brideFull ?? data.couple.bride, parents: data.couple.brideParents, photo: data.couple.bridePhoto },
    { role: "Anak", nick: data.couple.groom, name: data.couple.groomFull ?? data.couple.groom, parents: data.couple.groomParents, photo: data.couple.groomPhoto },
  ];

  return (
    <ThemeShell
      fonts={FONTS}
      background="#15100e"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Art name="rumah-bolon" eager className={s.house} />
          <p className={s.horas}>Horas!</p>
          <p className={s.kicker}>Undangan {label} Adat Batak</p>
          <h1 className={s.coverNames}><span>{data.couple.bride}</span><em>dohot</em><span>{data.couple.groom}</span></h1>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <span className={`${s.ulos} ${s.coverUlos}`} aria-hidden />
          <div className={s.guest}>
            <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
            <strong>{guestLabel(data)}</strong>
            {table && <span className={s.table}>{table}</span>}
          </div>
          <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#f4efe6" />Buka Undangan</button>
        </section>
      )}
    >
      <main className={s.main}>
        <header className={s.hero}>
          <Photo src={hero} alt={`Foto ${couple}`} className={s.heroImg} />
          <div className={s.heroText}>
            <p className={s.eyebrow}>Pesta Unjuk · {label}</p>
            <h1 className={s.heroNames}>{data.couple.bride} <em>&amp;</em> {data.couple.groom}</h1>
            <p className={s.heroDate}>{parts.day ? `${parts.weekday}, ${parts.day} ${parts.month} ${parts.year}` : DATE_TBA}</p>
          </div>
          <span className={`${s.gorga} ${s.gorgaWeave} ${s.heroGorga}`} aria-hidden />
        </header>

        <section className={s.opening} aria-label="Salam pembuka">
          <p className={s.openingHoras}>Horas! Syalom</p>
          <p className={s.openingTitle}>Dalihan Na Tolu</p>
          <p className={s.intro}>Dengan penuh sukacita dan atas berkat Tuhan Yang Maha Kasih, kami keluarga besar mengundang Bapak/Ibu/Saudara/i untuk hadir dan memberi doa restu pada {label.toLowerCase()} putra-putri kami.</p>
          <span className={s.tolu} aria-hidden><i /><i /><i /></span>
        </section>

        <Extras slot="opening" />

        <section className={`${s.section} ${s.couple}`} aria-labelledby="bt-couple">
          <Head id="bt-couple" kicker="Na Marhasohotan" title="Kedua Mempelai" />
          {people.map((person, index) => (
            <div key={person.role} className={s.personWrap}>
              {index === 1 && <p className={s.amp} aria-hidden>&amp;</p>}
              <article className={s.person}>
                <div className={s.diamond}>
                  <Art name="lozenge" />
                  {person.photo
                    ? <div className={s.diamondPhoto}><Photo src={person.photo} alt={person.name} /></div>
                    : <span className={s.initial} aria-hidden>{person.nick.slice(0, 1)}</span>}
                </div>
                <p className={s.role}>{person.role}</p>
                <h3>{person.name}</h3>
                {person.parents && <p className={s.parents}>{person.parents}</p>}
              </article>
            </div>
          ))}
        </section>

        <section className={`${s.section} ${s.dark} ${s.countSection}`} aria-labelledby="bt-count">
          <span className={`${s.gorga} ${s.gorgaWeave}`} aria-hidden />
          <Head id="bt-count" kicker="Tinggal Sebentar Lagi" title="Menuju Hari Pemberkatan" />
          {countdown.valid ? (
            <div className={s.count} role="timer" aria-label={`${countdown.days} hari ${countdown.hours} jam ${countdown.minutes} menit lagi`}>
              {[[countdown.days, "Hari"], [countdown.hours, "Jam"], [countdown.minutes, "Menit"], [countdown.seconds, "Detik"]].map(([value, unit]) => (
                <div key={unit}><b><Tick value={value} /></b><small>{unit}</small></div>
              ))}
            </div>
          ) : <p className={s.countTba}>{DATE_TBA}</p>}
          {calendar && <a className={s.ghostBtn} href={calendar} target="_blank" rel="noreferrer"><Lucide icon={ic.calendarPlus} size={15} color="#f4efe6" />Simpan ke Kalender</a>}
        </section>

        <section className={`${s.section} ${s.events}`} aria-labelledby="bt-events">
          <Head id="bt-events" kicker="Ulaon" title="Rangkaian Acara" />
          {data.events.map((event, index) => {
            const maps = mapsHref(data, event);
            return (
              <article key={event.name + index} className={s.event}>
                <span className={s.eventUlos} aria-hidden />
                <div className={s.eventBody}>
                  <span className={s.eventNo}>Acara {index + 1}</span>
                  <h3>{event.name}</h3>
                  <p className={s.meta}><Lucide icon={ic.calendarPlus} size={15} color="#b3261e" /><span>{formatDate(event.date || data.date)}</span></p>
                  {event.time && <p className={s.meta}><Lucide icon={ic.clock} size={15} color="#b3261e" /><span>{event.time}</span></p>}
                  {(event.venue || event.address) && (
                    <div className={s.venue}>
                      {event.venue && <strong>{event.venue}</strong>}
                      {event.address && <p>{event.address}</p>}
                    </div>
                  )}
                  {maps && <a className={s.mapBtn} href={maps} target="_blank" rel="noreferrer"><Lucide icon={ic.mapPin} size={14} color="#f4efe6" />Buka Peta</a>}
                </div>
              </article>
            );
          })}
        </section>

        <Extras slot="event" without={["calendar"]} />

        {stories.length > 0 && (
          <section className={`${s.section} ${s.story}`} aria-labelledby="bt-story">
            <Head id="bt-story" kicker="Turi-turian" title="Kisah Kami" />
            <ol className={s.timeline}>
              {stories.map((story, index) => (
                <li key={index}>
                  <span className={s.rail} aria-hidden><span><Art name="spiral-bone" /></span><i /></span>
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
          <section className={`${s.section} ${s.gallery}`} aria-labelledby="bt-gallery">
            <Head id="bt-gallery" kicker="Galeri" title="Momen Kami" />
            <div className={s.strip}>
              {gallery.map((src, index) => <Photo key={src + index} src={src} alt={`Foto galeri ${index + 1}`} className={s.shot} />)}
            </div>
          </section>
        )}

        <section className={`${s.section} ${s.wishes}`} aria-labelledby="bt-wishes">
          <Head id="bt-wishes" kicker="Pasu-pasu" title="Doa & Konfirmasi" />
          {wishes.status === "sent" ? (
            <div ref={sentRef} className={`${s.form} ${s.sentBox}`} role="status">
              <span className={s.sentMark} aria-hidden><Art name="spiral-bone" /></span>
              <p className={s.sent}>Mauliate godang — doa dan ucapan Anda sudah terkirim.</p>
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
              <label className={s.field}><span>Doa &amp; Ucapan</span><textarea name="message" required maxLength={500} rows={3} placeholder="Tuliskan doa dan pasu-pasu untuk kedua mempelai…" /></label>
              {rsvpClosed ? <div className={s.closed} role="status"><strong>Konfirmasi kehadiran sudah ditutup</strong><p>Mauliate atas doa dan perhatiannya. Ucapan masih bisa dikirim lewat form ini.</p></div> : (
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
          {wishes.wishes.length === 0 && <p className={s.empty}>Belum ada ucapan. Jadilah yang pertama memberi pasu-pasu.</p>}
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
          <section className={`${s.section} ${s.dark} ${s.gifts}`} aria-labelledby="bt-gift">
            <Head id="bt-gift" kicker="Tumpak" title="Tanda Kasih" />
            <p className={`${s.intro} ${s.introLight}`}>Kehadiran dan doa Anda adalah berkat bagi kami. Bagi yang ingin mengirimkan tumpak atau tanda kasih:</p>
            {data.gifts.map(gift => {
              const info = giftInfo(gift);
              const isCopied = !!info.copy && copied === info.copy;
              const title = gift.type === "bank" ? (/^bank/i.test(info.title) ? info.title : `Bank ${info.title}`) : gift.type === "address" ? "Kirim Kado" : info.title;
              const icon = gift.type === "bank" ? ic.landmark : gift.type === "address" ? ic.gift : gift.type === "qris" ? ic.qrCode : ic.wallet;
              return (
                <div key={gift.id} className={isCopied ? `${s.gift} ${s.giftCopied}` : s.gift}>
                  <div className={s.giftTop}><Lucide icon={icon} size={18} color="#b3261e" /><h3>{title}</h3></div>
                  {info.number && <strong className={s.giftNo}>{info.number}</strong>}
                  {info.holder && <small>a.n. {info.holder}</small>}
                  {info.image && <Photo src={info.image} alt="Kode QRIS" className={s.qris} />}
                  {info.copy && (
                    <button type="button" className={isCopied ? `${s.copy} ${s.copyOn}` : s.copy} onClick={() => copy(info.copy)}>
                      <Lucide key={isCopied ? "on" : "off"} icon={isCopied ? ic.check : ic.copy} size={14} color="#f4efe6" />
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
          <span className={`${s.gorga} ${s.gorgaWeave}`} aria-hidden />
          <Art name="rumah-bolon" className={s.closingHouse} />
          <p className={s.thanks}>Mauliate Godang</p>
          <p className={s.closingText}>Atas kehadiran, doa, dan pasu-pasu Bapak/Ibu/Saudara/i, kami mengucapkan terima kasih yang sebesar-besarnya.</p>
          <p className={s.closingHoras}>Horas! Horas! Horas!</p>
          <p className={s.family}>Kami yang berbahagia<br />Keluarga Besar {families || couple}</p>
          <a href="/" target="_blank" rel="noreferrer" className={s.made}>dibuat dengan ♥ di Rawuh</a>
        </footer>
      </main>

      {music.visible && !music.failed && (
        <button type="button" className={music.playing ? `${s.music} ${s.musicOn}` : s.music} onClick={music.toggle} aria-pressed={music.playing} aria-label={music.playing ? "Matikan musik" : "Putar musik"}>
          <Lucide icon={ic.music} size={18} color="#f4efe6" />
        </button>
      )}
    </ThemeShell>
  );
}
