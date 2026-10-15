"use client";
// Theme "Playlist" — undangan bergaya aplikasi streaming musik gelap (design: Tema Playlist (Kania & Dimas)).
import { useState } from "react";
import {
  Extras, Lucide, Photo, RsvpForm, Sheet, ThemeShell, WishForm, coupleLabel, dateParts, formatDate, giftInfo, guestLabel,
  mapsHref, storyItems, useCopy, useCountdown, useRsvp, useSheets, useWishes, type ThemeProps, type ThemeTint,
} from "../kit";
import { ic } from "./icons";
import s from "./styles.module.css";

const FONTS = ["DM Sans:wght@400;600;700;800"];
const tint: ThemeTint = {
  "--t-accent": "#1db954", "--t-accent-ink": "#000000", "--t-bg": "#1e1e1e", "--t-ink": "#ffffff", "--t-muted": "#b3b3b3",
  "--t-line": "#ffffff26", "--t-field": "#2a2a2a", "--t-radius": "10px", "--t-font": "'DM Sans', system-ui, sans-serif",
};
const DEMO_WISHES = [
  { id: "w1", name: "Rara", message: "Playlist paling ditunggu tahun ini! On repeat terus. Hadir!", created_at: new Date(Date.now() - 2 * 3600e3).toISOString() },
  { id: "w2", name: "Om Hendra", message: "Dari lagu pertama sudah tahu kalian bakal duet selamanya. Selamat!", created_at: new Date(Date.now() - 6 * 3600e3).toISOString() },
];

function city(address: string) {
  const parts = address.split(",").map(part => part.trim()).filter(Boolean);
  return parts[parts.length - 1] ?? "";
}

function Status() {
  return (
    <div className={s.status} aria-hidden>
      24:07
      <span><Lucide icon={ic.signal} /><Lucide icon={ic.wifi} /><Lucide icon={ic.batteryFull} /></span>
    </div>
  );
}

