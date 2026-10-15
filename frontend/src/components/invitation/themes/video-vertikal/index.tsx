"use client";
// Theme "Video Vertikal" — undangan bergaya aplikasi video pendek (design: Undangan — Tema Video Vertikal (Zahra & Evan)).
import { useState, type CSSProperties } from "react";
import {
  Extras, Lucide, Photo, RsvpForm, Sheet, ThemeShell, Tick, WishForm, coupleLabel, formatDate, giftInfo, guestLabel,
  mapsHref, storyItems, useCopy, useCountdown, useRsvp, useSheets, useWishes, type ThemeProps, type ThemeTint, type Wish,
} from "../kit";
import { toast } from "@/lib/celebrate";
import { ic } from "./icons";
import s from "./styles.module.css";

const FONTS = ["Inter:wght@400;500;600;700;800"];
const tint: ThemeTint = {
  "--t-accent": "#fe2c55", "--t-accent-ink": "#ffffff", "--t-bg": "#121212", "--t-ink": "#ffffff", "--t-muted": "rgba(255,255,255,.7)",
  "--t-line": "#262626", "--t-field": "#1c1c1c", "--t-radius": "6px", "--t-font": "Inter, system-ui, sans-serif",
};
const DEMO_WISHES: (Wish & { likes?: string })[] = [
  { id: "w1", name: "bestie.zahra", message: "INI YANG DITUNGGU-TUNGGU!! hadir dong", created_at: new Date(Date.now() - 2 * 3600e3).toISOString(), likes: "4.2rb" },
  { id: "w2", name: "bang.dul", message: "dari part 1 gue udah bilang bakal nikah. telat tapi selamat!", created_at: new Date(Date.now() - 5 * 3600e3).toISOString(), likes: "980" },
];
const THUMBS = [
  "linear-gradient(310deg, #fe2c55 0%, #8a1538 100%)",
  "linear-gradient(310deg, #25f4ee 0%, #0e6e8c 100%)",
  "linear-gradient(310deg, #b06bff 0%, #4a2580 100%)",
];
const DEMO_VIEWS = ["890rb ditonton", "1,1jt ditonton", "2,4jt ditonton"];
const WATCHED = ["100%", "100%", "100%", "82%", "64%"];
const GRID_VIEWS = ["1,2jt", "890rb", "2,4jt"];
const TIERS = [["🌹", "Mawar", "Rp10rb"], ["🧸", "Boneka", "Rp100rb"], ["🦁", "Singa", "Rp500rb"], ["🌌", "Galaxy", "Rp1jt"]];
const WISHLIST = [
  { name: "Kasur & Sprei Set", price: "Rp2.100.000", icon: ic.bedDouble },
  { name: "Microwave", price: "Rp1.300.000", icon: ic.microwave },
];


const nf = new Intl.NumberFormat("id-ID");
const clean = (v: string) => v.toLowerCase().normalize("NFD").replace(/[^a-z0-9]/g, "");
function city(address: string) {
  const parts = address.split(",").map(p => p.trim()).filter(Boolean);
  return parts[parts.length - 1] ?? "";
}

