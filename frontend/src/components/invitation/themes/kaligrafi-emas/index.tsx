"use client";
// Theme "Kaligrafi Emas" — undangan islami krem & emas: lengkung mihrab, rosette khatam, dan kisi bintang delapan.
import { useEffect, useRef, useState, type CSSProperties, type FormEvent } from "react";
import {
  DietaryField, Extras, GuestCount, Icon, Photo, ThemeShell, Tick, dateParts, formatDate, giftInfo, guestLabel, icons, mapsHref, storyItems,
  useCopy, useCountdown, DATE_TBA, sentSummary, useRsvp, useThankYou, useWishes, type Attendance, type ThemeProps, type Wish,
} from "../kit";
import { tableLabel } from "../extras";
import type { InvitationData } from "../../types";
import { celebrate } from "@/lib/celebrate";
import { ArchCrest, LATTICE, Rosette, Star } from "./ornaments";
import s from "./styles.module.css";

const FONTS = ["Cinzel:wght@400;600", "Cormorant Garamond:ital,wght@0,400;0,500;0,600;0,700;1,400;1,500;1,600", "Amiri:wght@400;700"];
const ATTEND: Record<Attendance, string> = { yes: "Hadir", maybe: "Ragu", no: "Berhalangan" };
const DEMO_WISHES: Wish[] = [
  { id: "w1", name: "Ustadzah Halimah", attendance: "yes", message: "Barakallahu lakuma wa baraka 'alaikuma wa jama'a bainakuma fii khair. Semoga menjadi keluarga sakinah, mawaddah, warahmah." },
  { id: "w2", name: "Keluarga Bpk. Rahmat", attendance: "yes", message: "Turut berbahagia. Semoga Allah melimpahkan keberkahan dalam setiap langkah rumah tangga kalian." },
];

const BISMILLAH = "بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ";
const SALAM = "السَّلَامُ عَلَيْكُمْ وَرَحْمَةُ اللَّهِ وَبَرَكَاتُهُ";
const AR_RUM_21 = {
  ar: "وَمِنْ آيَاتِهِ أَنْ خَلَقَ لَكُم مِّنْ أَنفُسِكُمْ أَزْوَاجًا لِّتَسْكُنُوا إِلَيْهَا وَجَعَلَ بَيْنَكُم مَّوَدَّةً وَرَحْمَةً",
  text: "Dan di antara tanda-tanda kebesaran-Nya ialah Dia menciptakan pasangan-pasangan untukmu dari jenismu sendiri, agar kamu cenderung dan merasa tenteram kepadanya, dan Dia menjadikan di antaramu rasa kasih dan sayang.",
  source: "QS. Ar-Rum: 21",
};
const DOA = {
  ar: "بَارَكَ اللَّهُ لَكُمَا وَبَارَكَ عَلَيْكُمَا وَجَمَعَ بَيْنَكُمَا فِي خَيْرٍ",
  text: "Semoga Allah memberkahi kalian berdua, melimpahkan keberkahan atas kalian, dan mengumpulkan kalian berdua dalam kebaikan.",
  source: "HR. Abu Dawud & At-Tirmidzi",
};

const isWedding = (label?: string) => !label || /nikah|wedding|walimah|akad|resepsi|ngunduh/i.test(label);

/** "Putri dari Bapak H. Abdullah & Ibu …" → "H. Abdullah". */
function fatherName(parents?: string) {
  return /(?:Bapak|Bpk\.?|Bp\.?)\s+([^&,\n]+)/i.exec(parents ?? "")?.[1].trim() || undefined;
}

type Person = { role: string; name: string; parents?: string; photo?: string; initial: string };

