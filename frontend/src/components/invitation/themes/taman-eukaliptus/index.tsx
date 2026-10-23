"use client";
// Theme "Taman Eukaliptus" — hijau sage, ranting eukaliptus menjuntai, bingkai oval, dan label ala herbarium.
import { useEffect, useRef, useState, type FormEvent } from "react";
import {
  DietaryField, Extras, GuestCount, Icon, Photo, ThemeShell, Tick, dateParts, formatDate, giftInfo, guestLabel, mapsHref, storyItems,
  DATE_TBA, useCopy, useCountdown, useMusic, useRsvp, useThankYou, useWishes, type Attendance, type ThemeProps, type Wish,
} from "../kit";
import { tableLabel } from "../extras";
import type { GiftMethod } from "../../types";
import { celebrate } from "@/lib/celebrate";
import { Branch, Sprig } from "./ornaments";
import { ic } from "./icons";
import s from "./styles.module.css";

const FONTS = ["DM Serif Display:ital@0;1", "DM Sans:ital,opsz,wght@0,9..40,400;0,9..40,500;0,9..40,700;1,9..40,400"];
const DEMO_WISHES: Wish[] = [
  { id: "w1", name: "Hana Safitri", attendance: "yes", message: "Nayla & Fikri, selamat! Pesta taman kalian pasti seindah kisahnya. Semoga sakinah, mawaddah, warahmah." },
  { id: "w2", name: "Rekan Kantor Fikri", attendance: "maybe", message: "Selamat menempuh hidup baru, Bro. Semoga jadi keluarga yang selalu teduh dan rimbun kebahagiaan." },
];
const ATTEND: Record<Attendance, string> = { yes: "Hadir", maybe: "Ragu", no: "Berhalangan" };
const pad = (n: number) => String(n).padStart(2, "0");

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
      <p className={s.kicker}>{kicker}</p>
      <h2 id={id}>{title}</h2>
      <Sprig className={s.headSprig} />
    </div>
  );
}

