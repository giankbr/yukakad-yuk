"use client";
// Theme "Arena Legenda" — undangan bergaya game MOBA (design: Undangan — Tema Arena Legenda (Aldo & Vina)).
import { useState, type CSSProperties } from "react";
import { toast } from "@/lib/celebrate";
import {
  Extras, Lucide, Photo, RsvpForm, Sheet, ThemeShell, Tick, WishForm, dateParts, formatDate, giftInfo, guestLabel,
  mapsHref, storyItems, useCopy, useCountdown, useRsvp, useSheets, useWishes, type ThemeProps, type ThemeTint,
} from "../kit";
import { ic } from "./icons";
import s from "./styles.module.css";

const FONTS = ["Cinzel:wght@400;700", "Exo 2:wght@400;600;700;800"];
const tint: ThemeTint = {
  "--t-accent": "#c9a24b", "--t-accent-ink": "#0a1128", "--t-bg": "#13204a", "--t-ink": "#eaf0ff", "--t-muted": "#8a96b8",
  "--t-line": "rgba(240, 201, 110, .25)", "--t-field": "#0a1128", "--t-radius": "8px", "--t-font": "'Exo 2', system-ui, sans-serif",
};
const DEMO_WISHES = [
  { id: "w1", name: "Riko", message: "gg wp! Selamat Aldo & Vina, duo terkuat musim ini!", created_at: new Date(Date.now() - 2 * 3600e3).toISOString() },
  { id: "w2", name: "Tante Wulan", message: "Selamat ya! Semoga jadi tim yang solid sampai kakek nenek.", created_at: new Date(Date.now() - 4 * 3600e3).toISOString() },
  { id: "w3", name: "Bayu", message: "Akhirnya push rank sampai pelaminan. Hadir dong!", created_at: new Date(Date.now() - 6 * 3600e3).toISOString() },
];
const NAME_COLORS = ["#39c5f3", "#ff6b9c", "#f0c96e"];
const SKINS = ["EPIC", "LEGEND", "STARLIGHT"];
const DEMO_STATS = [
  [["Kesabaran", 92], ["Humor", 85], ["Masak", 70]],
  [["Kesetiaan", 98], ["Strategi", 90], ["Nyanyi", 64]],
] as const;
const ROLES = ["FIGHTER · SABAR", "SUPPORT · SETIA"];
const ART = "/themes/art/arena-legenda";

/** Painted (gouache / foil) decorative image — never opens the photo lightbox. */
function Art({ name, w, h, className, eager }: { name: string; w: number; h: number; className?: string; eager?: boolean }) {
  return (
    // eslint-disable-next-line @next/next/no-img-element -- static painted ornament
    <img src={`${ART}/${name}.webp`} alt="" aria-hidden width={w} height={h} className={className} data-nolightbox
      loading={eager ? "eager" : "lazy"} fetchPriority={eager ? "high" : undefined} decoding="async" draggable={false} />
  );
}
const DEMO_SHOP = [
  { name: "Kulkas 2 Pintu", rarity: "EPIC", price: "3.450", art: "item-fridge", w: 99, h: 140, color: "#b06bff" },
  { name: "Mesin Cuci", rarity: "ELITE", price: "2.890", art: "item-washer", w: 104, h: 112, color: "#39c5f3" },
  { name: "Smart TV 50\"", rarity: "LEGEND", price: "4.100", art: "item-tv", w: 104, h: 83, color: "#f0c96e" },
];


function city(address: string) {
  const parts = address.split(",").map(part => part.trim()).filter(Boolean);
  return parts[parts.length - 1] ?? "";
}

function Head({ id, children }: { id: string; children: string }) {
  return <div className={s.head}><i aria-hidden /><h2 id={id}>{children}</h2></div>;
}

