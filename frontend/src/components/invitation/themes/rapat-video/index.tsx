"use client";
// Theme "Rapat Video" — undangan bergaya aplikasi rapat video (design: Undangan — Tema Rapat Video (Rani & Yudha)).
import { useRef, useState } from "react";
import {
  Extras, Lucide, Photo, RsvpForm, Sheet, ThemeShell, Tick, WishForm, coupleLabel, formatDate, giftInfo, guestLabel,
  mapsHref, storyItems, timeAgo, useCopy, useCountdown, useRsvp, useSheets, useWishes, type ThemeProps, type ThemeTint,
} from "../kit";
import { toast } from "@/lib/celebrate";
import { ic } from "./icons";
import s from "./styles.module.css";

const FONTS = ["Inter:wght@400;600;700;800", "JetBrains Mono:wght@400;700"];
const tint: ThemeTint = {
  "--t-accent": "#0e72ed", "--t-accent-ink": "#ffffff", "--t-bg": "#1f1f1f", "--t-ink": "#ffffff", "--t-muted": "#a6a6a6",
  "--t-line": "#3a3a3a", "--t-field": "#2a2a2a", "--t-radius": "10px", "--t-font": "Inter, system-ui, sans-serif",
};
const DEMO_WISHES = [
  { id: "w1", name: "Bu Marlina", message: "Selamat ya! Kami hadir offline, bukan cuma di layar.", created_at: new Date(Date.now() - 2 * 3600e3).toISOString() },
  { id: "w2", name: "Pak Dedi", message: "Akhirnya project jangka panjang kalian launching. Sukses!", created_at: new Date(Date.now() - 4 * 3600e3).toISOString() },
];
const DEMO_FILES = [["Prewedding.mp4", "24:10"], ["Lamaran.mp4", "08:52"], ["BTS.mp4", "12:33"]];
// Gift tiers + wishlist prices are invented sample content: rendered only in demo.
const DEMO_TIERS = [["👏", "Rp100rb"], ["❤", "Rp500rb"], ["🎉", "Rp1jt"]];
const DEMO_WISHLIST = [{ name: "Monitor Kerja 27\"", price: "Rp2.800.000", icon: ic.monitor }, { name: "Ring Light Pro", price: "Rp650.000", icon: ic.lamp }];


function NameTag({ name, muted }: { name: string; muted?: boolean }) {
  return (
    <span className={s.nameTag}>
      <Lucide icon={muted ? ic.micOff : ic.mic} size={11} color={muted ? "#f44336" : "#4caf50"} />
      {!muted && <span className={s.level} aria-hidden><i /><i /><i /></span>}
      {name}
    </span>
  );
}