function peopleOf(data: InvitationData): Person[] {
  const c = data.couple;
  const child = data.extras?.child;
  if (!isWedding(data.eventLabel) && child?.name && child.enabled !== false) {
    return [{ role: data.eventLabel ?? "Yang berbahagia", name: child.name, parents: child.parents, photo: child.photo, initial: child.name.slice(0, 1) }];
  }
  const list: Person[] = [{ role: "Mempelai Wanita", name: c.brideFull || c.bride, parents: c.brideParents, photo: c.bridePhoto, initial: c.bride.slice(0, 1) }];
  if (c.groom) list.push({ role: "Mempelai Pria", name: c.groomFull || c.groom, parents: c.groomParents, photo: c.groomPhoto, initial: c.groom.slice(0, 1) });
  return list;
}

/** The invitation's own opening verse (dashboard "quote"), else QS Ar-Rum 21 with its Arabic text. */
function verseOf(data: InvitationData): { ar?: string; text: string; source?: string } {
  const q = data.extras?.quote;
  if (q && q.enabled !== false && q.text?.trim()) {
    const rum = /rum\W*21/i.test(q.source ?? "");
    return { ar: rum ? AR_RUM_21.ar : undefined, text: q.text.trim(), source: q.source };
  }
  return AR_RUM_21;
}

function Head({ id, kicker, title }: { id: string; kicker?: string; title: string }) {
  return (
    <div className={s.head}>
      {kicker && <p className={s.kicker}>{kicker}</p>}
      <h2 id={id}>{title}</h2>
      <span className={s.divider} aria-hidden><i /><Star className={s.dividerStar} /><i /></span>
    </div>
  );
}