export default function VideoVertikalTheme({ data, slug, guestToken, demo, skipCover }: ThemeProps) {
  const user = `${clean(data.couple.bride + data.couple.groom) || "kami"}.wedding`;
  const tag = `#${data.couple.bride.replace(/\s+/g, "")}${data.couple.groom.replace(/\s+/g, "")}`;
  const where = city(data.address) || data.place;
  const dayMonthYear = formatDate(data.date, { day: "numeric", month: "long", year: "numeric" });
  const dayMonth = formatDate(data.date, { day: "numeric", month: "long" });
  const countdown = useCountdown(data.date);
  const rsvp = useRsvp({ slug, guestToken, demo });
  const wishes = useWishes({ slug, guestToken, demo, seed: DEMO_WISHES });
  const sheets = useSheets();
  const { copy, copied } = useCopy();
  const [following, setFollowing] = useState<Record<string, boolean>>({});
  const [liked, setLiked] = useState<Record<string, boolean>>({});
  const [tier, setTier] = useState<string | null>(null);
  const [marked, setMarked] = useState<Record<string, boolean>>({});
  const stories = storyItems(data);
  const hero = data.gallery[0];
  const railAvatar = data.gallery[1] ?? hero;
  const avatar = data.gallery[2] ?? railAvatar;
  const rest = data.gallery.slice(3);
  const grid = rest.length >= 3 ? rest : data.gallery;
  const people = [
    { key: "bride", name: data.couple.brideFull ?? data.couple.bride, parents: data.couple.brideParents, photo: data.couple.bridePhoto ?? data.gallery[1], note: demo ? "528rb pengikut hatinya" : "Siap jadi pasangan" },
    { key: "groom", name: data.couple.groomFull ?? data.couple.groom, parents: data.couple.groomParents, photo: data.couple.groomPhoto ?? data.gallery[2], note: "Mengikuti 1 orang saja" },
  ];
  const commentCount = demo ? "8.204" : nf.format(wishes.wishes.length);

  return (
    <ThemeShell
      fonts={FONTS}
      background="#000"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.video} aria-hidden><Photo src={hero} /></div>
          <span className={s.progress} aria-hidden><i /></span>
          <div className={s.dim} aria-hidden />
          <div className={s.feedTabs} aria-hidden><span>Mengikuti</span><b>Untukmu</b></div>
          <div className={s.spacer} />
          <div className={s.coverBottom}>
            <div className={s.coverLeft}>
              <div className={s.meta}>
                <strong>@{user}</strong>
                <p>POV: kamu diundang ke hari paling bahagia kami {dayMonthYear}{where ? `, ${where}` : ""}. #UndanganDigital {tag}</p>
                <span className={s.music}><Lucide icon={ic.music2} size={13} /><span className={s.marquee}><span><span>suara asli — Janji Kita ({coupleLabel(data)})</span><span aria-hidden>suara asli — Janji Kita ({coupleLabel(data)})</span></span></span></span>
              </div>
              <div className={s.kepada}>
                <small>VIDEO INI UNTUK</small>
                <strong>{guestLabel(data)}</strong>
              </div>
            </div>
            <div className={s.rail} aria-hidden>
              <Photo src={railAvatar} className={s.railAv} />
              <span><Lucide icon={ic.heart} size={30} color="#fe2c55" className={s.beat} />{demo ? "1,2jt" : "Suka"}</span>
              <span><Lucide icon={ic.messageCircle} size={30} />{demo ? "8.204" : "Ucapan"}</span>
              <span><Lucide icon={ic.bookmark} size={30} />{demo ? "52rb" : "Simpan"}</span>
              <span><Lucide icon={ic.share2} size={30} />Bagikan</span>
              <span className={s.disc}><Photo src={avatar} className={s.discImg} /></span>
            </div>
          </div>
          <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.play} size={15} />Tonton Undangan Lengkap</button>
        </section>
      )}
    >
      <header className={s.nav}>
        <span aria-hidden><Lucide icon={ic.arrowLeft} size={20} /></span>
        <strong>{user}</strong>
        <span aria-hidden><Lucide icon={ic.ellipsis} size={20} /></span>
      </header>

      <main className={s.body}>
        <section className={s.profile} aria-label="Profil">
          <Photo src={avatar} alt={`Foto ${coupleLabel(data)}`} className={s.avatar} />
          <div className={s.stats}>
            <div><b>2</b><small>Mempelai</small></div>
            {demo ? <div><b>1,2jt</b><small>Suka</small></div> : <div><b>{nf.format(wishes.wishes.length)}</b><small>Ucapan</small></div>}
            <div><b>{countdown.ready ? <Tick value={Number(countdown.days)} /> : "–"}</b><small>Hari lagi</small></div>
          </div>
          <h1>{data.couple.brideFull ?? data.couple.bride} × {data.couple.groomFull ?? data.couple.groom}<br />{formatDate(data.date)}{where ? ` · ${where}` : ""}</h1>
        </section>

        <Extras slot="opening" className={s.extras} />

        <section className={s.section} aria-labelledby="vv-mempelai">
          <h2 id="vv-mempelai">Mempelai</h2>
          {people.map(person => (
            <article key={person.key} className={s.person}>
              <Photo src={person.photo} alt={person.name} className={s.personAv} />
              <div className={s.personText}>
                <strong>{person.name}</strong>
                {person.parents && <small>{person.parents}</small>}
                <em>{person.note}</em>
              </div>
              <button type="button" className={following[person.key] ? s.followOn : s.follow} aria-pressed={!!following[person.key]}
                onClick={() => {
                  if (!following[person.key]) toast(`Kamu mengikuti ${person.name}`);
                  setFollowing(f => ({ ...f, [person.key]: !f[person.key] }));
                }}>
                {following[person.key] ? "Mengikuti" : "Ikuti"}
              </button>
            </article>
          ))}
        </section>

        {stories.length > 0 && (
          <section className={s.section} aria-labelledby="vv-kisah">
            <h2 id="vv-kisah">Kisah · Series</h2>
            {stories.map((story, index) => (
              <article key={story.title + index} className={s.part}>
                <span className={s.thumb} style={{ background: story.image ? `linear-gradient(0deg, rgba(0,0,0,.35), rgba(0,0,0,.35)), url(${JSON.stringify(story.image)}) center/cover` : THUMBS[index % THUMBS.length] } as CSSProperties} aria-hidden>
                  <Lucide icon={ic.play} size={16} color="rgba(255,255,255,.7)" />
                  <i className={s.watch} style={{ "--w": WATCHED[index] ?? "100%" } as CSSProperties} />
                </span>
                <div className={s.partText}>
                  <strong>Part {index + 1} — {story.title}</strong>
                  <small>{demo ? [story.date, DEMO_VIEWS[index]].filter(Boolean).join(" · ") : [story.date, story.body].filter(Boolean).join(" · ")}</small>
                </div>
              </article>
            ))}
            <article className={s.part}>
              <span className={`${s.thumb} ${s.thumbFinal}`} aria-hidden><Lucide icon={ic.play} size={16} color="#fe2c55" /></span>
              <div className={s.partText}>
                <strong>Final — Menuju {dayMonth}</strong>
                <small className={s.hot}><i className={s.liveDot} aria-hidden />Premiere · jangan skip</small>
              </div>
            </article>
          </section>
        )}

        <section className={s.section} aria-labelledby="vv-acara">
          <h2 id="vv-acara">Acara</h2>
          <p className={s.sub}>Catat jadwalnya, jangan cuma di-save</p>
          {data.events.map((event, index) => {
            const href = mapsHref(data, event);
            return (
              <article key={event.name + index} className={s.event}>
                <span className={s.eventIcon} aria-hidden><Lucide icon={ic.calendarHeart} size={18} color="#fe2c55" /></span>
                <div className={s.eventText}>
                  <strong>{event.name} · {formatDate(event.date || data.date, { weekday: "long", day: "numeric", month: "short", year: "numeric" })}</strong>
                  <small>{[event.time, [event.venue, event.address].filter(Boolean).join(", ")].filter(Boolean).join(" · ")}</small>
                </div>
                {href && <a className={s.peta} href={href} target="_blank" rel="noreferrer" aria-label={`Peta ${event.name}`}>Peta</a>}
              </article>
            );
          })}
        </section>

        <Extras slot="event" className={s.extras} />

        {grid.length > 0 && (
          <section className={s.section} aria-labelledby="vv-galeri">
            <h2 id="vv-galeri">Galeri</h2>
            <div className={s.grid}>
              {grid.map((src, index) => (
                <div key={src + index} className={s.cell}>
                  <Photo src={src} alt={`Foto ${index + 1}`} />
                  {demo && GRID_VIEWS[index] && <span aria-hidden><Lucide icon={ic.play} size={10} />{GRID_VIEWS[index]}</span>}
                </div>
              ))}
            </div>
          </section>
        )}

        <Extras slot="story" className={s.extras} />
        <Extras slot="end" className={s.extras} />

        {(demo || data.gifts.length > 0) && (
          <section className={s.section} aria-labelledby="vv-kado">
            <h2 id="vv-kado">Kado</h2>
            <p className={s.sub}>Kirim gift, masuk ke rumah baru kami</p>
            {demo && (
              <>
                <div className={s.tiers}>
                  {TIERS.map(([emoji, name, price]) => (
                    <button key={name} type="button" className={s.tier} aria-pressed={tier === name}
                      onClick={() => { setTier(t => (t === name ? null : name)); if (tier !== name) toast(`Gift ${name} dipilih`); }}>
                      <span aria-hidden>{emoji}</span><strong>{name}</strong><small>{price}</small>
                    </button>
                  ))}
                </div>
                <div className={s.wishlist}>
                  {WISHLIST.map(item => (
                    <div key={item.name} className={s.wish}>
                      <span className={s.wishIcon} aria-hidden><Lucide icon={item.icon} size={16} color="#25f4ee" /></span>
                      <div><strong>{item.name}</strong><small>{item.price}</small></div>
                      <button type="button" className={s.beri} aria-pressed={!!marked[item.name]}
                        onClick={() => { setMarked(m => ({ ...m, [item.name]: !m[item.name] })); if (!marked[item.name]) toast("Ditandai di perangkatmu"); }}>
                        {marked[item.name] ? "Dipilih" : "Beri"}
                      </button>
                    </div>
                  ))}
                </div>
              </>
            )}
            {data.gifts.map(gift => {
              const info = giftInfo(gift);
              return (
                <div key={gift.id} className={s.amplop}>
                  <Lucide icon={ic.wallet} size={16} color="#25f4ee" />
                  <div>
                    <strong>{gift.type === "address" ? "Kirim Kado" : "Amplop Digital"}</strong>
                    <small>{(gift.type === "address" ? [info.number] : [`${info.title} ${info.number}`.trim(), info.holder ? `a.n. ${info.holder}` : ""]).filter(Boolean).join(" · ")}</small>
                  </div>
                  {info.copy && <button type="button" className={s.salin} data-done={copied === info.copy || undefined} onClick={() => copy(info.copy)}>{copied === info.copy ? "Tersalin" : "Salin"}</button>}
                  {info.image && <a className={s.salin} href={info.image} target="_blank" rel="noreferrer">Lihat QR</a>}
                </div>
              );
            })}
          </section>
        )}

        <section className={s.section} aria-labelledby="vv-komentar">
          <h2 id="vv-komentar">Komentar · {commentCount}</h2>
          {wishes.wishes.length === 0 && <p className={s.sub}>Belum ada komentar. Jadi yang pertama, yuk!</p>}
          {wishes.wishes.slice(0, 8).map(wish => {
            const likes = (wish as Wish & { likes?: string }).likes;
            return (
              <article key={wish.id} className={s.comment}>
                <span className={s.cAv} aria-hidden>{wish.name.slice(0, 1).toUpperCase()}</span>
                <div className={s.cText}>
                  <small>{wish.name}</small>
                  <p>{wish.message}</p>
                  <small className={s.reply}>Balas</small>
                </div>
                <button type="button" className={s.cLike} aria-pressed={!!liked[wish.id]} aria-label={`Suka komentar ${wish.name}`}
                  onClick={() => setLiked(l => ({ ...l, [wish.id]: !l[wish.id] }))}>
                  <Lucide icon={ic.heart} size={14} color="currentColor" />{demo ? likes : liked[wish.id] ? "1" : ""}
                </button>
              </article>
            );
          })}
          <button type="button" className={s.addComment} onClick={sheets.openWish}>Tambah komentar…</button>
        </section>
      </main>

      <nav className={s.bottom} aria-label="Aksi undangan">
        <button type="button" className={s.like} onClick={sheets.openWish} aria-label="Kirim ucapan"><Lucide icon={ic.heart} size={18} color="#fe2c55" className={s.beat} /></button>
        <button type="button" className={s.rsvpBtn} onClick={sheets.openRsvp}>Konfirmasi Hadir</button>
      </nav>

      <Sheet open={sheets.sheet === "rsvp"} onClose={sheets.close} title="Konfirmasi Kehadiran" tint={tint}>
        <RsvpForm rsvp={rsvp} guestName={data.guestName} demo={demo} />
      </Sheet>
      <Sheet open={sheets.sheet === "wish"} onClose={sheets.close} title="Tulis Komentar" tint={tint}>
        <WishForm wishes={wishes} guestName={data.guestName} demo={demo} submitLabel="Kirim Komentar" />
      </Sheet>
    </ThemeShell>
  );
}
