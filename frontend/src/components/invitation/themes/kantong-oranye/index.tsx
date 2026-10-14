"use client";
// Theme "Kantong Oranye" — undangan bergaya aplikasi tabungan/kantong bersama (design: Kantong Bersama, Dion & Salsa).
import {
  Lucide, Photo, RsvpForm, Sheet, ThemeShell, WishForm, formatDate, giftInfo, guestLabel,
  mapsHref, storyItems, useCopy, useCountdown, useRsvp, useSheets, useWishes, type ThemeProps, type ThemeTint,
} from "../kit";
import { ic } from "./icons";
import s from "./styles.module.css";

const FONTS = ["DM Sans:wght@400;500;600;700;800"];
const tint: ThemeTint = {
  "--t-accent": "#1a1a1a", "--t-bg": "#fbf8f1", "--t-ink": "#1a1a1a", "--t-muted": "#6f6a62", "--t-line": "#ede6d6",
  "--t-field": "#ffffff", "--t-radius": "14px", "--t-font": "'DM Sans', system-ui, sans-serif",
};
const DEMO_WISHES = [
  { id: "w1", name: "Pak Rahmat", message: "Bunga-berbunga kebahagiaan. Kami sekeluarga ikut setor doa!", created_at: new Date(Date.now() - 2 * 3600e3).toISOString() },
  { id: "w2", name: "Mbak Dara", message: "Dari bootcamp sampai pelaminan. Investasi terbaik kalian!", created_at: new Date(Date.now() - 5 * 3600e3).toISOString() },
];
const DEMO_CAPTIONS = ["Setoran awal", "Nabung receh", "Kantong dikunci"];
const DEMO_WISHLIST = [
  { name: "Kantong: Mesin Cuci", note: "terkumpul 70% dari Rp2.400.000", pct: 70, icon: ic.washingMachine },
  { name: "Kantong: Kasur Baru", note: "terkumpul 45% dari Rp3.000.000", pct: 45, icon: ic.bedDouble },
];
const POCKETS = [
  { bg: "#f8a91b", ink: "#1a1a1a", icon: ic.moonStar },
  { bg: "#d9a3e6", ink: "#1a1a1a", icon: ic.partyPopper },
  { bg: "#5ea9cc", ink: "#ffffff", icon: ic.plane },
];
const YEAR_BG = ["#fdf0d2", "#fbefcb", "#e8f7ee"];
const NAV = [
  { label: "Beranda", icon: ic.landmark }, { label: "Kantong", icon: ic.wallet, active: true },
  { label: "Transaksi", icon: ic.arrowLeftRight }, { label: "Kartu", icon: ic.creditCard }, { label: "Lainnya", icon: ic.ellipsis },
];

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

