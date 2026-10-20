"use client";
// Theme "Masjid Biru" — undangan islami biru malam: siluet kubah & menara, lentera bergoyang, dan pola bintang delapan.
import type { CSSProperties } from "react";
import {
  Extras, Icon, Photo, RsvpForm, Sheet, ThemeShell, Tick, WishForm, dateParts, formatDate, giftInfo, guestLabel, icons, mapsHref, storyItems,
  timeAgo, useCopy, useCountdown, useSheets, useThankYou, useWishes, useRsvp, DATE_TBA, type ThemeProps, type Wish,
} from "../kit";
import { tableLabel } from "../extras";
import type { InvitationData } from "../../types";
import { Crescent, Lantern, Skyline, Star8, TILE } from "./ornaments";
import s from "./styles.module.css";

const FONTS = ["Marcellus", "Mulish:ital,wght@0,400;0,600;0,700;1,400", "Amiri:wght@400;700"];
const DEMO_WISHES: Wish[] = [
  { id: "w1", name: "Ustadz Hanafi Lubis", attendance: "yes", message: "Barakallahu lakuma. Semoga menjadi pasangan yang saling menguatkan dalam ketaatan." },
  { id: "w2", name: "Teman-teman Remaja Masjid", attendance: "yes", message: "Masya Allah, ikut bahagia! Semoga sakinah, mawaddah, warahmah sampai jannah." },
  { id: "w3", name: "Rania & Keluarga", attendance: "maybe", message: "Doa terbaik dari kami di Bandung. Semoga dilancarkan hingga hari H." },
];
const ATTEND = { yes: "Hadir", maybe: "Ragu", no: "Berhalangan" } as const;

const BISMILLAH = "بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ";
const ADZ_DZARIYAT_49 = {
  ar: "وَمِن كُلِّ شَيْءٍ خَلَقْنَا زَوْجَيْنِ لَعَلَّكُمْ تَذَكَّرُونَ",
  text: "Dan segala sesuatu Kami ciptakan berpasang-pasangan agar kamu mengingat (kebesaran Allah).",
  source: "QS. Adz-Dzariyat: 49",
};
const AR_RUM_21_AR = "وَجَعَلَ بَيْنَكُم مَّوَدَّةً وَرَحْمَةً";
const DOAS = [
  { title: "Doa untuk pengantin", ar: "بَارَكَ اللَّهُ لَكُمَا وَبَارَكَ عَلَيْكُمَا وَجَمَعَ بَيْنَكُمَا فِي خَيْرٍ", text: "Semoga Allah memberkahi kalian berdua dan mengumpulkan kalian dalam kebaikan." },
  { title: "QS. Al-Furqan: 74", ar: "رَبَّنَا هَبْ لَنَا مِنْ أَزْوَاجِنَا وَذُرِّيَّاتِنَا قُرَّةَ أَعْيُنٍ", text: "Ya Tuhan kami, anugerahkanlah kepada kami pasangan dan keturunan sebagai penyejuk hati kami." },
];

const isWedding = (label?: string) => !label || /nikah|wedding|walimah|akad|resepsi|ngunduh/i.test(label);

function fatherName(parents?: string) {
  return /(?:Bapak|Bpk\.?|Bp\.?)\s+([^&,\n]+)/i.exec(parents ?? "")?.[1].trim() || undefined;
}

type Person = { role: string; name: string; short: string; parents?: string; photo?: string };

function peopleOf(data: InvitationData): Person[] {
  const c = data.couple;
  const child = data.extras?.child;
  if (!isWedding(data.eventLabel) && child?.name && child.enabled !== false) {
    return [{ role: data.eventLabel ?? "Yang berbahagia", name: child.name, short: child.nickname || child.name, parents: child.parents, photo: child.photo }];
  }
  const list: Person[] = [{ role: "Mempelai Wanita", name: c.brideFull || c.bride, short: c.bride, parents: c.brideParents, photo: c.bridePhoto }];
  if (c.groom) list.push({ role: "Mempelai Pria", name: c.groomFull || c.groom, short: c.groom, parents: c.groomParents, photo: c.groomPhoto });
  return list;
}

