"use client";
// Theme "Wisuda Toga" — syukuran wisuda: navy & emas akademik, bingkai ijazah, toga yang bisa dilempar, transkrip perjalanan, segel emas.
import { useEffect, useId, useRef, useState, type CSSProperties, type FormEvent } from "react";
import {
  DietaryField, Extras, GuestCount, Lucide, Photo, ThemeShell, Tick, dateParts, formatDate, giftInfo, guestLabel, mapsHref,
  storyItems, toDate, useCopy, useCountdown, DATE_TBA, sentSummary, useRsvp, useThankYou, useWishes, type Attendance, type ThemeProps, type Wish,
} from "../kit";
import type { InvitationData } from "../../types";
import { tableLabel } from "../extras";
import { celebrate, toast } from "@/lib/celebrate";
import { ic } from "./icons";
import s from "./styles.module.css";

const FONTS = ["DM Serif Display", "Archivo:wght@400;500;600;700", "JetBrains Mono:wght@400;600"];
const ATTEND: Record<Attendance, string> = { yes: "Hadir", maybe: "Ragu", no: "Berhalangan" };
const DEMO_WISHES: Wish[] = [
  { id: "w1", name: "Bu Dewi (dosen pembimbing)", attendance: "yes", message: "Selamat, Nadia! Skripsimu bermanfaat untuk banyak petani. Teruslah belajar dan berkarya." },
  { id: "w2", name: "Raka, teman satu lab", attendance: "yes", message: "Akhirnya toga juga! Bangga banget, semoga cepat dapat kerja impian." },
];

/* ── Helpers ───────────────────────────────────────────────── */

function graduates(data: InvitationData) {
  const list = [
    { short: data.couple.bride?.trim() ?? "", full: data.couple.brideFull?.trim(), note: data.couple.brideParents?.trim(), photo: data.couple.bridePhoto },
    { short: data.couple.groom?.trim() ?? "", full: data.couple.groomFull?.trim(), note: data.couple.groomParents?.trim(), photo: data.couple.groomPhoto },
  ].filter(item => item.short || item.full);
  return list.map(item => ({ ...item, short: item.short || item.full || "", full: item.full || item.short }));
}

function calendarHref(title: string, data: InvitationData) {
  const start = toDate(data.date) ?? toDate(data.events[0]?.date);
  if (!start) return undefined;
  const stamp = (d: Date) => d.toISOString().replace(/[-:]|\.\d{3}/g, "");
  const params = new URLSearchParams({ action: "TEMPLATE", text: title, dates: `${stamp(start)}/${stamp(new Date(start.getTime() + 3 * 3600e3))}`, location: [data.place, data.address].filter(Boolean).join(", ") });
  return `https://calendar.google.com/calendar/render?${params.toString()}`;
}

function plainName(guest?: string) {
  if (!guest || guest === "Tamu Undangan") return "";
  return guest.replace(/^(bapak|ibu|bpk\.?|sdr\.?)\s+/i, "").replace(/\s*(&|dan)\s*keluarga$/i, "").trim();
}

function clock(value?: string) {
  const date = toDate(value);
  return date ? new Intl.DateTimeFormat("id-ID", { timeZone: "Asia/Jakarta", hour: "2-digit", minute: "2-digit" }).format(date).replace(":", ".") : "";
}

/* ── Ornaments ─────────────────────────────────────────────── */

function CapArt() {
  return (
    <svg className={s.cap} viewBox="0 0 120 92" aria-hidden="true" focusable="false">
      <path d="M28 40v20c0 9 14 15 32 15s32-6 32-15V40L60 53z" fill="#0d1d36" stroke="#c8a24a" strokeWidth="1.6" strokeLinejoin="round" />
      <path d="M60 8 116 30 60 53 4 30z" fill="#1c3866" stroke="#c8a24a" strokeWidth="1.6" strokeLinejoin="round" />
      <path d="M60 15 99 30 60 46 21 30z" fill="none" stroke="#c8a24a" strokeOpacity=".35" strokeWidth="1" />
      <g className={s.tassel}>
        <path d="M60 30 98 38v26" fill="none" stroke="#c8a24a" strokeWidth="1.8" strokeLinecap="round" />
        <path d="M94 62h8l2 16h-12z" fill="#c8a24a" />
        <path d="M95 66v11M98 66v12M101 66v11" stroke="#8a6d27" strokeWidth=".8" />
      </g>
      <circle cx="60" cy="30" r="3.2" fill="#c8a24a" />
    </svg>
  );
}

