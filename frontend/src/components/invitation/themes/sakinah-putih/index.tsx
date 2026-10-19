"use client";
// Theme "Sakinah Putih" — undangan syar'i putih & hijau lembut tanpa foto: rosette kelopak, sulur daun, untaian ayat dan doa.
import { useEffect, useRef, useState, type CSSProperties, type FormEvent } from "react";
import {
  DietaryField, Extras, GuestCount, Icon, Photo, ThemeShell, Tick, dateParts, formatDate, giftInfo, guestLabel, icons, mapsHref, storyItems,
  useCopy, useCountdown, DATE_TBA, sentSummary, useRsvp, useThankYou, useWishes, type Attendance, type ThemeProps, type Wish,
} from "../kit";
import { tableLabel } from "../extras";
import type { GiftMethod, InvitationData } from "../../types";
import { celebrate } from "@/lib/celebrate";
import { Bloom, Vine } from "./ornaments";
import s from "./styles.module.css";

const FONTS = ["Lora:ital,wght@0,500;0,600;1,500", "Nunito Sans:wght@400;600;700", "Amiri:wght@400;700"];
const ATTEND: Record<Attendance, string> = { yes: "Hadir", maybe: "Ragu", no: "Berhalangan" };
const DEMO_WISHES: Wish[] = [
  { id: "w1", name: "Ummu Salamah", attendance: "yes", message: "Barakallahu lakuma wa baraka 'alaikuma wa jama'a bainakuma fii khair. Semoga menjadi keluarga yang saling menuntun ke surga." },
  { id: "w2", name: "Akhi Fahmi", attendance: "yes", message: "Alhamdulillah, ikut bahagia. Semoga Allah mudahkan segala urusan menuju hari akad." },
];
const IC = {
  landmark: ["M3 22h18", "M6 18v-7", "M10 18v-7", "M14 18v-7", "M18 18v-7", "M12 2l8 5H4z"],
  wallet: ["M19 7V4a1 1 0 0 0-1-1H5a2 2 0 0 0 0 4h15a1 1 0 0 1 1 1v4h-3a2 2 0 0 0 0 4h3a1 1 0 0 0 1-1v-2a1 1 0 0 0-1-1", "M3 5v14a2 2 0 0 0 2 2h15a1 1 0 0 0 1-1v-4"],
};

const BISMILLAH = "بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ";
const SALAM = "السَّلَامُ عَلَيْكُمْ وَرَحْمَةُ اللَّهِ وَبَرَكَاتُهُ";
const AR_RUM_21 = {
  ar: "وَمِنْ آيَاتِهِ أَنْ خَلَقَ لَكُم مِّنْ أَنفُسِكُمْ أَزْوَاجًا لِّتَسْكُنُوا إِلَيْهَا وَجَعَلَ بَيْنَكُم مَّوَدَّةً وَرَحْمَةً",
  text: "Dan di antara tanda-tanda kebesaran-Nya ialah Dia menciptakan pasangan-pasangan untukmu dari jenismu sendiri, agar kamu cenderung dan merasa tenteram kepadanya, dan Dia menjadikan di antaramu rasa kasih dan sayang.",
  source: "QS. Ar-Rum: 21",
};
const PRAYERS = [
  { tab: "Doa Nabi", source: "HR. Abu Dawud & At-Tirmidzi", ar: "بَارَكَ اللَّهُ لَكُمَا وَبَارَكَ عَلَيْكُمَا وَجَمَعَ بَيْنَكُمَا فِي خَيْرٍ", text: "Semoga Allah memberkahi kalian berdua, melimpahkan keberkahan atas kalian, dan mengumpulkan kalian berdua dalam kebaikan." },
  { tab: "Al-Furqan", source: "QS. Al-Furqan: 74", ar: "رَبَّنَا هَبْ لَنَا مِنْ أَزْوَاجِنَا وَذُرِّيَّاتِنَا قُرَّةَ أَعْيُنٍ وَاجْعَلْنَا لِلْمُتَّقِينَ إِمَامًا", text: "Ya Tuhan kami, anugerahkanlah kepada kami pasangan kami dan keturunan kami sebagai penyenang hati, dan jadikanlah kami pemimpin bagi orang-orang yang bertakwa." },
  { tab: "Adz-Dzariyat", source: "QS. Adz-Dzariyat: 49", ar: "وَمِن كُلِّ شَيْءٍ خَلَقْنَا زَوْجَيْنِ لَعَلَّكُمْ تَذَكَّرُونَ", text: "Dan segala sesuatu Kami ciptakan berpasang-pasangan agar kamu mengingat (kebesaran Allah)." },
  { tab: "An-Nur", source: "QS. An-Nur: 32", ar: "إِن يَكُونُوا فُقَرَاءَ يُغْنِهِمُ اللَّهُ مِن فَضْلِهِ ۗ وَاللَّهُ وَاسِعٌ عَلِيمٌ", text: "Jika mereka miskin, Allah akan memberi kemampuan kepada mereka dengan karunia-Nya. Dan Allah Mahaluas (pemberian-Nya), Maha Mengetahui." },
];

