"use client";
// Theme "Pantai Senja" — gradasi langit senja di tepi pantai: matahari tenggelam, ombak berlapis, nyiur melambai.
import { useEffect, useRef, useState } from "react";
import {
  DATE_TBA, DietaryField, Extras, GuestCount, Icon, Photo, ThemeShell, Tick, coupleLabel, dateParts, formatDate, giftInfo, guestLabel, icons,
  mapsHref, sentSummary, storyItems, useCopy, useCountdown, useRsvp, useThankYou, useWishes, type Attendance, type ThemeProps, type Wish,
} from "../kit";
import { tableLabel } from "../extras";
import { celebrate } from "@/lib/celebrate";
import s from "./styles.module.css";

const FONTS = ["Great Vibes", "Cormorant Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500", "Mulish:wght@400;500;600;700"];
const ATTEND: Record<Attendance, string> = { yes: "Hadir", maybe: "Ragu", no: "Berhalangan" };
const DEMO_WISHES: Wish[] = [
  { id: "w1", name: "Gek Ayu", attendance: "yes", message: "Selamat Kirana & Damar! Semoga cinta kalian seluas samudra dan sehangat senja di Melasti." },
  { id: "w2", name: "Om Bagus", attendance: "maybe", message: "Bahagia selalu, semoga menjadi keluarga yang saling menguatkan di setiap musim." },
];
const wallet = ["M19 7V4a1 1 0 0 0-1-1H5a2 2 0 0 0 0 4h15a1 1 0 0 1 1 1v4h-3a2 2 0 0 0 0 4h3a1 1 0 0 0 1-1v-2a1 1 0 0 0-1-1", "M3 5v14a2 2 0 0 0 2 2h15a1 1 0 0 0 1-1v-4"];
const bank = ["M3 22h18", "M6 18v-7", "M10 18v-7", "M14 18v-7", "M18 18v-7", "M12 2l8 5H4z"];

const ART = "/themes/art/pantai-senja";

/** Painted art (decorative): never opens the photo lightbox. */
function Art({ src, className, width, height, eager }: { src: string; className?: string; width: number; height: number; eager?: boolean }) {
  return (
    // eslint-disable-next-line @next/next/no-img-element -- static decorative painting
    <img src={`${ART}/${src}.webp`} alt="" aria-hidden className={className} width={width} height={height} data-nolightbox
      loading={eager ? "eager" : "lazy"} fetchPriority={eager ? "high" : undefined} decoding="async" draggable={false} />
  );
}

/** Painted wave band; a seamless 390px tile repeated on a 200%-wide strip so it can drift. */
function Waves({ className }: { className?: string }) {
  return <span className={className} aria-hidden />;
}

/** Hand-painted palm silhouette: trunk + crown are separate paintings so the fronds can rustle on their own. */
function Palm({ className, eager }: { className?: string; eager?: boolean }) {
  return (
    <span className={className} aria-hidden>
      <Art src="palm-trunk" width={180} height={280} eager={eager} />
      <Art src="palm-crown" className={s.fronds} width={180} height={280} eager={eager} />
    </span>
  );
}

function Shell({ size = 22 }: { size?: number }) {
  return <Art src="shell" className={s.shellArt} width={size} height={Math.round(size * 92 / 109)} />;
}

function Head({ id, kicker, title }: { id: string; kicker?: string; title: string }) {
  return (
    <div className={s.head}>
      {kicker && <p className={s.kicker}>{kicker}</p>}
      <h2 id={id}>{title}</h2>
      <span className={s.ripple} aria-hidden><i /><b /><i /></span>
    </div>
  );
}

function plainName(guest?: string) {
  if (!guest || guest === "Tamu Undangan") return "";
  return guest.replace(/^(bapak|ibu|bpk\.?|sdr\.?|saudara|saudari)\s+/i, "").replace(/\s*(&|dan)\s*keluarga$/i, "").trim();
}

/** "Putri dari Bapak Made Suarta & Ibu …" → "Bapak Made Suarta" */
function fatherOf(parents?: string) {
  const match = /((?:Bapak|Bpk\.?)\s+[^&\n,]+)/i.exec(parents ?? "");
  return match?.[1].trim();
}

