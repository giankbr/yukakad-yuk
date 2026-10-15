"use client";
// Theme "Kursi Kereta" — undangan bergaya aplikasi pesan tiket kereta (design: E-Boarding Pass, Danang & Ratri).
import {
  Extras, Lucide, Photo, RsvpForm, Sheet, ThemeShell, WishForm, dateParts, formatDate, giftInfo, guestLabel,
  mapsHref, storyItems, useCopy, useRsvp, useSheets, useWishes, type ThemeProps, type ThemeTint,
} from "../kit";
import type { InvitationData } from "../../types";
import { ic } from "./icons";
import s from "./styles.module.css";

const FONTS = ["Poppins:wght@400;600;700;800"];
const tint: ThemeTint = {
  "--t-accent": "#f7941e", "--t-accent-ink": "#ffffff", "--t-bg": "#ffffff", "--t-ink": "#1e2a4a", "--t-muted": "#6b7390", "--t-line": "#e4e8f5",
  "--t-field": "#f4f6fb", "--t-radius": "12px", "--t-font": "'Poppins', system-ui, sans-serif",
};
const DEMO_WISHES = [
  { id: "w1", name: "Pak Slamet", message: "Kursi sudah dipilih, hati sudah mantap. Kami hadir sekeluarga!", created_at: new Date(Date.now() - 2 * 3600e3).toISOString() },
  { id: "w2", name: "Mbak Rini", message: "Perjalanan panjang kalian akhirnya sampai stasiun akhir. Selamat!", created_at: new Date(Date.now() - 5 * 3600e3).toISOString() },
];
const DEMO_CAPTIONS = ["Peron pertama", "Jendela favorit", "Lamaran"];
const DEMO_WISHLIST = [
  { name: "Sofa Ruang Tamu", price: "Rp2.600.000", icon: ic.sofa },
  { name: "Microwave", price: "Rp1.150.000", icon: ic.microwave },
  { name: "Koper Bulan Madu", price: "Rp1.500.000", icon: ic.luggage },
];
// Seat states for rows 2–4 (A, B, C). Demo shows the design's sample; real invitations reserve row 2 for the guest.
const DEMO_SEATS = [["in", "in", "in"], ["in", "free", "in"], ["free", "in", "free"]] as const;
const REAL_SEATS = [["you", "you", "you"], ["free", "free", "free"], ["free", "free", "free"]] as const;

type Event = InvitationData["events"][number];

function startTime(event?: Event) {
  if (!event) return "";
  return event.time?.match(/\d{1,2}[.:]\d{2}/)?.[0]?.replace(":", ".") ?? formatDate(event.date, { hour: "2-digit", minute: "2-digit" }).replace(":", ".");
}

function city(address: string) {
  const parts = address.split(",").map(part => part.trim()).filter(Boolean);
  return parts[parts.length - 1] ?? "";
}

function Status({ time }: { time: string }) {
  return (
    <div className={s.status} aria-hidden>
      {time}
      <span><Lucide icon={ic.signal} /><Lucide icon={ic.wifi} /><Lucide icon={ic.batteryFull} /></span>
    </div>
  );
}

