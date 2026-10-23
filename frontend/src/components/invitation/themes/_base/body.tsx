"use client";
// Shared page body for the painted-theme families (adat Jawa and every theme built on it since). Each theme brings its
// own cover, hero, CSS module (the class names used below) and painted art; this file only holds the section structure
// and behaviour so all of them stay feature-identical. `celebrant` switches the people section to the person being
// celebrated (khitan, aqiqah, ulang tahun, wisuda...), `copy` sets every heading/label.
import { useEffect, useRef, useState, type ReactNode } from "react";
import {
  DATE_TBA, DietaryField, Extras, GuestCount, Lucide, Photo, Tick, coupleLabel, formatDate, giftInfo, mapsHref, storyItems,
  toDate, useCopy, useCountdown, useMusic, useRsvp, useThankYou, useWishes, type Attendance, type ThemeProps,
} from "../kit";
import type { InvitationData } from "../../types";
import { celebrate } from "@/lib/celebrate";
import { ic } from "./icons";

export { ic };

export const ATTEND: Record<Attendance, string> = { yes: "Hadir", maybe: "Insyaallah", no: "Berhalangan" };

/** Demo wishes in Javanese (adat-Jawa themes pass these as `demoWishes`). */
export const JAWA_WISHES = [
  { id: "w1", name: "Bude Sri & Pakde Harjo", attendance: "yes" as Attendance, message: "Sugeng nempuh gesang enggal. Mugi dados kulawarga ingkang ayem tentrem, rukun, lan tansah pinaringan berkah." },
  { id: "w2", name: "Dimas Ardiansyah", attendance: "yes" as Attendance, message: "Selamat ya! Semoga langgeng sampai kakek-nenek, saling menguatkan di setiap musim." },
  { id: "w3", name: "Keluarga Tjokro", attendance: "maybe" as Attendance, message: "Nyuwun pangapunten kalau belum bisa hadir. Doa kami menyertai kalian berdua." },
];

/** Neutral demo wishes used by default. */
export const DEMO_WISHES = [
  { id: "w1", name: "Keluarga Bapak Hartono", attendance: "yes" as Attendance, message: "Selamat dan bahagia selalu. Semoga acaranya lancar dan penuh berkah." },
  { id: "w2", name: "Dimas Ardiansyah", attendance: "yes" as Attendance, message: "Ikut bahagia! Sampai jumpa di hari H, semoga semuanya berjalan indah." },
  { id: "w3", name: "Rina & Keluarga", attendance: "maybe" as Attendance, message: "Mohon maaf kalau belum bisa hadir. Doa terbaik kami menyertai." },
];

export type JawiCopy = {
  opening: { kicker?: string; title: string; sub?: string; intro: string; arabic?: string };
  /** Role labels above the two people (wedding) or above the celebrant. */
  roles?: [string, string];
  couple: [string, string];
  count: [string, string];
  units: [string, string, string, string];
  events: [string, string];
  story: [string, string];
  gallery: [string, string];
  wishes: [string, string];
  gifts: [string, string];
  closing: { thanks: string; text: string; salam?: string };
  sent: string;
  /** Attendance choice labels (e.g. "Mungkin" instead of "Insyaallah" for non-Muslim couples). */
  attend?: Partial<Record<Attendance, string>>;
  /** Placeholder of the wish textarea. */
  wishPlaceholder?: string;
  /** Text shown when RSVP is closed (thank-you mode). */
  closedNote?: string;
  /** Sentence above the gift cards (e.g. infaq wording). */
  giftIntro?: string;
  /** Title of the address (send-a-gift) card; defaults to "Kirim Kado". */
  giftAddressTitle?: string;
  /** Label of the wish textarea; defaults to "Ucapan & Doa". */
  wishLabel?: string;
  /** Label above the family names in the closing; `null` hides the family line. */
  familyLabel?: string | null;
};