const isWedding = (label?: string) => !label || /nikah|wedding|walimah|akad|resepsi|ngunduh/i.test(label);

function fatherName(parents?: string) {
  return /(?:Bapak|Bpk\.?|Bp\.?)\s+([^&,\n]+)/i.exec(parents ?? "")?.[1].trim() || undefined;
}

type Person = { role: string; name: string; parents?: string };

/** No photos in this theme: names, roles and parents only. */
function peopleOf(data: InvitationData): Person[] {
  const c = data.couple;
  const child = data.extras?.child;
  if (!isWedding(data.eventLabel) && child?.name && child.enabled !== false) return [{ role: data.eventLabel ?? "Yang berbahagia", name: child.name, parents: child.parents }];
  const list: Person[] = [{ role: "Mempelai Wanita", name: c.brideFull || c.bride, parents: c.brideParents }];
  if (c.groom) list.push({ role: "Mempelai Pria", name: c.groomFull || c.groom, parents: c.groomParents });
  return list;
}

function verseOf(data: InvitationData): { ar?: string; text: string; source?: string } {
  const q = data.extras?.quote;
  if (q && q.enabled !== false && q.text?.trim()) return { ar: /rum\W*21/i.test(q.source ?? "") ? AR_RUM_21.ar : undefined, text: q.text.trim(), source: q.source };
  return AR_RUM_21;
}

function giftIcon(gift: GiftMethod) {
  return gift.type === "bank" ? IC.landmark : gift.type === "ewallet" ? IC.wallet : gift.type === "address" ? icons.gift : icons.copy;
}

function Head({ id, kicker, title }: { id: string; kicker?: string; title: string }) {
  return (
    <div className={s.head}>
      {kicker && <p className={s.kicker}>{kicker}</p>}
      <h2 id={id}>{title}</h2>
      <Vine className={s.vine} />
    </div>
  );
}

