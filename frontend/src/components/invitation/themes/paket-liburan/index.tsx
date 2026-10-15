"use client";
// Theme "Paket Liburan" — undangan bergaya aplikasi pesan paket wisata / e-voucher (design: Fikri & Monica).
import { useState } from "react";
import {
  Extras, Lucide, Photo, RsvpForm, Sheet, ThemeShell, WishForm, formatDate, giftInfo, guestLabel,
  mapsHref, storyItems, useCopy, useCountdown, useRsvp, useSheets, useWishes, type ThemeProps, type ThemeTint,
} from "../kit";
import type { InvitationData } from "../../types";
import { ic } from "./icons";
import s from "./styles.module.css";

const FONTS = ["Poppins:wght@400;600;700;800"];
const tint: ThemeTint = {
  "--t-accent": "#0064d2", "--t-accent-ink": "#ffffff", "--t-bg": "#ffffff", "--t-ink": "#1e2a3b", "--t-muted": "#6e7a8f", "--t-line": "#e3eaf5",
  "--t-field": "#f0f4fb", "--t-radius": "12px", "--t-font": "'Poppins', system-ui, sans-serif",
};
const DEMO_WISHES = [
  { id: "w1", name: "Bang Ipul", message: "Paket terbaik tahun ini. Tour guide-nya serasi banget. Hadir!", created_at: new Date(Date.now() - 2 * 3600e3).toISOString() },
  { id: "w2", name: "Tante Erna", message: "Destinasi akhirnya jelas: pelaminan. Selamat ya kalian!", created_at: new Date(Date.now() - 5 * 3600e3).toISOString() },
];
const DEMO_SCORES = ["9.9", "10"];
const DEMO_CAPTIONS = ["Bromo 2019", "Pantai 2023", "Lamaran"];
const DEMO_WISHLIST = [
  { name: "Koper Honeymoon Set", score: "9.7", price: "Rp1.950.000", icon: ic.luggage },
  { name: "Coffee Maker", score: "9.5", price: "Rp1.250.000", icon: ic.coffee },
  { name: "Bedding Hotel 5★", score: "9.8", price: "Rp950.000", icon: ic.bedDouble },
];
const NAV = [
  { label: "Beranda", icon: ic.house, active: true }, { label: "Pesanan", icon: ic.ticket },
  { label: "Promo", icon: ic.percent }, { label: "Akun", icon: ic.user },
];

type Event = InvitationData["events"][number];

function startTime(event: Event) {
  return event.time?.match(/\d{1,2}[.:]\d{2}/)?.[0]?.replace(":", ".") ?? formatDate(event.date, { hour: "2-digit", minute: "2-digit" }).replace(":", ".");
}

function city(address: string) {
  const parts = address.split(",").map(part => part.trim()).filter(Boolean);
  return parts[parts.length - 1] ?? "";
}

function Status({ time, dark }: { time: string; dark?: boolean }) {
  return (
    <div className={s.status} style={{ color: dark ? "#1e2a3b" : "#fff" }} aria-hidden>
      {time}
      <span><Lucide icon={ic.signal} /><Lucide icon={ic.wifi} /><Lucide icon={ic.batteryFull} /></span>
    </div>
  );
}

