"use client";
// Theme "Surat Vintage" — sepucuk surat lama bernuansa sepia: amplop bersegel lilin, perangko berperforasi, cap pos.
import { useEffect, useId, useRef, useState, type CSSProperties, type ReactNode } from "react";
import {
  DietaryField, Extras, GuestCount, Lucide, Photo, ThemeShell, Tick, coupleLabel, dateParts, formatDate, giftInfo, guestLabel,
  mapsHref, storyItems, useCopy, useCountdown, useMusic, DATE_TBA, useRsvp, useThankYou, useWishes, type Attendance, type ThemeProps, type Wish,
} from "../kit";
import { tableLabel } from "../extras";
import type { InvitationData } from "../../types";
import { celebrate } from "@/lib/celebrate";
import { ic } from "./icons";
import s from "./styles.module.css";

const FONTS = ["IM Fell English:ital@0;1", "Special Elite", "Pinyon Script"];
const ATTEND: Record<Attendance, string> = { yes: "Hadir", maybe: "Ragu", no: "Berhalangan" };
const DEMO_WISHES: Wish[] = [
  { id: "w1", name: "Bu Laras", attendance: "yes", message: "Seperti surat yang sampai ke alamat yang tepat. Selamat menempuh hidup baru, Kirana dan Arya." },
  { id: "w2", name: "Dimas & Nadia", attendance: "maybe", message: "Semoga rumah tangga kalian hangat seperti tulisan tangan di surat pertama. Barakallah." },
];

const ART = "/themes/art/surat-vintage";

/** Decorative painted image (never opens the photo lightbox). */
function Art({ src, className, w, h, eager }: { src: string; className?: string; w: number; h: number; eager?: boolean }) {
  return (
    // eslint-disable-next-line @next/next/no-img-element -- static painted ornament
    <img src={`${ART}/${src}.webp`} alt="" aria-hidden width={w} height={h} className={className} data-nolightbox
      loading={eager ? "eager" : "lazy"} fetchPriority={eager ? "high" : undefined} decoding="async" draggable={false} />
  );
}

function initials(data: InvitationData) {
  const a = data.couple.bride?.trim().charAt(0) ?? "";
  const b = data.couple.groom?.trim().charAt(0) ?? "";
  return b ? `${a}${b}`.toUpperCase() : a.toUpperCase();
}

function WaxSeal({ letters, className, eager }: { letters: string; className?: string; eager?: boolean }) {
  return (
    <span className={`${s.wax} ${className ?? ""}`} aria-hidden="true">
      <Art src="seal" w={220} h={220} eager={eager} />
      <b className={s.sealText}>{letters}</b>
    </span>
  );
}

function Postmark({ city, date, className }: { city: string; date: string; className?: string }) {
  const id = useId().replace(/:/g, "");
  return (
    <svg className={className} viewBox="0 0 210 112" aria-hidden="true" focusable="false">
      <defs><path id={`pm${id}`} d="M56 56m-40 0a40 40 0 1 1 80 0a40 40 0 1 1-80 0" /></defs>
      <g fill="none" stroke="currentColor">
        <circle cx="56" cy="56" r="50" strokeWidth="2" />
        <circle cx="56" cy="56" r="31" strokeWidth="1.3" />
        {[0, 1, 2, 3, 4].map(line => <path key={line} d={`M112 ${28 + line * 14}c12-6 22 6 34 0s22-6 34 0 18 4 26 0`} strokeWidth="2" />)}
      </g>
      <text className={s.pmRing}><textPath href={`#pm${id}`} startOffset="2%">{`· POS ${city.toUpperCase()} · KANTOR CINTA ·`}</textPath></text>
      <text x="56" y="54" textAnchor="middle" className={s.pmDate}>{date}</text>
      <text x="56" y="68" textAnchor="middle" className={s.pmSmall}>SAMPAI</text>
    </svg>
  );
}

/** A small perforated postage stamp. */
function Stamp({ children, className, style }: { children: ReactNode; className?: string; style?: CSSProperties }) {
  return <span className={`${s.stamp} ${className ?? ""}`} style={style}><span className={s.stampFace}>{children}</span></span>;
}

function Rose() {
  return <Art src="rose" className={s.rose} w={120} h={226} eager />;
}

function Flourish() {
  return <Art src="flourish" className={s.flourish} w={320} h={21} />;
}

function Head({ id, kicker, title }: { id: string; kicker: string; title: string }) {
  return (
    <div className={s.head}>
      <p className={s.label}>{kicker}</p>
      <h2 id={id}>{title}</h2>
      <Flourish />
    </div>
  );
}

