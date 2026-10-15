"use client";
// Theme "Peta Rute" — undangan bergaya aplikasi peta & navigasi (design: Undangan — Tema Peta (Laras & Galih)).
import { useState } from "react";
import {
  Extras, Lucide, Photo, RsvpForm, Sheet, ThemeShell, WishForm, coupleLabel, formatDate, giftInfo, guestLabel,
  mapsHref, storyItems, timeAgo, toDate, useCopy, useCountdown, useRsvp, useSheets, useWishes, type ThemeProps, type ThemeTint,
} from "../kit";
import { ic } from "./icons";
import s from "./styles.module.css";

const FONTS = ["Roboto:wght@400;500;600;700"];
const MAP = "/themes/img/r60.webp";
const tint: ThemeTint = {
  "--t-accent": "#1a73e8", "--t-bg": "#ffffff", "--t-ink": "#202124", "--t-muted": "#5f6368", "--t-line": "#dadce0",
  "--t-field": "#f1f3f4", "--t-radius": "10px", "--t-font": "Roboto, system-ui, sans-serif",
};
const DEMO_WISHES = [
  { id: "w1", name: "Pak RT", message: "Tempat terbaik untuk menitipkan doa. Pemiliknya serasi sekali. Pasti hadir!", created_at: new Date(Date.now() - 3 * 86400e3).toISOString() },
  { id: "w2", name: "Mbak Tutik", message: "Sudah memantau dari 2020. Akhirnya grand opening juga. ★★★★★", created_at: new Date(Date.now() - 7 * 86400e3).toISOString() },
];
const WISHLIST = [
  { name: "Kasur Queen", price: "Rp3.100.000", icon: ic.bedDouble },
  { name: "Kursi Taman", price: "Rp850.000", icon: ic.armchair },
  { name: "Set Dapur", price: "Rp1.200.000", icon: ic.cookingPot },
];
const STORY_ICONS = [ic.flag, ic.navigation, ic.mapPin];
const EVENT_NOTES = ["Sekarang dinanti", "Ramai lancar"];


function city(address: string) {
  const parts = address.split(",").map(p => p.trim()).filter(Boolean);
  return parts[parts.length - 1] ?? "";
}

function calendarHref(data: ThemeProps["data"]) {
  const start = toDate(data.events[0]?.date ?? data.date);
  if (!start) return undefined;
  const end = new Date(start.getTime() + 3 * 3600e3);
  const fmt = (d: Date) => d.toISOString().replace(/[-:]/g, "").replace(/\.\d{3}/, "");
  const params = new URLSearchParams({
    action: "TEMPLATE", text: `${data.eventLabel ?? "Pernikahan"} ${coupleLabel(data)}`,
    dates: `${fmt(start)}/${fmt(end)}`, location: [data.place, data.address].filter(Boolean).join(", "),
  });
  return `https://calendar.google.com/calendar/render?${params.toString()}`;
}

const nf = new Intl.NumberFormat("id-ID");
const year = (v?: string) => v?.match(/\d{4}/)?.[0];

