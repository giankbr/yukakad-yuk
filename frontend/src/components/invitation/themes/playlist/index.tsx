"use client";
// Theme "Playlist" — undangan bergaya aplikasi streaming musik gelap (design: Tema Playlist (Kania & Dimas)).
import { useEffect, useRef, useState } from "react";
import {
  Extras, Lucide, Photo, RsvpForm, Sheet, ThemeShell, WishForm, coupleLabel, dateParts, formatDate, giftInfo, guestLabel,
  Tick, mapsHref, storyItems, useCopy, useCountdown, useRsvp, useSheets, useWishes, type ThemeProps, type ThemeTint,
} from "../kit";
import { toast } from "@/lib/celebrate";
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

/** Animated equalizer bars (frozen while paused). */
function Eq({ paused, className }: { paused?: boolean; className?: string }) {
  return <span className={`${s.eq} ${paused ? s.eqPaused : ""} ${className ?? ""}`} aria-hidden><i /><i /><i /><i /></span>;
}

/** "Wrapped"-style number that counts up once it scrolls into view. */
function CountUp({ value, className }: { value: string; className?: string }) {
  const ref = useRef<HTMLElement>(null);
  useEffect(() => {
    const el = ref.current;
    const text = el?.firstChild;
    const target = Number(value.replace(/\./g, ""));
    if (!el || !text || !/^\d[\d.]*$/.test(value) || window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    let raf = 0;
    const io = new IntersectionObserver(([entry]) => {
      if (!entry.isIntersecting) return;
      io.disconnect();
      const start = performance.now();
      const step = (now: number) => {
        const progress = Math.min(1, (now - start) / 1700);
        text.nodeValue = Math.round(target * (1 - Math.pow(1 - progress, 3))).toLocaleString("id-ID");
        if (progress < 1) raf = requestAnimationFrame(step);
      };
      raf = requestAnimationFrame(step);
    }, { threshold: 0.4 });
    io.observe(el);
    return () => { io.disconnect(); cancelAnimationFrame(raf); text.nodeValue = value; };
  }, [value]);
  return <strong ref={ref} className={className}>{value}</strong>;
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
  const [saved, setSaved] = useState(false);
  const [downloaded, setDownloaded] = useState(false);
  const [shuffle, setShuffle] = useState(true);
  const [chip, setChip] = useState("#pl-top");
  const [nowIndex, setNowIndex] = useState(0);
  const [playing, setPlaying] = useState(true);
  const [tier, setTier] = useState("Superfan");
  const [picked, setPicked] = useState<Record<string, boolean>>({});
  const [loved, setLoved] = useState<Record<string, boolean>>({});
  const follow = (name: string) => {
    if (!following[name]) toast(`Mengikuti ${name}`);
    setFollowing(f => ({ ...f, [name]: !f[name] }));
  };
  const save = () => {
    if (!saved) toast("Disimpan ke Koleksimu");
    setSaved(v => !v);
  };
  const pick = (name: string) => {
    if (!picked[name]) toast("Ditandai di wishlist");
    setPicked(state => ({ ...state, [name]: !state[name] }));
  };
  const art = data.gallery[0];
  const photos = data.gallery.length > 1 ? data.gallery.slice(1) : data.gallery;
  const firstYear = stories.map(story => story.date?.match(/\d{4}/)?.[0]).find(Boolean);
  const people = [
    { name: c.brideFull ?? c.bride, listeners: "2,1 jt pendengar hati", parents: c.brideParents, photo: c.bridePhoto ?? data.gallery[1] },
    { name: c.groomFull ?? c.groom, listeners: "1 pendengar setia", parents: c.groomParents, photo: c.groomPhoto ?? data.gallery[2] },
  ];
  const chips = [
    { href: "#pl-top", label: "Semua" },
    { href: "#pl-acara", label: "Acara" },
    ...(stories.length > 0 || photos.length > 0 ? [{ href: "#pl-kisah", label: "Kisah" }] : []),
    ...(demo || data.gifts.length > 0 ? [{ href: "#pl-kado", label: "Kado" }] : []),
  ];

  return (
    <ThemeShell
      fonts={FONTS}
      background="#000000"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.glow} aria-hidden />
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
                <span className={s.actionsL}>
                  <button type="button" className={s.iconBtn} aria-pressed={saved} aria-label="Simpan playlist" onClick={save}>
                    <span key={String(saved)} className={saved ? `${s.pop} ${s.filled}` : undefined}><Lucide icon={ic.heart} size={22} color={saved ? "#1db954" : "#b3b3b3"} /></span>
                  </button>
                  <button type="button" className={s.iconBtn} aria-pressed={downloaded} aria-label="Unduh playlist" onClick={() => setDownloaded(v => !v)}>
                    <span key={String(downloaded)} className={downloaded ? s.pop : undefined}><Lucide icon={ic.circleArrowDown} size={22} color={downloaded ? "#1db954" : "#b3b3b3"} /></span>
                  </button>
                  <span aria-hidden className={s.iconBtn}><Lucide icon={ic.ellipsis} size={20} color="#b3b3b3" /></span>
                </span>
                <span className={s.actionsR}>
                  <button type="button" className={`${s.iconBtn} ${shuffle ? s.dot : ""}`} aria-pressed={shuffle} aria-label="Acak" onClick={() => setShuffle(v => !v)}>
                    <Lucide icon={ic.shuffle} size={20} color={shuffle ? "#1db954" : "#b3b3b3"} />
                  </button>
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
                <Eq className={s.no} />
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
        <h1 className={s.hello}>Selamat datang, {guestLabel(data)}</h1>
        <nav className={s.chips} aria-label="Bagian undangan">
          {chips.map(item => (
            <a key={item.href} href={item.href} aria-current={chip === item.href ? "page" : undefined} onClick={() => setChip(item.href)}>{item.label}</a>
          ))}
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
                <button type="button" className={s.outline} aria-pressed={!!following[person.name]} onClick={() => follow(person.name)}>
                  <span key={String(!!following[person.name])} className={s.swap}>{following[person.name] && <Lucide icon={ic.check} size={12} />}{following[person.name] ? "Diikuti" : "Ikuti"}</span>
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
                <li key={event.name + index} className={index === nowIndex ? s.now : undefined}>
                  <button type="button" className={s.qIcon} aria-label={index === nowIndex ? (playing ? `Jeda ${event.name}` : `Putar ${event.name}`) : `Putar ${event.name}`}
                    onClick={() => { if (index === nowIndex) setPlaying(v => !v); else { setNowIndex(index); setPlaying(true); } }}>
                    {index === nowIndex ? <Eq paused={!playing} className={s.eqDark} /> : <Lucide icon={ic.music2} size={18} color="#b3b3b3" />}
                  </button>
                  <div><strong key={String(index === nowIndex)}>{event.name}</strong><small>{sub}</small></div>
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
            {demo ? <CountUp value="4.212.000" /> : <strong>{countdown.done ? "Hari ini" : <Tick value={countdown.days} />}</strong>}
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
                  {[["Dengar", "Rp100rb"], ["Fans", "Rp500rb"], ["Superfan", "Rp1jt"]].map(([name, price]) => (
                    <button key={name} type="button" aria-pressed={tier === name} className={tier === name ? s.tierHot : undefined} onClick={() => setTier(name)}>
                      <strong>{name}</strong><small>{price}</small>
                    </button>
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
                      <button type="button" className={`${s.outline} ${picked[item.name] ? s.outlineOn : ""}`} aria-pressed={!!picked[item.name]} onClick={() => pick(item.name)}>
                        <span key={String(!!picked[item.name])} className={s.swap}>{picked[item.name] && <Lucide icon={ic.check} size={12} />}{picked[item.name] ? "Dipilih" : "Beri"}</span>
                      </button>
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
                  {info.copy && (
                    <button type="button" className={s.copy} onClick={() => copy(info.copy)}>
                      <span key={String(copied === info.copy)} className={s.swap}>{copied === info.copy && <Lucide icon={ic.check} size={12} />}{copied === info.copy ? "Tersalin" : "Salin"}</span>
                    </button>
                  )}
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
              <button type="button" className={s.love} aria-pressed={!!loved[wish.id]} aria-label={`Sukai catatan ${wish.name}`}
                onClick={() => setLoved(state => ({ ...state, [wish.id]: !state[wish.id] }))}>
                <span key={String(!!loved[wish.id])} className={loved[wish.id] ? `${s.pop} ${s.filled}` : undefined}><Lucide icon={ic.heart} size={16} color={loved[wish.id] ? "#1db954" : "#b3b3b3"} /></span>
              </button>
            </article>
          ))}
          <button type="button" className={s.writeBtn} onClick={sheets.openWish}>Tulis Catatan</button>
        </section>
      </main>

      <nav className={s.bottom} aria-label="Aksi undangan">
        <div className={s.nowPlaying}>
          <i aria-hidden><Eq paused={!playing} /></i>
          <div>
            <strong>{parts.day ? `Menuju ${parts.day} ${parts.month} — Hitung Mundur` : "Hitung Mundur"}</strong>
            <small>{couple}{countdown.ready && (countdown.done ? " · Hari ini" : <> · <Tick value={Number(countdown.days)} /> hari lagi</>)}</small>
          </div>
          <button type="button" className={s.miniPlay} aria-label={playing ? "Jeda" : "Putar"} onClick={() => setPlaying(v => !v)}>
            <span key={String(playing)} className={s.swap}><Lucide icon={playing ? ic.pause : ic.play} size={18} color="#fff" /></span>
          </button>
          <b className={s.miniBar} aria-hidden><em className={playing ? undefined : s.paused} /></b>
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
