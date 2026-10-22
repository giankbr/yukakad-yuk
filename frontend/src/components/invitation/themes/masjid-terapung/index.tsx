"use client";
// Theme "Masjid Terapung" — masjid putih orisinal di atas tiang-tiang di laut saat senja (desain orisinal): kubah lebar,
// satu menara ramping, jendela lengkung yang menyala, dermaga panjang, bayangan panjang yang dipecah riak air, langit
// jingga ke nila. Potret berbingkai jendela lengkung yang memantul di air. Tanpa figur makhluk hidup.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, toDate, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Prata", "Alegreya Sans:ital,wght@0,400;0,500;1,400", "Italianno", "Amiri:wght@400;700"];
// Painted by /tmp/pen/art/themes/masjid-terapung.py (tools/art/themes in the repo).
const Art = makeArt("masjid-terapung", { mosque: [420, 374], ripple: [340, 43], window: [60, 93] } as const);

const BISMILLAH = "بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ";

const COPY = {
  ...DEFAULT_COPY,
  opening: {
    arabic: BISMILLAH,
    kicker: "Assalamu'alaikum Warahmatullahi Wabarakatuh",
    title: "Walimatul 'Ursy",
    intro: "Dengan memohon rahmat dan ridha Allah Subhanahu wa Ta'ala, kami bermaksud menyelenggarakan pernikahan putra-putri kami. Merupakan kehormatan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"] as [string, string],
  couple: ["Atas Izin Allah", "Kedua Mempelai"] as [string, string],
  count: ["Menanti Senja", "Menuju Hari Bahagia"] as [string, string],
  units: ["hari", "jam", "menit", "detik"] as [string, string, string, string],
  events: ["Waktu & Tempat", "Rangkaian Acara"] as [string, string],
  story: ["Riak Demi Riak", "Kisah Kami"] as [string, string],
  gallery: ["Galeri", "Pantulan Kenangan"] as [string, string],
  wishes: ["Doa & Kehadiran", "Ucapan & Konfirmasi"] as [string, string],
  gifts: ["Tanda Kasih", "Amplop Digital"] as [string, string],
  closing: {
    thanks: "Terima Kasih",
    text: "Atas kehadiran dan doa restu Bapak/Ibu/Saudara/i, kami sekeluarga mengucapkan terima kasih. Semoga Allah membalas setiap kebaikan dengan kebaikan yang berlipat.",
    salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh",
  },
  sent: "Jazakumullah khairan, doa dan ucapan Anda sudah terkirim.",
  wishPlaceholder: "Tuliskan doa terbaik untuk kedua mempelai…",
};

export default function MasjidTerapungTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Walimatul 'Ursy";
  const photo = data.gallery[0] ?? data.couple.bridePhoto ?? data.couple.groomPhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const year = toDate(data.date)?.getFullYear();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#3a3560"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <span className={s.shimmer} aria-hidden />
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
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={15} color="#2b2a52" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#ffd9a0"
        dark="#2b2a52"
        copy={COPY}
        hero={(
          <header className={s.hero}>
            <div className={s.heroPhoto}>
              {photo ? <Photo src={photo} alt={`${data.couple.bride} & ${data.couple.groom}`} /> : <span className={s.monogram} aria-hidden>{data.couple.bride.slice(0, 1)}</span>}
            </div>
            <Art name="ripple" className={s.waterline} />
            <p className={s.heroKicker}>{year ? `${label} · ${year}` : label}</p>
            <h1 className={s.heroNames}>{data.couple.bride} <em>&amp;</em> {data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="ripple" className={s.divider} />,
          node: <Art name="window" />,
          amp: <Art name="window" />,
          closingEmblem: <Art name="mosque" className={s.closingEmblem} />,
          sentArt: <Art name="window" />,
        }}
      />
    </ThemeShell>
  );
}
