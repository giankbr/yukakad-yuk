"use client";
// Theme "Repositori" — undangan bergaya repositori kode / pull request (design: Tema Repositori (Raka & Tami)).
import { useEffect, useRef, useState, type CSSProperties } from "react";
import {
  Extras, Lucide, Photo, RsvpForm, Sheet, ThemeShell, WishForm, formatDate, giftInfo, guestLabel,
  mapsHref, storyItems, useCopy, useCountdown, useRsvp, useSheets, useWishes, type ThemeProps, type ThemeTint,
} from "../kit";
import { toast } from "@/lib/celebrate";
import { ic } from "./icons";
import s from "./styles.module.css";

const FONTS = ["Inter:wght@400;500;600;700", "JetBrains Mono:wght@400;700"];
const tint: ThemeTint = {
  "--t-accent": "#238636", "--t-accent-ink": "#ffffff", "--t-bg": "#161b22", "--t-ink": "#e6edf3", "--t-muted": "#8d96a0",
  "--t-line": "#30363d", "--t-field": "#0d1117", "--t-radius": "8px", "--t-font": "Inter, system-ui, sans-serif",
};
const DEMO_WISHES = [
  { id: "w1", name: "budi_ops", message: "LGTM! Approved tanpa revisi. Selamat Raka & Tami!", created_at: new Date(Date.now() - 2 * 3600e3).toISOString() },
  { id: "w2", name: "mbak_qa", message: "Sudah ku-test 7 tahun, zero bug. Ship it! Samawa!", created_at: new Date(Date.now() - 5 * 3600e3).toISOString() },
];
const DEMO_FILES = ["pair_programming.jpg", "rooftop_date.jpg", "proposal_demo.jpg", "deploy_day.jpg"];
/* Contribution graph (decoration): 5 rows × 24 cells, each row cycles through 3 shades. */
const GRAPH = [
  ["", "#006d32", "#26a641"], ["#39d353", "#0e4429", "#006d32"], ["#26a641", "#39d353", "#0e4429"],
  ["#006d32", "#26a641", ""], ["#0e4429", "#006d32", "#39d353"],
];
const TABS = [
  { id: "repo-mempelai", label: "Kode", icon: ic.code },
  { id: "repo-acara", label: "Undangan", icon: ic.gitPullRequest },
  { id: "repo-ucapan", label: "Ucapan", icon: ic.messageSquare },
];
const MERGE_LINE = "git merge";

function slugify(value: string) {
  return value.toLowerCase().normalize("NFKD").replace(/[^\w\s-]/g, "").trim().replace(/[\s_]+/g, "-") || "kita";
}

/** Short fake commit hash derived from text (stable, decorative). */
function hash(text: string) {
  let h = 2166136261;
  for (let i = 0; i < text.length; i++) h = Math.imul(h ^ text.charCodeAt(i), 16777619);
  return (h >>> 0).toString(16).padStart(8, "0").slice(0, 7);
}

function city(address: string) {
  const parts = address.split(",").map(part => part.trim()).filter(Boolean);
  return parts[parts.length - 1] ?? "";
}


