"use client";
// Theme "Khatam Kayu" — pintu ganda kayu walnut berukir dengan tatahan khatam ala Persia (desain orisinal): mozaik mikro
// dari segitiga kecil kayu, tulang, dan kuningan yang membentuk bintang, cincin dan paku kuningan. Halaman gading
// bergaris pita khatam, potret berbingkai lengkung, panel walnut bertatah. Geometri saja, tanpa figur makhluk hidup.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, toDate, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Reem Kufi:wght@400;500;600", "Crimson Pro:ital,wght@0,400;0,600;1,400", "Amiri:wght@400;700"];
// Painted by /tmp/pen/art/themes/khatam-kayu.py (tools/art/themes in the repo).
const Art = makeArt("khatam-kayu", { door: [480, 814], frame: [434, 588], star: [200, 200], divider: [340, 49] } as const);

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
  couple: ["Dua Kepingan", "Kedua Mempelai"] as [string, string],
  count: ["Menanti Hari", "Menuju Akad"] as [string, string],
  units: ["hari", "jam", "menit", "detik"] as [string, string, string, string],
  events: ["Waktu & Tempat", "Rangkaian Acara"] as [string, string],
  story: ["Sepotong demi Sepotong", "Kisah Kami"] as [string, string],
  gallery: ["Galeri", "Bingkai Kenangan"] as [string, string],
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

export default function KhatamKayuTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Walimatul 'Ursy";
  const photo = data.gallery[0] ?? data.couple.bridePhoto ?? data.couple.groomPhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const year = toDate(data.date)?.getFullYear();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#3a2414"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.coverTop}>
            <p className={s.coverArabic} lang="ar" dir="rtl">{BISMILLAH}</p>
            <p className={s.kicker}>{label}</p>
            <h1 className={s.coverNames}><span>{data.couple.bride}</span><em>&amp;</em><span>{data.couple.groom}</span></h1>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
          </div>
          <div className={s.doorWrap}>
            <Art name="door" className={s.door} eager />
            <span className={s.sheen} aria-hidden />
            <div className={s.plaque}>
              <div className={s.guest}>
                <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
                <strong>{guestLabel(data)}</strong>
                {table && <span className={s.table}>{table}</span>}
              </div>
              <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={15} color="#3a2414" />Buka Undangan</button>
            </div>
          </div>
          <div className={s.coverFoot} aria-hidden />
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#ecd49a"
        dark="#3a2414"
        copy={COPY}
        hero={(
          <header className={s.hero}>
            <div className={s.arch}>
              <div className={s.heroPhoto}>
                {photo ? <Photo src={photo} alt={`${data.couple.bride} & ${data.couple.groom}`} /> : <span className={s.monogram} aria-hidden>{data.couple.bride.slice(0, 1)}</span>}
              </div>
              <Art name="frame" />
            </div>
            <p className={s.heroKicker}>{year ? `${label} · ${year}` : label}</p>
            <h1 className={s.heroNames}>{data.couple.bride} <em>&amp;</em> {data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="divider" className={s.divider} />,
          node: <Art name="star" />,
          amp: <Art name="star" />,
          portrait: <Art name="star" />,
          closingEmblem: <Art name="star" className={s.closingEmblem} />,
          sentArt: <Art name="star" />,
        }}
      />
    </ThemeShell>
  );
}