export default function PlaylistTheme({ data, slug, guestToken, demo, skipCover }: ThemeProps) {
  const couple = coupleLabel(data);
  const { couple: c } = data;
  const parts = dateParts(data.date);
  const longDate = formatDate(data.date);
  const where = city(data.address);
  const countdown = useCountdown(data.date);
  const rsvp = useRsvp({ slug, guestToken, demo });
  const wishes = useWishes({ slug, guestToken, demo, seed: DEMO_WISHES });
  const sheets = useSheets();
  const { copy, copied } = useCopy();
  const stories = storyItems(data);
  const [following, setFollowing] = useState<Record<string, boolean>>({});
  const art = data.gallery[0];
  const photos = data.gallery.length > 1 ? data.gallery.slice(1) : data.gallery;
  const firstYear = stories.map(story => story.date?.match(/\d{4}/)?.[0]).find(Boolean);
  const people = [
    { name: c.brideFull ?? c.bride, listeners: "2,1 jt pendengar hati", parents: c.brideParents, photo: c.bridePhoto ?? data.gallery[1] },
    { name: c.groomFull ?? c.groom, listeners: "1 pendengar setia", parents: c.groomParents, photo: c.groomPhoto ?? data.gallery[2] },
  ];
  const daysLeft = countdown.ready ? (countdown.done ? "Hari ini" : `${Number(countdown.days)} hari lagi`) : "";

  return (
    <ThemeShell
      fonts={FONTS}
      background="#000000"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.glow} aria-hidden />
          <Status />
          <div className={s.coverContent}>
            <Photo src={art} alt={`Sampul playlist ${couple}`} className={s.art} />
            <div className={s.coverTitle}>
              <h1>Playlist {data.eventLabel ?? "Pernikahan"} — {couple}</h1>
              {c.note && <p className={s.desc}>{c.note}</p>}
              <p className={s.meta}>
                <span className={s.mark} aria-hidden><Lucide icon={ic.heart} size={10} color="#000" /></span>
                {["Rawuh", demo ? "2.700 suka" : "", longDate, where].filter(Boolean).join(" · ")}
              </p>
              <div className={s.actions}>
                <span className={s.actionsL} aria-hidden>
                  <Lucide icon={ic.heart} size={20} color="#1db954" /><Lucide icon={ic.circleArrowDown} size={20} color="#b3b3b3" /><Lucide icon={ic.ellipsis} size={20} color="#b3b3b3" />
                </span>
                <span className={s.actionsR}>
                  <Lucide icon={ic.shuffle} size={20} color="#1db954" />
                  <button type="button" className={s.playCircle} onClick={open} aria-label="Putar undangan"><Lucide icon={ic.play} size={22} color="#000" /></button>
                </span>
              </div>
            </div>
            <div className={s.guest}>
              <small><Lucide icon={ic.share2} size={12} color="#1db954" />DIBAGIKAN KHUSUS UNTUK</small>
              <strong>{guestLabel(data)}</strong>
              <span>Tekan putar untuk membuka undangan</span>
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.play} color="#000" />Putar Undangan</button>
            <ol className={s.preview} aria-label="Rangkaian acara">
              <li className={s.playing}>
                <Lucide icon={ic.audioLines} size={14} color="#1db954" className={s.no} />
                <div><strong>Intro — Dua Nama Satu Janji</strong><small>{couple}</small></div>
                <Lucide icon={ic.ellipsis} color="#b3b3b3" />
              </li>
              {data.events.map((event, index) => (
                <li key={event.name + index}>
                  <span className={s.no}>{index + 2}</span>
                  <div><strong>{event.name}</strong><small>{event.time}</small></div>
                  <Lucide icon={ic.ellipsis} color="#b3b3b3" />
                </li>
              ))}
            </ol>
          </div>
        </section>
      )}
    >
      <header className={s.header} id="pl-top">
        <Status />
        <h1 className={s.hello}>Selamat datang, {guestLabel(data)}</h1>
        <nav className={s.chips} aria-label="Bagian undangan">
          <a href="#pl-top" aria-current="page">Semua</a>
          <a href="#pl-acara">Acara</a>
          {(stories.length > 0 || photos.length > 0) && <a href="#pl-kisah">Kisah</a>}
          {(demo || data.gifts.length > 0) && <a href="#pl-kado">Kado</a>}
        </nav>
      </header>

      <main className={s.body}>
        <Extras slot="opening" className={s.extras} />

        <section className={s.section} aria-labelledby="pl-mempelai">
          <h2 id="pl-mempelai">Artis Bulan Ini</h2>
          <div className={s.artists}>
            {people.map(person => (
              <article key={person.name}>
                <Photo src={person.photo} alt={person.name} className={s.artistPhoto} />
                <strong>{person.name}</strong>
                {demo && <small>{person.listeners}</small>}
                {person.parents && <small>{person.parents}</small>}
                <button type="button" className={s.outline} aria-pressed={!!following[person.name]}
                  onClick={() => setFollowing(f => ({ ...f, [person.name]: !f[person.name] }))}>
                  {following[person.name] ? "Diikuti" : "Ikuti"}
                </button>
              </article>
            ))}
          </div>
        </section>

        <section className={s.section} aria-labelledby="pl-acara">
          <h2 id="pl-acara">Antrean Hari H</h2>
          <p className={s.lead}>{[longDate, data.place].filter(Boolean).join(" · ")}</p>
          <ol className={s.queue}>
            {data.events.map((event, index) => {
              const href = mapsHref(data, event);
              const sub = [event.time, event.venue && event.venue !== data.place ? event.venue : "", event.date && formatDate(event.date) !== longDate ? formatDate(event.date) : ""].filter(Boolean).join(" · ");
              return (
                <li key={event.name + index} className={index === 0 ? s.now : undefined}>
                  <span className={s.qIcon} aria-hidden><Lucide icon={index === 0 ? ic.audioLines : ic.music2} size={18} color={index === 0 ? "#000" : "#b3b3b3"} /></span>
                  <div><strong>{event.name}</strong><small>{sub}</small></div>
                  {href && <a className={s.outline} href={href} target="_blank" rel="noreferrer" aria-label={`Peta ${event.venue || event.name}`}>Peta</a>}
                </li>
              );
            })}
          </ol>
        </section>

        <Extras slot="event" className={s.extras} />

        <section className={s.section} aria-label="Ringkasan">
          <div className={s.wrapped}>
            <small>KALIAN WRAPPED · {demo ? "2019–2027" : firstYear && firstYear !== parts.year ? `${firstYear}–${parts.year}` : parts.year}</small>
            <strong>{demo ? "4.212.000" : countdown.done ? "Hari ini" : countdown.days}</strong>
            <p>{demo ? "menit dihabiskan bersama — naik 100% tiap tahun" : countdown.done ? "hari bahagia telah tiba" : "hari lagi menuju hari bahagia"}</p>
            <dl>
              {(demo
                ? [["Lagu teratas", "Janji (2019) — pertama ngobrol di konser"], ["Genre favorit", "Jazz hujan-hujanan · Indie senja"], ["Momen #1", "Lamaran di rooftop, 17 Des 2026"]]
                : [["Tanggal rilis", longDate], ["Lokasi", data.place], ["Jumlah acara", `${data.events.length} acara`]]
              ).filter(([, value]) => value).map(([label, value]) => (
                <div key={label}><dt>{label}</dt><dd>{value}</dd></div>
              ))}
            </dl>
          </div>
        </section>

        {(stories.length > 0 || photos.length > 0) && (
          <section className={s.section} aria-labelledby="pl-kisah">
            <h2 id="pl-kisah">Album &amp; Single</h2>
            {stories.length > 0 && (
              <div className={s.albums}>
                {stories.map((story, index) => (
                  <article key={story.title + index}>
                    <Photo src={story.image ?? data.gallery[index % Math.max(1, data.gallery.length)]} alt={story.title} className={s.albumArt} />
                    <strong>{story.title}{story.date && !story.title.includes(story.date) ? ` (${story.date})` : ""}</strong>
                    <small>{couple}</small>
                    {story.body && <p>{story.body}</p>}
                  </article>
                ))}
              </div>
            )}
            {photos.length > 0 && (
              <div className={s.canvas}>
                <Photo src={photos[0]} alt="Foto prewedding" />
                <span>{demo ? <><Lucide icon={ic.play} size={12} color="#fff" />Canvas · Prewedding Loop</> : "Galeri Prewedding"}</span>
              </div>
            )}
            {photos.length > 1 && (
              <div className={s.photos}>
                {photos.slice(1).map((src, index) => <Photo key={src + index} src={src} alt={`Foto ${index + 2}`} />)}
              </div>
            )}
          </section>
        )}

        <Extras slot="story" className={s.extras} />

        <Extras slot="end" className={s.extras} />

        {(demo || data.gifts.length > 0) && (
          <section className={s.section} aria-labelledby="pl-kado">
            <h2 id="pl-kado">{demo ? "Merch & Wishlist Kado" : "Kirim Kado"}</h2>
            {demo && (
              <>
                <div className={s.tiers}>
                  {[["Dengar", "Rp100rb"], ["Fans", "Rp500rb"], ["Superfan", "Rp1jt"]].map(([name, price], index) => (
                    <div key={name} className={index === 2 ? s.tierHot : undefined}><strong>{name}</strong><small>{price}</small></div>
                  ))}
                </div>
                <ul className={s.merch}>
                  {[
                    { name: "Vinyl Player", price: "Rp2.500.000", icon: ic.disc3 },
                    { name: "Smart Speaker", price: "Rp1.350.000", icon: ic.speaker },
                    { name: "Gitar Akustik", price: "Rp2.900.000", icon: ic.guitar },
                  ].map(item => (
                    <li key={item.name}>
                      <span className={s.merchIcon}><Lucide icon={item.icon} size={22} color="#1db954" /></span>
                      <div><strong>{item.name}</strong><small>{item.price}</small></div>
                      <span className={s.outline}>Beri</span>
                    </li>
                  ))}
                </ul>
              </>
            )}
            {data.gifts.map(gift => {
              const info = giftInfo(gift);
              return (
                <div key={gift.id} className={s.amplop}>
                  <Lucide icon={ic.wallet} size={18} color="#1db954" />
                  <div>
                    <strong>{gift.type === "address" ? "Kirim Kado" : gift.type === "qris" ? "QRIS" : "Amplop Digital"}</strong>
                    <small>{[[info.title !== "Alamat kado" && gift.type !== "qris" ? info.title : "", info.number].filter(Boolean).join(" "), info.holder ? `a.n. ${info.holder}` : ""].filter(Boolean).join(" · ")}</small>
                    {info.image && <Photo src={info.image} alt="Kode QRIS" className={s.qris} />}
                  </div>
                  {info.copy && <button type="button" className={s.copy} onClick={() => copy(info.copy)}>{copied === info.copy ? "Tersalin" : "Salin"}</button>}
                </div>
              );
            })}
          </section>
        )}

        <section className={s.section} aria-labelledby="pl-ucapan">
          <h2 id="pl-ucapan">Catatan Pendengar · {demo ? 312 : wishes.wishes.length}</h2>
          {wishes.wishes.length === 0 && <p className={s.lead}>Belum ada catatan. Jadilah pendengar pertama!</p>}
          {wishes.wishes.slice(0, 8).map(wish => (
            <article key={wish.id} className={s.note}>
              <span aria-hidden>{wish.name.slice(0, 1).toUpperCase()}</span>
              <div><strong>{wish.name}</strong><p>{wish.message}</p></div>
            </article>
          ))}
          <button type="button" className={s.writeBtn} onClick={sheets.openWish}>Tulis Catatan</button>
        </section>
      </main>

      <nav className={s.bottom} aria-label="Aksi undangan">
        <div className={s.nowPlaying}>
          <i aria-hidden />
          <div>
            <strong>{parts.day ? `Menuju ${parts.day} ${parts.month} — Hitung Mundur` : "Hitung Mundur"}</strong>
            <small>{[couple, daysLeft].filter(Boolean).join(" · ")}</small>
          </div>
          <Lucide icon={ic.play} size={18} color="#fff" />
        </div>
        <div className={s.rsvpRow}><button type="button" className={s.rsvp} onClick={sheets.openRsvp}>Konfirmasi Hadir</button></div>
      </nav>

      <Sheet open={sheets.sheet === "rsvp"} onClose={sheets.close} title="Konfirmasi Kehadiran" tint={tint}>
        <RsvpForm rsvp={rsvp} guestName={data.guestName} demo={demo} />
      </Sheet>
      <Sheet open={sheets.sheet === "wish"} onClose={sheets.close} title="Tulis Catatan & Doa" tint={tint}>
        <WishForm wishes={wishes} guestName={data.guestName} demo={demo} submitLabel="Kirim Catatan" />
      </Sheet>
    </ThemeShell>
  );
}