export default function RepositoriTheme({ data, slug, guestToken, demo, skipCover }: ThemeProps) {
  const { couple } = data;
  const groom = slugify(couple.groom);
  const bride = slugify(couple.bride);
  const repo = slugify(data.eventLabel ?? "pernikahan");
  const where = city(data.address) || data.place;
  const countdown = useCountdown(data.date);
  const rsvp = useRsvp({ slug, guestToken, demo });
  const wishes = useWishes({ slug, guestToken, demo, seed: DEMO_WISHES });
  const sheets = useSheets();
  const { copy, copied } = useCopy();
  const stories = storyItems(data);
  const [starred, setStarred] = useState(false);
  const [tab, setTab] = useState(TABS[0].id);
  const [selectedTier, setTier] = useState<string>();
  const [reacted, setReacted] = useState<Record<string, boolean>>({});
  const tabsRef = useRef<HTMLElement>(null);
  // Scroll-spy: the tab of the last section whose heading passed under the sticky header is active.
  useEffect(() => {
    const onScroll = () => {
      let current = TABS[0].id;
      for (const { id } of TABS) {
        const el = document.getElementById(id);
        if (el && el.getBoundingClientRect().top < 170) current = id;
      }
      setTab(current);
    };
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);
  // Slide the underline under the active tab.
  useEffect(() => {
    const nav = tabsRef.current;
    const active = nav?.querySelector<HTMLElement>("a[aria-current]");
    if (!nav || !active) return;
    nav.style.setProperty("--ink-x", `${active.offsetLeft}px`);
    nav.style.setProperty("--ink-w", `${active.offsetWidth}px`);
  }, [tab]);
  const toggleStar = () => {
    if (!starred) toast("Repositori diberi bintang");
    setStarred(value => !value);
  };
  const noteLines = couple.note.split("\n").map(line => line.trim()).filter(Boolean);
  const people = [
    { name: couple.groomFull ?? couple.groom, handle: demo ? "@rakadev" : `@${groom}`, parents: couple.groomParents, photo: couple.groomPhoto ?? data.gallery[1], commits: "1.204 commit kesabaran" },
    { name: couple.brideFull ?? couple.bride, handle: demo ? "@tamicodes" : `@${bride}`, parents: couple.brideParents, photo: couple.bridePhoto ?? data.gallery[2], commits: "2.048 commit perhatian" },
  ];
  const fileName = (src: string, index: number) => {
    if (demo && DEMO_FILES[index]) return DEMO_FILES[index];
    const base = src.split(/[?#]/)[0].split("/").pop() ?? "";
    return /\.(jpe?g|png|webp|gif|avif)$/i.test(base) && base.length < 32 ? base : `foto_${String(index + 1).padStart(2, "0")}.jpg`;
  };

  return (
    <ThemeShell
      fonts={FONTS}
      background="#010409"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={`${s.cover} ${s.coverBody}`}>
            <div className={s.crumb}>
              <Lucide icon={ic.bookMarked} size={15} color="#8d96a0" />
              <span className={s.link}>{groom}</span><span className={s.muted}>/</span><strong className={s.link}>{repo}</strong>
              <span className={s.pill}>Public</span>
            </div>
            <div className={s.stats}>
              <button type="button" className={`${s.star} ${starred ? s.starred : ""}`} aria-pressed={starred} onClick={toggleStar}>
                <Lucide icon={ic.star} size={14} color={starred ? "#d29922" : "currentColor"} />{starred ? "Starred" : "Star"}{demo && <b>2,7rb</b>}
              </button>
              <span><Lucide icon={ic.gitFork} size={14} />2 → 1</span>
              <span><Lucide icon={ic.eye} size={14} />Semua tamu</span>
            </div>

            <div className={s.card}>
              <div><span className={s.open}><Lucide icon={ic.gitPullRequest} size={13} color="#fff" />Open</span></div>
              <h1 className={s.prTitle}>feat: menikah selamanya #1</h1>
              <div className={s.branch}>
                <code>{groom}/lajang</code><Lucide icon={ic.arrowRight} size={12} color="#8d96a0" /><code>{bride}/selamanya</code>
              </div>
              <p className={s.meta}>{formatDate(data.date)}{where ? ` · ${where}` : ""}</p>
            </div>

            <div className={`${s.card} ${s.readme}`}>
              <div className={s.fileHead}><Lucide icon={ic.fileText} size={13} />README.md</div>
              <h2 className={s.readmeTitle}># {couple.groom} &amp; {couple.bride}</h2>
              {noteLines.length > 0 && <p className={s.quote}>{noteLines.map(line => <span key={line}>&gt; {line}</span>)}</p>}
              <ul className={s.checks}>
                <li><Lucide icon={ic.circleCheck} size={14} color="#3fb950" />Restu orang tua</li>
                <li><Lucide icon={ic.circleCheck} size={14} color="#3fb950" />Cincin &amp; mahar</li>
                <li><Lucide icon={ic.circleDashed} size={14} color="#d29922" />Kehadiranmu</li>
              </ul>
            </div>

            <div className={s.guest}>
              <div className={s.guestHead}><Lucide icon={ic.userCheck} size={13} color="#a371f7" />Reviewer diundang</div>
              <strong>{guestLabel(data)}</strong>
              <small>Review Anda sangat berarti untuk merge ini.</small>
            </div>

            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.gitMerge} size={17} color="#fff" />Buka Undangan</button>

            <div className={s.term} aria-hidden>
              <code className={`${s.green} ${s.typed}`} style={{ "--n": `${`$ ${MERGE_LINE} ${bride} --forever`.length}` } as CSSProperties}>$ {MERGE_LINE} {bride} --forever</code>
              <code className={s.after}>Merging... <i className={s.mergeBar}><b /></i> 100% (∞/∞), selesai.</code>
            </div>

            <div className={s.contrib} aria-hidden>
              <code>{demo ? "2.555 hari saling kontribusi" : countdown.ready ? `${countdown.days} hari menuju merge` : "Riwayat kontribusi"}</code>
              <div className={s.graph}>
                {GRAPH.map((row, r) => (
                  <div key={r}>{Array.from({ length: 24 }, (_, i) => <i key={i} style={{ "--d": `${(i + r) * 22}ms`, ...(row[i % 3] ? { background: row[i % 3], borderColor: row[i % 3] } : {}) } as CSSProperties} />)}</div>
                ))}
              </div>
              <code className={s.tiny}>Sedikit → Banyak cinta</code>
            </div>
        </section>
      )}
    >
      <header className={s.header}>
        <div className={s.nav}>
          <Lucide icon={ic.gitBranch} size={18} color="#e6edf3" />
          <span>{groom}/{repo}</span>
          <Lucide icon={ic.bell} size={18} color="#8d96a0" />
        </div>
        <nav className={s.tabs} aria-label="Bagian undangan" ref={tabsRef}>
          {TABS.map(item => (
            <a key={item.id} href={`#${item.id}`} aria-current={tab === item.id ? "page" : undefined}><Lucide icon={item.icon} size={14} />{item.label}</a>
          ))}
          <i className={s.tabInk} aria-hidden />
        </nav>
      </header>

      <main className={s.body}>
        <Extras slot="opening" className={s.extras} />

        <section className={s.section} aria-labelledby="repo-mempelai">
          <h2 className={s.head} id="repo-mempelai"><Lucide icon={ic.users} size={16} color="#8d96a0" />contributors (2)</h2>
          {people.map(person => (
            <article key={person.name} className={s.person}>
              <Photo src={person.photo} alt={person.name} className={s.avatar} />
              <div>
                <strong>{person.name}</strong>
                <small>{[person.handle, person.parents].filter(Boolean).join(" · ")}</small>
                {demo && <code className={s.commits}><Lucide icon={ic.gitCommitHorizontal} size={12} color="#3fb950" />{person.commits}</code>}
              </div>
            </article>
          ))}
        </section>

        {stories.length > 0 && (
          <section className={s.section} aria-labelledby="repo-kisah">
            <h2 className={s.head} id="repo-kisah"><Lucide icon={ic.history} size={16} color="#8d96a0" />git log --kisah</h2>
            <ol className={s.log}>
              {stories.map((story, index) => (
                <li key={story.title + index}>
                  <span className={s.rail} aria-hidden><i /><b /></span>
                  <div className={s.commit}>
                    <div><code className={s.link}>{hash(story.title + story.body + index)}</code>{story.date && <code className={s.muted}>{story.date}</code>}</div>
                    <p>{story.title}</p>
                    {story.body && <small>{story.body}</small>}
                    {story.image && <Photo src={story.image} alt={story.title} className={s.storyImg} />}
                  </div>
                </li>
              ))}
            </ol>
          </section>
        )}

        <section className={s.section} aria-labelledby="repo-acara">
          <h2 className={s.head} id="repo-acara"><Lucide icon={ic.rocket} size={16} color="#8d96a0" />Releases ({data.events.length})</h2>
          {data.events.map((event, index) => {
            const href = mapsHref(data, event);
            return (
              <article key={event.name + index} className={`${s.card} ${s.release}`}>
                <div className={s.releaseHead}>
                  <Lucide icon={ic.tag} size={13} color="#8d96a0" />
                  <code>v{index + 1}.0.0</code>
                  <span className={index === 0 ? s.latest : s.pre}>{index === 0 ? "Latest" : "Pre-release"}</span>
                  {href && <a className={s.maps} href={href} target="_blank" rel="noreferrer" aria-label={`Buka Maps ${event.venue}`}>Maps</a>}
                </div>
                <h3>{event.name} — {formatDate(event.date, { weekday: "long", day: "numeric", month: "short", year: "numeric" })}</h3>
                <p>{[event.time, event.venue].filter(Boolean).join(" · ")}</p>
              </article>
            );
          })}
        </section>

        <Extras slot="event" className={s.extras} />

        {data.gallery.length > 0 && (
          <section className={s.section} aria-labelledby="repo-galeri">
            <h2 className={s.head} id="repo-galeri"><Lucide icon={ic.image} size={16} color="#8d96a0" />assets/prewedding/</h2>
            <div className={s.grid}>
              {data.gallery.map((src, index) => (
                <figure key={src + index} className={s.file}>
                  <Photo src={src} alt={`Foto prewedding ${index + 1}`} />
                  <figcaption><Lucide icon={ic.fileImage} size={11} color="#8d96a0" /><span>{fileName(src, index)}</span></figcaption>
                </figure>
              ))}
            </div>
          </section>
        )}

        <Extras slot="story" className={s.extras} />

        <Extras slot="end" className={s.extras} />

        {(demo || data.gifts.length > 0) && (
          <section className={s.section} aria-labelledby="repo-kado">
            <h2 className={s.head} id="repo-kado"><Lucide icon={ic.heart} size={16} color="#8d96a0" />Sponsor pernikahan ini</h2>
            {demo && (
              <>
                <div className={s.tiers}>
                  {[
                    { name: "Supporter", price: "Rp100rb", icon: ic.heart, color: "#db61a2" },
                    { name: "Backer", price: "Rp500rb", icon: ic.sparkles, color: "#58a6ff" },
                    { name: "Gold", price: "Rp1jt", icon: ic.crown, color: "#d29922" },
                  ].map(tier => (
                    <button key={tier.name} type="button" className={s.tier} aria-pressed={tier.name === selectedTier}
                      style={{ borderColor: tier.color, "--c": tier.color } as CSSProperties} onClick={() => setTier(value => value === tier.name ? undefined : tier.name)}>
                      <Lucide icon={tier.icon} size={18} color={tier.color} />
                      <strong>{tier.name}</strong>
                      <code style={{ color: tier.color }}>{tier.price}</code>
                      {tier.name === selectedTier && <em className={s.tierCheck}><Lucide icon={ic.check} size={10} color="#fff" /></em>}
                    </button>
                  ))}
                </div>
                <ul className={s.wishlist}>
                  {[
                    { name: "monitor-ultrawide.kado", price: "Rp4.500.000", icon: ic.monitor },
                    { name: "keyboard-mechanical.kado", price: "Rp1.800.000", icon: ic.keyboard },
                    { name: "sofa-ruang-kerja.kado", price: "Rp3.200.000", icon: ic.sofa },
                  ].map(item => (
                    <li key={item.name}><Lucide icon={item.icon} size={15} color="#8d96a0" /><code>{item.name}</code><small>{item.price}</small></li>
                  ))}
                </ul>
              </>
            )}
            {data.gifts.map(gift => {
              const info = giftInfo(gift);
              return (
                <div key={gift.id} className={s.amplop}>
                  <Lucide icon={ic.wallet} size={16} color="#3fb950" />
                  <div>
                    <strong>{gift.type === "address" ? "Kirim Kado" : gift.type === "qris" ? "QRIS" : "Amplop Digital"}</strong>
                    <code>{[[info.title !== "Alamat kado" && gift.type !== "qris" ? info.title : "", info.number].filter(Boolean).join(" "), info.holder ? `a.n. ${info.holder}` : ""].filter(Boolean).join(" · ")}</code>
                    {info.image && <Photo src={info.image} alt="Kode QRIS" className={s.qris} />}
                  </div>
                  {info.copy && (
                    <button type="button" className={`${s.copy} ${copied === info.copy ? s.copied : ""}`} onClick={() => copy(info.copy)}>
                      {copied === info.copy && <Lucide icon={ic.check} size={11} color="#fff" />}{copied === info.copy ? "Tersalin" : "Salin"}
                    </button>
                  )}
                </div>
              );
            })}
          </section>
        )}

        <section className={s.section} aria-labelledby="repo-ucapan">
          <h2 className={s.head} id="repo-ucapan"><Lucide icon={ic.messageSquare} size={16} color="#8d96a0" />Diskusi ({wishes.wishes.length})</h2>
          {wishes.wishes.length === 0 && <p className={s.empty}>Belum ada diskusi. Jadilah reviewer pertama!</p>}
          {wishes.wishes.slice(0, 8).map(wish => (
            <article key={wish.id} className={`${s.card} ${s.wish}`}>
              <div className={s.wishHead}>
                <span aria-hidden>{wish.name.slice(0, 1).toUpperCase()}</span>
                <code>{wish.name}</code>
                <em><Lucide icon={ic.check} size={10} color="#3fb950" />approved</em>
              </div>
              <p>{wish.message}</p>
              <button type="button" className={`${s.react} ${reacted[wish.id] ? s.reacted : ""}`} aria-pressed={!!reacted[wish.id]} aria-label={`Beri hati untuk ucapan ${wish.name}`}
                onClick={() => setReacted(state => ({ ...state, [wish.id]: !state[wish.id] }))}>
                <Lucide icon={ic.heart} size={12} color={reacted[wish.id] ? "#db61a2" : "#8d96a0"} />{reacted[wish.id] ? 1 : ""}
              </button>
            </article>
          ))}
        </section>
      </main>

      <nav className={s.bottom} aria-label="Aksi undangan">
        <button type="button" className={s.comment} onClick={sheets.openWish} aria-label="Kirim ucapan"><Lucide icon={ic.messageSquare} size={18} color="#e6edf3" /></button>
        <button type="button" className={s.rsvp} onClick={sheets.openRsvp}><Lucide icon={ic.gitMerge} size={16} color="#fff" />Merge · Konfirmasi Hadir</button>
      </nav>

      <Sheet open={sheets.sheet === "rsvp"} onClose={sheets.close} title="Konfirmasi Kehadiran" tint={tint}>
        <RsvpForm rsvp={rsvp} guestName={data.guestName} demo={demo} labels={{ submit: "Merge Kehadiran" }} />
      </Sheet>
      <Sheet open={sheets.sheet === "wish"} onClose={sheets.close} title="Tulis Komentar & Doa" tint={tint}>
        <WishForm wishes={wishes} guestName={data.guestName} demo={demo} submitLabel="Kirim Komentar" />
      </Sheet>
    </ThemeShell>
  );
}
