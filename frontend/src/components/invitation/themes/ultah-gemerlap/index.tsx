"use client";
// Theme "Ultah Gemerlap" — pesta ulang tahun dewasa bernuansa malam & emas: angka foil berkilau, hujan glitter, kue dengan lilin yang bisa ditiup.
import { useEffect, useRef, useState, type CSSProperties } from "react";
import {
  DATE_TBA, DietaryField, Extras, GuestCount, Icon, Photo, ThemeShell, Tick, dateParts, formatDate, giftInfo, guestLabel, icons,
  mapsHref, sentSummary, storyItems, toDate, useCopy, useCountdown, useRsvp, useThankYou, useWishes, type Attendance, type ThemeProps, type Wish,
} from "../kit";
import type { InvitationData } from "../../types";
import { tableLabel } from "../extras";
import { celebrate, toast } from "@/lib/celebrate";
import s from "./styles.module.css";

const FONTS = ["Playfair Display:ital,wght@0,500;0,600;0,700;0,800;1,500;1,600", "Cinzel:wght@500;600;700", "DM Sans:wght@400;500;600;700"];
const ATTEND: Record<Attendance, string> = { yes: "Hadir", maybe: "Ragu", no: "Berhalangan" };
const DEMO_WISHES: Wish[] = [
  { id: "w1", name: "Tasya", attendance: "yes", message: "Happy 30th, Nad! Makin bersinar, makin bahagia. Sampai ketemu di rooftop!" },
  { id: "w2", name: "Mas Dimas", attendance: "yes", message: "Selamat ulang tahun! Semoga sehat, rezeki lancar, dan semua mimpinya tercapai satu per satu." },
];
const wallet = ["M19 7V4a1 1 0 0 0-1-1H5a2 2 0 0 0 0 4h15a1 1 0 0 1 1 1v4h-3a2 2 0 0 0 0 4h3a1 1 0 0 0 1-1v-2a1 1 0 0 0-1-1", "M3 5v14a2 2 0 0 0 2 2h15a1 1 0 0 0 1-1v-4"];
const bank = ["M3 22h18", "M6 18v-7", "M10 18v-7", "M14 18v-7", "M18 18v-7", "M12 2l8 5H4z"];
const sparkles = "M12 3l1.9 5.8L20 10l-6.1 1.2L12 17l-1.9-5.8L4 10l6.1-1.2z";
/** Deterministic glitter flakes: x %, delay s, duration s, size px. */
const FLAKES = [[6, 0, 9, 6], [14, 3.5, 11, 4], [23, 1.2, 8, 5], [31, 5.4, 12, 3], [40, 2.2, 10, 6], [48, 6.8, 9, 4], [57, 0.8, 13, 5], [65, 4.1, 10, 3], [73, 2.9, 8, 6], [81, 7.3, 12, 4], [89, 1.7, 9, 5], [95, 5.9, 11, 3]];

function Glitter({ className }: { className?: string }) {
  return (
    <span className={`${s.glitter} ${className ?? ""}`} aria-hidden>
      {FLAKES.map(([x, delay, dur, size], index) => (
        <i key={index} style={{ "--x": `${x}%`, "--d": `${delay}s`, "--t": `${dur}s`, "--s": `${size}px` } as CSSProperties} />
      ))}
    </span>
  );
}

function Burst({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 100 100" aria-hidden="true" focusable="false" fill="none" stroke="currentColor" strokeLinecap="round">
      {Array.from({ length: 12 }, (_, i) => {
        const a = (i * 30 * Math.PI) / 180;
        const r1 = i % 2 ? 22 : 16;
        const r2 = i % 2 ? 40 : 46;
        return <path key={i} d={`M${(50 + Math.cos(a) * r1).toFixed(2)} ${(50 + Math.sin(a) * r1).toFixed(2)} L${(50 + Math.cos(a) * r2).toFixed(2)} ${(50 + Math.sin(a) * r2).toFixed(2)}`} strokeWidth={i % 2 ? 1.2 : 2} />;
      })}
      <circle cx="50" cy="50" r="3" fill="currentColor" stroke="none" />
    </svg>
  );
}

