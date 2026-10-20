"use client";
// Theme "Game Retro" — undangan bergaya game 8-bit (design: The Final Level, Dina & Rama).
import { useState } from "react";
import { toast } from "@/lib/celebrate";
import {
  Extras, Lucide, Photo, RsvpForm, Sheet, ThemeShell, WishForm, dateParts, formatDate, giftInfo, guestLabel,
  mapsHref, storyItems, useCopy, useRsvp, useSheets, useWishes, type ThemeProps, type ThemeTint,
} from "../kit";
import { ic } from "./icons";
import s from "./styles.module.css";

const FONTS = ["Press Start 2P", "VT323"];
const ART = "/themes/art/game-retro";
const tint: ThemeTint = {
  "--t-accent": "#ffd93d", "--t-accent-ink": "#1a1040", "--t-bg": "#1a1040", "--t-ink": "#ffffff", "--t-muted": "#b9a8f0",
  "--t-line": "#5a4a99", "--t-field": "#241656", "--t-radius": "0px", "--t-font": "'VT323', ui-monospace, monospace",
};
const DEMO_WISHES = [
  { id: "w1", name: "Player Bimo", message: "GG! Dari warnet sampai pelaminan. Hadir pastinya!" },
  { id: "w2", name: "Auntie Rina", message: "Combo terkuat 2027. Semoga HP-nya selalu penuh. ♥" },
];
const DEMO_STATS = [
  [["CINTA", 96, "fillPink"], ["SABAR", 88, "fillGreen"]],
  [["SETIA", 99, "fillPink"], ["MASAK", 42, "fillGreen"]],
] as const;
const DEMO_SHOP = [
  { name: "RICE COOKER", price: "800", sprite: "rice-cooker" },
  { name: "VACUUM BOT", price: "3200", sprite: "vacuum-bot" },
  { name: "SOFA +5 DEF", price: "2700", sprite: "sofa" },
];


function city(address: string) {
  const parts = address.split(",").map(part => part.trim()).filter(Boolean);
  return parts[parts.length - 1] ?? "";
}

const handle = (name: string) => name.trim().toUpperCase().replace(/\s+/g, "_");