function city(address?: string) {
  const parts = (address ?? "").split(",").map(part => part.trim()).filter(Boolean);
  return parts.length > 1 ? parts[parts.length - 1].replace(/\s*\d{5}$/, "") : "";
}

/** "Putra sulung dari\nBapak Darmawan & Ibu Lestari" → "Darmawan" */
function father(parents?: string) {
  const match = /(?:Bapak|Bpk\.?)\s+([^&\n]+?)\s*(?:&|\n|$)/i.exec(parents ?? "");
  return match?.[1].trim();
}

function plainName(guest?: string) {
  if (!guest || guest === "Tamu Undangan") return "";
  return guest.replace(/^(bapak|ibu|bpk\.?|sdr\.?|saudara|saudari)\s+/i, "").replace(/\s*(&|dan)\s*keluarga$/i, "").trim();
}

/** Islamic salam only when the invitation itself reads as an Islamic ceremony. */
function islamic(data: InvitationData) {
  return data.events.some(event => /akad|ijab|walimah/i.test(event.name)) || /\bQS\b|Q\.S\./.test(data.extras?.quote?.source ?? "");
}

export default function SuratVintageTheme({ data, slug, guestToken, demo, skipCover }: ThemeProps) {
  const couple = coupleLabel(data);
  const label = data.eventLabel ?? "Pernikahan";
  const parts = dateParts(data.date);
  const where = city(data.address) || city(data.events[0]?.address);
  const mark = parts.day ? `${parts.day} ${parts.monthShort} ${parts.year}` : "SEGERA";
  const countdown = useCountdown(data.date);
  const rsvp = useRsvp({ slug, guestToken, demo });
  const wishes = useWishes({ slug, guestToken, demo, seed: DEMO_WISHES });
  const thanks = useThankYou();
  const rsvpClosed = thanks.active || rsvp.status === "closed";
  const { copy, copied } = useCopy();
  const music = useMusic(data.music);
  const [attendance, setAttendance] = useState<Attendance>("yes");
  const [unsealing, setUnsealing] = useState(false);
  const stories = storyItems(data);
  const gallery = data.gallery;
  const hero = gallery[0];
  const letters = initials(data);
  const muslim = islamic(data);
  const quote = data.extras?.quote && data.extras.quote.enabled !== false ? data.extras.quote : undefined;
  const families = [father(data.couple.brideParents), father(data.couple.groomParents)].filter(Boolean).join(" & ");
  const table = tableLabel(data.guestTable);
  const sentRef = useRef<HTMLDivElement>(null);
  useEffect(() => { if (wishes.status === "sent") celebrate(sentRef.current); }, [wishes.status]);

  const people = [
    { key: "bride", short: data.couple.bride, name: data.couple.brideFull ?? data.couple.bride, parents: data.couple.brideParents, photo: data.couple.bridePhoto },
    { key: "groom", short: data.couple.groom, name: data.couple.groomFull ?? data.couple.groom, parents: data.couple.groomParents, photo: data.couple.groomPhoto },
  ].filter(person => person.short || person.name);

  const unseal = (open: () => void) => {
    if (unsealing) return;
    const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    setUnsealing(true);
    window.setTimeout(open, reduce ? 0 : 820);
  };

  return (
    <ThemeShell
      fonts={FONTS}
      background="#3a2a1c"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={`${s.cover} ${unsealing ? s.unsealing : ""}`}>
          <p className={s.coverKicker}>Sepucuk Surat Undangan {label}</p>
          <h1 className={s.coverNames}><span>{data.couple.bride}</span>{data.couple.groom && <><em>dan</em><span>{data.couple.groom}</span></>}</h1>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.envelope}>
            <Art src="sprig" className={s.coverSprig} w={460} h={312} eager />
            <div className={s.letterPeek} aria-hidden><i /><i /><i /></div>
            <div className={s.envBody}>
              <div className={s.envStamp} aria-hidden>
                <Stamp><Rose /><b>POS CINTA</b></Stamp>
                <Postmark className={s.envPostmark} city={where || "Kota"} date={mark} />
              </div>
              <div className={s.address}>
                <small>Kepada Yth.</small>
                <strong>{guestLabel(data)}</strong>
                {table && <span className={s.table}>{table}</span>}
                <small>di tempat</small>
              </div>
            </div>
            <div className={s.flap} aria-hidden />
            <WaxSeal className={s.seal} letters={letters} eager />
          </div>
          <button type="button" className={s.openBtn} onClick={() => unseal(open)}><Lucide icon={ic.mailOpen} size={16} color="#f4ead2" />Buka Surat</button>
        </section>
      )}
    >
      <main className={s.main}>
        <header className={s.letter} data-reveal-block>
          <div className={s.airmail} aria-hidden />
          <div className={s.letterMeta}>
            <span>No. {parts.day ? `${parts.day.padStart(2, "0")}/${parts.year}` : "01"}</span>
            <span>{where ? `${where}, ` : ""}{parts.day ? `${parts.day} ${parts.month} ${parts.year}` : DATE_TBA}</span>
          </div>
          <p className={s.perihal}>Perihal: <u>Undangan {label}</u></p>
          {hero && (
            <figure className={s.heroPrint}>
              <span className={s.tape} aria-hidden />
              <Photo src={hero} alt={`Foto ${couple}`} className={s.heroImg} />
              <figcaption>{couple}{parts.year ? `, ${parts.year}` : ""}</figcaption>
            </figure>
          )}
          <p className={s.salam}>{muslim ? "Assalamu'alaikum Warahmatullahi Wabarakatuh," : "Salam sejahtera,"}</p>
          <p className={s.body}>
            Dengan penuh rasa syukur, melalui surat ini kami bermaksud mengundang Bapak/Ibu/Saudara/i untuk hadir dan memberikan doa restu pada hari bahagia kami.
            {data.couple.note ? ` ${data.couple.note}` : ""}
          </p>
          <p className={s.signoff}>Dengan hormat,<span>{couple}</span></p>
        </header>

        {quote && (
          <section className={s.clipping} aria-label="Kutipan">
            <p>“{quote.text}”</p>
            {quote.source && <cite>{quote.source}</cite>}
          </section>
        )}

        <Extras slot="opening" without={["quote"]} />

        <section className={s.section} aria-labelledby="sv-couple">
          <Head id="sv-couple" kicker="Lembar I" title="Yang Berbahagia" />
          <div className={s.people}>
            {people.map((person, index) => (
              <article key={person.key} className={`${s.person} ${index % 2 ? s.personAlt : ""}`}>
                <div className={s.print}>
                  <span className={s.tape} aria-hidden />
                  {person.photo ? <Photo src={person.photo} alt={person.name} className={s.printImg} /> : (
                    <div className={s.monogram} aria-hidden><WaxSeal className={s.monoSeal} letters={person.short.charAt(0).toUpperCase()} /></div>
                  )}
                </div>
                <div className={s.personText}>
                  <p className={s.script}>{person.short}</p>
                  <h3>{person.name}</h3>
                  {person.parents && <p className={s.parents}>{person.parents}</p>}
                </div>
              </article>
            ))}
          </div>
        </section>

        <section className={`${s.section} ${s.countSection}`} aria-labelledby="sv-count">
          <Head id="sv-count" kicker="Lembar II" title="Menuju Hari Bahagia" />
          {countdown.valid ? (
            <div className={s.count} role="timer" aria-label={`${countdown.days} hari ${countdown.hours} jam ${countdown.minutes} menit lagi`}>
              {[[countdown.days, "Hari"], [countdown.hours, "Jam"], [countdown.minutes, "Menit"], [countdown.seconds, "Detik"]].map(([value, unit], index) => (
                <Stamp key={unit} className={s.countStamp} style={{ rotate: `${[-3, 2, -1.5, 3][index]}deg` }}>
                  <b><Tick value={value} /></b><small>{unit}</small>
                </Stamp>
              ))}
            </div>
          ) : <p className={s.countTba}>{DATE_TBA}</p>}
          <div className={s.pmWrap} aria-hidden><Postmark className={s.bigPostmark} city={where || "Kota"} date={mark} /></div>
        </section>

        <section className={s.section} aria-labelledby="sv-events">
          <Head id="sv-events" kicker="Lembar III" title="Waktu & Tempat" />
          <div className={s.events}>
            {data.events.map((event, index) => {
              const p = dateParts(event.date || data.date);
              const maps = mapsHref(data, event);
              return (
                <article key={event.name + index} className={s.postcard}>
                  <div className={s.pcTop}>
                    <div>
                      <p className={s.label}>Kartu Pos No. {index + 1}</p>
                      <h3>{event.name}</h3>
                    </div>
                    <Stamp className={s.pcStamp}><b>{p.day || "—"}</b><small>{p.monthShort || "TBA"}</small></Stamp>
                  </div>
                  <dl className={s.lines}>
                    <div><dt>Hari</dt><dd>{formatDate(event.date || data.date)}</dd></div>
                    {event.time && <div><dt>Pukul</dt><dd>{event.time}</dd></div>}
                    <div><dt>Tempat</dt><dd><strong>{event.venue}</strong>{event.address && <span>{event.address}</span>}</dd></div>
                  </dl>
                  {maps && <a className={s.inkBtn} href={maps} target="_blank" rel="noreferrer"><Lucide icon={ic.mapPin} size={15} />Petunjuk Arah</a>}
                </article>
              );
            })}
          </div>
        </section>

        <Extras slot="event" />

        {stories.length > 0 && (
          <section className={s.section} aria-labelledby="sv-story">
            <Head id="sv-story" kicker="Lembar IV" title="Catatan Perjalanan" />
            <ol className={s.diary}>
              {stories.map((story, index) => (
                <li key={index}>
                  <span className={s.rail} aria-hidden><i /></span>
                  <div className={s.entry}>
                    <p className={s.entryDate}>{story.date ?? `Catatan ${index + 1}`}</p>
                    <h3>{story.title}</h3>
                    {story.body && <p>{story.body}</p>}
                    {story.image && <Photo src={story.image} alt={story.title} className={s.entryImg} />}
                  </div>
                </li>
              ))}
            </ol>
          </section>
        )}

        {gallery.length > 0 && (
          <section className={s.section} aria-labelledby="sv-gallery">
            <Head id="sv-gallery" kicker="Lembar V" title="Album Kenangan" />
            <div className={s.album}>
              {gallery.slice(0, 9).map((src, index) => (
                <figure key={src + index} className={s.albumPrint} style={{ rotate: `${[-2.5, 2, -1.2, 2.6, -2, 1.4, -1.8, 2.2, -1][index]}deg` }}>
                  <Photo src={src} alt={`Foto kenangan ${index + 1}`} />
                  <figcaption>No. {String(index + 1).padStart(2, "0")}</figcaption>
                </figure>
              ))}
            </div>
          </section>
        )}

        <Extras slot="story" />

        <Extras slot="end" />

        {data.gifts.length > 0 && (
          <section className={s.section} aria-labelledby="sv-gift">
            <Head id="sv-gift" kicker="Lembar VI" title="Tanda Kasih" />
            <p className={s.intro}>Doa restu Anda adalah hadiah terindah. Bila berkenan mengirim tanda kasih, dapat melalui wesel berikut:</p>
            <div className={s.gifts}>
              {data.gifts.map(gift => {
                const info = giftInfo(gift);
                const on = Boolean(info.copy) && copied === info.copy;
                const title = gift.type === "bank" ? (/^bank/i.test(info.title) ? info.title : `Bank ${info.title}`) : info.title;
                return (
                  <article key={gift.id} className={`${s.wesel} ${on ? s.weselOn : ""}`}>
                    <div className={s.weselHead}>
                      <Lucide icon={gift.type === "bank" ? ic.landmark : gift.type === "address" ? ic.gift : gift.type === "qris" ? ic.qrCode : ic.wallet} size={16} />
                      <span>{info.kind}</span>
                      <b>{title}</b>
                    </div>
                    {info.number && <p className={s.weselNo}>{info.number}</p>}
                    {info.holder && <p className={s.weselName}>a.n. {info.holder}</p>}
                    {info.image && <Photo src={info.image} alt="Kode QRIS" className={s.qris} />}
                    {info.copy && (
                      <button type="button" className={s.copyBtn} onClick={() => copy(info.copy)} aria-label={on ? "Tersalin" : `Salin ${title}`}>
                        <Lucide key={on ? "on" : "off"} icon={on ? ic.check : ic.copy} size={14} />{on ? "Tersalin" : gift.type === "address" ? "Salin Alamat" : "Salin Nomor"}
                      </button>
                    )}
                  </article>
                );
              })}
            </div>
          </section>
        )}

        <section className={s.section} aria-labelledby="sv-reply">
          <Head id="sv-reply" kicker="Lembar VII" title="Surat Balasan" />
          {wishes.status === "sent" ? (
            <div ref={sentRef} className={`${s.reply} ${s.sentBox}`} role="status">
              <WaxSeal className={s.sentSeal} letters={letters} />
              <p className={s.sent}>Surat balasan Anda sudah kami terima. Terima kasih atas doa dan perhatiannya.</p>
              {!demo && wishes.pending && <p className={s.sentNote}>Ucapan akan tampil setelah disetujui oleh mempelai.</p>}
              {demo && <p className={s.sentNote}>Ini pratinjau, ucapan hanya tampil di daftar di bawah.</p>}
              <button type="button" className={s.submit} onClick={() => { wishes.reset(); rsvp.reset(); }}>Tulis Lagi</button>
            </div>
          ) : (
            <form className={s.reply} onSubmit={event => {
              event.preventDefault();
              const form = new FormData(event.currentTarget);
              const name = String(form.get("name") ?? "").trim();
              const message = String(form.get("message") ?? "").trim();
              const guests = attendance === "no" ? 1 : Number(form.get("guests") ?? 1) || 1;
              if (!name || !message) return;
              void wishes.send(name, message);
              if (!rsvpClosed && rsvp.status !== "sent") void rsvp.submit({ name, attendance, guests, diet: String(form.get("diet") ?? "").trim() || undefined });
            }}>
              <p className={s.replyTo}>Kepada {couple},</p>
              <label className={s.field}><span>Dari</span><input name="name" required maxLength={100} defaultValue={plainName(data.guestName)} placeholder="Nama Anda" autoComplete="name" /></label>
              <label className={s.field}><span>Isi surat</span><textarea name="message" required maxLength={500} rows={4} placeholder="Tuliskan doa dan ucapan…" /></label>
              {rsvpClosed ? (
                <div className={s.closed} role="status"><strong>Konfirmasi kehadiran sudah ditutup</strong><p>Terima kasih atas doa dan perhatiannya. Ucapan masih bisa dikirim lewat surat ini.</p></div>
              ) : (
                <div className={s.choices} role="radiogroup" aria-label="Kehadiran">
                  {(["yes", "maybe", "no"] as Attendance[]).map(value => (
                    <button key={value} type="button" role="radio" aria-checked={attendance === value} className={attendance === value ? s.choiceOn : undefined} onClick={() => setAttendance(value)}>
                      <i aria-hidden />{ATTEND[value]}
                    </button>
                  ))}
                </div>
              )}
              {!rsvpClosed && attendance !== "no" && <GuestCount label="Jumlah tamu" className={s.guests} buttonClassName={s.step} />}
              {!rsvpClosed && attendance !== "no" && <DietaryField className={s.field} />}
              {wishes.status === "error" && <p className={s.error} role="alert">Surat belum terkirim. Coba lagi sebentar lagi.</p>}
              <button type="submit" className={s.submit} disabled={wishes.status === "sending"}><Lucide icon={ic.send} size={15} />{wishes.status === "sending" ? "Mengirim…" : "Kirim Balasan"}</button>
            </form>
          )}
          <div className={s.notes}>
            {wishes.wishes.length === 0 && <p className={s.empty}>Belum ada surat balasan. Jadilah yang pertama menulis.</p>}
            {wishes.wishes.slice(0, 10).map((wish, index) => (
              <article key={wish.id} className={s.note} style={{ rotate: `${index % 2 ? 0.8 : -0.8}deg` }}>
                <p>{wish.message}</p>
                <div><strong>{wish.name}</strong>{wish.attendance && <small>{ATTEND[wish.attendance]}</small>}</div>
              </article>
            ))}
          </div>
        </section>

        <footer className={s.closing}>
          <div className={s.airmail} aria-hidden />
          <p className={s.body}>Merupakan suatu kehormatan dan kebahagiaan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir. Atas kehadiran dan doa restunya, kami ucapkan terima kasih.</p>
          {muslim && <p className={s.salam}>Wassalamu&apos;alaikum Warahmatullahi Wabarakatuh.</p>}
          <p className={s.label}>Hormat kami,</p>
          <p className={s.closingNames}>{couple}</p>
          <p className={s.family}>beserta Keluarga Besar{families ? <><br />Bapak {families}</> : ""}</p>
          <div className={s.footArt}>
            <Art src="sprig" className={s.footSprig} w={460} h={312} />
            <WaxSeal className={s.footSeal} letters={letters} />
          </div>
          <a href="/" target="_blank" rel="noreferrer" className={s.made}>dibuat dengan ♥ di Rawuh</a>
        </footer>
      </main>

      {music.visible && !music.failed && (
        <button type="button" className={`${s.music} ${music.playing ? s.musicOn : ""}`} onClick={music.toggle} aria-pressed={music.playing} {...music.attrs} aria-label={music.playing ? "Matikan musik" : "Putar musik"}>
          <Lucide icon={ic.music} size={18} color="#f4ead2" />
        </button>
      )}
    </ThemeShell>
  );
}
