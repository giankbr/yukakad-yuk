"use client";
// Theme "Koran" — undangan bergaya surat kabar (design: Warta Bahagia, Ayu & Teguh).
import {
  Extras, Lucide, Photo, RsvpForm, Sheet, ThemeShell, WishForm, dateParts, formatDate, giftInfo, guestLabel,
  mapsHref, storyItems, useCopy, useRsvp, useSheets, useWishes, type ThemeProps, type ThemeTint,
} from "../kit";
import { ic } from "./icons";
import s from "./styles.module.css";

const FONTS = ["Playfair Display:wght@800", "Noto Serif:ital,wght@0,400;0,700;1,400"];
const tint: ThemeTint = {
  "--t-accent": "#1d1a14", "--t-accent-ink": "#f5f0e4", "--t-bg": "#f5f0e4", "--t-ink": "#1d1a14", "--t-muted": "#6b6456",
  "--t-line": "#c9c0ac", "--t-field": "#fbf8f0", "--t-radius": "0px", "--t-font": "'Noto Serif', Georgia, serif",
};
const DEMO_WISHES = [
  { id: "w1", name: "Bpk. Bambang W.", message: "Saya pelanggan sejak 2020. Akhirnya headline bahagia juga. Kami hadir!" },
  { id: "w2", name: "Ibu Sri Rejeki", message: "Semoga rumah tangganya selangsung koran ini terbit: setiap hari." },
];

function Status() {
  return (
    <div className={s.status} aria-hidden>
      <span>06:00</span>
      <span className={s.statusIcons}><Lucide icon={ic.signal} /><Lucide icon={ic.wifi} /><Lucide icon={ic.batteryFull} /></span>
    </div>
  );
}

function city(address: string) {
  const parts = address.split(",").map(part => part.trim()).filter(Boolean);
  return parts[parts.length - 1] ?? "";
}

/** "08.00" from "08.00 – 10.00 WIB". */
function startTime(time?: string) {
  const match = time?.match(/\d{1,2}[.:]\d{2}/);
  return match ? match[0].replace(":", ".") : "";
}

