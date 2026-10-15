"use client";
// Theme "Oranye" — undangan bergaya aplikasi belanja oranye (design: Undangan — Tema Oranye (Dewi & Arya)).
import { useState, type CSSProperties } from "react";
import { toast } from "@/lib/celebrate";
import {
  Extras, Lucide, Photo, RsvpForm, Sheet, ThemeShell, Tick, WishForm, coupleLabel, dateParts, formatDate, giftInfo, guestLabel,
  mapsHref, storyItems, useCopy, useCountdown, useRsvp, useSheets, useWishes, type Attendance, type ThemeProps, type ThemeTint,
} from "../kit";
import { ic } from "./icons";
import s from "./styles.module.css";

const FONTS = ["Roboto:wght@400;500;700;900"];
const tint: ThemeTint = {
  "--t-accent": "#ee4d2d", "--t-bg": "#ffffff", "--t-ink": "#222222", "--t-muted": "#757575", "--t-line": "#f0f0f0",
  "--t-field": "#f5f5f5", "--t-radius": "4px", "--t-font": "Roboto, system-ui, sans-serif",
};
const DEMO_WISHES = [
  { id: "w1", name: "Rizky", attendance: "yes" as Attendance, message: "Selamat Dewi & Arya! Seller-nya ramah, pengiriman doa tepat waktu. Semoga samawa sampai kakek-nenek!", created_at: new Date(Date.now() - 2 * 3600e3).toISOString() },
  { id: "w2", name: "Tante Mira", attendance: "yes" as Attendance, message: "Barang sesuai deskripsi: pasangan serasi 100%. Bintang lima tanpa ragu.", created_at: new Date(Date.now() - 6 * 3600e3).toISOString() },
];
const DEMO_SEATS = [
  { name: "Kursi Akad", sub: "50 kursi", icon: ic.armchair, pct: 81, label: "SEGERA HABIS" },
  { name: "Kursi Resepsi", sub: "400 kursi", icon: ic.armchair, pct: 59, label: "TERSISA 152" },
  { name: "Meja VIP", sub: "12 meja", icon: ic.crown, pct: 38, label: "TERSISA 7" },
];
const DEMO_FEED = [["Pagi di Lembang", "2,1rb suka"], ["Jalan-jalan Braga", "1,3rb suka"], ["Kencan Pertama", "845 suka"], ["Senja Ciwidey", "3rb suka"]];
const ATTEND: Record<Attendance, string> = { yes: "Hadir", maybe: "Ragu", no: "Berhalangan" };
const pad = (n: number) => String(n).padStart(2, "0");


function city(address: string) {
  const parts = address.split(",").map(part => part.trim()).filter(Boolean);
  return parts.length > 1 ? parts[parts.length - 1] : "";
}

/** Story body → chat bubbles. Lines "Nama: pesan" pick the sender; other lines alternate. */
function chatLines(body: string, bride: string, groom: string, start: number) {
  let turn = start;
  return body.split(/\n+/).map(line => line.trim()).filter(Boolean).map(line => {
    const match = /^([^:]{1,40}):\s*(.+)$/.exec(line);
    const who = match?.[1].trim().toLowerCase();
    if (match && (who === bride.toLowerCase() || who === groom.toLowerCase())) {
      const fromGroom = who === groom.toLowerCase();
      turn = fromGroom ? 0 : 1;
      return { fromGroom, name: fromGroom ? groom : bride, text: match[2] };
    }
    const fromGroom = turn % 2 === 1;
    turn += 1;
    return { fromGroom, name: fromGroom ? groom : bride, text: line };
  });
}

