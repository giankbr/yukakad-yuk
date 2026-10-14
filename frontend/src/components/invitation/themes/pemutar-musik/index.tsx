"use client";
// Theme "Pemutar Musik" — undangan bergaya aplikasi pemutar musik (design: Tema Pemutar Musik (Nada & Raga)).
import {
  Lucide, Photo, RsvpForm, Sheet, ThemeShell, WishForm, coupleLabel, formatDate, giftInfo, guestLabel,
  mapsHref, storyItems, timeAgo, useCopy, useRsvp, useSheets, useWishes, type ThemeProps, type ThemeTint,
} from "../kit";
import { ic } from "./icons";
import s from "./styles.module.css";

const FONTS = ["Inter:wght@400;600;700;800"];
const tint: ThemeTint = {
  "--t-accent": "#fa2d48", "--t-ink": "#1d1d1f", "--t-muted": "#86868b", "--t-line": "#e8e8ed", "--t-field": "#f2f2f7",
  "--t-radius": "12px", "--t-font": "Inter, system-ui, sans-serif",
};
const DEMO_WISHES = [
  { id: "w1", name: "Bude Retno", message: "Album terbaik tahun ini! Track 2 bikin merinding. Pasti hadir!", created_at: new Date(Date.now() - 3 * 3600e3).toISOString() },
  { id: "w2", name: "Yoga", message: "Sudah pre-save dari 2019. Akhirnya rilis juga. Selamat!", created_at: new Date(Date.now() - 7 * 3600e3).toISOString() },
];
const DEMO_VIDEOS = [{ title: "MV — Selamanya", length: "4:12" }, { title: "Sesi Akustik", length: "2:48" }, { title: "Di Balik Lagu", length: "6:30" }];

function city(address: string) {
  const parts = address.split(",").map(part => part.trim()).filter(Boolean);
  return parts[parts.length - 1] ?? "";
}

/** "08.00 – 10.00 WIB" → "08.00" */
function startTime(time: string) {
  return time.split(/\s*[–-]\s*/)[0].replace(/\s*(WIB|WITA|WIT)$/i, "").trim();
}

function Status() {
  return (
    <div className={s.status} aria-hidden>
      21:05
      <span><Lucide icon={ic.signal} /><Lucide icon={ic.wifi} /><Lucide icon={ic.batteryFull} /></span>
    </div>
  );
}

