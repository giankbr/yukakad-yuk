"use client";
// Theme "Pesan-Antar" — undangan bergaya aplikasi pesan-antar makanan (design: Undangan — Tema Pesan-Antar (Rendi & Salma)).
import {
  Extras, Lucide, Photo, RsvpForm, Sheet, ThemeShell, WishForm, dateParts, formatDate, giftInfo, guestLabel,
  mapsHref, storyItems, toDate, useCopy, useCountdown, useRsvp, useSheets, useWishes, type ThemeProps, type ThemeTint,
} from "../kit";
import { ic } from "./icons";
import s from "./styles.module.css";

const FONTS = ["Figtree:wght@400;600;700;800"];
const tint: ThemeTint = {
  "--t-accent": "#00b14f", "--t-accent-ink": "#ffffff", "--t-bg": "#ffffff", "--t-ink": "#1c1c1c", "--t-muted": "#707579", "--t-line": "#edeff1",
  "--t-field": "#f7f7f7", "--t-radius": "12px", "--t-font": "Figtree, system-ui, sans-serif",
};
const DEMO_WISHES = [
  { id: "w1", name: "Bang Ucok", message: "Pesanan diterima dengan sempurna! Semoga langgeng, kurirnya ramah pula.", created_at: new Date(Date.now() - 2 * 3600e3).toISOString() },
  { id: "w2", name: "Kak Maya", message: "Rasa bahagianya sampai! Samawa ya Rendi & Salma.", created_at: new Date(Date.now() - 5 * 3600e3).toISOString() },
];
const DEMO_CAPTIONS = [["Ngopi bareng", "2,1rb"], ["Jalan sore", "1,4rb"], ["Nonton konser", "960"], ["Piknik taman", "960"]];
const DEMO_PRODUCTS = [
  { name: "Sprei & Bedcover Set", price: "Rp750.000", tag: "Paling laris", icon: ic.bedDouble },
  { name: "Set Panci Premium", price: "Rp1.100.000", tag: "", icon: ic.cookingPot },
  { name: "Lampu Meja Estetik", price: "Rp450.000", tag: "Hemat", icon: ic.lamp },
];


function city(address: string) {
  const parts = address.split(",").map(part => part.trim()).filter(Boolean);
  return parts[parts.length - 1] ?? "";
}

function voucherLabel(name: string, index: number) {
  if (/akad/i.test(name)) return "AKAD";
  if (/resepsi|pesta/i.test(name)) return "PESTA";
  return (name.split(" ")[0] || `ACARA ${index + 1}`).toUpperCase();
}

const Dash = () => <i className={s.dash} aria-hidden />;

