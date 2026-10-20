"use client";
// Theme "Palembang Aesan" — adat Palembang merah-emas: mahkota bergaya karsuhun aesan gede dengan kembang goyang,
// bidang songket limar, dan bingkai bertingkat (kekijing) ala rumah limas. Ornamen digambar sendiri untuk Rawuh.
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
import { Corner, Crown, Limar } from "./ornaments";
import s from "./styles.module.css";

const FONTS = ["Playfair Display:ital,wght@0,400;0,500;0,600;0,700;1,400;1,500;1,600", "Cormorant Garamond:ital,wght@0,400;0,500;0,600;0,700;1,400;1,500"];
const ATTEND: Record<Attendance, string> = { yes: "Hadir", maybe: "Ragu", no: "Berhalangan" };
const DEMO_WISHES: Wish[] = [
  { id: "w1", name: "Nyimas Fitri", attendance: "yes", message: "Selamat ya Ayu dan Rizky! Semoga jadi keluarga sakinah, mawaddah, warahmah. Dak sabar nak liat kalian di pelaminan." },
  { id: "w2", name: "Mang Udin & Bik Ani", attendance: "yes", message: "Barakallahu lakuma wa baraka 'alaikuma. Semoga rukun sampai tuo." },
];
const QUOTE = { text: "Dan di antara tanda-tanda kekuasaan-Nya ialah Dia menciptakan untukmu pasangan dari jenismu sendiri, supaya kamu merasa tenteram kepadanya, dan dijadikan-Nya di antaramu rasa kasih dan sayang.", source: "QS. Ar-Rum: 21" };

function Divider({ light }: { light?: boolean }) {
  return <span className={light ? `${s.divider} ${s.dividerLight}` : s.divider} aria-hidden><i /><Limar className={s.limar} /><i /></span>;
}

function Head({ id, kicker, title, light }: { id: string; kicker?: string; title: string; light?: boolean }) {
  return (
    <div className={light ? `${s.head} ${s.headLight}` : s.head}>
      {kicker && <p className={s.kicker}>{kicker}</p>}
      <h2 id={id}>{title}</h2>
      <Divider light={light} />
    </div>
  );
}

/** "Putri pertama dari\nBapak Kemas H. Abdullah & Ibu ..." → "Kemas H. Abdullah" */
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

