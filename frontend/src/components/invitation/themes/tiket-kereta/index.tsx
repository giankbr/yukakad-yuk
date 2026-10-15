"use client";
// Theme "Tiket Kereta" — undangan bergaya e-tiket kereta (design: KA Argo Asmara, Wulan & Seno).
import {
  Extras, Lucide, Photo, RsvpForm, Sheet, ThemeShell, WishForm, coupleLabel, dateParts, formatDate, giftInfo, guestLabel,
  mapsHref, storyItems, toDate, useCopy, useRsvp, useSheets, useWishes, type ThemeProps, type ThemeTint,
} from "../kit";
import { ic } from "./icons";
import s from "./styles.module.css";

const FONTS = ["Archivo:wght@400;700;800", "JetBrains Mono:wght@700;800"];
const COVER_ART = "/themes/img/r39.webp";
const tint: ThemeTint = {
  "--t-accent": "#f26a21", "--t-accent-ink": "#ffffff", "--t-bg": "#f7f3ec", "--t-ink": "#2b2b33", "--t-muted": "#6e6e78", "--t-line": "#e3dacb",
  "--t-field": "#ffffff", "--t-radius": "10px", "--t-font": "'Archivo', system-ui, sans-serif",
};
const DEMO_WISHES = [
  { id: "w1", name: "Pak Darto", message: "Dari rebutan kursi sampai sehidup semati. Selamat berangkat!" },
  { id: "w2", name: "Mbak Ajeng", message: "Sampai jumpa di St. Selamanya! Kami satu gerbong." },
];
const DEMO_WISHLIST = [
  { name: "Sofa Dua Dudukan", price: "Rp2.700.000", icon: ic.sofa },
  { name: "Set Kopi Manual Brew", price: "Rp740.000", icon: ic.coffee },
  { name: "Koper Liburan", price: "Rp1.400.000", icon: ic.luggage },
];

function Status() {
  return (
    <div className={s.status} aria-hidden>
      <span>05:45</span>
      <span className={s.statusIcons}><Lucide icon={ic.signal} /><Lucide icon={ic.wifi} /><Lucide icon={ic.batteryFull} /></span>
    </div>
  );
}

/** "08.00" from an ISO date (Asia/Jakarta). */
function clock(value?: string, shiftMinutes = 0) {
  const date = toDate(value);
  if (!date) return "";
  return new Intl.DateTimeFormat("id-ID", { timeZone: "Asia/Jakarta", hour: "2-digit", minute: "2-digit" }).format(new Date(date.getTime() + shiftMinutes * 60000));
}

/** First time in a "08.00 – 10.00 WIB" string, else from the date. */
function startTime(event: ThemeProps["data"]["events"][number]) {
  const match = event.time?.match(/\d{1,2}[.:]\d{2}/);
  return match ? match[0].replace(":", ".").padStart(5, "0") : clock(event.date);
}

function city(address: string) {
  const parts = address.split(",").map(part => part.trim()).filter(Boolean);
  return parts[parts.length - 1] ?? "";
}

