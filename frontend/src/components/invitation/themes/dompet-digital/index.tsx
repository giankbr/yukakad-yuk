"use client";
// Theme "Dompet Digital" — undangan bergaya bukti transfer e-wallet (design: Dompet Cinta, Nisa & Fajar).
import { useState } from "react";
import {
  Extras, Lucide, Photo, RsvpForm, Sheet, ThemeShell, WishForm, coupleLabel, dateParts, formatDate, giftInfo, guestLabel,
  mapsHref, storyItems, toDate, useCopy, useRsvp, useSheets, useWishes, type ThemeProps, type ThemeTint,
} from "../kit";
import { ic } from "./icons";
import s from "./styles.module.css";

const FONTS = ["Inter:wght@400;600;700;800"];
const tint: ThemeTint = {
  "--t-accent": "#108ee9", "--t-accent-ink": "#ffffff", "--t-bg": "#ffffff", "--t-ink": "#20232a", "--t-muted": "#78808c", "--t-line": "#dde5ee",
  "--t-field": "#f2f5f9", "--t-radius": "12px", "--t-font": "'Inter', system-ui, sans-serif",
};
const DEMO_WISHES = [
  { id: "w1", name: "Bu Farida", message: "Barakallah Nisa & Fajar! Transferan doa sudah dikirim, hadir pasti." },
  { id: "w2", name: "Mas Didit", message: "Saldo kebahagiaan kalian jangan sampai limit ya. Selamat!" },
];
const DEMO_AMOUNTS = ["+100 simpati", "+1.000 yakin"];
const DEMO_CAPTIONS = ["Kajian pertama", "Kencan halal", "Lamaran"];
const DEMO_WISHLIST = [
  { name: "Mesin Cuci 2 Tabung", price: "Rp2.350.000", icon: ic.washingMachine },
  { name: "Kulkas Mini Duo", price: "Rp1.750.000", icon: ic.refrigerator },
];
const BADGES = ["+1 doa tulus", "+1 restu"];
const TAGS = ["WAJIB HADIR", "JANGAN TELAT"];


function city(address: string) {
  const parts = address.split(",").map(part => part.trim()).filter(Boolean);
  return parts[parts.length - 1] ?? "";
}

const initial = (name: string) => (name.trim().replace(/^(bu|ibu|pak|bapak|bpk\.?|mas|mbak|kak|om|tante)\s+/i, "").slice(0, 1) || "?").toUpperCase();

const icsText = (value: string) => value.replace(/([,;\\])/g, "\\$1").replace(/\n/g, "\\n");

