"use client";
// Theme "Rencana Perjalanan" — undangan bergaya aplikasi travel/itinerary (design: Arga & Bella, Bali).
import {
  Lucide, Photo, RsvpForm, Sheet, ThemeShell, WishForm, dateParts, formatDate, giftInfo, guestLabel,
  mapsHref, safeUrl, storyItems, useCopy, useRsvp, useSheets, useWishes, type ThemeProps, type ThemeTint,
} from "../kit";
import type { InvitationData } from "../../types";
import { ic } from "./icons";
import s from "./styles.module.css";

const FONTS = ["Mulish:wght@400;600;700;800"];
const tint: ThemeTint = {
  "--t-accent": "#ff5e1f", "--t-bg": "#ffffff", "--t-ink": "#1f2a37", "--t-muted": "#687176", "--t-line": "#e4eef7",
  "--t-field": "#f3f8fc", "--t-radius": "12px", "--t-font": "'Mulish', system-ui, sans-serif",
};
const DEMO_WISHES = [
  { id: "w1", name: "Gede M.", message: "Itinerary paling ditunggu. Sunset, cinta, dan makan enak. Hadir!", created_at: new Date(Date.now() - 2 * 3600e3).toISOString() },
  { id: "w2", name: "Kak Sari", message: "Dua backpacker akhirnya settle. Perjalanan terbaik memang pulang ke satu orang.", created_at: new Date(Date.now() - 5 * 3600e3).toISOString() },
];
const DEMO_WISHLIST = [
  { name: "Paket Honeymoon Lombok", tag: "Best Seller", price: "Rp2.500.000", icon: ic.luggage },
  { name: "Kamera Mirrorless", tag: "", price: "Rp6.900.000", icon: ic.camera },
  { name: "Glamping Set", tag: "Promo", price: "Rp1.700.000", icon: ic.tent },
];

type Event = InvitationData["events"][number];

function startTime(event: Event) {
  return event.time?.match(/\d{1,2}[.:]\d{2}/)?.[0]?.replace(":", ".") ?? formatDate(event.date, { hour: "2-digit", minute: "2-digit" }).replace(":", ".");
}

function eventIcon(name: string) {
  if (/akad|nikah|pemberkatan|sumpah|janji/i.test(name)) return ic.heartHandshake;
  if (/resepsi|pesta|party|dinner/i.test(name)) return ic.partyPopper;
  if (/foto|photo/i.test(name)) return ic.camera;
  if (/kumpul|tamu|registrasi/i.test(name)) return ic.users;
  return ic.heart;
}

function city(address: string) {
  const parts = address.split(",").map(part => part.trim()).filter(Boolean);
  return parts[parts.length - 1] ?? "";
}

function Status() {
  return (
    <div className={s.status} aria-hidden>
      09:11
      <span><Lucide icon={ic.signal} /><Lucide icon={ic.wifi} /><Lucide icon={ic.batteryFull} /></span>
    </div>
  );
}

