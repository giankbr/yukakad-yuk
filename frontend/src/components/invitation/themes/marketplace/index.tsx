"use client";
// Theme "Marketplace" — undangan bergaya aplikasi belanja (design: Undangan — Tema Marketplace (Rina & Bima)).
import { useState } from "react";
import {
  Lucide, Photo, RsvpForm, Sheet, ThemeShell, WishForm, coupleLabel, dateParts, formatDate, giftInfo, guestLabel,
  mapsHref, storyItems, timeAgo, useCopy, useCountdown, useRsvp, useSheets, useWishes, type ThemeProps, type ThemeTint,
} from "../kit";
import { ic } from "./icons";
import s from "./styles.module.css";

const FONTS = ["Nunito Sans:wght@400;600;700;800"];
const tint: ThemeTint = { "--t-accent": "#00aa5b", "--t-ink": "#212121", "--t-muted": "#6d7588", "--t-line": "#e4ebf5", "--t-radius": "10px", "--t-font": "'Nunito Sans', system-ui, sans-serif" };
const BARCODE = [2, 1, 3, 1, 2, 1, 1, 3, 2, 1, 2, 3, 1, 1, 2, 1, 3, 2, 1, 2, 1, 3, 1, 2];
const DEMO_WISHES = [
  { id: "w1", name: "Sinta", message: "Barakallahu lakuma! Semoga jadi keluarga sakinah, mawaddah, warahmah.", created_at: new Date(Date.now() - 2 * 3600e3).toISOString() },
  { id: "w2", name: "Om Hendra", message: "Produk original, seller ramah, pengiriman cinta super cepat. Recommended!", created_at: new Date(Date.now() - 5 * 3600e3).toISOString() },
];

function Status({ time, color }: { time: string; color: string }) {
  return (
    <div className={s.status} style={{ color }} aria-hidden>
      {time}
      <span><Lucide icon={ic.signal} color={color} /><Lucide icon={ic.wifi} color={color} /><Lucide icon={ic.batteryFull} color={color} /></span>
    </div>
  );
}

function city(address: string) {
  const parts = address.split(",").map(part => part.trim()).filter(Boolean);
  return parts[parts.length - 1] ?? "";
}

