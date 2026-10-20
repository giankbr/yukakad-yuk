"use client";
// Theme "Boarding Pass" — undangan bergaya tiket pesawat (design: Undangan — Tema Boarding Pass (Citra & Bagus)).
import {
  Extras, Lucide, Photo, RsvpForm, Sheet, ThemeShell, WishForm, coupleLabel, dateParts, formatDate, giftInfo, guestLabel,
  mapsHref, storyItems, Tick, timeAgo, useCopy, useCountdown, useRsvp, useSheets, useWishes, type ThemeProps, type ThemeTint,
} from "../kit";
import { useState } from "react";
import { toast } from "@/lib/celebrate";
import { ic } from "./icons";
import s from "./styles.module.css";

const FONTS = ["Barlow:wght@400;500;600;700;800"];
const tint: ThemeTint = {
  "--t-accent": "#f4a000", "--t-accent-ink": "#ffffff", "--t-bg": "#ffffff", "--t-ink": "#13293d", "--t-muted": "#5e748a",
  "--t-line": "#dae3ee", "--t-field": "#f4f7fb", "--t-radius": "10px", "--t-font": "Barlow, system-ui, sans-serif",
};
const ART = "/themes/art/boarding-pass";

/** Decorative painted image (never opens the photo lightbox). */
function Art({ src, className, w, h, eager }: { src: string; className?: string; w: number; h: number; eager?: boolean }) {
  return (
    // eslint-disable-next-line @next/next/no-img-element -- static painted ornament
    <img src={`${ART}/${src}.webp`} alt="" aria-hidden width={w} height={h} className={className} data-nolightbox
      loading={eager ? "eager" : "lazy"} fetchPriority={eager ? "high" : undefined} decoding="async" draggable={false} />
  );
}

const BARCODE = [2, 1, 3, 1, 1, 2, 3, 1, 2, 1, 1, 3, 2, 1, 2, 2, 1, 3, 1, 1, 2, 1, 3, 2, 1, 1, 2, 3, 1, 2, 1, 2, 1, 1, 3, 2, 1, 2, 1, 3];
const DEMO_WISHES = [
  { id: "w1", name: "Pak Surya", message: "Penerbangan paling dinanti tahun ini. Kru-nya serasi. ★★★★★", created_at: new Date(Date.now() - 3 * 3600e3).toISOString() },
  { id: "w2", name: "Mbak Gita", message: "Check-in dari 2021, akhirnya mendarat juga. Selamat!", created_at: new Date(Date.now() - 7 * 3600e3).toISOString() },
];
// Venue facilities, seat zone and the gift wishlist (with prices) are invented sample content: demo only.
const DEMO_FACILITIES = [[ic.utensils, "Makan enak"], [ic.music, "Live music"], [ic.camera, "Photo booth"], [ic.handHeart, "Doa unlimited"]];
const DEMO_BAGGAGE = [
  { name: "Koper Kabin Premium", price: "Rp1.900.000", icon: ic.luggage },
  { name: "Tiket Bulan Madu", price: "Bebas nominal", icon: ic.plane },
  { name: "Sprei Hotel 5★", price: "Rp860.000", icon: ic.bedDouble },
];

function lastPart(address: string) {
  const parts = address.split(",").map(part => part.trim()).filter(Boolean);
  return parts[parts.length - 1] ?? "";
}