export default function KantongOranyeTheme({ data, slug, guestToken, demo, skipCover }: ThemeProps) {
  const { bride, groom } = data.couple;
  const couple = `${groom} & ${bride}`;
  const dd = formatDate(data.date, { day: "2-digit" });
  const mm = formatDate(data.date, { month: "2-digit" });
  const clock = /^\d+$/.test(dd) && /^\d+$/.test(mm) ? `${dd}:${mm}` : "09:41";
  const longDate = formatDate(data.date);
  const midDate = formatDate(data.date, { weekday: "long", day: "numeric", month: "short", year: "numeric" });
  const where = city(data.address) || data.place;
  const countdown = useCountdown(data.date);
  // Progress over the final year before the day (derived from the date, not invented).
  const pct = demo ? 86 : countdown.ready ? Math.min(100, Math.max(1, Math.round(100 - Number(countdown.days) / 3.65))) : 0;

  const rsvp = useRsvp({ slug, guestToken, demo });
  const wishes = useWishes({ slug, guestToken, demo, seed: DEMO_WISHES });
  const sheets = useSheets();
  const { copy, copied } = useCopy();
  const stories = storyItems(data);
  const since = stories.find(story => story.date)?.date?.match(/\d{4}/)?.[0];
  const lastYear = [...stories].reverse().find(story => story.date)?.date?.match(/\d{4}/)?.[0];
  const gallery = data.gallery;
  const people = [
    { name: data.couple.groomFull ?? groom, parents: data.couple.groomParents, photo: data.couple.groomPhoto ?? gallery[1], role: "Si rajin nabung" },
    { name: data.couple.brideFull ?? bride, parents: data.couple.brideParents, photo: data.couple.bridePhoto ?? gallery[2], role: "Si penjaga kunci" },
  ];
  const pockets = [
    ...data.events.map(event => ({ label: event.name.split(" ")[0], value: "100%" })),
    ...(data.events.length < 3 ? [{ label: "Bulan Madu", value: demo ? "62%" : "Segera" }] : []),
  ];

  return (
    <ThemeShell
      fonts={FONTS}
      background="#efe9dc"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.coverHead}>
            <Status time={clock} />
            <div className={s.notif}>
              <span className={s.appIcon} aria-hidden><Lucide icon={ic.piggyBank} size={30} color="#f8a91b" /></span>
              <h1>Kantong Baru Dibuat!</h1>
              <p>{couple} membuat kantong bersama</p>
            </div>
          </div>
          <div className={s.coverBody}>
            <div className={s.mainPocket}>
              <div className={s.row}>
                <span className={s.houseIcon} aria-hidden><Lucide icon={ic.house} size={22} color="#1a1a1a" /></span>
                <div className={s.grow}>
                  <strong className={s.mpTitle}>Kantong Rumah Tangga</strong>
                  <small className={s.muted11}>{lastYear ? `Dibuat ${lastYear} · ` : ""}anggota: 2 orang</small>
                </div>
                <span className={s.locked}>Terkunci</span>
              </div>
              <div className={s.prog}>
                <div className={s.progRow}><span>Progres menuju hari H</span><b>{pct}%</b></div>
                <div className={s.bar} role="progressbar" aria-valuenow={pct} aria-valuemin={0} aria-valuemax={100} aria-label="Progres menuju hari H"><i style={{ width: `${pct}%` }} /></div>
              </div>
              <p className={s.target}>Target cair: {longDate}{where ? ` · ${where}` : ""}</p>
            </div>
            <div className={s.kepada}>
              <span className={s.kicker}><Lucide icon={ic.userPlus} size={14} color="#f8a91b" />Undangan Gabung Kantong</span>
              <strong>{guestLabel(data)}</strong>
              <p>Diundang sebagai saksi kebahagiaan — tanpa biaya admin.</p>
            </div>
            <div className={s.pockets}>
              {pockets.map((pocket, index) => {
                const look = POCKETS[index % POCKETS.length];
                return (
                  <div key={pocket.label + index} className={s.pocket} style={{ background: look.bg, color: look.ink }}>
                    <span aria-hidden><Lucide icon={look.icon} color={look.ink} /></span>
                    <strong>{pocket.label}</strong>
                    <small>{pocket.value}</small>
                  </div>
                );
              })}
            </div>
            <button type="button" className={s.dark} onClick={open}><Lucide icon={ic.piggyBank} size={17} color="#fff" />Gabung Kantong — Buka Undangan</button>
            <p className={s.coverNote}>{since ? `Menabung cinta sejak ${since}, bunganya kebahagiaan.` : "Menabung cinta, bunganya kebahagiaan."}</p>
          </div>
          <div className={s.tabbar} aria-hidden>
            {NAV.map(item => (
              <span key={item.label} className={item.active ? s.tabActive : undefined}>
                <Lucide icon={item.icon} size={22} color={item.active ? "#f8a91b" : "#6f6a62"} />{item.label}
              </span>
            ))}
          </div>
        </section>
      )}
    >
      <header className={s.top}>
        <Status time={clock} />
        <div className={s.nav}>
          <div className={s.grow}>
            <h1>Kantong Bersama</h1>
            <p>{couple} · {midDate}{where ? ` · ${where}` : ""}</p>
          </div>
          <span className={s.mono} aria-hidden>{groom.slice(0, 1).toUpperCase()}♥{bride.slice(0, 1).toUpperCase()}</span>
        </div>
      </header>

      <main className={s.body}>
        <section className={s.card} aria-labelledby="ko-members">
          <div className={s.head}><h2 id="ko-members">Anggota Kantong</h2></div>
          {people.map(person => (
            <article key={person.name} className={s.row}>
              <Photo src={person.photo} alt={person.name} className={s.avatar} />
              <div className={s.grow}>
                <strong className={s.t14}>{person.name}</strong>
                {person.parents && <small className={s.muted11}>{person.parents}</small>}
              </div>
              <span className={s.role}>{person.role}</span>
            </article>
          ))}
        </section>

        {stories.length > 0 && (
          <section className={s.card} aria-labelledby="ko-story">
            <div className={s.head}><h2 id="ko-story">Riwayat Kantong</h2><span aria-hidden>Semua</span></div>
            <ol className={s.list}>
              {stories.map((story, index) => (
                <li key={story.title + index} className={s.story}>
                  {story.date && <span className={s.year} style={{ background: YEAR_BG[index % YEAR_BG.length] }}>{story.date}</span>}
                  <div className={s.grow}>
                    <strong>{story.title}</strong>
                    <p>{story.body}</p>
                    {story.image && <Photo src={story.image} alt={story.title} className={s.storyImg} />}
                  </div>
                </li>
              ))}
            </ol>
          </section>
        )}

        <section className={s.card} aria-labelledby="ko-events">
          <div className={s.head}><h2 id="ko-events">Jadwal Pencairan</h2></div>
          {data.events.map((event, index) => {
            const href = mapsHref(data, event);
            return (
              <article key={event.name + index} className={s.event}>
                <span className={s.evIcon} aria-hidden><Lucide icon={ic.calendarCheck} size={18} color="#f8a91b" /></span>
                <div className={s.grow}>
                  <strong>{event.name}{event.date ? ` · ${formatDate(event.date, { weekday: "long", day: "numeric", month: "short", year: "numeric" })}` : ""}</strong>
                  <small className={s.muted11}>{[event.time, event.venue].filter(Boolean).join(" · ")}</small>
                </div>
                {href && <a className={s.route} href={href} target="_blank" rel="noreferrer" aria-label={`Rute ke ${event.venue}`}>Rute</a>}
              </article>
            );
          })}
        </section>

        {gallery.length > 0 && (
          <section className={s.card} aria-labelledby="ko-gallery">
            <div className={s.head}><h2 id="ko-gallery">Galeri Tabungan Momen</h2><span>{gallery.length}</span></div>
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
          <section className={s.card} aria-labelledby="ko-gift">
            <div className={s.head}><h2 id="ko-gift">Top Up Kantong Kado</h2>{demo && <span>Wishlist</span>}</div>
            {demo && (
              <>
                <div className={s.tiers} aria-hidden>
                  {["Rp100rb", "Rp300rb", "Rp1jt", "Bebas"].map((tier, index) => <span key={tier} className={index === 1 ? s.tierOn : undefined}>{tier}</span>)}
                </div>
                {DEMO_WISHLIST.map(item => (
                  <div key={item.name} className={s.wish}>
                    <div className={s.row}>
                      <span className={s.wIcon} aria-hidden><Lucide icon={item.icon} color="#f8a91b" /></span>
                      <div className={s.grow}><strong>{item.name}</strong><small className={s.muted11}>{item.note}</small></div>
                      <span className={s.isi} aria-hidden>Isi</span>
                    </div>
                    <div className={s.barSm}><i style={{ width: `${item.pct}%` }} /></div>
                  </div>
                ))}
              </>
            )}
            {data.gifts.map(gift => {
              const info = giftInfo(gift);
              return (
                <div key={gift.id} className={s.amplop}>
                  <Lucide icon={ic.wallet} size={17} color="#f7c94b" />
                  <div className={s.grow}>
                    <strong>{gift.type === "address" ? "Alamat Kirim Kado" : gift.type === "qris" ? "QRIS Kantong" : "Nomor Kantong Digital"}</strong>
                    <small>{[gift.type === "bank" || gift.type === "ewallet" ? info.title : "", info.number, info.holder ? `a.n. ${info.holder}` : ""].filter(Boolean).join(" · ")}</small>
                    {info.image && <Photo src={info.image} alt="Kode QRIS" className={s.qris} />}
                  </div>
                  {info.copy && <button type="button" className={s.isi} onClick={() => copy(info.copy)}>{copied === info.copy ? "Tersalin" : "Salin"}</button>}
                </div>
              );
            })}
          </section>
        )}

        <section className={s.card} aria-labelledby="ko-wishes">
          <div className={s.head}><h2 id="ko-wishes">Catatan Anggota</h2><span>{demo ? "248" : wishes.wishes.length}</span></div>
          {wishes.wishes.length === 0 && <p className={s.empty}>Belum ada catatan. Jadilah yang pertama setor doa!</p>}
          {wishes.wishes.slice(0, 8).map(wish => (
            <article key={wish.id} className={s.note}>
              <span className={s.initial} aria-hidden>{(wish.name.trim().split(/\s+/).pop() ?? wish.name).slice(0, 1).toUpperCase()}</span>
              <div className={s.grow}><strong>{wish.name}</strong><p>{wish.message}</p></div>
            </article>
          ))}
        </section>
      </main>

      <nav className={s.bottom} aria-label="Aksi undangan">
        <button type="button" className={s.chat} onClick={sheets.openWish} aria-label="Kirim ucapan"><Lucide icon={ic.messageCircle} size={18} color="#f8a91b" /></button>
        <button type="button" className={s.dark} onClick={sheets.openRsvp}><Lucide icon={ic.piggyBank} color="#fff" />Setor Kehadiran — Hadir</button>
      </nav>

      <Sheet open={sheets.sheet === "rsvp"} onClose={sheets.close} title="Setor Kehadiran" tint={tint}>
        <RsvpForm rsvp={rsvp} guestName={data.guestName} demo={demo} labels={{ submit: "Setor Kehadiran" }} />
      </Sheet>
      <Sheet open={sheets.sheet === "wish"} onClose={sheets.close} title="Tulis Catatan & Doa" tint={tint}>
        <WishForm wishes={wishes} guestName={data.guestName} demo={demo} />
      </Sheet>
    </ThemeShell>
  );
}
