"use client";
// Theme "Streaming" — undangan ala serial streaming (design: Undangan — Tema Streaming (Sekar & Damar)).
import { useState } from "react";
import {
  Lucide, Photo, RsvpForm, Sheet, ThemeShell, WishForm, coupleInitials, coupleLabel, dateParts, formatDate, giftInfo, guestLabel,
  mapsHref, storyItems, toDate, useCopy, useCountdown, useRsvp, useSheets, useWishes, type Attendance, type ThemeProps, type ThemeTint,
} from "../kit";
import type { InvitationData } from "../../types";
import { ic } from "./icons";
import s from "./styles.module.css";

const FONTS = ["Inter:wght@400;500;600;700;800;900", "Bebas Neue"];
const tint: ThemeTint = {
  "--t-accent": "#e50914", "--t-accent-ink": "#ffffff", "--t-bg": "#181818", "--t-ink": "#ffffff", "--t-muted": "#b3b3b3",
  "--t-line": "#333333", "--t-field": "#232323", "--t-radius": "4px", "--t-font": "Inter, system-ui, sans-serif",
};
const DEMO_WISHES = [
  { id: "w1", name: "Laras", attendance: "yes" as Attendance, message: "Akhirnya season final! Udah nunggu dari episode 1. Selamat Sekar & Damar!" },
  { id: "w2", name: "Pakde Joko", attendance: "yes" as Attendance, message: "Ceritanya bagus, pemerannya serasi. Semoga langgeng sampai musim ke-100." },
  { id: "w3", name: "Nadia", attendance: "no" as Attendance, message: "Maaf belum bisa nonton langsung, doa terbaik dari Medan." },
];
const DEMO_RUNTIME = ["45m", "52m", "48m"];
const AVATARS = ["#0071eb", "#e87c03", "#46d369"];
const ATTEND: Record<Attendance, string> = { yes: "Hadir", maybe: "Ragu", no: "Berhalangan" };
const pad = (n: number) => String(n).padStart(2, "0");

function StatusBar({ time }: { time: string }) {
  return (
    <div className={s.status} aria-hidden>
      <span>{time}</span>
      <span className={s.statusIcons}><Lucide icon={ic.signal} color="#fff" /><Lucide icon={ic.wifi} color="#fff" /><Lucide icon={ic.batteryFull} color="#fff" /></span>
    </div>
  );
}

function city(address: string) {
  const parts = address.split(",").map(part => part.trim()).filter(Boolean);
  return parts.length > 1 ? parts[parts.length - 1] : "";
}

function parentsOnly(text?: string) {
  return text?.replace(/^(putr[ai]\s+(ke-?\d+\s+)?(dari\s+)?)/i, "").trim();
}

function calendarHref(data: InvitationData) {
  const start = toDate(data.events[0]?.date ?? data.date);
  if (!start) return undefined;
  const end = new Date(start.getTime() + 3 * 3600e3);
  const fmt = (d: Date) => d.toISOString().replace(/[-:]|\.\d{3}/g, "");
  const params = new URLSearchParams({
    action: "TEMPLATE", text: `${data.eventLabel ?? "Pernikahan"} ${coupleLabel(data)}`, dates: `${fmt(start)}/${fmt(end)}`,
    location: [data.place, data.address].filter(Boolean).join(", "),
  });
  return `https://calendar.google.com/calendar/render?${params.toString()}`;
}