export default function MarketplaceTheme({ data, slug, guestToken, demo, skipCover }: ThemeProps) {
  const couple = coupleLabel(data);
  const parts = dateParts(data.date);
  const promo = parts.day && parts.monthShort ? `SPESIAL ${parts.day}.${String(new Date(data.date).getMonth() + 1).padStart(2, "0")}` : "SPESIAL";
  const clock = parts.day ? `${parts.day.padStart(2, "0")}:${String(new Date(data.date).getMonth() + 1).padStart(2, "0")}` : "12:12";
  const resi = parts.day ? `RB-${parts.day.padStart(2, "0")}${String(new Date(data.date).getMonth() + 1).padStart(2, "0")}${parts.year.slice(-2)}` : "RB-000000";
  const longDate = formatDate(data.date);
  const shortDate = formatDate(data.date, { day: "numeric", month: "short", year: "numeric" });
  const countdown = useCountdown(data.date);
  const rsvp = useRsvp({ slug, guestToken, demo });
  const wishes = useWishes({ slug, guestToken, demo, seed: DEMO_WISHES });
  const sheets = useSheets();
  const { copy, copied } = useCopy();
  const stories = storyItems(data);
  const gallery = data.gallery.length > 4 ? data.gallery.slice(1) : data.gallery;
  const [active, setActive] = useState(0);
  const hero = data.gallery[0];
  const where = city(data.address) || data.place;

  return (
    <ThemeShell
      fonts={FONTS}
      background="#e9edf2"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.coverBg} aria-hidden><Photo src={hero} /></div>
          <Status time={clock} color="#fff" />
          <div className={s.notifWrap}>
            <div className={s.notif}>
              <span className={s.appIcon}><Lucide icon={ic.package} size={18} color="#fff" /></span>
              <div><strong>Paket spesial untukmu telah tiba!</strong><small>Dari {couple}, khusus untukmu.</small></div>
              <em>baru saja</em>
            </div>
          </div>
          <div className={s.spacer} />
          <div className={s.coverContent}>
            <span className={s.tag}>{promo}</span>
            <div className={s.names}>
              <span>{data.eventLabel ?? "Pernikahan"}</span>
              <h1>{couple}</h1>
              <p>{longDate}</p>
            </div>
            <div className={s.label}>
              <div className={s.labelHead}>
                <span><Lucide icon={ic.truck} size={14} color="#00aa5b" />Pengiriman Cinta · Prioritas</span>
                <small>{resi}</small>
              </div>
              <div className={s.labelBody}>
                <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
                <strong>{guestLabel(data)}</strong>
                <span><Lucide icon={ic.mapPin} size={12} color="#6d7588" />Di tempat</span>
              </div>
              <div className={s.barcodeRow}>
                <span className={s.barcode} aria-hidden>{BARCODE.map((w, i) => <i key={i} style={{ width: w }} />)}</span>
                <small>Pengirim: {couple}</small>
              </div>
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.packageOpen} size={18} color="#fff" />Buka Paket Undangan</button>
            <p className={s.coverNote}>Mohon maaf apabila ada kesalahan penulisan nama &amp; gelar.</p>
          </div>
        </section>
      )}
    >
      <header className={s.top}>
        <Status time={clock} color="#212121" />
        <div className={s.searchRow}>
          <div className={s.search}><Lucide icon={ic.search} color="#6d7588" />Cari momen bahagia…</div>
          <span className={s.cart} aria-hidden><Lucide icon={ic.shoppingCart} size={24} color="#212121" /><b>1</b></span>
          <Lucide icon={ic.heart} size={24} color="#f94d63" />
        </div>
      </header>

      <main className={s.body}>
        <div className={s.bannerWrap}>
          <section className={s.banner} aria-label="Sampul">
            <Photo src={hero} alt={`Foto ${couple}`} />
            <div className={s.bannerOverlay}>
              <span className={s.tag}>{promo}</span>
              <span>{data.eventLabel ?? "Pernikahan"}</span>
              <h1>{couple}</h1>
              <p>{longDate}{where ? ` · ${where}` : ""}</p>
            </div>
          </section>
        </div>

        <section className={s.countdown} aria-label="Hitung mundur">
          <div className={s.countHead}>
            <span><Lucide icon={ic.zap} size={18} color="#fff" />Menuju Hari H</span>
            <span className={s.timer} aria-label={`${countdown.days} hari ${countdown.hours} jam ${countdown.minutes} menit lagi`}>
              <b>{countdown.days}</b>:<b>{countdown.hours}</b>:<b>{countdown.minutes}</b>
            </span>
          </div>
          <p>Stok kursi terbatas! Konfirmasi kehadiranmu sebelum hari H.</p>
        </section>

        <section className={s.section} aria-labelledby="mp-couple">
          <div className={s.sectionHead}><h2 id="mp-couple">Mempelai Pilihan</h2><span>Official ✓</span></div>
          <div className={s.couple}>
            {[
              { name: data.couple.brideFull ?? data.couple.bride, parents: data.couple.brideParents, photo: data.couple.bridePhoto ?? data.gallery[1] },
              { name: data.couple.groomFull ?? data.couple.groom, parents: data.couple.groomParents, photo: data.couple.groomPhoto ?? data.gallery[2] },
            ].map(person => (
              <article key={person.name} className={s.person}>
                <Photo src={person.photo} alt={person.name} />
                <div className={s.personInfo}>
                  <strong>{person.name}</strong>
                  {person.parents && <small>{person.parents}</small>}
                  <span><b className={s.star}>★</b>5.0 · Siap dipinang</span>
                  <span><Lucide icon={ic.badgeCheck} size={12} color="#00aa5b" />Terverifikasi</span>
                </div>
              </article>
            ))}
          </div>
        </section>

        {stories.length > 0 && (
          <section className={s.section} aria-labelledby="mp-story">
            <div className={s.sectionHead}><h2 id="mp-story">Lacak Perjalanan Cinta</h2><span>Detail</span></div>
            <div className={s.invoice}>
              <Lucide icon={ic.truck} size={20} color="#00aa5b" />
              <div><strong>Dalam pengiriman · Estimasi tiba {shortDate}</strong><small>No. Resi: {resi}-SELAMANYA</small></div>
            </div>
            <ol className={s.timeline} style={{ listStyle: "none", margin: 0, padding: 0 }}>
              {stories.map(story => (
                <li key={story.title + story.body} className={s.step}>
                  <span className={s.rail} aria-hidden><i className={s.dot} /><i className={s.line} /></span>
                  <div className={s.stepText}>
                    <div className={s.stepHead}><strong>{story.title}</strong>{story.date && <small>{story.date}</small>}</div>
                    <p>{story.body}</p>
                    {story.image && <Photo src={story.image} alt={story.title} />}
                  </div>
                </li>
              ))}
              <li className={`${s.step} ${s.stepNow}`}>
                <span className={s.rail} aria-hidden><i className={`${s.dot} ${s.dotNow}`} /></span>
                <div className={s.stepText}>
                  <div className={s.stepHead}><strong>Dalam Pengiriman</strong><small>{shortDate}</small></div>
                  <p>{data.events.map(e => e.name).join(" & ")} — menuju rumah tangga bersama.</p>
                </div>
              </li>
            </ol>
          </section>
        )}

        {gallery.length > 0 && (
          <section className={s.section} aria-labelledby="mp-gallery">
            <div className={s.sectionHead}><h2 id="mp-gallery">Foto dari Pembeli</h2><span>Lihat {gallery.length} foto</span></div>
            <div className={s.mainPhoto}>
              <Photo src={gallery[active]} alt={`Foto ${active + 1} dari ${gallery.length}`} />
              <span>{active + 1}/{gallery.length}</span>
            </div>
            {gallery.length > 1 && (
              <div className={s.thumbs}>
                {gallery.slice(0, 4).map((src, index) => (
                  <button key={src + index} type="button" className={s.thumb} aria-pressed={active === index} aria-label={`Lihat foto ${index + 1}`}
                    onClick={() => setActive(index === 3 && gallery.length > 4 ? (active + 1) % gallery.length : index)}>
                    <Photo src={src} />
                    {index === 3 && gallery.length > 4 && <b>+{gallery.length - 4}</b>}
                  </button>
                ))}
              </div>
            )}
            {demo && (
              <div className={s.video}>
                <span className={s.play}><Lucide icon={ic.play} size={14} color="#fff" /></span>
                <div><strong>Video Prewedding</strong><small>Durasi 2:34 · Ditonton 1,2rb kali</small></div>
                <Lucide icon={ic.chevronRight} size={18} color="#6d7588" />
              </div>
            )}
          </section>
        )}

        <section className={s.section} aria-labelledby="mp-events">
          <div className={s.sectionHead}><h2 id="mp-events">Detail Pengiriman Doa</h2></div>
          {data.events.map((event, index) => (
            <article key={event.name + index} className={s.event}>
              <span className={s.eventIcon}><Lucide icon={index === 0 ? ic.moon : ic.partyPopper} size={18} color="#00aa5b" /></span>
              <div className={s.eventInfo}>
                <div className={s.eventTop}><strong>{event.name}</strong><em>Gratis Ongkir</em></div>
                <b>{event.time}</b>
                <span>{event.venue}</span>
                {(event.address ?? formatDate(event.date)) && <small>{event.address ?? formatDate(event.date)}</small>}
              </div>
            </article>
          ))}
          {mapsHref(data, data.events[data.events.length - 1]) && (
            <a className={s.outlineBtn} href={mapsHref(data, data.events[data.events.length - 1])} target="_blank" rel="noreferrer">
              <Lucide icon={ic.mapPin} color="#00aa5b" />Lacak Lokasi di Maps
            </a>
          )}
        </section>

        {(demo || data.gifts.length > 0) && (
          <section className={s.section} aria-labelledby="mp-gift">
            <div className={s.sectionHead}><h2 id="mp-gift">{demo ? "Wishlist Kado" : "Kirim Kado"}</h2>{demo && <span>Lihat Semua</span>}</div>
            {demo && (
              <div className={s.wishlist}>
                {[
                  { name: "Mesin Kopi Espresso", price: "Rp2.499.000", was: "Rp3.200.000", icon: ic.coffee, bg: "#fff3e8" },
                  { name: "Sprei Katun Premium", price: "Rp689.000", was: "Rp899.000", icon: ic.bedDouble, bg: "#e5f7ee" },
                  { name: "Set Panci Keramik", price: "Rp1.150.000", was: "Rp1.450.000", icon: ic.cookingPot, bg: "#feecef" },
                ].map(item => (
                  <div key={item.name} className={s.product}>
                    <div className={s.productImg} style={{ background: item.bg }}><Lucide icon={item.icon} size={36} color="#212121" /></div>
                    <div className={s.productInfo}><span>{item.name}</span><strong>{item.price}</strong><div><em>-22%</em><s>{item.was}</s></div></div>
                  </div>
                ))}
              </div>
            )}
            {data.gifts.map(gift => {
              const info = giftInfo(gift);
              return (
                <div key={gift.id} className={s.amplop}>
                  <span className={s.amplopIcon}><Lucide icon={ic.wallet} size={20} color="#fff" /></span>
                  <div>
                    <strong>{gift.type === "address" ? "Kirim Kado" : "Amplop Digital"}</strong>
                    <small>{[info.title !== "Alamat kado" ? info.title : "", info.number, info.holder ? `a.n. ${info.holder}` : ""].filter(Boolean).join(" · ")}</small>
                  </div>
                  {info.copy && <button type="button" className={s.copy} onClick={() => copy(info.copy)}>{copied === info.copy ? "Tersalin" : "Salin"}</button>}
                </div>
              );
            })}
          </section>
        )}

        <section className={s.section} aria-labelledby="mp-wishes">
          <div className={s.sectionHead}>
            <h2 id="mp-wishes">Ulasan Tamu</h2>
            <span>{demo ? "248 ulasan" : `${wishes.wishes.length} ulasan`}</span>
          </div>
          {demo && (
            <div className={s.summary}>
              <div className={s.score}><div><span className={s.star}>★</span><b>5.0</b></div><small>100% tamu bahagia</small></div>
              <div className={s.bars}>
                {[["Hadir", 86], ["Ragu", 9], ["Berhalangan", 5]].map(([label, pct]) => (
                  <div key={label} className={s.barRow}><span>{label}</span><i><b style={{ width: `${pct}%` }} /></i>{pct}%</div>
                ))}
              </div>
            </div>
          )}
          {wishes.wishes.length === 0 && <p className={s.empty}>Belum ada ulasan. Jadilah yang pertama mengirim ucapan!</p>}
          {wishes.wishes.slice(0, 6).map(wish => (
            <article key={wish.id} className={s.review}>
              <div className={s.reviewHead}><span aria-hidden>{wish.name.slice(0, 1).toUpperCase()}</span><strong>{wish.name}</strong><small>{timeAgo(wish.created_at)}</small></div>
              <div className={s.stars} aria-label="5 bintang">★★★★★</div>
              <p>{wish.message}</p>
            </article>
          ))}
        </section>

        <footer className={s.footerNote}>
          <p>Merupakan suatu kehormatan apabila Bapak/Ibu/Saudara/i berkenan hadir.</p>
          <a href="/" target="_blank" rel="noreferrer">dibuat dengan ♥ di Rawuh</a>
        </footer>
      </main>

      <nav className={s.bottom} aria-label="Aksi undangan">
        <button type="button" className={s.chatBtn} onClick={sheets.openWish} aria-label="Kirim ucapan"><Lucide icon={ic.messageSquareHeart} size={20} color="#212121" /></button>
        <button type="button" className={s.ghostBtn} onClick={sheets.openWish}>+ Kirim Ucapan</button>
        <button type="button" className={s.solidBtn} onClick={sheets.openRsvp}>Konfirmasi Hadir</button>
      </nav>

      <Sheet open={sheets.sheet === "rsvp"} onClose={sheets.close} title="Konfirmasi Kehadiran" tint={tint}>
        <RsvpForm rsvp={rsvp} guestName={data.guestName} demo={demo} labels={{ submit: "Checkout Kehadiran" }} />
      </Sheet>
      <Sheet open={sheets.sheet === "wish"} onClose={sheets.close} title="Tulis Ulasan & Doa" tint={tint}>
        <WishForm wishes={wishes} guestName={data.guestName} demo={demo} />
      </Sheet>
    </ThemeShell>
  );
}
