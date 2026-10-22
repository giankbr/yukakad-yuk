"use client";
// Theme "Mezquita Cordoba" — cahaya keemasan di aula berpilar. Sampul: lorong lengkung ganda (tapal kuda di bawah
// lengkung bundar, batu baji bata merah dan batu gading berselang) dilukis gouache sebagai latar, foto di dalam satu
// lengkung tapal kuda berbingkai alfiz dengan ukiran palmet. Bingkai potret dan penghitung waktu berbentuk tapal kuda
// dengan cincin batu baji; friz deretan lengkung memahkotai tiap bagian. Arsitektur, geometri, dan flora saja.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Cormorant Upright:wght@400;500;600;700", "Gentium Book Plus:ital,wght@0,400;0,700;1,400", "Monsieur La Doulaise", "Amiri:wght@400;700"];
// Painted by /tmp/pen/art/themes/mezquita-cordoba.py (tools/art/themes in the repo).
const Art = makeArt("mezquita-cordoba", { hall: [720, 928], frame: [480, 656], divider: [300, 44], emblem: [140, 162] } as const);

const BISMILLAH = "بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ";

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    arabic: BISMILLAH,
    kicker: "Assalamu'alaikum Wr. Wb.",
    title: "Dengan Rahmat Allah",
    intro: "Maha Suci Allah yang telah menciptakan makhluk-Nya berpasang-pasangan. Dengan memohon ridha-Nya, kami bermaksud menyelenggarakan walimah pernikahan putra-putri kami. Merupakan kehormatan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan mendoakan.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"],
  couple: ["Bismillah, Kami Menikah", "Kedua Mempelai"],
  count: ["Insyaallah Sebentar Lagi", "Hitung Mundur"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Waktu & Tempat", "Rangkaian Acara"],
  story: ["Lengkung demi Lengkung", "Perjalanan Kami"],
  gallery: ["Galeri", "Potret Kami"],
  wishes: ["Doa & Kehadiran", "Ucapan & Konfirmasi"],
  gifts: ["Tanda Kasih", "Amplop Digital"],
  closing: { thanks: "Jazakumullah Khairan", text: "Atas kehadiran dan doa Bapak/Ibu/Saudara/i, kami ucapkan terima kasih. Semoga Allah membalas kebaikan dengan sebaik-baik balasan.", salam: "Wassalamu'alaikum Wr. Wb." },
  sent: "Jazakumullah khairan, doa dan ucapan Anda sudah terkirim.",
};

export default function MezquitaCordobaTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const hero = data.gallery[0] ?? data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#2e1c12"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Art name="hall" eager className={s.coverHall} />
          <p className={s.coverArabic} lang="ar" dir="rtl">{BISMILLAH}</p>
          <p className={s.coverKicker}>Assalamu&apos;alaikum Wr. Wb.</p>
          <div className={s.arch}>
            {hero ? <div className={s.archPhoto}><Photo src={hero} alt="" /></div> : <span className={s.archEmpty} aria-hidden />}
            <Art name="frame" eager />
          </div>
          <p className={s.coverLabel}>{label}</p>
          <h1 className={s.coverNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.guestCard}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={17} color="#fff" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#f4d488"
        dark="#2e1c12"
        copy={COPY}
        hero={(
          <header className={s.hero}>
            <Art name="emblem" className={s.heroEmblem} />
            <p className={s.heroKicker}>{label}</p>
            <h1 className={s.heroNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="divider" className={s.divider} />,
          node: <Art name="emblem" />,
          closingDecor: <Art name="hall" className={s.closingHall} />,
          closingEmblem: <Art name="emblem" className={s.closingMotif} />,
          sentArt: <Art name="emblem" />,
        }}
      />
    </ThemeShell>
  );
}