function Head({ id, kicker, title }: { id: string; kicker?: string; title: string }) {
  return (
    <div className={s.head}>
      {kicker && <p className={s.kicker}>{kicker}</p>}
      <h2 id={id}>{title}</h2>
      <span className={s.stars} aria-hidden><Icon d={sparkles} size={10} fill="currentColor" strokeWidth={0} /><i /><Icon d={sparkles} size={14} fill="currentColor" strokeWidth={0} /><i /><Icon d={sparkles} size={10} fill="currentColor" strokeWidth={0} /></span>
    </div>
  );
}

function plainName(guest?: string) {
  if (!guest || guest === "Tamu Undangan") return "";
  return guest.replace(/^(bapak|ibu|bpk\.?|sdr\.?|saudara|saudari|kak|mas|mbak)\s+/i, "").replace(/\s*(&|dan)\s*(keluarga|partner|pasangan)$/i, "").trim();
}

/** Age on the party day from the birth date, else a number in the event label ("Ulang Tahun ke-30"). */
function ageOf(data: InvitationData) {
  const birth = toDate(data.extras?.child?.birthDate);
  const party = toDate(data.date) ?? new Date();
  if (birth) {
    let age = party.getFullYear() - birth.getFullYear();
    if (party.getMonth() < birth.getMonth() || (party.getMonth() === birth.getMonth() && party.getDate() < birth.getDate())) age -= 1;
    if (age > 0 && age < 130) return String(age);
  }
  return /(\d{1,3})/.exec(data.eventLabel ?? "")?.[1] ?? "";
}

function Cake({ lit }: { lit: boolean }) {
  return (
    <svg className={lit ? s.cake : `${s.cake} ${s.cakeOut}`} viewBox="0 0 160 150" aria-hidden="true" focusable="false">
      <ellipse cx="80" cy="140" rx="70" ry="7" fill="rgba(0,0,0,.35)" />
      <rect x="22" y="92" width="116" height="46" rx="8" fill="#2a2350" stroke="#d9b45a" strokeWidth="1.5" />
      <path d="M22 104 q 9.7 10 19.3 0 t 19.3 0 t 19.3 0 t 19.3 0 t 19.3 0 t 19.3 0" fill="none" stroke="#f3dc9b" strokeWidth="2" />
      <rect x="38" y="60" width="84" height="34" rx="7" fill="#3b3170" stroke="#d9b45a" strokeWidth="1.5" />
      <path d="M38 70 q 7 8 14 0 t 14 0 t 14 0 t 14 0 t 14 0 t 14 0" fill="none" stroke="#f3dc9b" strokeWidth="2" />
      {[124, 92, 60].map((y, i) => <circle key={y} cx={46 + i * 34} cy={y + 30} r="2.4" fill="#f3dc9b" />)}
      {[58, 80, 102].map((x, i) => (
        <g key={x}>
          <rect x={x - 3} y="36" width="6" height="24" rx="2" fill={i === 1 ? "#f3dc9b" : "#e8b4a0"} />
          <path className={s.flame} d={`M${x} 22 C ${x + 5} 28 ${x + 4} 34 ${x} 35 C ${x - 4} 34 ${x - 5} 28 ${x} 22 Z`} fill="#ffcf6b" style={{ animationDelay: `${i * 0.3}s` }} />
          <path className={s.smoke} d={`M${x} 34 c -4 -5 4 -8 0 -14 c -3 -4 3 -7 1 -11`} fill="none" stroke="rgba(243,220,155,.6)" strokeWidth="1.4" strokeLinecap="round" />
        </g>
      ))}
    </svg>
  );
}

