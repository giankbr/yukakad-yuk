"use client";
// Theme "Hijau Ojek" — undangan bergaya aplikasi ojek online (design: Undangan — Tema Hijau Ojek (Sigit & Ratna)).
import { useState, type CSSProperties } from "react";
import { toast } from "@/lib/celebrate";
import {
  Extras, Lucide, Photo, RsvpForm, Sheet, ThemeShell, Tick, WishForm, dateParts, formatDate, giftInfo, guestLabel,
  mapsHref, storyItems, timeAgo, toDate, useCopy, useCountdown, useRsvp, useSheets, useWishes, type ThemeProps, type ThemeTint,
} from "../kit";
import { ic } from "./icons";
import s from "./styles.module.css";

const FONTS = ["Plus Jakarta Sans:wght@400;600;700;800"];
const FONT = "'Plus Jakarta Sans', system-ui, sans-serif";
const tint: ThemeTint = {
  "--t-accent": "#00aa13", "--t-accent-ink": "#ffffff", "--t-bg": "#ffffff", "--t-ink": "#1a1a1a", "--t-muted": "#697077", "--t-line": "#e0e3e7",
  "--t-field": "#f6f7f8", "--t-radius": "14px", "--t-font": FONT,
};
const DEMO_WISHES = [
  { id: "w1", name: "Mas Bowo", message: "Mantap! Semoga perjalanan rumah tangganya selalu lancar tanpa macet.", attendance: "yes" as const, created_at: new Date(Date.now() - 2 * 3600e3).toISOString() },
  { id: "w2", name: "Dina", message: "Bintang lima buat kalian berdua! Samawa ya!", attendance: "yes" as const, created_at: new Date(Date.now() - 5 * 3600e3).toISOString() },
];
const DEMO_TAG: Record<string, string> = { w1: "Hadir · 2 orang", w2: "Hadir · 1 orang" };
const ATTEND: Record<string, string> = { yes: "Hadir", maybe: "Ragu", no: "Berhalangan" };
const DEMO_PRODUCTS = [
  { name: "Microwave", price: "Rp1.250.000", art: "p-microwave", bg: "#fff3e0" },
  { name: "Sofa Mini", price: "Rp2.400.000", art: "p-sofa", bg: "#e8f1ff" },
  { name: "Mesin Kopi", price: "Rp899.000", art: "p-coffee", bg: "#e6f6e6" },
];
const ART = "/themes/art/hijau-ojek";

/** Painted (gouache + ink) decorative image — never opens the photo lightbox. */
function Art({ name, w, h, className, eager }: { name: string; w: number; h: number; className?: string; eager?: boolean }) {
  return (
    // eslint-disable-next-line @next/next/no-img-element -- static painted illustration
    <img src={`${ART}/${name}.webp`} alt="" aria-hidden width={w} height={h} className={className} data-nolightbox
      loading={eager ? "eager" : "lazy"} fetchPriority={eager ? "high" : undefined} decoding="async" draggable={false} />
  );
}


function city(address: string) {
  const parts = address.split(",").map(part => part.trim()).filter(Boolean);
  return parts[parts.length - 1] ?? "";
}