export default function PantaiSenjaTheme({ data, slug, guestToken, demo, skipCover }: ThemeProps) {
  const couple = coupleLabel(data);
  const label = data.eventLabel ?? "Pernikahan";
  const parts = dateParts(data.date);
  const countdown = useCountdown(data.date);
  const rsvp = useRsvp({ slug, guestToken, demo });
  const wishes = useWishes({ slug, guestToken, demo, seed: DEMO_WISHES });
  const thanks = useThankYou();
  const rsvpClosed = thanks.active || rsvp.status === "closed";
  const { copy, copied } = useCopy();
  const [attendance, setAttendance] = useState<Attendance>("yes");
  const stories = storyItems(data);
  const hero = data.gallery[0] ?? data.couple.bridePhoto ?? data.couple.groomPhoto;
  const [feature, ...rest] = data.gallery.slice(1).length ? data.gallery.slice(1) : data.gallery;
  const table = tableLabel(data.guestTable);
  const families = [fatherOf(data.couple.brideParents), fatherOf(data.couple.groomParents)].filter(Boolean);
  const sentRef = useRef<HTMLDivElement>(null);
  const sent = wishes.status === "sent";
  useEffect(() => { if (sent) celebrate(sentRef.current); }, [sent]);
  const people = [
    { role: "Mempelai Wanita", nick: data.couple.bride, name: data.couple.brideFull || data.couple.bride, parents: data.couple.brideParents, photo: data.couple.bridePhoto },
    { role: "Mempelai Pria", nick: data.couple.groom, name: data.couple.groomFull || data.couple.groom, parents: data.couple.groomParents, photo: data.couple.groomPhoto },
  ];

  return (
    <ThemeShell
      fonts={FONTS}
      background="#2b2148"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.sky} aria-hidden />
          <Art src="birds" className={s.birds} width={64} height={25} eager />
          <span className={s.sun} aria-hidden><i /></span>
          <div className={s.sea} aria-hidden>
            <Waves className={`${s.wave} ${s.waveBack}`} />
            <Waves className={`${s.wave} ${s.waveMid}`} />
            <Waves className={`${s.wave} ${s.waveFront}`} />
          </div>
          <Palm className={`${s.palm} ${s.palmLeft}`} eager />
          <Palm className={`${s.palm} ${s.palmRight}`} eager />
          <div className={s.coverTop}>
            <p className={s.coverKicker}>The Wedding of</p>
            <h1 className={s.coverNames}><span>{data.couple.bride}</span><em>&amp;</em><span>{data.couple.groom}</span></h1>
            <p className={s.coverDate}>{parts.day ? `${parts.weekday}, ${parts.day} ${parts.month} ${parts.year}` : DATE_TBA}</p>
          </div>
          <div className={s.coverBottom}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Icon d={icons.mailOpen} size={16} />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <main className={s.main}>
        <header className={s.hero}>
          <Photo src={hero} alt={`Foto ${couple}`} className={s.heroImg} />
          <div className={s.heroTint} aria-hidden />
          <div className={s.heroText}>
            <p className={s.kickerLight}>Kami menikah</p>
            <h1>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.heroDate}>{parts.day ? `${parts.day} · ${parts.month} · ${parts.year}` : DATE_TBA}</p>
          </div>
          <Waves className={`${s.edge} ${s.edgeSand}`} />
        </header>

        <section className={`${s.section} ${s.opening}`} aria-label="Salam pembuka">
          <Shell size={44} />
          <p className={s.salam}><span>Om Swastiastu</span><span>Assalamu&apos;alaikum</span><span>Salam sejahtera</span></p>
          <p className={s.lead}>{data.couple.note || "Dengan penuh syukur, kami mengundang Anda untuk menyaksikan hari bahagia kami."}</p>
          <p className={s.body}>Dengan memohon rahmat Tuhan Yang Maha Esa, kami bermaksud melangsungkan {label.toLowerCase()} di tepi pantai, tepat saat langit berubah jingga.</p>
        </section>

        <Extras slot="opening" />

        <section className={`${s.section} ${s.couple}`} aria-labelledby="ps-couple">
          <Head id="ps-couple" kicker="Dua hati, satu cakrawala" title="Sang Mempelai" />
          {people.map((person, index) => (
            <div key={index} className={s.personWrap}>
              {index === 1 && <p className={s.amp} aria-hidden>&amp;</p>}
              <article className={s.person}>
                <div className={s.porthole}>
                  {person.photo ? <Photo src={person.photo} alt={person.name} /> : <span className={s.mono} aria-hidden>{person.nick.slice(0, 1)}</span>}
                </div>
                <p className={s.role}>{person.role}</p>
                <h3>{person.name}</h3>
                {person.parents && <p className={s.parents}>{person.parents}</p>}
              </article>
            </div>
          ))}
        </section>

        <section className={`${s.section} ${s.dusk}`} aria-labelledby="ps-count">
          <span className={s.duskSun} aria-hidden />
          <Head id="ps-count" kicker="Menuju hari bahagia" title="Hitung Mundur" />
          {countdown.valid ? (
            <div className={s.count} role="timer" aria-label={`${countdown.days} hari ${countdown.hours} jam ${countdown.minutes} menit lagi`}>
              {[[countdown.days, "Hari"], [countdown.hours, "Jam"], [countdown.minutes, "Menit"], [countdown.seconds, "Detik"]].map(([value, unit]) => (
                <div key={unit}><b><Tick value={value} /></b><small>{unit}</small></div>
              ))}
            </div>
          ) : <p className={s.tba}>{DATE_TBA}</p>}
          <p className={s.duskNote}>{formatDate(data.date)}</p>
          <Waves className={`${s.edge} ${s.edgeFoam}`} />
        </section>

        <section className={`${s.section} ${s.events}`} aria-labelledby="ps-events">
          <Head id="ps-events" kicker="Simpan tanggalnya" title="Rangkaian Acara" />
          {data.events.map((event, index) => {
            const maps = mapsHref(data, event);
            return (
              <article key={event.name + index} className={s.event}>
                <span className={s.eventSun} aria-hidden />
                <p className={s.eventNo}>{String(index + 1).padStart(2, "0")}</p>
                <h3>{event.name}</h3>
                <p className={s.eventDate}><Icon d={icons.calendar} size={14} />{formatDate(event.date || data.date)}</p>
                {event.time && <p className={s.eventDate}><Icon d={icons.clock} size={14} />{event.time}</p>}
                <hr />
                <strong>{event.venue}</strong>
                {event.address && <p className={s.addr}>{event.address}</p>}
                {maps && <a className={s.ghostBtn} href={maps} target="_blank" rel="noreferrer"><Icon d={icons.mapPin} size={15} />Petunjuk Lokasi</a>}
              </article>
            );
          })}
        </section>

        <Extras slot="event" />

        {stories.length > 0 && (
          <section className={`${s.section} ${s.story}`} aria-labelledby="ps-story">
            <Head id="ps-story" kicker="Jejak di pasir" title="Kisah Kami" />
            <ol className={s.shore}>
              {stories.map((story, index) => (
                <li key={index}>
                  <span className={s.shell} aria-hidden><Shell size={26} /></span>
                  <div>
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

        {feature && (
          <section className={`${s.section} ${s.gallery}`} aria-labelledby="ps-gallery">
            <Head id="ps-gallery" kicker="Potret senja" title="Galeri" />
            <div className={s.feature}><Photo src={feature} alt="Foto galeri 1" /></div>
            {rest.length > 0 && (
              <div className={s.grid}>
                {rest.map((src, index) => <div key={src + index} className={s.tile}><Photo src={src} alt={`Foto galeri ${index + 2}`} /></div>)}
              </div>
            )}
          </section>
        )}

        <Extras slot="story" />

        <section className={`${s.section} ${s.wishes}`} aria-labelledby="ps-wishes">
          <Head id="ps-wishes" kicker={rsvpClosed ? "Kirim doa" : "RSVP & ucapan"} title="Konfirmasi Kehadiran" />
          {sent ? (
            <div ref={sentRef} className={`${s.form} ${s.sentBox}`} role="status">
              <span className={s.sentBadge} aria-hidden><Icon d={icons.check} size={22} strokeWidth={2.6} /></span>
              <strong>Terima kasih!</strong>
              <p>{demo ? "Ini pratinjau — ucapanmu hanya tampil di daftar." : sentSummary(rsvp, wishes)}</p>
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
              if (!rsvpClosed && rsvp.status !== "sent") void rsvp.submit({ name, attendance, guests, message, diet: String(form.get("diet") ?? "").trim() || undefined });
            }}>
              <label className={s.field}><span>Nama</span><input name="name" required maxLength={100} defaultValue={plainName(data.guestName)} placeholder="Nama Anda" autoComplete="name" /></label>
              {rsvpClosed ? (
                <div className={s.closed} role="status"><strong>Konfirmasi kehadiran sudah ditutup</strong><p>Terima kasih atas doa dan perhatiannya. Ucapan &amp; doa masih bisa dikirim lewat form ini.</p></div>
              ) : (
                <div className={s.choices} role="radiogroup" aria-label="Kehadiran">
                  {(["yes", "maybe", "no"] as Attendance[]).map(value => (
                    <button key={value} type="button" role="radio" aria-checked={attendance === value} className={attendance === value ? s.choiceOn : undefined} onClick={() => setAttendance(value)}>{ATTEND[value]}</button>
                  ))}
                </div>
              )}
              {!rsvpClosed && attendance !== "no" && <GuestCount className={s.guests} buttonClassName={s.step} />}
              {!rsvpClosed && attendance !== "no" && <DietaryField className={s.field} />}
              <label className={s.field}><span>Ucapan &amp; doa</span><textarea name="message" required maxLength={500} rows={3} placeholder="Tuliskan doa terbaik untuk kami…" /></label>
              {wishes.status === "error" && <p className={s.error} role="alert">Belum terkirim. Coba lagi sebentar lagi.</p>}
              <button type="submit" className={s.submit} disabled={wishes.status === "sending"}>{wishes.status === "sending" ? "Mengirim…" : "Kirim"}</button>
            </form>
          )}
          <div className={s.wishList}>
            {wishes.wishes.length === 0 && <p className={s.empty}>Belum ada ucapan. Jadilah yang pertama mendoakan.</p>}
            {wishes.wishes.slice(0, 12).map(wish => (
              <article key={wish.id} className={s.wish}>
                <div><strong>{wish.name}</strong>{wish.attendance && <small>{ATTEND[wish.attendance]}</small>}</div>
                <p>{wish.message}</p>
              </article>
            ))}
          </div>
        </section>

        {data.gifts.length > 0 && (
          <section className={`${s.section} ${s.gifts}`} aria-labelledby="ps-gifts">
            <Head id="ps-gifts" kicker="Tanda kasih" title="Amplop Digital" />
            <p className={s.body}>Doa restu Anda adalah hadiah terindah. Bila ingin berbagi tanda kasih, dapat melalui:</p>
            {data.gifts.map(gift => {
              const info = giftInfo(gift);
              const on = Boolean(info.copy) && copied === info.copy;
              const icon = gift.type === "bank" ? bank : gift.type === "address" ? icons.gift : wallet;
              return (
                <div key={gift.id} className={on ? `${s.gift} ${s.giftOn}` : s.gift}>
                  <span className={s.giftIcon}><Icon d={icon} size={20} /></span>
                  <div className={s.giftText}>
                    <small>{info.kind}</small>
                    <h3>{info.title}</h3>
                    {info.number && <strong>{info.number}</strong>}
                    {info.holder && <p>a.n. {info.holder}</p>}
                    {info.image && <Photo src={info.image} alt="Kode QRIS" className={s.qris} />}
                  </div>
                  {info.copy && (
                    <button type="button" className={on ? `${s.copy} ${s.copyOn}` : s.copy} onClick={() => copy(info.copy)} aria-label={on ? "Tersalin" : `Salin ${info.title}`}>
                      <Icon key={on ? "on" : "off"} d={on ? icons.check : icons.copy} size={15} />{on ? "Tersalin" : "Salin"}
                    </button>
                  )}
                </div>
              );
            })}
          </section>
        )}

        <Extras slot="end" />

        <footer className={s.closing}>
          <Art src="moon" className={s.moon} width={90} height={90} />
          <span className={s.stars} aria-hidden />
          <p className={s.kickerLight}>Sampai jumpa di tepi pantai</p>
          <p className={s.thanks}>Terima kasih</p>
          <p className={s.closingText}>{thanks.active ? thanks.message : "Merupakan kebahagiaan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu."}</p>
          <p className={s.family}><small>Kami yang berbahagia</small>{couple}{families.length > 0 && <span>Keluarga {families.join(" & ")}</span>}</p>
          <Waves className={`${s.wave} ${s.closingWave}`} />
          <a href="/" target="_blank" rel="noreferrer" className={s.made}>dibuat dengan ♥ di Rawuh</a>
        </footer>
      </main>
    </ThemeShell>
  );
}