export default function StreamingTheme({ data, slug, guestToken, demo, skipCover }: ThemeProps) {
  const couple = coupleLabel(data);
  const brand = coupleInitials(data);
  const parts = dateParts(data.date);
  const date = toDate(data.date);
  const month = date ? pad(Number(new Intl.DateTimeFormat("en", { timeZone: "Asia/Jakarta", month: "numeric" }).format(date))) : "";
  const clock = parts.day ? `${pad(Number(parts.day))}:${month}` : "20:06";
  const where = city(data.address);
  const label = data.eventLabel ?? "Pernikahan";
  const countdown = useCountdown(data.date);
  const rsvp = useRsvp({ slug, guestToken, demo });
  const wishes = useWishes({ slug, guestToken, demo, seed: DEMO_WISHES });
  const sheets = useSheets();
  const { copy, copied } = useCopy();
  const [showAll, setShowAll] = useState(false);
  const stories = storyItems(data);
  const hero = data.gallery[0];
  const photos = data.gallery.length > 1 ? data.gallery.slice(1) : data.gallery;
  const [trailer, big, small1, small2] = photos;
  const extra = demo ? 21 : Math.max(0, photos.length - 4);
  const parents = [parentsOnly(data.couple.brideParents), parentsOnly(data.couple.groomParents)].filter(Boolean).join(", ");
  const cast = [data.couple.brideFull ?? data.couple.bride, data.couple.groomFull ?? data.couple.groom].join(", ");
  const calendar = calendarHref(data);
  const finalThumb = data.gallery[data.gallery.length - 1] ?? hero;
  const shortDate = formatDate(data.date, { day: "numeric", month: "short", year: "numeric" });

  return (
    <ThemeShell
      fonts={FONTS}
      background="#0b0b0b"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <StatusBar time={clock} />
          <div className={s.coverNav}>
            <span aria-hidden style={{ width: 22 }} />
            <span className={s.logo}>{brand}</span>
            <Lucide icon={ic.pencil} size={22} color="#fff" />
          </div>
          <div className={s.picker}>
            <h1>Siapa yang menonton?</h1>
            <button type="button" className={s.guest} onClick={open} aria-label={`Buka undangan untuk ${guestLabel(data)}`}>
              <span className={s.guestAvatar}><Lucide icon={ic.smile} size={72} color="#fff" strokeWidth={1.8} /></span>
              <span className={s.guestName}><small>Kepada Yth.</small><strong>{guestLabel(data)}</strong></span>
            </button>
            <div className={s.others} aria-hidden>
              {[["Keluarga", "#0071eb"], ["Sahabat", "#e87c03"], ["Rekan", "#46d369"]].map(([name, bg]) => (
                <span key={name}><i style={{ background: bg }}><Lucide icon={ic.smile} size={34} color="#fff" /></i>{name}</span>
              ))}
            </div>
          </div>
          <div className={s.coverBottom}>
            <p className={s.series}><b>R</b>S E R I E S &nbsp;·&nbsp; THE WEDDING</p>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.play} size={18} color="#fff" />Mulai Menonton Undangan</button>
            <p className={s.coverNote}>Mohon maaf apabila ada kesalahan penulisan nama &amp; gelar.</p>
          </div>
        </section>
      )}
    >
      <header id="st-top" className={s.billboard}>
        <Photo src={hero} alt={`Foto ${couple}`} className={s.billboardImg} />
        <div className={s.billTop}>
          <StatusBar time={clock} />
          <div className={s.nav}>
            <span className={s.logo}>{brand}</span>
            <span className={s.navIcons} aria-hidden>
              <Lucide icon={ic.cast} size={22} color="#fff" /><Lucide icon={ic.search} size={22} color="#fff" />
              <i><Lucide icon={ic.smile} size={16} color="#fff" /></i>
            </span>
          </div>
          <nav className={s.chips} aria-label="Bagian undangan">
            {stories.length > 0 && <a href="#st-kisah">Kisah</a>}
            {photos.length > 0 && <a href="#st-galeri">Galeri</a>}
            <a href="#st-acara">Acara</a>
          </nav>
        </div>
        <div className={s.billBottom}>
          <p className={s.seriesSm}><b>R</b>S E R I E S</p>
          <h1>{couple.toUpperCase()}</h1>
          <p className={s.kind}>{label.toUpperCase()}</p>
          <p className={s.top10}><span aria-hidden><small>TOP</small>10</span>#1 {label} Paling Ditunggu Tahun Ini</p>
          <p className={s.meta}>
            <b>100% Cocok</b>{parts.year && <span>{parts.year}</span>}<i>SU</i><span>Romansa · Keluarga{where ? ` · ${where}` : ""}</span>
          </p>
          <div className={s.heroBtns}>
            <button type="button" className={s.playBtn} onClick={sheets.openRsvp}><Lucide icon={ic.play} size={18} color="#000" />Hadiri</button>
            {calendar
              ? <a className={s.listBtn} href={calendar} target="_blank" rel="noreferrer"><Lucide icon={ic.plus} size={18} color="#fff" />Simpan Tanggal</a>
              : <a className={s.listBtn} href="#st-acara"><Lucide icon={ic.plus} size={18} color="#fff" />Lihat Jadwal</a>}
          </div>
        </div>
      </header>

      <main className={s.body}>
        <section className={s.synopsis} aria-label="Sinopsis">
          {data.couple.note && <p className={s.lead}>{data.couple.note}</p>}
          <p className={s.credits}>Pemeran: {cast}{parents && <><br />Sutradara: {parents} (orang tua mempelai)</>}</p>
          <div className={s.premiere}>
            <p className={s.premiereHead}><Lucide icon={ic.bellRing} size={14} color="#e50914" />TAYANG PERDANA</p>
            <div className={s.count} role="timer" aria-label={`${countdown.days} hari ${countdown.hours} jam ${countdown.minutes} menit lagi`}>
              {[[countdown.days, "HARI"], [countdown.hours, "JAM"], [countdown.minutes, "MENIT"], [countdown.seconds, "DETIK"]].map(([value, unit]) => (
                <div key={unit}><b>{value}</b><small>{unit}</small></div>
              ))}
            </div>
            <p className={s.premiereDate}>{formatDate(data.date)}{where ? ` · ${where}` : ""}</p>
          </div>
        </section>

        <section className={s.section} aria-labelledby="st-cast">
          <h2 id="st-cast">Pemeran Utama</h2>
          <div className={s.castRow}>
            {[
              { name: data.couple.brideFull ?? data.couple.bride, parents: data.couple.brideParents, photo: data.couple.bridePhoto ?? photos[0] ?? hero },
              { name: data.couple.groomFull ?? data.couple.groom, parents: data.couple.groomParents, photo: data.couple.groomPhoto ?? photos[1] ?? hero },
            ].map((person, index) => (
              <article key={index} className={s.castCard}>
                <Photo src={person.photo} alt={person.name} />
                <strong>{person.name}</strong>
                {person.parents && <p>{person.parents}</p>}
              </article>
            ))}
          </div>
        </section>

        {stories.length > 0 && (
          <section id="st-kisah" className={s.section} aria-labelledby="st-episodes">
            <div className={s.head}>
              <h2 id="st-episodes">Episode · Kisah Kami</h2>
              <span className={s.season} aria-hidden>Musim 1<Lucide icon={ic.chevronDown} size={14} color="#fff" /></span>
            </div>
            <ol className={s.episodes}>
              {stories.map((story, index) => (
                <li key={index} className={s.episode}>
                  <div className={s.epTop}>
                    <div className={s.thumb}>
                      <Photo src={story.image ?? data.gallery[(index + 1) % Math.max(1, data.gallery.length)]} alt="" />
                      <span className={s.thumbPlay} aria-hidden><Lucide icon={ic.play} size={14} color="#fff" /></span>
                      <span className={s.thumbBar} aria-hidden><i /></span>
                    </div>
                    <div className={s.epText}>
                      <strong>{index + 1}. {story.title}</strong>
                      {(story.date || demo) && <small>{[story.date, demo ? DEMO_RUNTIME[index] : ""].filter(Boolean).join(" · ")}</small>}
                    </div>
                  </div>
                  {story.body && <p>{story.body}</p>}
                </li>
              ))}
              <li className={s.episode}>
                <div className={s.epTop}>
                  <div className={s.thumb}>
                    <Photo src={finalThumb} alt="" />
                    <span className={s.thumbPlay} aria-hidden><Lucide icon={ic.play} size={14} color="#fff" /></span>
                  </div>
                  <div className={s.epText}>
                    <strong>{stories.length + 1}. Episode Final: Sah!</strong>
                    <small className={s.live}>{shortDate} · Live</small>
                  </div>
                </div>
                <p>Saksikan langsung. Kehadiranmu melengkapi cerita.</p>
              </li>
            </ol>
          </section>
        )}

        {photos.length > 0 && (
          <section id="st-galeri" className={s.gallery} aria-labelledby="st-gallery">
            <div className={s.galleryHead}>
              <h2 id="st-gallery">Galeri Momen</h2>
              <span>{demo ? "24 foto · 3 video" : `${photos.length} foto`}</span>
            </div>
            <div className={s.tabs} aria-hidden><span className={s.tabOn}>Foto</span><span>Trailer</span><span>Di Balik Layar</span></div>
            <div className={s.galleryBody}>
              <figure className={s.trailer}>
                <Photo src={trailer} alt={demo ? "Senja di Parangtritis" : `Foto ${couple}`} />
                <div className={s.trTop}><span><b>R</b>TRAILER PREWEDDING</span><i>HD</i></div>
                <span className={s.trPlay} aria-hidden><Lucide icon={ic.play} size={22} color="#fff" /></span>
                <figcaption className={s.trBottom}>
                  <span><strong>{demo ? "Senja di Parangtritis" : couple}</strong>{demo && <small>0:48 / 2:34</small>}</span>
                  {demo && <span className={s.trBar} aria-hidden><i /><b /></span>}
                </figcaption>
              </figure>
              {big && (
                <div className={s.grid}>
                  <figure className={s.big}>
                    <Photo src={big} alt={demo ? "Taman Sari" : "Foto galeri 2"} />
                    {demo && <figcaption><Lucide icon={ic.mapPin} size={10} color="#fff" />Taman Sari</figcaption>}
                  </figure>
                  {small1 && (
                    <div className={s.stack}>
                      <Photo src={small1} alt="Foto galeri 3" />
                      {small2 && (
                        <button type="button" className={s.more} onClick={() => setShowAll(true)} disabled={extra === 0} aria-label={extra ? `Lihat ${extra} foto lainnya` : "Foto galeri 4"}>
                          <Photo src={small2} />
                          {extra > 0 && <span><b>+{extra}</b><small>FOTO LAINNYA</small></span>}
                        </button>
                      )}
                    </div>
                  )}
                </div>
              )}
              {showAll && photos.length > 4 && (
                <div className={s.allGrid}>
                  {photos.slice(4).map((src, index) => <Photo key={src + index} src={src} alt={`Foto galeri ${index + 5}`} />)}
                </div>
              )}
              {photos.length > 4 && (
                <button type="button" className={s.moreBtn} onClick={() => setShowAll(v => !v)} aria-expanded={showAll}>
                  <Lucide icon={ic.images} size={16} color="#fff" />{showAll ? "Sembunyikan" : `Lihat Semua ${demo ? 24 : photos.length} Momen`}
                </button>
              )}
            </div>
          </section>
        )}

        <section id="st-acara" className={s.section} aria-labelledby="st-events">
          <h2 id="st-events">Jadwal Tayang</h2>
          {data.events.map((event, index) => {
            const p = dateParts(event.date || data.date);
            const href = mapsHref(data, event);
            return (
              <article key={event.name + index} className={s.event}>
                <div className={s.dateBox}><small>{p.monthShort}</small><b>{p.day}</b><span>{p.weekdayShort}</span></div>
                <div className={s.eventInfo}>
                  <strong><Lucide icon={index === 0 ? ic.moonStar : ic.sparkles} size={14} color="#e50914" />{event.name}</strong>
                  <em>{event.time}</em>
                  <span>{event.venue}</span>
                  {event.address && <small>{event.address}</small>}
                  {href && <a href={href} target="_blank" rel="noreferrer"><Lucide icon={ic.mapPin} size={12} color="#fff" />Buka Maps</a>}
                </div>
              </article>
            );
          })}
        </section>

        {data.gifts.length > 0 && (
          <section id="st-kado" className={s.section} aria-labelledby="st-gift">
            <h2 id="st-gift">Pilih Paket Hadiah</h2>
            {data.gifts.map(gift => {
              const info = giftInfo(gift);
              const isAddress = gift.type === "address";
              return (
                <div key={gift.id} className={isAddress ? `${s.gift} ${s.giftPlain}` : s.gift}>
                  <div>
                    <strong>{isAddress ? "Kirim Kado" : gift.type === "qris" ? "QRIS" : "Amplop Digital"}</strong>
                    <small>{isAddress ? info.number : [`${info.title} ${info.number}`.trim(), info.holder ? `a.n. ${info.holder}` : ""].filter(Boolean).join(" · ")}</small>
                    {info.image && <Photo src={info.image} alt="Kode QRIS" className={s.qris} />}
                  </div>
                  {info.copy && (
                    <button type="button" className={s.copy} onClick={() => copy(info.copy)}>
                      <Lucide icon={ic.copy} size={12} color="#000" />{copied === info.copy ? "Tersalin" : "Salin"}
                    </button>
                  )}
                </div>
              );
            })}
          </section>
        )}

        <section className={s.section} aria-labelledby="st-wishes">
          <div className={s.head}>
            <h2 id="st-wishes">Ulasan Penonton</h2>
            <span className={s.liked}><Lucide icon={ic.thumbsUp} size={14} color="#46d369" />{demo ? "Disukai 98%" : `${wishes.wishes.length} ulasan`}</span>
          </div>
          <button type="button" className={s.input} onClick={sheets.openWish}>
            <Lucide icon={ic.messageSquare} size={16} color="#b3b3b3" /><span>Tulis ucapan &amp; doa…</span><b>Kirim</b>
          </button>
          {wishes.wishes.length === 0 && <p className={s.empty}>Belum ada ulasan. Jadilah penonton pertama yang memberi ucapan!</p>}
          {wishes.wishes.slice(0, 8).map((wish, index) => (
            <article key={wish.id} className={s.review}>
              <span className={s.avatar} style={{ background: AVATARS[index % AVATARS.length] }} aria-hidden><Lucide icon={ic.smile} size={18} color="#fff" /></span>
              <div>
                <p className={s.reviewHead}>
                  <strong>{wish.name}</strong>
                  {wish.attendance && <span className={wish.attendance === "yes" ? s.tagYes : s.tag}>{ATTEND[wish.attendance]}</span>}
                </p>
                <p>{wish.message}</p>
              </div>
            </article>
          ))}
        </section>

        <footer className={s.end}>
          <p className={s.endTitle}>{couple.toUpperCase()}</p>
          <p>Terima kasih telah menjadi bagian dari cerita kami.</p>
          <a href="/" target="_blank" rel="noreferrer">dibuat dengan ♥ di Rawuh</a>
        </footer>
      </main>

      <nav className={s.bottom} aria-label="Aksi undangan">
        <button type="button" className={s.rsvp} onClick={sheets.openRsvp}><Lucide icon={ic.ticket} size={18} color="#fff" />Konfirmasi Kehadiran</button>
        <div className={s.tabBar}>
          <a href="#st-top" className={s.tabActive}><Lucide icon={ic.house} size={20} />Beranda</a>
          {stories.length > 0 && <a href="#st-kisah"><Lucide icon={ic.clapperboard} size={20} />Kisah</a>}
          {photos.length > 0 && <a href="#st-galeri"><Lucide icon={ic.images} size={20} />Galeri</a>}
          {data.gifts.length > 0
            ? <a href="#st-kado"><Lucide icon={ic.gift} size={20} />Kado</a>
            : <button type="button" onClick={sheets.openWish}><Lucide icon={ic.messageSquare} size={20} />Ucapan</button>}
        </div>
      </nav>

      <Sheet open={sheets.sheet === "rsvp"} onClose={sheets.close} title="Konfirmasi Kehadiran" tint={tint}>
        <RsvpForm rsvp={rsvp} guestName={data.guestName} demo={demo} labels={{ submit: "Kirim Konfirmasi", yes: "Hadir", maybe: "Mungkin", no: "Berhalangan" }} />
      </Sheet>
      <Sheet open={sheets.sheet === "wish"} onClose={sheets.close} title="Tulis Ulasan & Doa" tint={tint}>
        <WishForm wishes={wishes} guestName={data.guestName} demo={demo} />
      </Sheet>
    </ThemeShell>
  );
}