export default function SakinahPutihTheme({ data, slug, guestToken, demo, skipCover }: ThemeProps) {
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
  // Story text only: this theme shows no photos at all.
  const stories = storyItems(data);
  const [tab, setTab] = useState(0);
  const [attendance, setAttendance] = useState<Attendance>("yes");
  const sentRef = useRef<HTMLDivElement>(null);
  useEffect(() => { if (wishes.status === "sent") celebrate(sentRef.current); }, [wishes.status]);
  const guestDefault = data.guestName && data.guestName !== "Tamu Undangan" ? data.guestName : "";
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const families = people.map(p => fatherName(p.parents)).filter((name): name is string => Boolean(name));
  const prayer = PRAYERS[tab];

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
      background="#eef5ef"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Bloom className={s.coverBloom} />
          <p className={s.arabic} lang="ar" dir="rtl">{BISMILLAH}</p>
          <p className={s.kicker}>{wedding ? "Undangan Walimatul 'Ursy" : `Undangan ${label}`}</p>
          <h1 className={s.coverNames}>
            <span>{data.couple.bride}</span>
            {data.couple.groom && <><small aria-hidden>&amp;</small><span>{data.couple.groom}</span></>}
          </h1>
          <Vine className={s.vine} />
          <p className={s.coverDate}>{parts.day ? `${parts.weekday}, ${parts.day} ${parts.month} ${parts.year}` : DATE_TBA}</p>
          <div className={s.kepada}>
            <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
            <strong>{guestLabel(data)}</strong>
            {table && <span>{table}</span>}
          </div>
          <button type="button" className={s.btn} onClick={open}><Icon d={icons.mailOpen} size={16} />Buka Undangan</button>
        </section>
      )}
    >
      <main className={s.page}>
        <section className={s.opening} aria-label="Pembuka">
          <Bloom className={s.openingBloom} />
          <p className={s.arabicLg} lang="ar" dir="rtl">{BISMILLAH}</p>
          <p className={s.arabic} lang="ar" dir="rtl">{SALAM}</p>
          <h2 className={s.salam}>Assalamu&apos;alaikum Warahmatullahi Wabarakatuh</h2>
          <p className={s.lead}>
            Dengan memohon rahmat dan ridha Allah SWT, kami bermaksud menyelenggarakan {wedding ? "walimatul 'ursy" : `acara ${label.toLowerCase()}`} putra-putri kami.
            Kehadiran dan doa Bapak/Ibu/Saudara/i adalah kebahagiaan bagi kami.
          </p>
          <h1 className={s.openingNames}>{names}</h1>
          <p className={s.kicker}>{formatDate(data.date)}</p>
        </section>

        <section className={s.section} aria-label="Ayat pilihan">
          <figure className={s.ayat}>
            {verse.ar && <p className={s.arabic} lang="ar" dir="rtl">{verse.ar}</p>}
            <blockquote>&ldquo;{verse.text}&rdquo;</blockquote>
            {verse.source && <figcaption className={s.ayatSrc}>{verse.source}</figcaption>}
          </figure>
          {note && <p className={s.lead}>{note}</p>}
        </section>

        <Extras slot="opening" without={["quote"]} />

        <section className={`${s.section} ${s.tint}`} aria-labelledby="sp-couple">
          <Head id="sp-couple" kicker="Dengan izin Allah" title={wedding ? "Kedua Mempelai" : "Yang Berbahagia"} />
          <div className={s.couple}>
            <div className={s.monogram} aria-hidden>
              <Bloom />
              <b>{data.couple.bride.slice(0, 1).toUpperCase()}{data.couple.groom && <><i>&amp;</i>{data.couple.groom.slice(0, 1).toUpperCase()}</>}</b>
            </div>
            {people.map((person, index) => (
              <div key={person.role} className={s.couple}>
                {index > 0 && <span className={s.and} aria-hidden>&amp;</span>}
                <article className={s.person}>
                  <small>{person.role}</small>
                  <h3>{person.name}</h3>
                  {person.parents && <p>{person.parents}</p>}
                </article>
              </div>
            ))}
          </div>
        </section>

        <section className={s.section} aria-labelledby="sp-count">
          <Head id="sp-count" kicker="Insya Allah" title="Menuju Hari Akad" />
          {countdown.valid ? (
            <div className={s.count} role="timer" aria-label={`${countdown.days} hari ${countdown.hours} jam ${countdown.minutes} menit ${countdown.seconds} detik lagi`}>
              {([[countdown.days, "Hari"], [countdown.hours, "Jam"], [countdown.minutes, "Menit"], [countdown.seconds, "Detik"]] as const).map(([value, unit]) => (
                <div key={unit} className={s.countBox} aria-hidden><b><Tick value={value} /></b><span>{unit}</span></div>
              ))}
            </div>
          ) : <p className={s.tba}>{DATE_TBA}</p>}
        </section>

        <section className={`${s.section} ${s.tint}`} aria-labelledby="sp-events">
          <Head id="sp-events" kicker="Waktu & tempat" title="Rangkaian Acara" />
          <div className={s.events}>
            {data.events.map((event, index) => {
              const ep = dateParts(event.date);
              const maps = mapsHref(data, event);
              return (
                <article key={event.name + index} className={s.event}>
                  <div className={s.eventDay} aria-hidden>{ep.day ? <><small>{ep.weekdayShort}</small><b>{ep.day}</b><small>{ep.monthShort}</small></> : <small>TBA</small>}</div>
                  <div className={s.eventBody}>
                    <h3>{event.name}</h3>
                    <p>{formatDate(event.date)}</p>
                    {event.time && <p className={s.time}><Icon d={icons.clock} size={14} />{event.time}</p>}
                    <p className={s.venue}>{event.venue}</p>
                    {event.address && <p>{event.address}</p>}
                    {maps && <a className={s.btnSoft} href={maps} target="_blank" rel="noreferrer"><Icon d={icons.mapPin} size={14} />Lihat Lokasi</a>}
                  </div>
                </article>
              );
            })}
          </div>
        </section>

        <Extras slot="event" />

        <section className={s.section} aria-labelledby="sp-doa">
          <Head id="sp-doa" kicker="Ayat & doa" title="Untaian Doa" />
          <div className={s.tabs} role="tablist" aria-label="Pilih doa" style={{ "--n": PRAYERS.length, "--k": tab } as CSSProperties}>
            <span className={s.tabPill} aria-hidden />
            {PRAYERS.map((item, index) => (
              <button key={item.tab} type="button" role="tab" id={`sp-tab-${index}`} aria-selected={tab === index} aria-controls="sp-panel" onClick={() => setTab(index)}>{item.tab}</button>
            ))}
          </div>
          <div key={tab} id="sp-panel" role="tabpanel" aria-labelledby={`sp-tab-${tab}`} className={s.panel}>
            <p className={s.arabic} lang="ar" dir="rtl">{prayer.ar}</p>
            <blockquote>&ldquo;{prayer.text}&rdquo;</blockquote>
            <p className={s.ayatSrc}>{prayer.source}</p>
          </div>
        </section>

        {stories.length > 0 && (
          <section className={`${s.section} ${s.tint}`} aria-labelledby="sp-story">
            <Head id="sp-story" kicker="Atas takdir-Nya" title="Kisah Kami" />
            <ol className={s.stories}>
              {stories.map((story, index) => (
                <li key={story.title + index} className={s.story}>
                  <Bloom className={s.storyDot} />
                  {story.date && <small>{story.date}</small>}
                  <h3>{story.title}</h3>
                  <p>{story.body}</p>
                </li>
              ))}
            </ol>
          </section>
        )}

        <Extras slot="story" />

        <Extras slot="end" />

        {data.gifts.length > 0 && (
          <section className={s.section} aria-labelledby="sp-gift">
            <Head id="sp-gift" kicker="Tanda kasih" title="Kado & Amplop" />
            <p className={s.lead}>Doa restu Anda adalah hadiah terindah. Bagi yang ingin memberi tanda kasih, dapat melalui:</p>
            <div className={s.gifts}>
              {data.gifts.map(gift => {
                const info = giftInfo(gift);
                const on = Boolean(info.copy) && copied === info.copy;
                return (
                  <div key={gift.id} className={on ? `${s.gift} ${s.giftOn}` : s.gift}>
                    <span className={s.giftIcon}><Icon d={giftIcon(gift)} size={18} /></span>
                    <div className={s.giftText}>
                      <small>{info.title}</small>
                      {info.number && <strong>{info.number}</strong>}
                      {info.holder && <span>a.n. {info.holder}</span>}
                      {info.image && <Photo src={info.image} alt="Kode QRIS" className={s.qris} />}
                    </div>
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

        <section className={`${s.section} ${s.tint}`} aria-labelledby="sp-rsvp">
          <Head id="sp-rsvp" kicker="Konfirmasi & doa" title="Doa dan Kehadiran" />
          {wishes.status === "sent" ? (
            <div ref={sentRef} className={`${s.card} ${s.sentCard}`} role="status">
              <Bloom className={s.sentBloom} />
              <p className={s.sent}>Jazakumullahu khairan. {demo ? "Ini pratinjau — doamu muncul di daftar." : sentSummary(rsvp, wishes)}</p>
              <button type="button" className={s.btnWide} onClick={() => { wishes.reset(); rsvp.reset(); }}>Tulis Lagi</button>
            </div>
          ) : (
            <form className={s.card} onSubmit={onSend}>
              <label className={s.field}><span>Nama</span><input name="name" required maxLength={100} defaultValue={guestDefault} placeholder="Nama Anda" autoComplete="name" /></label>
              <label className={s.field}><span>Doa &amp; ucapan</span><textarea name="message" required maxLength={500} rows={3} placeholder="Tuliskan doa untuk kedua mempelai…" /></label>
              {rsvpClosed ? (
                <div className={s.closed} role="status"><strong>Konfirmasi kehadiran sudah ditutup</strong><p>Terima kasih atas doa dan perhatiannya. Doa &amp; ucapan masih bisa dikirim lewat form ini.</p></div>
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
              <button type="submit" className={s.btnWide} disabled={wishes.status === "sending"}>{wishes.status === "sending" ? "Mengirim…" : "Kirim Doa"}</button>
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
          <Bloom className={s.closingBloom} />
          <p className={s.lead}>Merupakan suatu kehormatan dan kebahagiaan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.</p>
          <p className={s.arabic} lang="ar" dir="rtl">جَزَاكُمُ اللَّهُ خَيْرًا</p>
          <h2>Wassalamu&apos;alaikum Warahmatullahi Wabarakatuh</h2>
          <Vine className={s.vine} />
          <p className={s.families}>Kami yang berbahagia<br /><b>{names}</b>{families.length > 0 && <><br />beserta keluarga {families.join(" & ")}</>}</p>
          <a href="/" target="_blank" rel="noreferrer" className={s.credit}>dibuat dengan ♥ di Rawuh</a>
        </footer>
      </main>
    </ThemeShell>
  );
}