export default function PesanAntarTheme({ data, slug, guestToken, demo, skipCover }: ThemeProps) {
  const { couple } = data;
  const names = `${couple.groom} & ${couple.bride}`;
  const parts = dateParts(data.date);
  const date = toDate(data.date);
  const code = date ? `${parts.day.padStart(2, "0")}${String(date.getMonth() + 1).padStart(2, "0")}${parts.year.slice(-2)}` : "";
  const orderNo = `RS-${code ? `${code}-` : ""}BAHAGIA`;
  const longDate = formatDate(data.date);
  const shortDate = formatDate(data.date, { day: "numeric", month: "short", year: "numeric" });
  const where = city(data.address) || data.place;
  const countdown = useCountdown(data.date);
  const rsvp = useRsvp({ slug, guestToken, demo });
  const wishes = useWishes({ slug, guestToken, demo, seed: DEMO_WISHES });
  const sheets = useSheets();
  const { copy, copied } = useCopy();
  const stories = storyItems(data);
  const eta = !countdown.ready ? "Segera tiba" : countdown.done ? "Pesanan telah tiba!" : `Tiba dalam ${Number(countdown.days)} hari`;
  const people = [
    { key: "groom", name: couple.groomFull ?? couple.groom, parents: couple.groomParents, photo: couple.groomPhoto ?? data.gallery[0] },
    { key: "bride", name: couple.brideFull ?? couple.bride, parents: couple.brideParents, photo: couple.bridePhoto ?? data.gallery[1] },
  ];
  const money = data.gifts.filter(gift => gift.type !== "address");
  const addresses = data.gifts.filter(gift => gift.type === "address");

  const share = async () => {
    const url = window.location.href;
    if (navigator.share) {
      try { await navigator.share({ title: `Undangan ${names}`, url }); } catch { /* dismissed */ }
    } else {
      void copy(url);
    }
  };

  return (
    <ThemeShell
      fonts={FONTS}
      background="#e6e9eb"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.illus} aria-hidden><Photo src="/themes/img/a98.webp" /></div>
          <span className={s.eta}>{eta}</span>
          <div className={s.coverSpacer} />
          <div className={s.receipt}>
            <div className={s.receiptHead}>
              <div><small>Pesanan Spesial</small><h1>{names}</h1></div>
              <span className={s.badge} aria-hidden><Lucide icon={ic.packageCheck} size={22} color="#009643" /></span>
            </div>
            <p className={s.receiptDate}>{[longDate, where].filter(Boolean).join(" · ")}</p>
            <Dash />
            <ul className={s.items}>
              {data.events.map((event, index) => (
                <li key={event.name + index}><b>1x</b><span>{event.name}</span><strong>Gratis</strong></li>
              ))}
              <li><b>1x</b><span>Cinta selamanya</span><strong>Tak ternilai</strong></li>
            </ul>
            <Dash />
            <div className={s.total}><span>Total dibayar dengan</span><strong>Doa &amp; Kehadiranmu</strong></div>
            <div className={s.kepada}><small>Diantar kepada Yth.</small><strong>{guestLabel(data)}</strong></div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.packageOpen} color="#fff" />Terima Pesanan</button>
          </div>
          <div className={s.strip} aria-hidden>
            <span><Lucide icon={ic.bike} size={12} color="#fff" />Diantar dengan cinta</span>
            <span><Lucide icon={ic.shieldCheck} size={12} color="#fff" />Dijamin bahagia</span>
            <span><Lucide icon={ic.timer} size={12} color="#fff" />Tepat waktu</span>
          </div>
        </section>
      )}
    >
      <header className={s.header}>
        <div className={s.nav}>
          <Lucide icon={ic.arrowLeft} size={20} color="#1c1c1c" />
          <div><h1>Lacak Pesanan</h1><small>No. {orderNo}</small></div>
          <button type="button" className={s.share} onClick={share} aria-label="Bagikan undangan">
            <Lucide icon={copied ? ic.check : ic.share2} size={18} color="#1c1c1c" />
          </button>
        </div>
      </header>

      <main className={s.body}>
        <Extras slot="opening" className={s.extras} />

        <section className={s.section} aria-labelledby="pa-status">
          <h2 id="pa-status">Status Pengiriman Cinta</h2>
          <ol className={s.track}>
            {stories.map((story, index) => (
              <li key={story.title + index} className={s.step}>
                <span className={s.rail} aria-hidden><i className={s.dot}><Lucide icon={ic.check} size={13} color="#009643" /></i><i className={s.line} /></span>
                <div className={s.stepText}>
                  <strong>{[story.date, story.title].filter(Boolean).join(" · ")}</strong>
                  <p>{story.body}</p>
                  {story.image && <Photo src={story.image} alt={story.title} className={s.stepImg} />}
                </div>
              </li>
            ))}
            <li className={`${s.step} ${s.stepNow}`}>
              <span className={s.rail} aria-hidden><i className={s.dot}><Lucide icon={ic.package} size={13} color="#fff" /></i></span>
              <div className={s.stepText}>
                <strong>{[shortDate, "Tiba di tujuan"].filter(Boolean).join(" · ")}</strong>
                <p>{data.events.map(event => event.name).join(" & ") || data.eventLabel} — pesanan selesai, selamanya.</p>
              </div>
            </li>
          </ol>
        </section>

        <section className={s.section} aria-labelledby="pa-couple">
          <h2 id="pa-couple">Dapur Cinta · Mempelai</h2>
          <p className={s.sub}>Dua koki di balik pesanan istimewa ini</p>
          <div className={s.couple}>
            {people.map(person => (
              <article key={person.key} className={s.person}>
                <Photo src={person.photo} alt={person.name} className={s.personPhoto} />
                <div className={s.personText}>
                  <strong>{person.name}</strong>
                  {person.parents && <small>{person.parents}</small>}
                  {demo && <span><b>★ 4.9</b>(jutaan doa)</span>}
                </div>
              </article>
            ))}
          </div>
        </section>

        <section className={s.section} aria-labelledby="pa-events">
          <h2 id="pa-events">Voucher Acara</h2>
          {longDate && <p className={s.sub}>Berlaku {longDate}</p>}
          {data.events.map((event, index) => {
            const href = mapsHref(data, event);
            const sameDay = formatDate(event.date) === longDate;
            return (
              <article key={event.name + index} className={s.voucher}>
                <div className={s.voucherL} aria-hidden>
                  <Lucide icon={index === 0 ? ic.moonStar : ic.partyPopper} size={22} color="#fff" />
                  <span>{voucherLabel(event.name, index)}</span>
                </div>
                <div className={s.voucherR}>
                  <div><strong>{event.name}</strong>{href && <a href={href} target="_blank" rel="noreferrer" aria-label={`Maps ${event.venue}`}>Maps</a>}</div>
                  <b>{[sameDay ? "" : formatDate(event.date, { weekday: "short", day: "numeric", month: "short" }), event.time].filter(Boolean).join(" · ")}</b>
                  <small>{event.venue}</small>
                </div>
              </article>
            );
          })}
        </section>

        <Extras slot="event" className={s.extras} />

        {data.gallery.length > 0 && (
          <section className={s.section} aria-labelledby="pa-gallery">
            <h2 id="pa-gallery">Menu Favorit Kami</h2>
            <p className={s.sub}>{demo ? "Paling banyak dipesan ulang" : "Momen favorit kami berdua"}</p>
            <div className={s.grid}>
              {data.gallery.map((src, index) => (
                <figure key={src + index} className={s.dish}>
                  <Photo src={src} alt={demo && DEMO_CAPTIONS[index] ? DEMO_CAPTIONS[index][0] : `Foto ${index + 1}`} />
                  {demo && DEMO_CAPTIONS[index] && (
                    <figcaption><strong>{DEMO_CAPTIONS[index][0]}</strong><span><Lucide icon={ic.heart} size={11} color="#00b14f" />{DEMO_CAPTIONS[index][1]}</span></figcaption>
                  )}
                </figure>
              ))}
            </div>
          </section>
        )}

        <Extras slot="story" className={s.extras} />

        {demo && (
          <section className={s.section} aria-labelledby="pa-wishlist">
            <h2 id="pa-wishlist">Menu Wishlist Kado</h2>
            <p className={s.sub}>Pilih menu, kami yang bahagia</p>
            <div className={s.products}>
              {DEMO_PRODUCTS.map(item => (
                <div key={item.name} className={s.product}>
                  <span className={s.productIcon}><Lucide icon={item.icon} size={24} color="#009643" /></span>
                  <div><strong>{item.name}</strong><p><b>{item.price}</b>{item.tag && <em>{item.tag}</em>}</p></div>
                  <span className={s.plus}><Lucide icon={ic.plus} size={14} color="#00b14f" /></span>
                </div>
              ))}
            </div>
          </section>
        )}

        <Extras slot="end" className={s.extras} />

        {data.gifts.length > 0 && (
          <section className={s.section} aria-labelledby="pa-gift">
            <h2 id="pa-gift">Kirim Hadiah</h2>
            {money.map(gift => {
              const info = giftInfo(gift);
              return (
                <div key={gift.id} className={s.wallet}>
                  <span className={s.walletIcon} aria-hidden><Lucide icon={ic.wallet} size={20} color="#fff" /></span>
                  <div>
                    <strong>Amplop Digital</strong>
                    <small>{[[info.title, info.number].filter(Boolean).join(" "), info.holder ? `a.n. ${info.holder}` : ""].filter(Boolean).join(" · ")}</small>
                    {info.image && <Photo src={info.image} alt="Kode QRIS" className={s.qris} />}
                  </div>
                  {info.copy && <button type="button" onClick={() => copy(info.copy)}>{copied === info.copy ? "Tersalin" : "Salin"}</button>}
                </div>
              );
            })}
            {addresses.map(gift => (
              <div key={gift.id} className={s.address}>
                <Lucide icon={ic.mapPin} size={18} color="#00b14f" />
                <div><small>Alamat kirim kado</small><strong>{gift.address}</strong></div>
                {gift.address && <button type="button" onClick={() => copy(gift.address)}>{copied === gift.address ? "Tersalin" : "Salin"}</button>}
              </div>
            ))}
          </section>
        )}

        <section className={s.section} aria-labelledby="pa-wishes">
          <h2 id="pa-wishes">Ulasan Tamu</h2>
          <p className={s.sub}>{demo ? "★ 5.0 · 312 ulasan" : `${wishes.wishes.length} ucapan`}</p>
          {wishes.wishes.length === 0 && <p className={s.empty}>Belum ada ulasan. Jadilah yang pertama mengirim ucapan!</p>}
          {wishes.wishes.slice(0, 8).map(wish => (
            <article key={wish.id} className={s.review}>
              <div><strong>{wish.name}</strong><span aria-hidden>★★★★★</span></div>
              <p>{wish.message}</p>
            </article>
          ))}
        </section>

        <footer className={s.note}><a href="/" target="_blank" rel="noreferrer">dibuat dengan ♥ di Rawuh</a></footer>
      </main>

      <nav className={s.bottom} aria-label="Aksi undangan">
        <button type="button" className={s.ghostBtn} onClick={sheets.openWish}>Kirim Ucapan</button>
        <button type="button" className={s.solidBtn} onClick={sheets.openRsvp}>Konfirmasi Hadir</button>
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
