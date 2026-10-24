"use client";
// Theme "Bintang Duabelas" — dinding riad dari plester kapur gading (desain orisinal, tanpa makhluk bernyawa dan tanpa
// kaligrafi lukis): medali rosette bintang dua belas berukir di tengah sampul, nama dalam huruf kufi geometris, dado
// ubin zellige di kaki dinding. Pola ubinnya dikonstruksi dengan metode poligon bersentuhan (Hankin) di atas teselasi
// 4.6.12: bintang 12 toska, bintang 6 terakota, tali putih. Monogram mempelai di dalam bingkai bintang dua belas,
// hitung mundur di ubin segi delapan, kartu acara berlis zellige, penutup rosette dan dado. Basmalah diketik.
import { Lucide, ThemeShell, formatDate, guestLabel, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Reem Kufi:wght@400;500;600;700", "Lustria", "Amiri:wght@400"];
// Painted by /tmp/pen/art/themes/bintang-duabelas.py
const Art = makeArt("bintang-duabelas", { rosette: [620, 620], star: [120, 120] } as const);
const BISMILLAH = "بِسْمِ اللّٰهِ الرَّحْمٰنِ الرَّحِيْمِ";

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    arabic: BISMILLAH,
    kicker: "Assalamu'alaikum Warahmatullahi Wabarakatuh",
    title: "Dengan Rahmat Allah",
    intro: "Maha Suci Allah yang menciptakan segala sesuatu berpasang-pasangan. Dengan memohon rida-Nya, kami bermaksud menyelenggarakan akad nikah dan walimah putra-putri kami. Merupakan kehormatan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"],
  couple: ["Dua yang bertemu di satu pusat", "Kedua Mempelai"],
  count: ["Hitung Mundur", "Menuju Hari Akad"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Waktu & Tempat", "Rangkaian Acara"],
  story: ["Garis yang bertemu", "Kisah Kami"],
  gallery: ["Album", "Galeri Foto"],
  wishes: ["Doa & Kehadiran", "Ucapan & Konfirmasi"],
  gifts: ["Tanda Kasih", "Amplop Digital"],
  closing: {
    thanks: "Jazakumullah Khairan",
    text: "Kehadiran dan doa restu Bapak/Ibu/Saudara/i adalah kebahagiaan bagi kami sekeluarga. Semoga Allah membalas setiap kebaikan dengan berlipat ganda.",
    salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh",
  },
  sent: "Jazakumullah khairan, doa dan ucapan Anda sudah terkirim.",
};

const WISHES = [
  { id: "w1", name: "Keluarga Ir. Yusuf Hidayat", attendance: "yes" as Attendance, message: "Barakallahu lakuma wa baraka 'alaikuma wa jama'a bainakuma fi khair. Semoga menjadi keluarga sakinah, mawaddah, wa rahmah." },
  { id: "w2", name: "Teman Studio Ornamen ITB", attendance: "yes" as Attendance, message: "Dari kelas jangka dan busur sampai pelaminan! Selamat Naila dan Hafiz, semoga hidup kalian seimbang dan simetris." },
  { id: "w3", name: "Ustazah Laila", attendance: "maybe" as Attendance, message: "Insyaallah hadir selepas kajian. Doa terbaik untuk kalian berdua, semoga Allah lapangkan rezeki dan berkahi rumah tangga kalian." },
];

export default function BintangDuabelasTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Walimatul 'Ursy";
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#14504e"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <span className={s.frieze} aria-hidden />
          <p className={s.arabicCover} lang="ar" dir="rtl">{BISMILLAH}</p>
          <p className={s.kicker}>{label}</p>
          <div className={s.medal} aria-hidden><Art name="rosette" eager /></div>
          <h1 className={s.names}>{data.couple.bride} <em>&amp;</em> {data.couple.groom}</h1>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <span className={s.spacer} aria-hidden />
          <div className={s.dadoCover}>
            <div className={s.plaque}>
              <div className={s.guest}>
                <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
                <strong>{guestLabel(data)}</strong>
                {table && <span className={s.table}>{table}</span>}
              </div>
              <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={17} color="#fbf6ea" />Buka Undangan</button>
            </div>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        noPhotos
        light="#fbf6ea"
        dark="#14504e"
        copy={COPY}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            <span className={s.frieze} aria-hidden />
            <Art name="rosette" className={s.heroMedal} />
            <p className={s.heroKicker}>{label}</p>
            <h1 className={s.heroNames}>{data.couple.bride} <em>&amp;</em> {data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <span className={s.divider} aria-hidden><Art name="star" /></span>,
          node: <Art name="star" />,
          amp: <Art name="star" />,
          closingDecor: <Art name="rosette" className={s.closingRosette} />,
          closingEmblem: null,
          sentArt: <Art name="star" />,
        }}
      />
    </ThemeShell>
  );
}
