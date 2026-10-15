"use client";
// Theme "Feed Foto" — undangan bergaya feed & profil aplikasi foto (design: Undangan — Tema Feed Foto (Alika & Rio)).
import {
  Extras, Lucide, Photo, RsvpForm, Sheet, ThemeShell, WishForm, coupleLabel, formatDate, giftInfo, guestLabel,
  mapsHref, storyItems, toDate, useCopy, useCountdown, useRsvp, useSheets, useWishes, type ThemeProps, type ThemeTint,
} from "../kit";
import { ic } from "./icons";
import s from "./styles.module.css";

const FONTS = ["Inter:wght@400;500;600;700;800"];
const tint: ThemeTint = {
  "--t-accent": "#0095f6", "--t-bg": "#ffffff", "--t-ink": "#262626", "--t-muted": "#8e8e8e", "--t-line": "#dbdbdb",
  "--t-field": "#fafafa", "--t-radius": "8px", "--t-font": "Inter, system-ui, sans-serif",
};
const DEMO_WISHES = [
  { id: "w1", name: "sahabat.alika", message: "Akhirnya hard launch terakhir!! See you di Bali", created_at: new Date(Date.now() - 2 * 3600e3).toISOString() },
  { id: "w2", name: "om_wayan", message: "Rahajeng! Pasti hadir sekeluarga.", created_at: new Date(Date.now() - 5 * 3600e3).toISOString() },
];
const WISHLIST = [
  { name: "Lampu Vintage", price: "Rp520.000", icon: ic.lampDesk },
  { name: "Vas Keramik", price: "Rp340.000", icon: ic.flower2 },
  { name: "Kursi Rotan", price: "Rp1.150.000", icon: ic.armchair },
];

function Status({ time }: { time: string }) {
  return (
    <div className={s.status} aria-hidden>
      <span>{time}</span>
      <span className={s.statusIcons}><Lucide icon={ic.signal} /><Lucide icon={ic.wifi} /><Lucide icon={ic.batteryFull} /></span>
    </div>
  );
}

function handle(data: ThemeProps["data"]) {
  const slug = `${data.couple.bride}${data.couple.groom}`.toLowerCase().normalize("NFD").replace(/[^a-z0-9]/g, "");
  return `${slug || "kami"}.wedding`;
}

