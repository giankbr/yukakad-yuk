"use client";
// Theme "Jawa Keraton" — adat Jawa klasik cokelat-emas dengan gunungan (design: Undangan — Tema Jawa (Laksmi & Bayu)).
import { useCallback, useEffect, useRef, useState } from "react";
import {
  Lucide, Photo, RsvpForm, Sheet, ThemeShell, coupleLabel, dateParts, formatDate, giftInfo, guestLabel, mapsHref, storyItems,
  toDate, useCopy, useCountdown, useRsvp, useSheets, useWishes, type Attendance, type ThemeProps, type ThemeTint,
} from "../kit";
import type { InvitationData } from "../../types";
import { gunungan, ic } from "./icons";
import s from "./styles.module.css";

const FONTS = ["Cinzel:wght@400;600;700", "Cormorant Garamond:ital,wght@0,400;0,500;0,600;0,700;1,400;1,500;1,600"];
const tint: ThemeTint = {
  "--t-accent": "#2b1a10", "--t-accent-ink": "#e6c77a", "--t-bg": "#f5eddc", "--t-ink": "#3a2618", "--t-muted": "#7a5e48",
  "--t-line": "#d9c7a3", "--t-field": "#ffffff", "--t-radius": "6px", "--t-font": "'Cormorant Garamond', Georgia, serif",
};
const DEMO_WISHES = [
  { id: "w1", name: "Rini Handayani", attendance: "yes" as Attendance, message: "Selamat menempuh bahtera rumah tangga. Semoga selalu rukun, tenteram, dan dijauhkan dari marabahaya." },
  { id: "w2", name: "Pakdhe Darmo", attendance: "yes" as Attendance, message: "Semoga menjadi keluarga yang sakinah, mawaddah, warahmah. Amin." },
];
const ATTEND: Record<Attendance, string> = { yes: "Hadir", maybe: "Ragu", no: "Berhalangan" };
const pad = (n: number) => String(n).padStart(2, "0");

function Divider({ light }: { light?: boolean }) {
  return <span className={light ? `${s.divider} ${s.dividerLight}` : s.divider} aria-hidden><i /><b /><i /></span>;
}

function Head({ id, title, light }: { id: string; title: string; light?: boolean }) {
  return (
    <div className={s.head}>
      <h2 id={id} className={light ? s.titleLight : undefined}>{title}</h2>
      <Divider light={light} />
    </div>
  );
}

function city(address: string) {
  const parts = address.split(",").map(part => part.trim()).filter(Boolean);
  return parts.length > 1 ? parts[parts.length - 1] : "";
}

/** "Bapak R. Soetomo & Ibu Sri" → "R. Soetomo" */
function father(parents?: string) {
  const match = /(?:Bapak|Bpk\.?)\s+([^&\n]+?)\s*(?:&|\n|$)/i.exec(parents ?? "");
  return match?.[1].trim();
}

/** "Bapak Hendro Wibowo & Keluarga" → "Hendro Wibowo" (prefill for the wish form). */
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

/** Soft gamelan-like chimes (slendro-ish scale) generated with WebAudio — no audio file needed. */
function useGamelan() {
  const ctx = useRef<AudioContext | null>(null);
  const timer = useRef<ReturnType<typeof setInterval> | null>(null);
  const [playing, setPlaying] = useState(false);
  const stop = useCallback(() => {
    if (timer.current) clearInterval(timer.current);
    timer.current = null;
    void ctx.current?.suspend();
    setPlaying(false);
  }, []);
  const start = useCallback(() => {
    const AC = window.AudioContext ?? (window as unknown as { webkitAudioContext?: typeof AudioContext }).webkitAudioContext;
    if (!AC) return;
    ctx.current ??= new AC();
    const audio = ctx.current;
    void audio.resume();
    const scale = [293.7, 336.2, 386.4, 445.1, 512.8, 587.3];
    const melody = [0, 2, 3, 2, 4, 3, 2, 0, 1, 2, 4, 5, 4, 2, 3, 2];
    let step = 0;
    const ring = () => {
      const t = audio.currentTime;
      const freq = scale[melody[step % melody.length]];
      for (const [mult, gain] of [[1, 0.12], [2.76, 0.03], [0.5, 0.05]] as const) {
        const osc = audio.createOscillator();
        const amp = audio.createGain();
        osc.type = "sine";
        osc.frequency.value = freq * mult;
        amp.gain.setValueAtTime(0.0001, t);
        amp.gain.exponentialRampToValueAtTime(gain, t + 0.01);
        amp.gain.exponentialRampToValueAtTime(0.0001, t + 2.2);
        osc.connect(amp).connect(audio.destination);
        osc.start(t);
        osc.stop(t + 2.3);
      }
      step += 1;
    };
    ring();
    timer.current = setInterval(ring, 700);
    setPlaying(true);
  }, []);
  useEffect(() => () => {
    if (timer.current) clearInterval(timer.current);
    void ctx.current?.close();
  }, []);
  return { playing, toggle: () => (playing ? stop() : start()) };
}

