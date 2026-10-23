"use client";
// Theme "Mawar Blush" — mawar cat air merah muda, bingkai lengkung, nama bertulisan tangan.
import { useEffect, useRef, useState, type FormEvent } from "react";
import {
  DietaryField, Extras, GuestCount, Icon, Photo, ThemeShell, Tick, dateParts, formatDate, giftInfo, guestLabel, mapsHref, storyItems,
  DATE_TBA, useCopy, useCountdown, useMusic, useRsvp, useThankYou, useWishes, type Attendance, type ThemeProps, type Wish,
} from "../kit";
import { tableLabel } from "../extras";
import type { GiftMethod } from "../../types";
import { celebrate } from "@/lib/celebrate";
import { ArchLine, Bouquet, Petal, Sprig } from "./ornaments";
import { ic } from "./icons";
import s from "./styles.module.css";

const FONTS = ["Pinyon Script", "Lora:ital,wght@0,400;0,500;0,600;1,400;1,500"];
const DEMO_WISHES: Wish[] = [
  { id: "w1", name: "Anindya Putri", attendance: "yes", message: "Kirana & Arya, selamat menempuh hidup baru! Semoga cinta kalian selalu mekar seperti hari ini." },
  { id: "w2", name: "Tante Wulan", attendance: "yes", message: "Barakallahu lakuma wa baraka 'alaikuma. Semoga menjadi keluarga sakinah, mawaddah, warahmah." },
];
const ATTEND: Record<Attendance, string> = { yes: "Hadir", maybe: "Ragu", no: "Berhalangan" };

/** "Putri kedua dari\nBapak Hadi Prasetyo & Ibu …" → "Hadi Prasetyo". */
function father(parents?: string) {
  const match = /(?:Bapak|Bpk\.?)\s+([^&\n]+?)\s*(?:&|\n|$)/i.exec(parents ?? "");
  return match?.[1].trim();
}

function plainName(guest?: string) {
  if (!guest || guest === "Tamu Undangan") return "";
  return guest.replace(/^(bapak|ibu|bpk\.?|sdr\.?|saudara|saudari)\s+/i, "").replace(/\s*(&|dan)\s*keluarga$/i, "").trim();
}

function giftIcon(gift: GiftMethod) {
  return gift.type === "bank" ? ic.landmark : gift.type === "ewallet" ? ic.wallet : gift.type === "qris" ? ic.qr : ic.gift;
}

function Head({ id, kicker, title }: { id: string; kicker: string; title: string }) {
  return (
    <div className={s.head}>
      <Sprig className={s.headSprig} />
      <p className={s.kicker}>{kicker}</p>
      <h2 id={id}>{title}</h2>
    </div>
  );
}