export default function TiketKeretaTheme({ data, slug, guestToken, demo, skipCover }: ThemeProps) {
  const couple = coupleLabel(data);
  const parts = dateParts(data.date);
  const date = toDate(data.date);
  const mm = date ? new Intl.DateTimeFormat("id-ID", { timeZone: "Asia/Jakarta", month: "2-digit" }).format(date) : "";
  const initials = `${data.couple.bride.slice(0, 1)}${data.couple.groom.slice(0, 1)}`.toUpperCase();
  const code = parts.day ? `${initials}-${parts.day.padStart(2, "0")}${mm}${parts.year.slice(-2)}-SAH` : `${initials}-SAH`;
  const shortDate = formatDate(data.date, { weekday: "long", day: "numeric", month: "short", year: "numeric" });
  const firstEvent = data.events[0];
  const depart = firstEvent ? startTime(firstEvent) : clock(data.date);
  const boarding = firstEvent?.date ? clock(firstEvent.date, -30) : clock(data.date, -30);
  const rsvp = useRsvp({ slug, guestToken, demo });
  const wishes = useWishes({ slug, guestToken, demo, seed: DEMO_WISHES });
  const sheets = useSheets();
  const { copy, copied } = useCopy();
  const stories = storyItems(data);
  const where = city(data.address) || data.place;
  const stations = [...stories.map(story => story.title.toUpperCase()), "ST. SELAMANYA"];
  const [bigPhoto, ...restPhotos] = data.gallery;
  const people = [
    { name: data.couple.brideFull ?? data.couple.bride, parents: data.couple.brideParents, photo: data.couple.bridePhoto ?? data.gallery[0] },
    { name: data.couple.groomFull ?? data.couple.groom, parents: data.couple.groomParents, photo: data.couple.groomPhoto ?? data.gallery[1] },
  ];

  return (
    <ThemeShell
      fonts={FONTS}
      background="#20306b"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.coverBg} aria-hidden><Photo src={COVER_ART} /></div>
          <Status />
          <div className={s.coverHead}>
            <span>E-TIKET {(data.eventLabel ?? "Pernikahan").toUpperCase()}</span>
            <strong>KA ARGO ASMARA</strong>
          </div>

          <article className={s.ticket} aria-label="E-tiket undangan">
            <div className={s.ticketHead}>
              <span>ARGO ASMARA{parts.day ? ` (${parts.day})` : ""} · EKSEKUTIF CINTA</span>
              <Lucide icon={ic.trainFront} color="#fff" />
            </div>
            <div className={s.route}>
              <div className={s.station}>
                <b>LJG</b><small>St. Lajang</small><span className={s.mono}>{depart}</span>
              </div>
              <div className={s.routeMid} aria-hidden>
                <span className={s.track}><i /><i /></span><small>{demo ? "6 jam 12 mnt" : "tanpa transit"}</small>
              </div>
              <div className={`${s.station} ${s.stationEnd}`}>
                <b>SLM</b><small>St. Selamanya</small><span className={s.mono}>{shortDate}</span>
              </div>
            </div>
            <dl className={s.ticketInfo}>
              <div><dt>PENUMPANG</dt><dd>{couple}</dd></div>
              <div><dt>GERBONG</dt><dd>CINTA 1</dd></div>
              <div><dt>KURSI</dt><dd>1A &amp; 1B</dd></div>
              <div><dt>KELAS</dt><dd>Eksekutif</dd></div>
            </dl>
            <div className={s.perforation} aria-hidden />
            <div className={s.kepada}>
              <span>PENUMPANG KEHORMATAN</span>
              <h1>{guestLabel(data)}</h1>
              <small>Tunjukkan tiket ini di gerbang pelaminan</small>
            </div>
            <div className={s.qrRow}>
              <p className={s.mono}>Kode Pesanan<br />{code}</p>
              <span className={s.qr} aria-hidden><Lucide icon={ic.qrCode} size={44} color="#2b2b33" /></span>
            </div>
          </article>

          <dl className={s.peron}>
            <div><dt>PERON</dt><dd>1</dd></div>
            <div><dt>BOARDING</dt><dd>{boarding || "—"}</dd></div>
            <div><dt>GERBANG</dt><dd>CINTA</dd></div>
            <div><dt>STATUS</dt><dd className={s.onTime}>TEPAT WAKTU</dd></div>
          </dl>
          <div className={s.grow} style={{ flexBasis: 66 }} />
          <button type="button" className={s.openBtn} onClick={open}>
            <Lucide icon={ic.ticketCheck} size={17} color="#fff" />Boarding — Buka Undangan
          </button>
          <p className={s.coverNote}>Kereta menuju pelaminan berangkat tepat waktu. Jangan sampai ketinggalan!</p>
          <div className={s.grow} style={{ flexBasis: 80 }} />
          <div className={s.marquee} aria-hidden>
            <div className={s.marqueeTrack}>
              {[0, 1].map(copyIndex => (
                <span key={copyIndex} className={s.marqueeSet}>
                  {stations.map((station, index) => (
                    <span key={station + index} className={s.marqueeItem}>
                      <span className={index === stations.length - 1 ? s.marqueeNow : undefined}>{station}</span><i />
                    </span>
                  ))}
                </span>
              ))}
            </div>
          </div>
        </section>
      )}
    >
      <header className={s.top}>
        <Status />
        <div className={s.nav}>
          <h1>KA Argo Asmara · Info Perjalanan</h1>
          <p>St. Lajang → St. Selamanya{where ? ` · ${where}` : ""}</p>
        </div>
      </header>

      <main className={s.body}>
        <Extras slot="opening" className={s.extras} />

        <section className={s.section} aria-labelledby="tk-route">
          <h2 id="tk-route">Rute Perjalanan Cinta</h2>
          <ol className={s.timeline}>
            {stories.map((story, index) => (
              <li key={story.title + index} className={s.stop}>
                <span className={s.rail} aria-hidden><i className={s.dot} /><i className={s.line} /></span>
                <div className={s.stopText}>
                  <strong>{story.title}</strong>
                  <p>{[story.date, story.body].filter(Boolean).join(" · ")}</p>
                  {story.image && <Photo src={story.image} alt={story.title} className={s.stopImg} />}
                </div>
              </li>
            ))}
            <li className={`${s.stop} ${s.stopNow}`}>
              <span className={s.rail} aria-hidden><i className={s.dot} /></span>
              <div className={s.stopText}>
                <strong>St. Selamanya</strong>
                <p>{shortDate} · pemberhentian terakhir</p>
              </div>
            </li>
          </ol>
        </section>

        <section className={s.section} aria-labelledby="tk-couple">
          <h2 id="tk-couple">Masinis &amp; Asisten Perjalanan</h2>
          <div className={s.couple}>
            {people.map((person, index) => (
              <article key={index} className={s.person}>
                <Photo src={person.photo} alt={person.name} className={s.personImg} />
                <div>
                  <strong>{person.name}</strong>
                  {person.parents && <small>{person.parents}</small>}
                </div>
              </article>
            ))}
          </div>
        </section>

        {data.events.length > 0 && (
          <section className={s.section} aria-labelledby="tk-events">
            <h2 id="tk-events">Jadwal Pemberhentian</h2>
            {data.events.map((event, index) => {
              const href = mapsHref(data, event);
              const place = [event.venue, event.address].filter(Boolean).join(", ");
              return (
                <article key={event.name + index} className={`${s.card} ${s.event}`}>
                  <span className={`${s.mono} ${s.eventTime}`}>{startTime(event) || "—"}</span>
                  <div className={s.grow1}>
                    <strong>{event.name.toUpperCase()}</strong>
                    <small>{[formatDate(event.date, { weekday: "long", day: "numeric", month: "short", year: "numeric" }), place].filter(Boolean).join(" · ")}</small>
                  </div>
                  {href && <a className={s.mapBtn} href={href} target="_blank" rel="noreferrer" aria-label={`Peta ${event.name}`}>Peta</a>}
                </article>
              );
            })}
          </section>
        )}

        <Extras slot="event" className={s.extras} />

        {data.gallery.length > 0 && (
          <section className={s.section} aria-labelledby="tk-gallery">
            <h2 id="tk-gallery">Pemandangan dari Jendela</h2>
            <div className={s.big}>
              <Photo src={bigPhoto} alt={`Foto ${couple} 1`} />
              {demo && <span>KM 2019 — perjalanan pertama</span>}
            </div>
            {restPhotos.length > 0 && (
              <div className={s.grid}>
                {restPhotos.map((src, index) => <Photo key={src + index} src={src} alt={`Foto ${couple} ${index + 2}`} />)}
              </div>
            )}
          </section>
        )}

        <Extras slot="story" className={s.extras} />
        <Extras slot="end" className={s.extras} />

        {(demo || data.gifts.length > 0) && (
          <section className={s.section} aria-labelledby="tk-gift">
            <h2 id="tk-gift">Bagasi Kado</h2>
            {demo && DEMO_WISHLIST.map(item => (
              <div key={item.name} className={`${s.card} ${s.gift}`}>
                <span className={s.giftIcon}><Lucide icon={item.icon} size={17} color="#f26a21" /></span>
                <div className={s.grow1}><b>{item.name}</b><small>{item.price}</small></div>
                <button type="button" className={s.navyBtn} onClick={sheets.openWish}>Beri</button>
              </div>
            ))}
            {data.gifts.map(gift => {
              const info = giftInfo(gift);
              const line = [info.title !== "Alamat kado" ? `${info.title} ${info.number}`.trim() : info.number, info.holder ? `a.n. ${info.holder}` : ""].filter(Boolean).join(" · ");
              return (
                <div key={gift.id} className={s.amplop}>
                  <Lucide icon={ic.wallet} size={17} color="#ffd9a8" />
                  <div className={s.grow1}>
                    <strong>{gift.type === "address" ? "Kirim Kado" : "Amplop Digital"}</strong>
                    <small>{line}</small>
                    {info.image && <Photo src={info.image} alt="Kode QRIS" className={s.qris} />}
                  </div>
                  {info.copy && <button type="button" className={s.orangeBtn} onClick={() => copy(info.copy)}>{copied === info.copy ? "Tersalin" : "Salin"}</button>}
                </div>
              );
            })}
          </section>
        )}

        <section className={s.section} aria-labelledby="tk-wishes">
          <h2 id="tk-wishes">Buku Tamu Peron</h2>
          {wishes.wishes.length === 0 && <p className={s.empty}>Belum ada pesan di buku tamu. Jadilah penumpang pertama yang menulis!</p>}
          {wishes.wishes.slice(0, 8).map(wish => (
            <article key={wish.id} className={`${s.card} ${s.wish}`}>
              <strong>{wish.name}</strong>
              <p>{wish.message}</p>
            </article>
          ))}
        </section>
      </main>

      <nav className={s.bottom} aria-label="Aksi undangan">
        <button type="button" className={s.chatBtn} onClick={sheets.openWish} aria-label="Tulis di buku tamu"><Lucide icon={ic.messageCircle} size={18} color="#20306b" /></button>
        <button type="button" className={s.rsvpBtn} onClick={sheets.openRsvp}><Lucide icon={ic.ticketCheck} color="#fff" />Konfirmasi Naik — Hadir</button>
      </nav>

      <Sheet open={sheets.sheet === "rsvp"} onClose={sheets.close} title="Konfirmasi Naik" tint={tint}>
        <RsvpForm rsvp={rsvp} guestName={data.guestName} demo={demo} labels={{ submit: "Konfirmasi Tiket" }} />
      </Sheet>
      <Sheet open={sheets.sheet === "wish"} onClose={sheets.close} title="Buku Tamu Peron" tint={tint}>
        <WishForm wishes={wishes} guestName={data.guestName} demo={demo} />
      </Sheet>
    </ThemeShell>
  );
}
