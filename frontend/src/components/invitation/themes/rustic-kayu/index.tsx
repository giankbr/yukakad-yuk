"use client";
// Theme "Rustic Kayu" — kertas kraft, papan kayu hangat, label bertali rami, dan rangkaian baby's breath.
import { useEffect, useRef, useState, type FormEvent } from "react";
import {
  DietaryField, Extras, GuestCount, Icon, Photo, ThemeShell, Tick, dateParts, formatDate, giftInfo, guestLabel, mapsHref, storyItems,
  DATE_TBA, useCopy, useCountdown, useMusic, useRsvp, useThankYou, useWishes, type Attendance, type ThemeProps, type Wish,
} from "../kit";
import { tableLabel } from "../extras";
import type { GiftMethod } from "../../types";
import { celebrate } from "@/lib/celebrate";
import { BabysBreath, Bow, Twine } from "./ornaments";
import { ic } from "./icons";
import s from "./styles.module.css";

const FONTS = ["Sacramento", "EB Garamond:ital,wght@0,400;0,500;0,600;1,400", "Caveat:wght@400;600"];
const DEMO_WISHES: Wish[] = [
  { id: "w1", name: "Laras & Dimas", attendance: "yes", message: "Sekar, Bagas, selamat ya! Nggak sabar lihat dekorasi kayunya. Semoga langgeng sampai kakek-nenek." },
  { id: "w2", name: "Bude Sri", attendance: "yes", message: "Mugi dados keluarga ingkang sakinah, mawaddah, warahmah. Bude ikut bahagia." },
];
const ATTEND: Record<Attendance, string> = { yes: "Hadir", maybe: "Ragu", no: "Berhalangan" };

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

function Head({ id, note, title }: { id: string; note: string; title: string }) {
  return (
    <div className={s.head}>
      <p className={s.hand}>{note}</p>
      <h2 id={id}>{title}</h2>
      <Twine className={s.twine} />
    </div>
  );
}

