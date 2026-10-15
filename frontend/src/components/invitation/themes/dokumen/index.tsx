"use client";
// Theme "Dokumen" — undangan bergaya halaman catatan/wiki (design: Undangan — Tema Dokumen (Tasya & Bram)).
import { useState } from "react";
import {
  Extras, Lucide, Photo, RsvpForm, Sheet, ThemeShell, WishForm, coupleLabel, formatDate, giftInfo, guestLabel,
  mapsHref, storyItems, timeAgo, useCopy, useRsvp, useSheets, useWishes, type ThemeProps, type ThemeTint,
} from "../kit";
import { ic } from "./icons";
import s from "./styles.module.css";

const FONTS = ["Inter:wght@400;500;600;700", "Lora:wght@400;700", "JetBrains Mono:wght@400;600"];
const tint: ThemeTint = {
  "--t-accent": "#2383e2", "--t-bg": "#ffffff", "--t-ink": "#37352f", "--t-muted": "#787774", "--t-line": "#e9e9e7",
  "--t-field": "#f7f6f3", "--t-radius": "6px", "--t-font": "Inter, system-ui, sans-serif",
};
const DEMO_WISHES = [
  { id: "w1", name: "Yoga P.", message: "Halaman paling rapi yang pernah kubuka. Hadir!", created_at: new Date(Date.now() - 2 * 3600e3).toISOString() },
  { id: "w2", name: "Bu Rukmini", message: "Terharu lihat dokumentasinya. Sampai jumpa di BSD!", created_at: new Date(Date.now() - 5 * 3600e3).toISOString() },
];
const DEMO_FILES = ["kisah-01.jpg", "lamaran.jpg", "prewed.jpg"];
const DEMO_TODO: Array<[string, boolean]> = [["Robot vacuum — Rp3.200.000", false], ["Set gelas kristal — Rp780.000", true], ["Coffee maker — Rp1.450.000", false]];


function Heading({ emoji, id, children }: { emoji: string; id: string; children: string }) {
  return <h2 className={s.h2} id={id}><span aria-hidden>{emoji}</span>{children}</h2>;
}

function storyLine(story: { title: string; body: string; date?: string }) {
  const title = story.title.trim();
  const joined = [title, story.body.trim()].filter(Boolean).join(/[.!?]$/.test(title) ? " " : ". ");
  return story.date ? `${story.date} — ${joined}` : joined;
}

