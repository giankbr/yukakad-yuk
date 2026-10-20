"use client";
// Theme "Sunda Siger" — adat Sunda hijau zamrud & emas: siger, roncean melati, dan awan Mega Mendung.
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

const FONTS = ["Marcellus", "EB Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500", "Pinyon Script"];
const DEMO_WISHES = [
  { id: "w1", name: "Euis Komalasari", attendance: "yes" as Attendance, message: "Wilujeng nikah, Neng Sekar & Kang Rangga. Mugia janten kulawarga sakinah, mawaddah, warahmah. Aamiin." },
  { id: "w2", name: "Kang Dadan & Teh Lilis", attendance: "yes" as Attendance, message: "Selamat menempuh hidup baru. Semoga langgeng sampai kakek-nenek, rukun salawasna." },
];
const ATTEND: Record<Attendance, string> = { yes: "Hadir", maybe: "Insyaallah", no: "Berhalangan" };

// Hand-painted raster ornaments (rendered by /tmp/pen/art/themes/sunda-siger.py): foil siger, gouache Mega Mendung, melati.
const ART = {
  siger: [400, 291], "cloud-dark": [542, 232], "cloud-light": [541, 229], ronce: [44, 531], melati: [96, 97], divider: [320, 44],
} as const;
const Art = ({ name, className, eager }: { name: keyof typeof ART; className?: string; eager?: boolean }) => (
  // eslint-disable-next-line @next/next/no-img-element -- decorative painted ornament, static asset
  <img src={`/themes/art/sunda-siger/${name}.webp`} alt="" aria-hidden width={ART[name][0]} height={ART[name][1]} className={className} data-nolightbox draggable={false}
    loading={eager ? "eager" : "lazy"} fetchPriority={eager ? "high" : undefined} decoding="async" />
);
const Divider = () => <Art name="divider" className={s.divider} />;

