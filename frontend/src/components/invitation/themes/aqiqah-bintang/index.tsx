"use client";
// Theme "Aqiqah Bintang" — aqiqah bayi bernuansa pastel: bulan sabit tidur, awan, dan mainan gantung bintang yang berayun.
import { useEffect, useId, useRef, useState } from "react";
import {
  DietaryField, Extras, GuestCount, Icon, Photo, ThemeShell, Tick, dateParts, formatDate, giftInfo, guestLabel, icons,
  mapsHref, storyItems, useCopy, useCountdown, DATE_TBA, useRsvp, useThankYou, useWishes, type Attendance, type ThemeProps, type Wish,
} from "../kit";
import { tableLabel } from "../extras";
import { celebrate, toast } from "@/lib/celebrate";
import s from "./styles.module.css";

const FONTS = ["Nunito:wght@400;600;700;800;900", "Caveat:wght@500;700", "Amiri:wght@400;700"];
const ATTEND: Record<Attendance, string> = { yes: "Hadir", maybe: "Ragu", no: "Berhalangan" };
const DEMO_WISHES: Wish[] = [
  { id: "w1", name: "Tante Dewi", attendance: "yes", message: "Selamat datang di dunia, Naura sayang. Semoga jadi anak salehah, sehat, dan menyejukkan hati ayah bunda." },
  { id: "w2", name: "Keluarga Pak RT", attendance: "maybe", message: "Barakallahu fiikum. Semoga Naura tumbuh menjadi penyejuk mata dan kebanggaan keluarga." },
];
const HOPES = ["Anak salehah yang taat kepada Allah", "Sehat dan tumbuh dengan ceria", "Berbakti kepada ayah dan bunda", "Bermanfaat bagi sesama"];
const WALLET = ["M19 7V4a1 1 0 0 0-1-1H5a2 2 0 0 0 0 4h15a1 1 0 0 1 1 1v4h-3a2 2 0 0 0 0 4h3a1 1 0 0 0 1-1v-2a1 1 0 0 0-1-1", "M3 5v14a2 2 0 0 0 2 2h15a1 1 0 0 0 1-1v-4"];
const BANK = ["M3 22h18", "M6 18v-7", "M10 18v-7", "M14 18v-7", "M18 18v-7", "M12 2l8 5H4z"];
const STAR = "M12 2.5l2.6 5.6 6.1.7-4.5 4.2 1.2 6-5.4-3-5.4 3 1.2-6L3.3 8.8l6.1-.7z";
const CLOUD = "M18 46a14 14 0 0 1 2-28 20 20 0 0 1 37-6 15 15 0 0 1 25 11 12 12 0 0 1-1 23z";

/** Sleeping crescent moon cradling a swaddled baby (original illustration). */
function MoonBaby({ className }: { className?: string }) {
  const id = useId().replace(/:/g, "");
  return (
    <svg className={className} viewBox="0 0 220 190" aria-hidden="true" focusable="false">
      <defs>
        <mask id={`m${id}`}><rect width="220" height="190" fill="#fff" /><circle cx="138" cy="70" r="66" fill="#000" /></mask>
      </defs>
      <g className={s.moonBody}>
        <circle cx="104" cy="98" r="84" fill="#ffe08f" mask={`url(#m${id})`} />
        <path d="M38 96q8 7 16 0" fill="none" stroke="#7a5c2e" strokeWidth="3" strokeLinecap="round" />
        <circle cx="40" cy="112" r="7" fill="#f7a7b4" opacity=".7" />
        <path d="M44 126q8 6 16 1" fill="none" stroke="#7a5c2e" strokeWidth="2.6" strokeLinecap="round" />
      </g>
      <g className={s.baby}>
        <path d="M78 150c-4-18 16-32 46-34 22-1 40 4 46 14 4 9-6 20-30 24-26 5-58 6-62-4z" fill="#f9c9d4" />
        <path d="M96 130c18-6 40-6 58 0" fill="none" stroke="#f1aebd" strokeWidth="3" strokeLinecap="round" />
        <path d="M92 142c22-5 46-5 64 1" fill="none" stroke="#f1aebd" strokeWidth="3" strokeLinecap="round" />
        <circle cx="172" cy="118" r="20" fill="#ffe2cc" />
        <path d="M156 110c2-14 22-20 34-8-8-2-14 0-18 4-4-3-10-2-16 4z" fill="#cfdcff" />
        <circle cx="191" cy="99" r="4" fill="#ffd37a" />
        <path d="M163 121q4 3 8 0" fill="none" stroke="#5b4636" strokeWidth="2" strokeLinecap="round" />
        <circle cx="164" cy="128" r="3.5" fill="#f7a7b4" opacity=".75" />
        <path d="M176 131q3 2 6 0" fill="none" stroke="#c98a7a" strokeWidth="1.8" strokeLinecap="round" />
      </g>
      <g className={s.zz} fill="#8f9ad1" fontFamily="Nunito, sans-serif" fontWeight="800">
        <text x="186" y="74" fontSize="14">z</text><text x="198" y="58" fontSize="11">z</text>
      </g>
    </svg>
  );
}