function location(address: string, place: string) {
  const parts = address.split(",").map(p => p.trim()).filter(Boolean);
  return parts.slice(-2).join(", ") || place;
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

export default function FeedFotoTheme({ data, slug, guestToken, demo, skipCover }: ThemeProps) {
  const user = handle(data);
  const where = location(data.address, data.place);
  const longDate = formatDate(data.date);
  const clock = toDate(data.date) ? `${formatDate(data.date, { day: "2-digit" })}:${formatDate(data.date, { month: "2-digit" })}` : "07:03";
  const countdown = useCountdown(data.date);
  const rsvp = useRsvp({ slug, guestToken, demo });
  const wishes = useWishes({ slug, guestToken, demo, seed: DEMO_WISHES });
  const sheets = useSheets();
  const { copy, copied } = useCopy();
  const stories = storyItems(data);
  const hero = data.gallery[0];
  const avatar = data.gallery[1] ?? hero;
  const ringAvatar = data.gallery[2] ?? avatar;
  const rest = data.gallery.slice(3);
  const grid = rest.length >= 3 ? rest : data.gallery;
  const years = [...stories.map(st => st.date?.match(/\d{4}/)?.[0]).filter(Boolean), formatDate(data.date, { year: "numeric" })].filter(Boolean) as string[];
  const span = years.length > 1 ? `Sorotan dari ${years[0]} → ${years[years.length - 1]}` : "Sorotan perjalanan kami";
  const parents = [data.couple.brideParents, data.couple.groomParents].filter(Boolean);
  const calendar = calendarHref(data);
  const mainMaps = mapsHref(data, data.events[data.events.length - 1]);
  const commentCount = demo ? "1.024" : nf.format(wishes.wishes.length);

  return (
    <ThemeShell
      fonts={FONTS}
      background="#fafafa"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Status time={clock} />
          <div className={s.coverNav}>
            <span className={s.logo}>Undangan</span>
            <span className={s.navIcons} aria-hidden><Lucide icon={ic.heart} size={22} /><Lucide icon={ic.messageCircle} size={22} /></span>
          </div>
          <div className={s.postHead}>
            <span className={s.ring}><Photo src={ringAvatar} className={s.ringImg} /></span>
            <div className={s.postUser}>
              <span className={s.userRow}><strong>{user}</strong><Lucide icon={ic.badgeCheck} size={13} color="#0095f6" /></span>
              <small>{where}</small>
            </div>
            <Lucide icon={ic.ellipsis} size={18} />
          </div>
          <Photo src={hero} alt={`Foto ${coupleLabel(data)}`} className={s.postPhoto} />
          <div className={s.actions} aria-hidden>
            <span><Lucide icon={ic.heart} size={24} color="#ff3040" /><Lucide icon={ic.messageCircle} size={24} /><Lucide icon={ic.send} size={24} /></span>
            <Lucide icon={ic.bookmark} size={24} />
          </div>
          <div className={s.caption}>
            <strong>{demo ? "Disukai oleh keluargabesar dan 2.700 lainnya" : "Disukai oleh keluarga besar & sahabat"}</strong>
            <p><b>{user}</b>{"  "}Kami {data.eventLabel === "Menikah" || !data.eventLabel ? "menikah" : `mengundangmu ke ${data.eventLabel.toLowerCase()} kami`}! {longDate}{where ? ` · ${where}` : ""}. Geser untuk detail acara.</p>
            <div className={s.kepada}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
            </div>
            <button type="button" className={s.openBtn} onClick={open}>Buka Undangan</button>
            <small className={s.muted12}>{demo ? "Lihat semua 1.024 komentar" : "Lihat semua komentar"}</small>
          </div>
        </section>
      )}
    >
      <Status time={clock} />
      <header className={s.nav}>
        <span className={s.userRow}><strong className={s.navUser}>{user}</strong><Lucide icon={ic.badgeCheck} size={15} color="#0095f6" /></span>
        <span className={s.navIcons} aria-hidden><Lucide icon={ic.squarePlus} size={22} /><Lucide icon={ic.menu} size={22} /></span>
      </header>

      <section className={s.profile} aria-label="Profil">
        <Photo src={avatar} alt={`Foto ${coupleLabel(data)}`} className={s.avatar} />
        <div className={s.stats}>
          {demo
            ? <div><b>2.190</b><small>Hari bersama</small></div>
            : <div><b>{nf.format(wishes.wishes.length)}</b><small>Ucapan</small></div>}
          <div><b>{countdown.ready ? Number(countdown.days) : "–"}</b><small>Hari lagi</small></div>
          <div><b>∞</b><small>Selamanya</small></div>
        </div>
      </section>

      <section className={s.bio}>
        <h1>{coupleLabel(data)}</h1>
        <p>
          {[data.eventLabel ?? "Pernikahan", longDate, where].filter(Boolean).join(" · ")}
          {parents.length > 0 && <><br />{parents.join("  ×   ")}</>}
        </p>
      </section>

      <div className={s.btns}>
        <button type="button" className={s.btnBlue} onClick={sheets.openRsvp}>Ikuti</button>
        <button type="button" className={s.btnGray} onClick={sheets.openWish}>Kirim Pesan</button>
        {calendar
          ? <a className={s.btnGray} href={calendar} target="_blank" rel="noreferrer">Simpan Tanggal</a>
          : <button type="button" className={s.btnGray} onClick={sheets.openRsvp}>Simpan Tanggal</button>}
      </div>

      <nav className={s.highlights} aria-label="Sorotan">
        {stories.length > 0 && <a href="#ff-kisah"><span><Lucide icon={ic.heartHandshake} size={22} /></span>Kisah</a>}
        {data.events.map((event, index) => (
          <a key={event.name + index} href={`#ff-event-${index}`}>
            <span><Lucide icon={index === 0 ? ic.calendar : ic.partyPopper} size={22} /></span>{event.name.replace(/ Nikah$/, "")}
          </a>
        ))}
        {data.gifts.length > 0 && <a href="#ff-kado"><span><Lucide icon={ic.gift} size={22} /></span>Kado</a>}
        {mainMaps && <a href={mainMaps} target="_blank" rel="noreferrer"><span><Lucide icon={ic.mapPin} size={22} /></span>Lokasi</a>}
      </nav>

      <main className={s.body}>
        <Extras slot="opening" className={s.extras} />

        {stories.length > 0 && (
          <section id="ff-kisah" className={s.section} aria-labelledby="ff-kisah-h">
            <h2 id="ff-kisah-h">Kisah Kami</h2>
            <p className={s.sub}>{span}</p>
            {stories.map((story, index) => (
              <div key={story.title + index} className={s.story}>
                <span className={s.yearRing}><span>{story.date?.match(/\d{4}/)?.[0] ?? story.date ?? index + 1}</span></span>
                <p>{story.body}</p>
              </div>
            ))}
          </section>
        )}

        <section className={s.section} aria-labelledby="ff-acara">
          <h2 id="ff-acara">Acara</h2>
          <p className={s.sub}>Tandai kalendermu</p>
          {data.events.map((event, index) => {
            const href = mapsHref(data, event);
            const month = formatDate(event.date || data.date, { month: "short" }).replace(".", "").toUpperCase();
            const day = formatDate(event.date || data.date, { day: "2-digit" });
            return (
              <article id={`ff-event-${index}`} key={event.name + index} className={s.event}>
                <span className={s.cal} aria-hidden><small>{month}</small><b>{day}</b></span>
                <div className={s.eventText}>
                  <strong>{event.name}{event.time ? ` · ${event.time}` : ""}</strong>
                  <small>{[event.venue, event.address].filter(Boolean).join(", ")}</small>
                </div>
                {href && <a className={s.chip} href={href} target="_blank" rel="noreferrer" aria-label={`Peta ${event.name}`}>Peta</a>}
              </article>
            );
          })}
        </section>

        <Extras slot="event" without={["calendar"]} className={s.extras} />

        {grid.length > 0 && (
          <section className={s.gallery} aria-label="Galeri foto">
            <div className={s.tabs} aria-hidden>
              <span className={s.tabOn}><Lucide icon={ic.grid3x3} size={20} /></span>
              <span><Lucide icon={ic.clapperboard} size={20} color="#8e8e8e" /></span>
              <span><Lucide icon={ic.userRound} size={20} color="#8e8e8e" /></span>
            </div>
            <div className={s.grid}>
              {grid.map((src, index) => <Photo key={src + index} src={src} alt={`Foto ${index + 1}`} className={s.cell} />)}
            </div>
          </section>
        )}

        <Extras slot="story" className={s.extras} />
        <Extras slot="end" className={s.extras} />

        {(demo || data.gifts.length > 0) && (
          <section id="ff-kado" className={s.section} aria-labelledby="ff-kado-h">
            <h2 id="ff-kado-h">{demo ? "Wishlist Kado" : "Kado"}</h2>
            <p className={s.sub}>{demo ? "Tap untuk mengirim hadiah" : "Doa restu adalah hadiah terbaik"}</p>
            {demo && (
              <div className={s.wishlist}>
                {WISHLIST.map(item => (
                  <div key={item.name} className={s.product}>
                    <span className={s.productImg}><Lucide icon={item.icon} size={24} /></span>
                    <strong>{item.name}</strong>
                    <small>{item.price}</small>
                    <span className={s.beri}>Beri</span>
                  </div>
                ))}
              </div>
            )}
            {data.gifts.map(gift => {
              const info = giftInfo(gift);
              return (
                <div key={gift.id} className={s.amplop}>
                  <Lucide icon={ic.wallet} size={18} color="#fff" />
                  <div>
                    <strong>{gift.type === "address" ? "Kirim Kado" : "Amplop Digital"}</strong>
                    <small>{(gift.type === "address" ? [info.number] : [`${info.title} ${info.number}`.trim(), info.holder ? `a.n. ${info.holder}` : ""]).filter(Boolean).join(" · ")}</small>
                  </div>
                  {info.copy && <button type="button" className={s.copy} onClick={() => copy(info.copy)}>{copied === info.copy ? "Tersalin" : "Salin"}</button>}
                  {info.image && <a className={s.copy} href={info.image} target="_blank" rel="noreferrer">Lihat QR</a>}
                </div>
              );
            })}
          </section>
        )}

        <section className={s.section} aria-labelledby="ff-komentar">
          <h2 id="ff-komentar">Komentar</h2>
          <p className={s.sub}>{commentCount} komentar</p>
          {wishes.wishes.length === 0 && <p className={s.empty}>Belum ada komentar. Jadilah yang pertama!</p>}
          {wishes.wishes.slice(0, 8).map(wish => (
            <article key={wish.id} className={s.comment}>
              <span className={s.cAv} aria-hidden>{wish.name.slice(0, 1).toUpperCase()}</span>
              <div>
                <p><b>{wish.name}</b>{"  "}{wish.message}</p>
                <small>Balas · Suka</small>
              </div>
              <Lucide icon={ic.heart} size={13} color="#8e8e8e" />
            </article>
          ))}
          <button type="button" className={s.addComment} onClick={sheets.openWish}>Tambahkan komentar…</button>
        </section>
      </main>

      <nav className={s.bottom} aria-label="Aksi undangan">
        <button type="button" className={s.dm} onClick={sheets.openWish} aria-label="Kirim ucapan"><Lucide icon={ic.send} size={18} /></button>
        <button type="button" className={s.rsvpBtn} onClick={sheets.openRsvp}>Konfirmasi Hadir</button>
      </nav>

      <Sheet open={sheets.sheet === "rsvp"} onClose={sheets.close} title="Konfirmasi Kehadiran" tint={tint}>
        <RsvpForm rsvp={rsvp} guestName={data.guestName} demo={demo} />
      </Sheet>
      <Sheet open={sheets.sheet === "wish"} onClose={sheets.close} title="Tulis Komentar & Doa" tint={tint}>
        <WishForm wishes={wishes} guestName={data.guestName} demo={demo} submitLabel="Kirim Komentar" />
      </Sheet>
    </ThemeShell>
  );
}