export default function OranyeTheme({ data, slug, guestToken, demo, skipCover }: ThemeProps) {
  const couple = coupleLabel(data);
  const parts = dateParts(data.date);
  const date = new Date(data.date);
  const valid = !Number.isNaN(date.getTime()) && !!parts.day;
  const month = valid ? pad(Number(new Intl.DateTimeFormat("en", { timeZone: "Asia/Jakarta", month: "numeric" }).format(date))) : "";
  const code = valid ? `${pad(Number(parts.day))}.${month}` : "";
  const longDate = formatDate(data.date);
  const where = city(data.address);
  const countdown = useCountdown(data.date);
  const rsvp = useRsvp({ slug, guestToken, demo });
  const wishes = useWishes({ slug, guestToken, demo, seed: DEMO_WISHES });
  const sheets = useSheets();
  const { copy, copied } = useCopy();
  const [allWishes, setAllWishes] = useState(false);
  const [hearts, setHearts] = useState<string[]>([]);
  const [filter, setFilter] = useState(0);
  const toggleHeart = (key: string, label: string) => {
    const on = !hearts.includes(key);
    setHearts(h => (on ? [...h, key] : h.filter(k => k !== key)));
    if (on) toast(label);
  };
  const stories = storyItems(data);
  const hero = data.gallery[0];
  const feed = data.gallery.length > 1 ? data.gallery.slice(1) : data.gallery;
  const cols = [feed.map((src, i) => ({ src, i })).filter(x => x.i % 2 === 0), feed.map((src, i) => ({ src, i })).filter(x => x.i % 2 === 1)];
  const label = data.eventLabel ?? "Pernikahan";
  const sale = `${/^pernikahan$/i.test(label) ? "WEDDING" : label.toUpperCase()} DAY SALE`;
  const firstEvent = data.events[0]?.name.split(" ")[0]?.toLowerCase();
  const seats = demo ? DEMO_SEATS : data.events.slice(0, 3).map((event, index) => ({
    name: event.name, sub: event.time, icon: index === 0 ? ic.armchair : ic.crown, pct: 100, label: "AMANKAN KURSI",
  }));
  const shownWishes = allWishes ? wishes.wishes : wishes.wishes.slice(0, 3);
  const chatGroups = stories.reduce<{ turn: number; groups: Array<{ story: (typeof stories)[number]; lines: ReturnType<typeof chatLines> }> }>((acc, story) => {
    const lines = chatLines(story.body, data.couple.bride, data.couple.groom, acc.turn);
    return { turn: acc.turn + lines.length, groups: [...acc.groups, { story, lines }] };
  }, { turn: 0, groups: [] }).groups;

  return (
    <ThemeShell
      fonts={FONTS}
      background="#ececec"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.coverBg} aria-hidden><Photo src={hero} /></div>
          <div className={s.coverTop}>
            <span className={s.saleBadge}><Lucide icon={ic.zap} size={14} color="#ee4d2d" />{code ? `${code} ` : ""}{sale}</span>
          </div>
          <div className={s.spacer} />
          <div className={s.coverContent}>
            <div className={s.coverNames}>
              <span>Undangan {label}</span>
              <h1>{couple}</h1>
              <p>{longDate}</p>
            </div>
            <div className={s.coverVoucher}>
              <div className={s.cvLeft}>
                <span className={s.cvIcon}><Lucide icon={ic.ticket} size={22} color="#fff" /></span>
                <b>VOUCHER</b><b>KEHADIRAN</b>
              </div>
              <div className={s.cvRight}>
                <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
                <strong>{guestLabel(data)}</strong>
                <div className={s.cvRow}><span className={s.outlineTag}>Khusus Untukmu</span><small>Di tempat</small></div>
                {valid && <div className={s.cvExp}><Lucide icon={ic.timer} size={11} color="#757575" />Berlaku s/d {code}.{parts.year}</div>}
              </div>
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={18} color="#ee4d2d" />Klaim &amp; Buka Undangan</button>
            <p className={s.coverNote}>Mohon maaf apabila ada kesalahan penulisan nama &amp; gelar.</p>
          </div>
        </section>
      )}
    >
      <header className={s.header}>
        <div className={s.searchRow}>
          <div className={s.search}>
            <Lucide icon={ic.search} color="#757575" />
            <span>{couple}{code ? ` ${code}` : ""}</span>
            <Lucide icon={ic.camera} color="#757575" />
          </div>
          <span className={s.badgeIcon} aria-hidden><Lucide icon={ic.shoppingCart} size={24} color="#fff" /><b>1</b></span>
          <button type="button" className={s.badgeIcon} onClick={sheets.openWish} aria-label={`Ucapan (${wishes.wishes.length})`}>
            <Lucide icon={ic.messageCircleMore} size={24} color="#fff" /><b>{wishes.wishes.length || 1}</b>
          </button>
        </div>
      </header>

      <main className={s.body}>
        <section className={s.banner} aria-label="Sampul">
          <Photo src={hero} alt={`Foto ${couple}`} />
          <div className={s.bannerOverlay}>
            <div className={s.bigSale}>{code && <b>{code}</b>}<span>{sale}</span></div>
            <h1>{couple}</h1>
            <p>{longDate}{where ? ` · ${where}` : ""}</p>
            <div className={s.dots} aria-hidden><i /><i /><i /><i /><i /></div>
          </div>
        </section>

        <nav className={s.menu} aria-label="Menu undangan">
          {[
            { label: "Mempelai", icon: ic.heartHandshake, bg: "#ffeee8", href: "#or-mempelai" },
            { label: "Kisah", icon: ic.messageCircleHeart, bg: "#fff5e0", href: stories.length ? "#or-kisah" : undefined },
            { label: "Galeri", icon: ic.images, bg: "#e6faf7", href: feed.length ? "#or-galeri" : undefined },
            { label: "Acara", icon: ic.calendarHeart, bg: "#ffeee8", href: "#or-acara" },
            { label: "Kado", icon: ic.gift, bg: "#fff5e0", href: data.gifts.length ? "#or-kado" : undefined },
          ].filter(item => item.href).map(item => (
            <a key={item.label} href={item.href} className={s.menuItem}>
              <span style={{ background: item.bg }}><Lucide icon={item.icon} size={22} color="#ee4d2d" /></span>{item.label}
            </a>
          ))}
          <button type="button" className={s.menuItem} onClick={sheets.openRsvp}>
            <span style={{ background: "#e6faf7" }}><Lucide icon={ic.mailCheck} size={22} color="#ee4d2d" /></span>RSVP
          </button>
        </nav>

        <section className={s.section} aria-labelledby="or-flash">
          <div className={s.flashHead}>
            <h2 id="or-flash" className={s.flashLogo}>F<Lucide icon={ic.zap} size={16} color="#ffd424" style={{ fill: "#ffd424" }} className={s.bolt} />LASH SALE</h2>
            <span className={s.timer} aria-label={`${countdown.days} hari ${countdown.hours} jam ${countdown.minutes} menit lagi`}>
              <Tick className={s.tick} value={countdown.days} />:<Tick className={s.tick} value={countdown.hours} />:<Tick className={s.tick} value={countdown.minutes} />:<Tick className={s.tick} value={countdown.seconds} />
            </span>
            <span className={s.flex} />
            <small>menuju {firstEvent ?? "hari H"}</small>
          </div>
          {seats.length > 0 && (
            <div className={s.seats}>
              {seats.map(seat => (
                <button type="button" key={seat.name} className={s.seat} onClick={sheets.openRsvp} aria-label={`${seat.name} — konfirmasi kehadiran`}>
                  <span className={s.seatImg}><Lucide icon={seat.icon} size={26} color="#ee4d2d" /></span>
                  <strong>{seat.name}</strong>
                  <small>{seat.sub}</small>
                  <span className={s.bar}><i style={{ width: `${seat.pct}%` }} /><b>{seat.label}</b></span>
                </button>
              ))}
            </div>
          )}
        </section>

        <Extras slot="opening" className={s.extras} />

        <section id="or-mempelai" className={s.section} aria-labelledby="or-couple">
          <div className={s.head}><h2 id="or-couple">Mempelai Pilihan</h2><span aria-hidden>Lihat Profil<Lucide icon={ic.chevronRight} size={14} color="#757575" /></span></div>
          <div className={s.coupleRow}>
            {[
              { name: data.couple.brideFull ?? data.couple.bride, parents: data.couple.brideParents, photo: data.couple.bridePhoto ?? data.gallery[1] ?? hero, badge: "Mall", bg: "#d0011b" },
              { name: data.couple.groomFull ?? data.couple.groom, parents: data.couple.groomParents, photo: data.couple.groomPhoto ?? data.gallery[2] ?? hero, badge: "Star+", bg: "#ee4d2d" },
            ].map(person => (
              <article key={person.badge} className={s.card}>
                <div className={s.cardPhoto}>
                  <Photo src={person.photo} alt={person.name} />
                  <span className={s.cardBadge} style={{ background: person.bg }}>{person.badge}</span>
                </div>
                <div className={s.cardInfo}>
                  <strong>{person.name}</strong>
                  {person.parents && <p>{person.parents}</p>}
                  <span className={s.outlineTag}>Cashback Cinta 100%</span>
                  <div className={s.cardBottom}>
                    {demo ? <span><b className={s.star}>★</b>5.0</span> : <span />}
                    <button type="button" className={s.heartBtn} aria-pressed={hearts.includes(person.badge)} aria-label={`Suka ${person.name}`}
                      onClick={() => toggleHeart(person.badge, "Kamu ikut terpikat")}>
                      <Lucide icon={ic.heart} size={13} />{hearts.includes(person.badge) ? 2 : 1} hati
                    </button>
                  </div>
                </div>
              </article>
            ))}
          </div>
        </section>

        {stories.length > 0 && (
          <section id="or-kisah" className={s.section} aria-labelledby="or-story">
            <div className={s.head}><h2 id="or-story">Chat Penjual: Kisah Kami</h2><span aria-hidden>Lihat Semua<Lucide icon={ic.chevronRight} size={14} color="#757575" /></span></div>
            <div className={s.chat}>
              {chatGroups.map(({ story, lines }, index) => {
                return (
                  <div key={index} className={s.chatGroup}>
                    {(story.title || story.date) && <p className={s.pill}>{[story.date, story.title].filter(Boolean).join(" · ")}</p>}
                    {lines.map((line, i) => (
                      <div key={i} className={line.fromGroom ? `${s.msg} ${s.msgMe}` : s.msg} style={{ "--i": Math.min(i, 4) } as CSSProperties}>
                        <div className={s.bubble}><b>{line.name}</b><p>{line.text}</p></div>
                      </div>
                    ))}
                    {story.image && <div className={s.msg}><Photo src={story.image} alt={story.title} className={s.chatImg} /></div>}
                  </div>
                );
              })}
              <div className={s.typing} aria-hidden><span className={s.typingDots}><i /><i /><i /></span>{data.couple.bride} sedang mengetik</div>
            </div>
          </section>
        )}

        <section id="or-acara" className={s.section} aria-labelledby="or-events">
          <div className={s.head}><h2 id="or-events">Klaim Voucher Acara</h2></div>
          {data.events.map((event, index) => {
            const href = mapsHref(data, event);
            return (
              <article key={event.name + index} className={s.voucher}>
                <div className={s.vLeft}>
                  <Lucide icon={index === 0 ? ic.moonStar : ic.partyPopper} size={26} color="#fff" />
                  <b>{(event.name.split(" ")[0] ?? event.name).toUpperCase()}</b>
                </div>
                <div className={s.vRight}>
                  <div className={s.vTop}>
                    <strong>{event.name}</strong>
                    {href && <a href={href} target="_blank" rel="noreferrer" aria-label={`Buka Maps ${event.name}`}>Maps</a>}
                  </div>
                  <em>{event.time}</em>
                  <p>{[event.venue, event.address].filter(Boolean).join(", ")}</p>
                  <small>Berlaku: {formatDate(event.date || data.date, { weekday: "long", day: "numeric", month: "short", year: "numeric" })}</small>
                </div>
              </article>
            );
          })}
        </section>

        <Extras slot="event" className={s.extras} />

        {feed.length > 0 && (
          <section id="or-galeri" className={s.section} aria-labelledby="or-gallery">
            <div className={s.head}><h2 id="or-gallery">Rekomendasi Untukmu · Galeri</h2><span>{demo ? "24" : feed.length} foto<Lucide icon={ic.chevronRight} size={14} color="#757575" /></span></div>
            <div className={s.feed}>
              {cols.map((col, c) => (
                <div key={c} className={s.feedCol}>
                  {col.map(({ src, i }) => {
                    const tall = (Math.floor(i / 2) + c) % 2 === 0;
                    const caption = demo ? DEMO_FEED[i]?.[0] ?? `Momen #${i + 1}` : `Momen #${i + 1}`;
                    return (
                      <figure key={src + i} className={s.product}>
                        <div className={s.productImg} style={{ height: tall ? 220 : 150 }}>
                          <Photo src={src} alt={caption} />
                          {demo && i === 0 && <span className={s.live}><Lucide icon={ic.play} size={10} color="#fff" />VIDEO</span>}
                          <button type="button" className={s.likeBtn} aria-pressed={hearts.includes(`f${i}`)} aria-label={`Suka ${caption}`}
                            onClick={() => toggleHeart(`f${i}`, "Disukai")}><Lucide icon={ic.heart} size={14} /></button>
                        </div>
                        <figcaption>
                          <span>{caption}</span>
                          <div><b>Rp ∞</b>{demo && DEMO_FEED[i] && <small data-on={hearts.includes(`f${i}`) ? "" : undefined}>{hearts.includes(`f${i}`) ? `Kamu & ${DEMO_FEED[i][1]}` : DEMO_FEED[i][1]}</small>}</div>
                        </figcaption>
                      </figure>
                    );
                  })}
                </div>
              ))}
            </div>
          </section>
        )}

        <Extras slot="story" className={s.extras} />

        <Extras slot="end" className={s.extras} />

        {data.gifts.length > 0 && (
          <section id="or-kado" className={s.section} aria-labelledby="or-gift">
            <div className={s.head}><h2 id="or-gift">Kirim Hadiah</h2></div>
            {data.gifts.map(gift => {
              const info = giftInfo(gift);
              if (gift.type === "address") {
                return (
                  <div key={gift.id} className={s.address}>
                    <strong><Lucide icon={ic.mapPin} size={14} color="#ee4d2d" />Alamat Kirim Kado</strong>
                    {gift.account_name && <span>{gift.account_name}</span>}
                    <small>{gift.address}</small>
                    <div className={s.tags}>
                      <span className={s.outlineTag} style={{ color: "#00bfa5", borderColor: "#00bfa5" }}>Gratis Ongkir</span>
                      <span className={s.outlineTag}>COD Cinta</span>
                      {info.copy && <button type="button" className={s.copyText} data-copied={copied === info.copy ? "" : undefined} onClick={() => copy(info.copy)}>{copied === info.copy ? "Tersalin" : "Salin alamat"}</button>}
                    </div>
                  </div>
                );
              }
              return (
                <div key={gift.id} className={s.wallet}>
                  <span className={s.walletIcon}><Lucide icon={ic.wallet} size={20} color="#fff" /></span>
                  <div>
                    <strong>{gift.type === "qris" ? "QRIS" : "Amplop Digital"}</strong>
                    <small>{[`${info.title !== "QRIS" ? info.title : ""} ${info.number}`.trim(), info.holder ? `a.n. ${info.holder}` : ""].filter(Boolean).join(" · ")}</small>
                    {info.image && <Photo src={info.image} alt="Kode QRIS" className={s.qris} />}
                  </div>
                  {info.copy && <button type="button" className={s.copy} data-copied={copied === info.copy ? "" : undefined} onClick={() => copy(info.copy)}>{copied === info.copy ? "Tersalin" : "Salin"}</button>}
                </div>
              );
            })}
          </section>
        )}

        <section className={s.section} aria-labelledby="or-wishes">
          <div className={s.head}>
            <h2 id="or-wishes">Penilaian Tamu</h2>
            {wishes.wishes.length > 3
              ? <button type="button" onClick={() => setAllWishes(v => !v)} aria-expanded={allWishes}>{allWishes ? "Lebih Sedikit" : "Lihat Semua"}<Lucide icon={ic.chevronRight} size={14} color="#757575" /></button>
              : <button type="button" onClick={sheets.openWish}>Tulis Ucapan<Lucide icon={ic.chevronRight} size={14} color="#757575" /></button>}
          </div>
          {demo ? (
            <>
              <div className={s.summary}><b>5.0</b><small>/5</small><span className={s.stars}>★★★★★</span><small>(312 ucapan)</small></div>
              <div className={s.filters} role="group" aria-label="Saring ucapan">
                {["Semua", "Hadir (268)", "Dengan Foto (42)"].map((label, i) => (
                  <button key={label} type="button" aria-pressed={filter === i} onClick={() => setFilter(i)}>{label}</button>
                ))}
              </div>
            </>
          ) : (
            <div className={s.summary}><b>{wishes.wishes.length}</b><small>ucapan &amp; doa</small></div>
          )}
          {wishes.wishes.length === 0 && <p className={s.empty}>Belum ada ucapan. Jadilah yang pertama memberi penilaian!</p>}
          {shownWishes.filter(wish => !(demo && filter === 1) || wish.attendance === "yes").map(wish => (
            <article key={wish.id} className={s.review}>
              <span className={s.avatar} aria-hidden>{wish.name.slice(0, 1).toUpperCase()}</span>
              <div>
                <strong>{wish.name}</strong>
                <span className={s.stars} aria-hidden>{[0, 1, 2, 3, 4].map(i => <i key={i} style={{ animationDelay: `${i * 70}ms` }}>★</i>)}</span>
                {wish.attendance && <small>Kehadiran: {ATTEND[wish.attendance]}{demo ? " · 2 orang" : ""}</small>}
                <p>{wish.message}</p>
              </div>
            </article>
          ))}
        </section>

        <p className={s.footer}>Atas kehadiran &amp; doa restunya, kami ucapkan terima kasih. · <a href="/" target="_blank" rel="noreferrer">dibuat dengan ♥ di Rawuh</a></p>
      </main>

      <nav className={s.bottom} aria-label="Aksi undangan">
        <button type="button" className={s.bottomIcon} onClick={sheets.openWish}><Lucide icon={ic.messageCircleHeart} size={18} color="#fff" />Ucapan</button>
        {data.gifts.length > 0
          ? <a className={`${s.bottomIcon} ${s.bottomSplit}`} href="#or-kado"><Lucide icon={ic.gift} size={18} color="#fff" />Kado</a>
          : <a className={`${s.bottomIcon} ${s.bottomSplit}`} href="#or-acara"><Lucide icon={ic.calendarHeart} size={18} color="#fff" />Acara</a>}
        <button type="button" className={s.bottomCta} onClick={sheets.openRsvp}>Konfirmasi Hadir</button>
      </nav>

      <Sheet open={sheets.sheet === "rsvp"} onClose={sheets.close} title="Konfirmasi Kehadiran" tint={tint}>
        <RsvpForm rsvp={rsvp} guestName={data.guestName} demo={demo} labels={{ submit: "Klaim Kursi Saya" }} />
      </Sheet>
      <Sheet open={sheets.sheet === "wish"} onClose={sheets.close} title="Beri Penilaian & Doa" tint={tint}>
        <WishForm wishes={wishes} guestName={data.guestName} demo={demo} />
      </Sheet>
    </ThemeShell>
  );
}
