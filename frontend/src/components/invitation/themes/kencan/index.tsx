"use client";
// Theme "Kencan" — undangan bergaya aplikasi kencan "It's a Match!" (design: Undangan — Tema Kencan (Maya & Kevin)).
import {
  Lucide, Photo, RsvpForm, Sheet, ThemeShell, WishForm, coupleLabel, formatDate, giftInfo, guestLabel,
  mapsHref, storyItems, toDate, useCopy, useRsvp, useSheets, useWishes, type ThemeProps, type ThemeTint,
} from "../kit";
import { ic } from "./icons";
import s from "./styles.module.css";

const FONTS = ["Poppins:wght@400;500;700;800", "Caveat:wght@700"];
const tint: ThemeTint = {
  "--t-accent": "#fd3a73", "--t-bg": "#ffffff", "--t-ink": "#21262e", "--t-muted": "#7c8591", "--t-line": "#e8eaed",
  "--t-field": "#fff7f9", "--t-radius": "14px", "--t-font": "Poppins, system-ui, sans-serif",
};
const DEMO_WISHES = [
  { id: "w1", name: "Sarah", message: "Dari dulu yakin kalian endgame! Swipe right-ku paling berfaedah.", created_at: new Date(Date.now() - 2 * 3600e3).toISOString() },
  { id: "w2", name: "Bang Reza", message: "Match terbaik sepanjang masa. Samawa Maya & Kevin!", created_at: new Date(Date.now() - 5 * 3600e3).toISOString() },
];
const DEMO_PROFILE = { bride: { age: "27", likes: "kopi susu, hujan, kamu" }, groom: { age: "29", likes: "naik gunung, dia, dia, dia" } };
const TIERS = [
  { name: "Super Like", price: "Rp200rb", icon: ic.star, color: "#35c9f3" },
  { name: "Boost", price: "Rp500rb", icon: ic.zap, color: "#b06bff" },
  { name: "Flame", price: "Rp1jt", icon: ic.flame, color: "#fd3a73" },
];
const WISHLIST = [
  { name: "Mesin Espresso", price: "Rp2.350.000", icon: ic.coffee },
  { name: "Tenda Camping 4P", price: "Rp1.600.000", icon: ic.tent },
];

function Status({ time }: { time: string }) {
  return (
    <div className={s.status} aria-hidden>
      <span>{time}</span>
      <span className={s.statusIcons}><Lucide icon={ic.signal} /><Lucide icon={ic.wifi} /><Lucide icon={ic.batteryFull} /></span>
    </div>
  );
}

function city(address: string) {
  const parts = address.split(",").map(p => p.trim()).filter(Boolean);
  return parts[parts.length - 1] ?? "";
}