export default function GameRetroTheme({ data, slug, guestToken, demo, skipCover }: ThemeProps) {
  const parts = dateParts(data.date);
  const year = parts.year || "2027";
  const rsvp = useRsvp({ slug, guestToken, demo });
  const wishes = useWishes({ slug, guestToken, demo, seed: DEMO_WISHES });
  const sheets = useSheets();
  const { copy, copied } = useCopy();
  const [later, setLater] = useState(false);
  const [picked, setPicked] = useState<number[]>([]);
  const [bag, setBag] = useState<string[]>([]);
  const pick = (index: number, name: string) => {
    const on = !picked.includes(index);
    setPicked(list => on ? [...list, index] : list.filter(item => item !== index));
    if (on) toast(`${name.toUpperCase()} siap bertarung!`);
  };
  const buy = (name: string) => {
    const on = !bag.includes(name);
    setBag(list => on ? [...list, name] : list.filter(item => item !== name));
    if (on) toast(`${name} masuk inventori`);
  };
  const stories = storyItems(data);
  const where = city(data.address) || data.place;
  const label = (data.eventLabel ?? "Pernikahan").toUpperCase();
  const subtitle = [label, parts.day ? `${parts.day} ${parts.month} ${parts.year}`.toUpperCase() : "", where.toUpperCase()].filter(Boolean).join(" · ");
  const shortDate = formatDate(data.date, { day: "numeric", month: "short", year: "numeric" });
  const people = [
    { name: data.couple.bride, parents: data.couple.brideParents, photo: data.couple.bridePhoto ?? data.gallery[0] },
    { name: data.couple.groom, parents: data.couple.groomParents, photo: data.couple.groomPhoto ?? data.gallery[1] },
  ];

  return (
    <ThemeShell
      fonts={FONTS}
      background="#1a1040"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.coverBg} aria-hidden>
            {/* eslint-disable-next-line @next/next/no-img-element -- painted pixel art, static asset */}
            <img src={`${ART}/castle.webp`} alt="" width={640} height={688} loading="eager" fetchPriority="high" data-nolightbox />
          </div>
          <div className={s.hud} aria-hidden>
            <span className={s.yellow}>SCORE {year}</span>
            <span className={s.hearts}><i /><i /><i /></span>
            <span className={s.cyan}>LV.99</span>
          </div>
          <div className={s.coverSpace} />
          <div className={s.title}>
            <h1>{data.couple.bride.toUpperCase()} <span aria-label="dan">♥</span> {data.couple.groom.toUpperCase()}</h1>
            <p className={s.level}>THE FINAL LEVEL</p>
            <p className={s.tagline}>— {subtitle} —</p>
          </div>
          <div className={s.grow} style={{ flexBasis: 61 }} />
          <div className={s.dialog} aria-live="polite">
            <p className={s.detected}>{later ? "PROGRESS TERSIMPAN!" : "PLAYER BARU TERDETEKSI!"}</p>
            <p className={s.kepada}>Kepada Yth. Bapak/Ibu/Saudara/i</p>
            <h2>{guestLabel(data).toUpperCase()}</h2>
            <p className={s.dialogText}>
              {later ? "Tidak apa-apa, undangan menunggumu. Tekan MULAI kapan saja untuk lanjut bermain." : "Kamu diundang untuk menyaksikan boss terakhir kami: KOMITMEN SEUMUR HIDUP."}
            </p>
          </div>
          <div className={s.select}>
            <button type="button" className={s.startBtn} onClick={open}><span aria-hidden>► </span>MULAI — BUKA UNDANGAN</button>
            <button type="button" className={s.laterBtn} onClick={() => setLater(true)}>&nbsp;&nbsp;LIHAT NANTI</button>
          </div>
          <p className={s.press} aria-hidden>PRESS START</p>
        </section>
      )}
    >
      <header className={s.nav}>
        <h1>WORLD MAP</h1>
        <span className={s.coins} aria-hidden><i className={s.coin} />x{year}{bag.length > 0 && <b key={bag.length} className={s.bagCount}>+{bag.length}</b>}</span>
      </header>

      <main className={s.body}>
        <Extras slot="opening" className={s.extras} />

        <section className={s.section} aria-labelledby="gr-chars">
          <h2 id="gr-chars" className={s.cyan}><i className={s.blk} aria-hidden>■</i> PILIH KARAKTER</h2>
          <div className={s.chars}>
            {people.map((person, index) => (
              <article key={index} className={s.char} data-picked={picked.includes(index) || undefined}>
                <Photo src={person.photo} alt={person.name} className={s.charImg} />
                <h3>{person.name.toUpperCase()}</h3>
                {person.parents && <p>{person.parents}</p>}
                {demo && DEMO_STATS[index].map(([stat, value, color]) => (
                  <div key={stat} className={s.stat} aria-hidden>
                    <span>{stat}</span>
                    <i className={s.bar}><b className={s[color]} style={{ width: `${value}%` }} /></i>
                    <em>{value}</em>
                  </div>
                ))}
                <button type="button" className={s.pickBtn} aria-pressed={picked.includes(index)} onClick={() => pick(index, person.name)}>
                  {picked.includes(index) ? `P${index + 1} SIAP!` : "► PILIH"}
                </button>
              </article>
            ))}
          </div>
        </section>

        <section className={s.section} aria-labelledby="gr-story">
          <h2 id="gr-story" className={s.yellow}><i className={s.blk} aria-hidden>■</i> WORLD 1 — KISAH</h2>
          <ol className={s.levels}>
            {stories.map((story, index) => (
              <li key={story.title + index} className={s.levelRow}>
                <span className={s.levelNo}>1-{index + 1}</span>
                <div className={s.levelText}>
                  <strong>{story.title}</strong>
                  <p>{[story.date, story.body].filter(Boolean).join(" · ")}</p>
                  {story.image && <Photo src={story.image} alt={story.title} className={s.levelImg} />}
                </div>
                <span className={s.star} aria-hidden>★</span>
              </li>
            ))}
            <li className={`${s.levelRow} ${s.finalRow}`}>
              <span className={s.levelNo}>1-{stories.length + 1}</span>
              <div className={s.levelText}>
                <strong>FINAL LEVEL</strong>
                <p>{shortDate} · pelaminan, save point terakhir</p>
              </div>
            </li>
          </ol>
        </section>

        {data.events.length > 0 && (
          <section className={s.section} aria-labelledby="gr-quest">
            <h2 id="gr-quest" className={s.green}><i className={s.blk} aria-hidden>■</i> QUEST HARI-H</h2>
            {data.events.map((event, index) => {
              const href = mapsHref(data, event);
              return (
                <article key={event.name + index} className={s.quest}>
                  <div className={s.questHead}>
                    <h3>QUEST {index + 1}: {event.name.toUpperCase()}</h3>
                    {href && <a className={s.mapBtn} href={href} target="_blank" rel="noreferrer" aria-label={`Peta ${event.name}`}>MAP</a>}
                  </div>
                  <p>{[formatDate(event.date), event.time, [event.venue, event.address].filter(Boolean).join(", ")].filter(Boolean).join(" · ")}</p>
                  <small>Hadiah quest: makan enak + doa restu +9999 XP kebahagiaan</small>
                </article>
              );
            })}
          </section>
        )}

        <Extras slot="event" className={s.extras} />

        {data.gallery.length > 0 && (
          <section className={s.section} aria-labelledby="gr-gallery">
            <h2 id="gr-gallery" className={s.pink}><i className={s.blk} aria-hidden>■</i> GALERI SPRITE</h2>
            <div className={s.gallery}>
              {data.gallery.map((src, index) => <Photo key={src + index} src={src} alt={`Foto ${index + 1}`} />)}
            </div>
          </section>
        )}

        <Extras slot="story" className={s.extras} />
        <Extras slot="end" className={s.extras} />

        {(demo || data.gifts.length > 0) && (
          <section className={s.section} aria-labelledby="gr-shop">
            <h2 id="gr-shop" className={s.yellow}><i className={s.blk} aria-hidden>■</i> {demo ? "ITEM SHOP" : "KASIR KOIN"}</h2>
            {demo && (
              <>
                <div className={s.shop}>
                  {DEMO_SHOP.map(item => (
                    <button key={item.name} type="button" className={s.item} aria-pressed={bag.includes(item.name)} onClick={() => buy(item.name)}>
                      {/* eslint-disable-next-line @next/next/no-img-element -- painted pixel sprite, static asset */}
                      <img className={s.sprite} src={`${ART}/${item.sprite}.webp`} alt="" aria-hidden width={48} height={48} loading="lazy" data-nolightbox />
                      <strong>{item.name}</strong>
                      <span><i className={s.coinSm} />{item.price}</span>
                      {bag.includes(item.name) && <em className={s.plus} aria-hidden>+1</em>}
                    </button>
                  ))}
                </div>
                <p className={s.shopNote}>1 koin = Rp1.000 · beli lewat kasir di bawah</p>
              </>
            )}
            {data.gifts.map(gift => {
              const info = giftInfo(gift);
              const line = [info.title !== "Alamat kado" ? `${info.title} ${info.number}`.trim() : info.number, info.holder ? `a.n. ${info.holder}` : ""].filter(Boolean).join(" · ");
              return (
                <div key={gift.id} className={s.cash}>
                  <Lucide icon={ic.wallet} color="#39ff88" />
                  <div className={s.cashText}>
                    <strong>{gift.type === "address" ? "KIRIM KADO" : "KASIR KOIN"}</strong>
                    <span>{line}</span>
                    {info.image && <Photo src={info.image} alt="Kode QRIS" className={s.qris} />}
                  </div>
                  {info.copy && <button type="button" className={s.copyBtn} onClick={() => copy(info.copy)}><span key={String(copied === info.copy)} className={s.copyLabel}>{copied === info.copy ? "TERSALIN" : "SALIN"}</span></button>}
                </div>
              );
            })}
          </section>
        )}

        <section className={s.section} aria-labelledby="gr-wishes">
          <h2 id="gr-wishes" className={s.cyan}><i className={s.blk} aria-hidden>■</i> GUESTBOOK.SAV</h2>
          {wishes.wishes.length === 0 && <p className={s.empty}>Belum ada data tersimpan. Tekan B untuk menulis ucapan pertama!</p>}
          {wishes.wishes.slice(0, 8).map((wish, index) => (
            <article key={wish.id} className={s.wish}>
              <strong>{handle(wish.name)}{index === 0 && <i className={s.caret} aria-hidden />}</strong>
              <p>{wish.message}</p>
            </article>
          ))}
        </section>
      </main>

      <nav className={s.bottom} aria-label="Aksi undangan">
        <button type="button" className={s.bBtn} onClick={sheets.openWish} aria-label="Tulis ucapan di guestbook">B</button>
        <button type="button" className={s.aBtn} onClick={sheets.openRsvp}>A — KONFIRMASI HADIR</button>
      </nav>

      <Sheet open={sheets.sheet === "rsvp"} onClose={sheets.close} title="Konfirmasi Hadir" tint={tint}>
        <RsvpForm rsvp={rsvp} guestName={data.guestName} demo={demo} labels={{ submit: "A — Simpan Kehadiran", success: "Quest diterima!" }} />
      </Sheet>
      <Sheet open={sheets.sheet === "wish"} onClose={sheets.close} title="Tulis di Guestbook" tint={tint}>
        <WishForm wishes={wishes} guestName={data.guestName} demo={demo} />
      </Sheet>
    </ThemeShell>
  );
}
