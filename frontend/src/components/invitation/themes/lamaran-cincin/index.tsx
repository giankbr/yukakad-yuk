"use client";
// Theme "Lamaran Cincin" — lamaran & tunangan bernuansa champagne: cincin bertaut yang tergambar sendiri, kilau berlian, bunga baby's breath.
import { useEffect, useRef, useState } from "react";
import {
  DATE_TBA, DietaryField, Extras, GuestCount, Icon, Photo, ThemeShell, Tick, coupleLabel, dateParts, formatDate, giftInfo, guestLabel, icons,
  mapsHref, sentSummary, storyItems, useCopy, useCountdown, useRsvp, useThankYou, useWishes, type Attendance, type ThemeProps, type Wish,
} from "../kit";
import { tableLabel } from "../extras";
import { celebrate } from "@/lib/celebrate";
import s from "./styles.module.css";

const FONTS = ["Cormorant Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500;1,600", "Figtree:wght@400;500;600;700", "Amiri"];
const ATTEND: Record<Attendance, string> = { yes: "Hadir", maybe: "Ragu", no: "Berhalangan" };
const DEMO_WISHES: Wish[] = [
  { id: "w1", name: "Tante Yuni", attendance: "yes", message: "Barakallah Nadhira & Arkan. Semoga dimudahkan sampai hari akad, dan dilimpahi keberkahan selalu." },
  { id: "w2", name: "Salma (teman kuliah)", attendance: "maybe", message: "Akhirnya! Ikut bahagia, semoga lancar semua persiapannya." },
];
const wallet = ["M19 7V4a1 1 0 0 0-1-1H5a2 2 0 0 0 0 4h15a1 1 0 0 1 1 1v4h-3a2 2 0 0 0 0 4h3a1 1 0 0 0 1-1v-2a1 1 0 0 0-1-1", "M3 5v14a2 2 0 0 0 2 2h15a1 1 0 0 0 1-1v-4"];
const bank = ["M3 22h18", "M6 18v-7", "M10 18v-7", "M14 18v-7", "M18 18v-7", "M12 2l8 5H4z"];

const round = (n: number) => Math.round(n * 100) / 100;

/** Two interlocking rings with a solitaire; strokes draw themselves in. */
function Rings({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 120 92" aria-hidden="true" focusable="false" fill="none" strokeLinecap="round" strokeLinejoin="round">
      <circle className={s.draw} cx="46" cy="56" r="28" stroke="currentColor" strokeWidth="3.2" pathLength={1} />
      <circle className={`${s.draw} ${s.drawLate}`} cx="74" cy="56" r="28" stroke="currentColor" strokeWidth="3.2" pathLength={1} />
      <path className={s.gem} d="M38 22 L46 12 L54 22 L46 31 Z M38 22 H54 M42 22 L46 31 L50 22 M42 22 L46 12 L50 22" stroke="currentColor" strokeWidth="1.4" fill="rgba(255,255,255,.55)" />
      <g className={s.spark} stroke="currentColor" strokeWidth="1.2"><path d="M64 8 v8 M60 12 h8" /><path d="M24 18 v6 M21 21 h6" /></g>
    </svg>
  );
}

/** Baby's breath / small blossom sprig. */
function Sprig({ className }: { className?: string }) {
  const bloom = (x: number, y: number, r = 3.2) => (
    <g key={`${x}-${y}`} transform={`translate(${x} ${y})`}>
      {[0, 72, 144, 216, 288].map(a => <circle key={a} cx={round(Math.cos((a * Math.PI) / 180) * r)} cy={round(Math.sin((a * Math.PI) / 180) * r)} r={r * 0.75} />)}
      <circle r={r * 0.5} className={s.bloomEye} />
    </g>
  );
  return (
    <svg className={className} viewBox="0 0 120 140" aria-hidden="true" focusable="false">
      <g fill="none" stroke="currentColor" strokeWidth="1.2" strokeLinecap="round" opacity=".75">
        <path d="M10 136 C 32 104 48 72 86 22" /><path d="M40 92 C 30 76 22 66 12 58" /><path d="M56 70 C 70 64 84 62 104 64" /><path d="M70 50 C 64 38 62 26 64 12" />
      </g>
      <g className={s.leaves} opacity=".55">
        <ellipse cx="28" cy="110" rx="9" ry="3.4" transform="rotate(-50 28 110)" /><ellipse cx="52" cy="80" rx="9" ry="3.4" transform="rotate(30 52 80)" /><ellipse cx="80" cy="34" rx="8" ry="3" transform="rotate(-40 80 34)" />
      </g>
      <g className={s.blooms}>{[bloom(86, 22, 4), bloom(12, 58), bloom(104, 64, 3.6), bloom(64, 12), bloom(96, 46, 2.6), bloom(20, 76, 2.6), bloom(74, 66, 2.4)]}</g>
    </svg>
  );
}

