"use client";
// Theme "Kanal Video" — undangan bergaya platform video (design: Undangan — Tema Video (Dika & Putri)).
import { useState } from "react";
import {
  Extras, Lucide, Photo, RsvpForm, Sheet, ThemeShell, WishForm, formatDate, giftInfo, guestLabel,
  mapsHref, storyItems, timeAgo, toDate, useCopy, useRsvp, useSheets, useWishes, type ThemeProps, type ThemeTint,
} from "../kit";
import { toast } from "@/lib/celebrate";
import type { InvitationData } from "../../types";
import { ic } from "./icons";
import s from "./styles.module.css";

const FONTS = ["Roboto:wght@400;500;600;700"];
const tint: ThemeTint = {
  "--t-accent": "#ff0033", "--t-accent-ink": "#ffffff", "--t-bg": "#ffffff", "--t-ink": "#0f0f0f", "--t-muted": "#606060", "--t-line": "#e5e5e5",
  "--t-field": "#f2f2f2", "--t-radius": "12px", "--t-font": "Roboto, system-ui, sans-serif",
};
const DEMO_WISHES = [
  { id: "w1", name: "bimasakti88", message: "Nangis nonton trailernya selamat Dika & Putri!", created_at: new Date(Date.now() - 2 * 3600e3).toISOString() },
  { id: "w2", name: "tantedewi", message: "Ditunggu premiere-nya, pasti hadir! Samawa ya kalian.", created_at: new Date(Date.now() - 5 * 3600e3).toISOString() },
];
const DEMO_LIKES: Record<string, string> = { w1: "842", w2: "367" };
const DEMO_DURATIONS = ["4:05", "3:28", "5:12"];
const DEMO_CLIPS = [["Prewedding di Kebun Teh", "12:04"], ["Di Balik Layar", "8:51"], ["Trailer Teaser", "0:58"], ["Q&A Bareng Kami", "15:22"]];
const DEMO_AGES = ["28 th", "26 th"];
const DEMO_TIERS = [["Rp50rb", "#2196f3"], ["Rp100rb", "#00bfa5"], ["Rp500rb", "#ffb300"], ["Rp1jt", "#ff0033"]];
const ART = "/themes/art/kanal-video";
const DEMO_PRODUCTS = [
  { name: "Air Purifier", price: "Rp1.450.000", art: "gift-purifier", w: 45, h: 50 },
  { name: "Speaker Bluetooth", price: "Rp750.000", art: "gift-speaker", w: 90, h: 50 },
  { name: "Kamera Pocket", price: "Rp3.200.000", art: "gift-camera", w: 71, h: 50 },
];

/** Painted (gouache + ink) decorative image — never opens the photo lightbox. */
function Art({ name, w, h, className }: { name: string; w: number; h: number; className?: string }) {
  return (
    // eslint-disable-next-line @next/next/no-img-element -- static painted illustration
    <img src={`${ART}/${name}.webp`} alt="" aria-hidden width={w} height={h} className={className} data-nolightbox loading="lazy" decoding="async" draggable={false} />
  );
}


function city(address: string) {
  const parts = address.split(",").map(part => part.trim()).filter(Boolean);
  return parts[parts.length - 1] ?? "";
}

/** Google Calendar "add event" link (2 hours by default). */
function calendarHref(data: InvitationData, title: string, start?: string, location?: string) {
  const date = toDate(start);
  if (!date) return undefined;
  const fmt = (d: Date) => d.toISOString().replace(/[-:]/g, "").replace(/\.\d{3}/, "");
  const end = new Date(date.getTime() + 2 * 3600e3);
  const params = new URLSearchParams({ action: "TEMPLATE", text: title, dates: `${fmt(date)}/${fmt(end)}`, details: `Undangan ${data.couple.groom} & ${data.couple.bride}` });
  if (location) params.set("location", location);
  return `https://calendar.google.com/calendar/render?${params.toString()}`;
}

function handle(name: string) {
  return `@${name.replace(/\s+/g, "").toLowerCase()}`;
}