export default function RencanaPerjalananTheme({ data, slug, guestToken, demo, skipCover }: ThemeProps) {
  const { bride, groom } = data.couple;
  const couple = `${groom} & ${bride}`;
  const label = data.eventLabel ?? "Pernikahan";
  const parts = dateParts(data.date);
  const where = city(data.address);
  const shortDate = formatDate(data.date, { day: "numeric", month: "short", year: "numeric" });
  const midDate = formatDate(data.date, { weekday: "long", day: "numeric", month: "short", year: "numeric" });
  const dayTag = parts.day ? `${parts.weekdayShort.slice(0, 1)}${parts.weekdayShort.slice(1).toLowerCase()}, ${parts.day} ${parts.monthShort.slice(0, 1)}${parts.monthShort.slice(1).toLowerCase()}` : "";
  const mainDay = formatDate(data.date, { day: "numeric", month: "long", year: "numeric" });

  const rsvp = useRsvp({ slug, guestToken, demo });
  const wishes = useWishes({ slug, guestToken, demo, seed: DEMO_WISHES });
  const sheets = useSheets();
  const { copy, copied } = useCopy();
  const stories = storyItems(data);
  const hero = data.gallery[0];
  const gallery = data.gallery.length > 3 ? data.gallery.slice(1) : data.gallery;
  const people = [
    { name: data.couple.groomFull ?? groom, parents: data.couple.groomParents, photo: data.couple.groomPhoto ?? data.gallery[1] },
    { name: data.couple.brideFull ?? bride, parents: data.couple.brideParents, photo: data.couple.bridePhoto ?? data.gallery[2] },
  ];
  const mainMaps = mapsHref(data);

  return (
    <ThemeShell
      fonts={FONTS}
      background="#dcebf6"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.hero}>
            <Photo src={hero} alt={`Foto ${couple}`} className={s.heroImg} />
            <span className={s.dim} aria-hidden />
            <Status />
            <div className={s.heroText}>
              <small>Perjalanan Seumur Hidup</small>
              <h1>{couple}{where || shortDate ? " — " : ""}{[where, shortDate].filter(Boolean).join(", ")}</h1>
            </div>
          </div>
          <div className={s.coverBody}>
            <div className={s.search}>
              <SearchRow icon={ic.plane} kicker="Perjalanan" title="Masa Lajang → Pelaminan" note="1 rute, tanpa kembali" />
              <SearchRow icon={ic.building2} kicker="Venue" title={data.place} note={midDate} />
              <SearchRow icon={ic.users} kicker="Tamu" title="2 Dewasa + keluarga besar" note="Kursi VIP tersedia" />
            </div>
            <div className={s.kepada}>
              <small>Traveler Utama</small>
              <strong>{guestLabel(data)}</strong>
              <p>Semua biaya ditanggung kebahagiaan kami.</p>
            </div>
            <button type="button" className={s.orange} onClick={open}><Lucide icon={ic.search} size={17} color="#fff" />Cari &amp; Buka Undangan</button>
            <div className={s.perks} aria-hidden>
              <span><Lucide icon={ic.shieldCheck} size={11} color="#0194f3" />Pasti bahagia</span>
              <span><Lucide icon={ic.refreshCcw} size={11} color="#0194f3" />Tanpa refund</span>
              {demo ? <span><Lucide icon={ic.star} size={11} color="#0194f3" />Rating 5.0</span> : <span><Lucide icon={ic.heart} size={11} color="#0194f3" />Penuh doa</span>}
            </div>
          </div>
        </section>
      )}
    >
      <header className={s.top}>
        <Status />
        <div className={s.nav}>
          <h1>Itinerary Perjalananmu</h1>
          <p>{label} {couple} · {midDate}{where ? ` · ${where}` : ""}</p>
        </div>
      </header>

      <main className={s.body}>
        {data.events.length > 0 && (
          <section className={s.card} aria-labelledby="rp-day">
            <div className={s.head}><h2 id="rp-day">Itinerary Hari H</h2>{dayTag && <span>{dayTag}</span>}</div>
            <ol className={s.day}>
              {data.events.map((event, index) => {
                const own = safeUrl(event.mapsUrl) || event.address ? mapsHref(data, event) : undefined;
                const otherDay = event.date && formatDate(event.date, { day: "numeric", month: "long", year: "numeric" }) !== mainDay;
                return (
                  <li key={event.name + index}>
                    <b className={s.time}>{startTime(event)}</b>
                    <span className={s.rail} aria-hidden>
                      <i><Lucide icon={eventIcon(event.name)} size={12} color="#0194f3" /></i>
                      {index < data.events.length - 1 && <em />}
                    </span>
                    <div className={s.grow}>
                      <strong>{event.name}</strong>
                      <small>{[otherDay ? formatDate(event.date, { weekday: "long", day: "numeric", month: "short" }) : "", event.time && !/^\d{1,2}[.:]\d{2}$/.test(event.time.trim()) ? event.time : "", event.venue, event.address].filter(Boolean).join(" · ")}</small>
                      {own && <a href={own} target="_blank" rel="noreferrer" className={s.pin}><Lucide icon={ic.mapPin} size={11} color="#0194f3" />Lihat peta</a>}
                    </div>
                  </li>
                );
              })}
            </ol>
            {mainMaps && (
              <a href={mainMaps} target="_blank" rel="noreferrer" className={s.outline}><Lucide icon={ic.mapPin} size={14} color="#0194f3" />Lihat Lokasi Venue di Maps</a>
            )}
          </section>
        )}

        <section className={s.card} aria-labelledby="rp-host">
          <div className={s.head}><h2 id="rp-host">Host Perjalananmu</h2></div>
          <div className={s.hosts}>
            {people.map(person => (
              <article key={person.name} className={s.host}>
                <Photo src={person.photo} alt={person.name} />
                <div>
                  <strong>{person.name}</strong>
                  {person.parents && <small>{person.parents}</small>}
                </div>
              </article>
            ))}
          </div>
        </section>

        {stories.length > 0 && (
          <section className={s.card} aria-labelledby="rp-story">
            <div className={s.head}><h2 id="rp-story">Riwayat Perjalanan Kami</h2><span>{stories.length} trip</span></div>
            <ol className={s.trips}>
              {stories.map((story, index) => (
                <li key={story.body + index}>
                  <span className={s.tripIcon} aria-hidden><Lucide icon={ic.mapPin} size={13} color="#0194f3" /></span>
                  <div className={s.grow}>
                    <strong>{[`Trip #${index + 1}`, story.date, story.title].filter(Boolean).join(" · ")}</strong>
                    <p>{story.body}</p>
                    {story.image && <Photo src={story.image} alt={story.title || `Trip ${index + 1}`} className={s.storyImg} />}
                  </div>
                </li>
              ))}
            </ol>
          </section>
        )}

        {gallery.length > 0 && (
          <section className={s.card} aria-labelledby="rp-gallery">
            <div className={s.head}><h2 id="rp-gallery">Xperience · Galeri</h2><span>{gallery.length}</span></div>
            <div className={s.big}>
              <Photo src={gallery[0]} alt="Foto galeri 1" />
              {demo && <span>Bali Swing · ★ 4.9</span>}
            </div>
            {gallery.length > 1 && (
              <div className={s.grid}>
                {gallery.slice(1).map((src, index) => <Photo key={src + index} src={src} alt={`Foto galeri ${index + 2}`} />)}
              </div>
            )}
          </section>
        )}

        {(demo || data.gifts.length > 0) && (
          <section className={s.card} aria-labelledby="rp-gift">
            <div className={s.head}><h2 id="rp-gift">Add-on Kado</h2>{demo && <span>Wishlist</span>}</div>
            {demo && DEMO_WISHLIST.map(item => (
              <div key={item.name} className={s.item}>
                <span className={s.itemIcon} aria-hidden><Lucide icon={item.icon} size={17} color="#0194f3" /></span>
                <div className={s.grow}>
                  <span className={s.itemHead}><strong>{item.name}</strong>{item.tag && <em>{item.tag}</em>}</span>
                  <small>{item.price}</small>
                </div>
                <span className={s.ghost} aria-hidden>Tambah</span>
              </div>
            ))}
            {data.gifts.map(gift => {
              const info = giftInfo(gift);
              return (
                <div key={gift.id} className={s.amplop}>
                  <Lucide icon={ic.wallet} size={17} color="#a9dcff" />
                  <div className={s.grow}>
                    <strong>{gift.type === "address" ? "Alamat Kirim Kado" : gift.type === "qris" ? "QRIS" : "Amplop Digital"}</strong>
                    <small>{[gift.type === "bank" || gift.type === "ewallet" ? `${info.title} ${info.number}` : info.number, info.holder ? `a.n. ${info.holder}` : ""].filter(Boolean).join(" · ")}</small>
                    {info.image && <Photo src={info.image} alt="Kode QRIS" className={s.qris} />}
                  </div>
                  {info.copy && <button type="button" className={s.salin} onClick={() => copy(info.copy)}>{copied === info.copy ? "Tersalin" : "Salin"}</button>}
                </div>
              );
            })}
          </section>
        )}

        <section className={s.card} aria-labelledby="rp-wishes">
          <div className={s.head}><h2 id="rp-wishes">Review Traveler</h2><span>{demo ? "★ 5.0 · 312" : wishes.wishes.length}</span></div>
          {wishes.wishes.length === 0 && <p className={s.empty}>Belum ada review. Jadilah traveler pertama yang menulis doa!</p>}
          {wishes.wishes.slice(0, 8).map(wish => (
            <article key={wish.id} className={s.review}>
              <span className={s.initial} aria-hidden>{wish.name.slice(0, 1).toUpperCase()}</span>
              <div className={s.grow}>
                <span className={s.itemHead}><strong>{wish.name}</strong>{demo && <i className={s.stars} aria-hidden>★★★★★</i>}</span>
                <p>{wish.message}</p>
              </div>
            </article>
          ))}
        </section>
      </main>

      <nav className={s.bottom} aria-label="Aksi undangan">
        <button type="button" className={s.chat} onClick={sheets.openWish} aria-label="Kirim ucapan"><Lucide icon={ic.messageCircle} size={18} color="#0194f3" /></button>
        <button type="button" className={s.orange} onClick={sheets.openRsvp}><Lucide icon={ic.check} color="#fff" />Pesan Kursi — Konfirmasi Hadir</button>
      </nav>

      <Sheet open={sheets.sheet === "rsvp"} onClose={sheets.close} title="Konfirmasi Kehadiran" tint={tint}>
        <RsvpForm rsvp={rsvp} guestName={data.guestName} demo={demo} labels={{ submit: "Pesan Kursi" }} />
      </Sheet>
      <Sheet open={sheets.sheet === "wish"} onClose={sheets.close} title="Tulis Review & Doa" tint={tint}>
        <WishForm wishes={wishes} guestName={data.guestName} demo={demo} />
      </Sheet>
    </ThemeShell>
  );
}

function SearchRow({ icon, kicker, title, note }: { icon: string; kicker: string; title: string; note: string }) {
  return (
    <div className={s.searchRow}>
      <span className={s.itemIcon} aria-hidden><Lucide icon={icon} size={17} color="#0194f3" /></span>
      <div className={s.grow}><small>{kicker}</small><strong>{title}</strong>{note && <span>{note}</span>}</div>
    </div>
  );
}
