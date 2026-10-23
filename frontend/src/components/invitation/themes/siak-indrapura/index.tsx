"use client";
// Theme "Siak Indrapura" — adat Melayu Riau dalam ungu tua dan emas: Istana Siak berkubah di tepi Sungai Siak
// (arsitektur saja) dilukis gouache saat senja di dalam jendela wajik, sampan berkajang yang hanyut pelan, dan
// songket Siak bertenun benang emas (pucuk rebung, bunga tabur) sebagai latar. Pantun pembuka, bismillah diketik.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Cormorant SC:wght@500;600;700", "Vollkorn:ital,wght@0,400;0,600;0,700;1,400", "Mea Culpa", "Amiri:wght@400"];
// Painted by /tmp/pen/art/themes/siak-indrapura.py.
const Art = makeArt("siak-indrapura", {
  scene: [608, 704], boat: [200, 64], bunga: [96, 95], divider: [280, 31],
} as const);
const BISMILLAH = "بِسْمِ اللّٰهِ الرَّحْمٰنِ الرَّحِيْمِ";

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    arabic: "السَّلَامُ عَلَيْكُمْ وَرَحْمَةُ اللّٰهِ وَبَرَكَاتُهُ",
    kicker: "Assalamu'alaikum Warahmatullahi Wabarakatuh",
    title: "Walimatul 'Urs",
    sub: "Dari Negeri Istana, di Tepian Sungai Siak",
    intro: "Dengan memohon rahmat dan ridha Allah SWT, kami bermaksud melangsungkan akad nikah dan kenduri pernikahan putra-putri kami. Besar harapan kami Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
  },
  roles: ["Pengantin Perempuan", "Pengantin Lelaki"],
  couple: ["Yang Akan Bersanding", "Kedua Mempelai"],
  count: ["Menanti Hari Baik", "Hitung Mundur"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Masa & Tempat", "Rangkaian Majelis"],
  story: ["Hikayat Kami", "Kisah Dua Hati"],
  gallery: ["Galeri", "Kenangan Bersama"],
  wishes: ["Doa & Kehadiran", "Ucapan & Konfirmasi"],
  gifts: ["Tanda Kasih", "Amplop Digital"],
  closing: {
    thanks: "Terima Kasih",
    text: "Atas kehadiran dan doa restu Bapak/Ibu/Saudara/i, kami sekeluarga mengucapkan terima kasih. Semoga Allah membalas segala kebaikan dengan berlipat ganda.",
    salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh",
  },
  sent: "Jazakumullahu khairan, doa dan ucapan Anda sudah kami terima.",
  wishPlaceholder: "Tuliskan doa restu untuk kedua mempelai…",
  giftIntro: "Doa restu Anda adalah hadiah yang paling berharga. Bagi yang hendak memberi tanda kasih, dapat melalui:",
};

const WISHES = [
  { id: "w1", name: "Keluarga Datuk Wan Abdul Rahman", attendance: "yes" as const, message: "Barakallahu lakuma wa baraka 'alaikuma. Semoga menjadi keluarga sakinah, mawaddah, warahmah hingga ke anak cucu." },
  { id: "w2", name: "Sanggar Zapin Lancang Kuning", attendance: "yes" as const, message: "Pisang emas dibawa berlayar, masak sebiji di atas peti. Selamat bersanding Syafiqah dan Hafizh, kami datang membawa kompang!" },
  { id: "w3", name: "Cik Puan Rohana, Pekanbaru", attendance: "maybe" as const, message: "Insyaallah menyusul selepas zuhur. Doa terbaik untuk kalian berdua, semoga penuh berkah." },
];

export default function SiakIndrapuraTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const photo = data.gallery[0] ?? data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const groom = data.couple.groom?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#2a0d26"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <span className={s.coverGlow} aria-hidden />
          <p className={s.coverArabic} lang="ar" dir="rtl">{BISMILLAH}</p>
          <p className={s.kicker}>Undangan {label}</p>
          <div className={s.win} aria-hidden>
            <div className={s.winIn}>
              <Art name="scene" eager />
              <Art name="boat" eager className={s.boat} />
            </div>
          </div>
          <h1 className={s.coverNames}><span>{data.couple.bride}</span>{groom && <><em>&amp;</em><span>{groom}</span></>}</h1>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.guest}>
            <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
            <strong>{guestLabel(data)}</strong>
            {table && <span className={s.table}>{table}</span>}
          </div>
          <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#3b1534" />Buka Undangan</button>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        demoWishes={WISHES}
        light="#f0d28a"
        dark="#3b1534"
        copy={COPY}
        hero={(
          <header className={s.hero}>
            <div className={s.heroPhoto}>{photo ? <Photo src={photo} alt={`${data.couple.bride}${groom ? ` dan ${groom}` : ""}`} /> : <span className={s.heroMono} aria-hidden>{data.couple.bride.slice(0, 1)}</span>}</div>
            <span className={s.heroHem} aria-hidden />
            <span className={s.heroBand} aria-hidden />
            <p className={s.heroKicker}>Walimatul &apos;Urs</p>
            <h1 className={s.heroNames}><span>{data.couple.bride}</span>{groom && <><em>&amp;</em><span>{groom}</span></>}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="divider" className={s.divider} />,
          node: <Art name="bunga" />,
          amp: <Art name="bunga" />,
          portrait: <Art name="bunga" className={s.portraitBunga} />,
          closingDecor: <div className={s.closingWin} aria-hidden><span /></div>,
          closingEmblem: <Art name="bunga" className={s.closingEmblem} />,
          sentArt: <Art name="bunga" />,
        }}
      />
    </ThemeShell>
  );
}