function verseOf(data: InvitationData): { ar?: string; text: string; source?: string } {
  const q = data.extras?.quote;
  if (q && q.enabled !== false && q.text?.trim()) return { ar: /rum\W*21/i.test(q.source ?? "") ? AR_RUM_21_AR : undefined, text: q.text.trim(), source: q.source };
  return ADZ_DZARIYAT_49;
}

function Head({ id, kicker, title }: { id: string; kicker?: string; title: string }) {
  return (
    <div className={s.head}>
      <Star8 className={s.headStar} />
      {kicker && <p className={s.kicker}>{kicker}</p>}
      <h2 id={id}>{title}</h2>
    </div>
  );
}

export default function MasjidBiruTheme({ data, slug, guestToken, demo, skipCover }: ThemeProps) {
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
  const sheets = useSheets();
  const { copy, copied } = useCopy();
  const stories = storyItems(data);
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const families = people.map(p => fatherName(p.parents)).filter((name): name is string => Boolean(name));
  const tile = { "--tile": TILE } as CSSProperties;

  return (
    <ThemeShell
      fonts={FONTS}
      background="#050b1d"
      skipCover={skipCover}
      className={s.root}
      style={tile}
      cover={open => (
        <section className={s.cover}>
          <div className={s.sky} aria-hidden><i className={s.stars} /><i className={`${s.stars} ${s.starsB}`} /></div>
          <div className={s.lanterns} aria-hidden>
            <Lantern className={s.lantern} drop={40} eager />
            <Lantern className={`${s.lantern} ${s.lanternB}`} drop={96} eager />
            <Lantern className={`${s.lantern} ${s.lanternC}`} drop={20} eager />
          </div>
          <Crescent className={s.moon} eager />
          <div className={s.coverInner}>
            <p className={s.arabic} lang="ar" dir="rtl">{BISMILLAH}</p>
            <p className={s.kicker}>{wedding ? "Undangan Walimatul 'Ursy" : `Undangan ${label}`}</p>
            <h1 className={s.coverNames}>{names}</h1>
            <p className={s.coverDate}>{parts.day ? `${parts.weekday} · ${parts.day} ${parts.month} ${parts.year}` : DATE_TBA}</p>
            <div className={s.kepada}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span>{table}</span>}
            </div>
            <button type="button" className={s.btn} onClick={open}><Icon d={icons.mailOpen} size={16} />Buka Undangan</button>
          </div>
          <Skyline className={s.skyline} eager />
        </section>
      )}
    >
      <main className={s.page}>
        <section className={s.hero} aria-label="Pembuka">
          <div className={s.sky} aria-hidden><i className={s.stars} /></div>
          <div className={s.lanterns} aria-hidden>
            <Lantern className={s.lantern} drop={24} />
            <Lantern className={`${s.lantern} ${s.lanternC}`} drop={60} />
          </div>
          <div className={s.heroText}>
            <p className={s.kicker}>Assalamu&apos;alaikum Warahmatullahi Wabarakatuh</p>
            <h1 className={s.heroNames}>{names}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
          </div>
          <Skyline className={s.skyline} />
        </section>

        <section className={s.intro} aria-label="Salam pembuka">
          <p className={s.lead}>
            Dengan memohon rahmat dan ridha Allah SWT, kami bermaksud mengundang Bapak/Ibu/Saudara/i untuk hadir dan
            memberikan doa restu pada {wedding ? "pernikahan" : `acara ${label.toLowerCase()}`} kami.
          </p>
          {note && <p className={s.note}>{note}</p>}
          <figure className={s.verse}>
            {verse.ar && <p className={s.arabic} lang="ar" dir="rtl">{verse.ar}</p>}
            <blockquote>&ldquo;{verse.text}&rdquo;</blockquote>
            {verse.source && <figcaption>{verse.source}</figcaption>}
          </figure>
        </section>

        <Extras slot="opening" without={["quote"]} />

        <section className={s.section} aria-labelledby="mb-people">
          <Head id="mb-people" kicker="Bismillah" title={wedding ? "Kedua Mempelai" : "Yang Berbahagia"} />
          <div className={s.people}>
            {people.map((person, index) => (
              <article key={person.role} className={s.person}>
                <div className={s.medal}>
                  <div className={s.medalInner}>
                    {person.photo ? <Photo src={person.photo} alt={person.name} /> : <b aria-hidden>{person.short.slice(0, 1).toUpperCase()}</b>}
                  </div>
                </div>
                <small>{person.role}</small>
                <h3>{person.name}</h3>
                {person.parents && <p>{person.parents}</p>}
                {index === 0 && people.length > 1 && <span className={s.amp} aria-hidden>&amp;</span>}
              </article>
            ))}
          </div>
        </section>

        <section className={`${s.section} ${s.deep}`} aria-labelledby="mb-count">
          <Head id="mb-count" kicker="Insya Allah" title="Menghitung Hari" />
          {countdown.valid ? (
            <div className={s.count} role="timer" aria-label={`${countdown.days} hari ${countdown.hours} jam ${countdown.minutes} menit ${countdown.seconds} detik lagi`}>
              {([[countdown.days, "Hari"], [countdown.hours, "Jam"], [countdown.minutes, "Menit"], [countdown.seconds, "Detik"]] as const).map(([value, unit]) => (
                <div key={unit} className={s.countItem} aria-hidden>
                  <div className={s.countStar}><b><Tick value={value} /></b></div>
                  <span>{unit}</span>
                </div>
              ))}
            </div>
          ) : <p className={s.tba}>{DATE_TBA}</p>}
        </section>

        <section className={s.section} aria-labelledby="mb-events">
          <Head id="mb-events" kicker="Waktu & tempat" title="Rangkaian Acara" />
          <div className={s.events}>
            {data.events.map((event, index) => {
              const maps = mapsHref(data, event);
              return (
                <article key={event.name + index} className={s.event}>
                  <span className={s.eventNo} aria-hidden>{String(index + 1).padStart(2, "0")}</span>
                  <h3>{event.name}</h3>
                  <ul className={s.eventMeta}>
                    <li><Icon d={icons.calendar} size={15} />{formatDate(event.date)}</li>
                    {event.time && <li><Icon d={icons.clock} size={15} />{event.time}</li>}
                    <li><Icon d={icons.mapPin} size={15} /><span><strong>{event.venue}</strong>{event.address && <><br />{event.address}</>}</span></li>
                  </ul>
                  {maps && <a className={s.btnLine} href={maps} target="_blank" rel="noreferrer">Buka Peta<Icon d={icons.arrowRight} size={15} /></a>}
                </article>
              );
            })}
          </div>
        </section>

        <Extras slot="event" />

        {stories.length > 0 && (
          <section className={`${s.section} ${s.deep}`} aria-labelledby="mb-story">
            <Head id="mb-story" kicker="Takdir terbaik-Nya" title="Perjalanan Kami" />
            <ol className={s.stories}>
              {stories.map((story, index) => (
                <li key={story.title + index} className={s.story}>
                  <Lantern className={s.storyLantern} drop={4} />
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
          <section className={s.section} aria-labelledby="mb-gallery">
            <Head id="mb-gallery" kicker="Jendela kenangan" title="Galeri" />
            <div className={s.gallery}>
              {data.gallery.map((src, index) => (
                <div key={src + index} className={s.window}><Photo src={src} alt={`Foto galeri ${index + 1}`} /></div>
              ))}
            </div>
          </section>
        )}

        <Extras slot="story" />

        <section className={`${s.section} ${s.deep}`} aria-labelledby="mb-doa">
          <Head id="mb-doa" kicker="Mohon diaminkan" title="Doa untuk Kami" />
          <div className={s.doas}>
            {DOAS.map(doa => (
              <article key={doa.title} className={s.doa}>
                <small>{doa.title}</small>
                <p className={s.arabic} lang="ar" dir="rtl">{doa.ar}</p>
                <p>{doa.text}</p>
              </article>
            ))}
          </div>
        </section>

        <Extras slot="end" />

        {data.gifts.length > 0 && (
          <section className={s.section} aria-labelledby="mb-gift">
            <Head id="mb-gift" kicker="Tanda kasih" title="Hadiah Pernikahan" />
            <p className={s.lead}>Kehadiran dan doa Anda sudah lebih dari cukup. Bila ingin berbagi tanda kasih:</p>
            <div className={s.gifts}>
              {data.gifts.map(gift => {
                const info = giftInfo(gift);
                const on = Boolean(info.copy) && copied === info.copy;
                return (
                  <div key={gift.id} className={on ? `${s.gift} ${s.giftOn}` : s.gift}>
                    <div className={s.giftHead}><small>{info.kind}</small><strong>{info.title}</strong></div>
                    {info.number && <p className={gift.type === "address" ? s.giftAddr : s.giftNo}>{info.number}</p>}
                    {info.holder && <span className={s.giftHolder}>a.n. {info.holder}</span>}
                    {info.image && <Photo src={info.image} alt="Kode QRIS" className={s.qris} />}
                    {info.copy && (
                      <button type="button" className={on ? `${s.copy} ${s.copyOn}` : s.copy} onClick={() => copy(info.copy)} aria-label={on ? "Tersalin" : `Salin ${gift.type === "address" ? "alamat" : "nomor"}`}>
                        <Icon key={on ? "on" : "off"} d={on ? icons.check : icons.copy} size={16} />
                      </button>
                    )}
                  </div>
                );
              })}
            </div>
          </section>
        )}

        <section className={`${s.section} ${s.deep}`} aria-labelledby="mb-rsvp">
          <Head id="mb-rsvp" kicker="Konfirmasi & doa" title="Kehadiran dan Ucapan" />
          {rsvpClosed ? (
            <div className={s.closed} role="status"><strong>Konfirmasi kehadiran sudah ditutup</strong><p>Terima kasih atas doa dan perhatiannya. Ucapan &amp; doa masih bisa dikirim.</p></div>
          ) : rsvp.status === "sent" ? (
            <p className={s.closed} role="status"><strong>Jazakumullahu khairan, konfirmasi Anda sudah kami terima.</strong></p>
          ) : (
            <p className={s.lead}>Mohon konfirmasi kehadiran Anda agar kami dapat mempersiapkan jamuan dengan baik.</p>
          )}
          <div className={s.actions}>
            {!rsvpClosed && rsvp.status !== "sent" && <button type="button" className={s.btn} onClick={() => sheets.openRsvp()}><Icon d={icons.check} size={16} />Konfirmasi Kehadiran</button>}
            <button type="button" className={s.btnLine} onClick={sheets.openWish}><Icon d={icons.messageCircle} size={15} />Kirim Ucapan &amp; Doa</button>
          </div>
          {wishes.wishes.length > 0 && (
            <div className={s.wishes}>
              {wishes.wishes.slice(0, 8).map(wish => (
                <article key={wish.id} className={s.wish}>
                  <span className={s.wishAvatar} aria-hidden>{wish.name.slice(0, 1).toUpperCase()}</span>
                  <div>
                    <p className={s.wishHead}><strong>{wish.name}</strong>{wish.attendance && <span>{ATTEND[wish.attendance]}</span>}</p>
                    <p>{wish.message}</p>
                    {wish.created_at && <small>{timeAgo(wish.created_at)}</small>}
                  </div>
                </article>
              ))}
            </div>
          )}
        </section>

        <footer className={s.closing}>
          <Crescent className={s.closingMoon} />
          <p className={s.lead}>Merupakan suatu kehormatan dan kebahagiaan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.</p>
          <p className={s.arabicSm} lang="ar" dir="rtl">وَالسَّلَامُ عَلَيْكُمْ وَرَحْمَةُ اللَّهِ وَبَرَكَاتُهُ</p>
          <h2>Wassalamu&apos;alaikum Warahmatullahi Wabarakatuh</h2>
          <p className={s.families}>Kami yang berbahagia<br /><b>{names}</b>{families.length > 0 && <><br />beserta keluarga {families.join(" & ")}</>}</p>
          <a href="/" target="_blank" rel="noreferrer" className={s.credit}>dibuat dengan ♥ di Rawuh</a>
          <Skyline className={s.closingSkyline} />
        </footer>
      </main>

      <Sheet open={sheets.sheet === "rsvp"} onClose={sheets.close} title="Konfirmasi Kehadiran">
        <RsvpForm key={sheets.attendance} rsvp={rsvp} guestName={data.guestName} demo={demo} initialAttendance={sheets.attendance} labels={{ success: "Jazakumullahu khairan!" }} />
      </Sheet>
      <Sheet open={sheets.sheet === "wish"} onClose={sheets.close} title="Ucapan & Doa">
        <WishForm wishes={wishes} guestName={data.guestName} demo={demo} submitLabel="Kirim Doa" />
      </Sheet>
    </ThemeShell>
  );
}