export default function PetaRuteTheme({ data, slug, guestToken, demo, skipCover }: ThemeProps) {
  const couple = coupleLabel(data);
  const title = `${data.eventLabel ?? "Pernikahan"} ${couple}`;
  const longDate = formatDate(data.date);
  const where = city(data.address);
  const placeLine = [data.place, where && where !== data.place ? where : ""].filter(Boolean).join(", ");
  const countdown = useCountdown(data.date);
  const rsvp = useRsvp({ slug, guestToken, demo });
  const wishes = useWishes({ slug, guestToken, demo, seed: DEMO_WISHES });
  const sheets = useSheets();
  const { copy, copied } = useCopy();
  const [shared, setShared] = useState(false);
  const stories = storyItems(data);
  const start = year(stories[0]?.date);
  const end = formatDate(data.date, { year: "numeric" });
  const span = start && /^\d{4}$/.test(end) ? Number(end) - Number(start) : 0;
  const calendar = calendarHref(data);
  const mainMaps = mapsHref(data, data.events[data.events.length - 1]);
  const hero = data.gallery[0];
  const rest = data.gallery.slice(1);
  const photos = rest.length >= 2 ? rest : data.gallery;
  const shown = photos.slice(0, 5);
  const more = demo ? 18 : photos.length - shown.length;
  const people = [
    { key: "bride", name: data.couple.brideFull ?? data.couple.bride, parents: data.couple.brideParents, photo: data.couple.bridePhoto ?? data.gallery[1] },
    { key: "groom", name: data.couple.groomFull ?? data.couple.groom, parents: data.couple.groomParents, photo: data.couple.groomPhoto ?? data.gallery[2] },
  ];
  const reviews = demo ? "2.700 ulasan" : `${nf.format(wishes.wishes.length)} ucapan`;

  const share = async () => {
    const url = window.location.href;
    try {
      if (navigator.share) await navigator.share({ title, url });
      else { await navigator.clipboard.writeText(url); setShared(true); setTimeout(() => setShared(false), 2000); }
    } catch { /* dismissed */ }
  };

  return (
    <ThemeShell
      fonts={FONTS}
      background="#e8eaed"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.map} aria-hidden><Photo src={MAP} /></div>
          <div className={s.search}>
            <Lucide icon={ic.search} size={18} color="#5f6368" />
            <span>{title}</span>
            <Lucide icon={ic.mic} size={18} color="#1a73e8" />
          </div>
          <div className={s.pin} aria-hidden>
            <span className={s.pinHead}><Lucide icon={ic.heart} size={28} color="#fff" /></span>
            <i />
          </div>
          <span className={s.eta}>{countdown.ready ? (countdown.done ? "Sudah tiba di tujuan" : `${Number(countdown.days)} hari menuju tujuan`) : "Menghitung rute…"}</span>
          <div className={s.sheet}>
            <span className={s.handle} aria-hidden />
            <h1>Rute: Lajang → Pelaminan</h1>
            <p className={s.green}>{[span > 0 ? `${span} tahun` : "", "jalur tercepat lewat kesabaran", "lancar"].filter(Boolean).join(" · ")}</p>
            <ol className={s.route}>
              <li>
                <span className={s.rail} aria-hidden><Lucide icon={ic.circle} size={14} color="#1a73e8" /><i /><i /><i /></span>
                <div className={s.stop}><strong>Kota Lajang</strong>{start && <small>Berangkat {start}</small>}</div>
              </li>
              <li>
                <span className={s.rail} aria-hidden><Lucide icon={ic.mapPin} size={14} color="#ea4335" /></span>
                <div className={s.stop}><strong>Pelaminan — {[data.place, where && where !== data.place ? where : ""].filter(Boolean).join(" ")}</strong><small>Tiba {longDate}{where && where !== data.place ? ` · ${where}` : ""}</small></div>
              </li>
            </ol>
            <div className={s.kepada}>
              <small>Penumpang perjalanan ini</small>
              <strong>{guestLabel(data)}</strong>
            </div>
            <div className={s.coverBtns}>
              <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.navigation} size={16} color="#fff" />Mulai — Buka Undangan</button>
              {calendar && <a className={s.saveBtn} href={calendar} target="_blank" rel="noreferrer"><Lucide icon={ic.bookmark} size={15} color="#1a73e8" />Simpan</a>}
            </div>
          </div>
        </section>
      )}
    >
      <Photo src={hero} alt={`Foto ${couple}`} className={s.hero} />
      <section className={s.place}>
        <h1>{title}</h1>
        <div className={s.rating}>
          {demo ? <><span>5,0</span><span className={s.stars} aria-hidden>★★★★★</span><span>(2.700 ulasan) · Acara Bahagia</span></> : <span>{reviews} · Acara Bahagia</span>}
        </div>
        <p className={s.green}>Buka {longDate}{placeLine ? ` · ${placeLine}` : ""}</p>
        <div className={s.chips}>
          {mainMaps && <a className={`${s.chip} ${s.chipOn}`} href={mainMaps} target="_blank" rel="noreferrer"><Lucide icon={ic.navigation} size={14} color="#fff" />Rute</a>}
          {calendar && <a className={s.chip} href={calendar} target="_blank" rel="noreferrer"><Lucide icon={ic.bookmark} size={14} color="#1a73e8" />Simpan</a>}
          <button type="button" className={s.chip} onClick={share}><Lucide icon={ic.share2} size={14} color="#1a73e8" />{shared ? "Tautan disalin" : "Bagikan"}</button>
          <button type="button" className={s.chip} onClick={sheets.openWish}><Lucide icon={ic.phone} size={14} color="#1a73e8" />Kontak</button>
        </div>
      </section>

      <main className={s.body}>
        <section className={s.section} aria-labelledby="pr-jam">
          <h2 id="pr-jam">Jam Acara</h2>
          {data.events.map((event, index) => {
            const href = mapsHref(data, event);
            const first = index === 0;
            const venue = event.venue && event.venue !== data.place ? [event.venue, event.address].filter(Boolean).join(", ") : "";
            const day = event.date && formatDate(event.date) !== longDate ? formatDate(event.date, { weekday: "short", day: "numeric", month: "short" }) : "";
            return (
              <article key={event.name + index} className={s.event}>
                <Lucide icon={ic.clock3} size={16} color={first ? "#188038" : "#5f6368"} />
                <div className={s.eventText}>
                  <strong className={first ? s.bold : undefined}>{event.name}{event.time ? ` · ${event.time}` : ""}</strong>
                  <small className={first ? s.green : undefined}>{[EVENT_NOTES[Math.min(index, 1)], day, venue].filter(Boolean).join(" · ")}</small>
                </div>
                {href && <a className={s.pill} href={href} target="_blank" rel="noreferrer" aria-label={`Rute ke ${event.name}`}>Rute</a>}
              </article>
            );
          })}
        </section>

        <Extras slot="event" without={["calendar"]} className={s.extras} />

        <section className={s.section} aria-labelledby="pr-pemilik">
          <h2 id="pr-pemilik">Tentang Pemilik Tempat</h2>
          <p className={s.sub}>{start ? `Dikelola dua hati sejak ${start}` : "Dikelola dua hati"}</p>
          {people.map(person => (
            <article key={person.key} className={s.owner}>
              <Photo src={person.photo} alt={person.name} className={s.ownerAv} />
              <div className={s.ownerText}><strong>{person.name}</strong>{person.parents && <small>{person.parents}</small>}</div>
              <span className={s.resmi}><Lucide icon={ic.badgeCheck} size={12} color="#188038" />Resmi</span>
            </article>
          ))}
        </section>

        <Extras slot="opening" className={s.extras} />

        {stories.length > 0 && (
          <section className={s.section} aria-labelledby="pr-riwayat">
            <h2 id="pr-riwayat">Riwayat Perjalananmu Bersama Kami</h2>
            <p className={s.sub}>{start ? `Linimasa ${start} → ${end}` : "Linimasa perjalanan kami"}</p>
            {stories.map((story, index) => (
              <article key={story.title + index} className={s.trip}>
                <span className={s.tripIcon} aria-hidden><Lucide icon={STORY_ICONS[index % STORY_ICONS.length]} size={15} color="#1a73e8" /></span>
                <div className={s.tripText}>
                  <strong>{[story.date, story.title].filter(Boolean).join(" — ")}</strong>
                  <p>{story.body}</p>
                </div>
              </article>
            ))}
          </section>
        )}

        {shown.length > 0 && (
          <section className={s.section} aria-labelledby="pr-foto">
            <h2 id="pr-foto">Foto</h2>
            <p className={s.sub}>Dari pengunjung &amp; pemilik</p>
            <div className={s.photos}>
              {shown.map((src, index) => (
                <div key={src + index} className={index < 2 ? s.big : s.small}>
                  <Photo src={src} alt={`Foto ${index + 1}`} />
                  {index === shown.length - 1 && more > 0 && <span>+{more}</span>}
                </div>
              ))}
            </div>
          </section>
        )}

        <Extras slot="story" className={s.extras} />
        <Extras slot="end" className={s.extras} />

        {(demo || data.gifts.length > 0) && (
          <section className={s.section} aria-labelledby="pr-hadiah">
            <h2 id="pr-hadiah">Kirim Hadiah</h2>
            <p className={s.sub}>{demo ? "Wishlist pemilik tempat" : "Tanda kasih untuk pemilik tempat"}</p>
            {demo && WISHLIST.map(item => (
              <div key={item.name} className={s.item}>
                <span className={s.itemIcon} aria-hidden><Lucide icon={item.icon} size={17} color="#1a73e8" /></span>
                <div><strong>{item.name}</strong><small>{item.price}</small></div>
                <span className={s.pill}>Beri</span>
              </div>
            ))}
            {data.gifts.map(gift => {
              const info = giftInfo(gift);
              return (
                <div key={gift.id} className={s.amplop}>
                  <Lucide icon={ic.wallet} size={17} color="#1a73e8" />
                  <div>
                    <strong>{gift.type === "address" ? "Kirim Kado" : "Amplop Digital"}</strong>
                    <small>{(gift.type === "address" ? [info.number] : [`${info.title} ${info.number}`.trim(), info.holder ? `a.n. ${info.holder}` : ""]).filter(Boolean).join(" · ")}</small>
                  </div>
                  {info.copy && <button type="button" className={s.salin} onClick={() => copy(info.copy)}>{copied === info.copy ? "Tersalin" : "Salin"}</button>}
                  {info.image && <a className={s.salin} href={info.image} target="_blank" rel="noreferrer">Lihat QR</a>}
                </div>
              );
            })}
          </section>
        )}

        <section className={s.section} aria-labelledby="pr-ulasan">
          <h2 id="pr-ulasan">Ulasan</h2>
          <p className={s.sub}>{demo ? "★ 5,0 · 2.700 ulasan" : reviews}</p>
          {wishes.wishes.length === 0 && <p className={s.sub}>Belum ada ulasan. Jadilah yang pertama menitipkan doa!</p>}
          {wishes.wishes.slice(0, 8).map(wish => (
            <article key={wish.id} className={s.review}>
              <div className={s.reviewHead}>
                <span className={s.rAv} aria-hidden>{wish.name.slice(0, 1).toUpperCase()}</span>
                <div><strong>{wish.name}</strong><span><b aria-hidden>★★★★★</b>{timeAgo(wish.created_at)}</span></div>
              </div>
              <p>{wish.message}</p>
            </article>
          ))}
          <button type="button" className={s.write} onClick={sheets.openWish}>Tulis ulasan &amp; doa</button>
        </section>
      </main>

      <nav className={s.bottom} aria-label="Aksi undangan">
        <button type="button" className={s.msg} onClick={sheets.openWish} aria-label="Kirim ucapan"><Lucide icon={ic.messageCircle} size={18} color="#1a73e8" /></button>
        <button type="button" className={s.rsvpBtn} onClick={sheets.openRsvp}><Lucide icon={ic.navigation} size={15} color="#fff" />Konfirmasi Hadir</button>
      </nav>

      <Sheet open={sheets.sheet === "rsvp"} onClose={sheets.close} title="Konfirmasi Kehadiran" tint={tint}>
        <RsvpForm rsvp={rsvp} guestName={data.guestName} demo={demo} />
      </Sheet>
      <Sheet open={sheets.sheet === "wish"} onClose={sheets.close} title="Tulis Ulasan & Doa" tint={tint}>
        <WishForm wishes={wishes} guestName={data.guestName} demo={demo} />
      </Sheet>
    </ThemeShell>
  );
}