/** Tap the mortarboard to toss it (decorative). */
function Cap({ className }: { className?: string }) {
  const [tossing, setTossing] = useState(false);
  const [tosses, setTosses] = useState(0);
  return (
    <button type="button" className={`${s.capBtn} ${tossing ? s.tossing : ""} ${className ?? ""}`} aria-label="Lempar toga" data-noreveal
      onClick={event => {
        if (tossing) return;
        setTossing(true);
        setTosses(n => n + 1);
        if (tosses === 0) toast("Selamat atas kelulusannya!");
        const element = event.currentTarget;
        window.setTimeout(() => { setTossing(false); celebrate(element); }, 900);
      }}>
      <span className={s.capArt}><CapArt /></span>
    </button>
  );
}

function Seal({ text }: { text: string }) {
  const id = useId().replace(/:/g, "");
  return (
    <svg className={s.seal} viewBox="0 0 120 120" aria-hidden="true" focusable="false">
      <defs><path id={`seal-${id}`} d="M60 60m-44 0a44 44 0 1 1 88 0a44 44 0 1 1-88 0" /></defs>
      <path d="M60 2l7 6 9-2 4 8 9 1 1 9 8 4-2 9 6 7-6 7 2 9-8 4-1 9-9 1-4 8-9-2-7 6-7-6-9 2-4-8-9-1-1-9-8-4 2-9-6-7 6-7-2-9 8-4 1-9 9-1 4-8 9 2z" fill="#c8a24a" />
      <circle cx="60" cy="60" r="51" fill="none" stroke="#0d1d36" strokeOpacity=".35" strokeWidth="1" />
      <circle cx="60" cy="60" r="34" fill="#13294b" />
      <g className={s.sealSpin}><text className={s.sealText}><textPath href={`#seal-${id}`} textLength="272" lengthAdjust="spacing">{text}</textPath></text></g>
      <path d="M60 44l4.7 9.6 10.6 1.5-7.6 7.5 1.8 10.5L60 68l-9.5 5.1 1.8-10.5-7.6-7.5 10.6-1.5z" fill="#c8a24a" />
    </svg>
  );
}

function Rule() {
  return <span className={s.rule} aria-hidden><i /></span>;
}

function Head({ id, num, children }: { id: string; num: string; children: string }) {
  return (
    <div className={s.head}>
      <span className={s.num}>{num}</span>
      <h2 id={id}>{children}</h2>
    </div>
  );
}

/* ── Theme ─────────────────────────────────────────────────── */

