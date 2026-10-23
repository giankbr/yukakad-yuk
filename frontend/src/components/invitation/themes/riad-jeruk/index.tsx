"use client";
// Theme "Riad Jeruk" — Islami, halaman riad Maroko dilihat dari atas: lantai zellige pastel, air mancur marmer berpita
// zellige (nama mempelai mengapung di airnya), empat pohon jeruk dalam bak tanam, atap genteng hijau. Di dalam: lengkung
// plester berukir bergigi diapit pohon jeruk dalam pot, pita ubin, dan setangkai jeruk. Tanpa figur, tanpa kaligrafi lukis.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Lustria", "Tenor Sans", "Amiri:wght@400;700"];
// Painted by /tmp/pen/art/themes/riad-jeruk.py (tile.webp and frieze.webp are CSS backgrounds).
const Art = makeArt("riad-jeruk", { court: [780, 780], tree: [300, 516], arch: [560, 752], sprig: [200, 102] } as const);
const BISMILLAH = "بِسْمِ اللّٰهِ الرَّحْمٰنِ الرَّحِيْمِ";

const WISHES = [
  { id: "w1", name: "Ustadzah Laila Fitri", attendance: "yes" as const, message: "Barakallahu lakuma wa baraka 'alaikuma wa jama'a bainakuma fi khair. Semoga rumah kalian teduh seperti halaman yang dinaungi pohon jeruk." },
  { id: "w2", name: "Studio Arsitektur Ruang Teduh", attendance: "yes" as const, message: "Selamat Syifa & Rayhan! Dari meja gambar ke pelaminan. Semoga rancangan hidup kalian selalu kokoh dan lapang." },
  { id: "w3", name: "Keluarga Bapak Haris", attendance: "maybe" as const, message: "Insyaallah kami usahakan hadir. Doa terbaik untuk kalian berdua dan kedua keluarga." },
];

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    arabic: BISMILLAH,
    kicker: "Assalamu'alaikum Wr. Wb.",
    title: "Dengan Memohon Ridha Allah",
    intro: "Maha Suci Allah yang menciptakan segala sesuatu berpasang-pasangan. Dengan memohon rahmat dan ridha-Nya, kami bermaksud menyelenggarakan pernikahan putra-putri kami. Merupakan kehormatan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"],
  couple: ["Bismillah", "Kedua Mempelai"],
  count: ["Insyaallah", "Menuju Hari Akad"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Waktu & Tempat", "Rangkaian Acara"],
  story: ["Takdir yang Indah", "Kisah Kami"],
  gallery: ["Kenangan", "Galeri"],
  wishes: ["Doa & Ucapan", "Ucapan & Kehadiran"],
  gifts: ["Tanda Kasih", "Amplop Digital"],
  closing: { thanks: "Jazakumullah Khairan", text: "Atas kehadiran dan doa restu Bapak/Ibu/Saudara/i, kami ucapkan terima kasih. Semoga Allah membalas setiap kebaikan dengan yang lebih baik.", salam: "Wassalamu'alaikum Wr. Wb." },
  sent: "Jazakumullah khairan, doa dan ucapan Anda sudah terkirim.",
  wishPlaceholder: "Tuliskan doa terbaik untuk kedua mempelai…",
};

function Divider() {
  return <span className={s.divider} aria-hidden><Art name="sprig" /></span>;
}

export default function RiadJerukTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const hero = data.gallery[0] ?? data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#f6efe3"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.coverTop}>
            <p className={s.coverArabic} lang="ar" dir="rtl">{BISMILLAH}</p>
            <p className={s.kicker}>{/walim|nikah|perni/i.test(label) ? label : `Undangan ${label}`}</p>
          </div>
          <div className={s.court}>
            <Art name="court" eager className={s.courtArt} />
            <div className={s.pool}>
              <h1 className={s.coverNames}><span>{data.couple.bride}</span><em>&amp;</em><span>{data.couple.groom}</span></h1>
            </div>
          </div>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.guestWrap}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#fbf7ef" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        copy={COPY}
        demoWishes={WISHES}
        light="#f6cf98"
        dark="#1f4540"
        hero={(
          <header className={s.hero}>
            <div className={s.heroArch}>
              <div className={s.heroPhoto}>{hero && <Photo src={hero} alt="" />}</div>
              <Art name="arch" className={s.heroFrame} />
              <Art name="tree" className={`${s.heroTree} ${s.heroTreeL}`} />
              <Art name="tree" className={`${s.heroTree} ${s.heroTreeR}`} />
            </div>
            <p className={s.heroKicker}>{label}</p>
            <h1 className={s.heroNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Divider />,
          node: <Art name="sprig" />,
          amp: <Art name="sprig" />,
          closingDecor: <span aria-hidden><Art name="tree" className={s.closingTree} /><Art name="tree" className={s.closingTree} /></span>,
          closingEmblem: <Art name="sprig" className={s.closingSprig} />,
          sentArt: <Art name="sprig" />,
        }}
      />
    </ThemeShell>
  );
}
