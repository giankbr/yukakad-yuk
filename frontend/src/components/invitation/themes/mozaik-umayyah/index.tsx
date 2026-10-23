"use client";
// Theme "Mozaik Umayyah" — mozaik kaca berlatar emas ala dinding masjid Umayyah (komposisi orisinal, tanpa figur dan
// tanpa kaligrafi lukis): pohon berbuah, cemara, paviliun bertiang dan kubah di tepi sungai, tersusun dari tessera yang
// mengikuti kontur. Sampul menaruh mozaik di bawah pelengkung, pita sulur mozaik, lalu nama di atas hijau zamrud.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["El Messiri:wght@400;500;600", "Gentium Book Plus:ital,wght@0,400;0,700;1,400", "Amiri:wght@400"];
// Rendered by /tmp/pen/art/themes/mozaik-umayyah.py (scene and frieze are CSS backgrounds)
const Art = makeArt("mozaik-umayyah", { tree: [240, 325] } as const);

const WISHES = [
  { id: "w1", name: "Ustazah Hanifah", attendance: "yes" as const, message: "Barakallahu lakuma wa baraka 'alaikuma wa jama'a bainakuma fi khair. Semoga menjadi keluarga yang sakinah, mawaddah, wa rahmah." },
  { id: "w2", name: "Teman Studio Arsitektur 2016", attendance: "yes" as const, message: "Dari debat kubah sampai pelaminan. Kami semua datang, siap jadi saksi kisah yang paling indah tersusun." },
  { id: "w3", name: "Keluarga Om Ridwan (Makassar)", attendance: "maybe" as const, message: "Insyaallah kami usahakan terbang ke Jakarta. Doa terbaik dari jauh untuk Salma dan Fadhil." },
];

export default function MozaikUmayyahTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const hero = data.gallery[0] || data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const label = data.eventLabel?.trim() || "Walimatul 'Ursy";

  return (
    <ThemeShell
      fonts={FONTS}
      background="#0b231a"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={`${s.arch} ${s.tessera}`} aria-hidden><div className={s.archInner} /></div>
          <span className={s.coverFrieze} aria-hidden />
          <p className={s.bismillah} lang="ar" dir="rtl">بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيم</p>
          <p className={s.kicker}>{label}</p>
          <h1 className={s.coverNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.guest}>
            <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
            <strong>{guestLabel(data)}</strong>
            {table && <span className={s.table}>{table}</span>}
          </div>
          <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#0f2d22" />Buka Undangan</button>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#ecd38c"
        dark="#0f2d22"
        demoWishes={WISHES}
        copy={{
          ...DEFAULT_COPY,
          opening: {
            arabic: "السَّلَامُ عَلَيْكُمْ وَرَحْمَةُ اللهِ وَبَرَكَاتُهُ",
            kicker: "Assalamu'alaikum Wr. Wb.",
            title: "Bismillahirrahmanirrahim",
            intro: "Dengan memohon rahmat dan ridha Allah SWT, kami bermaksud menyelenggarakan walimatul 'ursy putra-putri kami. Merupakan kehormatan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
          },
          roles: ["Mempelai Wanita", "Mempelai Pria"],
          couple: ["Dengan Izin Allah", "Kedua Mempelai"],
          count: ["Menghitung Hari", "Menuju Akad"],
          units: ["Hari", "Jam", "Menit", "Detik"],
          events: ["Waktu & Tempat", "Rangkaian Acara"],
          story: ["Kepingan Kisah", "Perjalanan Kami"],
          gallery: ["Galeri", "Momen Kami"],
          wishes: ["Doa & Kehadiran", "Ucapan & Konfirmasi"],
          gifts: ["Tanda Kasih", "Amplop Digital"],
          closing: {
            thanks: "Jazakumullah Khairan",
            text: "Atas kehadiran dan doa restu Bapak/Ibu/Saudara/i, kami ucapkan terima kasih. Semoga Allah membalas setiap kebaikan dengan yang lebih baik.",
            salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh",
          },
          sent: "Jazakumullah khairan, doa dan ucapan Anda sudah terkirim.",
          wishPlaceholder: "Tuliskan doa terbaik untuk kedua mempelai…",
          familyLabel: "Kami yang berbahagia",
        }}
        hero={(
          <header className={s.hero}>
            <span className={s.heroFrieze} aria-hidden />
            {hero && <div className={`${s.heroFrame} ${s.tessera}`}><div className={s.heroPhoto}><Photo src={hero} alt={`${data.couple.bride} dan ${data.couple.groom}`} /></div></div>}
            <p className={s.heroKicker}>{label}</p>
            <h1 className={s.heroNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
            <span className={s.heroScene} aria-hidden />
          </header>
        )}
        slots={{
          divider: <span className={s.divider} aria-hidden><Art name="tree" /></span>,
          node: <Art name="tree" />,
          amp: <Art name="tree" />,
          closingDecor: <span className={s.closingFrieze} aria-hidden />,
          closingEmblem: <Art name="tree" className={s.closingTree} />,
          sentArt: <Art name="tree" />,
        }}
      />
    </ThemeShell>
  );
}