export default function UltahGemerlapTheme({ data, slug, guestToken, demo, skipCover }: ThemeProps) {
  const child = data.extras?.child?.enabled === false ? undefined : data.extras?.child;
  const nick = child?.nickname?.trim() || child?.name?.trim() || data.couple.bride;
  const fullName = child?.name?.trim() || data.couple.brideFull || data.couple.bride;
  const parents = child?.parents?.trim() || data.couple.brideParents;
  const photo = child?.photo || data.couple.bridePhoto;
  const partner = data.couple.groom?.trim() && data.couple.groom.trim() !== nick ? data.couple.groom.trim() : "";
  const age = ageOf(data);
  const birth = child?.birthDate ? formatDate(child.birthDate, { day: "numeric", month: "long", year: "numeric" }) : "";
  const parts = dateParts(data.date);
  const countdown = useCountdown(data.date);
  const rsvp = useRsvp({ slug, guestToken, demo });
  const wishes = useWishes({ slug, guestToken, demo, seed: DEMO_WISHES });
  const thanks = useThankYou();
  const rsvpClosed = thanks.active || rsvp.status === "closed";
  const { copy, copied } = useCopy();
  const [attendance, setAttendance] = useState<Attendance>("yes");
  const [lit, setLit] = useState(true);
  const cakeRef = useRef<HTMLDivElement>(null);
  const stories = storyItems(data);
  const table = tableLabel(data.guestTable);
  const sentRef = useRef<HTMLDivElement>(null);
  const sent = wishes.status === "sent";
  useEffect(() => { if (sent) celebrate(sentRef.current); }, [sent]);
  const dateLine = parts.day ? `${parts.weekday}, ${parts.day} ${parts.month} ${parts.year}` : DATE_TBA;
  const blow = () => {
    if (lit) { celebrate(cakeRef.current); toast("Semoga semua harapannya terkabul!"); }
    setLit(value => !value);
  };

  return (
    <ThemeShell
      fonts={FONTS}
      background="#07060f"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <span className={s.spot} aria-hidden />
          <Glitter />
          <Burst className={`${s.burst} ${s.burstA}`} />
          <Burst className={`${s.burst} ${s.burstB}`} />
          <div className={s.coverTop}>
            <p className={s.kicker}>Undangan Pesta Ulang Tahun</p>
            {age ? <p className={s.foil} aria-label={`ke-${age}`}>{age}</p> : <Burst className={s.foilBurst} />}
            <h1 className={s.coverName}>{nick}</h1>
            <p className={s.coverDate}>{dateLine}</p>
            <p className={s.coverTag}><i />Malam penuh kilau<i /></p>
          </div>
          <div className={s.coverBottom}>
            <div className={s.pass}>
              <small>Kepada Yth.</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Icon d={sparkles} size={15} fill="currentColor" strokeWidth={0} />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <main className={s.main}>
        <header className={s.hero}>
          <span className={s.spot} aria-hidden />
          <Glitter />
          <p className={s.kicker}>{age ? `Ulang tahun ke-${age}` : "Pesta ulang tahun"}</p>
          <div className={s.disco}>
            {photo ? <Photo src={photo} alt={`Foto ${nick}`} /> : <span className={s.mono} aria-hidden>{nick.slice(0, 1)}</span>}
            {age && <span className={s.ageBadge}><small>ke-</small>{age}</span>}
          </div>
          <h1 className={s.heroName}>{nick}</h1>
          <p className={s.heroDate}>{dateLine}</p>
        </header>

        <section className={`${s.section} ${s.opening}`} aria-label="Pembuka">
          <p className={s.hello}>Halo, teman-teman tersayang!</p>
          <p className={s.lead}>{data.couple.note || "Satu tahun lagi telah berlalu. Mari rayakan bersama malam ini."}</p>
          <p className={s.body}>Dengan penuh syukur, {nick} mengundangmu untuk merayakan {age ? `ulang tahun ke-${age}` : "hari ulang tahunnya"} dalam malam yang hangat, penuh tawa, dan sedikit gemerlap.</p>
        </section>

        <Extras slot="opening" without={["child"]} />

        <section className={`${s.section} ${s.star}`} aria-labelledby="ug-star">
          <Head id="ug-star" kicker="Bintang malam ini" title={fullName} />
          <div className={s.profile}>
            {birth && <p><small>Lahir</small>{birth}</p>}
            {age && <p className={birth ? undefined : s.wide}><small>Usia baru</small>{age} tahun</p>}
            {parents && <p className={s.wide}><small>Keluarga</small>{parents}</p>}
            {partner && <p className={s.wide}><small>Bersama</small>{partner}</p>}
          </div>
        </section>

        <section className={`${s.section} ${s.countWrap}`} aria-labelledby="ug-count">
          <Head id="ug-count" kicker="Pesta dimulai dalam" title="Hitung Mundur" />
          {countdown.valid ? (
            <div className={s.count} role="timer" aria-label={`${countdown.days} hari ${countdown.hours} jam ${countdown.minutes} menit lagi`}>
              {[[countdown.days, "Hari"], [countdown.hours, "Jam"], [countdown.minutes, "Menit"], [countdown.seconds, "Detik"]].map(([value, unit]) => (
                <div key={unit}><b><Tick value={value} /></b><small>{unit}</small></div>
              ))}
            </div>
          ) : <p className={s.tba}>{DATE_TBA}</p>}
        </section>

        <section className={`${s.section} ${s.events}`} aria-labelledby="ug-events">
          <Head id="ug-events" kicker="Catat tanggalnya" title="Detail Pesta" />
          {data.events.map((event, index) => {
            const maps = mapsHref(data, event);
            const p = dateParts(event.date || data.date);
            return (
              <article key={event.name + index} className={s.ticket}>
                <div className={s.stub}>
                  <b>{p.day || "—"}</b>
                  <small>{p.monthShort || "TBA"}</small>
                  <span>{p.weekdayShort}</span>
                </div>
                <div className={s.ticketBody}>
                  <p className={s.admit}>Admit one · {String(index + 1).padStart(2, "0")}</p>
                  <h3>{event.name}</h3>
                  <p className={s.meta}><Icon d={icons.calendar} size={13} />{formatDate(event.date || data.date)}</p>
                  {event.time && <p className={s.meta}><Icon d={icons.clock} size={13} />{event.time}</p>}
                  <strong>{event.venue}</strong>
                  {event.address && <p className={s.addr}>{event.address}</p>}
                  {maps && <a className={s.ghostBtn} href={maps} target="_blank" rel="noreferrer"><Icon d={icons.mapPin} size={14} />Lihat Lokasi</a>}
                </div>
              </article>
            );
          })}
        </section>

        <Extras slot="event" />

        <section className={`${s.section} ${s.wish}`} aria-labelledby="ug-wish">
          <Head id="ug-wish" kicker="Make a wish" title="Tiup Lilinnya" />
          <div ref={cakeRef} className={s.cakeWrap}><Cake lit={lit} /></div>
          <p className={s.body}>{lit ? `Ketuk tombol di bawah dan titipkan satu harapan untuk ${nick}.` : "Lilin sudah ditiup. Semoga semua harapan baik terkabul!"}</p>
          <button type="button" className={s.blowBtn} onClick={blow} aria-pressed={!lit}>{lit ? "Tiup lilin" : "Nyalakan lagi"}</button>
        </section>

        {stories.length > 0 && (
          <section className={`${s.section} ${s.story}`} aria-labelledby="ug-story">
            <Head id="ug-story" kicker="Kilas balik" title={age ? `${age} Tahun Bersinar` : "Perjalanan"} />
            <ol className={s.milestones}>
              {stories.map((story, index) => (
                <li key={index}>
                  <span className={s.year}>{story.date ?? String(index + 1).padStart(2, "0")}</span>
                  <div>
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
          <section className={`${s.section} ${s.gallery}`} aria-labelledby="ug-gallery">
            <Head id="ug-gallery" kicker="Momen" title="Galeri" />
            <div className={s.polaroids}>
              {data.gallery.map((src, index) => (
                <figure key={src + index} className={s.polaroid}>
                  <Photo src={src} alt={`Foto galeri ${index + 1}`} />
                </figure>
              ))}
            </div>
          </section>
        )}

        <Extras slot="story" />

        <section className={`${s.section} ${s.rsvp}`} aria-labelledby="ug-rsvp">
          <Head id="ug-rsvp" kicker={rsvpClosed ? "Kirim ucapan" : "RSVP"} title="Kamu Datang?" />
          {sent ? (
            <div ref={sentRef} className={`${s.form} ${s.sentBox}`} role="status">
              <span className={s.sentBadge} aria-hidden><Icon d={icons.check} size={22} strokeWidth={2.6} /></span>
              <strong>Yeay, terkirim!</strong>
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
              <label className={s.field}><span>Nama</span><input name="name" required maxLength={100} defaultValue={plainName(data.guestName)} placeholder="Nama kamu" autoComplete="name" /></label>
              {rsvpClosed ? (
                <div className={s.closed} role="status"><strong>Konfirmasi kehadiran sudah ditutup</strong><p>Terima kasih sudah ikut merayakan. Ucapan masih bisa dikirim lewat form ini.</p></div>
              ) : (
                <div className={s.choices} role="radiogroup" aria-label="Kehadiran">
                  {(["yes", "maybe", "no"] as Attendance[]).map(value => (
                    <button key={value} type="button" role="radio" aria-checked={attendance === value} className={attendance === value ? s.choiceOn : undefined} onClick={() => setAttendance(value)}>{ATTEND[value]}</button>
                  ))}
                </div>
              )}
              {!rsvpClosed && attendance !== "no" && <GuestCount className={s.guests} buttonClassName={s.step} />}
              {!rsvpClosed && attendance !== "no" && <DietaryField className={s.field} />}
              <label className={s.field}><span>Ucapan</span><textarea name="message" required maxLength={500} rows={3} placeholder={`Tulis ucapan untuk ${nick}…`} /></label>
              {wishes.status === "error" && <p className={s.error} role="alert">Belum terkirim. Coba lagi sebentar lagi.</p>}
              <button type="submit" className={s.submit} disabled={wishes.status === "sending"}>{wishes.status === "sending" ? "Mengirim…" : "Kirim"}</button>
            </form>
          )}
          <div className={s.wishList}>
            {wishes.wishes.length === 0 && <p className={s.empty}>Belum ada ucapan. Jadilah yang pertama!</p>}
            {wishes.wishes.slice(0, 12).map(wish => (
              <article key={wish.id} className={s.note}>
                <div><strong>{wish.name}</strong>{wish.attendance && <small>{ATTEND[wish.attendance]}</small>}</div>
                <p>{wish.message}</p>
              </article>
            ))}
          </div>
        </section>

        {data.gifts.length > 0 && (
          <section className={`${s.section} ${s.gifts}`} aria-labelledby="ug-gifts">
            <Head id="ug-gifts" kicker="Kado" title="Kirim Hadiah" />
            <p className={s.body}>Kehadiranmu sudah jadi kado terbaik. Kalau ingin mengirim hadiah, bisa lewat:</p>
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
          <Glitter />
          <Burst className={`${s.burst} ${s.burstC}`} />
          <p className={s.kicker}>Sampai jumpa di pesta</p>
          <p className={s.thanks}>Terima kasih!</p>
          <p className={s.body}>{thanks.active ? thanks.message : "Kehadiran dan doamu akan membuat malam ini jauh lebih bersinar."}</p>
          <p className={s.sign}><small>Dengan sayang</small>{nick}{parents ? <span>{parents}</span> : null}</p>
          <a href="/" target="_blank" rel="noreferrer" className={s.made}>dibuat dengan ♥ di Rawuh</a>
        </footer>
      </main>
    </ThemeShell>
  );
}