function Head({ id, kicker, title }: { id: string; kicker?: string; title: string }) {
  return (
    <div className={s.head}>
      {kicker && <p className={s.eyebrow}>{kicker}</p>}
      <h2 id={id}>{title}</h2>
      <Divider />
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
  const start = toDate(data.events[0]?.date ?? data.date);
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

export default function SundaSigerTheme({ data, slug, guestToken, demo, skipCover }: ThemeProps) {
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
    { role: "Mempelai Istri", nick: data.couple.bride, name: data.couple.brideFull ?? data.couple.bride, parents: data.couple.brideParents, photo: data.couple.bridePhoto },
    { role: "Mempelai Pria", nick: data.couple.groom, name: data.couple.groomFull ?? data.couple.groom, parents: data.couple.groomParents, photo: data.couple.groomPhoto },
  ];

  return (
    <ThemeShell
      fonts={FONTS}
      background="#0f2a1e"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.coverClouds} aria-hidden>
            <Art name="cloud-dark" eager className={`${s.cloud} ${s.cloudA}`} />
            <Art name="cloud-dark" className={`${s.cloud} ${s.cloudB}`} />
            <Art name="cloud-dark" className={`${s.cloud} ${s.cloudC}`} />
          </div>
          <div className={s.strands} aria-hidden>
            <Art name="ronce" eager className={s.strand} />
            <Art name="ronce" eager className={s.strand} />
          </div>
          <div className={s.coverFrame} aria-hidden />
          <Art name="siger" eager className={s.coverSiger} />
          <div className={s.coverText}>
            <p className={s.salam}>Sampurasun</p>
            <p className={s.kicker}>Undangan {label}</p>
            <h1 className={s.coverNames}><span>{data.couple.bride}</span><em>&amp;</em><span>{data.couple.groom}</span></h1>
            <Divider />
            <p className={s.coverDate}>{formatDate(data.date)}</p>
          </div>
          <div className={s.guest}>
            <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
            <strong>{guestLabel(data)}</strong>
            {table && <span className={s.table}>{table}</span>}
          </div>
          <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#123323" />Buka Undangan</button>
        </section>
      )}
    >
      <main className={s.main}>
        <header className={s.hero}>
          <Art name="cloud-light" className={s.heroCloud} />
          <div className={s.heroArch}>
            <Art name="siger" className={s.heroSiger} />
            <div className={s.heroPhoto}><Photo src={hero} alt={`Foto ${couple}`} /></div>
          </div>
          <p className={s.kickerDark}>The Wedding of</p>
          <h1 className={s.heroNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
          <p className={s.heroDate}>{parts.day ? `${parts.weekday}, ${parts.day} ${parts.month} ${parts.year}` : DATE_TBA}</p>
        </header>

        <section className={s.salamBlock} aria-label="Salam pembuka">
          <p className={s.arabic} lang="ar" dir="rtl">بِسْمِ اللّٰهِ الرَّحْمٰنِ الرَّحِيْمِ</p>
          <p className={s.salamTitle}>Sampurasun</p>
          <p className={s.salamSub}>Assalamu&apos;alaikum Warahmatullahi Wabarakatuh</p>
          <p className={s.intro}>Dengan memohon rahmat dan ridha Allah SWT, kami bermaksud menyelenggarakan {label.toLowerCase()} putra-putri kami. Merupakan kehormatan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.</p>
        </section>

        <Extras slot="opening" />

        <section className={`${s.section} ${s.couple}`} aria-labelledby="sg-couple">
          <Head id="sg-couple" kicker="Duaan Jadi Hiji" title="Mempelai" />
          {people.map((person, index) => (
            <div key={person.role} className={s.personWrap}>
              {index === 1 && <div className={s.amp} aria-hidden><Art name="melati" className={s.ampBloom} /><span>&amp;</span><Art name="melati" className={s.ampBloom} /></div>}
              <article className={s.person}>
                <div className={s.portrait}>
                  <Art name="ronce" className={s.portraitStrand} />
                  <div className={s.portraitFrame}>
                    {person.photo ? <Photo src={person.photo} alt={person.name} /> : <span className={s.monogram} aria-hidden>{person.nick.slice(0, 1)}</span>}
                  </div>
                </div>
                <p className={s.role}>{person.role}</p>
                <h3 className={s.nick}>{person.nick}</h3>
                <p className={s.fullName}>{person.name}</p>
                {person.parents && <p className={s.parents}>{person.parents}</p>}
              </article>
            </div>
          ))}
        </section>

        <section className={`${s.section} ${s.countBand}`} aria-labelledby="sg-count">
          <Art name="cloud-dark" className={s.bandCloudL} />
          <Art name="cloud-dark" className={s.bandCloudR} />
          <div className={s.headLight}><p className={s.eyebrow}>Ngitung Poé</p><h2 id="sg-count">Menuju Hari Bahagia</h2></div>
          {countdown.valid ? (
            <div className={s.count} role="timer" aria-label={`${countdown.days} hari ${countdown.hours} jam ${countdown.minutes} menit lagi`}>
              {[[countdown.days, "Poé"], [countdown.hours, "Jam"], [countdown.minutes, "Menit"], [countdown.seconds, "Detik"]].map(([value, unit]) => (
                <div key={unit}><b><Tick value={value} /></b><small>{unit}</small></div>
              ))}
            </div>
          ) : <p className={s.countTba}>{DATE_TBA}</p>}
          {calendar && <a className={s.ghostBtn} href={calendar} target="_blank" rel="noreferrer"><Lucide icon={ic.calendarPlus} size={15} color="#e8cf8a" />Simpan ke Kalender</a>}
        </section>

        <section className={`${s.section} ${s.events}`} aria-labelledby="sg-events">
          <Head id="sg-events" kicker="Runtuyan Acara" title="Rangkaian Upacara" />
          {data.events.map((event, index) => {
            const maps = mapsHref(data, event);
            return (
              <article key={event.name + index} className={s.event}>
                <span className={s.eventNo} aria-hidden>{String(index + 1).padStart(2, "0")}</span>
                <h3>{event.name}</h3>
                <p className={s.eventDate}>{formatDate(event.date || data.date)}</p>
                {event.time && <p className={s.eventTime}><Lucide icon={ic.clock} size={14} color="#9a7a2c" />{event.time}</p>}
                <span className={s.rule} aria-hidden />
                {event.venue && <strong>{event.venue}</strong>}
                {event.address && <p className={s.eventAddr}>{event.address}</p>}
                {maps && <a className={s.mapBtn} href={maps} target="_blank" rel="noreferrer"><Lucide icon={ic.mapPin} size={14} color="#f7f2e4" />Petunjuk Lokasi</a>}
              </article>
            );
          })}
        </section>

        <Extras slot="event" without={["calendar"]} />

        {stories.length > 0 && (
          <section className={`${s.section} ${s.story}`} aria-labelledby="sg-story">
            <Head id="sg-story" kicker="Carita Urang" title="Kisah Kami" />
            <ol className={s.timeline}>
              {stories.map((story, index) => (
                <li key={index}>
                  <span className={s.node} aria-hidden><Art name="melati" /></span>
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
          <section className={`${s.section} ${s.gallery}`} aria-labelledby="sg-gallery">
            <Head id="sg-gallery" kicker="Galeri" title="Momen Bahagia" />
            <div className={s.mosaic}>
              {gallery.map((src, index) => <Photo key={src + index} src={src} alt={`Foto galeri ${index + 1}`} className={s.tile} />)}
            </div>
          </section>
        )}

        <section className={`${s.section} ${s.wishes}`} aria-labelledby="sg-wishes">
          <Head id="sg-wishes" kicker="Du'a & Kahadiran" title="Ucapan & Konfirmasi" />
          {wishes.status === "sent" ? (
            <div ref={sentRef} className={`${s.form} ${s.sentBox}`} role="status">
              <Art name="melati" className={s.sentBloom} />
              <p className={s.sent}>Hatur nuhun — doa dan ucapan Anda sudah terkirim.</p>
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
              <label className={s.field}><span>Ucapan &amp; Du&apos;a</span><textarea name="message" required maxLength={500} rows={3} placeholder="Tuliskan doa restu untuk kedua mempelai…" /></label>
              {rsvpClosed ? <div className={s.closed} role="status"><strong>Konfirmasi kehadiran sudah ditutup</strong><p>Hatur nuhun atas doa dan perhatiannya. Ucapan masih bisa dikirim lewat form ini.</p></div> : (
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
          <section className={`${s.section} ${s.gifts}`} aria-labelledby="sg-gift">
            <Head id="sg-gift" kicker="Tanda Kaasih" title="Amplop Digital" />
            <p className={s.intro}>Doa restu Anda adalah kado terindah bagi kami. Jika berkenan memberi tanda kasih, dapat melalui:</p>
            {data.gifts.map(gift => {
              const info = giftInfo(gift);
              const isCopied = !!info.copy && copied === info.copy;
              const title = gift.type === "bank" ? (/^bank/i.test(info.title) ? info.title : `Bank ${info.title}`) : gift.type === "address" ? "Kirim Kado" : info.title;
              const icon = gift.type === "bank" ? ic.landmark : gift.type === "address" ? ic.gift : gift.type === "qris" ? ic.qrCode : ic.wallet;
              return (
                <div key={gift.id} className={isCopied ? `${s.gift} ${s.giftCopied}` : s.gift}>
                  <div className={s.giftTop}>
                    <span className={s.giftIcon}><Lucide icon={icon} size={18} color="#e8cf8a" /></span>
                    <h3>{title}</h3>
                  </div>
                  {info.number && <strong className={s.giftNo}>{info.number}</strong>}
                  {info.holder && <small>a.n. {info.holder}</small>}
                  {info.image && <Photo src={info.image} alt="Kode QRIS" className={s.qris} />}
                  {info.copy && (
                    <button type="button" className={isCopied ? `${s.copy} ${s.copyOn}` : s.copy} onClick={() => copy(info.copy)}>
                      <Lucide key={isCopied ? "on" : "off"} icon={isCopied ? ic.check : ic.copy} size={14} color={isCopied ? "#123323" : "#e8cf8a"} />
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
          <Art name="cloud-dark" className={s.closingCloud} />
          <Art name="siger" className={s.closingSiger} />
          <p className={s.thanks}>Hatur Nuhun</p>
          <p className={s.closingText}>Kehadiran dan doa restu Bapak/Ibu/Saudara/i merupakan kebahagiaan yang tak ternilai bagi kami sekeluarga.</p>
          <p className={s.closingSalam}>Wassalamu&apos;alaikum Warahmatullahi Wabarakatuh</p>
          <p className={s.family}>Keluarga Besar<br />{families || couple}</p>
          <p className={s.closingNames}>{couple}</p>
          <a href="/" target="_blank" rel="noreferrer" className={s.made}>dibuat dengan ♥ di Rawuh</a>
        </footer>
      </main>

      {music.visible && !music.failed && (
        <button type="button" className={music.playing ? `${s.music} ${s.musicOn}` : s.music} onClick={music.toggle} aria-pressed={music.playing} aria-label={music.playing ? "Matikan musik" : "Putar musik"}>
          <Lucide icon={ic.music} size={18} color="#e8cf8a" />
        </button>
      )}
    </ThemeShell>
  );
}
