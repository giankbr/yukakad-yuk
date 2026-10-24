"use client";
// Theme "Lili Syari" — undangan syar'i tanpa foto dalam cat air bersih: satu ikat lili calla putih dan lili Madonna
// bertangkai hijau panjang diikat pita emas berdiri di kolom kiri sampul, nama dan kartu tamu rata kiri di kolom kanan,
// bingkai garis emas ganda. Halaman: bingkai bersudut takik di bawah lili Madonna, monogram dalam lengkung ramping,
// hitung mundur di kelopak lonjong pada pita hijau daun, kartu acara dengan kuncup calla di sudut.
import { Lucide, ThemeShell, formatDate, guestLabel, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Castoro:ital@0;1", "Spectral:ital,wght@0,400;0,600;1,400", "Tenor Sans", "Amiri"];
// Painted by /tmp/pen/art/themes/lili-syari.py
const Art = makeArt("lili-syari", { tangkai: [360, 1289], lili: [300, 195], kuncup: [129, 327], daun: [420, 69] } as const);

const WISHES = [
  { id: "w1", name: "Ustadzah Khadijah", attendance: "yes" as Attendance, message: "Barakallahu lakuma wa baraka 'alaikuma wa jama'a bainakuma fi khair. Semoga menjadi keluarga yang saling menuntun ke surga." },
  { id: "w2", name: "Teman Liqo' Bintaro", attendance: "yes" as Attendance, message: "MasyaAllah, ikut bahagia untuk Maryam. Semoga Allah mudahkan setiap langkah setelah akad, aamiin." },
  { id: "w3", name: "Keluarga H. Zainal, Bogor", attendance: "maybe" as Attendance, message: "Mohon maaf apabila belum dapat hadir. Doa terbaik kami menyertai, semoga sakinah, mawaddah, warahmah." },
];

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    arabic: "السَّلَامُ عَلَيْكُمْ وَرَحْمَةُ اللهِ وَبَرَكَاتُهُ",
    kicker: "Assalamu'alaikum Wr. Wb.",
    title: "Dengan Rahmat Allah",
    intro: "Maha Suci Allah yang telah menciptakan makhluk-Nya berpasang-pasangan. Dengan memohon ridha-Nya, kami bermaksud menyelenggarakan walimatul 'ursy putra-putri kami. Kehadiran dan doa Bapak/Ibu/Saudara/i merupakan kehormatan bagi kami.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"],
  couple: ["Dengan Izin Allah", "Kedua Mempelai"],
  count: ["Insyaallah", "Menuju Hari Akad"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Waktu & Tempat", "Rangkaian Acara"],
  story: ["Perjalanan", "Ta'aruf Hingga Akad"],
  gallery: ["Galeri", "Momen Bahagia"],
  wishes: ["Doa & Kehadiran", "Ucapan & Konfirmasi"],
  gifts: ["Tanda Kasih", "Amplop Digital"],
  closing: {
    thanks: "Jazakumullah Khairan",
    text: "Atas kehadiran dan doa restu Bapak/Ibu/Saudara/i, kami ucapkan terima kasih. Semoga Allah membalas setiap kebaikan dengan yang lebih baik.",
    salam: "Wassalamu'alaikum Wr. Wb.",
  },
  sent: "Jazakumullah khairan, doa dan ucapan Anda sudah terkirim.",
  wishPlaceholder: "Tuliskan doa untuk kedua mempelai…",
};

export default function LiliSyariTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Walimatul 'Ursy";
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#4f6e55"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <p className={s.bismillah} lang="ar" dir="rtl">بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ</p>
          <div className={s.split}>
            <div className={s.bouquet} aria-hidden><Art name="tangkai" eager /></div>
            <div className={s.col}>
              <p className={s.kicker}>{label}</p>
              <h1 className={s.coverNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
              <p className={s.coverDate}>{formatDate(data.date)}</p>
              <div className={s.guest}>
                <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
                <strong>{guestLabel(data)}</strong>
                {table && <span className={s.table}>{table}</span>}
              </div>
              <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#fbf7ec" />Buka Undangan</button>
            </div>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        noPhotos
        light="#fbf7ec"
        dark="#2f5a43"
        copy={COPY}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            <Art name="lili" className={s.heroLily} />
            <div className={s.frame}>
              <p className={s.heroKicker}>{label}</p>
              <h1 className={s.heroNames}>{data.couple.bride} <em>&amp;</em> {data.couple.groom}</h1>
              <p className={s.heroDate}>{formatDate(data.date)}</p>
              {note && <p className={s.heroNote}>{note}</p>}
            </div>
          </header>
        )}
        slots={{
          divider: <Art name="daun" className={s.divider} />,
          node: <Art name="kuncup" />,
          amp: <Art name="daun" />,
          portrait: <Art name="kuncup" className={s.portraitArt} />,
          closingDecor: <div className={s.closingFlank} aria-hidden><Art name="tangkai" /><Art name="tangkai" /></div>,
          closingEmblem: <Art name="lili" className={s.closingEmblem} />,
          sentArt: <Art name="lili" />,
        }}
      />
    </ThemeShell>
  );
}