export default function WisudaTogaTheme({ data, slug, guestToken, demo, skipCover }: ThemeProps) {
  const grads = graduates(data);
  const main = grads[0] ?? { short: "Wisudawan", full: "Wisudawan", note: "", photo: undefined };
  const names = grads.map(g => g.short).join(" & ") || main.short;
  const label = data.eventLabel?.trim() || "Syukuran Wisuda";
  const parts = dateParts(data.date);
  const countdown = useCountdown(data.date);
  const rsvp = useRsvp({ slug, guestToken, demo });
  const wishes = useWishes({ slug, guestToken, demo, seed: DEMO_WISHES });
  const thanks = useThankYou();
  const rsvpClosed = thanks.active || rsvp.status === "closed";
  const { copy, copied } = useCopy();
  const stories = storyItems(data);
  const gallery = data.gallery.filter(Boolean);
  const [attendance, setAttendance] = useState<Attendance>("yes");
  const calendar = calendarHref(`${label} ${names}`, data);
  const table = tableLabel(data.guestTable);
  const sealText = `${label.toUpperCase()} · ${parts.year || "ANGKATAN"} · ${main.short.toUpperCase().slice(0, 12)} · `;
  const degree = (main.note ?? "").split("\n").map(line => line.trim()).filter(Boolean).join(" · ");
  const sending = rsvp.status === "sending" || wishes.status === "sending";
  const sent = rsvp.status === "sent" || wishes.status === "sent";
  const sentRef = useRef<HTMLDivElement>(null);
  useEffect(() => { if (sent) celebrate(sentRef.current); }, [sent]);
  let n = 0;
  const num = () => String(++n).padStart(2, "0");

  const onSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const form = new FormData(event.currentTarget);
    const name = String(form.get("name") ?? "").trim();
    const message = String(form.get("message") ?? "").trim();
    const guests = attendance === "no" ? 1 : Number(form.get("guests")) || 1;
    if (!name) return;
    if (!rsvpClosed) void rsvp.submit({ name, attendance, guests, message, diet: String(form.get("diet") ?? "").trim() || undefined });
    if (message) void wishes.send(name, message);
  };

  return (
    <ThemeShell
      fonts={FONTS}
      background="#0d1d36"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.certificate}>
            <i className={s.corner} aria-hidden /><i className={s.corner} aria-hidden /><i className={s.corner} aria-hidden /><i className={s.corner} aria-hidden />
            <Cap className={s.coverCap} />
            <p className={s.coverKicker}>Undangan {label}</p>
            <h1 className={s.coverName}>{names}</h1>
            {degree && <p className={s.coverDegree}>{degree}</p>}
            <p className={s.coverDate}>{parts.day ? `${parts.day} ${parts.month.toUpperCase()} ${parts.year}` : DATE_TBA}</p>
            <div className={s.kepada}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={`${s.btn} ${s.btnGold}`} onClick={open}><Lucide icon={ic.mailOpen} size={16} />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <main className={s.page}>
        <header className={s.hero}>
          <div className={s.heroTop}>
            <p className={s.coverKicker}>{label}</p>
            <Cap className={s.heroCap} />
          </div>
          <h1 className={s.heroName}>{names}</h1>
          {grads.length === 1 && main.full !== main.short && <p className={s.heroDegree}>{main.full}</p>}
          <Rule />
          <dl className={s.heroMeta}>
            <div><dt>Tanggal</dt><dd>{parts.day ? `${parts.day} ${parts.monthShort} ${parts.year}` : DATE_TBA}</dd></div>
            <div><dt>Tempat</dt><dd>{data.place || data.events[0]?.venue || "Menyusul"}</dd></div>
          </dl>
        </header>

        <section className={s.section} aria-label="Pembuka">
          <p className={s.lead}>Puji syukur ke hadirat Tuhan Yang Maha Esa atas segala rahmat-Nya. {data.couple.note?.trim() || `Dengan bahagia kami mengundang Bapak/Ibu/Saudara/i untuk merayakan kelulusan ${names}.`}</p>
          <blockquote className={s.quote}>“Pendidikan adalah senjata paling ampuh yang bisa kamu gunakan untuk mengubah dunia.”<cite>— Nelson Mandela</cite></blockquote>
        </section>

        <Extras slot="opening" />

        <section className={s.section} aria-labelledby="wt-grad">
          <Head id="wt-grad" num={num()}>{grads.length > 1 ? "Para Wisudawan" : "Sang Wisudawan"}</Head>
          {(grads.length ? grads : [main]).map((grad, index) => (
            <article key={grad.full + index} className={s.grad}>
              <div className={s.pasFoto}>{grad.photo ? <Photo src={grad.photo} alt={`Foto ${grad.short}`} /> : <span aria-hidden>{grad.short.slice(0, 1).toUpperCase()}</span>}</div>
              <div className={s.gradText}>
                <small>Wisudawan{grads.length > 1 ? ` ${index + 1}` : ""}</small>
                <h3>{grad.full}</h3>
                {grad.note && <p>{grad.note}</p>}
                <span className={s.sealWrap}><Seal text={sealText} /></span>
              </div>
            </article>
          ))}
        </section>

        <section className={`${s.section} ${s.navyBand}`} aria-labelledby="wt-count">
          <Head id="wt-count" num={num()}>Menuju Hari Syukur</Head>
          {countdown.valid ? (
            <div className={s.count} role="timer" aria-label={`${countdown.days} hari ${countdown.hours} jam ${countdown.minutes} menit lagi`}>
              {([["Hari", countdown.days], ["Jam", countdown.hours], ["Menit", countdown.minutes], ["Detik", countdown.seconds]] as const).map(([unit, value]) => (
                <div key={unit}><b><Tick value={value} /></b><small>{unit}</small></div>
              ))}
            </div>
          ) : <p className={s.tba}>{DATE_TBA}</p>}
          {calendar && <a className={`${s.btn} ${s.btnGold}`} href={calendar} target="_blank" rel="noreferrer"><Lucide icon={ic.calendarPlus} size={15} />Simpan ke Kalender</a>}
        </section>

        <section className={s.section} aria-labelledby="wt-events">
          <Head id="wt-events" num={num()}>Jadwal Acara</Head>
          <div className={s.schedule}>
            {data.events.map((event, index) => {
              const when = event.date || data.date;
              const href = mapsHref(data, event);
              const p = dateParts(when);
              return (
                <article key={event.name + index} className={s.row}>
                  <div className={s.rowWhen}><b>{clock(when) || p.day || "--"}</b><small>{p.day ? `${p.day} ${p.monthShort}` : "TBA"}</small></div>
                  <div className={s.rowBody}>
                    <h3>{event.name}</h3>
                    <p>{formatDate(when)}{event.time ? ` · ${event.time}` : ""}</p>
                    {event.venue && <strong>{event.venue}</strong>}
                    {event.address && <p>{event.address}</p>}
                    {href && <a className={s.mapLink} href={href} target="_blank" rel="noreferrer"><Lucide icon={ic.mapPin} size={13} />Lihat peta</a>}
                  </div>
                </article>
              );
            })}
          </div>
        </section>

        <Extras slot="event" without={["calendar"]} />

        {stories.length > 0 && (
          <section className={s.section} aria-labelledby="wt-story">
            <Head id="wt-story" num={num()}>{data.story?.title?.trim() && data.stories?.length ? data.story.title : "Transkrip Perjalanan"}</Head>
            <div className={s.transcript}>
              <div className={s.transcriptHead} aria-hidden><span>Tahun</span><span>Pencapaian</span></div>
              <ol>
              {stories.map((story, index) => (
                <li key={story.title + index}>
                  <span className={s.term}>{story.date || `S${index + 1}`}</span>
                  <div>
                    <h3>{story.title}</h3>
                    {story.body && <p>{story.body}</p>}
                    {story.image && <Photo src={story.image} alt={story.title} className={s.storyImg} />}
                    <span className={s.bar} style={{ "--p": `${Math.round(((index + 1) / stories.length) * 100)}%` } as CSSProperties} aria-hidden />
                  </div>
                </li>
              ))}
              </ol>
            </div>
          </section>
        )}

        {gallery.length > 0 && (
          <section className={s.section} aria-labelledby="wt-gallery">
            <Head id="wt-gallery" num={num()}>Galeri</Head>
            <div className={s.gallery}>{gallery.map((src, index) => <Photo key={src + index} src={src} alt={`Foto ${index + 1}`} />)}</div>
          </section>
        )}

        <Extras slot="story" />

        <Extras slot="end" />

        <section className={s.section} aria-labelledby="wt-rsvp">
          <Head id="wt-rsvp" num={num()}>Konfirmasi &amp; Ucapan</Head>
          <div className={s.formCard}>
            {sent ? (
              <div ref={sentRef} className={s.sent} role="status">
                <span className={s.sentIcon}><Lucide icon={ic.check} size={22} strokeWidth={2.6} /></span>
                <strong>Terima kasih!</strong>
                <p>{demo ? "Ini pratinjau — jawaban contoh tidak dikirim." : sentSummary(rsvp, wishes)}</p>
                <button type="button" className={`${s.btn} ${s.btnLine}`} onClick={() => { rsvp.reset(); wishes.reset(); }}>Tulis lagi</button>
              </div>
            ) : (
              <form className={s.form} onSubmit={onSubmit}>
                <label className={s.field}><span>Nama</span><input name="name" required maxLength={100} placeholder="Nama Anda" autoComplete="name" defaultValue={plainName(data.guestName)} /></label>
                <label className={s.field}><span>Ucapan selamat</span><textarea name="message" required={rsvpClosed} maxLength={500} rows={3} placeholder={`Tulis ucapan untuk ${names}…`} /></label>
                {rsvpClosed ? (
                  <div className={s.closed} role="status"><strong>Konfirmasi kehadiran sudah ditutup</strong><p>Acara telah berlangsung. Terima kasih atas doa dan dukungannya. Ucapan masih bisa dikirim lewat form ini.</p></div>
                ) : (
                  <fieldset className={s.choices}>
                    <legend className={s.srOnly}>Kehadiran</legend>
                    {(Object.keys(ATTEND) as Attendance[]).map(key => (
                      <label key={key} className={attendance === key ? s.chosen : undefined}>
                        <input type="radio" name="attendance" value={key} checked={attendance === key} onChange={() => setAttendance(key)} />{ATTEND[key]}
                      </label>
                    ))}
                  </fieldset>
                )}
                {!rsvpClosed && attendance !== "no" && <GuestCount label="Jumlah tamu" className={s.guests} buttonClassName={s.step} />}
                {!rsvpClosed && attendance !== "no" && <DietaryField className={s.field} />}
                {(rsvp.status === "error" || wishes.status === "error") && <p className={s.error} role="alert">Belum terkirim. Periksa koneksi lalu coba lagi.</p>}
                <button type="submit" className={`${s.btn} ${s.submit}`} disabled={sending}>{sending ? "Mengirim…" : "Kirim"}</button>
              </form>
            )}
          </div>
          {wishes.wishes.length === 0 && <p className={s.empty}>Belum ada ucapan. Jadilah yang pertama memberi selamat.</p>}
          <div className={s.wishes}>
            {wishes.wishes.slice(0, 10).map(wish => (
              <article key={wish.id} className={s.wish}>
                <div><strong>{wish.name}</strong>{wish.attendance && <small>{ATTEND[wish.attendance]}</small>}</div>
                <p>{wish.message}</p>
              </article>
            ))}
          </div>
        </section>

        {data.gifts.length > 0 && (
          <section className={`${s.section} ${s.navyBand}`} aria-labelledby="wt-gift">
            <Head id="wt-gift" num={num()}>Tanda Apresiasi</Head>
            <p className={s.lead}>Doa dan dukungan Anda sudah sangat berarti. Bagi yang ingin memberi tanda apresiasi, dapat melalui:</p>
            <div className={s.gifts}>
              {data.gifts.map(gift => {
                const info = giftInfo(gift);
                const on = Boolean(info.copy) && copied === info.copy;
                const icon = gift.type === "bank" ? ic.landmark : gift.type === "ewallet" ? ic.wallet : gift.type === "qris" ? ic.qrCode : ic.gift;
                return (
                  <div key={gift.id} className={`${s.gift} ${on ? s.giftOn : ""}`}>
                    <span className={s.giftIcon}><Lucide icon={icon} size={20} /></span>
                    <div className={s.giftText}>
                      <small>{info.kind}</small>
                      <strong>{gift.type === "address" ? "Alamat kirim" : info.title}</strong>
                      {info.number && <span className={s.giftNumber}>{info.number}</span>}
                      {info.holder && <span>a.n. {info.holder}</span>}
                      {info.image && <Photo src={info.image} alt="Kode QRIS" className={s.qris} />}
                    </div>
                    {info.copy ? (
                      <button type="button" className={`${s.copy} ${on ? s.copyOn : ""}`} onClick={() => copy(info.copy)} aria-label={on ? "Tersalin" : `Salin ${info.title}`}>
                        <Lucide key={on ? "on" : "off"} icon={on ? ic.check : ic.copy} size={16} />
                      </button>
                    ) : <span />}
                  </div>
                );
              })}
            </div>
          </section>
        )}

        <footer className={s.closing}>
          <span className={s.sealWrap}><Seal text={sealText} /></span>
          <h2>Terima Kasih</h2>
          <p>Kehadiran dan doa Anda melengkapi kebahagiaan kami. Semoga ilmu yang diperoleh bermanfaat bagi sesama.</p>
          <strong>Keluarga besar {names}</strong>
          <a href="/" target="_blank" rel="noreferrer" className={s.made}>dibuat dengan ♥ di Rawuh</a>
        </footer>
      </main>
    </ThemeShell>
  );
}