export const DEFAULT_COPY: JawiCopy = {
  opening: {
    kicker: "Sugeng Rawuh",
    title: "Nyuwun Pangestu",
    intro: "Dengan memohon rahmat Tuhan Yang Maha Esa, kami bermaksud menyelenggarakan pahargyan pernikahan putra-putri kami. Merupakan kehormatan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
  },
  couple: ["Sigaraning Nyawa", "Mempelai"],
  count: ["Ngetung Dina", "Menuju Hari Bahagia"],
  units: ["Dina", "Jam", "Menit", "Detik"],
  events: ["Rerangkening Adicara", "Rangkaian Acara"],
  story: ["Lelampahan", "Kisah Kami"],
  gallery: ["Galeri", "Momen Bahagia"],
  wishes: ["Pandonga & Rawuh", "Ucapan & Konfirmasi"],
  gifts: ["Tanda Katresnan", "Amplop Digital"],
  closing: { thanks: "Matur Nuwun", text: "Kehadiran dan doa restu Bapak/Ibu/Saudara/i merupakan kebahagiaan yang tak ternilai bagi kami sekeluarga." },
  sent: "Matur nuwun, doa dan ucapan Anda sudah terkirim.",
};

export function father(parents?: string) {
  const match = /(?:Bapak|Bpk\.?)\s+([^&\n]+?)\s*(?:&|\n|$)/i.exec(parents ?? "");
  return match?.[1].trim();
}

export function plainName(guest?: string) {
  if (!guest || guest === "Tamu Undangan") return "";
  return guest.replace(/^(bapak|ibu|bpk\.?|sdr\.?|saudara|saudari)\s+/i, "").replace(/\s*(&|dan)\s*keluarga$/i, "").trim();
}

export function calendarHref(data: InvitationData) {
  const start = toDate(data.events[0]?.date ?? data.date);
  if (!start) return undefined;
  const lastStart = toDate(data.events[data.events.length - 1]?.date) ?? start;
  const end = new Date(Math.max(start.getTime(), lastStart.getTime()) + 3 * 3600e3);
  const fmt = (d: Date) => d.toISOString().replace(/[-:]|\.\d{3}/g, "");
  const params = new URLSearchParams({
    action: "TEMPLATE", text: `${data.eventLabel ?? "Pernikahan"} ${coupleLabel(data)}`, dates: `${fmt(start)}/${fmt(end)}`,
    location: [data.place, data.address].filter(Boolean).join(", "),
  });
  return `https://calendar.google.com/calendar/render?${params.toString()}`;
}

function Head({ s, id, kicker, title, divider }: { s: Record<string, string>; id: string; kicker?: string; title: string; divider: ReactNode }) {
  return (
    <div className={s.head}>
      {kicker && <p className={s.eyebrow}>{kicker}</p>}
      <h2 id={id}>{title}</h2>
      {divider}
    </div>
  );
}

type Slots = {
  /** Painted divider under every section heading. */
  divider: ReactNode;
  /** Ornament inside each timeline node. */
  node?: ReactNode;
  /** Ornament on both sides of the "&" between bride and groom. */
  amp?: ReactNode;
  /** Painted ornament shown over each portrait frame. */
  portrait?: ReactNode;
  /** Decoration layered behind the countdown band. */
  countDecor?: ReactNode;
  /** Decoration layered behind the closing (bottom). */
  closingDecor?: ReactNode;
  /** Emblem above "Matur Nuwun". */
  closingEmblem?: ReactNode;
  /** Ornament shown when a wish was sent. */
  sentArt?: ReactNode;
};

