"use client";
// Theme "Saku Biru" — undangan bergaya dompet digital biru dengan layar PIN (design: Saku Bersama, Rizki & Amanda).
import { useState, type CSSProperties } from "react";
import { toast } from "@/lib/celebrate";
import {
  Extras, Lucide, Photo, RsvpForm, Sheet, ThemeShell, WishForm, dateParts, formatDate, giftInfo, guestLabel,
  Tick, mapsHref, storyItems, toDate, useCopy, useCountdown, useRsvp, useSheets, useWishes, type ThemeProps, type ThemeTint,
} from "../kit";
import { ic } from "./icons";
import s from "./styles.module.css";

const FONTS = ["Plus Jakarta Sans:wght@400;600;700;800"];
const tint: ThemeTint = {
  "--t-accent": "#1c8fe0", "--t-accent-ink": "#ffffff", "--t-bg": "#ffffff", "--t-ink": "#1c1c1c", "--t-muted": "#6b7280", "--t-line": "#e3e6ea",
  "--t-field": "#f3f7f9", "--t-radius": "12px", "--t-font": "'Plus Jakarta Sans', system-ui, sans-serif",
};
const DEMO_WISHES = [
  { id: "w1", name: "Bang Hendri", message: "Transferan doa terkirim instan, tanpa biaya admin. Selamat!" },
  { id: "w2", name: "Kak Vina", message: "Saldo bahagianya awet ya sampai kakek nenek!" },
];
const DEMO_AMOUNTS = ["-Rp24.000", "+1 pasangan"];
const DEMO_CAPTIONS = ["Scan pertama", "Top up bareng", "Checkout cincin"];
const DEMO_WISHLIST = [
  { name: "AC 1/2 PK", price: "Rp2.900.000", icon: ic.airVent },
  { name: "Sofa Bed", price: "Rp1.850.000", icon: ic.armchair },
];
const TX_ICONS = [ic.qrCode, ic.arrowDownLeft, ic.gem];
const BADGES = ["+1 doa", "+1 restu"];
const TIERS = ["Rp50rb", "Rp200rb", "Rp500rb", "Bebas"];
const BACKSPACE = <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true"><path d="M10 5h10a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1H10l-7-7z" /><path d="m12 9 6 6" /><path d="m18 9-6 6" /></svg>;


function city(address: string) {
  const parts = address.split(",").map(part => part.trim()).filter(Boolean);
  return parts[parts.length - 1] ?? "";
}

const initial = (name: string) => (name.trim().replace(/^(bu|ibu|pak|bapak|bpk\.?|mas|mbak|bang|kak|om|tante)\s+/i, "").slice(0, 1) || "?").toUpperCase();