function Diamond() {
  return <svg className={s.diamond} viewBox="0 0 16 16" aria-hidden="true" focusable="false"><path d="M8 1 L15 8 L8 15 L1 8 Z" /></svg>;
}

function Head({ id, kicker, title }: { id: string; kicker?: string; title: string }) {
  return (
    <div className={s.head}>
      {kicker && <p className={s.kicker}>{kicker}</p>}
      <h2 id={id}>{title}</h2>
      <span className={s.divider} aria-hidden><i /><Diamond /><i /></span>
    </div>
  );
}

function plainName(guest?: string) {
  if (!guest || guest === "Tamu Undangan") return "";
  return guest.replace(/^(bapak|ibu|bpk\.?|sdr\.?|saudara|saudari)\s+/i, "").replace(/\s*(&|dan)\s*keluarga$/i, "").trim();
}

function fatherOf(parents?: string) {
  const match = /((?:Bapak|Bpk\.?)\s+[^&\n,]+)/i.exec(parents ?? "");
  return match?.[1].trim();
}

export default function LamaranCincinTheme({ data, slug, guestToken, demo, skipCover }: ThemeProps) {
  const couple = coupleLabel(data);
  const label = data.eventLabel ?? "Lamaran";
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
  const photos = data.gallery.length > 1 ? data.gallery.slice(1) : data.gallery;
  const table = tableLabel(data.guestTable);
  const families = [fatherOf(data.couple.brideParents), fatherOf(data.couple.groomParents)].filter(Boolean);
  const ringEvent = data.events.find(event => /cincin|ring/i.test(event.name)) ?? data.events[data.events.length - 1];
  const sentRef = useRef<HTMLDivElement>(null);
  const sent = wishes.status === "sent";
  useEffect(() => { if (sent) celebrate(sentRef.current); }, [sent]);
  const people = [
    { role: "Calon mempelai wanita", nick: data.couple.bride, name: data.couple.brideFull || data.couple.bride, parents: data.couple.brideParents, photo: data.couple.bridePhoto },
    { role: "Calon mempelai pria", nick: data.couple.groom, name: data.couple.groomFull || data.couple.groom, parents: data.couple.groomParents, photo: data.couple.groomPhoto },
  ];
  const dateLine = parts.day ? `${parts.weekday}, ${parts.day} ${parts.month} ${parts.year}` : DATE_TBA;

  return (
    <ThemeShell
      fonts={FONTS}
      background="#efe4d5"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <span className={s.glowA} aria-hidden />
          <span className={s.glowB} aria-hidden />
          <Sprig className={`${s.sprig} ${s.sprigTL}`} />
          <Sprig className={`${s.sprig} ${s.sprigBR}`} />
          <div className={s.coverInner}>
            <Rings className={s.coverRings} />
            <p className={s.kicker}>Undangan {label}</p>
            <h1 className={s.coverNames}><span>{data.couple.bride}</span><em>&amp;</em><span>{data.couple.groom}</span></h1>
            <p className={s.coverDate}>{dateLine}</p>
          </div>
          <div className={s.guest}>
            <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
            <strong>{guestLabel(data)}</strong>
            {table && <span>{table}</span>}
          </div>
          <button type="button" className={s.openBtn} onClick={open}><Icon d={icons.mailOpen} size={16} />Buka Undangan</button>
        </section>
      )}
    >
      <main className={s.main}>
        <header className={s.hero}>
          <Sprig className={`${s.sprig} ${s.heroSprig}`} />
          <p className={s.kicker}>{label} · {parts.year || "segera"}</p>
          <div className={s.oval}><Photo src={hero} alt={`Foto ${couple}`} /></div>
          <h1 className={s.heroNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
          <p className={s.heroDate}>{dateLine}</p>
        </header>

        <section className={`${s.section} ${s.opening}`} aria-label="Salam pembuka">
          <p className={s.arabic} lang="ar" dir="rtl">بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ</p>
          <p className={s.salam}>Assalamu&apos;alaikum warahmatullahi wabarakatuh</p>
          <p className={s.body}>Dengan memohon rahmat dan ridha Allah SWT, kami bermaksud menyelenggarakan acara {label.toLowerCase()} dan tukar cincin putra-putri kami. Merupakan kehormatan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.</p>
        </section>

        <Extras slot="opening" />

        <section className={`${s.section} ${s.families}`} aria-labelledby="lc-family">
          <Head id="lc-family" kicker="Dua keluarga, satu niat baik" title="Yang Berbahagia" />
          <div className={s.pair}>
            {people.map((person, index) => (
              <article key={index} className={s.person}>
                <div className={s.locket}>
                  {person.photo ? <Photo src={person.photo} alt={person.name} /> : <span className={s.mono} aria-hidden>{person.nick.slice(0, 1)}</span>}
                </div>
                <small>{person.role}</small>
                <h3>{person.name}</h3>
                {person.parents && <p>{person.parents}</p>}
              </article>
            ))}
            <span className={s.pairRings} aria-hidden><Rings /></span>
          </div>
        </section>

        {ringEvent && (
          <section className={`${s.section} ${s.exchange}`} aria-labelledby="lc-ring">
            <Rings className={s.exchangeRings} />
            <p className={s.kicker}>Momen utama</p>
            <h2 id="lc-ring" className={s.exchangeTitle}>Tukar Cincin</h2>
            <p className={s.body}>Sebuah janji yang disematkan di jari manis, disaksikan kedua keluarga, sebagai tanda ikatan menuju pernikahan.</p>
            <p className={s.exchangeWhen}>{formatDate(ringEvent.date || data.date)}{ringEvent.time ? ` · ${ringEvent.time}` : ""}</p>
          </section>
        )}

        <section className={`${s.section} ${s.countWrap}`} aria-labelledby="lc-count">
          <Head id="lc-count" kicker="Menuju hari baik" title="Hitung Mundur" />
          {countdown.valid ? (
            <div className={s.count} role="timer" aria-label={`${countdown.days} hari ${countdown.hours} jam ${countdown.minutes} menit lagi`}>
              {[[countdown.days, "Hari"], [countdown.hours, "Jam"], [countdown.minutes, "Menit"], [countdown.seconds, "Detik"]].map(([value, unit]) => (
                <div key={unit}><b><Tick value={value} /></b><small>{unit}</small></div>
              ))}
            </div>
          ) : <p className={s.tba}>{DATE_TBA}</p>}
        </section>

        <section className={`${s.section} ${s.events}`} aria-labelledby="lc-events">
          <Head id="lc-events" kicker="Waktu & tempat" title="Rangkaian Acara" />
          {data.events.map((event, index) => {
            const maps = mapsHref(data, event);
            return (
              <article key={event.name + index} className={s.box}>
                <div className={s.lid}><Diamond /><h3>{event.name}</h3></div>
                <div className={s.boxBody}>
                  <p className={s.when}>{formatDate(event.date || data.date)}</p>
                  {event.time && <p className={s.time}><Icon d={icons.clock} size={14} />{event.time}</p>}
                  <strong>{event.venue}</strong>
                  {event.address && <p className={s.addr}>{event.address}</p>}
                  {maps && <a className={s.ghostBtn} href={maps} target="_blank" rel="noreferrer"><Icon d={icons.mapPin} size={15} />Lihat Lokasi</a>}
                </div>
              </article>
            );
          })}
        </section>

        <Extras slot="event" />

        {stories.length > 0 && (
          <section className={`${s.section} ${s.story}`} aria-labelledby="lc-story">
            <Head id="lc-story" kicker="Sampai di titik ini" title="Perjalanan Kami" />
            <ol className={s.timeline}>
              {stories.map((story, index) => (
                <li key={index}>
                  <span className={s.node} aria-hidden><Diamond /></span>
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

        {photos.length > 0 && (
          <section className={`${s.section} ${s.gallery}`} aria-labelledby="lc-gallery">
            <Head id="lc-gallery" kicker="Kenangan" title="Galeri" />
            <div className={s.grid}>
              {photos.map((src, index) => <div key={src + index} className={s.tile}><Photo src={src} alt={`Foto galeri ${index + 1}`} /></div>)}
            </div>
          </section>
        )}

        <Extras slot="story" />

        <section className={`${s.section} ${s.wishes}`} aria-labelledby="lc-wishes">
          <Head id="lc-wishes" kicker={rsvpClosed ? "Doa & ucapan" : "Mohon konfirmasi"} title="Kehadiran & Doa" />
          {sent ? (
            <div ref={sentRef} className={`${s.form} ${s.sentBox}`} role="status">
              <Rings className={s.sentRings} />
              <strong>Jazakumullah khairan</strong>
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
              <label className={s.field}><span>Doa &amp; ucapan</span><textarea name="message" required maxLength={500} rows={3} placeholder="Tuliskan doa terbaik…" /></label>
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
          <section className={`${s.section} ${s.gifts}`} aria-labelledby="lc-gifts">
            <Head id="lc-gifts" kicker="Tanda kasih" title="Hadiah" />
            <p className={s.body}>Doa restu Anda adalah hadiah yang paling berharga. Namun bila berkenan memberi tanda kasih:</p>
            {data.gifts.map(gift => {
              const info = giftInfo(gift);
              const on = Boolean(info.copy) && copied === info.copy;
              const icon = gift.type === "bank" ? bank : gift.type === "address" ? icons.gift : wallet;
              return (
                <div key={gift.id} className={on ? `${s.gift} ${s.giftOn}` : s.gift}>
                  <span className={s.giftIcon}><Icon d={icon} size={19} /></span>
                  <div className={s.giftText}>
                    <small>{info.kind}</small>
                    <h3>{info.title}</h3>
                    {info.number && <strong>{info.number}</strong>}
                    {info.holder && <p>a.n. {info.holder}</p>}
                    {info.image && <Photo src={info.image} alt="Kode QRIS" className={s.qris} />}
                  </div>
                  {info.copy && (
                    <button type="button" className={on ? `${s.copy} ${s.copyOn}` : s.copy} onClick={() => copy(info.copy)} aria-label={on ? "Tersalin" : `Salin ${info.title}`}>
                      <Icon key={on ? "on" : "off"} d={on ? icons.check : icons.copy} size={14} />{on ? "Tersalin" : "Salin"}
                    </button>
                  )}
                </div>
              );
            })}
          </section>
        )}

        <Extras slot="end" />

        <footer className={s.closing}>
          <Sprig className={`${s.sprig} ${s.closingSprig}`} />
          <p className={s.kicker}>Wassalamu&apos;alaikum warahmatullahi wabarakatuh</p>
          <p className={s.thanks}>Terima Kasih</p>
          <p className={s.body}>{thanks.active ? thanks.message : "Atas kehadiran dan doa restunya, kami ucapkan terima kasih. Semoga Allah memudahkan langkah kami hingga hari akad."}</p>
          <p className={s.family}><small>Kami yang berbahagia</small>{families.length > 0 ? `Keluarga ${families.join(" & ")}` : couple}</p>
          <a href="/" target="_blank" rel="noreferrer" className={s.made}>dibuat dengan ♥ di Rawuh</a>
        </footer>
      </main>
    </ThemeShell>
  );
}