function Cloud({ className }: { className?: string }) {
  return <svg className={className} viewBox="0 0 96 50" aria-hidden="true" focusable="false"><path d={CLOUD} fill="currentColor" /></svg>;
}

/** Crib mobile: an arched bar with a star, moon and cloud each swinging on its own string. */
function Mobile() {
  return (
    <div className={s.mobile} aria-hidden>
      <svg className={s.mobileBar} viewBox="0 0 260 40" focusable="false"><path d="M10 34Q130-6 250 34" fill="none" stroke="#b7c2ec" strokeWidth="3" strokeLinecap="round" /><circle cx="130" cy="14" r="5" fill="#ffd37a" /></svg>
      <span className={s.hang} style={{ ["--len" as string]: "46px", left: "14%" }}><svg viewBox="0 0 24 24"><path d={STAR} fill="#ffd37a" /></svg></span>
      <span className={s.hang} style={{ ["--len" as string]: "70px", left: "38%", animationDelay: "-1.2s" }}><Cloud className={s.hangCloud} /></span>
      <span className={s.hang} style={{ ["--len" as string]: "58px", left: "62%", animationDelay: "-2.1s" }}><svg viewBox="0 0 24 24"><path d="M15 3a9 9 0 1 0 6 13A7 7 0 0 1 15 3z" fill="#f9c9d4" /></svg></span>
      <span className={s.hang} style={{ ["--len" as string]: "40px", left: "84%", animationDelay: "-.6s" }}><svg viewBox="0 0 24 24"><path d={STAR} fill="#cdeee0" /></svg></span>
    </div>
  );
}

function Sparkles({ count = 8, seed = 1 }: { count?: number; seed?: number }) {
  return (
    <div className={s.sparkles} aria-hidden>
      {Array.from({ length: count }, (_, i) => {
        const n = (i + 2) * 41 * seed;
        return <svg key={i} viewBox="0 0 24 24" style={{ left: `${(n * 11) % 94}%`, top: `${(n * 7) % 90}%`, width: 8 + (n % 4) * 3, animationDelay: `${(n % 6) * 0.6}s` }}><path d={STAR} fill="currentColor" /></svg>;
      })}
    </div>
  );
}

function Head({ id, kicker, title }: { id: string; kicker?: string; title: string }) {
  return (
    <div className={s.head}>
      {kicker && <p className={s.script}>{kicker}</p>}
      <h2 id={id}>{title}</h2>
    </div>
  );
}

/** The opening extras without the shared child card — this theme draws the child's profile itself. */
function OpeningExtras() {
  return <Extras slot="opening" without={["quote", "child"]} />;
}

/** "Muhammad Rafa Alfarizi" → "Rafa", "Naura Kamila" → "Naura" */
function shortName(name: string) {
  const words = name.trim().split(/\s+/);
  return /^(muhammad|muh\.?|moh\.?|m\.)$/i.test(words[0]) && words[1] ? words[1] : words[0];
}

function plainName(guest?: string) {
  if (!guest || guest === "Tamu Undangan") return "";
  return guest.replace(/^(bapak|ibu|bpk\.?|sdr\.?|saudara|saudari)\s+/i, "").replace(/\s*(&|dan)\s*keluarga$/i, "").trim();
}

