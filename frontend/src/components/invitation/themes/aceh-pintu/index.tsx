"use client";
// Theme "Aceh Pintu" — tamu memandang lewat pintu Aceh berukir: ambang dengan tulak angin bercat merah-kuning-hijau,
// tiang berukir bungong, daun pintu yang terbuka saat undangan dimuat, pita kerawang Gayo bersulam di setiap ruang,
// dan rumah Krong Bade di halaman. Pembuka Islami (basmalah + salam), tanpa ornamen makhluk bernyawa.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Marcellus", "Mulish:ital,wght@0,400;0,600;0,700;0,800;1,400", "Amiri:wght@400;700"];
// Painted by /tmp/pen/art/themes/aceh-pintu.py (tools/art/themes in the repo).
const Art = makeArt("aceh-pintu", { lintel: [640, 260], krong: [720, 332], medallion: [180, 180], divider: [300, 33] } as const);
const BISMILLAH = "بِسْمِ اللّٰهِ الرَّحْمٰنِ الرَّحِيْمِ";

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    arabic: BISMILLAH,
    kicker: "Assalamu'alaikum",
    title: "Warahmatullahi Wabarakatuh",
    intro: "Dengan memohon rahmat dan ridha Allah SWT, kami bermaksud menyelenggarakan pernikahan putra-putri kami. Merupakan kehormatan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
  },
  roles: ["Dara Baro", "Linto Baro"],
  couple: ["Linto & Dara Baro", "Kedua Mempelai"],
  count: ["Menghitung Hari", "Menuju Hari Bahagia"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Waktu & Tempat", "Rangkaian Acara"],
  story: ["Perjalanan", "Kisah Kami"],
  gallery: ["Galeri", "Momen Bahagia"],
  wishes: ["Doa & Kehadiran", "Ucapan & Konfirmasi"],
  gifts: ["Tanda Kasih", "Amplop Digital"],
  closing: { thanks: "Teurimong Geunaseh", text: "Atas kehadiran dan doa restu Bapak/Ibu/Saudara/i, kami sekeluarga mengucapkan terima kasih. Semoga Allah membalas setiap kebaikan.", salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh" },
  sent: "Teurimong geunaseh, doa dan ucapan Anda sudah terkirim.",
};

export default function AcehPintuTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const hero = data.gallery[0] ?? data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#0c0909"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <span className={`${s.jamb} ${s.jambL}`} aria-hidden />
          <span className={`${s.jamb} ${s.jambR}`} aria-hidden />
          <Art name="lintel" eager className={s.lintel} />
          <span className={s.threshold} aria-hidden />
          <p className={s.arabicCover} lang="ar" dir="rtl">{BISMILLAH}</p>
          <p className={s.kicker}>Assalamu&apos;alaikum Wr. Wb.</p>
          {hero && <div className={s.coverPhoto}><Photo src={hero} alt="" /></div>}
          <p className={s.coverLabel}>{label}</p>
          <h1 className={s.coverNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.guestWrap}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#141111" />Buka Undangan</button>
          </div>
          <span className={`${s.leaf} ${s.leafL}`} aria-hidden data-noreveal />
          <span className={`${s.leaf} ${s.leafR}`} aria-hidden data-noreveal />
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#f2d995"
        dark="#141111"
        copy={COPY}
        hero={(
          <header className={s.hero}>
            <p className={s.heroKicker}>Undangan {label}</p>
            <h1 className={s.heroNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {hero && <div className={s.heroPhoto}><Photo src={hero} alt="" /></div>}
            {note && <p className={s.heroNote}>{note}</p>}
            <Art name="krong" className={s.heroKrong} />
            <span className={s.heroBand} aria-hidden />
          </header>
        )}
        slots={{
          divider: <Art name="divider" className={s.divider} />,
          node: <Art name="medallion" />,
          amp: <Art name="medallion" />,
          closingEmblem: <Art name="krong" className={s.closingKrong} />,
          sentArt: <Art name="medallion" />,
        }}
      />
    </ThemeShell>
  );
}