export default function SakuBiruTheme({ data, slug, guestToken, demo, skipCover }: ThemeProps) {
  const { bride, groom } = data.couple;
  const pair = `${groom} & ${bride}`;
  const parts = dateParts(data.date);
  const date = toDate(data.date);
  const mm = date ? new Intl.DateTimeFormat("id-ID", { timeZone: "Asia/Jakarta", month: "2-digit" }).format(date) : "";
  const dd = parts.day.padStart(2, "0");
  const code = parts.day ? `${dd}${mm}` : "";
  const where = city(data.address) || data.place;
  const label = data.eventLabel ?? "Pernikahan";
  const shortDate = formatDate(data.date, { weekday: "long", day: "numeric", month: "short", year: "numeric" });
  const countdown = useCountdown(data.date);
  const rsvp = useRsvp({ slug, guestToken, demo });
  const wishes = useWishes({ slug, guestToken, demo, seed: DEMO_WISHES });
  const sheets = useSheets();
  const { copy, copied } = useCopy();
  const [pin, setPin] = useState(code);
  const [tier, setTier] = useState(2);
  const [given, setGiven] = useState<string[]>([]);
  const [scans, setScans] = useState(0);
  const stories = storyItems(data);
  const people = [
    { name: data.couple.groomFull ?? groom, parents: data.couple.groomParents, photo: data.couple.groomPhoto ?? data.gallery[0] },
    { name: data.couple.brideFull ?? bride, parents: data.couple.brideParents, photo: data.couple.bridePhoto ?? data.gallery[1] },
  ];
  const daysLeft = !countdown.ready ? "–" : countdown.done ? "Hari ini" : <><Tick value={Number(countdown.days)} /> hari</>;
  const press = (key: string) => setPin(value => (key === "back" ? value.slice(0, -1) : key === "fill" ? code : value.length >= 6 ? value : value + key));
  const pinOk = Boolean(code) && pin === code;

  return (
    <ThemeShell
      fonts={FONTS}
      background="#042a42"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.coverBody}>
            <div className={s.merchant}>
              <Photo src={data.gallery[0] ?? data.couple.groomPhoto} alt={`Foto ${pair}`} className={s.merchantAv} />
              <small>Pembayaran kepada</small>
              <h1>{label} {pair}</h1>
              <small>{[formatDate(data.date), where].filter(Boolean).join(" · ")}</small>
              <div className={s.total}>
                <small>Total yang harus dibayar</small>
                <strong>Kehadiran &amp; Doa Restu</strong>
              </div>
            </div>
            <div className={s.pin}>
              <p id="sb-pin">Masukkan PIN untuk membuka undangan</p>
              <div className={`${s.dots} ${pinOk ? s.dotsOk : code && pin.length >= code.length ? s.dotsBad : ""}`} aria-hidden>
                {Array.from({ length: 6 }, (_, index) => <i key={index} className={index < pin.length ? s.dotOn : undefined} />)}
              </div>
            </div>
            <div className={s.guest}>
              <span>AKUN TAMU TERVERIFIKASI</span>
              <h2>{guestLabel(data)}</h2>
            </div>
            <div className={s.pad} role="group" aria-labelledby="sb-pin">
              {["1", "2", "3", "4", "5", "6", "7", "8", "9"].map(key => (
                <button key={key} type="button" className={s.key} onClick={() => press(key)}>{key}</button>
              ))}
              <button type="button" className={`${s.key} ${s.keyHeart}`} onClick={() => press("fill")} aria-label="Isi PIN otomatis">♥</button>
              <button type="button" className={s.key} onClick={() => press("0")}>0</button>
              <button type="button" className={`${s.key} ${s.keyBack}`} onClick={() => press("back")} aria-label="Hapus angka">{BACKSPACE}</button>
            </div>
            <button type="button" className={s.openBtn} onClick={open}>
              <Lucide icon={ic.lockOpen} color="#063f63" />{pinOk ? "PIN benar — Buka Undangan" : "Buka Undangan"}
            </button>
            {code && <p className={s.hint}>Hint: tanggal hari H kami ya, {code}</p>}
          </div>
        </section>
      )}
    >
      <header className={s.head}>
        <div className={s.hi}>
          <div>
            <h1>Saku Bersama</h1>
            <p>{[pair, shortDate].filter(Boolean).join(" · ")}</p>
          </div>
          <button type="button" className={s.qr} onClick={() => { setScans(count => count + 1); toast("Undangan terverifikasi"); }} aria-label="Pindai undangan">
            <Lucide icon={ic.scanLine} size={18} />
            <i key={scans} className={s.qrBeam} aria-hidden />
          </button>
        </div>
      </header>

      <main className={s.body}>
        <section className={s.stats} aria-label="Ringkasan">
          <div><span className={s.beat}><Lucide icon={ic.heart} color="#1c8fe0" /></span><strong>100%</strong><small>Cinta</small></div>
          <div><Lucide icon={ic.calendarCheck} color="#1c8fe0" /><strong>{daysLeft}</strong><small>Hari H</small></div>
          <div>
            <Lucide icon={ic.users} color="#1c8fe0" />
            <strong>{demo ? "512" : wishes.wishes.length}</strong>
            <small>{demo ? "Tamu" : "Ucapan"}</small>
          </div>
        </section>

        <Extras slot="opening" className={s.extras} />

        <section className={s.card} aria-labelledby="sb-couple">
          <div className={s.cardHead}><h2 id="sb-couple">Pemilik Saku</h2></div>
          {people.map((person, index) => (
            <div key={index} className={s.owner}>
              <Photo src={person.photo} alt={person.name} className={s.avatar} />
              <div className={s.ownerText}><strong>{person.name}</strong>{person.parents && <small>{person.parents}</small>}</div>
              <span className={s.badge}><Lucide icon={ic.shieldCheck} size={12} />Premium</span>
            </div>
          ))}
        </section>

        {stories.length > 0 && (
          <section className={s.card} aria-labelledby="sb-story">
            <div className={s.cardHead}><h2 id="sb-story">Riwayat Transaksi</h2></div>
            <ol className={s.list}>
              {stories.map((story, index) => {
                const last = index === stories.length - 1 && stories.length > 1;
                return (
                  <li key={story.title + index} className={s.tx}>
                    <span className={s.txIcon} aria-hidden><Lucide icon={TX_ICONS[index % TX_ICONS.length]} color="#0a5a8a" /></span>
                    <div className={s.txText}>
                      <strong>{[story.date, story.title].filter(Boolean).join(" · ")}</strong>
                      <small>{story.body}</small>
                      {story.image && <Photo src={story.image} alt={story.title} className={s.txImg} />}
                    </div>
                    <span className={`${s.txAmt} ${demo && index === 0 && !last ? s.txSpend : ""}`}>{last ? "LUNAS" : demo ? DEMO_AMOUNTS[index % 2] : "Berhasil"}</span>
                  </li>
                );
              })}
            </ol>
          </section>
        )}

        {data.events.length > 0 && (
          <section className={s.card} aria-labelledby="sb-events">
            <div className={s.cardHead}><h2 id="sb-events">Jadwal Pembayaran Kehadiran</h2></div>
            {data.events.map((event, index) => {
              const href = mapsHref(data, event);
              return (
                <article key={event.name + index} className={s.event}>
                  <span className={s.eventIcon} aria-hidden><Lucide icon={ic.calendarHeart} size={18} color="#1c8fe0" /></span>
                  <div className={s.eventText}>
                    <strong>{[event.name, formatDate(event.date, { weekday: "long", day: "numeric", month: "short", year: "numeric" })].filter(Boolean).join(" · ")}</strong>
                    <small>{[event.time, [event.venue, event.address].filter(Boolean).join(", ")].filter(Boolean).join(" · ")}</small>
                  </div>
                  {href && <a className={s.routeBtn} href={href} target="_blank" rel="noreferrer" aria-label={`Rute ke ${event.name}`}>Rute</a>}
                </article>
              );
            })}
          </section>
        )}

        <Extras slot="event" className={s.extras} />

        {data.gallery.length > 0 && (
          <section className={s.card} aria-labelledby="sb-gallery">
            <div className={s.cardHead}><h2 id="sb-gallery">Galeri</h2><span>{data.gallery.length} foto</span></div>
            <div className={s.gallery}>
              {data.gallery.map((src, index) => (
                <figure key={src + index} className={s.shot}>
                  <Photo src={src} alt={demo && DEMO_CAPTIONS[index] ? DEMO_CAPTIONS[index] : `Foto ${index + 1}`} />
                  {demo && DEMO_CAPTIONS[index] && <figcaption>{DEMO_CAPTIONS[index]}</figcaption>}
                </figure>
              ))}
            </div>
          </section>
        )}

        <Extras slot="story" className={s.extras} />
        <Extras slot="end" className={s.extras} />

        {(demo || data.gifts.length > 0) && (
          <section className={s.card} aria-labelledby="sb-gift">
            <div className={s.cardHead}><h2 id="sb-gift">Kirim Kado</h2>{demo && <span>Wishlist</span>}</div>
            {demo && (
              <>
                <div className={s.tiers} role="group" aria-label="Nominal kado" style={{ "--i": tier } as CSSProperties}>
                  <i className={s.tierPill} aria-hidden />
                  {TIERS.map((name, index) => (
                    <button key={name} type="button" className={index === tier ? s.tierOn : undefined} aria-pressed={index === tier} onClick={() => setTier(index)}>{name}</button>
                  ))}
                </div>
                {DEMO_WISHLIST.map(item => (
                  <div key={item.name} className={s.item}>
                    <span className={s.itemIcon}><Lucide icon={item.icon} size={17} color="#0a5a8a" /></span>
                    <div><strong>{item.name}</strong><small>{item.price}</small></div>
                    <button type="button" className={s.ghostBtn} aria-pressed={given.includes(item.name)}
                      onClick={() => { setGiven(list => list.includes(item.name) ? list : [...list, item.name]); sheets.openWish(); }}>
                      {given.includes(item.name) ? <><Lucide icon={ic.check} size={12} />Ditandai</> : "Beri"}
                    </button>
                  </div>
                ))}
              </>
            )}
            {data.gifts.map(gift => {
              const info = giftInfo(gift);
              const number = gift.type === "bank" ? `${info.title} ${info.number}` : info.number;
              const title = gift.type === "address" ? "Kirim Kado" : gift.type === "bank" ? "Amplop Digital" : `Amplop Digital · ${info.title}`;
              return (
                <div key={gift.id} className={s.amplop}>
                  <Lucide icon={ic.qrCode} size={18} color="#1c8fe0" />
                  <div>
                    <strong>{title}</strong>
                    <small>{[number, info.holder ? `a.n. ${info.holder}` : ""].filter(Boolean).join(" · ")}</small>
                    {info.image && <Photo src={info.image} alt="Kode QRIS" className={s.qris} />}
                  </div>
                  {info.copy && <button type="button" className={s.copyBtn} onClick={() => copy(info.copy)}><span key={String(copied === info.copy)} className={s.copyLabel}>{copied === info.copy ? "Tersalin" : "Salin"}</span></button>}
                </div>
              );
            })}
          </section>
        )}

        <section className={s.card} aria-labelledby="sb-wishes">
          <div className={s.cardHead}><h2 id="sb-wishes">Ucapan Masuk</h2><span>{demo ? "248" : wishes.wishes.length}</span></div>
          {wishes.wishes.length === 0 && <p className={s.empty}>Belum ada ucapan masuk. Kirim doa pertamamu lewat tombol di bawah.</p>}
          {wishes.wishes.slice(0, 8).map((wish, index) => (
            <article key={wish.id} className={s.msg}>
              <span className={s.msgAv} aria-hidden>{initial(wish.name)}</span>
              <div className={s.msgText}>
                <div className={s.msgHead}><strong>{wish.name}</strong><em>{BADGES[index % 2]}</em></div>
                <p>{wish.message}</p>
              </div>
            </article>
          ))}
        </section>
      </main>

      <nav className={s.bottom} aria-label="Aksi undangan">
        <button type="button" className={s.chatBtn} onClick={sheets.openWish} aria-label="Kirim ucapan"><Lucide icon={ic.messageCircle} size={18} color="#1c8fe0" /></button>
        <button type="button" className={s.rsvpBtn} onClick={sheets.openRsvp}><Lucide icon={ic.check} color="#fff" />Konfirmasi Hadir</button>
      </nav>

      <Sheet open={sheets.sheet === "rsvp"} onClose={sheets.close} title="Konfirmasi Kehadiran" tint={tint}>
        <RsvpForm rsvp={rsvp} guestName={data.guestName} demo={demo} labels={{ submit: "Bayar dengan Kehadiran" }} />
      </Sheet>
      <Sheet open={sheets.sheet === "wish"} onClose={sheets.close} title="Kirim Doa & Ucapan" tint={tint}>
        <WishForm wishes={wishes} guestName={data.guestName} demo={demo} submitLabel="Kirim Doa" />
      </Sheet>
    </ThemeShell>
  );
}
