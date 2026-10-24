"use client";
// Theme "Toska Syari" — tanpa foto, segar dan modern: kertas putih bersemu tosca, cakram cat air tosca dengan roset
// geometri delapan bertekan foil emas, ranting daun eukaliptus bertangkai emas, tipografi Bodoni rata kiri, monogram
// dalam lingkaran, dan hitung mundur berbingkai garis emas di atas pita tosca tua. Geometri dan flora saja.
import { Lucide, ThemeShell, formatDate, guestLabel, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Bodoni Moda:ital,wght@0,400;0,500;0,600;1,400", "Jost:wght@400;500;600", "Amiri"];
// Painted by /tmp/pen/art/themes/toska-syari.py (tools/art/themes in the repo).
const Art = makeArt("toska-syari", { cakra: [560, 554], ranting: [360, 464], daun: [160, 115], bintang: [100, 100], garis: [320, 27] } as const);

const WISHES = [
  { id: "w1", name: "Ustadzah Rahmah & Keluarga", attendance: "yes" as Attendance, message: "Barakallahu lakuma wa baraka 'alaikuma wa jama'a bainakuma fii khair. Semoga menjadi keluarga sakinah, mawaddah, warahmah." },
  { id: "w2", name: "Teman-teman Farmasi 2019", attendance: "yes" as Attendance, message: "MasyaAllah, ikut bahagia, Sal! Semoga Allah mudahkan setiap langkah kalian berdua." },
  { id: "w3", name: "Keluarga Bapak Asep, Cianjur", attendance: "maybe" as Attendance, message: "Mohon maaf bila belum bisa hadir. Doa terbaik kami dari jauh, semoga walimahnya lancar dan berkah." },
];

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    arabic: "السَّلَامُ عَلَيْكُمْ وَرَحْمَةُ اللهِ وَبَرَكَاتُهُ",
    kicker: "Dengan Rahmat Allah",
    title: "Kami Mengundang Anda",
    intro: "Dengan memohon rahmat dan ridho Allah SWT, kami bermaksud menyelenggarakan walimatul 'ursy putra-putri kami. Merupakan kehormatan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan mendoakan.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"],
  couple: ["Bismillah", "Kedua Mempelai"],
  count: ["Menghitung Hari", "Menuju Akad"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Waktu & Tempat", "Rangkaian Acara"],
  story: ["Perjalanan", "Ikhtiar Kami"],
  gallery: ["Galeri", "Kenangan"],
  wishes: ["Doa & Kehadiran", "Kirim Doa"],
  gifts: ["Tanda Kasih", "Amplop Digital"],
  closing: {
    thanks: "Jazakumullahu Khairan",
    text: "Atas kehadiran dan doa Bapak/Ibu/Saudara/i, kami ucapkan terima kasih. Semoga Allah membalas dengan kebaikan yang berlipat.",
    salam: "Wassalamu'alaikum Wr. Wb.",
  },
  sent: "Jazakumullahu khairan, doa Anda sudah terkirim.",
  wishPlaceholder: "Tuliskan doa untuk kedua mempelai…",
  giftIntro: "Doa Anda adalah hadiah terbaik bagi kami. Jika berkenan memberi tanda kasih, dapat melalui:",
};

export default function ToskaSyariTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Walimatul 'Ursy";
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const initials = [data.couple.bride, data.couple.groom].map(n => n.trim().slice(0, 1)).filter(Boolean);

  return (
    <ThemeShell
      fonts={FONTS}
      background="#0d6159"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Art name="cakra" eager className={s.disc} />
          <Art name="ranting" eager className={s.spray} />
          <Art name="daun" eager className={s.sprayTop} />
          <p className={s.arabicTop} lang="ar" dir="rtl">بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيم</p>
          <p className={s.salamTop}>Assalamu&apos;alaikum Wr. Wb.</p>
          <p className={s.kicker}>{label}</p>
          <h1 className={s.coverNames}>{data.couple.bride}<em>dan</em>{data.couple.groom}</h1>
          <Art name="garis" eager className={s.coverDivider} />
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.guestWrap}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#ffffff" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        noPhotos
        light="#f1d99a"
        dark="#0d7068"
        copy={COPY}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            <div className={s.heroDiscWrap}>
              <Art name="cakra" className={s.heroDisc} />
              <p className={s.heroMono} aria-hidden>{initials[0]}{initials[1] && <><em>&amp;</em>{initials[1]}</>}</p>
            </div>
            <p className={s.heroKicker}>{label}</p>
            <h1 className={s.heroNames}>{data.couple.bride} <em>&amp;</em> {data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="garis" className={s.divider} />,
          node: <Art name="bintang" />,
          amp: <Art name="bintang" />,
          portrait: <Art name="daun" className={s.portraitArt} />,
          closingEmblem: <Art name="cakra" className={s.closingEmblem} />,
          sentArt: <Art name="bintang" />,
        }}
      />
    </ThemeShell>
  );
}