export default function KoranTheme({ data, slug, guestToken, demo, skipCover }: ThemeProps) {
  const { bride, groom } = data.couple;
  const brideFull = data.couple.brideFull ?? bride;
  const groomFull = data.couple.groomFull ?? groom;
  const parts = dateParts(data.date);
  const longDate = formatDate(data.date);
  const where = city(data.address) || data.place;
  const label = data.eventLabel ?? "Pernikahan";
  const rsvp = useRsvp({ slug, guestToken, demo });
  const wishes = useWishes({ slug, guestToken, demo, seed: DEMO_WISHES });
  const sheets = useSheets();
  const { copy, copied } = useCopy();
  const stories = storyItems(data);
  const firstYear = Number(stories.find(story => /\d{4}/.test(story.date ?? ""))?.date?.match(/\d{4}/)?.[0]);
  const span = firstYear && parts.year ? Number(parts.year) - firstYear : 0;
  const deck = `${span > 0 ? `Setelah ${span} tahun pemberitaan berseri, pasangan ini` : "Pasangan ini"} akhirnya menuju pelaminan${longDate ? ` • ${longDate}` : ""}`;
  const hero = data.gallery[0];
  const photos = data.gallery.length > 1 ? data.gallery.slice(1) : data.gallery;
  const [mainPhoto, ...sidePhotos] = photos;
  const lead = `${where ? `${where.toUpperCase()} — ` : ""}Kabar yang dinanti itu tiba juga. ${groomFull}${demo ? " (29)" : ""} resmi akan menikahi ${brideFull}${demo ? " (27)" : ""}. "Kami mengundang Anda," ujar keduanya kepada redaksi, sambil tersenyum lebar.`;
  const agenda = data.events.map((event, index) => {
    const at = startTime(event.time);
    const venue = event.venue ? ` di ${event.venue}` : "";
    return index === 0
      ? `Upacara ${event.name.toLowerCase().replace(/\s+nikah$/, "")} digelar${at ? ` pukul ${at} WIB` : ""}${venue}`
      : `disusul ${event.name.toLowerCase()}${venue}`;
  }).join(", ");
  const people = [
    { name: brideFull, bio: data.couple.brideParents, photo: data.couple.bridePhoto ?? data.gallery[1] },
    { name: groomFull, bio: data.couple.groomParents, photo: data.couple.groomPhoto ?? data.gallery[2] },
  ];

  return (
    <ThemeShell
      fonts={FONTS}
      background="#e9e3d4"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Status />
          <div className={s.page}>
            <header className={s.masthead}>
              <strong>WARTA BAHAGIA</strong>
              <div className={s.meta}>
                <span>Edisi Istimewa</span>
                <span>{[where, parts.day ? `${parts.day} ${parts.month} ${parts.year}` : ""].filter(Boolean).join(", ")}</span>
                <span>Gratis</span>
              </div>
            </header>
            <h2 className={s.headline}>{groom.toUpperCase()} RESMI MELAMAR {bride.toUpperCase()},<br />SELURUH KOTA IKUT BAHAGIA</h2>
            <p className={s.deck}>{deck}</p>
            {hero && <Photo src={hero} alt={`Foto ${bride} & ${groom}`} className={s.hero} />}
            {hero && (
              <p className={s.caption}>
                {demo ? "Foto: Ayu & Teguh sesaat setelah lamaran diterima, Simpang Lima. (dok. keluarga)" : `Foto: ${bride} & ${groom}. (dok. keluarga)`}
              </p>
            )}
            <div className={s.cols}>
              <p>{lead}</p>
              <p>{agenda ? `${agenda}. ` : ""}Seluruh pembaca setia harian ini termasuk dalam daftar undangan kehormatan.</p>
            </div>
            <div className={s.kepada}>
              <span>— UNTUK PELANGGAN TERHORMAT —</span>
              <h1>{guestLabel(data)}</h1>
              <small>Edisi lengkap undangan ada di halaman berikutnya</small>
            </div>
            <button type="button" className={s.openBtn} onClick={open}>
              <Lucide icon={ic.newspaper} size={15} />BACA SELENGKAPNYA — HLM. 2
            </button>
          </div>
        </section>
      )}
    >
      <Status />
      <main className={s.body}>
        <header className={s.pageHead}>
          <strong>WARTA BAHAGIA</strong>
          <span>HLM. 2 · RUBRIK {label.toUpperCase()}</span>
        </header>

        <Extras slot="opening" className={s.extras} />

        <section className={s.section} aria-labelledby="ko-couple">
          <div className={s.sectionHead}><h2 id="ko-couple">PROFIL MEMPELAI</h2></div>
          <div className={s.couple}>
            {people.map((person, index) => (
              <article key={index} className={s.person}>
                <Photo src={person.photo} alt={person.name} className={s.personImg} />
                <h3>{person.name}</h3>
                {person.bio && <p>{person.bio}</p>}
              </article>
            ))}
          </div>
        </section>

        {stories.length > 0 && (
          <section className={s.section} aria-labelledby="ko-story">
            <div className={s.sectionHead}><h2 id="ko-story">KRONOLOGI PEMBERITAAN</h2></div>
            <ol className={s.chrono}>
              {stories.map((story, index) => (
                <li key={story.title + index} className={s.chronoRow}>
                  <b>{story.date ?? "—"}</b>
                  <div>
                    <p>&ldquo;{story.title}&rdquo; — {story.body}</p>
                    {story.image && <Photo src={story.image} alt={story.title} className={s.chronoImg} />}
                  </div>
                </li>
              ))}
            </ol>
          </section>
        )}

        {data.events.length > 0 && (
          <section className={s.section} aria-labelledby="ko-events">
            <div className={s.sectionHead}><h2 id="ko-events">AGENDA ACARA</h2></div>
            {data.events.map((event, index) => {
              const day = dateParts(event.date);
              const href = mapsHref(data, event);
              return (
                <article key={event.name + index} className={s.event}>
                  {day.day && <span className={s.cal}><small>{day.monthShort}</small><b>{day.day}</b></span>}
                  <div className={s.eventText}>
                    <h3>{event.name.toUpperCase()}</h3>
                    <p>{[event.time, [event.venue, event.address].filter(Boolean).join(", ")].filter(Boolean).join(" · ")}</p>
                  </div>
                  {href && <a className={s.mapLink} href={href} target="_blank" rel="noreferrer" aria-label={`Peta ${event.name}`}>PETA →</a>}
                </article>
              );
            })}
          </section>
        )}

        <Extras slot="event" className={s.extras} />

        {mainPhoto && (
          <section className={s.section} aria-labelledby="ko-gallery">
            <div className={s.sectionHead}><h2 id="ko-gallery">GALERI FOTO</h2></div>
            <div className={s.gallery}>
              <figure className={s.galleryMain}>
                <Photo src={mainPhoto} alt="Foto galeri 1" className={s.photo} />
                {demo && <span>Liputan kencan pertama, Kota Lama (2020)</span>}
              </figure>
              {sidePhotos.length > 0 && (
                <div className={s.gallerySide}>
                  {sidePhotos.slice(0, 2).map((src, index) => <Photo key={src + index} src={src} alt={`Foto galeri ${index + 2}`} className={s.photo} />)}
                </div>
              )}
            </div>
            {sidePhotos.length > 2 && (
              <div className={s.galleryMore}>
                {sidePhotos.slice(2).map((src, index) => <Photo key={src + index} src={src} alt={`Foto galeri ${index + 4}`} className={s.photo} />)}
              </div>
            )}
          </section>
        )}

        <Extras slot="story" className={s.extras} />
        <Extras slot="end" className={s.extras} />

        {(demo || data.gifts.length > 0) && (
          <section className={s.section} aria-labelledby="ko-gift">
            <div className={s.sectionHead}><h2 id="ko-gift">{demo ? "IKLAN BARIS — WISHLIST KADO" : "IKLAN BARIS — TANDA KASIH"}</h2></div>
            {demo && (
              <div className={s.ads}>
                <p>DICARI: Mesin kopi utk rumah baru. Rp1,9jt. Hub: mempelai.</p>
                <p>DIJUAL CEPAT: Status lajang. Gratis. Sudah laku 16/1/2028.</p>
                <p>DICARI: Rak buku jati, Rp1,2jt. Serius hubungi kado@ayuteguh.</p>
              </div>
            )}
            {data.gifts.map(gift => {
              const info = giftInfo(gift);
              const head = gift.type === "address" ? "KIRIM KADO" : `AMPLOP DIGITAL — ${[info.title, info.number].filter(Boolean).join(" ")}`.toUpperCase();
              return (
                <div key={gift.id} className={s.amplop}>
                  <Lucide icon={ic.wallet} size={15} />
                  <div className={s.amplopText}>
                    <strong>{head}</strong>
                    {gift.type === "address" ? <small>{info.number}</small> : info.holder && <small>a.n. {info.holder}</small>}
                    {info.image && <Photo src={info.image} alt="Kode QRIS" className={s.qris} />}
                  </div>
                  {info.copy && <button type="button" className={s.copyBtn} onClick={() => copy(info.copy)}>{copied === info.copy ? "TERSALIN" : "SALIN"}</button>}
                </div>
              );
            })}
          </section>
        )}

        <section className={s.section} aria-labelledby="ko-wishes">
          <div className={s.sectionHead}><h2 id="ko-wishes">SURAT PEMBACA</h2></div>
          {wishes.wishes.length === 0 && <p className={s.empty}>Belum ada surat pembaca. Kirim ucapan Anda lewat tombol pena di bawah.</p>}
          {wishes.wishes.slice(0, 8).map(wish => (
            <blockquote key={wish.id} className={s.letter}>
              <p>&ldquo;{wish.message}&rdquo;</p>
              <cite>— {wish.name}</cite>
            </blockquote>
          ))}
        </section>
      </main>

      <nav className={s.bottom} aria-label="Aksi undangan">
        <button type="button" className={s.penBtn} onClick={sheets.openWish} aria-label="Kirim surat pembaca (ucapan)"><Lucide icon={ic.penLine} size={17} /></button>
        <button type="button" className={s.rsvpBtn} onClick={sheets.openRsvp}>KONFIRMASI KEHADIRAN</button>
      </nav>

      <Sheet open={sheets.sheet === "rsvp"} onClose={sheets.close} title="Konfirmasi Kehadiran" tint={tint}>
        <RsvpForm rsvp={rsvp} guestName={data.guestName} demo={demo} />
      </Sheet>
      <Sheet open={sheets.sheet === "wish"} onClose={sheets.close} title="Kirim Surat Pembaca" tint={tint}>
        <WishForm wishes={wishes} guestName={data.guestName} demo={demo} />
      </Sheet>
    </ThemeShell>
  );
}