export default function KaligrafiEmasTheme({ data, slug, guestToken, demo, skipCover }: ThemeProps) {
  const label = data.eventLabel ?? "Pernikahan";
  const wedding = isWedding(label);
  const names = data.couple.groom ? `${data.couple.bride} & ${data.couple.groom}` : data.couple.bride;
  const parts = dateParts(data.date);
  const people = peopleOf(data);
  const verse = verseOf(data);
  const countdown = useCountdown(data.date);
  const rsvp = useRsvp({ slug, guestToken, demo });
  const wishes = useWishes({ slug, guestToken, demo, seed: DEMO_WISHES });
  const thanks = useThankYou();
  const rsvpClosed = thanks.active || rsvp.status === "closed";
  const { copy, copied } = useCopy();
  const stories = storyItems(data);
  const [attendance, setAttendance] = useState<Attendance>("yes");
  const sentRef = useRef<HTMLDivElement>(null);
  useEffect(() => { if (wishes.status === "sent") celebrate(sentRef.current); }, [wishes.status]);
  const guestDefault = data.guestName && data.guestName !== "Tamu Undangan" ? data.guestName : "";
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const families = people.map(p => fatherName(p.parents)).filter((name): name is string => Boolean(name));
  const lattice = { "--lattice": LATTICE } as CSSProperties;

  const onSend = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const form = new FormData(event.currentTarget);
    const name = String(form.get("name") ?? "").trim();
    const message = String(form.get("message") ?? "").trim();
    if (!name || !message) return;
    const guests = attendance === "no" ? 1 : Number(form.get("guests") ?? 1) || 1;
    if (!rsvpClosed) void rsvp.submit({ name, attendance, guests, message, diet: String(form.get("diet") ?? "").trim() || undefined });
    void wishes.send(name, message);
  };

  return (
    <ThemeShell
      fonts={FONTS}
      background="#e9dec6"
      skipCover={skipCover}
      className={s.root}
      style={lattice}
      cover={open => (
        <section className={s.cover} style={lattice}>
          <div className={s.coverArch} aria-hidden />
          <div className={s.coverInner}>
            <Rosette className={s.coverRosette} eager />
            <p className={s.arabicSm} lang="ar" dir="rtl">{BISMILLAH}</p>
            <p className={s.kicker}>{wedding ? "Walimatul 'Ursy" : label}</p>
            <h1 className={s.coverNames}>
              {data.couple.groom ? <><span>{data.couple.bride}</span><em>&amp;</em><span>{data.couple.groom}</span></> : <span>{data.couple.bride}</span>}
            </h1>
            <p className={s.coverDate}>{parts.day ? `${parts.weekday}, ${parts.day} ${parts.month} ${parts.year}` : DATE_TBA}</p>
            <div className={s.kepada}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.btn} onClick={open}><Icon d={icons.mailOpen} size={16} />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <main className={s.page}>
        <section className={s.hero} aria-label="Pembuka">
          <div className={s.heroArch} aria-hidden />
          <Rosette className={s.heroRosette} />
          <p className={s.arabic} lang="ar" dir="rtl">{BISMILLAH}</p>
          <p className={s.kicker}>{wedding ? "Walimatul 'Ursy" : label}</p>
          <h1 className={s.heroNames}>{names}</h1>
          <p className={s.heroDate}>{formatDate(data.date)}</p>
        </section>

        <section className={s.salam} aria-label="Salam">
          <p className={s.arabicSm} lang="ar" dir="rtl">{SALAM}</p>
          <h2 className={s.salamTitle}>Assalamu&apos;alaikum Warahmatullahi Wabarakatuh</h2>
          <p className={s.lead}>
            Dengan memohon rahmat dan ridha Allah SWT, kami bermaksud menyelenggarakan {wedding ? "walimatul 'ursy" : `acara ${label.toLowerCase()}`} dan
            mengharap kehadiran serta doa restu Bapak/Ibu/Saudara/i.
          </p>
          {note && <p className={s.note}>{note}</p>}
        </section>

        <section className={s.verse} aria-label="Ayat">
          <span className={s.verseStar} aria-hidden><Star /></span>
          {verse.ar && <p className={s.arabic} lang="ar" dir="rtl">{verse.ar}</p>}
          <p className={s.verseText}>&ldquo;{verse.text}&rdquo;</p>
          {verse.source && <p className={s.verseSrc}>{verse.source}</p>}
        </section>

        <Extras slot="opening" without={["quote"]} />

        <section className={s.section} aria-labelledby="ke-people">
          <Head id="ke-people" kicker={wedding ? "Dengan izin Allah" : "Dengan penuh syukur"} title={wedding ? "Kedua Mempelai" : "Yang Berbahagia"} />
          <div className={s.people}>
            {people.map((person, index) => (
              <article key={person.role} className={s.person}>
                {index > 0 && <p className={s.amp} aria-hidden>&amp;</p>}
                <div className={s.portrait}>
                  <ArchCrest className={s.crest} />
                  {person.photo
                    ? <div className={s.portraitImg}><Photo src={person.photo} alt={person.name} /></div>
                    : <div className={`${s.portraitImg} ${s.monogram}`} aria-hidden><Rosette className={s.monoRosette} /><b>{person.initial.toUpperCase()}</b></div>}
                </div>
                <small>{person.role}</small>
                <h3>{person.name}</h3>
                {person.parents && <p>{person.parents}</p>}
              </article>
            ))}
          </div>
        </section>

        <section className={`${s.section} ${s.panel}`} aria-labelledby="ke-count">
          <Head id="ke-count" kicker="Insya Allah" title="Menuju Hari Bahagia" />
          {countdown.valid ? (
            <div className={s.count} role="timer" aria-label={`${countdown.days} hari ${countdown.hours} jam ${countdown.minutes} menit ${countdown.seconds} detik lagi`}>
              {([[countdown.days, "Hari"], [countdown.hours, "Jam"], [countdown.minutes, "Menit"], [countdown.seconds, "Detik"]] as const).map(([value, unit]) => (
                <div key={unit} className={s.countBox} aria-hidden><b><Tick value={value} /></b><span>{unit}</span></div>
              ))}
            </div>
          ) : <p className={s.tba}>{DATE_TBA}</p>}
        </section>

        <section className={s.section} aria-labelledby="ke-events">
          <Head id="ke-events" kicker="Waktu & tempat" title="Rangkaian Acara" />
          <div className={s.events}>
            {data.events.map((event, index) => {
              const ep = dateParts(event.date);
              const maps = mapsHref(data, event);
              return (
                <article key={event.name + index} className={s.event}>
                  <div className={s.eventDate}>
                    {ep.day ? <><small>{ep.weekday}</small><b>{ep.day}</b><small>{ep.month} {ep.year}</small></> : <small>{DATE_TBA}</small>}
                  </div>
                  <h3>{event.name}</h3>
                  {event.time && <p className={s.eventTime}><Icon d={icons.clock} size={14} />{event.time}</p>}
                  <p className={s.eventVenue}>{event.venue}</p>
                  {event.address && <p className={s.eventAddr}>{event.address}</p>}
                  {maps && <a className={s.btnGhost} href={maps} target="_blank" rel="noreferrer"><Icon d={icons.mapPin} size={15} />Petunjuk Lokasi</a>}
                </article>
              );
            })}
          </div>
        </section>

        <Extras slot="event" />

        {stories.length > 0 && (
          <section className={`${s.section} ${s.panel}`} aria-labelledby="ke-story">
            <Head id="ke-story" kicker="Atas takdir-Nya" title="Kisah Kami" />
            <ol className={s.stories}>
              {stories.map((story, index) => (
                <li key={story.title + index} className={s.story}>
                  <span className={s.storyMark} aria-hidden><Star /></span>
                  <div>
                    {story.date && <small>{story.date}</small>}
                    <h3>{story.title}</h3>
                    <p>{story.body}</p>
                    {story.image && <Photo src={story.image} alt={story.title} className={s.storyImg} />}
                  </div>
                </li>
              ))}
            </ol>
          </section>
        )}

        {data.gallery.length > 0 && (
          <section className={s.section} aria-labelledby="ke-gallery">
            <Head id="ke-gallery" kicker="Kenangan" title="Galeri" />
            <div className={s.gallery}>
              {data.gallery.map((src, index) => (
                <div key={src + index} className={s.frame}><Photo src={src} alt={`Foto galeri ${index + 1}`} /></div>
              ))}
            </div>
          </section>
        )}

        <Extras slot="story" />

        <section className={`${s.section} ${s.doa}`} aria-labelledby="ke-doa">
          <Head id="ke-doa" kicker="Doa untuk pengantin" title="Barakallahu Lakuma" />
          <p className={s.arabic} lang="ar" dir="rtl">{DOA.ar}</p>
          <p className={s.verseText}>&ldquo;{DOA.text}&rdquo;</p>
          <p className={s.verseSrc}>{DOA.source}</p>
        </section>

        <Extras slot="end" />

        {data.gifts.length > 0 && (
          <section className={s.section} aria-labelledby="ke-gift">
            <Head id="ke-gift" kicker="Tanda kasih" title="Amplop Digital" />
            <p className={s.lead}>Doa restu Anda adalah karunia terindah bagi kami. Bila berkenan memberi tanda kasih, dapat melalui:</p>
            <div className={s.gifts}>
              {data.gifts.map(gift => {
                const info = giftInfo(gift);
                const on = Boolean(info.copy) && copied === info.copy;
                return (
                  <div key={gift.id} className={on ? `${s.gift} ${s.giftOn}` : s.gift}>
                    <small>{info.kind}</small>
                    <strong>{info.title}</strong>
                    {info.number && <p className={gift.type === "address" ? s.giftAddr : s.giftNo}>{info.number}</p>}
                    {info.holder && <span>a.n. {info.holder}</span>}
                    {info.image && <Photo src={info.image} alt="Kode QRIS" className={s.qris} />}
                    {info.copy && (
                      <button type="button" className={on ? `${s.copy} ${s.copyOn}` : s.copy} onClick={() => copy(info.copy)}>
                        <Icon key={on ? "on" : "off"} d={on ? icons.check : icons.copy} size={14} />{on ? "Tersalin" : gift.type === "address" ? "Salin Alamat" : "Salin Nomor"}
                      </button>
                    )}
                  </div>
                );
              })}
            </div>
          </section>
        )}

        <section className={`${s.section} ${s.panel}`} aria-labelledby="ke-rsvp">
          <Head id="ke-rsvp" kicker="Konfirmasi & doa" title="Ucapan dan Kehadiran" />
          {wishes.status === "sent" ? (
            <div ref={sentRef} className={`${s.card} ${s.sentCard}`} role="status">
              <Star className={s.sentStar} />
              <p className={s.sent}>Jazakumullahu khairan. {demo ? "Ini pratinjau — ucapanmu muncul di daftar." : sentSummary(rsvp, wishes)}</p>
              <button type="button" className={s.btnWide} onClick={() => { wishes.reset(); rsvp.reset(); }}>Tulis Lagi</button>
            </div>
          ) : (
            <form className={s.card} onSubmit={onSend}>
              <label className={s.field}><span>Nama</span><input name="name" required maxLength={100} defaultValue={guestDefault} placeholder="Nama Anda" autoComplete="name" /></label>
              <label className={s.field}><span>Ucapan &amp; doa</span><textarea name="message" required maxLength={500} rows={3} placeholder="Tuliskan doa terbaik Anda…" /></label>
              {rsvpClosed ? (
                <div className={s.closed} role="status"><strong>Konfirmasi kehadiran sudah ditutup</strong><p>Terima kasih atas doa dan perhatiannya. Ucapan &amp; doa masih bisa dikirim lewat form ini.</p></div>
              ) : (
                <fieldset className={s.choices}>
                  <legend className={s.srOnly}>Kehadiran</legend>
                  {(["yes", "maybe", "no"] as const).map(value => (
                    <label key={value} className={attendance === value ? s.on : undefined}>
                      <input type="radio" name="attendance" value={value} checked={attendance === value} onChange={() => setAttendance(value)} />
                      {ATTEND[value]}
                    </label>
                  ))}
                </fieldset>
              )}
              {!rsvpClosed && attendance !== "no" && <GuestCount label="Jumlah tamu" className={s.guests} labelClassName={s.guestsLabel} buttonClassName={s.step} />}
              {!rsvpClosed && attendance !== "no" && <DietaryField className={`${s.field} ${s.diet}`} />}
              {wishes.status === "error" && <p className={s.error} role="alert">Belum terkirim. Periksa koneksi lalu coba lagi.</p>}
              <button type="submit" className={s.btnWide} disabled={wishes.status === "sending"}>{wishes.status === "sending" ? "Mengirim…" : rsvpClosed ? "Kirim Ucapan" : "Kirim Ucapan & Konfirmasi"}</button>
            </form>
          )}
          {wishes.wishes.length > 0 && (
            <div className={s.wishes}>
              {wishes.wishes.slice(0, 8).map(wish => (
                <article key={wish.id} className={s.wish}>
                  <div><strong>{wish.name}</strong>{wish.attendance && <span>{ATTEND[wish.attendance]}</span>}</div>
                  <p>{wish.message}</p>
                </article>
              ))}
            </div>
          )}
        </section>

        <footer className={s.closing}>
          <div className={s.closingArch} aria-hidden />
          <Rosette className={s.closingRosette} />
          <p className={s.closingText}>
            Merupakan suatu kehormatan dan kebahagiaan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.
          </p>
          <p className={s.arabicSm} lang="ar" dir="rtl">جَزَاكُمُ اللَّهُ خَيْرًا</p>
          <h2>Wassalamu&apos;alaikum Warahmatullahi Wabarakatuh</h2>
          <p className={s.families}>Kami yang berbahagia<br /><b>{names}</b>{families.length > 0 && <><br />beserta keluarga besar {families.join(" & ")}</>}</p>
          <a href="/" target="_blank" rel="noreferrer" className={s.credit}>dibuat dengan ♥ di Rawuh</a>
        </footer>
      </main>
    </ThemeShell>
  );
}