export default function KursiKeretaTheme({ data, slug, guestToken, demo, skipCover }: ThemeProps) {
  const { bride, groom } = data.couple;
  const couple = `${groom} & ${bride}`;
  const parts = dateParts(data.date);
  const clock = "06:07";
  const longDate = formatDate(data.date);
  const shortDate = formatDate(data.date, { day: "numeric", month: "short", year: "numeric" });
  const passDate = parts.day ? `${parts.weekdayShort}, ${parts.day} ${parts.monthShort} ${parts.year}` : "";
  const where = city(data.address);
  const stories = storyItems(data);
  const firstYear = stories.map(story => story.date?.match(/\d{4}/)?.[0]).find(Boolean);
  const years = firstYear && parts.year ? Number(parts.year) - Number(firstYear) : 0;
  const depart = startTime(data.events[0]) || "08.00";
  const schedule = data.events.map(event => [event.name.split(" ")[0], startTime(event)].filter(Boolean).join(" ")).join(" · ");
  const seats = demo ? DEMO_SEATS : REAL_SEATS;

  const rsvp = useRsvp({ slug, guestToken, demo });
  const wishes = useWishes({ slug, guestToken, demo, seed: DEMO_WISHES });
  const sheets = useSheets();
  const { copy, copied } = useCopy();
  const gallery = data.gallery;
  const people = [
    { name: data.couple.groomFull ?? groom, parents: data.couple.groomParents, photo: data.couple.groomPhoto ?? gallery[1] },
    { name: data.couple.brideFull ?? bride, parents: data.couple.brideParents, photo: data.couple.bridePhoto ?? gallery[2] },
  ];

  return (
    <ThemeShell
      fonts={FONTS}
      background="#e6eaf5"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.coverHead}>
            <Status time={clock} />
            <h1>Pesan Tiket {data.eventLabel ?? "Pernikahan"}</h1>
            <div className={s.form}>
              <div className={s.formRow}>
                <Lucide icon={ic.circle} size={12} color="#f7941e" />
                <div className={s.grow}><small>Dari</small><strong>Masa Lajang (LJG)</strong></div>
              </div>
              <div className={`${s.formRow} ${s.formRow2}`}>
                <Lucide icon={ic.mapPin} size={12} color="#f7941e" />
                <div className={s.grow}><small>Ke</small><strong>Pelaminan Selamanya (SLM)</strong></div>
              </div>
            </div>
          </div>
          <div className={s.coverBody}>
            <p className={s.caption}>Hasil pencarian · {longDate}</p>
            <div className={s.result}>
              <div className={s.between}>
                <strong className={s.train}>KA CINTA ABADI (1)</strong>
                <span className={s.tag}>Eksekutif Hati</span>
              </div>
              <div className={s.route}>
                <div><b>{depart}</b><small>LJG{firstYear ? ` · ${firstYear}` : ""}</small></div>
                <div className={s.mid}>
                  <small>{years > 0 ? `${years} thn perjalanan` : "Perjalanan cinta"}</small>
                  <Lucide icon={ic.moveRight} size={24} color="#3d5be9" style={{ width: 40, height: 14 }} />
                  <em>Langsung, tanpa transit</em>
                </div>
                <div className={s.end}><b>Selamanya</b><small>SLM · {shortDate}</small></div>
              </div>
              <div className={`${s.between} ${s.resultFoot}`}>
                <span className={s.price}>Harga: cukup doa &amp; kehadiran</span>
                <span className={s.avail}>Tersedia</span>
              </div>
            </div>
            <p className={s.caption}>Pilih kursimu · Gerbong CINTA 1</p>
            <div className={s.seatmap} aria-hidden>
              <div className={s.seatRow}>
                <span>1</span>
                <i className={s.seatCouple}>{groom.slice(0, 1).toUpperCase()}</i>
                <i className={s.seatCouple}>{bride.slice(0, 1).toUpperCase()}</i>
                <b />
                <i />
              </div>
              {seats.map((row, r) => (
                <div key={r} className={s.seatRow}>
                  <span>{r + 2}</span>
                  {row.map((state, c) => (
                    <SeatCell key={c} state={state} aisle={c === 2} />
                  ))}
                </div>
              ))}
              <div className={s.legend}>
                <span><i style={{ background: "#3d5be9" }} />Mempelai</span>
                {demo ? <span><i style={{ background: "#18a45d" }} />Tamu hadir</span> : <span><i style={{ background: "#f7941e" }} />Kursimu</span>}
                <span><i style={{ background: "#cdd4e6" }} />Masih kosong</span>
              </div>
            </div>
            <div className={s.kepada}>
              <small>Penumpang Terdaftar</small>
              <strong>{guestLabel(data)}</strong>
              <p>Kursi 2A–2D sudah dipesankan untukmu</p>
            </div>
            <button type="button" className={s.orange} onClick={open}><Lucide icon={ic.armchair} size={17} color="#fff" />Pesan Kursi — Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <header className={s.top}>
        <Status time={clock} />
        <div className={s.nav}>
          <h1>E-Boarding Pass {data.eventLabel ?? "Pernikahan"}</h1>
          <p>KA Cinta Abadi · {couple}{where ? ` · ${where}` : ""}</p>
        </div>
      </header>

      <main className={s.body}>
        <section className={s.pass} aria-label="E-boarding pass">
          <div className={s.passHead}><span>E-Boarding Pass{passDate ? ` · ${passDate}` : ""}</span><Lucide icon={ic.trainFront} color="#fff" /></div>
          <div className={s.passBody}>
            <span className={s.qr} aria-hidden><Lucide icon={ic.qrCode} size={60} color="#1e2a4a" /></span>
            <div className={s.grow}>
              <strong>{couple}{schedule ? ` — ${schedule}` : ""}</strong>
              <small>Gerbong CINTA 1 · Kursi mempelai 1A-1B</small>
              <small>Lokasi: {[data.place, where].filter(Boolean).join(", ")}</small>
            </div>
          </div>
          {data.events.length > 0 && (
            <ul className={s.stops}>
              {data.events.map((event, index) => {
                const href = mapsHref(data, event);
                return (
                  <li key={event.name + index}>
                    <div className={s.grow}>
                      <strong>{event.name}</strong>
                      <small>{[formatDate(event.date, { weekday: "long", day: "numeric", month: "long" }), event.time].filter(Boolean).join(" · ")}</small>
                      <small>{[event.venue, event.address].filter(Boolean).join(", ")}</small>
                    </div>
                    {href && <a href={href} target="_blank" rel="noreferrer" className={s.mapBtn} aria-label={`Buka Maps ${event.venue}`}><Lucide icon={ic.mapPin} size={14} color="#3d5be9" />Maps</a>}
                  </li>
                );
              })}
            </ul>
          )}
        </section>

        <Extras slot="event" className={s.extras} />

        <section className={s.card} aria-labelledby="kk-crew">
          <div className={s.head}><h2 id="kk-crew">Kondektur Perjalanan</h2></div>
          {people.map(person => (
            <article key={person.name} className={s.person}>
              <Photo src={person.photo} alt={person.name} className={s.avatar} />
              <div className={s.grow}>
                <strong>{person.name}</strong>
                {person.parents && <small>{person.parents}</small>}
              </div>
              <span className={s.tag}>Resmi</span>
            </article>
          ))}
        </section>

        <Extras slot="opening" className={s.extras} />

        {stories.length > 0 && (
          <section className={s.card} aria-labelledby="kk-story">
            <div className={s.head}><h2 id="kk-story">Pemberhentian Sebelumnya</h2></div>
            <ol className={s.timeline}>
              {stories.map((story, index) => (
                <li key={story.title + index}>
                  <span className={s.rail} aria-hidden><i className={s.dot} />{index < stories.length - 1 && <i className={s.line} />}</span>
                  <div className={s.grow}>
                    <strong>{story.date ? `${story.date} · ` : ""}{story.title}</strong>
                    <p>{story.body}</p>
                    {story.image && <Photo src={story.image} alt={story.title} className={s.storyImg} />}
                  </div>
                </li>
              ))}
            </ol>
          </section>
        )}

        {gallery.length > 0 && (
          <section className={s.card} aria-labelledby="kk-gallery">
            <div className={s.head}><h2 id="kk-gallery">Galeri Perjalanan</h2><span>{gallery.length}</span></div>
            <div className={s.grid}>
              {gallery.map((src, index) => (
                <figure key={src + index}>
                  <Photo src={src} alt={`Foto perjalanan ${index + 1}`} />
                  {demo && DEMO_CAPTIONS[index] && <figcaption>{DEMO_CAPTIONS[index]}</figcaption>}
                </figure>
              ))}
            </div>
          </section>
        )}

        <Extras slot="story" className={s.extras} />
        <Extras slot="end" className={s.extras} />

        {(demo || data.gifts.length > 0) && (
          <section className={s.card} aria-labelledby="kk-gift">
            <div className={s.head}><h2 id="kk-gift">Bagasi Kado</h2>{demo && <span>Wishlist</span>}</div>
            {demo && DEMO_WISHLIST.map(item => (
              <div key={item.name} className={s.item}>
                <span className={s.itemIcon} aria-hidden><Lucide icon={item.icon} size={17} color="#3d5be9" /></span>
                <div className={s.grow}><strong>{item.name}</strong><small>{item.price}</small></div>
                <span className={s.small} aria-hidden>Beri</span>
              </div>
            ))}
            {data.gifts.map(gift => {
              const info = giftInfo(gift);
              return (
                <div key={gift.id} className={s.amplop}>
                  <Lucide icon={ic.wallet} size={17} color="#f7941e" />
                  <div className={s.grow}>
                    <strong>{gift.type === "address" ? "Alamat Kirim Kado" : gift.type === "qris" ? "QRIS" : "Amplop Digital"}</strong>
                    <small>{[gift.type === "bank" || gift.type === "ewallet" ? `${info.title} ${info.number}` : info.number, info.holder ? `a.n. ${info.holder}` : ""].filter(Boolean).join(" · ")}</small>
                    {info.image && <Photo src={info.image} alt="Kode QRIS" className={s.qris} />}
                  </div>
                  {info.copy && <button type="button" className={s.small} onClick={() => copy(info.copy)}>{copied === info.copy ? "Tersalin" : "Salin"}</button>}
                </div>
              );
            })}
          </section>
        )}

        <section className={s.card} aria-labelledby="kk-wishes">
          <div className={s.head}><h2 id="kk-wishes">Ulasan Penumpang</h2><span>{demo ? "312" : wishes.wishes.length}</span></div>
          {wishes.wishes.length === 0 && <p className={s.empty}>Belum ada ulasan. Jadilah penumpang pertama yang menulis doa!</p>}
          {wishes.wishes.slice(0, 8).map(wish => (
            <article key={wish.id} className={s.review}>
              <span className={s.initial} aria-hidden>{(wish.name.trim().split(/\s+/).pop() ?? wish.name).slice(0, 1).toUpperCase()}</span>
              <div className={s.grow}><strong>{wish.name}</strong><p>{wish.message}</p></div>
            </article>
          ))}
        </section>
      </main>

      <nav className={s.bottom} aria-label="Aksi undangan">
        <button type="button" className={s.chat} onClick={sheets.openWish} aria-label="Kirim ucapan"><Lucide icon={ic.messageCircle} size={18} color="#3d5be9" /></button>
        <button type="button" className={s.orange} onClick={sheets.openRsvp}><Lucide icon={ic.armchair} color="#fff" />Kunci Kursi — Konfirmasi Hadir</button>
      </nav>

      <Sheet open={sheets.sheet === "rsvp"} onClose={sheets.close} title="Kunci Kursi" tint={tint}>
        <RsvpForm rsvp={rsvp} guestName={data.guestName} demo={demo} labels={{ submit: "Konfirmasi Hadir" }} />
      </Sheet>
      <Sheet open={sheets.sheet === "wish"} onClose={sheets.close} title="Tulis Ulasan & Doa" tint={tint}>
        <WishForm wishes={wishes} guestName={data.guestName} demo={demo} />
      </Sheet>
    </ThemeShell>
  );
}

function SeatCell({ state, aisle }: { state: "in" | "free" | "you"; aisle: boolean }) {
  return (
    <>
      {aisle && <b />}
      <i className={state === "in" ? s.seatIn : state === "you" ? s.seatYou : undefined}>
        {state === "in" && <Lucide icon={ic.check} size={14} color="#18a45d" />}
        {state === "you" && <Lucide icon={ic.armchair} size={14} color="#f7941e" />}
      </i>
    </>
  );
}