export default function KanalVideoTheme({ data, slug, guestToken, demo, skipCover }: ThemeProps) {
  const { couple } = data;
  const names = `${couple.groom} & ${couple.bride}`;
  const brand = `${couple.groom}${couple.bride}`.replace(/\s+/g, "");
  const longDate = formatDate(data.date);
  const shortDate = formatDate(data.date, { day: "numeric", month: "short", year: "numeric" });
  const where = city(data.address) || data.place;
  const rsvp = useRsvp({ slug, guestToken, demo });
  const wishes = useWishes({ slug, guestToken, demo, seed: DEMO_WISHES });
  const sheets = useSheets();
  const { copy, copied } = useCopy();
  const [subscribed, setSubscribed] = useState<Record<string, boolean>>({});
  const [liked, setLiked] = useState(false);
  const [activeChip, setActiveChip] = useState("#kv-top");
  const [tier, setTier] = useState<string>();
  const [cLiked, setCLiked] = useState<Record<string, boolean>>({});
  const stories = storyItems(data);
  const thumb = data.gallery[0];
  const clips = data.gallery.length > 4 ? data.gallery.slice(1) : data.gallery;
  const people = [
    { key: "groom", short: couple.groom, name: couple.groomFull ?? couple.groom, parents: couple.groomParents, photo: couple.groomPhoto ?? data.gallery[1] },
    { key: "bride", short: couple.bride, name: couple.brideFull ?? couple.bride, parents: couple.brideParents, photo: couple.bridePhoto ?? data.gallery[2] },
  ];
  const mainCalendar = calendarHref(data, `${data.eventLabel ?? "Pernikahan"} ${names}`, data.date, [data.place, data.address].filter(Boolean).join(", "));
  const chips = [
    { label: "Semua", href: "#kv-top" },
    { label: "Mempelai", href: "#kv-couple" },
    { label: "Acara", href: "#kv-events" },
    ...(clips.length ? [{ label: "Galeri", href: "#kv-gallery" }] : []),
    ...(data.gifts.length || demo ? [{ label: "Kado", href: "#kv-gift" }] : []),
  ];

  const share = async () => {
    const url = window.location.href;
    if (navigator.share) {
      try { await navigator.share({ title: `Undangan ${names}`, url }); } catch { /* dismissed */ }
    } else {
      void copy(url);
    }
  };
  const toggleSub = (key: string) => {
    if (!subscribed[key]) toast("Berhasil subscribe");
    setSubscribed(state => ({ ...state, [key]: !state[key] }));
  };
  const toggleLike = () => {
    if (!liked) toast("Ditambahkan ke video yang disukai");
    setLiked(v => !v);
  };
  // Remounting the icon wrapper on every change replays the pop animation.
  const likeIcon = (size: number, off: string) => (
    <span key={String(liked)} className={`${s.likeIcon} ${liked ? s.popped : ""}`}><Lucide icon={ic.thumbsUp} size={size} color={liked ? "#ff0033" : off} /></span>
  );
  const subBtn = (id: string, className: string) => (
    <button type="button" className={`${className} ${subscribed[id] ? s.subbed : ""}`} aria-pressed={!!subscribed[id]} onClick={() => toggleSub(id)}>
      <span key={String(!!subscribed[id])} className={s.subLabel}>{subscribed[id] && <Lucide icon={ic.bell} size={12} />}{subscribed[id] ? "Disubscribe" : "Subscribe"}</span>
    </button>
  );

  return (
    <ThemeShell
      fonts={FONTS}
      background="#0f0f0f"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.premiere}><span><Lucide icon={ic.radio} size={13} color="#fff" />PREMIERE</span></div>
          <div className={s.player}>
            <Photo src={thumb} alt={`Foto ${names}`} />
            <button type="button" className={s.play} onClick={open} aria-label="Tonton undangan"><Lucide icon={ic.play} size={30} color="#fff" /></button>
            <span className={s.dur} aria-hidden>∞</span>
            <i className={s.progress} aria-hidden><b><em /></b></i>
          </div>
          <div className={s.meta}>
            <h1>{names} — Menuju Selamanya (Trailer Resmi)</h1>
            <p>{[demo ? "1,2 jt x ditonton" : "", longDate ? `Tayang perdana ${longDate}` : "", where].filter(Boolean).join(" · ")}</p>
            <div className={s.channel}>
              <Photo src={thumb} alt="" className={s.chAv} />
              <div><strong>Keluarga {names}</strong><small>2 mempelai · 1 cinta</small></div>
              {subBtn("cover", s.subLight)}
            </div>
            <div className={s.actions}>
              <button type="button" aria-pressed={liked} onClick={toggleLike}>
                {likeIcon(14, "#fff")}{demo ? "12 rb" : liked ? "Disukai" : "Suka"}
              </button>
              <button type="button" onClick={share}><Lucide icon={copied && copied.startsWith("http") ? ic.check : ic.share2} size={14} color="#fff" />Bagikan</button>
              {mainCalendar && <a href={mainCalendar} target="_blank" rel="noreferrer"><Lucide icon={ic.bookmark} size={14} color="#fff" />Simpan</a>}
            </div>
          </div>
          <div className={s.pinned}>
            <small><Lucide icon={ic.pin} size={12} color="#aaa" />Disematkan oleh Keluarga {names}</small>
            <strong>Kepada Yth. {guestLabel(data)}</strong>
          </div>
          <button type="button" className={s.watch} onClick={open}><Lucide icon={ic.play} color="#fff" />Tonton Undangan</button>
        </section>
      )}
    >
      <header className={s.header} id="kv-top">
        <div className={s.nav}>
          <span className={s.logo}><i aria-hidden><Lucide icon={ic.play} size={11} color="#fff" /></i>{brand}</span>
          <span className={s.navIcons} aria-hidden><Lucide icon={ic.cast} size={20} /><Lucide icon={ic.bell} size={20} /><Lucide icon={ic.search} size={20} /></span>
        </div>
        <nav className={s.chips} aria-label="Bagian undangan">
          {chips.map(chip => (
            <a key={chip.href} href={chip.href} className={activeChip === chip.href ? s.chipOn : undefined} aria-current={activeChip === chip.href ? "true" : undefined} onClick={() => setActiveChip(chip.href)}>{chip.label}</a>
          ))}
        </nav>
      </header>

      <main className={s.body}>
        <Extras slot="opening" className={s.extras} />

        <section className={s.section} id="kv-couple" aria-labelledby="kv-couple-h">
          <h2 id="kv-couple-h">Channel Mempelai</h2>
          {people.map((person, index) => (
            <article key={person.key} className={s.person}>
              <Photo src={person.photo} alt={person.name} className={s.personAv} />
              <div>
                <strong>{person.name}</strong>
                <small>{[handle(person.short), demo ? DEMO_AGES[index] : ""].filter(Boolean).join(" · ")}</small>
                {person.parents && <small>{person.parents}</small>}
              </div>
              {subBtn(person.key, s.subDark)}
            </article>
          ))}
        </section>

        <section className={s.section} aria-labelledby="kv-story">
          <h2 id="kv-story">Playlist · Kisah Kami</h2>
          {stories.map((story, index) => (
            <article key={story.title + index} className={s.episode}>
              <span className={s.epThumb}>
                <Photo src={story.image ?? clips[index]} alt="" />
                <i className={s.epPlay} aria-hidden><Lucide icon={ic.play} size={11} color="#fff" /></i>
                <b className={s.epBar} aria-hidden style={{ width: `${index === stories.length - 1 ? 62 : 100}%` }} />
              </span>
              <div className={s.epText}>
                <strong>Ep. {index + 1} — {story.title}</strong>
                <small>{[story.date, demo ? DEMO_DURATIONS[index] : ""].filter(Boolean).join(" · ")}</small>
                {!demo && story.body && <p>{story.body}</p>}
              </div>
              <Lucide icon={ic.ellipsisVertical} size={16} color="#606060" />
            </article>
          ))}
          <article className={s.episode}>
            <span className={`${s.epThumb} ${s.epFinal}`}><Art name="final-thumb" w={120} h={68} /><i className={s.epPlay} aria-hidden><Lucide icon={ic.play} size={11} color="#fff" /></i></span>
            <div className={s.epText}>
              <strong>Final — Menuju Selamanya</strong>
              <small className={s.live}>{shortDate && `${shortDate} · `}<i className={s.liveDot} aria-hidden />LIVE</small>
            </div>
            <Lucide icon={ic.ellipsisVertical} size={16} color="#606060" />
          </article>
        </section>

        <section className={s.section} id="kv-events" aria-labelledby="kv-events-h">
          <h2 id="kv-events-h">Jadwal Tayang Perdana</h2>
          {data.events.map((event, index) => {
            const location = [event.venue, event.address].filter(Boolean).join(", ");
            const cal = calendarHref(data, `${event.name} ${names}`, event.date, location);
            const maps = mapsHref(data, event);
            return (
              <article key={event.name + index} className={s.event}>
                <span className={s.eventIcon} aria-hidden><Lucide icon={ic.calendarHeart} size={20} color="#ff0033" /></span>
                <div className={s.eventText}>
                  <strong>{event.name}</strong>
                  <small>{[formatDate(event.date, { weekday: "long", day: "numeric", month: "short" }), event.time].filter(Boolean).join(" · ")}</small>
                  {maps ? <a href={maps} target="_blank" rel="noreferrer">{location}<Lucide icon={ic.mapPin} size={11} color="#606060" /></a> : <small>{location}</small>}
                </div>
                {cal && <a className={s.remind} href={cal} target="_blank" rel="noreferrer" aria-label={`Ingatkan ${event.name} di kalender`}><Lucide icon={ic.bell} size={12} />Ingatkan</a>}
              </article>
            );
          })}
        </section>

        <Extras slot="event" without={["calendar"]} className={s.extras} />

        {clips.length > 0 && (
          <section className={s.section} id="kv-gallery" aria-labelledby="kv-gallery-h">
            <h2 id="kv-gallery-h">Video &amp; Momen</h2>
            <div className={s.clips}>
              {clips.map((src, index) => {
                const clip = demo ? DEMO_CLIPS[index] : undefined;
                return (
                  <figure key={src + index} className={s.clip}>
                    <span><Photo src={src} alt={clip?.[0] ?? `Momen ${index + 1}`} />{clip && <b>{clip[1]}</b>}</span>
                    {clip && <figcaption>{clip[0]}</figcaption>}
                  </figure>
                );
              })}
            </div>
          </section>
        )}

        <Extras slot="story" className={s.extras} />

        <Extras slot="end" className={s.extras} />

        {(demo || data.gifts.length > 0) && (
          <section className={s.section} id="kv-gift" aria-labelledby="kv-gift-h">
            <h2 id="kv-gift-h">{demo ? "Super Thanks · Hadiah Pilihan" : "Super Thanks · Kirim Kado"}</h2>
            {demo && (
              <>
                <div className={s.tiers}>
                  {DEMO_TIERS.map(([label, color]) => (
                    <button key={label} type="button" aria-pressed={tier === label} className={tier === label ? s.tierOn : undefined}
                      style={{ color: tier === label ? "#fff" : color, borderColor: color, background: tier === label ? color : `${color}1a` }}
                      onClick={() => setTier(value => value === label ? undefined : label)}>{label}</button>
                  ))}
                </div>
                <div className={s.rack}>
                  {DEMO_PRODUCTS.map(item => (
                    <div key={item.name} className={s.product}>
                      <span><Art name={item.art} w={item.w} h={item.h} /></span>
                      <strong>{item.name}</strong>
                      <b>{item.price}</b>
                    </div>
                  ))}
                </div>
              </>
            )}
            {data.gifts.map(gift => {
              const info = giftInfo(gift);
              const address = gift.type === "address";
              return (
                <div key={gift.id} className={s.amplop}>
                  <Lucide icon={address ? ic.mapPin : ic.wallet} size={18} color="#fff" />
                  <div>
                    <strong>{address ? "Alamat Kado" : "Amplop Digital"}</strong>
                    <small>{[[address ? "" : info.title, info.number].filter(Boolean).join(" "), info.holder ? `a.n. ${info.holder}` : ""].filter(Boolean).join(" · ")}</small>
                    {info.image && <Photo src={info.image} alt="Kode QRIS" className={s.qris} />}
                  </div>
                  {info.copy && (
                    <button type="button" className={copied === info.copy ? s.copiedBtn : undefined} onClick={() => copy(info.copy)}>
                      <span key={String(copied === info.copy)} className={s.subLabel}>{copied === info.copy && <Lucide icon={ic.check} size={12} />}{copied === info.copy ? "Tersalin" : "Salin"}</span>
                    </button>
                  )}
                </div>
              );
            })}
          </section>
        )}

        <section className={s.section} aria-labelledby="kv-comments">
          <h2 id="kv-comments">Komentar · {demo ? "1,4 rb" : wishes.wishes.length}</h2>
          <button type="button" className={s.addComment} onClick={sheets.openWish}>
            <span aria-hidden>{(data.guestName?.trim() || "T").slice(0, 1).toUpperCase()}</span>Tambahkan komentar…
          </button>
          {wishes.wishes.slice(0, 8).map(wish => (
            <article key={wish.id} className={s.comment}>
              <span className={s.cAv} aria-hidden>{wish.name.slice(0, 1).toUpperCase()}</span>
              <div>
                <p className={s.cHead}><b>{handle(wish.name)}</b><span>{timeAgo(wish.created_at).replace(/ lalu$/, "")}</span></p>
                <p className={s.cBody}>{wish.message}</p>
                <p className={s.cFoot}>
                  <button type="button" className={`${s.cLike} ${cLiked[wish.id] ? s.cLikeOn : ""}`} aria-pressed={!!cLiked[wish.id]} aria-label={`Suka komentar ${handle(wish.name)}`}
                    onClick={() => setCLiked(state => ({ ...state, [wish.id]: !state[wish.id] }))}>
                    <span key={String(!!cLiked[wish.id])} className={cLiked[wish.id] ? s.popped : undefined}><Lucide icon={ic.thumbsUp} size={12} color={cLiked[wish.id] ? "#ff0033" : "#606060"} /></span>
                    {demo && DEMO_LIKES[wish.id] ? (cLiked[wish.id] ? String(Number(DEMO_LIKES[wish.id]) + 1) : DEMO_LIKES[wish.id]) : cLiked[wish.id] ? "1" : ""}
                  </button>
                  <button type="button" onClick={sheets.openWish}>Balas</button>
                </p>
              </div>
            </article>
          ))}
        </section>

        <footer className={s.note}><a href="/" target="_blank" rel="noreferrer">dibuat dengan ♥ di Rawuh</a></footer>
      </main>

      <nav className={s.bottom} aria-label="Aksi undangan">
        <button type="button" className={`${s.likeBtn} ${liked ? s.likeOn : ""}`} aria-pressed={liked} aria-label="Suka undangan ini" onClick={toggleLike}>
          {likeIcon(18, "#0f0f0f")}
        </button>
        <button type="button" className={s.rsvpBtn} onClick={sheets.openRsvp}>Konfirmasi Hadir</button>
      </nav>

      <Sheet open={sheets.sheet === "rsvp"} onClose={sheets.close} title="Konfirmasi Kehadiran" tint={tint}>
        <RsvpForm rsvp={rsvp} guestName={data.guestName} demo={demo} />
      </Sheet>
      <Sheet open={sheets.sheet === "wish"} onClose={sheets.close} title="Tulis Komentar" tint={tint}>
        <WishForm wishes={wishes} guestName={data.guestName} demo={demo} submitLabel="Kirim Komentar" />
      </Sheet>
    </ThemeShell>
  );
}