export default function PalembangAesanTheme({ data, slug, guestToken, demo, skipCover }: ThemeProps) {
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
  const coverPhoto = data.gallery[1] ?? hero;
  const calendar = calendarHref(data);
  const table = tableLabel(data.guestTable);
  const quote = data.extras?.quote && data.extras.quote.enabled !== false && data.extras.quote.text ? data.extras.quote : QUOTE;
  const families = [father(data.couple.brideParents), father(data.couple.groomParents)].filter(Boolean).join(" & ");
  const sentRef = useRef<HTMLDivElement>(null);
  useEffect(() => { if (wishes.status === "sent") celebrate(sentRef.current); }, [wishes.status]);

  const people = [
    { role: "Mempelai Wanita", name: data.couple.brideFull || data.couple.bride, short: data.couple.bride, parents: data.couple.brideParents, photo: data.couple.bridePhoto },
    { role: "Mempelai Pria", name: data.couple.groomFull || data.couple.groom, short: data.couple.groom, parents: data.couple.groomParents, photo: data.couple.groomPhoto },
  ].filter(person => person.name);

  return (
    <ThemeShell
      fonts={FONTS}
      background="#2a0508"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.coverPattern} aria-hidden />
          <div className={s.coverFrame} aria-hidden><Corner className={s.cTL} /><Corner className={s.cTR} /><Corner className={s.cBL} /><Corner className={s.cBR} /></div>
          {coverPhoto ? <>
            <Crown className={s.coverCrown} eager />
            <div className={s.coverPhoto}><Photo src={coverPhoto} alt="" /></div>
          </> : <Crown className={s.coverCrownSolo} eager />}
          <p className={s.kicker}>Walimatul &lsquo;Ursy</p>
          <h1 className={s.coverNames}>
            <span>{data.couple.bride}</span>
            {data.couple.groom && <><em>&amp;</em><span>{data.couple.groom}</span></>}
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
        <header className={hero ? s.opening : `${s.opening} ${s.openingPlain}`}>
          {hero ? <Photo src={hero} alt={`Foto ${couple}`} className={s.openingImg} /> : <div className={s.darkPattern} aria-hidden />}
          <div className={s.openingText}>
            <Crown className={s.openingCrown} />
            <p className={s.kicker}>{label}</p>
            <h1>{couple}</h1>
            <p className={s.openingDate}>{parts.day ? `${parts.weekday}, ${parts.day} ${parts.month} ${parts.year}` : DATE_TBA}</p>
          </div>
        </header>

        <section className={s.salam} aria-labelledby="pl-salam">
          <p className={s.arabic} lang="ar" dir="rtl">بِسْمِ اللّٰهِ الرَّحْمٰنِ الرَّحِيْمِ</p>
          <h2 id="pl-salam" className={s.salamTitle}>Assalamu&rsquo;alaikum Warahmatullahi Wabarakatuh</h2>
          <p className={s.salamText}>Dengan memohon rahmat dan ridho Allah SWT, kami bermaksud menyelenggarakan {label.toLowerCase()} putra-putri kami dalam balutan adat Palembang Darussalam.</p>
          <figure className={s.quote}>
            <blockquote>&ldquo;{quote.text}&rdquo;</blockquote>
            {quote.source && <figcaption>{quote.source}</figcaption>}
          </figure>
        </section>

        <Extras slot="opening" without={["quote"]} />

        <section className={`${s.section} ${s.couple}`} aria-labelledby="pl-couple">
          <Head id="pl-couple" kicker="Pasangan Pengantin" title="Mempelai" />
          {people.map((person, index) => (
            <div key={person.role} className={s.personWrap}>
              {index === 1 && <p className={s.amp} aria-hidden>&amp;</p>}
              <article className={s.person}>
                <div className={s.kijing}>
                  <div className={s.kijingIn}>
                    {person.photo ? <Photo src={person.photo} alt={person.name} /> : <span className={s.mono} aria-hidden>{person.short.slice(0, 1)}</span>}
                  </div>
                </div>
                <small className={s.role}>{person.role}</small>
                <h3>{person.name}</h3>
                {person.parents && <p>{person.parents}</p>}
              </article>
            </div>
          ))}
        </section>

        <section className={`${s.section} ${s.dark}`} aria-labelledby="pl-count">
          <div className={s.darkPattern} aria-hidden />
          <Head id="pl-count" kicker="Menuju Hari Bahagia" title="Hitung Mundur" light />
          {countdown.valid ? (
            <div className={s.count} role="timer" aria-label={`${countdown.days} hari ${countdown.hours} jam ${countdown.minutes} menit lagi`}>
              {[[countdown.days, "Hari"], [countdown.hours, "Jam"], [countdown.minutes, "Menit"], [countdown.seconds, "Detik"]].map(([value, unit]) => (
                <div key={unit}><b><Tick value={value} /></b><small>{unit}</small></div>
              ))}
            </div>
          ) : <p className={s.countTba}>{DATE_TBA}</p>}
          {calendar && <a className={s.ghostBtn} href={calendar} target="_blank" rel="noreferrer"><Lucide icon={ic.calendarPlus} size={15} />Simpan ke Kalender</a>}
        </section>

        <section className={s.section} aria-labelledby="pl-events">
          <Head id="pl-events" kicker="Waktu & Tempat" title="Rangkaian Acara" />
          {data.events.map((event, index) => {
            const maps = mapsHref(data, event);
            const p = dateParts(event.date || data.date);
            return (
              <article key={event.name + index} className={s.event}>
                <div className={s.eventIn}>
                  <div className={s.eventDate}>
                    {p.day ? <><small>{p.weekday}</small><b>{p.day}</b><small>{p.monthShort} {p.year}</small></> : <small>{DATE_TBA}</small>}
                  </div>
                  <div className={s.eventBody}>
                    <h3>{event.name}</h3>
                    {event.time && <p className={s.eventMeta}>{event.time}</p>}
                    {event.venue && <strong>{event.venue}</strong>}
                    {event.address && <p>{event.address}</p>}
                    {maps && <a className={s.mapBtn} href={maps} target="_blank" rel="noreferrer"><Lucide icon={ic.mapPin} size={14} />Petunjuk Lokasi</a>}
                  </div>
                </div>
              </article>
            );
          })}
        </section>

        <Extras slot="event" without={["calendar"]} />

        {stories.length > 0 && (
          <section className={`${s.section} ${s.story}`} aria-labelledby="pl-story">
            <Head id="pl-story" kicker="Dari Madik hingga Munggah" title="Kisah Kami" />
            <ol className={s.timeline}>
              {stories.map((story, index) => (
                <li key={index}>
                  <span className={s.node} aria-hidden><Limar className={s.nodeIcon} tone="red" /></span>
                  <div className={s.storyText}>
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

        {data.gallery.length > 0 && (
          <section className={`${s.section} ${s.dark} ${s.gallery}`} aria-labelledby="pl-gallery">
            <div className={s.darkPattern} aria-hidden />
            <Head id="pl-gallery" kicker="Album" title="Galeri" light />
            <div className={s.grid}>
              {data.gallery.map((src, index) => (
                <div key={src + index} className={index === 0 ? `${s.frame} ${s.frameWide}` : s.frame}><Photo src={src} alt={`Foto galeri ${index + 1}`} /></div>
              ))}
            </div>
          </section>
        )}

        <Extras slot="story" />

        <Extras slot="end" />

        {data.gifts.length > 0 && (
          <section className={s.section} aria-labelledby="pl-gift">
            <Head id="pl-gift" kicker="Tanda Kasih" title="Amplop Digital" />
            <p className={s.intro}>Doa restu Anda adalah karunia terindah. Bila berkenan mengirim tanda kasih, dapat melalui:</p>
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
                    </button>
                  )}
                </div>
              );
            })}
          </section>
        )}

        <section className={`${s.section} ${s.wishes}`} aria-labelledby="pl-wishes">
          <Head id="pl-wishes" kicker={rsvpClosed ? "Doa Restu" : "Konfirmasi & Doa"} title="Ucapan & Kehadiran" />
          {wishes.status === "sent" ? (
            <div ref={sentRef} className={`${s.form} ${s.sentBox}`} role="status">
              <Limar className={s.sentIcon} tone="red" />
              <p className={s.sent}>Terimo kasih, ucapan &amp; doa Anda sudah terkirim.</p>
              {!demo && wishes.pending && <p className={s.sentNote}>Ucapan Anda akan tampil setelah disetujui oleh mempelai.</p>}
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
              <label className={s.field}><span>Ucapan &amp; doa</span><textarea name="message" required maxLength={500} rows={3} placeholder="Tuliskan doa restu untuk kedua mempelai…" /></label>
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
              {!rsvpClosed && attendance !== "no" && <DietaryField className={`${s.field} ${s.diet}`} />}
              {wishes.status === "error" && <p className={s.error} role="alert">Belum terkirim. Coba lagi sebentar lagi.</p>}
              <button type="submit" className={s.submit} disabled={wishes.status === "sending"}>{wishes.status === "sending" ? "Mengirim…" : rsvpClosed ? "Kirim Ucapan" : "Kirim Ucapan & Konfirmasi"}</button>
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
          <div className={s.darkPattern} aria-hidden />
          <Crown className={s.closingCrown} />
          <p className={s.thanks}>Terimo Kasih</p>
          <p className={s.closingText}>Merupakan suatu kehormatan dan kebahagiaan bagi kami sekeluarga apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.</p>
          <p className={s.wassalam}>Wassalamu&rsquo;alaikum Warahmatullahi Wabarakatuh</p>
          <p className={s.family}>Kami yang berbahagia,<br />Keluarga Besar {families || couple}</p>
          <a href="/" target="_blank" rel="noreferrer" className={s.made}>dibuat dengan ♥ di Rawuh</a>
        </footer>
      </main>

      {music.visible && !music.failed && (
        <button type="button" className={music.playing ? `${s.music} ${s.musicOn}` : s.music} onClick={music.toggle} aria-pressed={music.playing} aria-label={music.playing ? "Matikan musik" : "Putar musik"}>
          <Lucide icon={ic.music} size={18} />
        </button>
      )}
    </ThemeShell>
  );
}