export function ThemeBody({ data, slug, guestToken, demo, s, copy = DEFAULT_COPY, slots, hero, noPhotos = false, celebrant = false, demoWishes = DEMO_WISHES, light = "#f3dfae", dark = "#2b1a12" }: ThemeProps & {
  s: Record<string, string>;
  copy?: JawiCopy;
  slots: Slots;
  hero: ReactNode;
  /** No-photo theme: portraits become monograms and the gallery only shows uploaded photos. */
  noPhotos?: boolean;
  /** Non-wedding event: the people section shows the celebrant (extras.child, else bride [+ groom]). */
  celebrant?: boolean;
  /** Seed wishes shown in the demo. */
  demoWishes?: typeof DEMO_WISHES;
  /** Icon colours on dark (light) and on light (dark) surfaces. */
  light?: string;
  dark?: string;
}) {
  const attendLabel = { ...ATTEND, ...copy.attend };
  const countdown = useCountdown(data.date);
  const rsvp = useRsvp({ slug, guestToken, demo });
  const wishes = useWishes({ slug, guestToken, demo, seed: demoWishes });
  const thanks = useThankYou();
  const rsvpClosed = thanks.active || rsvp.status === "closed";
  const { copy: copyText, copied } = useCopy();
  const music = useMusic(data.music);
  const [attendance, setAttendance] = useState<Attendance>("yes");
  const stories = storyItems(data);
  const calendar = calendarHref(data);

  const sentRef = useRef<HTMLDivElement>(null);
  useEffect(() => { if (wishes.status === "sent") celebrate(sentRef.current); }, [wishes.status]);
  const child = data.extras?.child?.enabled !== false && data.extras?.child?.name?.trim() ? data.extras.child : undefined;
  const couple = celebrant && child ? (child.nickname?.trim() || child.name.trim()) : celebrant && !data.couple.groom?.trim() ? data.couple.bride : coupleLabel(data);
  const families = (celebrant && child ? [father(child.parents)] : [father(data.couple.brideParents), father(data.couple.groomParents)]).filter(Boolean).join(" & ");
  const roles = copy.roles ?? (celebrant ? [data.eventLabel ?? "Acara", "Bersama"] : ["Mempelai Putri", "Mempelai Kakung"]);
  const people = celebrant
    ? (child
      ? [{ role: roles[0], nick: child.nickname?.trim() || child.name.trim(), name: child.name.trim(), parents: child.parents?.trim() || data.couple.brideParents, photo: noPhotos ? undefined : child.photo || data.couple.bridePhoto }]
      : [
        { role: roles[0], nick: data.couple.bride, name: data.couple.brideFull ?? data.couple.bride, parents: data.couple.brideParents, photo: noPhotos ? undefined : data.couple.bridePhoto },
        ...(data.couple.groom?.trim() ? [{ role: roles[1], nick: data.couple.groom, name: data.couple.groomFull ?? data.couple.groom, parents: data.couple.groomParents, photo: noPhotos ? undefined : data.couple.groomPhoto }] : []),
      ])
    : [
      { role: roles[0], nick: data.couple.bride, name: data.couple.brideFull ?? data.couple.bride, parents: data.couple.brideParents, photo: noPhotos ? undefined : data.couple.bridePhoto },
      { role: roles[1], nick: data.couple.groom, name: data.couple.groomFull ?? data.couple.groom, parents: data.couple.groomParents, photo: noPhotos ? undefined : data.couple.groomPhoto },
    ];

  return (
    <>
      <main className={s.main}>
        {hero}

        <section className={s.salamBlock} aria-label="Salam pembuka">
          {copy.opening.arabic && <p className={s.arabic} lang="ar" dir="rtl">{copy.opening.arabic}</p>}
          {copy.opening.kicker && <p className={s.salamKicker}>{copy.opening.kicker}</p>}
          <p className={s.salamTitle}>{copy.opening.title}</p>
          {copy.opening.sub && <p className={s.salamSub}>{copy.opening.sub}</p>}
          {slots.divider}
          <p className={s.intro}>{copy.opening.intro}</p>
        </section>

        <Extras slot="opening" without={celebrant && child ? ["child"] : []} />

        <section className={`${s.section} ${s.couple}`} aria-labelledby="jw-couple">
          <Head s={s} divider={slots.divider} id="jw-couple" kicker={copy.couple[0]} title={copy.couple[1]} />
          {people.map((person, index) => (
            <div key={person.role} className={s.personWrap}>
              {index === 1 && !celebrant && <div className={s.amp} aria-hidden>{slots.amp}<span>&amp;</span>{slots.amp}</div>}
              <article className={s.person}>
                <div className={s.portrait}>
                  {slots.portrait}
                  <div className={s.portraitFrame}>
                    {person.photo ? <Photo src={person.photo} alt={person.name} /> : <span className={s.monogram} aria-hidden>{person.nick.slice(0, 1)}</span>}
                  </div>
                </div>
                <p className={s.role}>{person.role}</p>
                <h3 className={s.nick}>{person.nick}</h3>
                <p className={s.fullName}>{person.name}</p>
                {person.parents && <p className={s.parents}>{person.parents}</p>}
              </article>
            </div>
          ))}
        </section>

        <section className={`${s.section} ${s.countBand}`} aria-labelledby="jw-count">
          {slots.countDecor}
          <div className={s.headLight}><p className={s.eyebrow}>{copy.count[0]}</p><h2 id="jw-count">{copy.count[1]}</h2></div>
          {countdown.valid ? (
            <div className={s.count} role="timer" aria-label={`${countdown.days} hari ${countdown.hours} jam ${countdown.minutes} menit lagi`}>
              {[countdown.days, countdown.hours, countdown.minutes, countdown.seconds].map((value, i) => (
                <div key={copy.units[i]}><b><Tick value={value} /></b><small>{copy.units[i]}</small></div>
              ))}
            </div>
          ) : <p className={s.countTba}>{DATE_TBA}</p>}
          {calendar && <a className={s.ghostBtn} href={calendar} target="_blank" rel="noreferrer"><Lucide icon={ic.calendarPlus} size={15} color={light} />Simpan ke Kalender</a>}
        </section>

        <section className={`${s.section} ${s.events}`} aria-labelledby="jw-events">
          <Head s={s} divider={slots.divider} id="jw-events" kicker={copy.events[0]} title={copy.events[1]} />
          {data.events.map((event, index) => {
            const maps = mapsHref(data, event);
            return (
              <article key={event.name + index} className={s.event}>
                <span className={s.eventNo} aria-hidden>{String(index + 1).padStart(2, "0")}</span>
                <h3>{event.name}</h3>
                <p className={s.eventDate}>{formatDate(event.date || data.date)}</p>
                {event.time && <p className={s.eventTime}><Lucide icon={ic.clock} size={14} color="currentColor" />{event.time}</p>}
                <span className={s.rule} aria-hidden />
                {event.venue && <strong>{event.venue}</strong>}
                {event.address && <p className={s.eventAddr}>{event.address}</p>}
                {maps && <a className={s.mapBtn} href={maps} target="_blank" rel="noreferrer"><Lucide icon={ic.mapPin} size={14} color="currentColor" />Petunjuk Lokasi</a>}
              </article>
            );
          })}
        </section>

        <Extras slot="event" without={["calendar"]} />

        {stories.length > 0 && (
          <section className={`${s.section} ${s.story}`} aria-labelledby="jw-story">
            <Head s={s} divider={slots.divider} id="jw-story" kicker={copy.story[0]} title={copy.story[1]} />
            <ol className={s.timeline}>
              {stories.map((story, index) => (
                <li key={index}>
                  <span className={s.node} aria-hidden>{slots.node}</span>
                  <div className={s.storyBody}>
                    {story.date && <small>{story.date}</small>}
                    <h3>{story.title}</h3>
                    {story.body && <p>{story.body}</p>}
                    {story.image && <Photo src={story.image} alt={story.title} className={s.storyImg} />}
                  </div>
                </li>
              ))}
            </ol>
          </section>
        )}

        <Extras slot="story" />

        {data.gallery.length > 0 && (
          <section className={`${s.section} ${s.gallery}`} aria-labelledby="jw-gallery">
            <Head s={s} divider={slots.divider} id="jw-gallery" kicker={copy.gallery[0]} title={copy.gallery[1]} />
            <div className={s.mosaic}>
              {data.gallery.map((src, index) => <Photo key={src + index} src={src} alt={`Foto galeri ${index + 1}`} className={s.tile} />)}
            </div>
          </section>
        )}

        <section className={`${s.section} ${s.wishes}`} aria-labelledby="jw-wishes">
          <Head s={s} divider={slots.divider} id="jw-wishes" kicker={copy.wishes[0]} title={copy.wishes[1]} />
          {wishes.status === "sent" ? (
            <div ref={sentRef} className={`${s.form} ${s.sentBox}`} role="status">
              {slots.sentArt}
              <p className={s.sent}>{copy.sent}</p>
              {!demo && wishes.pending && <p className={s.sentNote}>Ucapan akan tampil setelah disetujui.</p>}
              {demo && <p className={s.sentNote}>Ini pratinjau, ucapan hanya tampil di daftar.</p>}
              <button type="button" className={s.submit} onClick={() => { wishes.reset(); rsvp.reset(); }}>Tulis Lagi</button>
            </div>
          ) : (
            <form className={s.form} onSubmit={event => {
              event.preventDefault();
              const form = new FormData(event.currentTarget);
              const name = String(form.get("name") ?? "").trim();
              const message = String(form.get("message") ?? "").trim();
              const guests = attendance === "no" ? 1 : Number(form.get("guests") ?? 1) || 1;
              if (!name || !message) return;
              void wishes.send(name, message);
              if (!rsvpClosed && rsvp.status !== "sent") void rsvp.submit({ name, attendance, guests, diet: String(form.get("diet") ?? "").trim() || undefined });
            }}>
              <label className={s.field}><span>Nama</span><input name="name" required maxLength={100} defaultValue={plainName(data.guestName)} placeholder="Nama Anda" autoComplete="name" /></label>
              <label className={s.field}><span>{copy.wishLabel ?? "Ucapan & Doa"}</span><textarea name="message" required maxLength={500} rows={3} placeholder={copy.wishPlaceholder ?? (celebrant ? "Tuliskan doa dan ucapan terbaik…" : "Tuliskan doa restu untuk kedua mempelai…")} /></label>
              {rsvpClosed ? <div className={s.closed} role="status"><strong>Konfirmasi kehadiran sudah ditutup</strong><p>{copy.closedNote ?? "Terima kasih atas doa dan perhatiannya. Ucapan masih bisa dikirim lewat form ini."}</p></div> : (
                <div className={s.choices} role="radiogroup" aria-label="Kehadiran">
                  {(["yes", "maybe", "no"] as Attendance[]).map(value => (
                    <button key={value} type="button" role="radio" aria-checked={attendance === value} className={attendance === value ? s.choiceOn : undefined} onClick={() => setAttendance(value)}>{attendLabel[value]}</button>
                  ))}
                </div>
              )}
              {!rsvpClosed && attendance !== "no" && <GuestCount label="Jumlah tamu" className={s.guests} labelClassName={s.guestsLabel} buttonClassName={s.step} />}
              {!rsvpClosed && attendance !== "no" && <DietaryField className={`${s.field} ${s.diet}`} />}
              {wishes.status === "error" && <p className={s.error} role="alert">Belum terkirim. Coba lagi sebentar lagi.</p>}
              <button type="submit" className={s.submit} disabled={wishes.status === "sending"}>{wishes.status === "sending" ? "Mengirim…" : "Kirim Ucapan"}</button>
            </form>
          )}
          {wishes.wishes.length === 0 && <p className={s.empty}>Belum ada ucapan. Jadilah yang pertama mendoakan.</p>}
          <div className={s.wishList}>
            {wishes.wishes.slice(0, 10).map(wish => (
              <article key={wish.id} className={s.wish}>
                <div><strong>{wish.name}</strong>{wish.attendance && <small>{attendLabel[wish.attendance]}</small>}</div>
                <p>{wish.message}</p>
              </article>
            ))}
          </div>
        </section>

        {data.gifts.length > 0 && (
          <section className={`${s.section} ${s.gifts}`} aria-labelledby="jw-gift">
            <Head s={s} divider={slots.divider} id="jw-gift" kicker={copy.gifts[0]} title={copy.gifts[1]} />
            <p className={s.intro}>{copy.giftIntro ?? "Doa restu Anda adalah kado terindah bagi kami. Jika berkenan memberi tanda kasih, dapat melalui:"}</p>
            {data.gifts.map(gift => {
              const info = giftInfo(gift);
              const isCopied = !!info.copy && copied === info.copy;
              const title = gift.type === "bank" ? (/^bank/i.test(info.title) ? info.title : `Bank ${info.title}`) : gift.type === "address" ? (copy.giftAddressTitle ?? "Kirim Kado") : info.title;
              const icon = gift.type === "bank" ? ic.landmark : gift.type === "address" ? ic.gift : gift.type === "qris" ? ic.qrCode : ic.wallet;
              return (
                <div key={gift.id} className={isCopied ? `${s.gift} ${s.giftCopied}` : s.gift}>
                  <div className={s.giftTop}>
                    <span className={s.giftIcon}><Lucide icon={icon} size={18} color={light} /></span>
                    <h3>{title}</h3>
                  </div>
                  {info.number && <strong className={s.giftNo}>{info.number}</strong>}
                  {info.holder && <small>a.n. {info.holder}</small>}
                  {info.image && <Photo src={info.image} alt="Kode QRIS" className={s.qris} />}
                  {info.copy && (
                    <button type="button" className={isCopied ? `${s.copy} ${s.copyOn}` : s.copy} onClick={() => copyText(info.copy)}>
                      <Lucide key={isCopied ? "on" : "off"} icon={isCopied ? ic.check : ic.copy} size={14} color={isCopied ? dark : light} />
                      {isCopied ? "Tersalin" : gift.type === "address" ? "Salin Alamat" : "Salin Nomor"}
                    </button>
                  )}
                </div>
              );
            })}
          </section>
        )}

        <Extras slot="end" />

        <footer className={s.closing}>
          {slots.closingDecor}
          {slots.closingEmblem}
          <p className={s.thanks}>{copy.closing.thanks}</p>
          <p className={s.closingText}>{copy.closing.text}</p>
          {copy.closing.salam && <p className={s.closingSalam}>{copy.closing.salam}</p>}
          {copy.familyLabel !== null && <p className={s.family}>{copy.familyLabel ?? "Keluarga Besar"}<br />{families || couple}</p>}
          <p className={s.closingNames}>{couple}</p>
          <a href="/" target="_blank" rel="noreferrer" className={s.made}>dibuat dengan ♥ di Rawuh</a>
        </footer>
      </main>

      {music.visible && !music.failed && (
        <button type="button" className={music.playing ? `${s.music} ${s.musicOn}` : s.music} onClick={music.toggle} aria-pressed={music.playing} aria-label={music.playing ? "Matikan musik" : "Putar musik"}>
          <Lucide icon={ic.music} size={18} color={light} />
        </button>
      )}
    </>
  );
}

/** Decorative painted art (never opens the lightbox). */
export function makeArt<T extends Record<string, readonly [number, number]>>(theme: string, sizes: T) {
  return function Art({ name, className, eager }: { name: keyof T & string; className?: string; eager?: boolean }) {
    const [w, h] = sizes[name];
    return (
      // eslint-disable-next-line @next/next/no-img-element -- decorative painted ornament, static asset
      <img src={`/themes/art/${theme}/${name}.webp`} alt="" aria-hidden width={w} height={h} className={className} data-nolightbox draggable={false}
        loading={eager ? "eager" : "lazy"} fetchPriority={eager ? "high" : undefined} decoding="async" />
    );
  };
}

/** @deprecated name kept for the adat-Jawa themes. */
export const JawiBody = ThemeBody;
export type ThemeCopy = JawiCopy;
