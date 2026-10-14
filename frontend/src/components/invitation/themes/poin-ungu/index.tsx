"use client";
// Theme "Poin Ungu" — undangan bergaya aplikasi poin/loyalti (design: Poin Bahagia, Putra & Keisha).
import {
  Lucide, Photo, RsvpForm, Sheet, ThemeShell, WishForm, formatDate, giftInfo, guestLabel,
  mapsHref, storyItems, useCopy, useRsvp, useSheets, useWishes, type ThemeProps, type ThemeTint,
} from "../kit";
import { ic } from "./icons";
import s from "./styles.module.css";

const FONTS = ["Poppins:wght@400;600;700;800", "JetBrains Mono:wght@700"];
const tint: ThemeTint = {
  "--t-accent": "#4f2bd1", "--t-bg": "#ffffff", "--t-ink": "#2b1f5c", "--t-muted": "#6e6a8a", "--t-line": "#ece7fa",
  "--t-field": "#f5f3fb", "--t-radius": "14px", "--t-font": "'Poppins', system-ui, sans-serif",
};
const DEMO_WISHES = [
  { id: "w1", name: "Tante Lusi", message: "Double points buat kalian: bahagia dunia akhirat. Hadir!", created_at: new Date(Date.now() - 2 * 3600e3).toISOString() },
  { id: "w2", name: "Raffi", message: "Member sejak 2019, akhirnya naik tier jadi suami istri. Selamat!", created_at: new Date(Date.now() - 5 * 3600e3).toISOString() },
];
const DEMO_CAPTIONS = ["Food court 2019", "Nonton midnight", "Lamaran"];
const DEMO_WISHLIST = [
  { name: "Microwave Digital", note: "22.000 poin ≈ Rp1.100.000", icon: ic.microwave },
  { name: "Smart Lamp Set", note: "9.000 poin ≈ Rp450.000", icon: ic.lamp },
  { name: "Kursi Santai", note: "36.000 poin ≈ Rp1.800.000", icon: ic.armchair },
];

const fmt = (n: number) => n.toLocaleString("id-ID");

function Status({ time }: { time: string }) {
  return (
    <div className={s.status} aria-hidden>
      {time}
      <span><Lucide icon={ic.signal} /><Lucide icon={ic.wifi} /><Lucide icon={ic.batteryFull} /></span>
    </div>
  );
}

function city(address: string) {
  const parts = address.split(",").map(part => part.trim()).filter(Boolean);
  return parts[parts.length - 1] ?? "";
}