export default function RusticKayuTheme({ data, slug, guestToken, demo, skipCover }: ThemeProps) {
  const { bride, groom } = data.couple;
  const couple = [bride, groom].filter(Boolean).join(" & ");
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
  const table = tableLabel(data.guestTable);
  const families = [father(data.couple.brideParents), father(data.couple.groomParents)].filter(Boolean).join(" & ");
  const sentRef = useRef<HTMLDivElement>(null);
  useEffect(() => { if (wishes.status === "sent") celebrate(sentRef.current); }, [wishes.status]);

  const people = [
    { role: "Sang Mempelai Wanita", short: bride, name: data.couple.brideFull || bride, parents: data.couple.brideParents, photo: data.couple.bridePhoto },
    ...(groom ? [{ role: "Sang Mempelai Pria", short: groom, name: data.couple.groomFull || groom, parents: data.couple.groomParents, photo: data.couple.groomPhoto }] : []),
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
      background="#3e281a"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.planks} aria-hidden />
          <div className={s.kraftCard}>
            <div className={s.spray} aria-hidden>
              <BabysBreath className={s.sprayL} eager />
              <BabysBreath className={s.sprayR} eager />
              <Bow className={s.bow} eager />
            </div>
            <p className={s.hand}>undangan {label.toLowerCase()}</p>
            <h1 className={s.coverNames}>
              <span>{bride}</span>
              {groom && <><em>&amp;</em><span>{groom}</span></>}
            </h1>
            <div className={s.stamp}>
              {parts.day ? <><small>{parts.weekday}</small><b>{parts.day}</b><small>{parts.monthShort} {parts.year}</small></> : <small>{DATE_TBA}</small>}
            </div>
          </div>
          <div className={s.hangTag}>
            <span className={s.string} aria-hidden />
            <div className={s.tag}>
              <small>Kepada Yth.</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
          </div>
          <button type="button" className={s.openBtn} onClick={open}><Icon d={ic.mailOpen} size={16} />Buka Undangan</button>
        </section>
      )}
    >
      <main className={s.main}>
        <header className={s.opening}>
          <figure className={s.polaroid}>
            <span className={s.tape} aria-hidden />
            <Photo src={hero} alt={`Foto ${couple}`} />
            <figcaption>{couple}{parts.year ? `, ${parts.year}` : ""}</figcaption>
          </figure>
          <p className={s.kicker}>The Wedding of</p>
          <h1 className={s.heroNames}>{couple}</h1>
          <p className={s.heroDate}>{formatDate(data.date)}</p>
        </header>

        <section className={s.salam} aria-label="Salam pembuka">
          <BabysBreath className={s.salamSpray} />
          <p className={s.salamTitle}>Assalamu&apos;alaikum Warahmatullahi Wabarakatuh</p>
          <p>Dengan memohon rahmat dan ridha Allah SWT, kami bermaksud menyelenggarakan {label.toLowerCase()} kami secara sederhana dan hangat. Kehadiran Bapak/Ibu/Saudara/i akan melengkapi kebahagiaan kami.</p>
          {data.couple.note && <p className={s.note}>{data.couple.note}</p>}
        </section>

        <Extras slot="opening" />

        <section className={`${s.section} ${s.kraft}`} aria-labelledby="rk-couple">
          <Head id="rk-couple" note="dua hati, satu rumah" title="Mempelai" />
          <div className={s.tags}>
            {people.map((person, index) => (
              <article key={index} className={s.personTag}>
                <span className={s.string} aria-hidden />
                <div className={`${s.tag} ${s.bigTag}`}>
                  <div className={s.portrait}>
                    {person.photo ? <Photo src={person.photo} alt={person.name} /> : <span className={s.monogram} aria-hidden>{person.short.slice(0, 1)}</span>}
                  </div>
                  <small className={s.role}>{person.role}</small>
                  <h3>{person.name}</h3>
                  {person.parents && <p>{person.parents}</p>}
                </div>
              </article>
            ))}
          </div>
        </section>

        <section className={`${s.section} ${s.wood}`} aria-labelledby="rk-count">
          <div className={s.head}>
            <p className={`${s.hand} ${s.handLight}`}>tinggal sebentar lagi</p>
            <h2 id="rk-count" className={s.light}>Menghitung Hari</h2>
          </div>
          {countdown.valid ? (
            <div className={s.count} role="timer" aria-label={`${countdown.days} hari ${countdown.hours} jam ${countdown.minutes} menit lagi`}>
              {([[countdown.days, "hari"], [countdown.hours, "jam"], [countdown.minutes, "menit"], [countdown.seconds, "detik"]] as const).map(([value, unit]) => (
                <div key={unit} className={s.plaque}><b><Tick value={value} /></b><small>{unit}</small></div>
              ))}
            </div>
          ) : <p className={s.countTba}>{DATE_TBA}</p>}
        </section>

        <section className={`${s.section} ${s.paper}`} aria-labelledby="rk-events">
          <Head id="rk-events" note="catat tanggalnya ya" title="Acara" />
          {data.events.map((event, index) => {
            const p = dateParts(event.date || data.date);
            const maps = mapsHref(data, event);
            return (
              <article key={event.name + index} className={s.label}>
                <div className={s.labelIn}>
                  <div className={s.labelTop}>
                    <h3>{event.name}</h3>
                    <span className={s.miniStamp} aria-hidden>{p.day ? <><b>{p.day}</b>{p.monthShort}</> : "?"}</span>
                  </div>
                  <p className={s.eventDate}>{formatDate(event.date || data.date)}</p>
                  {event.time && <p className={s.eventTime}><Icon d={ic.clock} size={14} />{event.time}</p>}
                  <strong>{event.venue}</strong>
                  {event.address && <p className={s.eventAddr}>{event.address}</p>}
                  {maps && <a className={s.woodBtn} href={maps} target="_blank" rel="noreferrer"><Icon d={ic.mapPin} size={14} />Buka Peta</a>}
                </div>
              </article>
            );
          })}
        </section>

        <Extras slot="event" />

        {stories.length > 0 && (
          <section className={`${s.section} ${s.kraft}`} aria-labelledby="rk-story">
            <Head id="rk-story" note="dari awal sampai sekarang" title="Cerita Kami" />
            <ol className={s.notes}>
              {stories.map((story, index) => (
                <li key={story.title + index} className={s.noteCard}>
                  <span className={s.pin} aria-hidden />
                  {story.date && <small className={s.hand}>{story.date}</small>}
                  <h3>{story.title}</h3>
                  {story.body && <p>{story.body}</p>}
                  {story.image && <Photo src={story.image} alt={story.title} className={s.storyImg} />}
                </li>
              ))}
            </ol>
          </section>
        )}

        <Extras slot="story" />

        {gallery.length > 0 && (
          <section className={`${s.section} ${s.paper}`} aria-labelledby="rk-gallery">
            <Head id="rk-gallery" note="kenangan kecil" title="Galeri" />
            <div className={s.polaroids}>
              {gallery.map((src, index) => (
                <figure key={src + index} className={s.snap}>
                  <Photo src={src} alt={`Foto galeri ${index + 1}`} />
                </figure>
              ))}
            </div>
          </section>
        )}

        <section className={`${s.section} ${s.kraft}`} aria-labelledby="rk-wishes">
          <Head id="rk-wishes" note="kabari kami ya" title="RSVP & Ucapan" />
          {wishes.status === "sent" ? (
            <div ref={sentRef} className={`${s.notebook} ${s.sentCard}`} role="status">
              <p className={s.sent}>Matur nuwun! Ucapan &amp; doa Anda sudah kami terima.</p>
              {!demo && wishes.pending && <p className={s.sentNote}>Ucapan akan tampil setelah disetujui mempelai.</p>}
              {demo && <p className={s.sentNote}>Ini pratinjau, ucapan hanya tampil di daftar.</p>}
              <button type="button" className={s.submit} onClick={() => { wishes.reset(); rsvp.reset(); }}>Tulis Lagi</button>
            </div>
          ) : (
            <form className={s.notebook} onSubmit={onSend}>
              <label className={s.field}><span>Nama</span><input name="name" required maxLength={100} defaultValue={plainName(data.guestName)} placeholder="Nama Anda" autoComplete="name" /></label>
              <label className={s.field}><span>Ucapan</span><textarea name="message" required maxLength={500} rows={3} placeholder="Tulis doa & ucapan…" /></label>
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
          <section className={`${s.section} ${s.paper}`} aria-labelledby="rk-gifts">
            <Head id="rk-gifts" note="dengan tulus" title="Tanda Kasih" />
            <p className={s.lead}>Doa restu Anda sudah lebih dari cukup. Bila ingin memberi tanda kasih, dapat melalui:</p>
            {data.gifts.map(gift => {
              const info = giftInfo(gift);
              const isAddress = gift.type === "address";
              const title = gift.type === "bank" ? (/^bank/i.test(info.title) ? info.title : `Bank ${info.title}`) : isAddress ? "Kirim Kado" : info.title;
              const on = Boolean(info.copy) && copied === info.copy;
              return (
                <div key={gift.id} className={`${s.envelope} ${on ? s.envelopeOn : ""}`}>
                  <span className={s.flap} aria-hidden />
                  <div className={s.envBody}>
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
                </div>
              );
            })}
          </section>
        )}

        <Extras slot="end" />

        <footer className={s.closing}>
          <div className={s.closeSpray} aria-hidden><BabysBreath /><BabysBreath /><Bow className={s.bow} /></div>
          <p className={s.thanks}>Terima Kasih</p>
          <p className={s.closingText}>Kehadiran dan doa restu Bapak/Ibu/Saudara/i adalah hadiah paling berharga bagi kami.</p>
          <p className={`${s.hand} ${s.handLight}`}>Wassalamu&apos;alaikum Wr. Wb.</p>
          <p className={s.family}>Kami yang berbahagia,<br /><b>{couple}</b>{families && <><br />beserta keluarga Bpk. {families}</>}</p>
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