export default function ArenaLegendaTheme({ data, slug, guestToken, demo, skipCover }: ThemeProps) {
  const { couple } = data;
  const names = `${couple.groom} & ${couple.bride}`;
  const initials = `${couple.groom.slice(0, 1)}♥${couple.bride.slice(0, 1)}`.toUpperCase();
  const longDate = formatDate(data.date);
  const where = city(data.address) || data.place;
  const rsvp = useRsvp({ slug, guestToken, demo });
  const wishes = useWishes({ slug, guestToken, demo, seed: DEMO_WISHES });
  const sheets = useSheets();
  const { copy, copied } = useCopy();
  const stories = storyItems(data);
  const countdown = useCountdown(data.date);
  const [picked, setPicked] = useState<string | null>(null);
  const [bought, setBought] = useState<string[]>([]);
  const pickHero = (key: string, name: string) => {
    setPicked(current => (current === key ? null : key));
    if (picked !== key) toast(`Hero dipilih: ${name}`);
  };
  const buy = (name: string) => {
    const on = !bought.includes(name);
    setBought(b => (on ? [...b, name] : b.filter(n => n !== name)));
    toast(on ? `${name} ditandai` : "Batal ditandai");
  };
  const heroes = [
    { key: "groom", short: couple.groom, name: couple.groomFull ?? couple.groom, parents: couple.groomParents, photo: couple.groomPhoto ?? data.gallery[0] },
    { key: "bride", short: couple.bride, name: couple.brideFull ?? couple.bride, parents: couple.brideParents, photo: couple.bridePhoto ?? data.gallery[1] },
  ];

  return (
    <ThemeShell
      fonts={FONTS}
      background="#060b1c"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.bg} aria-hidden><Art name="cover" w={640} h={1400} eager /></div>
          <div className={s.match}>
            <h1>Pasangan Ditemukan!</h1>
            <p>DUO RANKED · SELAMANYA</p>
          </div>
          <div className={s.vs}>
            <span className={s.rune} aria-hidden><Art name="rune" w={440} h={440} eager /></span>
            {heroes.map((hero, index) => (
              <div key={hero.key} className={s.vsHero} style={{ order: index === 0 ? 0 : 2 }}>
                <span className={s.ring}><Photo src={hero.photo} alt={hero.name} /></span>
                <strong>{hero.short}</strong>
                <em>{ROLES[index]}</em>
              </div>
            ))}
            <div className={s.vsMid} aria-hidden><span>❤</span><b>&amp;</b></div>
          </div>
          <div className={s.rank}>
            <Art name="crest" w={231} h={219} className={s.crest} eager />
            <small>NAIK PERINGKAT</small>
            <strong>MYTHIC PELAMINAN</strong>
            <span>{[longDate, where].filter(Boolean).join(" · ")}</span>
          </div>
          <div className={s.kepada}>
            <small>UNDANGAN UNTUK PEMAIN</small>
            <strong>{guestLabel(data)}</strong>
          </div>
          <div className={s.coverActions}>
            <button type="button" className={s.goldBtn} onClick={open}><Lucide icon={ic.swords} size={18} />Terima Undangan</button>
            <p>Mohon maaf bila ada kesalahan penulisan nama &amp; gelar</p>
          </div>
        </section>
      )}
    >
      <header className={s.header}>
        <div className={s.top}>
          <div className={s.player}>
            <span className={s.av} aria-hidden>{initials}</span>
            <div><h1>{names}</h1><small>Lobby {data.eventLabel ?? "Pernikahan"}</small></div>
          </div>
          <div className={s.chips}>
            <span aria-label="Doa tak terbatas"><Lucide icon={ic.gem} size={12} color="#39c5f3" />∞</span>
            <a href="#al-wishes" aria-label={demo ? "Restu 100%" : `${wishes.wishes.length} ucapan`}>
              <Lucide icon={ic.heart} size={12} color="#ff6b9c" />{demo ? "100%" : wishes.wishes.length}
            </a>
          </div>
        </div>
      </header>

      <main className={s.body}>
        <Extras slot="opening" className={s.extras} />

        <section className={s.section} aria-labelledby="al-hero">
          <Head id="al-hero">PILIH HERO</Head>
          {heroes.map((hero, index) => (
            <article key={hero.key} className={s.hero} data-picked={picked === hero.key ? "" : undefined}>
              <Photo src={hero.photo} alt={hero.name} className={s.heroPhoto} />
              <div className={s.heroText}>
                <strong>{hero.name}</strong>
                {hero.parents && <small>{hero.parents}</small>}
                {demo ? (
                  DEMO_STATS[index]?.map(([label, value], i) => (
                    <div key={label} className={s.stat}>
                      <span>{label}</span>
                      <i><b style={{ width: `${value}%`, "--i": i } as CSSProperties} /></i>
                      <em>{value}</em>
                    </div>
                  ))
                ) : (
                  <em className={s.role}>{ROLES[index]}</em>
                )}
                <button type="button" className={s.pick} aria-pressed={picked === hero.key} onClick={() => pickHero(hero.key, hero.short)}>
                  <Lucide icon={ic.swords} size={12} />{picked === hero.key ? "TERPILIH" : "PILIH"}
                </button>
              </div>
            </article>
          ))}
        </section>

        {stories.length > 0 && (
          <section className={s.section} aria-labelledby="al-story">
            <Head id="al-story">RIWAYAT MUSIM</Head>
            {stories.map((story, index) => (
              <article key={story.title + index} className={s.season} style={{ "--i": index } as CSSProperties}>
                <span className={s.badge} aria-hidden><Art name="shield" w={80} h={90} />{story.date && <small>{story.date}</small>}</span>
                <div>
                  <h3>{story.title}</h3>
                  {story.date && <span className={s.srOnly}>{story.date}</span>}
                  <p>{story.body}</p>
                  {story.image && <Photo src={story.image} alt={story.title} className={s.seasonImg} />}
                </div>
              </article>
            ))}
          </section>
        )}

        <section className={s.section} aria-labelledby="al-events">
          <Head id="al-events">JADWAL PERTANDINGAN</Head>
          {countdown.ready && !countdown.done && (
            <div className={s.timer} role="timer" aria-label={`${countdown.days} hari ${countdown.hours} jam ${countdown.minutes} menit lagi`}>
              <small>MATCH DIMULAI DALAM</small>
              <div>
                {[[countdown.days, "H"], [countdown.hours, "J"], [countdown.minutes, "M"], [countdown.seconds, "D"]].map(([value, unit]) => (
                  <span key={unit}><Tick className={s.tick} value={value} /><small>{unit}</small></span>
                ))}
              </div>
            </div>
          )}
          {data.events.map((event, index) => {
            const p = dateParts(event.date);
            const href = mapsHref(data, event);
            return (
              <article key={event.name + index} className={`${s.match2} ${index % 2 ? s.blue : ""}`}>
                {p.day && <span className={s.dateBox}><small>{p.monthShort}</small><b>{p.day.padStart(2, "0")}</b></span>}
                <div className={s.matchText}>
                  <h3>{event.name}</h3>
                  <strong>{event.time}</strong>
                  <small>{[event.venue, event.address].filter(Boolean).join(", ")}</small>
                </div>
                {href && <a href={href} target="_blank" rel="noreferrer" className={s.peta} aria-label={`Peta ${event.venue}`}>PETA</a>}
              </article>
            );
          })}
        </section>

        <Extras slot="event" className={s.extras} />

        {data.gallery.length > 0 && (
          <section className={s.section} aria-labelledby="al-gallery">
            <Head id="al-gallery">KOLEKSI SKIN</Head>
            <div className={s.skins}>
              {data.gallery.map((src, index) => (
                <figure key={src + index} className={s.skin}>
                  <Photo src={src} alt={`Foto ${index + 1}`} />
                  <figcaption>{SKINS[index % SKINS.length]}</figcaption>
                </figure>
              ))}
            </div>
          </section>
        )}

        <Extras slot="story" className={s.extras} />

        {demo && (
          <section className={s.section} aria-labelledby="al-shop">
            <Head id="al-shop">TOKO WISHLIST</Head>
            <div className={s.shop}>
              {DEMO_SHOP.map(item => (
                <button key={item.name} type="button" className={s.item} aria-pressed={bought.includes(item.name)} onClick={() => buy(item.name)}
                  style={{ borderColor: `${item.color}66`, "--rc": item.color } as CSSProperties}>
                  <em style={{ color: item.color, background: `${item.color}26` }}>{item.rarity}</em>
                  <span className={s.itemIcon} style={{ borderColor: item.color }}><Art name={item.art} w={item.w} h={item.h} /></span>
                  <strong>{item.name}</strong>
                  <b>{bought.includes(item.name) ? "DITANDAI" : <><Lucide icon={ic.gem} size={11} color="#39c5f3" />{item.price}</>}</b>
                </button>
              ))}
            </div>
            <p className={s.fine}>1 diamond = Rp1.000 · atau kirim langsung ke alamat di bawah</p>
          </section>
        )}

        <Extras slot="end" className={s.extras} />

        {data.gifts.length > 0 && (
          <section className={s.section} aria-labelledby="al-gift">
            <Head id="al-gift">TOP UP DOA &amp; KADO</Head>
            {data.gifts.map(gift => {
              const info = giftInfo(gift);
              const address = gift.type === "address";
              return (
                <div key={gift.id} className={s.wallet}>
                  <span className={s.walletIcon} aria-hidden><Lucide icon={address ? ic.mapPin : ic.gem} size={20} color="#39c5f3" /></span>
                  <div>
                    <strong>{address ? "Kirim Kado" : "Amplop Digital"}</strong>
                    <small>{[[address ? "" : info.title, info.number].filter(Boolean).join(" "), info.holder ? `a.n. ${info.holder}` : ""].filter(Boolean).join(" · ")}</small>
                    {info.image && <Photo src={info.image} alt="Kode QRIS" className={s.qris} />}
                  </div>
                  {info.copy && <button type="button" data-copied={copied === info.copy ? "" : undefined} onClick={() => copy(info.copy)}>{copied === info.copy ? "TERSALIN" : "SALIN"}</button>}
                </div>
              );
            })}
          </section>
        )}

        <section className={s.section} id="al-wishes" aria-labelledby="al-wishes-h">
          <Head id="al-wishes-h">OBROLAN TIM</Head>
          {wishes.wishes.length === 0 && <p className={s.fine}>Belum ada pesan di obrolan tim. Kirim ucapan pertamamu!</p>}
          {wishes.wishes.slice(0, 10).map((wish, index) => (
            <p key={wish.id} className={s.msg} style={{ "--i": Math.min(index, 6) } as CSSProperties}>
              <b style={{ color: NAME_COLORS[index % NAME_COLORS.length] }}>{wish.name}:</b>
              <span>{wish.message}</span>
            </p>
          ))}
          <p className={s.typing} aria-hidden><i /><i /><i /><span>{couple.bride} sedang mengetik</span></p>
        </section>

        <footer className={s.note}><a href="/" target="_blank" rel="noreferrer">dibuat dengan ♥ di Rawuh</a></footer>
      </main>

      <nav className={s.bottom} aria-label="Aksi undangan">
        <button type="button" className={s.chatBtn} onClick={sheets.openWish} aria-label="Kirim ucapan"><Lucide icon={ic.messageSquare} size={18} color="#39c5f3" /></button>
        <button type="button" className={s.goldBtn} onClick={sheets.openRsvp}><Lucide icon={ic.swords} size={16} />Konfirmasi Hadir</button>
      </nav>

      <Sheet open={sheets.sheet === "rsvp"} onClose={sheets.close} title="Konfirmasi Kehadiran" tint={tint}>
        <RsvpForm rsvp={rsvp} guestName={data.guestName} demo={demo} labels={{ submit: "Siap Bertanding!" }} />
      </Sheet>
      <Sheet open={sheets.sheet === "wish"} onClose={sheets.close} title="Kirim Pesan ke Tim" tint={tint}>
        <WishForm wishes={wishes} guestName={data.guestName} demo={demo} />
      </Sheet>
    </ThemeShell>
  );
}