export default function KencanTheme({ data, slug, guestToken, demo, skipCover }: ThemeProps) {
  const couple = coupleLabel(data);
  const handle = `${data.couple.bride}&${data.couple.groom}`.toLowerCase().replace(/\s+/g, "");
  const longDate = formatDate(data.date);
  const clock = toDate(data.date) ? `${formatDate(data.date, { day: "2-digit" })}:${formatDate(data.date, { month: "2-digit" })}` : "09:05";
  const where = city(data.address) || data.place;
  const rsvp = useRsvp({ slug, guestToken, demo });
  const wishes = useWishes({ slug, guestToken, demo, seed: DEMO_WISHES });
  const sheets = useSheets();
  const { copy, copied } = useCopy();
  const stories = storyItems(data);
  const since = stories[0]?.date?.match(/\d{4}/)?.[0];
  const cardA = data.gallery[0] ?? data.couple.bridePhoto;
  const cardB = data.gallery[1] ?? data.couple.groomPhoto;
  const rest = data.gallery.slice(2);
  const grid = rest.length >= 2 ? rest : data.gallery;
  const people = [
    { key: "bride" as const, name: data.couple.brideFull ?? data.couple.bride, parents: data.couple.brideParents, photo: data.couple.bridePhoto ?? data.gallery[0] },
    { key: "groom" as const, name: data.couple.groomFull ?? data.couple.groom, parents: data.couple.groomParents, photo: data.couple.groomPhoto ?? data.gallery[1] },
  ];

  return (
    <ThemeShell
      fonts={FONTS}
      background="#fff0f4"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Status time={clock} />
          <div className={s.match}>
            <h1>It&apos;s a Match!</h1>
            <p>Dan kali ini... selamanya.</p>
          </div>
          <div className={s.cards} aria-hidden>
            <div className={`${s.card} ${s.cardA}`}><Photo src={cardA} /></div>
            <div className={`${s.card} ${s.cardB}`}><Photo src={cardB} /></div>
            <span className={s.bigHeart}><Lucide icon={ic.heart} size={28} color="#fd3a73" /></span>
          </div>
          <div className={s.info}>
            <h2>{couple}</h2>
            <p>{[since ? `Match sejak ${since}` : "", `${data.eventLabel ?? "Pernikahan"} ${longDate}`, where].filter(Boolean).join(" · ")}</p>
          </div>
          <div className={s.kepada}>
            <small>UNDANGAN UNTUK</small>
            <strong>{guestLabel(data)}</strong>
          </div>
          <div className={s.coverBtns}>
            <span className={s.nope} aria-hidden><Lucide icon={ic.x} size={22} /></span>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.heart} size={17} color="#fd3a73" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <Status time={clock} />
      <header className={s.nav}>
        <span aria-hidden><Lucide icon={ic.arrowLeft} size={20} color="#7c8591" /></span>
        <span className={s.brand}><Lucide icon={ic.flame} size={20} color="#fd3a73" />{handle}</span>
        <span aria-hidden><Lucide icon={ic.slidersHorizontal} size={20} color="#7c8591" /></span>
      </header>

      <main className={s.body}>
        <section className={s.section} aria-labelledby="kc-profil">
          <h2 id="kc-profil">Profil Mempelai</h2>
          {people.map(person => (
            <article key={person.key} className={s.profile}>
              <Photo src={person.photo} alt={person.name} />
              <div className={s.profileText}>
                <span className={s.profileName}><strong>{person.name}{demo ? `, ${DEMO_PROFILE[person.key].age}` : ""}</strong><Lucide icon={ic.badgeCheck} size={15} color="#35c9f3" /></span>
                {person.parents && <small>{person.parents}</small>}
                {demo && <small>Suka: {DEMO_PROFILE[person.key].likes}</small>}
              </div>
            </article>
          ))}
        </section>

        {stories.length > 0 && (
          <section className={s.section} aria-labelledby="kc-chat">
            <h2 id="kc-chat">Riwayat Chat</h2>
            <p className={s.sub}>{since ? `Setelah match, ${since}` : "Dari match sampai pelaminan"}</p>
            <div className={s.chat}>
              {stories.map((story, index) => (
                <div key={story.title + index} className={index % 2 ? s.rowOut : s.rowIn}>
                  <p className={index % 2 ? s.out : s.in}>{story.body}</p>
                </div>
              ))}
              <div className={s.rowOut}><p className={`${s.out} ${s.fit}`}>Deal. Selamanya. ✓✓</p></div>
            </div>
          </section>
        )}

        <section className={s.section} aria-labelledby="kc-acara">
          <h2 id="kc-acara">Rencana Kencan Terakhir</h2>
          <p className={s.sub}>{longDate} — datang ya</p>
          {data.events.map((event, index) => {
            const href = mapsHref(data, event);
            return (
              <article key={event.name + index} className={s.event}>
                <span className={s.pin} aria-hidden><Lucide icon={ic.mapPin} size={18} color="#fff" /></span>
                <div className={s.eventText}>
                  <strong>{event.name}</strong>
                  <small>{[event.time, [event.venue, event.address].filter(Boolean).join(", ")].filter(Boolean).join(" · ")}</small>
                  {event.date && toDate(event.date) && formatDate(event.date) !== longDate && <small>{formatDate(event.date)}</small>}
                </div>
                {href && <a className={s.rute} href={href} target="_blank" rel="noreferrer" aria-label={`Rute ke ${event.name}`}>Rute</a>}
              </article>
            );
          })}
        </section>

        {grid.length > 0 && (
          <section className={s.section} aria-labelledby="kc-galeri">
            <h2 id="kc-galeri">Galeri</h2>
            <p className={s.sub}>Foto profil bersama</p>
            <div className={s.grid}>
              {[0, 1].map(col => (
                <div key={col} className={s.col}>
                  {grid.map((src, index) => index % 2 === col && (
                    <Photo key={src + index} src={src} alt={`Foto ${index + 1}`} className={Math.floor(index / 2) % 2 ? s.short : s.tall} />
                  ))}
                </div>
              ))}
            </div>
          </section>
        )}

        {(demo || data.gifts.length > 0) && (
          <section className={s.section} aria-labelledby="kc-kado">
            <h2 id="kc-kado">{demo ? "Kado & Super Like" : "Kado"}</h2>
            <p className={s.sub}>Dukung kencan selamanya kami</p>
            {demo && (
              <>
                <div className={s.tiers}>
                  {TIERS.map(tier => (
                    <div key={tier.name} className={s.tier} style={{ borderColor: tier.color }}>
                      <Lucide icon={tier.icon} size={20} color={tier.color} />
                      <strong>{tier.name}</strong><small>{tier.price}</small>
                    </div>
                  ))}
                </div>
                {WISHLIST.map(item => (
                  <div key={item.name} className={s.wish}>
                    <span className={s.wishIcon} aria-hidden><Lucide icon={item.icon} size={18} color="#fd3a73" /></span>
                    <div><strong>{item.name}</strong><small>{item.price}</small></div>
                    <span className={s.beri}>Beri</span>
                  </div>
                ))}
              </>
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
                  {info.copy && <button type="button" className={s.salin} onClick={() => copy(info.copy)}>{copied === info.copy ? "Tersalin" : "Salin"}</button>}
                  {info.image && <a className={s.salin} href={info.image} target="_blank" rel="noreferrer">Lihat QR</a>}
                </div>
              );
            })}
          </section>
        )}

        <section className={s.section} aria-labelledby="kc-ucapan">
          <h2 id="kc-ucapan">Mereka Sudah Swipe Right</h2>
          <p className={s.sub}>Ucapan yang masuk</p>
          {wishes.wishes.length === 0 && <p className={s.empty}>Belum ada ucapan. Jadilah yang pertama swipe right!</p>}
          {wishes.wishes.slice(0, 8).map(wish => (
            <article key={wish.id} className={s.wishCard}>
              <span className={s.wAv} aria-hidden>{wish.name.slice(0, 1).toUpperCase()}</span>
              <div><strong>{wish.name}</strong><p>{wish.message}</p></div>
            </article>
          ))}
        </section>
      </main>

      <nav className={s.bottom} aria-label="Aksi undangan">
        <button type="button" className={s.no} onClick={() => sheets.openRsvp("no")} aria-label="Tidak bisa hadir"><Lucide icon={ic.x} size={22} color="#ff7854" /></button>
        <button type="button" className={s.rsvpBtn} onClick={() => sheets.openRsvp("yes")}><Lucide icon={ic.heart} size={17} color="#fff" />Hadir — Swipe Right</button>
        <button type="button" className={s.star} onClick={sheets.openWish} aria-label="Kirim ucapan"><Lucide icon={ic.star} size={20} color="#35c9f3" /></button>
      </nav>

      <Sheet open={sheets.sheet === "rsvp"} onClose={sheets.close} title="Konfirmasi Kehadiran" tint={tint}>
        <RsvpForm key={sheets.attendance} initialAttendance={sheets.attendance} rsvp={rsvp} guestName={data.guestName} demo={demo} labels={{ yes: "Swipe right (hadir)", no: "Berhalangan" }} />
      </Sheet>
      <Sheet open={sheets.sheet === "wish"} onClose={sheets.close} title="Kirim Super Like & Ucapan" tint={tint}>
        <WishForm wishes={wishes} guestName={data.guestName} demo={demo} />
      </Sheet>
    </ThemeShell>
  );
}
