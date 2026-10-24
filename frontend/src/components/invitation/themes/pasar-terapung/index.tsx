"use client";
// Theme "Pasar Terapung" — subuh di pasar terapung Banjar dalam cat air: langit fajar jingga, sungai Martapura berkabut
// penuh jukung bermuatan jeruk, pisang, rambutan dan sayur dengan pedagang bertanggui, satu jukung besar yang terayun
// pelan di tepi dermaga hijau sungai; hitung mundur dalam bulatan jeruk, kartu acara bergaya papan dermaga, dan bingkai
// foto beratap pelana rumah lanting.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Fraunces:ital,wght@0,500;0,600;0,700;1,500", "Alegreya:ital,wght@0,400;0,700;1,400", "Alegreya Sans:wght@500;700;800", "Amiri"];
// Painted by /tmp/pen/art/themes/pasar-terapung.py (tools/art/themes in the repo).
const Art = makeArt("pasar-terapung", { sungai: [680, 637], jukung: [640, 144], tanggui: [240, 78], bakul: [280, 221], riak: [360, 32] } as const);

const WISHES = [
  { id: "w1", name: "Acil Norjanah & Keluarga", attendance: "yes" as Attendance, message: "Barakallahu lakuma. Salamat bakawin, semoga jadi keluarga yang sakinah, rukun, dan murah rezeki seperti pasar di subuh hari." },
  { id: "w2", name: "Fadli & Kawan-kawan ULM", attendance: "yes" as Attendance, message: "Akhirnya jukung kalian berlabuh juga! Ikut bahagia, sampai jumpa di Mahligai Pancasila." },
  { id: "w3", name: "Keluarga H. Rusdi, Martapura", attendance: "maybe" as Attendance, message: "Mohon maaf bila belum dapat hadir. Doa terbaik kami menyertai, semoga acaranya lancar dan berkah." },
];

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    arabic: "السَّلَامُ عَلَيْكُمْ وَرَحْمَةُ اللهِ وَبَرَكَاتُهُ",
    kicker: "Bismillahirrahmanirrahim",
    title: "Kami Mohon Doa Restu",
    intro: "Dengan memohon rahmat dan ridho Allah SWT, kami bermaksud menyelenggarakan pernikahan putra-putri kami. Merupakan kehormatan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"],
  couple: ["Dua Jukung, Satu Tujuan", "Kedua Mempelai"],
  count: ["Menunggu Fajar", "Menuju Hari Bahagia"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Waktu & Tempat", "Rangkaian Acara"],
  story: ["Kisah Kami", "Bermula di Atas Sungai"],
  gallery: ["Galeri", "Momen Bahagia"],
  wishes: ["Doa & Kehadiran", "Kirim Ucapan"],
  gifts: ["Tanda Kasih", "Amplop Digital"],
  closing: {
    thanks: "Terima Kasih",
    text: "Atas kehadiran dan doa restu Bapak/Ibu/Saudara/i, kami ucapkan terima kasih. Semoga Allah membalas setiap kebaikan.",
    salam: "Wassalamu'alaikum Wr. Wb.",
  },
  sent: "Terima kasih, doa dan ucapan Anda sudah terkirim.",
  giftIntro: "Doa restu Anda adalah hadiah terindah bagi kami. Jika berkenan memberi tanda kasih, dapat melalui:",
};

export default function PasarTerapungTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const heroPhoto = data.gallery[0] ?? data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#24453f"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.coverTop}>
            <p className={s.salamTop}>Assalamu&apos;alaikum</p>
            <p className={s.kicker}>Undangan {label}</p>
            <h1 className={s.coverNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
          </div>
          <div className={s.market} aria-hidden>
            <Art name="sungai" eager className={s.river} />
            <span className={s.mist} />
          </div>
          <div className={s.dock}>
            <Art name="jukung" eager className={s.boat} />
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={17} color="#2b170c" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#fbefe0"
        dark="#2c5651"
        copy={COPY}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            {heroPhoto && <div className={s.heroPhoto}><Photo src={heroPhoto} alt="" /></div>}
            <Art name="tanggui" className={s.heroHat} />
            <p className={s.heroKicker}>{label}</p>
            <h1 className={s.heroNames}>{data.couple.bride} <em>&amp;</em> {data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="riak" className={s.divider} />,
          node: <Art name="tanggui" />,
          amp: <Art name="riak" />,
          portrait: <Art name="riak" className={s.portraitArt} />,
          closingEmblem: <Art name="bakul" className={s.closingEmblem} />,
          sentArt: <Art name="bakul" />,
        }}
      />
    </ThemeShell>
  );
}
