"use client";
// Theme "Abu Syari" — syari tanpa foto dalam abu-abu merpati dan perak: nama mempelai di dalam cincin roset bintang
// delapan bergaris rambut (perak tekan, berputar sangat pelan), kisi khatam halus sebagai latar, ranting daun berurat
// perak di dua sudut, monogram dalam roset, kartu acara bersudut potong. Tenang, modern, tanpa figur makhluk hidup.
import { Lucide, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Bellefair", "Tenor Sans", "Lora:ital,wght@0,400;0,500;1,400", "Amiri"];
// Painted by /tmp/pen/art/themes/abu-syari.py (the lattice is a CSS background).
const Art = makeArt("abu-syari", { rosette: [560, 560], sprig: [300, 462], divider: [300, 32], star: [72, 72] } as const);

const WISHES = [
  { id: "w1", name: "Ustadzah Aminah & Keluarga", attendance: "yes" as const, message: "Barakallahu lakuma wa baraka 'alaikuma wa jama'a bainakuma fii khair. Semoga menjadi keluarga sakinah, mawaddah, warahmah." },
  { id: "w2", name: "Fikri & Salma", attendance: "yes" as const, message: "Alhamdulillah, ikut berbahagia. Semoga Allah mudahkan setiap langkah kalian berdua." },
  { id: "w3", name: "Keluarga Bapak Syukron, Gresik", attendance: "maybe" as const, message: "Mohon maaf bila belum bisa hadir. Doa terbaik kami dari jauh, semoga acaranya lancar dan penuh berkah." },
];

export default function AbuSyariTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Walimatul 'Ursy";
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#e3e4e7"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Art name="sprig" eager className={s.sprigTR} />
          <Art name="sprig" eager className={s.sprigBL} />
          <p className={s.arabicTop} lang="ar" dir="rtl">بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيم</p>
          <div className={s.ring}>
            <Art name="rosette" eager className={s.ringArt} />
            <div className={s.ringText}>
              <p className={s.kicker}>{label}</p>
              <h1 className={s.coverNames}>{data.couple.bride}<em>dan</em>{data.couple.groom}</h1>
            </div>
          </div>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.guest}>
            <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
            <strong>{guestLabel(data)}</strong>
            {table && <span className={s.table}>{table}</span>}
          </div>
          <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={15} color="#ffffff" />Buka Undangan</button>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        noPhotos
        light="#f4f5f6"
        dark="#4b4f57"
        demoWishes={WISHES}
        copy={{
          ...DEFAULT_COPY,
          opening: {
            arabic: "السَّلَامُ عَلَيْكُمْ وَرَحْمَةُ اللهِ وَبَرَكَاتُهُ",
            kicker: "Assalamu'alaikum Wr. Wb.",
            title: "Dengan Rahmat Allah",
            intro: "Maha Suci Allah yang menciptakan makhluk-Nya berpasang-pasangan. Dengan memohon ridho-Nya, kami bermaksud menyelenggarakan pernikahan putra-putri kami. Merupakan kehormatan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan mendoakan.",
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
            <Art name="sprig" className={s.heroSprig} />
            <p className={s.heroKicker}>{label}</p>
            <h1 className={s.heroNames}>{data.couple.bride} <em>&amp;</em> {data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            <Art name="star" className={s.heroStar} />
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="divider" className={s.divider} />,
          node: <Art name="star" />,
          amp: <Art name="star" />,
          portrait: <Art name="rosette" className={s.portraitArt} />,
          closingDecor: <Art name="sprig" className={s.closingDecor} />,
          closingEmblem: <Art name="star" className={s.closingEmblem} />,
          sentArt: <Art name="star" />,
        }}
      />
    </ThemeShell>
  );
}