export default function DompetDigitalTheme({ data, slug, guestToken, demo, skipCover }: ThemeProps) {
  const couple = coupleLabel(data);
  const parts = dateParts(data.date);
  const date = toDate(data.date);
  const mm = date ? new Intl.DateTimeFormat("id-ID", { timeZone: "Asia/Jakarta", month: "2-digit" }).format(date) : "";
  const dd = parts.day.padStart(2, "0");
  const clock = parts.day ? `${dd}:${mm}` : "20:02";
  const where = city(data.address) || data.place;
  const code = (where.replace(/[^a-z]/gi, "").replace(/(?!^)[aeiou]/gi, "").slice(0, 3) || "RWH").toUpperCase();
  const reference = parts.day ? `NIKAH-${dd}${mm}${parts.year}-${code}` : `NIKAH-${code}`;
  const label = data.eventLabel ?? "Pernikahan";
  const shortDate = formatDate(data.date, { weekday: "long", day: "numeric", month: "short", year: "numeric" });
  const rsvp = useRsvp({ slug, guestToken, demo });
  const wishes = useWishes({ slug, guestToken, demo, seed: DEMO_WISHES });
  const sheets = useSheets();
  const { copy, copied } = useCopy();
  const [hidden, setHidden] = useState(false);
  const stories = storyItems(data);
  const people = [
    { name: data.couple.brideFull ?? data.couple.bride, parents: data.couple.brideParents, photo: data.couple.bridePhoto ?? data.gallery[0] },
    { name: data.couple.groomFull ?? data.couple.groom, parents: data.couple.groomParents, photo: data.couple.groomPhoto ?? data.gallery[1] },
  ];
  const pageUrl = () => `${window.location.origin}${window.location.pathname}`;

  const saveCalendar = () => {
    const start = toDate(data.events[0]?.date ?? data.date);
    if (!start) return;
    const stamp = (value: Date) => value.toISOString().replace(/[-:]/g, "").replace(/\.\d{3}/, "");
    const last = toDate(data.events[data.events.length - 1]?.date) ?? start;
    const body = [
      "BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//Rawuh//Undangan//ID", "BEGIN:VEVENT",
      `UID:${slug}@rawuh`, `DTSTAMP:${stamp(new Date())}`, `DTSTART:${stamp(start)}`, `DTEND:${stamp(new Date(last.getTime() + 3 * 3600e3))}`,
      `SUMMARY:${icsText(`${label} ${couple}`)}`, `LOCATION:${icsText([data.place, data.address].filter(Boolean).join(", "))}`,
      `URL:${pageUrl()}`, "END:VEVENT", "END:VCALENDAR",
    ].join("\r\n");
    const url = URL.createObjectURL(new Blob([body], { type: "text/calendar" }));
    const link = document.createElement("a");
    link.href = url;
    link.download = `undangan-${slug || "rawuh"}.ics`;
    link.click();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  };
  const share = async () => {
    const url = pageUrl();
    if (navigator.share) {
      try { await navigator.share({ title: `${label} ${couple}`, url }); } catch { /* dismissed */ }
    } else {
      void copy(url);
    }
  };

  return (
    <ThemeShell
      fonts={FONTS}
      background="#e6ebf2"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.coverHead}>
            <div className={s.check}>
              <span className={s.checkCircle} aria-hidden><Lucide icon={ic.check} size={36} color="#2bb673" /></span>
              <h1>Transfer Berhasil!</h1>
              <p>{formatDate(data.date, { day: "numeric", month: "short", year: "numeric" })}{parts.day ? ` · ${clock} WIB` : ""}</p>
            </div>
          </div>
          <div className={s.receipt}>
            <div className={s.amount}>
              <small>Nominal Transfer</small>
              <strong>1 Hati, Seumur Hidup</strong>
              <small>biaya admin: ikhlas</small>
            </div>
            <dl className={s.line}><dt>Dari</dt><dd>{data.couple.groomFull ?? data.couple.groom}</dd></dl>
            <dl className={s.line}><dt>Kepada</dt><dd>{data.couple.brideFull ?? data.couple.bride}</dd></dl>
            {data.couple.note && <dl className={s.line}><dt>Berita</dt><dd>&ldquo;{data.couple.note}&rdquo;</dd></dl>}
            <dl className={s.line}><dt>Referensi</dt><dd>{reference}</dd></dl>
            <div className={s.forward}>
              <small>Notifikasi ini diteruskan kepada:</small>
              <h2>{guestLabel(data)}</h2>
              <small>sebagai saksi &amp; tamu undangan {label.toLowerCase()}</small>
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.receipt} size={15} />Lihat Detail — Buka Undangan</button>
          </div>
          <div className={s.share}>
            <button type="button" onClick={saveCalendar} aria-label="Simpan tanggal ke kalender"><Lucide icon={ic.download} size={15} />Simpan</button>
            <button type="button" onClick={share}><Lucide icon={ic.share2} size={15} />{copied ? "Tersalin" : "Bagikan"}</button>
            <button type="button" onClick={() => { open(); sheets.openWish(); }}><Lucide icon={ic.heart} size={15} />Doakan</button>
          </div>
          <p className={s.coverNote}>Transaksi cinta ini dilindungi restu orang tua &amp; doa keluarga</p>
          <div className={s.coverGrow} />
          <div className={s.tabbar} aria-hidden>
            {[["Beranda", ic.house], ["Riwayat", ic.clock3], ["Bayar", ic.scanLine], ["Kado", ic.gift], ["Profil", ic.userRound]].map(([name, icon], index) => (
              <span key={name} className={`${s.tab} ${index === 0 ? s.tabActive : ""}`}><Lucide icon={icon} size={20} />{name}</span>
            ))}
          </div>
        </section>
      )}
    >
      <header className={s.head}>
        <div className={s.hi}>
          <div>
            <h1>Dompet Cinta</h1>
            <p>{[couple, shortDate, where].filter(Boolean).join(" · ")}</p>
          </div>
          <Lucide icon={ic.bell} size={20} />
        </div>
      </header>

      <main className={s.body}>
        <section className={s.saldo} aria-label="Saldo kebahagiaan">
          <div className={s.saldoRow}>
            <div><small>Saldo Kebahagiaan</small><strong>{hidden ? "Rp••••••" : "Rp∞ (tak terhingga)"}</strong></div>
            <button type="button" className={s.eye} onClick={() => setHidden(value => !value)} aria-pressed={hidden} aria-label={hidden ? "Tampilkan saldo" : "Sembunyikan saldo"}>
              <Lucide icon={ic.eye} size={15} color="#78808c" />
            </button>
          </div>
          <nav className={s.menu} aria-label="Menu undangan">
            <a href="#dd-couple"><span><Lucide icon={ic.users} size={20} color="#108ee9" /></span>Mempelai</a>
            <a href="#dd-events"><span><Lucide icon={ic.calendarHeart} size={20} color="#108ee9" /></span>Acara</a>
            <a href="#dd-gallery"><span><Lucide icon={ic.images} size={20} color="#108ee9" /></span>Galeri</a>
            <a href="#dd-gift"><span><Lucide icon={ic.gift} size={20} color="#108ee9" /></span>Kado</a>
          </nav>
        </section>

        <Extras slot="opening" className={s.extras} />

        <section className={s.card} id="dd-couple" aria-labelledby="dd-couple-h">
          <div className={s.cardHead}><h2 id="dd-couple-h">Pemilik Rekening Bersama</h2></div>
          {people.map((person, index) => (
            <div key={index} className={s.owner}>
              <Photo src={person.photo} alt={person.name} className={s.avatar} />
              <div className={s.ownerText}><strong>{person.name}</strong>{person.parents && <small>{person.parents}</small>}</div>
              <span className={s.verified}><Lucide icon={ic.badgeCheck} size={12} />Terverifikasi</span>
            </div>
          ))}
        </section>

        {stories.length > 0 && (
          <section className={s.card} aria-labelledby="dd-story">
            <div className={s.cardHead}><h2 id="dd-story">Riwayat Transaksi Cinta</h2></div>
            <ol className={s.txList}>
              {stories.map((story, index) => {
                const last = index === stories.length - 1 && stories.length > 1;
                return (
                  <li key={story.title + index} className={`${s.tx} ${last ? s.txOut : ""}`}>
                    <span className={s.txIcon} aria-hidden><Lucide icon={last ? ic.arrowUpRight : ic.arrowDownLeft} size={16} color={last ? "#e2574c" : "#2bb673"} /></span>
                    <div className={s.txText}>
                      <strong>{[story.date, story.title].filter(Boolean).join(" · ")}</strong>
                      <small>{story.body}</small>
                      {story.image && <Photo src={story.image} alt={story.title} className={s.txImg} />}
                    </div>
                    <span className={s.txAmt}>{last ? "LUNAS" : demo ? DEMO_AMOUNTS[index % 2] : "Berhasil"}</span>
                  </li>
                );
              })}
            </ol>
          </section>
        )}

        {data.events.length > 0 && (
          <section className={s.card} id="dd-events" aria-labelledby="dd-events-h">
            <div className={s.cardHead}><h2 id="dd-events-h">Tagihan Jatuh Tempo</h2><span>{data.events.length}</span></div>
            {data.events.map((event, index) => {
              const href = mapsHref(data, event);
              const place = [event.venue, event.address].filter(Boolean).join(", ");
              return (
                <article key={event.name + index} className={s.bill}>
                  <span className={s.billIcon} aria-hidden><Lucide icon={ic.calendarHeart} size={18} color="#108ee9" /></span>
                  <div className={s.billText}>
                    <div className={s.billTitle}><strong>{event.name}</strong><em>{TAGS[Math.min(index, 1)]}</em></div>
                    <small>
                      {[formatDate(event.date, { weekday: "long", day: "numeric", month: "short", year: "numeric" }), event.time].filter(Boolean).join(" · ")}
                      {place && <> · {href ? <a href={href} target="_blank" rel="noreferrer">{place}</a> : place}</>}
                    </small>
                  </div>
                  <button type="button" className={s.payBtn} onClick={sheets.openRsvp} aria-label={`Konfirmasi hadir di ${event.name}`}>Bayar</button>
                </article>
              );
            })}
          </section>
        )}

        <Extras slot="event" className={s.extras} />

        {data.gallery.length > 0 && (
          <section className={s.card} id="dd-gallery" aria-labelledby="dd-gallery-h">
            <div className={s.cardHead}><h2 id="dd-gallery-h">Voucher Kenangan</h2><span>{data.gallery.length} foto</span></div>
            <div className={s.vouchers}>
              {data.gallery.map((src, index) => (
                <figure key={src + index} className={s.voucher}>
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
          <section className={s.card} id="dd-gift" aria-labelledby="dd-gift-h">
            <div className={s.cardHead}><h2 id="dd-gift-h">Kirim Kado</h2>{demo && <span>Wishlist</span>}</div>
            {demo && (
              <>
                <div className={s.tiers} aria-hidden>
                  {["Rp100rb", "Rp500rb", "Rp1jt", "Lainnya"].map((tier, index) => <span key={tier} className={index === 1 ? s.tierOn : undefined}>{tier}</span>)}
                </div>
                {DEMO_WISHLIST.map(item => (
                  <div key={item.name} className={s.wishItem}>
                    <span className={s.wishIcon}><Lucide icon={item.icon} size={17} color="#108ee9" /></span>
                    <div><strong>{item.name}</strong><small>{item.price}</small></div>
                    <button type="button" className={s.ghostBtn} onClick={sheets.openWish}>Beri</button>
                  </div>
                ))}
              </>
            )}
            {data.gifts.map(gift => {
              const info = giftInfo(gift);
              const number = gift.type === "bank" ? `${info.title} ${info.number}` : info.number;
              return (
                <div key={gift.id} className={s.amplop}>
                  <Lucide icon={ic.wallet} size={17} />
                  <div>
                    <strong>{gift.type === "address" ? "Kirim Kado" : "Amplop Digital"}</strong>
                    <small>{[number, info.holder ? `a.n. ${info.holder}` : ""].filter(Boolean).join(" · ")}</small>
                    {info.image && <Photo src={info.image} alt="Kode QRIS" className={s.qris} />}
                  </div>
                  {info.copy && <button type="button" className={s.copyBtn} onClick={() => copy(info.copy)}>{copied === info.copy ? "Tersalin" : "Salin"}</button>}
                </div>
              );
            })}
          </section>
        )}

        <section className={s.card} aria-labelledby="dd-wishes">
          <div className={s.cardHead}><h2 id="dd-wishes">Ucapan Masuk</h2><span>{demo ? "248" : wishes.wishes.length}</span></div>
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
        <button type="button" className={s.scanBtn} onClick={sheets.openWish} aria-label="Kirim ucapan"><Lucide icon={ic.scanLine} size={18} color="#108ee9" /></button>
        <button type="button" className={s.rsvpBtn} onClick={sheets.openRsvp}><Lucide icon={ic.check} />Bayar Kehadiran — Konfirmasi</button>
      </nav>

      <Sheet open={sheets.sheet === "rsvp"} onClose={sheets.close} title="Konfirmasi Kehadiran" tint={tint}>
        <RsvpForm rsvp={rsvp} guestName={data.guestName} demo={demo} labels={{ submit: "Bayar Kehadiran", success: "Pembayaran berhasil!" }} />
      </Sheet>
      <Sheet open={sheets.sheet === "wish"} onClose={sheets.close} title="Kirim Doa & Ucapan" tint={tint}>
        <WishForm wishes={wishes} guestName={data.guestName} demo={demo} submitLabel="Kirim Doa" />
      </Sheet>
    </ThemeShell>
  );
}