export default function TamanEukaliptusTheme({ data, slug, guestToken, demo, skipCover }: ThemeProps) {
  const { bride, groom } = data.couple;
  const couple = [bride, groom].filter(Boolean).join(" & ");
  const label = data.eventLabel ?? "Pernikahan";
  const parts = dateParts(data.date);
  const longDate = parts.day ? `${parts.weekday}, ${parts.day} ${parts.month} ${parts.year}` : DATE_TBA;
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
    { role: "Mempelai Wanita", short: bride, name: data.couple.brideFull || bride, parents: data.couple.brideParents, photo: data.couple.bridePhoto },
    ...(groom ? [{ role: "Mempelai Pria", short: groom, name: data.couple.groomFull || groom, parents: data.couple.groomParents, photo: data.couple.groomPhoto }] : []),
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
      background="#e3e7da"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.garland} aria-hidden>
            <Branch className={`${s.branch} ${s.b1}`} eager /><Branch className={`${s.branch} ${s.b2}`} variant="b" eager />
            <Branch className={`${s.branch} ${s.b3}`} variant="b" eager /><Branch className={`${s.branch} ${s.b4}`} eager />
          </div>
          <div className={s.oval}>
            <span className={s.ovalRing} aria-hidden />
            <Photo src={hero} alt="" className={s.ovalImg} />
          </div>
          <div className={s.coverText}>
            <p className={s.kicker}>The Wedding of</p>
            <h1 className={s.coverNames}>{bride}{groom && <><em> &amp; </em>{groom}</>}</h1>
            <p className={s.coverDate}>{longDate}</p>
          </div>
          <div className={s.specimen}>
            <div className={s.specRow}><small>Kepada Yth.</small><small>{table || "Tamu"}</small></div>
            <strong>{guestLabel(data)}</strong>
            <small className={s.specFoot}>Bapak/Ibu/Saudara/i, di tempat</small>
          </div>
          <button type="button" className={s.openBtn} onClick={open}><Icon d={ic.mailOpen} size={16} />Buka Undangan</button>
        </section>
      )}
    >
      <main className={s.main}>
        <header className={s.opening}>
          <Photo src={hero} alt={`Foto ${couple}`} className={s.openingImg} />
          <div className={s.openingText}>
            <p className={s.kicker}>{label}</p>
            <h1>{couple}</h1>
            <p>{longDate}</p>
          </div>
        </header>

        <section className={s.salam} aria-label="Salam pembuka">
          <Sprig className={s.headSprig} />
          <p className={s.salamTitle}>Assalamu&apos;alaikum Warahmatullahi Wabarakatuh</p>
          <p>Dengan memohon rahmat dan ridha Allah SWT, kami mengundang Bapak/Ibu/Saudara/i untuk hadir dalam pesta taman sederhana yang kami siapkan dengan sepenuh hati.</p>
          {data.couple.note && <p className={s.note}>{data.couple.note}</p>}
        </section>

        <Extras slot="opening" />

        <section className={`${s.section} ${s.tint}`} aria-labelledby="te-couple">
          <Head id="te-couple" kicker="Yang berbahagia" title="Kedua Mempelai" />
          <div className={`${s.duo} ${people.length === 1 ? s.solo : ""}`}>
            {people.map((person, index) => (
              <article key={index} className={s.person}>
                <div className={s.personOval}>
                  {person.photo ? <Photo src={person.photo} alt={person.name} /> : <span className={s.monogram} aria-hidden>{person.short.slice(0, 1)}</span>}
                </div>
                <small className={s.role}>{person.role}</small>
                <h3>{person.name}</h3>
                {person.parents && <p>{person.parents}</p>}
              </article>
            ))}
          </div>
        </section>

        <section className={s.section} aria-labelledby="te-count">
          <Head id="te-count" kicker={longDate} title="Hitung Mundur" />
          {countdown.valid ? (
            <div className={s.count} role="timer" aria-label={`${countdown.days} hari ${countdown.hours} jam ${countdown.minutes} menit lagi`}>
              {([[countdown.days, "Hari"], [countdown.hours, "Jam"], [countdown.minutes, "Menit"], [countdown.seconds, "Detik"]] as const).map(([value, unit]) => (
                <div key={unit} className={s.pod}><b><Tick value={value} /></b><small>{unit}</small></div>
              ))}
            </div>
          ) : <p className={s.countTba}>{DATE_TBA}</p>}
        </section>

        <section className={`${s.section} ${s.tint}`} aria-labelledby="te-events">
          <Head id="te-events" kicker="Catat tanggalnya" title="Rangkaian Acara" />
          {data.events.map((event, index) => {
            const maps = mapsHref(data, event);
            return (
              <article key={event.name + index} className={s.label}>
                <div className={s.labelHead}>
                  <small>No. {pad(index + 1)}</small>
                  <Sprig className={s.labelSprig} />
                </div>
                <h3>{event.name}</h3>
                <dl className={s.rows}>
                  <div><dt>Tanggal</dt><dd>{formatDate(event.date || data.date)}</dd></div>
                  {event.time && <div><dt>Waktu</dt><dd>{event.time}</dd></div>}
                  <div><dt>Tempat</dt><dd><b>{event.venue}</b>{event.address && <span>{event.address}</span>}</dd></div>
                </dl>
                {maps && <a className={s.pillBtn} href={maps} target="_blank" rel="noreferrer"><Icon d={ic.mapPin} size={14} />Petunjuk Arah</a>}
              </article>
            );
          })}
        </section>

        <Extras slot="event" />

        {stories.length > 0 && (
          <section className={s.section} aria-labelledby="te-story">
            <Head id="te-story" kicker="Tumbuh bersama" title="Kisah Cinta" />
            <ol className={s.vine}>
              {stories.map((story, index) => (
                <li key={story.title + index}>
                  <span className={s.bud} aria-hidden />
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
          <section className={`${s.section} ${s.tint}`} aria-labelledby="te-gallery">
            <Head id="te-gallery" kicker="Potret kebahagiaan" title="Galeri" />
            <div className={s.grid}>
              {gallery.map((src, index) => <Photo key={src + index} src={src} alt={`Foto galeri ${index + 1}`} />)}
            </div>
          </section>
        )}

        <section className={s.section} aria-labelledby="te-wishes">
          <Head id="te-wishes" kicker="Kabar & doa" title="RSVP & Ucapan" />
          {wishes.status === "sent" ? (
            <div ref={sentRef} className={`${s.card} ${s.sentCard}`} role="status">
              <p className={s.sent}>Terima kasih, ucapan &amp; doa Anda sudah kami terima.</p>
              {!demo && wishes.pending && <p className={s.sentNote}>Ucapan akan tampil setelah disetujui mempelai.</p>}
              {demo && <p className={s.sentNote}>Ini pratinjau, ucapan hanya tampil di daftar.</p>}
              <button type="button" className={s.submit} onClick={() => { wishes.reset(); rsvp.reset(); }}>Tulis Lagi</button>
            </div>
          ) : (
            <form className={s.card} onSubmit={onSend}>
              <label className={s.field}><span>Nama</span><input name="name" required maxLength={100} defaultValue={plainName(data.guestName)} placeholder="Nama Anda" autoComplete="name" /></label>
              <label className={s.field}><span>Ucapan &amp; doa</span><textarea name="message" required maxLength={500} rows={3} placeholder="Tuliskan doa terbaik…" /></label>
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
                <span className={s.avatar} aria-hidden>{wish.name.trim().slice(0, 1).toUpperCase()}</span>
                <div>
                  <div className={s.wishHead}><strong>{wish.name}</strong>{wish.attendance && <small>{ATTEND[wish.attendance]}</small>}</div>
                  <p>{wish.message}</p>
                </div>
              </article>
            ))}
          </div>
        </section>

        {data.gifts.length > 0 && (
          <section className={`${s.section} ${s.tint}`} aria-labelledby="te-gifts">
            <Head id="te-gifts" kicker="Tanda kasih" title="Kado Digital" />
            <p className={s.lead}>Kehadiran dan doa restu Anda adalah hadiah terindah. Bila ingin berbagi tanda kasih:</p>
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
                      <Icon key={on ? "on" : "off"} d={on ? ic.check : ic.copy} size={14} />{on ? "Tersalin" : "Salin"}
                    </button>
                  )}
                </div>
              );
            })}
          </section>
        )}

        <Extras slot="end" />

        <footer className={s.closing}>
          <div className={s.closeGarland} aria-hidden><Branch className={s.cb1} /><Branch className={s.cb2} variant="b" /></div>
          <p className={s.thanks}>Terima Kasih</p>
          <p className={s.closingText}>Merupakan kehormatan dan kebahagiaan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.</p>
          <p className={s.salamTitle}>Wassalamu&apos;alaikum Warahmatullahi Wabarakatuh</p>
          <p className={s.family}>Kami yang berbahagia<br /><b>{couple}</b>{families && <><br />Keluarga Bpk. {families}</>}</p>
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
