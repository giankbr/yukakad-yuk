"use client";
// Theme "Riau Lancang Kuning" — walimah Melayu Riau di tepi laut: perahu lancang kuning berlapis emas (haluan berukir
// sulur, tanpa figur) terombang-ambing di atas ombak lukisan yang terus bergerak, selembayung bersilang sebagai mahkota
// sampul dan bubung potret, tenun Siak benang emas di atas biru laut, kartu acara berlambung perahu, awan larat emas.
// Pembuka Islami (basmalah + salam), ornamen arsitektur, flora, dan geometri saja.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Della Respira", "Sorts Mill Goudy:ital@0;1", "Imperial Script", "Amiri:wght@400;700"];
// Painted by /tmp/pen/art/themes/riau-lancang.py (tools/art/themes in the repo).
const Art = makeArt("riau-lancang", { lancang: [680, 398], selembayung: [300, 193], awan: [320, 37] } as const);
const BISMILLAH = "بِسْمِ اللّٰهِ الرَّحْمٰنِ الرَّحِيْمِ";

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    arabic: BISMILLAH,
    kicker: "Assalamu'alaikum",
    title: "Warahmatullahi Wabarakatuh",
    intro: "Dengan memohon rahmat dan ridha Allah SWT, kami bermaksud menyelenggarakan walimatul 'ursy putra-putri kami. Merupakan suatu kehormatan apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
  },
  roles: ["Pengantin Perempuan", "Pengantin Lelaki"],
  couple: ["Seiring Sehaluan", "Kedua Mempelai"],
  count: ["Menghitung Hari", "Menuju Hari Bersanding"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Waktu & Tempat", "Rangkaian Majelis"],
  story: ["Hikayat Pelayaran", "Kisah Kami"],
  gallery: ["Galeri", "Momen Bahagia"],
  wishes: ["Doa & Kehadiran", "Ucapan & Konfirmasi"],
  gifts: ["Tanda Kasih", "Amplop Digital"],
  closing: { thanks: "Terima Kasih", text: "Atas kehadiran dan doa restu Bapak/Ibu/Saudara/i, kami sekeluarga menghaturkan terima kasih. Semoga Allah membalas setiap kebaikan.", salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh" },
  sent: "Terima kasih, doa dan ucapan Anda sudah terkirim.",
};

const WISHES = [
  { id: "w1", name: "Keluarga H. Tengku Said", attendance: "yes" as Attendance, message: "Barakallahu lakuma wa baraka 'alaikuma. Semoga bahtera Azizah dan Hafiz sampai ke pulau bahagia." },
  { id: "w2", name: "Kak Nurul & Bang Firdaus", attendance: "yes" as Attendance, message: "Dari Siak kami datang berlayar, membawa doa dan selendang tenun. Selamat bersanding!" },
  { id: "w3", name: "Ustazah Rahmah", attendance: "maybe" as Attendance, message: "Insyaallah hadir selepas Zuhur. Semoga sakinah, mawaddah, warahmah." },
];

export default function RiauLancangTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const hero = data.gallery[0] ?? data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#0f3a48"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Art name="selembayung" eager className={s.crown} />
          <p className={s.bismillah} lang="ar" dir="rtl">{BISMILLAH}</p>
          <p className={s.kicker}>Undangan {label}</p>
          <h1 className={s.coverNames}>{data.couple.bride}<em>dan</em>{data.couple.groom}</h1>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.guestWrap}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#0f3a48" />Buka Undangan</button>
          </div>
          <div className={s.sea} aria-hidden>
            <Art name="lancang" eager className={s.boat} />
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#f1d58a"
        dark="#0f3a48"
        copy={COPY}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            <p className={s.heroKicker}>{label}</p>
            <h1 className={s.heroNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {hero && <div className={s.heroFrame}><div className={s.heroPhoto}><Photo src={hero} alt="" /></div></div>}
            {note && <p className={s.heroNote}>{note}</p>}
            <div className={s.heroWave} aria-hidden />
          </header>
        )}
        slots={{
          divider: <Art name="awan" className={s.divider} />,
          node: <Art name="selembayung" />,
          amp: <Art name="awan" />,
          portrait: <Art name="selembayung" />,
          closingEmblem: <Art name="selembayung" className={s.closingEmblem} />,
          closingDecor: <div className={s.closingBoat} aria-hidden><Art name="lancang" /></div>,
          sentArt: <Art name="lancang" />,
        }}
      />
    </ThemeShell>
  );
}
