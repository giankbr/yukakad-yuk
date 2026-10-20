"use client";
// Theme "Emas Hitam" — mewah hitam-emas bergaya art deco: kipas sunburst, sudut bertingkat, bingkai bersegi.
import { useEffect, useRef, useState, type FormEvent, type ReactNode } from "react";
import {
  DietaryField, Extras, GuestCount, Icon, Photo, ThemeShell, Tick, dateParts, formatDate, giftInfo, guestLabel, mapsHref, storyItems,
  toDate, DATE_TBA, useCopy, useCountdown, useMusic, useRsvp, useThankYou, useWishes, type Attendance, type ThemeProps, type Wish,
} from "../kit";
import { tableLabel } from "../extras";
import type { GiftMethod } from "../../types";
import { celebrate } from "@/lib/celebrate";
import { Corner, Fan, Rule } from "./ornaments";
import { ic } from "./icons";
import s from "./styles.module.css";

const FONTS = ["Italiana", "Marcellus", "Josefin Sans:ital,wght@0,300;0,400;0,600;1,300"];
const DEMO_WISHES: Wish[] = [
  { id: "w1", name: "Clarissa Wijaya", attendance: "yes", message: "Selamat Alana & Raditya! Malam yang pasti tak terlupakan. Bahagia selamanya." },
  { id: "w2", name: "Keluarga Om Hendra", attendance: "maybe", message: "Semoga rumah tangga kalian selalu dilimpahi berkah, kasih, dan kesetiaan." },
];
const ATTEND: Record<Attendance, string> = { yes: "Hadir", maybe: "Ragu", no: "Berhalangan" };
const pad = (n: number | string) => String(n).padStart(2, "0");

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

function monthNum(value?: string) {
  const date = toDate(value);
  return date ? pad(new Intl.DateTimeFormat("en", { timeZone: "Asia/Jakarta", month: "numeric" }).format(date)) : "";
}

function Head({ id, title, sub }: { id: string; title: string; sub?: string }) {
  return (
    <div className={s.head}>
      <h2 id={id}>{title}</h2>
      <Rule className={s.rule} />
      {sub && <p className={s.sub}>{sub}</p>}
    </div>
  );
}

/** Chamfered gold-edged panel. */
function Panel({ className, children }: { className?: string; children: ReactNode }) {
  return <div className={`${s.panel} ${className ?? ""}`}><div className={s.panelIn}>{children}</div></div>;
}