/** "Putri pertama dari Bapak A & Ibu B" → "Bapak A & Ibu B" */
function parentNames(parents?: string) {
  const value = parents?.trim();
  if (!value) return "";
  const match = /\b(?:dari|of)\s+(.+)$/i.exec(value);
  return (match ? match[1] : value).trim();
}

function initial(name: string) {
  return name.trim().slice(0, 1).toUpperCase() || "·";
}

export default function AqiqahBintangTheme({ data, slug, guestToken, demo, skipCover }: ThemeProps) {
  const label = data.eventLabel ?? "Aqiqah";
  const child = data.extras?.child?.enabled !== false && data.extras?.child?.name?.trim() ? data.extras.child : undefined;
  const babies = child
    ? [{ name: child.name, nick: child.nickname || shortName(child.name), birth: child.birthDate, meaning: child.meaning, parents: child.parents || data.couple.brideParents, photo: child.photo }]
    : [
      { name: data.couple.brideFull || data.couple.bride, nick: data.couple.bride, birth: undefined, meaning: undefined, parents: data.couple.brideParents, photo: data.couple.bridePhoto },
      ...(data.couple.groom?.trim() ? [{ name: data.couple.groomFull || data.couple.groom, nick: data.couple.groom, birth: undefined, meaning: undefined, parents: data.couple.groomParents, photo: data.couple.groomPhoto }] : []),
    ];
  const nick = babies.map(baby => baby.nick).filter(Boolean).join(" & ") || "Si Kecil";
  const parents = parentNames(babies[0]?.parents);
  const girl = /\bputri\b/i.test(babies[0]?.parents ?? "");
  const parts = dateParts(data.date);
  const countdown = useCountdown(data.date);
  const rsvp = useRsvp({ slug, guestToken, demo });
  const wishes = useWishes({ slug, guestToken, demo, seed: DEMO_WISHES });
  const thanks = useThankYou();
  const rsvpClosed = thanks.active || rsvp.status === "closed";
  const { copy, copied } = useCopy();
  const [attendance, setAttendance] = useState<Attendance>("yes");
  const [lit, setLit] = useState<number[]>([]);
  const stories = storyItems(data);
  const table = tableLabel(data.guestTable);
  const quote = data.extras?.quote?.enabled !== false && data.extras?.quote?.text ? data.extras.quote : { text: "Harta dan anak-anak adalah perhiasan kehidupan dunia, tetapi amal kebajikan yang terus-menerus adalah lebih baik pahalanya di sisi Tuhanmu.", source: "QS. Al-Kahf: 46" };
  const sentRef = useRef<HTMLDivElement>(null);
  useEffect(() => { if (wishes.status === "sent") celebrate(sentRef.current); }, [wishes.status]);
  const light = (index: number) => {
    if (lit.includes(index)) return;
    const next = [...lit, index];
    setLit(next);
    if (next.length === HOPES.length) toast("Aamiin ya Rabbal 'alamin");
  };

  return (
    <ThemeShell
      fonts={FONTS}
      background="#e9eefc"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Sparkles count={12} seed={2} />
          <Cloud className={`${s.cloud} ${s.cloudA}`} />
          <Cloud className={`${s.cloud} ${s.cloudB}`} />
          <Mobile />
          <MoonBaby className={s.coverArt} />
          <div className={s.coverText}>
            <p className={s.pill}>Tasyakuran {label}</p>
            <h1 className={s.coverName}>{nick}</h1>
            {child && child.name !== nick && <p className={s.coverFull}>{child.name}</p>}
            <p className={s.coverDate}>{formatDate(data.date)}</p>
          </div>
          <div className={s.kepada}>
            <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
            <strong>{guestLabel(data)}</strong>
            {table && <span className={s.table}>{table}</span>}
          </div>
          <button type="button" className={s.btn} onClick={open}><Icon d={icons.mailOpen} size={17} strokeWidth={2.4} />Buka Undangan</button>
          <Cloud className={`${s.cloud} ${s.cloudBottom}`} />
        </section>
      )}
    >
      <main className={s.main}>
        <header className={s.hero}>
          <Sparkles count={9} seed={4} />
          <Cloud className={`${s.cloud} ${s.cloudA}`} />
          <p className={s.arabic} lang="ar" dir="rtl">بِسْمِ اللّٰهِ الرَّحْمٰنِ الرَّحِيْمِ</p>
          <MoonBaby className={s.heroArt} />
          <p className={s.script}>Alhamdulillah, telah hadir</p>
          <h1 className={s.heroName}>{babies.map(baby => baby.name).join(" & ")}</h1>
          {parts.day ? <p className={s.heroDate}>{parts.weekday}, {parts.day} {parts.month} {parts.year}</p> : <p className={s.heroDate}>{DATE_TBA}</p>}
        </header>

        <section className={s.section} aria-labelledby="aq-salam">
          <h2 id="aq-salam" className={s.salam}>Assalamu&rsquo;alaikum Warahmatullahi Wabarakatuh</h2>
          <p className={s.lead}>Dengan penuh rasa syukur atas karunia Allah Subhanahu wa Ta&rsquo;ala, kami mengundang Bapak/Ibu/Saudara/i untuk hadir dan mendoakan pada tasyakuran {label.toLowerCase()} buah hati kami.</p>
          <figure className={s.quote}>
            <Cloud className={s.quoteCloud} />
            <blockquote>&ldquo;{quote.text}&rdquo;</blockquote>
            {quote.source && <figcaption>{quote.source}</figcaption>}
          </figure>
        </section>

        <OpeningExtras />

        <section className={`${s.section} ${s.sky}`} aria-labelledby="aq-baby">
          <Sparkles count={7} seed={6} />
          <Head id="aq-baby" kicker="Kenalan, yuk!" title={babies.length > 1 ? "Si Kecil Kami" : "Profil Si Kecil"} />
          {babies.map((baby, index) => (
            <article key={index} className={s.baby}>
              <div className={s.badge}>
                {baby.photo ? <Photo src={baby.photo} alt={`Foto ${baby.nick}`} className={s.badgePhoto} /> : <span className={s.badgeInitial} aria-hidden>{initial(baby.nick || baby.name)}</span>}
                <svg className={s.badgeStar} viewBox="0 0 24 24" aria-hidden="true"><path d={STAR} fill="currentColor" /></svg>
              </div>
              <h3>{baby.name}</h3>
              {baby.nick && baby.nick !== baby.name && <p className={s.nick}>Panggil aku <b>{baby.nick}</b></p>}
              {baby.birth && (
                <dl className={s.facts}>
                  <div><dt>Lahir</dt><dd>{formatDate(baby.birth, { weekday: "long", day: "numeric", month: "long", year: "numeric" })}</dd></div>
                  {baby.birth.includes("T") && <div><dt>Pukul</dt><dd>{formatDate(baby.birth, { hour: "2-digit", minute: "2-digit" })} WIB</dd></div>}
                </dl>
              )}
              {baby.meaning && <div className={s.meaning}><small>Arti nama</small><p>{baby.meaning}</p></div>}
              {baby.parents && <p className={s.parents}>{baby.parents}</p>}
            </article>
          ))}
        </section>

        <section className={s.section} aria-labelledby="aq-doa">
          <Head id="aq-doa" kicker="Doa untuk si kecil" title="Untaian Doa" />
          <div className={s.doa}>
            <p className={s.arabic} lang="ar" dir="rtl">{girl ? "أُعِيْذُكِ" : "أُعِيْذُكَ"} بِكَلِمَاتِ اللّٰهِ التَّامَّةِ مِنْ كُلِّ شَيْطَانٍ وَهَامَّةٍ وَمِنْ كُلِّ عَيْنٍ لَامَّةٍ</p>
            <p className={s.translit}>&ldquo;Aku memohonkan perlindungan untukmu dengan kalimat-kalimat Allah yang sempurna, dari setiap setan, binatang berbisa, dan dari setiap pandangan mata yang jahat.&rdquo;</p>
            <cite>HR. Bukhari</cite>
          </div>
          <p className={s.hint}>Ketuk bintang untuk mengaminkan harapan kami</p>
          <ul className={s.hopes}>
            {HOPES.map((hope, index) => {
              const on = lit.includes(index);
              return (
                <li key={hope}>
                  <button type="button" className={on ? `${s.hope} ${s.hopeOn}` : s.hope} onClick={() => light(index)} aria-pressed={on}>
                    <svg viewBox="0 0 24 24" aria-hidden="true"><path d={STAR} /></svg>
                    <span>{hope}</span>
                    {on && <small>Aamiin</small>}
                  </button>
                </li>
              );
            })}
          </ul>
        </section>

        <section className={`${s.section} ${s.sky}`} aria-labelledby="aq-count">
          <Head id="aq-count" kicker="Sebentar lagi" title="Hitung Mundur" />
          {countdown.valid ? (
            <div className={s.count} role="timer" aria-label={`${countdown.days} hari ${countdown.hours} jam ${countdown.minutes} menit lagi`}>
              {[[countdown.days, "Hari"], [countdown.hours, "Jam"], [countdown.minutes, "Menit"], [countdown.seconds, "Detik"]].map(([value, unit]) => (
                <div key={unit} className={s.countBox}><Cloud className={s.countCloud} /><b><Tick value={value} /></b><small>{unit}</small></div>
              ))}
            </div>
          ) : <p className={s.tba}>{DATE_TBA}</p>}
        </section>

        <section className={s.section} aria-labelledby="aq-events">
          <Head id="aq-events" kicker="Catat tanggalnya" title="Waktu & Tempat" />
          <div className={s.events}>
            {data.events.map((event, index) => {
              const href = mapsHref(data, event);
              const day = dateParts(event.date || data.date);
              return (
                <article key={event.name + index} className={s.event}>
                  <div className={s.eventDay}>{day.day ? <><b>{day.day}</b><span>{day.monthShort}</span></> : <span>TBA</span>}</div>
                  <div className={s.eventText}>
                    <h3>{event.name}</h3>
                    <p><Icon d={icons.calendar} size={14} strokeWidth={2.4} />{formatDate(event.date || data.date)}</p>
                    {event.time && <p><Icon d={icons.clock} size={14} strokeWidth={2.4} />{event.time}</p>}
                    <strong>{event.venue}</strong>
                    {event.address && <span>{event.address}</span>}
                    {href && <a className={s.btnSm} href={href} target="_blank" rel="noreferrer"><Icon d={icons.mapPin} size={15} strokeWidth={2.4} />Lihat Peta</a>}
                  </div>
                </article>
              );
            })}
          </div>
        </section>

        <Extras slot="event" />

        {stories.length > 0 && (
          <section className={`${s.section} ${s.sky}`} aria-labelledby="aq-story">
            <Head id="aq-story" kicker="Cerita kecil" title="Perjalanan Kami" />
            <ol className={s.timeline}>
              {stories.map((story, index) => (
                <li key={index}>
                  <span className={s.dot} aria-hidden><svg viewBox="0 0 24 24"><path d={STAR} fill="currentColor" /></svg></span>
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

        {data.gallery.length > 0 && (
          <section className={s.section} aria-labelledby="aq-gallery">
            <Head id="aq-gallery" kicker="Momen manis" title="Galeri" />
            <div className={s.gallery}>
              {data.gallery.map((src, index) => <div key={src + index} className={s.polaroid}><Photo src={src} alt={`Foto galeri ${index + 1}`} /></div>)}
            </div>
          </section>
        )}

        <Extras slot="story" />
        <Extras slot="end" />

        {data.gifts.length > 0 && (
          <section className={`${s.section} ${s.sky}`} aria-labelledby="aq-gift">
            <Head id="aq-gift" kicker="Tanda sayang" title={`Kado untuk ${nick}`} />
            <p className={s.lead}>Doa Anda adalah kado terindah. Bila ingin berbagi tanda sayang, dapat melalui:</p>
            <div className={s.gifts}>
              {data.gifts.map(gift => {
                const info = giftInfo(gift);
                const on = Boolean(info.copy && copied === info.copy);
                return (
                  <div key={gift.id} className={on ? `${s.gift} ${s.giftOn}` : s.gift}>
                    <span className={s.giftIcon}><Icon d={gift.type === "bank" ? BANK : gift.type === "address" ? icons.gift : WALLET} size={19} strokeWidth={2.2} /></span>
                    <div className={s.giftText}>
                      <small>{info.kind}</small>
                      <strong>{info.title}</strong>
                      {info.number && <span className={s.giftNumber}>{info.number}</span>}
                      {info.holder && <span>a.n. {info.holder}</span>}
                      {info.image && <Photo src={info.image} alt="Kode QRIS" className={s.qris} />}
                    </div>
                    {info.copy && (
                      <button type="button" className={on ? `${s.copy} ${s.copyOn}` : s.copy} onClick={() => copy(info.copy)} aria-label={on ? "Tersalin" : `Salin ${info.title}`}>
                        <Icon key={on ? "on" : "off"} d={on ? icons.check : icons.copy} size={16} strokeWidth={2.4} />
                      </button>
                    )}
                  </div>
                );
              })}
            </div>
          </section>
        )}

        <section className={s.section} aria-labelledby="aq-wishes">
          <Head id="aq-wishes" kicker="Konfirmasi & doa" title="Kirim Doa Terbaik" />
          {wishes.status === "sent" ? (
            <div ref={sentRef} className={`${s.form} ${s.sentBox}`} role="status">
              <svg className={s.sentStar} viewBox="0 0 24 24" aria-hidden="true"><path d={STAR} fill="currentColor" /></svg>
              <strong>Terima kasih, Jazakumullah khairan!</strong>
              <p>{demo ? "Ini pratinjau — ucapan hanya tampil di daftar." : wishes.pending ? "Doamu akan tampil setelah disetujui keluarga." : rsvp.status === "sent" ? "Konfirmasi dan doamu sudah kami terima." : "Doamu sudah kami terima."}</p>
              <button type="button" className={s.btn} onClick={() => { wishes.reset(); rsvp.reset(); }}>Tulis Lagi</button>
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
                <div className={s.closed} role="status"><strong>Konfirmasi kehadiran sudah ditutup</strong><p>Terima kasih atas doa dan perhatiannya. Doa untuk si kecil masih bisa dikirim lewat form ini.</p></div>
              ) : (
                <div className={s.field}>
                  <span>Kehadiran</span>
                  <div className={s.choices} role="radiogroup" aria-label="Kehadiran">
                    {(["yes", "maybe", "no"] as Attendance[]).map(value => (
                      <button key={value} type="button" role="radio" aria-checked={attendance === value} className={attendance === value ? s.choiceOn : undefined} onClick={() => setAttendance(value)}>{ATTEND[value]}</button>
                    ))}
                  </div>
                </div>
              )}
              {!rsvpClosed && attendance !== "no" && <GuestCount label="Jumlah tamu" className={s.guests} buttonClassName={s.step} />}
              {!rsvpClosed && attendance !== "no" && <DietaryField className={s.field} />}
              <label className={s.field}><span>Doa &amp; ucapan</span><textarea name="message" required maxLength={500} rows={3} placeholder={`Tulis doa untuk ${nick}…`} /></label>
              {(wishes.status === "error" || rsvp.status === "error") && <p className={s.error} role="alert">Belum terkirim. Periksa koneksi lalu coba lagi.</p>}
              <button type="submit" className={s.btn} disabled={wishes.status === "sending"}>{wishes.status === "sending" ? "Mengirim…" : "Kirim Doa"}</button>
            </form>
          )}
          <div className={s.wishes}>
            {wishes.wishes.length === 0 && <p className={s.empty}>Belum ada doa. Jadilah yang pertama mendoakan {nick}.</p>}
            {wishes.wishes.slice(0, 12).map((wish, index) => (
              <article key={wish.id} className={s.wish} data-tone={index % 3}>
                <p className={s.wishHead}><strong>{wish.name}</strong>{wish.attendance && <small>{ATTEND[wish.attendance]}</small>}</p>
                <p>{wish.message}</p>
              </article>
            ))}
          </div>
        </section>

        <footer className={s.closing}>
          <Sparkles count={10} seed={8} />
          <MoonBaby className={s.closingArt} />
          <p className={s.lead}>Atas kehadiran dan doa restu Bapak/Ibu/Saudara/i, kami ucapkan terima kasih.</p>
          <p className={s.salamEnd}>Wassalamu&rsquo;alaikum Warahmatullahi Wabarakatuh</p>
          <p className={s.script}>Kami yang berbahagia</p>
          <p className={s.closingNames}>{parents || `Keluarga ${nick}`}</p>
          <a href="/" target="_blank" rel="noreferrer" className={s.made}>dibuat dengan ♥ di Rawuh</a>
          <Cloud className={`${s.cloud} ${s.cloudBottom}`} />
        </footer>
      </main>
    </ThemeShell>
  );
}