export default function PaketLiburanTheme({ data, slug, guestToken, demo, skipCover }: ThemeProps) {
  const { bride, groom } = data.couple;
  const couple = `${groom} & ${bride}`;
  const label = data.eventLabel ?? "Pernikahan";
  const dd = formatDate(data.date, { day: "2-digit" });
  const mm = formatDate(data.date, { month: "2-digit" });
  const yyyy = formatDate(data.date, { year: "numeric" });
  const valid = /^\d+$/.test(dd) && /^\d+$/.test(mm);
  const clock = valid ? `${dd}:${mm}` : "09:41";
  const orderId = valid ? `FM-${dd}${mm}${yyyy}` : "FM-000000";
  const longDate = formatDate(data.date);
  const where = city(data.address);
  const countdown = useCountdown(data.date);
  const events = data.events;
  const schedule = events.map(event => `${event.name.split(" ")[0]} ${startTime(event)}`.trim());
  const venueLine = [data.place, data.address].filter(Boolean).join(", ");
  const distinctVenues = new Set(events.map(event => event.venue)).size > 1;

  const rsvp = useRsvp({ slug, guestToken, demo });
  const wishes = useWishes({ slug, guestToken, demo, seed: DEMO_WISHES });
  const sheets = useSheets();
  const { copy, copied } = useCopy();
  const [shared, setShared] = useState(false);
  const stories = storyItems(data);
  const years = stories.map(story => Number(story.date?.match(/\d{4}/)?.[0] ?? NaN));
  const firstYear = years.find(year => !Number.isNaN(year));
  const gallery = data.gallery;
  const people = [
    { name: data.couple.groomFull ?? groom, parents: data.couple.groomParents, photo: data.couple.groomPhoto ?? gallery[1], note: demo ? "★ 5.0 · 2.190 hari pengalaman" : "Tour guide resmi" },
    { name: data.couple.brideFull ?? bride, parents: data.couple.brideParents, photo: data.couple.bridePhoto ?? gallery[2], note: demo ? "★ 5.0 · pemandu arah hidup" : "Pemandu arah hidup" },
  ];
  const mainMaps = mapsHref(data, events[0]);

  const share = async () => {
    const url = window.location.href;
    try {
      if (navigator.share) await navigator.share({ title: `${label} ${couple}`, url });
      else { await navigator.clipboard.writeText(url); setShared(true); setTimeout(() => setShared(false), 2000); }
    } catch { /* cancelled */ }
  };

  return (
    <ThemeShell
      fonts={FONTS}
      background="#dfe8f5"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.coverHead}>
            <Status time={clock} />
            <h1>Pesananmu Dikonfirmasi!</h1>
            <p>Order ID: {orderId} · Paket Selamanya</p>
          </div>
          <div className={s.coverBody}>
            <div className={s.order}>
              <div className={s.orderHead}>
                <Lucide icon={ic.packageCheck} size={20} color="#b8860b" />
                <div className={s.grow}>
                  <strong>Paket Liburan Selamanya</strong>
                  <small>{couple} · {longDate}{where ? ` · ${where}` : ""}</small>
                </div>
              </div>
              <ul className={s.items}>
                <OrderItem icon={ic.plane} title="1x Perjalanan Cinta" note="Lajang → Menikah · nonstop" tag="GRATIS" />
                <OrderItem icon={ic.building2} title="1x Venue Mewah" note={[data.place, where].filter(Boolean).join(", ")} tag="TERMASUK" />
                {events.length > 0 && <OrderItem icon={ic.ticket} title={`${events.length}x Tiket Acara`} note={schedule.join(" + ")} tag="TERMASUK" />}
                <OrderItem icon={ic.camera} title="1x Atraksi Photo Booth" note="Unlimited pose bersama mempelai" tag="BONUS" bonus />
              </ul>
              <div className={s.total}><span>Total pembayaran</span><strong>Doa &amp; Kehadiranmu</strong></div>
            </div>
            <div className={s.kepada}>
              <small>E-Voucher Atas Nama</small>
              <strong>{guestLabel(data)}</strong>
              <p>Tidak perlu cetak — tunjukkan senyummu saja.</p>
            </div>
            <div className={s.countdown} role="timer" aria-label={`${countdown.days} hari ${countdown.hours} jam ${countdown.minutes} menit lagi`}>
              <div><b>{countdown.days}</b><span>Hari</span></div>
              <div><b>{countdown.hours}</b><span>Jam</span></div>
              <div><b>{countdown.minutes}</b><span>Menit</span></div>
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.ticketCheck} size={17} color="#ffc900" />Lihat E-Voucher — Buka Undangan</button>
          </div>
          <div className={s.tabbar} aria-hidden>
            {NAV.map(item => (
              <span key={item.label} className={item.active ? s.tabActive : undefined}>
                <Lucide icon={item.icon} size={22} color={item.active ? "#0064d2" : "#6e7a8f"} />{item.label}
              </span>
            ))}
          </div>
        </section>
      )}
    >
      <header className={s.top}>
        <Status time={clock} dark />
        <div className={s.nav}>
          <span aria-hidden><Lucide icon={ic.arrowLeft} size={20} color="#1e2a3b" /></span>
          <div className={s.navTitle}>
            <h1>E-Voucher Saya</h1>
            <p>{label} {couple}</p>
          </div>
          <button type="button" className={s.share} onClick={share} aria-label={shared ? "Tautan disalin" : "Bagikan undangan"}>
            <Lucide icon={shared ? ic.ticketCheck : ic.share2} size={18} color="#1e2a3b" />
          </button>
        </div>
      </header>

      <main className={s.body}>
        <section className={s.voucher} aria-label="E-voucher">
          <div className={s.vHead}><span>E-Voucher · {events.length} Tiket Acara</span><em>Aktif</em></div>
          <div className={s.vBody}>
            <span className={s.qr} aria-hidden><Lucide icon={ic.qrCode} size={58} color="#1e2a3b" /></span>
            <div className={s.grow}>
              {schedule.length > 0 && <strong>{schedule.join(" · ")} WIB</strong>}
              <span className={s.vDate}>{longDate}</span>
              <small>{venueLine}</small>
              {mainMaps && !distinctVenues && <a href={mainMaps} target="_blank" rel="noreferrer" className={s.mapLink}><Lucide icon={ic.mapPin} size={12} color="#0064d2" />Lihat peta venue</a>}
            </div>
          </div>
          {distinctVenues && (
            <ul className={s.venues}>
              {events.map((event, index) => {
                const href = mapsHref(data, event);
                return (
                  <li key={event.name + index}>
                    <div className={s.grow}>
                      <strong>{event.name} · {event.time}</strong>
                      <small>{[event.venue, event.address].filter(Boolean).join(", ")}</small>
                    </div>
                    {href && <a href={href} target="_blank" rel="noreferrer" className={s.mapLink} aria-label={`Lihat peta ${event.venue}`}><Lucide icon={ic.mapPin} size={12} color="#0064d2" />Peta</a>}
                  </li>
                );
              })}
            </ul>
          )}
        </section>

        <Extras slot="event" className={s.extras} />

        <section className={s.card} aria-labelledby="pl-guide">
          <div className={s.head}><h2 id="pl-guide">Tour Guide Kamu</h2></div>
          {people.map(person => (
            <article key={person.name} className={s.person}>
              <Photo src={person.photo} alt={person.name} className={s.avatar} />
              <div className={s.grow}>
                <strong>{person.name}</strong>
                {person.parents && <small>{person.parents}</small>}
                <em>{person.note}</em>
              </div>
            </article>
          ))}
        </section>

        <Extras slot="opening" className={s.extras} />

        {stories.length > 0 && (
          <section className={s.card} aria-labelledby="pl-story">
            <div className={s.head}><h2 id="pl-story">Itinerary Cinta</h2>{firstYear && yyyy && <span>{firstYear} → {yyyy}</span>}</div>
            <ol className={s.itinerary}>
              {stories.map((story, index) => {
                const year = years[index];
                const day = firstYear !== undefined && !Number.isNaN(year) ? Math.max(1, (year - firstYear) * 365) : index + 1;
                return (
                  <li key={story.body + index}>
                    <span className={s.flag} aria-hidden><Lucide icon={ic.flag} size={13} color="#0064d2" /></span>
                    <div className={s.grow}>
                      <strong>{[`Hari ${day.toLocaleString("id-ID")}`, story.date, story.title].filter(Boolean).join(" · ")}</strong>
                      <p>{story.body}</p>
                      {story.image && <Photo src={story.image} alt={story.title} className={s.storyImg} />}
                    </div>
                  </li>
                );
              })}
            </ol>
          </section>
        )}

        {gallery.length > 0 && (
          <section className={s.card} aria-labelledby="pl-gallery">
            <div className={s.head}><h2 id="pl-gallery">Galeri Destinasi</h2><span>{gallery.length} foto</span></div>
            <div className={s.grid}>
              {gallery.map((src, index) => (
                <figure key={src + index}>
                  <Photo src={src} alt={`Foto destinasi ${index + 1}`} />
                  {demo && DEMO_CAPTIONS[index] && <figcaption>{DEMO_CAPTIONS[index]}</figcaption>}
                </figure>
              ))}
            </div>
          </section>
        )}

        <Extras slot="story" className={s.extras} />
        <Extras slot="end" className={s.extras} />

        {(demo || data.gifts.length > 0) && (
          <section className={s.card} aria-labelledby="pl-gift">
            <div className={s.head}><h2 id="pl-gift">Tambah ke Pesanan · Kado</h2>{demo && <span>Wishlist</span>}</div>
            {demo && DEMO_WISHLIST.map(item => (
              <div key={item.name} className={s.item}>
                <span className={s.itemIcon} aria-hidden><Lucide icon={item.icon} size={17} color="#0064d2" /></span>
                <div className={s.grow}>
                  <strong>{item.name}</strong>
                  <span className={s.scoreRow}><i>{item.score}</i>{item.price}</span>
                </div>
                <span className={s.yellow} aria-hidden>+ Pesan</span>
              </div>
            ))}
            {data.gifts.map(gift => {
              const info = giftInfo(gift);
              return (
                <div key={gift.id} className={s.amplop}>
                  <Lucide icon={ic.wallet} size={17} color="#ffc900" />
                  <div className={s.grow}>
                    <strong>{gift.type === "address" ? "Alamat Kirim Kado" : gift.type === "qris" ? "QRIS" : "Amplop Digital"}</strong>
                    <small>{[gift.type === "bank" || gift.type === "ewallet" ? `${info.title} ${info.number}` : info.number, info.holder ? `a.n. ${info.holder}` : ""].filter(Boolean).join(" · ")}</small>
                    {info.image && <Photo src={info.image} alt="Kode QRIS" className={s.qris} />}
                  </div>
                  {info.copy && <button type="button" className={s.yellow} onClick={() => copy(info.copy)}>{copied === info.copy ? "Tersalin" : "Salin"}</button>}
                </div>
              );
            })}
          </section>
        )}

        <section className={s.card} aria-labelledby="pl-wishes">
          <div className={s.head}><h2 id="pl-wishes">Ulasan Traveler</h2><span>{demo ? "★ 9.8 · 312 ulasan" : `${wishes.wishes.length} ulasan`}</span></div>
          {wishes.wishes.length === 0 && <p className={s.empty}>Belum ada ulasan. Jadilah traveler pertama yang menulis doa!</p>}
          {wishes.wishes.slice(0, 8).map((wish, index) => (
            <article key={wish.id} className={s.review}>
              <span className={s.score} aria-hidden>{demo && DEMO_SCORES[index] && !wish.id.startsWith("local-") ? DEMO_SCORES[index] : wish.name.slice(0, 1).toUpperCase()}</span>
              <div className={s.grow}><strong>{wish.name}</strong><p>{wish.message}</p></div>
            </article>
          ))}
        </section>
      </main>

      <nav className={s.bottom} aria-label="Aksi undangan">
        <button type="button" className={s.chat} onClick={sheets.openWish} aria-label="Kirim ucapan"><Lucide icon={ic.messageCircle} size={18} color="#0064d2" /></button>
        <button type="button" className={s.rsvp} onClick={sheets.openRsvp}><Lucide icon={ic.ticketCheck} color="#fff" />Konfirmasi Hadir</button>
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

function OrderItem({ icon, title, note, tag, bonus }: { icon: string; title: string; note: string; tag: string; bonus?: boolean }) {
  return (
    <li className={s.orderItem}>
      <span className={s.itemIcon} aria-hidden><Lucide icon={icon} color="#0064d2" /></span>
      <div className={s.grow}><strong>{title}</strong>{note && <small>{note}</small>}</div>
      <span className={bonus ? s.tagBonus : s.tag}>{tag}</span>
    </li>
  );
}
