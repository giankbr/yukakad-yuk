"use client";
// Theme "Belitung Granit" — cat air pantai ala Belitung (desain orisinal): batu granit raksasa yang licin di pasir
// putih, air toska yang jernih, pulau kecil bermercusuar di cakrawala, dan angin laut yang tenang. Sapaan Melayu-Islami,
// potret berbentuk batu kali, hitung mundur di atas batu granit di air dangkal. Tanpa figur makhluk hidup.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, toDate, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Italiana", "Karla:ital,wght@0,400;0,500;0,600;1,400", "Amiri:wght@400;700"];
// Painted by /tmp/pen/art/themes/belitung-granit.py (tools/art/themes in the repo).
const Art = makeArt("belitung-granit", { rocks: [460, 219], isle: [300, 178], foam: [340, 36], pebble: [100, 115] } as const);

const BISMILLAH = "بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ";

const COPY = {
  ...DEFAULT_COPY,
  opening: {
    arabic: BISMILLAH,
    kicker: "Assalamu'alaikum Warahmatullahi Wabarakatuh",
    title: "Walimatul 'Urus",
    intro: "Dengan memohon rahmat dan ridha Allah Subhanahu wa Ta'ala, kami bermaksud menyelenggarakan majelis pernikahan putra-putri kami. Merupakan suatu kehormatan apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"] as [string, string],
  couple: ["Dengan Rahmat Allah", "Kedua Mempelai"] as [string, string],
  count: ["Menghitung Hari", "Menuju Hari Bersanding"] as [string, string],
  units: ["hari", "jam", "menit", "detik"] as [string, string, string, string],
  events: ["Majelis", "Waktu & Tempat"] as [string, string],
  story: ["Riwayat", "Kisah Kami"] as [string, string],
  gallery: ["Kenangan", "Galeri"] as [string, string],
  wishes: ["Doa Restu", "Ucapan & Kehadiran"] as [string, string],
  gifts: ["Tanda Kasih", "Amplop Digital"] as [string, string],
  closing: {
    thanks: "Terima Kasih",
    text: "Kehadiran serta doa restu Bapak/Ibu/Saudara/i amatlah kami harapkan. Semoga Allah membalas segala kebaikan dengan kebaikan yang berlipat.",
    salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh",
  },
  sent: "Jazakumullah khairan, doa dan ucapan Anda sudah terkirim.",
  wishPlaceholder: "Tuliskan doa terbaik untuk kedua mempelai…",
};

export default function BelitungGranitTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Walimatul 'Urus";
  const photo = data.gallery[0] ?? data.couple.bridePhoto ?? data.couple.groomPhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const year = toDate(data.date)?.getFullYear();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#f7f3ea"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <span className={s.breeze} aria-hidden />
          <span className={s.beam} aria-hidden />
          <div className={s.coverTop}>
            <p className={s.coverArabic} lang="ar" dir="rtl">{BISMILLAH}</p>
            <p className={s.kicker}>{label}</p>
            <h1 className={s.coverNames}><span>{data.couple.bride}</span><em>&amp;</em><span>{data.couple.groom}</span></h1>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
          </div>
          <div className={s.coverBottom}>
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
        light="#ffffff"
        dark="#17657e"
        copy={COPY}
        hero={(
          <header className={s.hero}>
            <Art name="isle" className={s.heroIsle} />
            <div className={s.heroFrame}>
              <div className={s.heroPhoto}>
                {photo ? <Photo src={photo} alt={`${data.couple.bride} & ${data.couple.groom}`} /> : <span className={s.monogram} aria-hidden>{data.couple.bride.slice(0, 1)}</span>}
              </div>
              <Art name="rocks" className={s.heroRocks} />
            </div>
            <p className={s.heroKicker}>{year ? `${label} · ${year}` : label}</p>
            <h1 className={s.heroNames}>{data.couple.bride} <em>&amp;</em> {data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="foam" className={s.divider} />,
          node: <Art name="pebble" />,
          closingEmblem: <Art name="isle" className={s.closingEmblem} />,
          closingDecor: <Art name="rocks" className={s.closingDecor} />,
          sentArt: <Art name="pebble" />,
        }}
      />
    </ThemeShell>
  );
}