export default function BoardingPassTheme({ data, slug, guestToken, demo, skipCover }: ThemeProps) {
  const couple = coupleLabel(data);
  const parts = dateParts(data.date);
  const flight = `${data.couple.bride.slice(0, 1)}${data.couple.groom.slice(0, 1)}`.toUpperCase() + (parts.year ? `-${parts.year}` : "");
  const stories = storyItems(data);
  const firstYear = stories.map(story => ("date" in story ? story.date : undefined)).find(value => value && /\d{4}/.test(value))?.match(/\d{4}/)?.[0];
  const years = firstYear && parts.year ? Number(parts.year) - Number(firstYear) : 0;
  const shortDate = formatDate(data.date, { day: "numeric", month: "short", year: "numeric" });
  const longShort = formatDate(data.date, { weekday: "long", day: "numeric", month: "short", year: "numeric" });
  const ticketDate = parts.day ? `${parts.day} ${parts.monthShort} ${parts.year}` : "Menyusul";
  const city = lastPart(data.address) || data.place;
  const countdown = useCountdown(data.date);
  const rsvp = useRsvp({ slug, guestToken, demo });
  const wishes = useWishes({ slug, guestToken, demo, seed: DEMO_WISHES });
  const sheets = useSheets();
  const { copy, copied } = useCopy();
  const gallery = data.gallery.length > 3 ? data.gallery.slice(1) : data.gallery;
  const firstEvent = data.events[0]?.name?.toLowerCase();
  const statusLine = countdown.done ? "STATUS: SUDAH MENDARAT" : <>STATUS: ON TIME · {countdown.ready ? <Tick value={Number(countdown.days)} /> : "–"} HARI MENUJU BOARDING</>;
  const [picked, setPicked] = useState<string[]>([]);
  const togglePick = (name: string) => {
    const on = !picked.includes(name);
    setPicked(list => on ? [...list, name] : list.filter(item => item !== name));
    toast(on ? "Masuk bagasi kado" : "Dikeluarkan dari bagasi");
  };
  const crew = [
    { role: "KAPTEN RUMAH TANGGA", name: data.couple.brideFull ?? data.couple.bride, parents: data.couple.brideParents, photo: data.couple.bridePhoto ?? data.gallery[1] },
    { role: "CO-PILOT SETIA", name: data.couple.groomFull ?? data.couple.groom, parents: data.couple.groomParents, photo: data.couple.groomPhoto ?? data.gallery[2] },
  ];

  return (
    <ThemeShell
      fonts={FONTS}
      background="#0b2545"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.sky} aria-hidden><Art src="sky" w={780} h={1200} eager /><span className={s.plane} /></div>
          <span className={s.clouds} aria-hidden />
          <header className={s.coverHead}>
            <span>RAWUH AIR</span>
            <h1>Boarding Pass {data.eventLabel ?? "Pernikahan"}</h1>
          </header>
          <article className={s.ticket} aria-label="Boarding pass">
            <div className={s.ticketHead}>
              <span><Lucide icon={ic.plane} color="#0b2545" />{flight} · Penerbangan Cinta</span>
              <b>FIRST LOVE CLASS</b>
            </div>
            <div className={s.route}>
              <div><strong>SGL</strong><span>Lajang</span>{firstYear && <small>Boarding {firstYear}</small>}</div>
              <div className={s.routeMid}><span className={s.flightPath} aria-hidden><i /><Lucide icon={ic.plane} size={20} color="#f4a000" className={s.flyer} /></span>{years > 0 && <small>{years} thn</small>}</div>
              <div className={s.routeEnd}><strong>SLM</strong><span>Selamanya</span><small>Mendarat {shortDate}</small></div>
            </div>
            <dl className={s.info}>
              <div><dt>PENUMPANG</dt><dd>{couple}</dd></div>
              <div><dt>TANGGAL</dt><dd>{ticketDate}</dd></div>
              <div><dt>GERBANG</dt><dd>CINTA 1</dd></div>
              <div><dt>KURSI</dt><dd>Bersebelahan</dd></div>
            </dl>
            <div className={s.dash} aria-hidden />
            <div className={s.guest}>
              <small>TAMU KEHORMATAN</small>
              <strong>{guestLabel(data)}</strong>
              <span>{demo ? "Kursi VIP · Zona Keluarga" : "Kepada Yth. Bapak/Ibu/Saudara/i"}</span>
            </div>
            <div className={s.barcode} aria-hidden>{BARCODE.map((w, i) => <i key={i} style={{ width: w }} />)}<span className={s.scan} /></div>
            <Art src="stamp" className={s.stamp} w={260} h={259} eager />
          </article>
          <div className={s.coverSpacer} />
          <button type="button" className={s.checkIn} onClick={open}><Lucide icon={ic.scanLine} size={17} color="#fff" />Check-in — Buka Undangan</button>
          <div className={s.note}>
            <p>Gerbang ditutup saat {firstEvent ?? "acara"} dimulai. Mohon hadir 30 menit lebih awal.</p>
            <span className={s.onTime}><i aria-hidden className={s.dot} /><span>{statusLine}</span></span>
          </div>
          {demo && (
            <div className={s.facilities} aria-label="Fasilitas penerbangan">
              <small>FASILITAS PENERBANGAN</small>
              <div>{DEMO_FACILITIES.map(([icon, label]) => <span key={label}><Lucide icon={icon} size={18} color="#f4a000" />{label}</span>)}</div>
            </div>
          )}
        </section>
      )}
    >
      <header className={s.top}>
        <div className={s.topText}>
          <h1>Penerbangan {flight}</h1>
          <p>Lajang (SGL) → Selamanya (SLM){city ? ` · ${city}` : ""}</p>
        </div>
      </header>

      <main className={s.body}>
        <Extras slot="opening" className={s.extras} />

        <section className={s.section} aria-labelledby="bp-status">
          <h2 id="bp-status">Status Penerbangan</h2>
          <ol className={s.timeline}>
            {stories.map((story, index) => (
              <li key={story.title + index}>
                <span className={s.rail} aria-hidden><i className={s.done}><Lucide icon={ic.check} size={12} color="#1f7a4d" strokeWidth={2.5} /></i><b /></span>
                <div>
                  <strong>{story.title}</strong>
                  <p>{["date" in story ? story.date : undefined, story.body].filter(Boolean).join(" · ")}</p>
                </div>
              </li>
            ))}
            <li className={s.now}>
              <span className={s.rail} aria-hidden><i className={s.landing}><span className={s.ping} /><Lucide icon={ic.plane} size={12} color="#fff" /></i></span>
              <div>
                <strong>Mendarat — Pelaminan</strong>
                <p>{longShort} · final approach</p>
              </div>
            </li>
          </ol>
        </section>

        <section className={s.section} aria-labelledby="bp-crew">
          <h2 id="bp-crew">Awak Kabin</h2>
          <div className={s.crew}>
            {crew.map(person => (
              <article key={person.role} className={s.crewCard}>
                <Photo src={person.photo} alt={person.name} className={s.crewImg} />
                <div>
                  <small>{person.role}</small>
                  <strong>{person.name}</strong>
                  {person.parents && <p>{person.parents}</p>}
                </div>
              </article>
            ))}
          </div>
        </section>

        <Art src="divider" className={s.divider} w={360} h={30} />

        <section className={s.section} aria-labelledby="bp-events">
          <h2 id="bp-events">Jadwal Keberangkatan</h2>
          {data.events.map((event, index) => {
            const href = mapsHref(data, event);
            return (
              <article key={event.name + index} className={s.flight}>
                <span className={s.gate}><small>GATE</small><b>C-{index + 1}</b></span>
                <div>
                  <strong>{event.name.toUpperCase()}</strong>
                  <em>{formatDate(event.date || data.date, { weekday: "long", day: "numeric", month: "short", year: "numeric" })}{event.time ? ` · ${event.time}` : ""}</em>
                  <span>{[event.venue, event.address].filter(Boolean).join(", ")}</span>
                </div>
                {href && <a className={s.mapBtn} href={href} target="_blank" rel="noreferrer" aria-label={`Peta ${event.venue}`}>Peta</a>}
              </article>
            );
          })}
        </section>

        <Extras slot="event" className={s.extras} />

        {gallery.length > 0 && (
          <section className={s.section} aria-labelledby="bp-gallery">
            <h2 id="bp-gallery">Jendela Kabin · Galeri</h2>
            <div className={s.windows}>
              {gallery.map((src, index) => (
                <div key={src + index} className={s.window}>
                  <Photo src={src} alt={`Foto ${couple} ${index + 1}`} />
                </div>
              ))}
            </div>
          </section>
        )}

        <Extras slot="story" className={s.extras} />
        <Extras slot="end" className={s.extras} />

        {(demo || data.gifts.length > 0) && (
          <section className={`${s.section} ${s.giftSection}`} aria-labelledby="bp-gift">
            <h2 id="bp-gift">Bagasi Kado</h2>
            <Art src="luggage" className={s.luggage} w={220} h={185} />
            {demo && DEMO_BAGGAGE.map(item => (
              <div key={item.name} className={`${s.bag} ${picked.includes(item.name) ? s.bagOn : ""}`}>
                <span className={s.bagIcon}><Lucide icon={item.icon} size={17} color="#0b2545" /></span>
                <div><strong>{item.name}</strong><small>{item.price}</small></div>
                <button type="button" className={`${s.amberBtn} ${picked.includes(item.name) ? s.picked : ""}`} aria-pressed={picked.includes(item.name)} onClick={() => togglePick(item.name)}>
                  {picked.includes(item.name) ? <><Lucide icon={ic.check} size={12} color="#1f7a4d" strokeWidth={3} />Dipilih</> : "Beri"}
                </button>
              </div>
            ))}
            {data.gifts.map(gift => {
              const info = giftInfo(gift);
              const line = gift.type === "address" ? info.number : [[info.title, info.number].filter(Boolean).join(" "), info.holder ? `a.n. ${info.holder}` : ""].filter(Boolean).join(" · ");
              return (
                <div key={gift.id} className={s.amplop}>
                  <Lucide icon={ic.wallet} size={17} color="#fff" />
                  <div>
                    <strong>{gift.type === "address" ? "Kirim Kado" : "Amplop Digital"}</strong>
                    {line && <small>{line}</small>}
                    {"image" in info && info.image && <Photo src={info.image} alt="Kode QRIS" className={s.qris} />}
                  </div>
                  {info.copy && <button type="button" className={`${s.amberBtn} ${copied === info.copy ? s.picked : ""}`} onClick={() => copy(info.copy)}>{copied === info.copy ? "Tersalin" : "Salin"}</button>}
                </div>
              );
            })}
          </section>
        )}

        <Art src="divider" className={s.divider} w={360} h={30} />

        <section className={s.section} aria-labelledby="bp-wishes">
          <h2 id="bp-wishes">Ulasan Penumpang</h2>
          {wishes.wishes.length === 0 && <p className={s.empty}>Belum ada ulasan. Jadilah penumpang pertama yang mengirim doa!</p>}
          {wishes.wishes.slice(0, 8).map(wish => (
            <article key={wish.id} className={s.review}>
              <strong>{wish.name}{!demo && wish.created_at && <small> · {timeAgo(wish.created_at)}</small>}</strong>
              <p>{wish.message}</p>
            </article>
          ))}
        </section>
      </main>

      <nav className={s.bottom} aria-label="Aksi undangan">
        <button type="button" className={s.chatBtn} onClick={sheets.openWish} aria-label="Kirim ucapan"><Lucide icon={ic.messageCircle} size={18} color="#0b2545" /></button>
        <button type="button" className={s.rsvpBtn} onClick={sheets.openRsvp}><Lucide icon={ic.plane} color="#fff" />Konfirmasi Boarding</button>
      </nav>

      <Sheet open={sheets.sheet === "rsvp"} onClose={sheets.close} title="Konfirmasi Boarding" tint={tint}>
        <RsvpForm rsvp={rsvp} guestName={data.guestName} demo={demo} labels={{ submit: "Check-in Sekarang" }} />
      </Sheet>
      <Sheet open={sheets.sheet === "wish"} onClose={sheets.close} title="Tulis Ulasan Penumpang" tint={tint}>
        <WishForm wishes={wishes} guestName={data.guestName} demo={demo} />
      </Sheet>
    </ThemeShell>
  );
}