export default function DokumenTheme({ data, slug, guestToken, demo, skipCover }: ThemeProps) {
  const label = data.eventLabel ?? "Pernikahan";
  const title = `${label} ${coupleLabel(data)}`;
  const rsvp = useRsvp({ slug, guestToken, demo });
  const wishes = useWishes({ slug, guestToken, demo, seed: DEMO_WISHES });
  const sheets = useSheets();
  const { copy, copied } = useCopy();
  const stories = storyItems(data);
  const banner = data.gallery[0];
  const gallery = data.gallery.length > 3 ? data.gallery.slice(1) : data.gallery;
  const [shared, setShared] = useState(false);
  const people = [
    { name: data.couple.brideFull ?? data.couple.bride, parents: data.couple.brideParents, photo: data.couple.bridePhoto ?? data.gallery[1], tag: demo ? "PM proyek rumah tangga" : "Mempelai wanita" },
    { name: data.couple.groomFull ?? data.couple.groom, parents: data.couple.groomParents, photo: data.couple.groomPhoto ?? data.gallery[2], tag: demo ? "Eksekutor ide dadakan" : "Mempelai pria" },
  ];

  const share = async () => {
    const url = window.location.href;
    try {
      if (navigator.share) await navigator.share({ title, url });
      else { await navigator.clipboard.writeText(url); setShared(true); setTimeout(() => setShared(false), 2000); }
    } catch { /* share dismissed */ }
  };

  return (
    <ThemeShell
      fonts={FONTS}
      background="#f7f6f3"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.banner} aria-hidden><Photo src={banner} /></div>
          <div className={s.page}>
            <span className={s.pageIcon} aria-hidden>💍</span>
            <nav className={s.crumb} aria-label="Lokasi halaman"><span>Keluarga</span>/<span>Momen Besar</span>/<b>{label}</b></nav>
            <h1 className={s.title}>{title}</h1>
            <dl className={s.props}>
              <div><dt><Lucide icon={ic.calendar} size={14} color="#787774" />Tanggal</dt><dd>{formatDate(data.date)}</dd></div>
              <div><dt><Lucide icon={ic.mapPin} size={14} color="#787774" />Lokasi</dt><dd>{data.place}</dd></div>
              <div><dt><Lucide icon={ic.loader} size={14} color="#787774" />Status</dt><dd><span className={s.tagGreen}>Lajang → Selamanya</span></dd></div>
              <div><dt><Lucide icon={ic.users} size={14} color="#787774" />Tamu</dt><dd>Kepada Yth. di bawah ini</dd></div>
            </dl>
            <div className={s.callout}>
              <span aria-hidden>💌</span>
              <div>
                <small>Halaman ini dibagikan khusus untuk:</small>
                <strong>{guestLabel(data)}</strong>
                <em>Akses: dapat melihat &amp; mendoakan</em>
              </div>
            </div>
            <div className={s.toggles}>
              <details className={s.toggle}>
                <summary><Lucide icon={ic.chevronRight} size={14} color="#787774" />Mempelai</summary>
                <p>{people[0].name} &amp; {people[1].name}</p>
              </details>
              <details className={s.toggle}>
                <summary><Lucide icon={ic.chevronRight} size={14} color="#787774" />Rangkaian Acara</summary>
                <p>{data.events.map(event => [event.name, event.time].filter(Boolean).join(" · ")).join(" — ")}</p>
              </details>
              <details className={s.toggle} open={Boolean(data.couple.note)}>
                <summary><Lucide icon={ic.chevronRight} size={14} color="#787774" />Kisah Kami</summary>
                <p>{data.couple.note || (stories[0]?.body ?? "")}</p>
              </details>
              <details className={s.toggle}>
                <summary><Lucide icon={ic.chevronRight} size={14} color="#787774" />Galeri &amp; Kado</summary>
                <p>{gallery.length} foto{data.gifts.length ? ` · ${data.gifts.length} amplop digital` : ""}</p>
              </details>
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.bookOpen} size={15} color="#fff" />Buka Halaman Undangan</button>
          </div>
        </section>
      )}
    >
      <header className={s.nav}>
        <span className={s.navTitle}><span aria-hidden>💍</span>{title}</span>
        <span className={s.navIcons}>
          <button type="button" onClick={share} aria-label={shared ? "Tautan disalin" : "Bagikan undangan"}><Lucide icon={shared ? ic.check : ic.share2} size={17} color="#787774" /></button>
          <button type="button" onClick={sheets.openWish} aria-label="Tulis komentar"><Lucide icon={ic.messageSquare} size={17} color="#787774" /></button>
          <span aria-hidden><Lucide icon={ic.star} size={17} color="#787774" /></span>
          <span aria-hidden><Lucide icon={ic.ellipsis} size={17} color="#787774" /></span>
        </span>
      </header>

      <main className={s.body}>
        <section className={s.section} aria-labelledby="dk-couple">
          <Heading emoji="🤵" id="dk-couple">Mempelai</Heading>
          <div className={s.cards}>
            {people.map(person => (
              <article key={person.name} className={s.card}>
                <Photo src={person.photo} alt={person.name} className={s.cardImg} />
                <div className={s.cardText}>
                  <strong>{person.name}</strong>
                  {person.parents && <small>{person.parents}</small>}
                  <span className={s.tagPurple}>{person.tag}</span>
                </div>
              </article>
            ))}
          </div>
        </section>

        <Extras slot="opening" className={s.extras} />

        <section className={s.section} aria-labelledby="dk-events">
          <Heading emoji="📅" id="dk-events">Rangkaian Acara</Heading>
          <div className={s.tableWrap}>
            <table className={s.table}>
              <thead><tr><th scope="col">Acara</th><th scope="col">Waktu</th><th scope="col">Tempat</th></tr></thead>
              <tbody>
                {data.events.map((event, index) => {
                  const href = mapsHref(data, event);
                  const sameDay = formatDate(event.date) === formatDate(data.date);
                  return (
                    <tr key={event.name + index}>
                      <td>{event.name}</td>
                      <td>{!sameDay && event.date && <>{formatDate(event.date, { day: "numeric", month: "short" })}<br /></>}{event.time}</td>
                      <td>{href ? <a href={href} target="_blank" rel="noreferrer">{event.venue}</a> : event.venue}</td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </section>

        <Extras slot="event" className={s.extras} />

        {stories.length > 0 && (
          <section className={s.section} aria-labelledby="dk-story">
            <Heading emoji="📖" id="dk-story">Kisah Kami</Heading>
            <ul className={s.stories}>
              {stories.map((story, index) => (
                <li key={story.title + index}><Lucide icon={ic.chevronRight} size={14} color="#787774" style={{ marginTop: 3 }} /><p>{storyLine(story)}</p></li>
              ))}
            </ul>
          </section>
        )}

        {gallery.length > 0 && (
          <section className={s.section} aria-labelledby="dk-gallery">
            <Heading emoji="🖼" id="dk-gallery">Galeri</Heading>
            <div className={s.gallery}>
              {gallery.map((src, index) => {
                const name = demo && DEMO_FILES[index] ? DEMO_FILES[index] : `foto-${String(index + 1).padStart(2, "0")}.jpg`;
                return (
                  <a key={src + index} className={s.file} href={src} target="_blank" rel="noreferrer">
                    <Photo src={src} alt={`Foto ${index + 1}`} className={s.fileImg} />
                    <span>{name}</span>
                  </a>
                );
              })}
            </div>
          </section>
        )}

        <Extras slot="story" className={s.extras} />
        <Extras slot="end" className={s.extras} />

        {(demo || data.gifts.length > 0) && (
          <section className={s.section} aria-labelledby="dk-gift">
            <Heading emoji="🎁" id="dk-gift">{demo ? "Wishlist Kado" : "Kado"}</Heading>
            {demo && (
              <ul className={s.todo}>
                {DEMO_TODO.map(([item, done]) => (
                  <li key={item} className={done ? s.done : undefined}>
                    <span className={s.checkbox} aria-hidden>{done && <Lucide icon={ic.check} size={11} color="#fff" strokeWidth={3} />}</span>{item}
                  </li>
                ))}
              </ul>
            )}
            {data.gifts.map(gift => {
              const info = giftInfo(gift);
              const line = gift.type === "address" ? info.number : [[info.title, info.number].filter(Boolean).join(" "), info.holder ? `a.n. ${info.holder}` : ""].filter(Boolean).join(" · ");
              const file = gift.type === "address" ? "alamat-kado.txt" : gift.type === "qris" ? "qris.png" : "amplop-digital.txt";
              const body = (
                <>
                  <small>{file}</small>
                  {line && <code>{line}</code>}
                  {"image" in info && info.image && <Photo src={info.image} alt="Kode QRIS" className={s.qris} />}
                  {info.copy && <i>{copied === info.copy ? "// tersalin ✓" : "// klik untuk menyalin"}</i>}
                </>
              );
              return info.copy
                ? <button key={gift.id} type="button" className={s.code} onClick={() => copy(info.copy)} aria-label={`Salin ${line}`}>{body}</button>
                : <div key={gift.id} className={s.code}>{body}</div>;
            })}
          </section>
        )}

        <section className={s.section} aria-labelledby="dk-wishes">
          <Heading emoji="💬" id="dk-wishes">Komentar</Heading>
          {wishes.wishes.length === 0 && <p className={s.empty}>Belum ada komentar. Jadilah yang pertama mendoakan!</p>}
          {wishes.wishes.slice(0, 8).map(wish => (
            <article key={wish.id} className={s.comment}>
              <span className={s.avatar} aria-hidden>{wish.name.trim().slice(0, 1).toUpperCase()}</span>
              <div>
                <strong>{wish.name}{!demo && wish.created_at && <small> · {timeAgo(wish.created_at)}</small>}</strong>
                <p>{wish.message}</p>
              </div>
            </article>
          ))}
        </section>
      </main>

      <nav className={s.bottom} aria-label="Aksi undangan">
        <button type="button" className={s.commentBtn} onClick={sheets.openWish} aria-label="Tulis komentar"><Lucide icon={ic.messageSquare} size={17} color="#787774" /></button>
        <button type="button" className={s.rsvpBtn} onClick={sheets.openRsvp}><Lucide icon={ic.plus} size={15} color="#fff" />Tambah Konfirmasi Hadir</button>
      </nav>

      <Sheet open={sheets.sheet === "rsvp"} onClose={sheets.close} title="Konfirmasi Hadir" tint={tint}>
        <RsvpForm rsvp={rsvp} guestName={data.guestName} demo={demo} labels={{ submit: "Simpan Konfirmasi" }} />
      </Sheet>
      <Sheet open={sheets.sheet === "wish"} onClose={sheets.close} title="Tambah Komentar" tint={tint}>
        <WishForm wishes={wishes} guestName={data.guestName} demo={demo} submitLabel="Kirim Komentar" />
      </Sheet>
    </ThemeShell>
  );
}