export default function RapatVideoTheme({ data, slug, guestToken, demo, skipCover }: ThemeProps) {
  const couple = coupleLabel(data);
  const title = `${data.eventLabel ?? "Pernikahan"} ${couple}`;
  const num = (o: Intl.DateTimeFormatOptions) => formatDate(data.date, o);
  const valid = /^\d+$/.test(num({ day: "2-digit" }));
  const dd = valid ? num({ day: "2-digit" }) : "00";
  const mm = valid ? num({ month: "2-digit" }) : "00";
  const yyyy = valid ? num({ year: "numeric" }) : "0000";
  const meetingId = `${dd}${mm} ${yyyy}`;
  const startTime = valid ? num({ hour: "2-digit", minute: "2-digit", hour12: false }).replace(":", ".") : "";
  const waiting = [formatDate(data.date, { day: "numeric", month: "short", year: "numeric" }), startTime && `${startTime} WIB`].filter(Boolean).join(", ");
  const countdown = useCountdown(data.date);
  const rsvp = useRsvp({ slug, guestToken, demo });
  const wishes = useWishes({ slug, guestToken, demo, seed: DEMO_WISHES });
  const sheets = useSheets();
  const { copy, copied } = useCopy();
  const stories = storyItems(data);
  const guest = guestLabel(data);
  const [reactions, setReactions] = useState<{ id: number; emoji: string; x: number }[]>([]);
  const [tier, setTier] = useState<string | null>(null);
  const [given, setGiven] = useState<Record<string, boolean>>({});
  const nextId = useRef(0);
  const react = (emoji: string, amount: string) => {
    setTier(amount);
    const id = nextId.current++;
    setReactions(list => [...list.slice(-6), { id, emoji, x: 15 + Math.round(Math.random() * 70) }]);
  };
  const panel = [
    { role: "Host", short: data.couple.bride, name: data.couple.brideFull ?? data.couple.bride, parents: data.couple.brideParents, photo: data.couple.bridePhoto ?? data.gallery[0] },
    { role: "Co-host", short: data.couple.groom, name: data.couple.groomFull ?? data.couple.groom, parents: data.couple.groomParents, photo: data.couple.groomPhoto ?? data.gallery[1] },
  ];

  return (
    <ThemeShell
      fonts={FONTS}
      background="#111111"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.coverBody}>
            <p className={s.kicker}>Rapat Sakral</p>
            <h1 className={s.coverTitle}>{title}</h1>
            <div className={s.ids}>
              <div><small>ID Rapat</small><b>{meetingId}</b></div>
              <div><small>Kode</small><b>SAMAWA</b></div>
            </div>
            <p className={s.waiting}><i aria-hidden />Menunggu host memulai rapat…{waiting && ` (${waiting})`}</p>
            <div className={s.tiles}>
              {panel.map((person, index) => (
                <div key={person.role} className={`${s.tile} ${index === 0 ? s.speakA : s.speakB}`}>
                  <Photo src={person.photo} alt={person.short} className={s.tileImg} />
                  <NameTag name={`${person.short} (Mempelai)`} />
                </div>
              ))}
              <div className={`${s.tile} ${s.tileRoom}`} aria-hidden>
                <span className={`${s.tileAvatar} ${s.tileAvatarTalk}`}>K</span>
                <NameTag name="Keluarga Besar" />
              </div>
              <div className={`${s.tile} ${s.tileGarden}`} aria-hidden>
                <span className={`${s.tileAvatar} ${s.tileAvatarGrey}`}>K</span>
                <NameTag name="Kamu (Tamu)" muted />
              </div>
            </div>
            <div className={s.kepada}>
              <small>ANDA DIUNDANG SEBAGAI TAMU KEHORMATAN</small>
              <strong>{guest}</strong>
            </div>
            <button type="button" className={s.joinBtn} onClick={open}><Lucide icon={ic.video} size={17} color="#fff" />Gabung — Buka Undangan</button>
          </div>
          <div className={s.toolbar} aria-hidden>
            {[[ic.mic, "Audio"], [ic.video, "Video"], [ic.users, "Peserta"], [ic.messageSquare, "Chat"]].map(([icon, label]) => (
              <span key={label}><Lucide icon={icon} size={20} color="#fff" />{label}</span>
            ))}
            <span className={s.leave}><Lucide icon={ic.phone} size={20} color="#f44336" />Keluar</span>
          </div>
        </section>
      )}
    >
      <header className={s.nav}>
        <span className={s.rec}><i aria-hidden />REC · {title}</span>
        <span className={s.timer} aria-label={countdown.ready ? `${countdown.days} hari ${countdown.hours} jam ${countdown.minutes} menit lagi` : "Hitung mundur"}>
          {countdown.done ? "LIVE" : <><Tick value={countdown.days} /> hari <Tick value={countdown.hours} />:<Tick value={countdown.minutes} />:<Tick value={countdown.seconds} /></>}
        </span>
      </header>

      <main className={s.body}>
        <section className={s.section} aria-labelledby="rv-panel">
          <h2 id="rv-panel">Panelis Utama</h2>
          <div className={s.panel}>
            {panel.map(person => (
              <article key={person.role} className={s.panelist}>
                <Photo src={person.photo} alt={person.name} className={s.panelImg} />
                <div>
                  <small>{person.role}</small>
                  <strong>{person.name}</strong>
                  {person.parents && <p>{person.parents}</p>}
                </div>
              </article>
            ))}
          </div>
        </section>

        <Extras slot="opening" className={s.extras} />

        <section className={s.section} aria-labelledby="rv-agenda">
          <h2 id="rv-agenda">Agenda Rapat</h2>
          {data.events.map((event, index) => {
            const href = mapsHref(data, event);
            const where = [event.venue, event.address].filter(Boolean).join(", ");
            const time = event.time.split(/\s*[–-]\s*/)[0] || event.time;
            return (
              <article key={event.name + index} className={`${s.agenda} ${index === 0 ? s.agendaNow : ""}`}>
                <span className={s.agendaTime}>{time}</span>
                <div>
                  <strong>{event.name} · {formatDate(event.date || data.date, { weekday: "long", day: "numeric", month: "short", year: "numeric" })}</strong>
                  {where && (href ? <a href={href} target="_blank" rel="noreferrer">{where}</a> : <span>{where}</span>)}
                </div>
                <div className={s.agendaBtns}>
                  <button type="button" className={s.accept} onClick={() => sheets.openRsvp("yes")}>Terima</button>
                  <button type="button" className={s.decline} onClick={() => sheets.openRsvp("no")}>Tolak</button>
                </div>
              </article>
            );
          })}
        </section>

        <Extras slot="event" className={s.extras} />

        {stories.length > 0 && (
          <section className={s.section} aria-labelledby="rv-story">
            <h2 id="rv-story">Riwayat Rapat Kami</h2>
            {stories.map((story, index) => (
              <article key={story.title + index} className={s.story}>
                {"date" in story && story.date && <span className={s.year}>{story.date}</span>}
                <div><strong>{story.title}</strong><p>{story.body}</p></div>
              </article>
            ))}
          </section>
        )}

        {data.gallery.length > 0 && (
          <section className={s.section} aria-labelledby="rv-gallery">
            <h2 id="rv-gallery">Rekaman Sebelumnya · Galeri</h2>
            <div className={s.grid}>
              {data.gallery.map((src, index) => {
                const [name, duration] = demo && DEMO_FILES[index] ? DEMO_FILES[index] : [`Foto-${String(index + 1).padStart(2, "0")}.jpg`, ""];
                return (
                  <div key={src + index} className={s.rec2}>
                    <span className={s.thumb}>
                      <Photo src={src} alt={`Galeri ${index + 1}`} />
                      {duration && <b>{duration}</b>}
                      <span className={s.playIcon} aria-hidden><Lucide icon={ic.play} size={14} color="#fff" /></span>
                    </span>
                    <span className={s.recName}>{name}</span>
                  </div>
                );
              })}
            </div>
          </section>
        )}

        <Extras slot="story" className={s.extras} />
        <Extras slot="end" className={s.extras} />

        {(demo || data.gifts.length > 0) && (
          <section className={s.section} aria-labelledby="rv-gift">
            <h2 id="rv-gift">{demo ? "Reaksi & Kado" : "Kado"}</h2>
            {demo && (
              <>
                <div className={s.tiers}>
                  {DEMO_TIERS.map(([emoji, amount]) => (
                    <button key={amount} type="button" aria-pressed={tier === amount} aria-label={`Reaksi ${amount}`} onClick={() => react(emoji, amount)}>
                      <i aria-hidden>{emoji}</i>{amount}
                    </button>
                  ))}
                  <span className={s.floats} aria-hidden>
                    {reactions.map(item => (
                      <i key={item.id} style={{ left: `${item.x}%` }} onAnimationEnd={() => setReactions(list => list.filter(r => r.id !== item.id))}>{item.emoji}</i>
                    ))}
                  </span>
                </div>
                {DEMO_WISHLIST.map(item => (
                  <div key={item.name} className={s.item}>
                    <span className={s.itemIcon}><Lucide icon={item.icon} color="#6db0ff" /></span>
                    <div><strong>{item.name}</strong><small>{item.price}</small></div>
                    <button type="button" className={s.smallBtn} aria-pressed={!!given[item.name]}
                      onClick={() => { setGiven(g => ({ ...g, [item.name]: !g[item.name] })); if (!given[item.name]) toast("Ditandai di perangkatmu"); }}>
                      {given[item.name] ? "Dipilih" : "Beri"}
                    </button>
                  </div>
                ))}
              </>
            )}
            {data.gifts.map(gift => {
              const info = giftInfo(gift);
              const line = gift.type === "address" ? info.number : [[info.title, info.number].filter(Boolean).join(" "), info.holder ? `a.n. ${info.holder}` : ""].filter(Boolean).join(" · ");
              return (
                <div key={gift.id} className={s.amplop}>
                  <Lucide icon={ic.wallet} color="#6db0ff" />
                  <div>
                    <strong>{gift.type === "address" ? "Kirim Kado" : "Amplop Digital"}</strong>
                    {line && <small>{line}</small>}
                    {"image" in info && info.image && <Photo src={info.image} alt="Kode QRIS" className={s.qris} />}
                  </div>
                  {info.copy && <button type="button" className={s.smallBtn} data-done={copied === info.copy || undefined} onClick={() => copy(info.copy)}>{copied === info.copy ? "Tersalin" : "Salin"}</button>}
                </div>
              );
            })}
          </section>
        )}

        <section className={s.section} aria-labelledby="rv-chat">
          <h2 id="rv-chat">Chat Rapat</h2>
          {wishes.wishes.length === 0 && <p className={s.empty}>Belum ada pesan di chat. Kirim ucapan pertamamu!</p>}
          {wishes.wishes.slice(0, 8).map(wish => (
            <article key={wish.id} className={s.chat}>
              <small>{wish.name} → Semua panelis{!demo && wish.created_at ? ` · ${timeAgo(wish.created_at)}` : ""}</small>
              <p>{wish.message}</p>
            </article>
          ))}
          <p className={s.typing} aria-hidden><span><i /><i /><i /></span>{data.couple.bride} sedang mengetik…</p>
          <button type="button" className={s.chatBtn} onClick={sheets.openWish}><Lucide icon={ic.messageSquare} size={15} color="#6db0ff" />Tulis di chat…</button>
        </section>
      </main>

      <nav className={s.bottom} aria-label="Aksi undangan">
        <button type="button" className={s.handBtn} onClick={sheets.openWish} aria-label="Angkat tangan — kirim ucapan"><Lucide icon={ic.hand} size={18} color="#f9a825" /></button>
        <button type="button" className={s.rsvpBtn} onClick={sheets.openRsvp}><Lucide icon={ic.video} color="#fff" />Terima — Konfirmasi Hadir</button>
      </nav>

      <Sheet open={sheets.sheet === "rsvp"} onClose={sheets.close} title="Terima Undangan Rapat" tint={tint}>
        <RsvpForm key={sheets.attendance} initialAttendance={sheets.attendance} rsvp={rsvp} guestName={data.guestName} demo={demo} labels={{ yes: "Terima", maybe: "Mungkin", no: "Tolak", submit: "Konfirmasi Hadir" }} />
      </Sheet>
      <Sheet open={sheets.sheet === "wish"} onClose={sheets.close} title="Chat ke Semua Panelis" tint={tint}>
        <WishForm wishes={wishes} guestName={data.guestName} demo={demo} submitLabel="Kirim ke Chat" />
      </Sheet>
    </ThemeShell>
  );
}
