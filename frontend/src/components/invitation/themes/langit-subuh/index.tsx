"use client";
// Theme "Langit Subuh" — langit fajar cat air basah-di-atas-basah (biru bedak, lilac, merah muda, aprikot), siluet
// kubah dan menara masjid di kejauhan yang larut dalam kabut pagi, kipas cahaya pertama di balik cakrawala; tipografi
// lapang dan minimal, potret berbentuk kapsul (desain orisinal). Tanpa figur makhluk, tanpa kaligrafi yang digambar.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, toDate, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Cormorant Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500", "Nunito Sans:wght@400;600;700", "Amiri:wght@400"];
// Painted by /tmp/pen/art/themes/langit-subuh.py (tools/art/themes in the repo).
const Art = makeArt("langit-subuh", { skyline: [780, 300], rays: [780, 560], divider: [300, 29], sun: [110, 32] } as const);
const BISMILLAH = "بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ";

const COPY = {
  ...DEFAULT_COPY,
  opening: {
    arabic: BISMILLAH,
    kicker: "Assalamu'alaikum Warahmatullahi Wabarakatuh",
    title: "Di Ambang Fajar",
    intro: "Dengan memohon rahmat dan rida Allah Subhanahu wa Ta'ala, kami bermaksud menyelenggarakan pernikahan putra-putri kami. Merupakan kehormatan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"] as [string, string],
  couple: ["Atas Izin Allah", "Kedua Mempelai"] as [string, string],
  count: ["Menanti Fajar", "Menuju Hari Akad"] as [string, string],
  units: ["Hari", "Jam", "Menit", "Detik"] as [string, string, string, string],
  events: ["Waktu & Tempat", "Rangkaian Acara"] as [string, string],
  story: ["Perlahan Terang", "Kisah Kami"] as [string, string],
  gallery: ["Galeri", "Pagi-Pagi Kami"] as [string, string],
  wishes: ["Doa & Kehadiran", "Ucapan & Konfirmasi"] as [string, string],
  gifts: ["Tanda Kasih", "Amplop Digital"] as [string, string],
  closing: {
    thanks: "Jazakumullah Khairan",
    text: "Kehadiran dan doa restu Bapak/Ibu/Saudara/i adalah cahaya pertama bagi hari baru kami. Semoga Allah membalas setiap kebaikan dengan yang lebih baik.",
    salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh",
  },
  sent: "Jazakumullah khairan, doa dan ucapan Anda sudah terkirim.",
  wishPlaceholder: "Tuliskan doa terbaik untuk kedua mempelai…",
};

export default function LangitSubuhTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Walimatul 'Ursy";
  const photo = data.gallery[0] ?? data.couple.bridePhoto ?? data.couple.groomPhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const year = toDate(data.date)?.getFullYear();
  const { bride, groom } = data.couple;

  return (
    <ThemeShell
      fonts={FONTS}
      background="#f8f2ea"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.coverTop}>
            <p className={s.coverArabic} lang="ar" dir="rtl">{BISMILLAH}</p>
            <p className={s.kicker}>{label}</p>
            <h1 className={s.coverNames}><span>{bride}</span>{groom && <><em>&amp;</em><span>{groom}</span></>}</h1>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
          </div>
          <div className={s.dawn} aria-hidden>
            <Art name="rays" eager className={s.dawnRays} />
            <Art name="skyline" eager className={s.dawnSkyline} />
          </div>
          <div className={s.coverFoot}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={15} color="#ffffff" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#3f4170"
        dark="#ffffff"
        copy={COPY}
        hero={(
          <header className={s.hero}>
            <Art name="skyline" className={s.heroSkyline} />
            {photo && <div className={s.heroPhoto}><Photo src={photo} alt={`${bride} & ${groom}`} /></div>}
            <p className={s.heroKicker}>{year ? `${label} · ${year}` : label}</p>
            <h1 className={s.heroNames}>{bride}{groom && <> <em>&amp;</em> {groom}</>}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="divider" className={s.divider} />,
          node: <Art name="sun" />,
          portrait: <Art name="sun" />,
          countDecor: <><Art name="rays" className={s.countRays} /><Art name="skyline" className={s.countSkyline} /></>,
          closingDecor: <><Art name="rays" className={s.closeRays} /><Art name="skyline" className={s.closeSkyline} /></>,
          closingEmblem: <Art name="sun" className={s.closeSun} />,
          sentArt: <Art name="sun" />,
        }}
      />
    </ThemeShell>
  );
}