export default function PoinUnguTheme({ data, slug, guestToken, demo, skipCover }: ThemeProps) {
  const { bride, groom } = data.couple;
  const couple = `${groom} & ${bride}`;
  const dd = formatDate(data.date, { day: "2-digit" });
  const mm = formatDate(data.date, { month: "2-digit" });
  const yyyy = formatDate(data.date, { year: "numeric" });
  const valid = /^\d+$/.test(dd) && /^\d+$/.test(mm);
  const clock = valid ? `${dd}:${mm}` : "09:41";
  const points = valid ? fmt(Number(`${dd}${mm}`)) : "100";
  const code = valid ? `SAH-${dd}${mm}${yyyy}` : "SAH";
  const longDate = formatDate(data.date);
  const where = city(data.address) || data.place;
  const label = data.eventLabel ?? "Pernikahan";

  const rsvp = useRsvp({ slug, guestToken, demo });
  const wishes = useWishes({ slug, guestToken, demo, seed: DEMO_WISHES });
  const sheets = useSheets();
  const { copy, copied } = useCopy();
  const stories = storyItems(data);
  const gallery = data.gallery;
  const people = [
    { name: data.couple.groomFull ?? groom, parents: data.couple.groomParents, photo: data.couple.groomPhoto ?? gallery[1] },
    { name: data.couple.brideFull ?? bride, parents: data.couple.brideParents, photo: data.couple.bridePhoto ?? gallery[2] },
  ];

  return (
    <ThemeShell
      fonts={FONTS}
      background="#1e0f5c"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Status time={clock} />
          <div className={s.coverBody}>
            <div className={s.badge} aria-hidden><span><Lucide icon={ic.sparkles} size={40} color="#fff" /></span></div>
            <p className={s.congrats}>Selamat! Kamu dapat</p>
            <div className={s.pts}>
              <h1>+{points} Poin Bahagia</h1>
              <p>dari transaksi: {label} {couple}</p>
              <small>{longDate}{where ? ` · ${where}` : ""}</small>
            </div>
            <div className={s.voucher}>
              <div className={s.vHead}><span>Voucher Undangan Premium</span><Lucide icon={ic.ticket} color="#ffc01e" /></div>
              <div className={s.vBody}>
                <small>Berlaku untuk:</small>
                <strong>{guestLabel(data)}</strong>
                <div className={s.tags}>
                  {data.events.map((event, index) => <span key={event.name + index}>1x {event.name.split(" ")[0]}</span>)}
                  <span className={s.tagGreen}>Tak terbatas doa</span>
                </div>
              </div>
              <div className={s.dash} aria-hidden />
              <div className={s.vFoot}>
                <code>Kode: {code}</code>
                <button type="button" className={s.use} onClick={open}>Pakai Sekarang</button>
              </div>
            </div>
            {stories.length > 0 && (
              <div className={s.hist}>
                <h2>Riwayat Poin Kami</h2>
                {stories.map((story, index) => (
                  <div key={story.title + index} className={s.histRow}>
                    <span>{story.date ? `${story.date} · ` : ""}{story.title}</span>
                    <b>+{fmt(100 * 10 ** Math.min(index, 4))}</b>
                  </div>
                ))}
              </div>
            )}
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.gift} size={17} color="#3b1ba8" />Tukar Poin — Buka Undangan</button>
            <p className={s.coverNote}>Poin tidak akan hangus. Cinta kami juga.</p>
          </div>
        </section>
      )}
    >
      <header className={s.header}>
        <Status time={clock} />
        <div className={s.hi}>
          <div>
            <h1>Poin Bahagia</h1>
            <p>{couple} · {longDate}</p>
          </div>
          <span className={s.pill}><Lucide icon={ic.sparkles} size={13} color="#ffc01e" />{points}</span>
        </div>
      </header>

      <main className={s.body}>
        <nav className={s.tukar} aria-label="Pintasan">
          <button type="button" onClick={sheets.openWish}><Lucide icon={ic.handHeart} size={18} color="#4f2bd1" /><strong>Doa</strong><small>100 poin</small></button>
          <a href={gallery.length ? "#pu-gallery" : "#pu-misi"}><Lucide icon={ic.camera} size={18} color="#4f2bd1" /><strong>Foto bareng</strong><small>500 poin</small></a>
          <button type="button" onClick={sheets.openRsvp}><Lucide icon={ic.utensils} size={18} color="#4f2bd1" /><strong>Makan enak</strong><small>0 poin</small></button>
        </nav>

        <section className={s.card} aria-labelledby="pu-member">
          <div className={s.head}><h2 id="pu-member">Member Prioritas</h2></div>
          {people.map(person => (
            <article key={person.name} className={s.member}>
              <Photo src={person.photo} alt={person.name} className={s.avatar} />
              <div className={s.grow}>
                <strong>{person.name}</strong>
                {person.parents && <small>{person.parents}</small>}
              </div>
              <span className={s.tier}><Lucide icon={ic.crown} size={12} color="#1fb24b" />Platinum</span>
            </article>
          ))}
        </section>

        <section className={s.card} id="pu-misi" aria-labelledby="pu-misi-h">
          <div className={s.head}><h2 id="pu-misi-h">Misi Berhadiah Poin</h2></div>
          {data.events.map((event, index) => {
            const href = mapsHref(data, event);
            const content = (
              <>
                <span className={s.mIcon}><Lucide icon={ic.target} size={17} color="#4f2bd1" /></span>
                <span className={s.grow}>
                  <strong>Hadiri {event.name}</strong>
                  <small>{[event.time, event.venue].filter(Boolean).join(" · ")}</small>
                  {event.date && formatDate(event.date) !== longDate && <small>{formatDate(event.date)}</small>}
                </span>
                <span className={s.plus}>+{fmt((index + 1) * 500)}</span>
              </>
            );
            return href
              ? <a key={event.name + index} className={s.mission} href={href} target="_blank" rel="noreferrer" aria-label={`Hadiri ${event.name} — buka lokasi di Maps`}>{content}</a>
              : <div key={event.name + index} className={s.mission}>{content}</div>;
          })}
          <button type="button" className={s.mission} onClick={sheets.openWish}>
            <span className={s.mIcon}><Lucide icon={ic.target} size={17} color="#4f2bd1" /></span>
            <span className={s.grow}><strong>Kirim ucapan &amp; doa</strong><small>Kapan saja, dari mana saja</small></span>
            <span className={s.plus}>+100</span>
          </button>
        </section>

        {gallery.length > 0 && (
          <section className={s.card} id="pu-gallery" aria-labelledby="pu-gallery-h">
            <div className={s.head}><h2 id="pu-gallery-h">Galeri Momen</h2><span>{gallery.length}</span></div>
            <div className={s.grid}>
              {gallery.map((src, index) => (
                <figure key={src + index}>
                  <Photo src={src} alt={`Foto momen ${index + 1}`} />
                  {demo && DEMO_CAPTIONS[index] && <figcaption>{DEMO_CAPTIONS[index]}</figcaption>}
                </figure>
              ))}
            </div>
          </section>
        )}

        {(demo || data.gifts.length > 0) && (
          <section className={s.card} aria-labelledby="pu-gift">
            <div className={s.head}><h2 id="pu-gift">{demo ? "Tukar Poin · Wishlist Kado" : "Tukar Poin · Kado"}</h2></div>
            {demo && DEMO_WISHLIST.map(item => (
              <div key={item.name} className={s.wish}>
                <span className={s.wIcon}><Lucide icon={item.icon} size={17} color="#4f2bd1" /></span>
                <span className={s.grow}><strong>{item.name}</strong><small>{item.note}</small></span>
                <span className={s.tukarBtn} aria-hidden>Tukar</span>
              </div>
            ))}
            {data.gifts.map(gift => {
              const info = giftInfo(gift);
              return (
                <div key={gift.id} className={s.amplop}>
                  <Lucide icon={ic.wallet} size={17} color="#ffc01e" />
                  <span className={s.grow}>
                    <strong>{gift.type === "address" ? "Kirim Kado" : gift.type === "qris" ? "QRIS" : "Amplop Digital"}</strong>
                    <small>{[gift.type === "bank" || gift.type === "ewallet" ? info.title : "", info.number, info.holder ? `a.n. ${info.holder}` : ""].filter(Boolean).join(" · ")}</small>
                    {info.image && <Photo src={info.image} alt="Kode QRIS" className={s.qris} />}
                  </span>
                  {info.copy && <button type="button" className={s.salin} onClick={() => copy(info.copy)}>{copied === info.copy ? "Tersalin" : "Salin"}</button>}
                </div>
              );
            })}
          </section>
        )}

        <section className={s.card} aria-labelledby="pu-wishes">
          <div className={s.head}><h2 id="pu-wishes">Ucapan Member</h2><span>{demo ? "248" : wishes.wishes.length}</span></div>
          {wishes.wishes.length === 0 && <p className={s.empty}>Belum ada ucapan. Jadilah member pertama yang mengirim doa!</p>}
          {wishes.wishes.slice(0, 8).map(wish => (
            <article key={wish.id} className={s.wishItem}>
              <span className={s.initial} aria-hidden>{wish.name.slice(0, 1).toUpperCase()}</span>
              <div className={s.grow}><strong>{wish.name}</strong><p>{wish.message}</p></div>
            </article>
          ))}
        </section>
      </main>

      <nav className={s.bottom} aria-label="Aksi undangan">
        <button type="button" className={s.chat} onClick={sheets.openWish} aria-label="Kirim ucapan"><Lucide icon={ic.messageCircle} size={18} color="#4f2bd1" /></button>
        <button type="button" className={s.rsvp} onClick={sheets.openRsvp}><Lucide icon={ic.sparkles} size={15} color="#ffc01e" />Klaim Misi — Konfirmasi Hadir</button>
      </nav>

      <Sheet open={sheets.sheet === "rsvp"} onClose={sheets.close} title="Konfirmasi Kehadiran" tint={tint}>
        <RsvpForm rsvp={rsvp} guestName={data.guestName} demo={demo} labels={{ submit: "Klaim Misi" }} />
      </Sheet>
      <Sheet open={sheets.sheet === "wish"} onClose={sheets.close} title="Kirim Ucapan & Doa" tint={tint}>
        <WishForm wishes={wishes} guestName={data.guestName} demo={demo} />
      </Sheet>
    </ThemeShell>
  );
}