export default function PemutarMusikTheme({ data, slug, guestToken, demo, skipCover }: ThemeProps) {
  const couple = coupleLabel(data);
  const { couple: c } = data;
  const rsvp = useRsvp({ slug, guestToken, demo });
  const wishes = useWishes({ slug, guestToken, demo, seed: DEMO_WISHES });
  const sheets = useSheets();
  const { copy, copied } = useCopy();
  const stories = storyItems(data);
  const art = data.gallery[0];
  const where = city(data.address);
  const meta = [data.eventLabel ?? "Pernikahan", formatDate(data.date, { day: "numeric", month: "long", year: "numeric" }), where, "Lossless"].filter(Boolean).join(" · ");
  const liveIndex = Math.max(0, data.events.findIndex(event => /akad|pemberkatan|nikah/i.test(event.name)));
  const videos = data.gallery.length > 3 ? data.gallery.slice(1) : data.gallery;
  const initials = `${c.bride.slice(0, 1)}♥${c.groom.slice(0, 1)}`.toUpperCase();
  const people = [
    { name: c.brideFull ?? c.bride, role: "Vokal utama", parents: c.brideParents, photo: c.bridePhoto ?? data.gallery[1] },
    { name: c.groomFull ?? c.groom, role: "Komposer", parents: c.groomParents, photo: c.groomPhoto ?? data.gallery[2] },
  ];
  const mainMaps = mapsHref(data);

  return (
    <ThemeShell
      fonts={FONTS}
      background="#efe9ec"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.backdrop} aria-hidden />
          <Status />
          <div className={s.coverContent}>
            <Photo src={art} alt={`Sampul album ${couple}`} className={s.albumArt} />
            <div className={s.coverTitle}>
              <h1>Selamanya — Album {data.eventLabel ?? "Pernikahan"}</h1>
              <p className={s.artist}>{couple}</p>
              <p className={s.coverMeta}>{meta}</p>
            </div>
            <div className={s.coverButtons}>
              <button type="button" onClick={open}><Lucide icon={ic.play} color="#fa2d48" />Putar</button>
              <button type="button" onClick={open}><Lucide icon={ic.shuffle} color="#fa2d48" />Acak</button>
            </div>
            <div className={s.dedication}>
              <small>DIPERSEMBAHKAN UNTUK</small>
              <strong>{guestLabel(data)}</strong>
              <span>Dengarkan undangan ini sampai selesai ya</span>
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.play} color="#fff" />Putar Undangan</button>
          </div>
          <div className={s.mini} aria-hidden>
            <i />
            <div><strong>Janji Suci (feat. Keluarga)</strong><small>{couple}</small></div>
            <Lucide icon={ic.play} size={18} color="#1d1d1f" />
            <Lucide icon={ic.fastForward} size={18} color="#1d1d1f" />
          </div>
        </section>
      )}
    >
      <header className={s.header}>
        <Status />
        <div className={s.nav}>
          <h1>Sedang Diputar</h1>
          <span aria-label={couple}>{initials}</span>
        </div>
      </header>

      <main className={s.body}>
        <section className={s.section} aria-labelledby="pm-acara">
          <h2 id="pm-acara">Daftar Lagu · Rangkaian Hari</h2>
          <ol className={s.tracks}>
            {data.events.map((event, index) => {
              const live = index === liveIndex;
              const sub = [formatDate(event.date), event.venue && event.venue !== data.place ? event.venue : ""].filter(Boolean).join(" · ");
              return (
                <li key={event.name + index} className={live ? s.live : undefined}>
                  {live ? <Lucide icon={ic.audioLines} size={16} color="#fa2d48" className={s.trackNo} /> : <span className={s.trackNo}>{index + 1}</span>}
                  <div><strong>{event.name}</strong><small>{sub}</small></div>
                  <time>{startTime(event.time)}</time>
                  <Lucide icon={ic.ellipsis} size={16} color="#86868b" />
                </li>
              );
            })}
          </ol>
          <div className={s.place}>
            <Lucide icon={ic.mapPin} color="#fa2d48" />
            <div><strong>{data.place}</strong><small>{data.address}</small></div>
            {mainMaps && <a href={mainMaps} target="_blank" rel="noreferrer" className={s.pill}>Peta</a>}
          </div>
          {data.events.filter(event => event.venue && event.venue !== data.place).map((event, index) => {
            const href = mapsHref(data, event);
            return (
              <div key={event.venue + index} className={s.place}>
                <Lucide icon={ic.mapPin} color="#fa2d48" />
                <div><strong>{event.venue}</strong><small>{[event.address, event.name].filter(Boolean).join(" · ")}</small></div>
                {href && <a href={href} target="_blank" rel="noreferrer" className={s.pill}>Peta</a>}
              </div>
            );
          })}
        </section>

        <section className={s.section} aria-labelledby="pm-mempelai">
          <h2 id="pm-mempelai">Artis Utama</h2>
          <div className={s.artists}>
            {people.map(person => (
              <article key={person.name}>
                <Photo src={person.photo} alt={person.name} className={s.artistPhoto} />
                <strong>{person.name}</strong>
                <em>{person.role}</em>
                {person.parents && <small>{person.parents}</small>}
              </article>
            ))}
          </div>
        </section>

        {stories.length > 0 && (
          <section className={s.section} aria-labelledby="pm-kisah">
            <h2 id="pm-kisah">Diskografi Kisah</h2>
            <div className={s.albums}>
              {stories.map((story, index) => (
                <article key={story.title + index}>
                  <Photo src={story.image ?? data.gallery[(index + 1) % Math.max(1, data.gallery.length)]} alt={story.title} className={s.albumImg} />
                  <strong>{story.title}</strong>
                  {story.date && <small>{story.date}</small>}
                  {story.body && !demo && <p>{story.body}</p>}
                </article>
              ))}
            </div>
          </section>
        )}

        {videos.length > 0 && (
          <section className={s.section} aria-labelledby="pm-galeri">
            <h2 id="pm-galeri">{demo ? "Video Musik" : "Galeri"}</h2>
            <div className={s.bigShot}>
              <Photo src={videos[0]} alt={demo ? DEMO_VIDEOS[0].title : "Foto 1"} />
              {demo && (
                <>
                  <span className={s.playBig} aria-hidden><Lucide icon={ic.play} size={24} color="#fa2d48" /></span>
                  <span className={s.cap}>{DEMO_VIDEOS[0].title} · {DEMO_VIDEOS[0].length}</span>
                </>
              )}
            </div>
            {videos.length > 1 && (
              <div className={s.shots}>
                {videos.slice(1).map((src, index) => {
                  const video = demo ? DEMO_VIDEOS[index + 1] : undefined;
                  return (
                    <figure key={src + index}>
                      <div className={s.shot}>
                        <Photo src={src} alt={video?.title ?? `Foto ${index + 2}`} />
                        {video && <span>{video.length}</span>}
                      </div>
                      {video && <figcaption>{video.title}</figcaption>}
                    </figure>
                  );
                })}
              </div>
            )}
          </section>
        )}

        {(demo || data.gifts.length > 0) && (
          <section className={s.section} aria-labelledby="pm-kado">
            <h2 id="pm-kado">{demo ? "Wishlist Kado" : "Kirim Kado"}</h2>
            {demo && (
              <>
                <p className={s.lead}>Hadiah yang masuk tangga lagu kami</p>
                <ol className={s.chart}>
                  {[
                    { name: "Turntable Vinyl", price: "Rp2.750.000", icon: ic.disc3 },
                    { name: "Headphone Studio", price: "Rp1.900.000", icon: ic.headphones },
                    { name: "Keyboard 61 Tuts", price: "Rp3.400.000", icon: ic.piano },
                  ].map((item, index) => (
                    <li key={item.name}>
                      <b>#{index + 1}</b>
                      <span className={s.chartIcon}><Lucide icon={item.icon} size={22} color="#fa2d48" /></span>
                      <div><strong>{item.name}</strong><small>{item.price}</small></div>
                      <span className={s.pill}>Beri</span>
                    </li>
                  ))}
                </ol>
              </>
            )}
            {data.gifts.map(gift => {
              const info = giftInfo(gift);
              return (
                <div key={gift.id} className={s.amplop}>
                  <Lucide icon={ic.wallet} size={18} color="#fff" />
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

        <section className={s.section} aria-labelledby="pm-ucapan">
          <h2 id="pm-ucapan">Ulasan Pendengar</h2>
          <p className={s.lead}>{demo ? <><span className={s.grayStars} aria-hidden>★★★★★</span> 4,9 (312 ulasan)</> : `${wishes.wishes.length} ulasan`}</p>
          {wishes.wishes.length === 0 && <p className={s.lead}>Belum ada ulasan. Jadilah pendengar pertama yang menulis!</p>}
          {wishes.wishes.slice(0, 8).map(wish => (
            <article key={wish.id} className={s.review}>
              <div><strong>{wish.name}</strong>{demo ? <span aria-hidden>★★★★★</span> : <small>{timeAgo(wish.created_at)}</small>}</div>
              <p>{wish.message}</p>
            </article>
          ))}
          <button type="button" className={s.writeBtn} onClick={sheets.openWish}>Tulis Ulasan</button>
        </section>
      </main>

      <nav className={s.bottom} aria-label="Aksi undangan">
        <div className={s.progress} aria-hidden><i /></div>
        <div className={s.controls}>
          <span className={s.transport} aria-hidden>
            <Lucide icon={ic.skipBack} size={20} color="#1d1d1f" /><Lucide icon={ic.play} size={20} color="#1d1d1f" /><Lucide icon={ic.skipForward} size={20} color="#1d1d1f" />
          </span>
          <button type="button" className={s.rsvp} onClick={sheets.openRsvp}>Konfirmasi Hadir</button>
        </div>
      </nav>

      <Sheet open={sheets.sheet === "rsvp"} onClose={sheets.close} title="Konfirmasi Kehadiran" tint={tint}>
        <RsvpForm rsvp={rsvp} guestName={data.guestName} demo={demo} />
      </Sheet>
      <Sheet open={sheets.sheet === "wish"} onClose={sheets.close} title="Tulis Ulasan & Doa" tint={tint}>
        <WishForm wishes={wishes} guestName={data.guestName} demo={demo} submitLabel="Kirim Ulasan" />
      </Sheet>
    </ThemeShell>
  );
}
