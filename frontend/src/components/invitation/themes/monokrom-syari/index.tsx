"use client";
// Theme "Monokrom Syari" — syari tanpa foto dalam hitam-putih yang tegas: kisi khatam bintang delapan bercetak
// relief sebagai pita pemisah, bingkai bintang putih berisi monogram di atas panel hitam, panel putih berkisi
// yang naik membawa nama tamu, monogram dalam oktagon, kartu acara bergaris tebal dengan bayangan blok.
// Grafis dan modern, tanpa figur makhluk hidup.
import { Lucide, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Syne:wght@600;700;800", "Manrope:wght@400;500;600;700;800", "Reem Kufi:wght@500"];
// Printed by /tmp/pen/art/themes/monokrom-syari.py (the lattice tile is a CSS background).
const Art = makeArt("monokrom-syari", { frame: [560, 558], divider: [440, 39], star: [120, 120] } as const);

const WISHES = [
  { id: "w1", name: "Ustadzah Rahmi & Keluarga", attendance: "yes" as const, message: "Barakallahu lakuma wa baraka 'alaikuma wa jama'a bainakuma fii khair. Semoga menjadi keluarga sakinah, mawaddah, warahmah." },
  { id: "w2", name: "Teman Liqo Nabila", attendance: "yes" as const, message: "Alhamdulillah, ikut berbahagia. Semoga Allah mudahkan dan berkahi setiap langkah kalian berdua." },
  { id: "w3", name: "Keluarga Bapak Asep, Garut", attendance: "maybe" as const, message: "Mohon maaf bila belum bisa hadir. Doa terbaik kami dari Garut, semoga acaranya lancar dan penuh berkah." },
];

const initial = (name?: string) => (name?.trim().slice(0, 1) ?? "").toUpperCase();

export default function MonokromSyariTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Walimatul 'Ursy";
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const b = initial(data.couple.bride);
  const g = initial(data.couple.groom);

  return (
    <ThemeShell
      fonts={FONTS}
      background="#0e0e0e"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <p className={s.coverArabic} lang="ar" dir="rtl">بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيم</p>
          <div className={s.star}>
            <Art name="frame" eager className={s.starArt} />
            <p className={s.mono} aria-hidden>{b}{g && <i />}{g}</p>
          </div>
          <p className={s.kicker}>{label}</p>
          <h1 className={s.coverNames}>{data.couple.bride}{data.couple.groom?.trim() && <><em>dan</em>{data.couple.groom}</>}</h1>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.panel}>
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
        noPhotos
        light="#ffffff"
        dark="#111111"
        demoWishes={WISHES}
        copy={{
          opening: {
            arabic: "السَّلَامُ عَلَيْكُمْ وَرَحْمَةُ اللهِ وَبَرَكَاتُهُ",
            kicker: "Assalamu'alaikum Wr. Wb.",
            title: "Dengan Rahmat Allah",
            intro: "Maha Suci Allah yang menciptakan makhluk-Nya berpasang-pasangan. Dengan memohon ridha-Nya, kami bermaksud menyelenggarakan pernikahan putra-putri kami. Merupakan kehormatan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan mendoakan.",
          },
          roles: ["Mempelai Wanita", "Mempelai Pria"],
          couple: ["Bismillah", "Kedua Mempelai"],
          count: ["Menanti", "Hari yang Diberkahi"],
          units: ["Hari", "Jam", "Menit", "Detik"],
          events: ["Insyaallah", "Waktu & Tempat"],
          story: ["Perjalanan", "Kisah Kami"],
          gallery: ["Galeri", "Momen"],
          wishes: ["Doa", "Doa & Kehadiran"],
          gifts: ["Tanda Kasih", "Amplop Digital"],
          closing: {
            thanks: "Jazakumullah Khairan",
            text: "Atas kehadiran dan doa restu Bapak/Ibu/Saudara/i, kami ucapkan terima kasih. Semoga Allah membalas dengan kebaikan.",
            salam: "Wassalamu'alaikum Wr. Wb.",
          },
          sent: "Jazakallahu khairan, doa Anda sudah terkirim.",
          wishPlaceholder: "Tuliskan doa untuk kedua mempelai…",
        }}
        hero={(
          <header className={s.hero}>
            <Art name="star" className={s.heroStar} />
            <p className={s.heroKicker}>{label}</p>
            <h1 className={s.heroNames}>{data.couple.bride}{data.couple.groom?.trim() && <><em>dan</em>{data.couple.groom}</>}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="divider" className={s.divider} />,
          node: <Art name="star" />,
          amp: <Art name="star" />,
          portrait: <Art name="star" className={s.portraitStar} />,
          closingEmblem: <Art name="star" className={s.closingEmblem} />,
          sentArt: <Art name="star" />,
        }}
      />
    </ThemeShell>
  );
}