export default function EmasHitamTheme({ data, slug, guestToken, demo, skipCover }: ThemeProps) {
  const { bride, groom } = data.couple;
  const couple = [bride, groom].filter(Boolean).join(" & ");
  const label = data.eventLabel ?? "Pernikahan";
  const parts = dateParts(data.date);
  const numeric = parts.day ? `${pad(parts.day)} · ${monthNum(data.date)} · ${parts.year}` : DATE_TBA;
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
      background="#050505"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.pattern} aria-hidden data-noreveal />
          <div className={s.frame} aria-hidden>
            <Corner className={`${s.corner} ${s.c1}`} /><Corner className={`${s.corner} ${s.c2}`} />
            <Corner className={`${s.corner} ${s.c3}`} /><Corner className={`${s.corner} ${s.c4}`} />
          </div>
          <Fan className={s.coverFan} eager />
          <p className={s.kicker}>The Wedding of</p>
          <h1 className={s.coverNames}>
            <span className={s.gold}>{bride}</span>
            {groom && <><em>&amp;</em><span className={s.gold}>{groom}</span></>}
          </h1>
          <Rule className={s.coverRule} />
          <p className={s.coverDate}>{numeric}</p>
          <div className={s.guest}>
            <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
            <strong>{guestLabel(data)}</strong>
            {table && <span className={s.table}>{table}</span>}
          </div>
          <button type="button" className={s.openBtn} onClick={open}><Icon d={ic.mailOpen} size={15} />Buka Undangan</button>
        </section>
      )}
    >
      <main className={s.main}>
        <header className={s.opening}>
          <div className={s.heroFrame}><Photo src={hero} alt={`Foto ${couple}`} className={s.heroImg} /></div>
          <div className={s.heroText}>
            <Fan className={s.heroFan} />
            <p className={s.kicker}>{label}</p>
            <h1 className={s.heroNames}><span className={s.gold}>{couple}</span></h1>
            <p className={s.heroDate}>{numeric}</p>
          </div>
        </header>

        <section className={s.intro} aria-label="Pembuka">
          <Rule className={s.rule} />
          <p>Dengan penuh sukacita dan memohon rahmat Tuhan Yang Maha Esa, kami mengundang Bapak/Ibu/Saudara/i untuk merayakan {label.toLowerCase()} kami dalam sebuah malam yang istimewa.</p>
          {data.couple.note && <p className={s.note}>{data.couple.note}</p>}
        </section>

        <Extras slot="opening" />

        <section className={s.section} aria-labelledby="eh-couple">
          <Head id="eh-couple" title="Sang Mempelai" />
          <div className={`${s.duo} ${people.length === 1 ? s.solo : ""}`}>
            {people.map((person, index) => (
              <article key={index} className={s.person}>
                <div className={s.portrait}>
                  {person.photo ? <Photo src={person.photo} alt={person.name} /> : <span className={s.monogram} aria-hidden>{person.short.slice(0, 1)}</span>}
                </div>
                <small className={s.role}>{person.role}</small>
                <h3>{person.name}</h3>
                {person.parents && <p>{person.parents}</p>}
              </article>
            ))}
          </div>
        </section>

        <section className={`${s.section} ${s.band}`} aria-labelledby="eh-count">
          <Head id="eh-count" title="Menuju Hari H" sub={formatDate(data.date)} />
          {countdown.valid ? (
            <div className={s.count} role="timer" aria-label={`${countdown.days} hari ${countdown.hours} jam ${countdown.minutes} menit lagi`}>
              {([[countdown.days, "Hari"], [countdown.hours, "Jam"], [countdown.minutes, "Menit"], [countdown.seconds, "Detik"]] as const).map(([value, unit]) => (
                <div key={unit} className={s.tile}><b><Tick value={value} /></b><small>{unit}</small></div>
              ))}
            </div>
          ) : <p className={s.countTba}>{DATE_TBA}</p>}
        </section>

        <section className={s.section} aria-labelledby="eh-events">
          <Head id="eh-events" title="Rangkaian Acara" />
          {data.events.map((event, index) => {
            const p = dateParts(event.date || data.date);
            const maps = mapsHref(data, event);
            return (
              <Panel key={event.name + index} className={s.event}>
                <div className={s.eventDay}>
                  <b>{p.day ? pad(p.day) : "--"}</b>
                  <small>{p.monthShort || "TBA"}</small>
                  <small>{p.year}</small>
                </div>
                <div className={s.eventBody}>
                  <h3>{event.name}</h3>
                  <p className={s.eventMeta}>{p.weekday ? `${p.weekday}` : DATE_TBA}{event.time ? ` · ${event.time}` : ""}</p>
                  <strong>{event.venue}</strong>
                  {event.address && <p className={s.eventAddr}>{event.address}</p>}
                  {maps && <a className={s.lineBtn} href={maps} target="_blank" rel="noreferrer"><Icon d={ic.mapPin} size={13} />Lihat Lokasi</a>}
                </div>
              </Panel>
            );
          })}
        </section>

        <Extras slot="event" />

        {stories.length > 0 && (
          <section className={`${s.section} ${s.band}`} aria-labelledby="eh-story">
            <Head id="eh-story" title="Kisah Kami" />
            <ol className={s.timeline}>
              {stories.map((story, index) => (
                <li key={story.title + index}>
                  <span className={s.diamond} aria-hidden><i /></span>
                  <div className={s.storyText}>
                    <small>{story.date ?? `Bab ${index + 1}`}</small>
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
          <section className={s.section} aria-labelledby="eh-gallery">
            <Head id="eh-gallery" title="Galeri" />
            <div className={`${s.mosaic} ${gallery.length < 3 ? s.mosaicShort : ""}`}>
              {gallery.map((src, index) => <Photo key={src + index} src={src} alt={`Foto galeri ${index + 1}`} />)}
            </div>
          </section>
        )}

        <section className={`${s.section} ${s.band}`} aria-labelledby="eh-wishes">
          <Head id="eh-wishes" title="RSVP & Ucapan" sub="Mohon konfirmasi kehadiran Anda" />
          {wishes.status === "sent" ? (
            <div ref={sentRef} className={`${s.form} ${s.sentCard}`} role="status">
              <p className={s.sent}>Terima kasih. Ucapan Anda telah kami terima dengan hangat.</p>
              {!demo && wishes.pending && <p className={s.sentNote}>Ucapan akan tampil setelah disetujui mempelai.</p>}
              {demo && <p className={s.sentNote}>Ini pratinjau, ucapan hanya tampil di daftar.</p>}
              <button type="button" className={s.submit} onClick={() => { wishes.reset(); rsvp.reset(); }}>Tulis Lagi</button>
            </div>
          ) : (
            <form className={s.form} onSubmit={onSend}>
              <label className={s.field}><span>Nama</span><input name="name" required maxLength={100} defaultValue={plainName(data.guestName)} placeholder="Nama Anda" autoComplete="name" /></label>
              <label className={s.field}><span>Ucapan</span><textarea name="message" required maxLength={500} rows={3} placeholder="Tuliskan ucapan & doa…" /></label>
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
              <button type="submit" className={s.submit} disabled={wishes.status === "sending"}>{wishes.status === "sending" ? "Mengirim…" : "Kirim"}</button>
            </form>
          )}
          {wishes.wishes.length === 0 && <p className={s.empty}>Belum ada ucapan. Jadilah yang pertama.</p>}
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
          <section className={s.section} aria-labelledby="eh-gifts">
            <Head id="eh-gifts" title="Tanda Kasih" sub="Doa restu Anda adalah karunia terbesar. Bagi yang ingin berbagi tanda kasih:" />
            {data.gifts.map(gift => {
              const info = giftInfo(gift);
              const isAddress = gift.type === "address";
              const title = gift.type === "bank" ? (/^bank/i.test(info.title) ? info.title : `Bank ${info.title}`) : isAddress ? "Kirim Kado" : info.title;
              const on = Boolean(info.copy) && copied === info.copy;
              return (
                <div key={gift.id} className={`${s.card} ${isAddress ? s.cardPlain : ""} ${on ? s.cardOn : ""}`}>
                  <div className={s.cardTop}>
                    <span className={s.cardTitle}><Icon d={giftIcon(gift)} size={16} />{title}</span>
                    {!isAddress && gift.type !== "qris" && <span className={s.chip} aria-hidden />}
                  </div>
                  {info.number && <strong className={isAddress ? s.cardAddr : s.cardNo}>{info.number}</strong>}
                  {info.image && <Photo src={info.image} alt="Kode QRIS" className={s.qris} />}
                  <div className={s.cardBottom}>
                    <span>{info.holder ? info.holder : isAddress ? "Alamat pengiriman" : ""}</span>
                    {info.copy && (
                      <button type="button" className={`${s.copy} ${on ? s.copyOn : ""}`} onClick={() => copy(info.copy)} aria-label={on ? "Tersalin" : `Salin ${isAddress ? "alamat" : "nomor"}`}>
                        <Icon key={on ? "on" : "off"} d={on ? ic.check : ic.copy} size={13} />{on ? "Tersalin" : "Salin"}
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
          <Fan className={s.closeFan} />
          <p className={s.thanks}><span className={s.gold}>Terima Kasih</span></p>
          <p className={s.closingText}>Merupakan suatu kehormatan apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.</p>
          <Rule className={s.rule} />
          <p className={s.family}>Kami yang berbahagia<br /><b>{couple}</b>{families && <><br />Keluarga {families}</>}</p>
          <a href="/" target="_blank" rel="noreferrer" className={s.made}>dibuat dengan ♥ di Rawuh</a>
        </footer>
      </main>

      {music.visible && !music.failed && (
        <button type="button" className={`${s.music} ${music.playing ? s.musicOn : ""}`} onClick={music.toggle} aria-pressed={music.playing} aria-label={music.playing ? "Matikan musik" : "Putar musik"}>
          <Icon d={ic.music} size={17} />
        </button>
      )}
    </ThemeShell>
  );
}
