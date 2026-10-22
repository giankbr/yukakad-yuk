"use client";
// Theme "Samarkand Biru" — foto mempelai tampak di dalam lengkung iwan Timurid yang berlapis bata berglasir dan
// geometri bintang-silang, di bawah langit lapis; kubah melon toska bergaris menutup halaman. Pembuka Islami
// (basmalah + salam). Hanya arsitektur dan geometri: tanpa makhluk bernyawa, tanpa kaligrafi yang digambar.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["El Messiri:wght@400;500;600;700", "Spectral:ital,wght@0,400;0,500;0,600;1,400", "Amiri:wght@400;700"];
// Painted by /tmp/pen/art/themes/samarkand-biru.py (tools/art/themes in the repo).
const Art = makeArt("samarkand-biru", { iwan: [600, 800], domes: [706, 400], star: [160, 159], divider: [300, 27] } as const);
const BISMILLAH = "بِسْمِ اللّٰهِ الرَّحْمٰنِ الرَّحِيْمِ";

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    arabic: BISMILLAH,
    kicker: "Assalamu'alaikum",
    title: "Warahmatullahi Wabarakatuh",
    intro: "Dengan memohon rahmat dan ridha Allah SWT, kami bermaksud menyelenggarakan pernikahan putra-putri kami. Merupakan kehormatan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"],
  couple: ["Dua Insan", "Kedua Mempelai"],
  count: ["Menghitung Hari", "Menuju Hari Bahagia"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Waktu & Tempat", "Rangkaian Acara"],
  story: ["Perjalanan", "Kisah Kami"],
  gallery: ["Galeri", "Momen Bahagia"],
  wishes: ["Doa & Kehadiran", "Ucapan & Konfirmasi"],
  gifts: ["Tanda Kasih", "Amplop Digital"],
  closing: { thanks: "Terima Kasih", text: "Atas kehadiran dan doa restu Bapak/Ibu/Saudara/i, kami sekeluarga mengucapkan terima kasih. Semoga Allah membalas setiap kebaikan.", salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh" },
  sent: "Jazakumullah khairan, doa dan ucapan Anda sudah terkirim.",
};

export default function SamarkandBiruTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const hero = data.gallery[0] ?? data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#0e1745"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <p className={s.arabicCover} lang="ar" dir="rtl">{BISMILLAH}</p>
          <p className={s.kicker}>Assalamu&apos;alaikum Wr. Wb.</p>
          <div className={s.iwan}>
            {hero && <div className={s.iwanPhoto}><Photo src={hero} alt="" /></div>}
            <Art name="iwan" eager className={s.iwanArt} />
          </div>
          <div className={s.plinth}>
            <p className={s.coverLabel}>{label}</p>
            <h1 className={s.coverNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
            <div className={s.guestWrap}>
              <div className={s.guest}>
                <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
                <strong>{guestLabel(data)}</strong>
                {table && <span className={s.table}>{table}</span>}
              </div>
              <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#ffffff" />Buka Undangan</button>
            </div>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#f0d27c"
        dark="#142159"
        copy={COPY}
        hero={(
          <header className={s.hero}>
            <p className={s.heroKicker}>Undangan {label}</p>
            <h1 className={s.heroNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {hero && <div className={s.heroPhoto}><Photo src={hero} alt="" /></div>}
            {note && <p className={s.heroNote}>{note}</p>}
            <Art name="domes" className={s.heroDomes} />
          </header>
        )}
        slots={{
          divider: <Art name="divider" className={s.divider} />,
          node: <Art name="star" />,
          amp: <Art name="star" />,
          closingDecor: <><Art name="domes" className={s.closingDomes} /><span className={s.closingBase} aria-hidden /></>,
          sentArt: <Art name="star" />,
        }}
      />
    </ThemeShell>
  );
}