export default function JawaTheme({ data, slug, guestToken, demo, skipCover }: ThemeProps) {
  const couple = coupleLabel(data);
  const parts = dateParts(data.date);
  const date = toDate(data.date);
  const month = date ? pad(Number(new Intl.DateTimeFormat("en", { timeZone: "Asia/Jakarta", month: "numeric" }).format(date))) : "";
  const numeric = parts.day ? `${pad(Number(parts.day))} · ${month} · ${parts.year}` : "";
  const where = city(data.address);
  const label = data.eventLabel ?? "Pernikahan";
  const countdown = useCountdown(data.date);
  const rsvp = useRsvp({ slug, guestToken, demo });
  const wishes = useWishes({ slug, guestToken, demo, seed: DEMO_WISHES });
  const sheets = useSheets();
  const { copy, copied } = useCopy();
  const music = useGamelan();
  const [attendance, setAttendance] = useState<Attendance>("yes");
  const stories = storyItems(data);
  const hero = data.gallery[0];
  const photos = data.gallery.length > 1 ? data.gallery.slice(1) : data.gallery;
  const [bigPhoto, ...gridPhotos] = photos;
  const calendar = calendarHref(data);
  const maps = mapsHref(data);
  const families = [father(data.couple.brideParents), father(data.couple.groomParents)].filter(Boolean).join(" & ");

  return (
    <ThemeShell
      fonts={FONTS}
      background="#1e120b"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.batik} aria-hidden />
          <div className={s.vignette} aria-hidden />
          <div className={s.frame} aria-hidden />
          <div className={s.frameInner} aria-hidden />
          <svg className={s.gunungan} viewBox="0 0 160 220" aria-hidden="true" focusable="false" dangerouslySetInnerHTML={{ __html: gunungan }} />
          <div className={s.coverContent}>
            <p className={s.kicker}>UNDANGAN {label.toUpperCase()}</p>
            <h1 className={s.coverNames}><span>{data.couple.bride}</span><em>&amp;</em><span>{data.couple.groom}</span></h1>
            <Divider />
            <p className={s.coverDate}>{formatDate(data.date)}{where ? ` · ${where}` : ""}</p>
          </div>
          <div className={s.spacer} />
          <div className={s.katur}>
            <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
            <strong>{guestLabel(data)}</strong>
            <small>di tempat</small>
          </div>
          <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#2b1a10" />Buka Undangan</button>
        </section>
      )}
    >
      <main className={s.main}>
        <header className={s.opening}>
          <Photo src={hero} alt={`Foto ${couple}`} className={s.openingImg} />
          <div className={s.openingText}>
            <p className={s.kicker}>{label.toUpperCase()}</p>
            <h1>{couple}</h1>
            <Divider />
            {numeric && <p className={s.numeric}>{numeric}</p>}
          </div>
        </header>

        <section className={s.quote} aria-label="Kutipan">
          <p>“Dan di antara tanda-tanda kekuasaan-Nya ialah Dia menciptakan untukmu pasangan dari jenismu sendiri, supaya kamu merasa tenteram kepadanya.”</p>
          <cite>— QS. Ar-Rum: 21</cite>
        </section>

        <section className={`${s.section} ${s.couple}`} aria-labelledby="jw-couple">
          <Head id="jw-couple" title="Mempelai" />
          <p className={s.intro}>Dengan memohon rahmat dan ridha Tuhan Yang Maha Kuasa, kami bermaksud menyelenggarakan {label.toLowerCase()} putra-putri kami:</p>
          {[
            { name: data.couple.brideFull ?? data.couple.bride, parents: data.couple.brideParents, photo: data.couple.bridePhoto ?? photos[0] ?? hero },
            { name: data.couple.groomFull ?? data.couple.groom, parents: data.couple.groomParents, photo: data.couple.groomPhoto ?? photos[1] ?? hero },
          ].map((person, index) => (
            <div key={index} className={s.personWrap}>
              {index === 1 && <p className={s.amp} aria-hidden>&amp;</p>}
              <article className={s.person}>
                <div className={s.arch}><Photo src={person.photo} alt={person.name} /></div>
                <h3>{person.name}</h3>
                {person.parents && <p>{person.parents}</p>}
              </article>
            </div>
          ))}
        </section>

        <section className={`${s.section} ${s.dark}`} aria-labelledby="jw-count">
          <Head id="jw-count" title="Menghitung Hari" light />
          <div className={s.count} role="timer" aria-label={`${countdown.days} hari ${countdown.hours} jam ${countdown.minutes} menit lagi`}>
            {[[countdown.days, "Hari"], [countdown.hours, "Jam"], [countdown.minutes, "Menit"], [countdown.seconds, "Detik"]].map(([value, unit]) => (
              <div key={unit}><b>{value}</b><small>{unit}</small></div>
            ))}
          </div>
          {calendar && <a className={s.ghostBtn} href={calendar} target="_blank" rel="noreferrer"><Lucide icon={ic.calendarPlus} size={15} color="#e6c77a" />Simpan ke Kalender</a>}
        </section>

        <section className={`${s.section} ${s.events}`} aria-labelledby="jw-events">
          <Head id="jw-events" title="Rangkaian Acara" />
          {data.events.map((event, index) => (
            <article key={event.name + index} className={s.event}>
              <h3>{event.name}</h3>
              <em>{formatDate(event.date || data.date)}</em>
              <b>{event.time}</b>
              <Divider />
              <strong>{event.venue}</strong>
              {event.address && <p>{event.address}</p>}
            </article>
          ))}
          {maps && <a className={s.darkBtn} href={maps} target="_blank" rel="noreferrer"><Lucide icon={ic.mapPin} size={15} color="#e6c77a" />Lihat Peta Lokasi</a>}
        </section>

        {stories.length > 0 && (
          <section className={`${s.section} ${s.story}`} aria-labelledby="jw-story">
            <Head id="jw-story" title="Perjalanan Cinta" />
            <ol className={s.timeline}>
              {stories.map((story, index) => (
                <li key={index}>
                  <span className={s.rail} aria-hidden><b>{story.date ?? index + 1}</b><i /></span>
                  <div className={s.storyText}>
                    <h3>{story.title}</h3>
                    {story.body && <p>{story.body}</p>}
                    {story.image && <Photo src={story.image} alt={story.title} className={s.storyImg} />}
                  </div>
                </li>
              ))}
              <li className={s.final}>
                <span className={s.rail} aria-hidden><b>{parts.year || "♥"}</b></span>
                <div className={s.storyText}>
                  <h3>{label}</h3>
                  <p>Hari yang dinanti — bersatu dalam ikatan suci.</p>
                </div>
              </li>
            </ol>
          </section>
        )}

        {bigPhoto && (
          <section className={`${s.section} ${s.dark} ${s.gallery}`} aria-labelledby="jw-gallery">
            <Head id="jw-gallery" title="Galeri Kenangan" light />
            <div className={s.bigArch}><Photo src={bigPhoto} alt="Foto galeri 1" /></div>
            {gridPhotos.length > 0 && (
              <div className={s.grid}>
                {gridPhotos.map((src, index) => <div key={src + index} className={s.smallArch}><Photo src={src} alt={`Foto galeri ${index + 2}`} /></div>)}
              </div>
            )}
            <p className={s.caption}>“Cinta bukan sekadar saling memandang, tapi menyatu dalam tujuan.”</p>
          </section>
        )}

        {data.gifts.length > 0 && (
          <section className={`${s.section} ${s.gifts}`} aria-labelledby="jw-gift">
            <Head id="jw-gift" title="Tanda Kasih" />
            <p className={s.intro}>Doa restu Anda sudah cukup. Jika berkenan memberi tanda kasih, dapat melalui:</p>
            {data.gifts.map(gift => {
              const info = giftInfo(gift);
              const address = gift.type === "address" ? (gift.address ?? "") : "";
              const cut = address.indexOf(",");
              const title = gift.type === "bank" ? (/^bank/i.test(info.title) ? info.title : `Bank ${info.title}`) : gift.type === "address" ? "Kirim Kado" : info.title;
              const main = gift.type === "address" ? (cut > 0 ? address.slice(0, cut) : address) : info.number;
              const sub = gift.type === "address" ? (cut > 0 ? address.slice(cut + 1).trim() : "") : info.holder ? `a.n. ${info.holder}` : "";
              const icon = gift.type === "bank" ? ic.landmark : gift.type === "address" ? ic.gift : gift.type === "qris" ? ic.qrCode : ic.wallet;
              return (
                <div key={gift.id} className={s.gift}>
                  <span className={s.giftIcon}><Lucide icon={icon} size={20} color="#e6c77a" /></span>
                  <div>
                    <h3>{title}</h3>
                    {main && <strong>{main}</strong>}
                    {sub && <small>{sub}</small>}
                    {info.image && <Photo src={info.image} alt="Kode QRIS" className={s.qris} />}
                  </div>
                  {info.copy && (
                    <button type="button" className={s.copy} onClick={() => copy(info.copy)} aria-label={copied === info.copy ? "Tersalin" : `Salin ${title}`}>
                      <Lucide icon={copied === info.copy ? ic.check : ic.copy} size={14} color="#9a7224" />
                    </button>
                  )}
                </div>
              );
            })}
          </section>
        )}

        <section className={`${s.section} ${s.wishes}`} aria-labelledby="jw-wishes">
          <Head id="jw-wishes" title="Ucapan & Doa" />
          {wishes.status === "sent" ? (
            <div className={s.form} role="status">
              <p className={s.sent}>Matur nuwun — ucapan &amp; doa Anda sudah terkirim.</p>
              {demo && <p className={s.sentNote}>Ini pratinjau, ucapan hanya tampil di daftar.</p>}
              <button type="button" className={s.submit} onClick={() => { wishes.reset(); rsvp.reset(); }}>Tulis Lagi</button>
            </div>
          ) : (
            <form className={s.form} onSubmit={event => {
              event.preventDefault();
              const form = new FormData(event.currentTarget);
              const name = String(form.get("name") ?? "").trim();
              const message = String(form.get("message") ?? "").trim();
              if (!name || !message) return;
              void wishes.send(name, message);
              if (rsvp.status !== "sent") void rsvp.submit({ name, attendance, guests: 1 });
            }}>
              <label className={s.field}><span>Nama</span><input name="name" required maxLength={100} defaultValue={plainName(data.guestName)} placeholder="Nama Anda" autoComplete="name" /></label>
              <label className={s.field}><span>Ucapan</span><textarea name="message" required maxLength={500} rows={3} placeholder="Tuliskan doa & ucapan…" /></label>
              <div className={s.choices} role="radiogroup" aria-label="Kehadiran">
                {(["yes", "maybe", "no"] as Attendance[]).map(value => (
                  <button key={value} type="button" role="radio" aria-checked={attendance === value} className={attendance === value ? s.choiceOn : undefined} onClick={() => setAttendance(value)}>
                    {ATTEND[value]}
                  </button>
                ))}
              </div>
              {wishes.status === "error" && <p className={s.error} role="alert">Belum terkirim. Coba lagi sebentar lagi.</p>}
              <button type="submit" className={s.submit} disabled={wishes.status === "sending"}>{wishes.status === "sending" ? "Mengirim…" : "Kirim Ucapan"}</button>
            </form>
          )}
          <button type="button" className={s.textBtn} onClick={sheets.openRsvp}>Konfirmasi jumlah tamu yang hadir →</button>
          {wishes.wishes.length === 0 && <p className={s.empty}>Belum ada ucapan. Jadilah yang pertama mendoakan.</p>}
          {wishes.wishes.slice(0, 10).map(wish => (
            <article key={wish.id} className={s.wish}>
              <div><strong>{wish.name}</strong>{wish.attendance && <small>{ATTEND[wish.attendance]}</small>}</div>
              <p>{wish.message}</p>
            </article>
          ))}
        </section>

        <footer className={s.closing}>
          <p className={s.thanks}>Terima Kasih</p>
          <Divider />
          <p className={s.closingText}>Kehadiran dan doa restu Anda adalah kebahagiaan tak terhingga bagi kami sekeluarga.</p>
          <p className={s.family}>Keluarga Besar<br />{families || couple}</p>
          <a href="/" target="_blank" rel="noreferrer" className={s.made}>dibuat dengan ♥ di Rawuh</a>
        </footer>
      </main>

      <button type="button" className={music.playing ? `${s.music} ${s.musicOn}` : s.music} onClick={music.toggle} aria-pressed={music.playing} aria-label={music.playing ? "Matikan gending" : "Putar gending"}>
        <Lucide icon={ic.music} size={18} color="#e6c77a" />
      </button>

      <Sheet open={sheets.sheet === "rsvp"} onClose={sheets.close} title="Konfirmasi Kehadiran" tint={tint}>
        <RsvpForm rsvp={rsvp} guestName={data.guestName} demo={demo} labels={{ success: "Matur nuwun!" }} />
      </Sheet>
    </ThemeShell>
  );
}