export default function MawarBlushTheme({ data, slug, guestToken, demo, skipCover }: ThemeProps) {
  const { bride, groom } = data.couple;
  const couple = [bride, groom].filter(Boolean).join(" & ");
  const label = data.eventLabel ?? "Pernikahan";
  const parts = dateParts(data.date);
  const shortDate = parts.day ? `${parts.day} . ${parts.month} . ${parts.year}` : DATE_TBA;
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
  const table = tableLabel(data.guestTable);
  const families = [father(data.couple.brideParents), father(data.couple.groomParents)].filter(Boolean).join(" & ");
  const sentRef = useRef<HTMLDivElement>(null);
  useEffect(() => { if (wishes.status === "sent") celebrate(sentRef.current); }, [wishes.status]);

  const people = [
    { short: bride, name: data.couple.brideFull || bride, parents: data.couple.brideParents, photo: data.couple.bridePhoto },
    ...(groom ? [{ short: groom, name: data.couple.groomFull || groom, parents: data.couple.groomParents, photo: data.couple.groomPhoto }] : []),
  ];

  const onSend = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const form = new FormData(event.currentTarget);
    const name = String(form.get("name") ?? "").trim();
    const message = String(form.get("message") ?? "").trim();
    const guests = attendance === "no" ? 1 : Number(form.get("guests")) || 1;
    if (!name || !message) return;
    void wishes.send(name, message);
    if (!rsvpClosed && rsvp.status !== "sent") void rsvp.submit({ name, attendance, guests, message, diet: String(form.get("diet") ?? "").trim() || undefined });
  };

  return (
    <ThemeShell
      fonts={FONTS}
      background="#f3dcd9"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.wash} aria-hidden />
          <Bouquet className={`${s.coverBouquet} ${s.tl}`} eager />
          <Bouquet className={`${s.coverBouquet} ${s.br}`} eager />
          <div className={s.petals} aria-hidden>
            {[0, 1, 2, 3, 4, 5].map(i => <Petal key={i} />)}
          </div>
          <div className={s.coverArch}>
            <ArchLine className={s.archLine} />
            <p className={s.kicker}>The Wedding of</p>
            <h1 className={s.coverNames}>
              <span>{bride}</span>
              {groom && <><em>&amp;</em><span>{groom}</span></>}
            </h1>
            <p className={s.coverDate}>{shortDate}</p>
          </div>
          <div className={s.guest}>
            <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
            <strong>{guestLabel(data)}</strong>
            {table && <span className={s.table}>{table}</span>}
          </div>
          <button type="button" className={s.openBtn} onClick={open}><Icon d={ic.mailOpen} size={16} />Buka Undangan</button>
        </section>
      )}
    >
      <main className={s.main}>
        <header className={s.opening}>
          <div className={s.heroArch}>
            <Photo src={hero} alt={`Foto ${couple}`} className={s.heroImg} />
          </div>
          <Bouquet className={s.heroBouquet} />
          <p className={s.kicker}>{label}</p>
          <h1 className={s.heroNames}>{couple}</h1>
          <p className={s.heroDate}>{formatDate(data.date)}</p>
        </header>

        <section className={s.salam} aria-label="Salam pembuka">
          <p className={s.salamTitle}>Assalamu&apos;alaikum Warahmatullahi Wabarakatuh</p>
          <p>Dengan memohon rahmat dan ridha Allah SWT, kami bermaksud menyelenggarakan {label.toLowerCase()} putra-putri kami. Merupakan kebahagiaan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.</p>
          {data.couple.note && <p className={s.note}>“{data.couple.note}”</p>}
        </section>

        <Extras slot="opening" />

        <section className={`${s.section} ${s.couple}`} aria-labelledby="mb-couple">
          <Head id="mb-couple" kicker="Dengan penuh cinta" title="Mempelai" />
          {people.map((person, index) => (
            <div key={index} className={s.personWrap}>
              {index === 1 && <p className={s.amp} aria-hidden>&amp;</p>}
              <article className={s.person}>
                <div className={`${s.personArch} ${index === 1 ? s.personArchAlt : ""}`}>
                  {person.photo ? <Photo src={person.photo} alt={person.name} /> : <span className={s.monogram} aria-hidden>{person.short.slice(0, 1)}</span>}
                  <Sprig className={s.personSprig} />
                </div>
                <p className={s.personShort} aria-hidden>{person.short}</p>
                <h3>{person.name}</h3>
                {person.parents && <p className={s.parents}>{person.parents}</p>}
              </article>
            </div>
          ))}
        </section>

        <section className={`${s.section} ${s.countSection}`} aria-labelledby="mb-count">
          <Head id="mb-count" kicker="Menuju hari bahagia" title="Hitung Mundur" />
          {countdown.valid ? (
            <div className={s.count} role="timer" aria-label={`${countdown.days} hari ${countdown.hours} jam ${countdown.minutes} menit lagi`}>
              {([[countdown.days, "Hari"], [countdown.hours, "Jam"], [countdown.minutes, "Menit"], [countdown.seconds, "Detik"]] as const).map(([value, unit]) => (
                <div key={unit} className={s.bloom}><b><Tick value={value} /></b><small>{unit}</small></div>
              ))}
            </div>
          ) : <p className={s.countTba}>{DATE_TBA}</p>}
        </section>

        <section className={`${s.section} ${s.events}`} aria-labelledby="mb-events">
          <Head id="mb-events" kicker="Waktu & tempat" title="Rangkaian Acara" />
          {data.events.map((event, index) => {
            const maps = mapsHref(data, event);
            return (
              <article key={event.name + index} className={s.event}>
                <Sprig className={s.eventSprig} />
                <h3>{event.name}</h3>
                <p className={s.eventDate}>{formatDate(event.date || data.date)}</p>
                {event.time && <p className={s.eventTime}><Icon d={ic.clock} size={14} />{event.time}</p>}
                <span className={s.rule} aria-hidden />
                <strong>{event.venue}</strong>
                {event.address && <p className={s.eventAddr}>{event.address}</p>}
                {maps && <a className={s.ghostBtn} href={maps} target="_blank" rel="noreferrer"><Icon d={ic.mapPin} size={14} />Petunjuk Lokasi</a>}
              </article>
            );
          })}
        </section>

        <Extras slot="event" />

        {stories.length > 0 && (
          <section className={`${s.section} ${s.story}`} aria-labelledby="mb-story">
            <Head id="mb-story" kicker="Sebuah perjalanan" title="Kisah Kami" />
            <ol className={s.timeline}>
              {stories.map((story, index) => (
                <li key={story.title + index}>
                  <span className={s.node} aria-hidden><Sprig /></span>
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

        <Extras slot="story" />

        {gallery.length > 0 && (
          <section className={`${s.section} ${s.gallery}`} aria-labelledby="mb-gallery">
            <Head id="mb-gallery" kicker="Momen berharga" title="Galeri" />
            <div className={s.grid}>
              {gallery.map((src, index) => <Photo key={src + index} src={src} alt={`Foto galeri ${index + 1}`} className={index === 0 ? s.gridFirst : undefined} />)}
            </div>
          </section>
        )}

        <section className={`${s.section} ${s.wishes}`} aria-labelledby="mb-wishes">
          <Head id="mb-wishes" kicker="Doa & kehadiran" title="RSVP & Ucapan" />
          {wishes.status === "sent" ? (
            <div ref={sentRef} className={`${s.card} ${s.sentCard}`} role="status">
              <p className={s.sent}>Terima kasih, doa &amp; ucapan Anda sudah kami terima.</p>
              {!demo && wishes.pending && <p className={s.sentNote}>Ucapan akan tampil setelah disetujui mempelai.</p>}
              {demo && <p className={s.sentNote}>Ini pratinjau, ucapan hanya tampil di daftar.</p>}
              <button type="button" className={s.submit} onClick={() => { wishes.reset(); rsvp.reset(); }}>Tulis Lagi</button>
            </div>
          ) : (
            <form className={s.card} onSubmit={onSend}>
              <label className={s.field}><span>Nama</span><input name="name" required maxLength={100} defaultValue={plainName(data.guestName)} placeholder="Nama Anda" autoComplete="name" /></label>
              <label className={s.field}><span>Ucapan &amp; doa</span><textarea name="message" required maxLength={500} rows={3} placeholder="Tuliskan doa terbaik Anda…" /></label>
              {rsvpClosed ? (
                <div className={s.closed} role="status"><strong>Konfirmasi kehadiran sudah ditutup</strong><p>Terima kasih atas doa dan perhatiannya. Ucapan &amp; doa masih bisa dikirim lewat form ini.</p></div>
              ) : (
                <div className={s.choices} role="radiogroup" aria-label="Kehadiran">
                  {(["yes", "maybe", "no"] as const).map(value => (
                    <button key={value} type="button" role="radio" aria-checked={attendance === value} className={attendance === value ? s.choiceOn : undefined} onClick={() => setAttendance(value)}>{ATTEND[value]}</button>
                  ))}
                </div>
              )}
              {!rsvpClosed && attendance !== "no" && <GuestCount label="Jumlah tamu" className={s.guests} labelClassName={s.guestsLabel} buttonClassName={s.step} />}
              {!rsvpClosed && attendance !== "no" && <DietaryField className={`${s.field} ${s.diet}`} />}
              {wishes.status === "error" && <p className={s.error} role="alert">Belum terkirim. Periksa koneksi lalu coba lagi.</p>}
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
          <section className={`${s.section} ${s.gifts}`} aria-labelledby="mb-gifts">
            <Head id="mb-gifts" kicker="Tanda kasih" title="Amplop Digital" />
            <p className={s.lead}>Doa restu Anda adalah hadiah terindah. Namun bila ingin berbagi tanda kasih, dapat melalui:</p>
            {data.gifts.map(gift => {
              const info = giftInfo(gift);
              const isAddress = gift.type === "address";
              const title = gift.type === "bank" ? (/^bank/i.test(info.title) ? info.title : `Bank ${info.title}`) : isAddress ? "Kirim Kado" : info.title;
              const on = Boolean(info.copy) && copied === info.copy;
              return (
                <div key={gift.id} className={`${s.gift} ${on ? s.giftOn : ""}`}>
                  <span className={s.giftIcon}><Icon d={giftIcon(gift)} size={18} /></span>
                  <div className={s.giftText}>
                    <small>{title}</small>
                    {info.number && <strong className={isAddress ? s.giftAddr : undefined}>{info.number}</strong>}
                    {info.holder && <span>a.n. {info.holder}</span>}
                    {info.image && <Photo src={info.image} alt="Kode QRIS" className={s.qris} />}
                  </div>
                  {info.copy && (
                    <button type="button" className={`${s.copy} ${on ? s.copyOn : ""}`} onClick={() => copy(info.copy)} aria-label={on ? "Tersalin" : `Salin ${isAddress ? "alamat" : "nomor"}`}>
                      <Icon key={on ? "on" : "off"} d={on ? ic.check : ic.copy} size={15} />
                    </button>
                  )}
                </div>
              );
            })}
          </section>
        )}

        <Extras slot="end" />

        <footer className={s.closing}>
          <Bouquet className={s.closeBouquet} />
          <p className={s.kicker}>Dengan cinta</p>
          <p className={s.thanks}>Terima Kasih</p>
          <p className={s.closingText}>Atas kehadiran dan doa restu Bapak/Ibu/Saudara/i, kami ucapkan terima kasih.</p>
          <p className={s.salamTitle}>Wassalamu&apos;alaikum Warahmatullahi Wabarakatuh</p>
          <p className={s.family}>Kami yang berbahagia,<br /><b>{couple}</b>{families && <><br />Keluarga Bpk. {families}</>}</p>
          <a href="/" target="_blank" rel="noreferrer" className={s.made}>dibuat dengan ♥ di Rawuh</a>
        </footer>
      </main>

      {music.visible && !music.failed && (
        <button type="button" className={`${s.music} ${music.playing ? s.musicOn : ""}`} onClick={music.toggle} aria-pressed={music.playing} {...music.attrs} aria-label={music.playing ? "Matikan musik" : "Putar musik"}>
          <Icon d={ic.music} size={18} />
        </button>
      )}
    </ThemeShell>
  );
}