export default function HijauOjekTheme({ data, slug, guestToken, demo, skipCover }: ThemeProps) {
  const { couple } = data;
  const names = `${couple.groom} & ${couple.bride}`;
  const parts = dateParts(data.date);
  const date = toDate(data.date);
  const ddmm = date ? `${parts.day.padStart(2, "0")}${String(date.getMonth() + 1).padStart(2, "0")}` : "";
  const plate = ddmm ? `${couple.groom.slice(0, 1).toUpperCase()} ${ddmm} ${couple.bride.slice(0, 2).toUpperCase()}` : "";
  const longDate = formatDate(data.date);
  const where = city(data.address) || data.place;
  const countdown = useCountdown(data.date);
  const rsvp = useRsvp({ slug, guestToken, demo });
  const wishes = useWishes({ slug, guestToken, demo, seed: DEMO_WISHES });
  const sheets = useSheets();
  const { copy, copied } = useCopy();
  const stories = storyItems(data);
  const coverPhoto = data.gallery[0];
  const gallery = data.gallery.length > 3 ? data.gallery.slice(1) : data.gallery;
  const people = [
    { key: "groom", name: couple.groomFull ?? couple.groom, parents: couple.groomParents, photo: couple.groomPhoto ?? data.gallery[1], note: "4 th jadi partner setia" },
    { key: "bride", name: couple.brideFull ?? couple.bride, parents: couple.brideParents, photo: couple.bridePhoto ?? data.gallery[2], note: "Selalu kasih bintang 5" },
  ];
  const daysLeft = Number(countdown.days);
  const eta = !countdown.ready ? "Menuju hari bahagia" : countdown.done ? "Hari bahagia telah tiba!" : <>Menuju hari bahagia · <Tick value={daysLeft} /> hari lagi</>;
  const [cart, setCart] = useState<string[]>([]);
  const [stars, setStars] = useState(0);
  const toggleCart = (name: string) => {
    const on = !cart.includes(name);
    setCart(c => (on ? [...c, name] : c.filter(n => n !== name)));
    toast(on ? "Masuk keranjang kado" : "Dihapus dari keranjang");
  };
  const rate = (value: number) => {
    setStars(value);
    toast(value === 5 ? "Terima kasih atas bintang 5!" : `Kamu memberi ${value} bintang`);
  };
  const menu = [
    { label: "Mempelai", href: "#ho-couple", icon: ic.users, bg: "#00aa13" },
    ...data.events.slice(0, 2).map((event, index) => ({ label: event.name.split(" ")[0], href: `#ho-event-${index}`, icon: index === 0 ? ic.heartHandshake : ic.partyPopper, bg: index === 0 ? "#e8551e" : "#2d7ff9" })),
    data.gifts.length > 0 ? { label: "Kado", href: "#ho-gift", icon: ic.gift, bg: "#8d5cf6" } : { label: "Ucapan", href: "#ho-wishes", icon: ic.messageCircleHeart, bg: "#8d5cf6" },
  ];

  return (
    <ThemeShell
      fonts={FONTS}
      background="#e3e7ea"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.map} aria-hidden><Art name="map" w={640} h={1180} eager /></div>
          <div className={s.mapArea}>
            <svg className={s.routeLine} viewBox="0 0 390 360" preserveAspectRatio="none" aria-hidden>
              <path d="M40 40 C 90 120, 40 170, 120 200 S 250 160, 195 300" />
            </svg>
            <span className={s.riderStart} aria-hidden><Art name="rider" w={440} h={318} eager /></span>
            <span className={s.pin} aria-hidden><Lucide icon={ic.heart} size={32} color="#00aa13" /></span>
            <span className={s.eta}>{eta}</span>
          </div>
          <div className={s.sheet}>
            <i className={s.handle} aria-hidden />
            <div className={s.arrived}><i aria-hidden />Pasangan bahagia telah tiba di tujuan!</div>
            <div className={s.driver}>
              <Photo src={coverPhoto} alt={`Foto ${names}`} className={s.driverPhoto} />
              <div className={s.driverText}>
                <strong>{names}</strong>
                <small>{[plate, "Skuter Cinta Matic"].filter(Boolean).join(" · ")}</small>
                {demo
                  ? <span><b aria-hidden>★</b>5.0 · 2.700 perjalanan bersama</span>
                  : <span>{data.eventLabel ?? "Pernikahan"}</span>}
              </div>
              {ddmm && <div className={s.pinCode}><small>PIN</small><strong>{ddmm}</strong></div>}
            </div>
            <div className={s.route}>
              <div className={s.routeRow}>
                <span className={s.rail} aria-hidden><Lucide icon={ic.circle} size={14} color="#697077" /><i /></span>
                <div className={s.routeText} style={{ paddingBottom: 10 }}><small>Titik jemput</small><span>Dua kehidupan yang berbeda</span></div>
              </div>
              <div className={s.routeRow}>
                <span className={s.rail} aria-hidden><Lucide icon={ic.mapPin} size={14} color="#00aa13" /></span>
                <div className={s.routeText}><small>Tujuan</small><span>{["Pelaminan", longDate, where].filter(Boolean).join(" · ")}</span></div>
              </div>
            </div>
            <div className={s.kepada}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              <em>Di tempat · mohon maaf bila ada salah penulisan nama</em>
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} color="#fff" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <header className={s.header}>
        <h1>Selamat datang, Tamu Istimewa!</h1>
        <div className={s.search}><Lucide icon={ic.search} color="#00aa13" /><span>Cari momen bahagia {names}…</span></div>
      </header>

      <main className={s.body}>
        <div className={s.saldo}>
          <button type="button" onClick={sheets.openWish}>
            <Lucide icon={ic.handHeart} size={18} color="#00aa13" />
            <span><strong>∞</strong><small>Doa</small></span>
          </button>
          {demo ? (
            <div><Lucide icon={ic.smile} size={18} color="#00aa13" /><span><strong>100%</strong><small>Restu</small></span></div>
          ) : (
            <a href="#ho-wishes"><Lucide icon={ic.smile} size={18} color="#00aa13" /><span><strong>{wishes.wishes.length}</strong><small>Ucapan</small></span></a>
          )}
          <button type="button" onClick={sheets.openRsvp}>
            <Lucide icon={ic.calendarCheck} size={18} color="#00aa13" />
            <span><strong>RSVP</strong><small>Hadir</small></span>
          </button>
        </div>
        <div className={s.spacer} aria-hidden />

        <nav className={s.menu} aria-label="Menu undangan">
          {menu.map(item => (
            <a key={item.href} href={item.href} className={s.menuItem}>
              <span style={{ background: item.bg }}><Lucide icon={item.icon} size={24} color="#fff" /></span>
              {item.label}
            </a>
          ))}
        </nav>

        <Extras slot="opening" className={s.extras} />

        <section className={s.section} id="ho-couple" aria-labelledby="ho-couple-h">
          <div className={s.head}><h2 id="ho-couple-h">Profil Pengemudi Cinta</h2><span>Lengkap</span></div>
          {people.map(person => (
            <article key={person.key} className={s.person}>
              <Photo src={person.photo} alt={person.name} className={s.personPhoto} />
              <div className={s.personText}>
                <strong>{person.name}</strong>
                {person.parents && <small>{person.parents}</small>}
                {demo && <span><b>★ 5.0</b>· {person.note}</span>}
              </div>
              <em className={s.verified}>Terverifikasi</em>
            </article>
          ))}
        </section>

        {stories.length > 0 && (
          <section className={s.section} aria-labelledby="ho-story">
            <div className={s.head}><h2 id="ho-story">Riwayat Perjalanan</h2><span>Semua</span></div>
            <ol className={s.trips}>
              {stories.map((story, index) => {
                const last = index === stories.length - 1 && stories.length > 1;
                return (
                  <li key={story.title + index} className={s.trip} style={{ "--d": `${index * 90}ms` } as CSSProperties}>
                    <span className={`${s.tripIcon} ${last ? s.tripNow : ""}`} aria-hidden>
                      <Lucide icon={last ? ic.navigation : ic.check} size={15} color={last ? "#fff" : "#008a0f"} />
                    </span>
                    <div className={s.tripText}>
                      <div><strong>{story.title}</strong>{story.date && <small>{story.date}</small>}</div>
                      <p>{story.body}</p>
                      {story.image && <Photo src={story.image} alt={story.title} className={s.tripImg} />}
                    </div>
                  </li>
                );
              })}
            </ol>
          </section>
        )}

        <section className={s.section} aria-labelledby="ho-events">
          <div className={s.head}><h2 id="ho-events">Detail Pesanan</h2></div>
          {data.events.map((event, index) => {
            const href = mapsHref(data, event);
            return (
              <article key={event.name + index} id={`ho-event-${index}`} className={s.event}>
                <span className={s.eventIcon} aria-hidden><Lucide icon={index === 0 ? ic.heartHandshake : ic.partyPopper} size={20} color="#008a0f" /></span>
                <div className={s.eventText}>
                  <strong>{event.name}</strong>
                  <b>{[formatDate(event.date, { weekday: "long", day: "numeric", month: "short" }), event.time].filter(Boolean).join(" · ")}</b>
                  <small>{[event.venue, event.address].filter(Boolean).join(", ")}</small>
                </div>
                {href && <a className={s.routeBtn} href={href} target="_blank" rel="noreferrer" aria-label={`Rute ke ${event.venue}`}>Rute</a>}
              </article>
            );
          })}
        </section>

        <Extras slot="event" className={s.extras} />

        {gallery.length > 0 && (
          <section className={s.section} aria-labelledby="ho-gallery">
            <div className={s.head}><h2 id="ho-gallery">Galeri Perjalanan</h2><span>{demo ? "24 foto" : `${gallery.length} foto`}</span></div>
            <div className={s.big}>
              <Photo src={gallery[0]} alt="Foto galeri 1" />
              {demo && <span className={s.cap}><Lucide icon={ic.mapPin} size={12} color="#00aa13" />Kemang, Jakarta</span>}
            </div>
            {gallery.length > 1 && (
              <div className={s.grid}>
                {gallery.slice(1).map((src, index) => (
                  <figure key={src + index}>
                    <Photo src={src} alt={`Foto galeri ${index + 2}`} />
                    {index < 2 && <figcaption>{index === 0 ? "Titik jemput pertama" : "Menuju tujuan"}</figcaption>}
                  </figure>
                ))}
              </div>
            )}
          </section>
        )}

        <Extras slot="story" className={s.extras} />

        {demo && (
          <section className={s.section} aria-labelledby="ho-wishlist">
            <div className={s.head}><h2 id="ho-wishlist">Wishlist Kado</h2><span>Belanja</span></div>
            <div className={s.products}>
              {DEMO_PRODUCTS.map(item => (
                <div key={item.name} className={s.product} data-on={cart.includes(item.name) ? "" : undefined}>
                  <span style={{ background: item.bg }}><Art name={item.art} w={150} h={150} /></span>
                  <strong>{item.name}</strong>
                  <b>{item.price}</b>
                  <button type="button" aria-pressed={cart.includes(item.name)} onClick={() => toggleCart(item.name)}>{cart.includes(item.name) ? "✓ Dipilih" : "Beli"}</button>
                </div>
              ))}
            </div>
          </section>
        )}

        <Extras slot="end" className={s.extras} />

        {data.gifts.length > 0 && (
          <section className={s.section} id="ho-gift" aria-labelledby="ho-gift-h">
            <div className={s.head}><h2 id="ho-gift-h">Kirim Tanda Kasih</h2></div>
            {data.gifts.map(gift => {
              const info = giftInfo(gift);
              const title = gift.type === "address" ? "Alamat Kado" : info.title;
              return (
                <div key={gift.id} className={s.wallet}>
                  <span className={s.walletIcon} aria-hidden><Lucide icon={gift.type === "address" ? ic.gift : ic.wallet} size={20} color="#fff" /></span>
                  <div>
                    <strong>{title}</strong>
                    <small>{[info.number, info.holder ? `a.n. ${info.holder}` : ""].filter(Boolean).join(" · ")}</small>
                    {info.image && <Photo src={info.image} alt="Kode QRIS" className={s.qris} />}
                  </div>
                  {info.copy && <button type="button" data-copied={copied === info.copy ? "" : undefined} onClick={() => copy(info.copy)}>{copied === info.copy ? "Tersalin" : "Salin"}</button>}
                </div>
              );
            })}
          </section>
        )}

        <section className={s.section} id="ho-wishes" aria-labelledby="ho-wishes-h">
          <div className={s.head}>
            <h2 id="ho-wishes-h">Chat Ucapan</h2>
            <span>{demo ? "248" : wishes.wishes.length}</span>
          </div>
          {wishes.wishes.length === 0 && <p className={s.empty}>Belum ada ucapan. Jadilah yang pertama mengirim doa!</p>}
          {wishes.wishes.slice(0, 8).map((wish, index) => (
            <article key={wish.id} className={s.chat} style={{ "--d": `${index * 80}ms` } as CSSProperties}>
              <span className={s.avatar} aria-hidden>{wish.name.slice(0, 1).toUpperCase()}</span>
              <div className={s.bubble}>
                <div><strong>{wish.name}</strong><small>{(demo && DEMO_TAG[wish.id]) || (wish.attendance ? ATTEND[wish.attendance] : timeAgo(wish.created_at))}</small></div>
                <p>{wish.message}</p>
              </div>
            </article>
          ))}
        </section>

        <section className={s.rateCard} aria-labelledby="ho-rate">
          <span className={s.rateArt} aria-hidden><Art name="rider" w={440} h={318} /></span>
          <h2 id="ho-rate">Bagaimana perjalanan cinta mereka?</h2>
          <p>Beri bintang untuk {names}</p>
          <div className={s.rate} role="radiogroup" aria-label="Beri bintang">
            {[1, 2, 3, 4, 5].map(value => (
              <button key={value} type="button" role="radio" aria-checked={stars === value} aria-label={`${value} bintang`} data-on={stars >= value ? "" : undefined}
                style={{ transitionDelay: `${(value - 1) * 40}ms` }} onClick={() => rate(value)}>★</button>
            ))}
          </div>
          {stars > 0 && <small key={stars}>{stars === 5 ? "Sempurna! Doamu ikut menemani perjalanan mereka." : "Terima kasih atas penilaianmu."}</small>}
        </section>

        <footer className={s.note}><a href="/" target="_blank" rel="noreferrer">dibuat dengan ♥ di Rawuh</a></footer>
      </main>

      <nav className={s.bottom} aria-label="Aksi undangan">
        <button type="button" className={s.chatBtn} onClick={sheets.openWish} aria-label="Kirim ucapan"><Lucide icon={ic.messageCircleHeart} size={20} color="#00aa13" /></button>
        <button type="button" className={s.rsvpBtn} onClick={sheets.openRsvp}>Konfirmasi Kehadiran</button>
      </nav>

      <Sheet open={sheets.sheet === "rsvp"} onClose={sheets.close} title="Konfirmasi Kehadiran" tint={tint}>
        <RsvpForm rsvp={rsvp} guestName={data.guestName} demo={demo} />
      </Sheet>
      <Sheet open={sheets.sheet === "wish"} onClose={sheets.close} title="Kirim Ucapan" tint={tint}>
        <WishForm wishes={wishes} guestName={data.guestName} demo={demo} />
      </Sheet>
    </ThemeShell>
  );
}
