"use client";
// Theme "Masjid Tajug" — pagi hangat di halaman berpasir sebuah masjid kuno Nusantara (rancangan orisinal, terilhami
// Demak dan Kudus): atap tajug tumpang tiga dari sirap, mustaka tanah liat, serambi bertiang jati, gapura paduraksa
// bata merah, pohon sawo kecik. Foto dipandang dari bawah serambi. Pembuka Islami, tanpa makhluk bernyawa.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Libre Caslon Display", "Libre Caslon Text:ital,wght@0,400;0,700;1,400", "Amiri:wght@400;700"];
// Painted by /tmp/pen/art/themes/masjid-tajug.py (tools/art/themes in the repo).
const Art = makeArt("masjid-tajug", { masjid: [780, 473], gapura: [420, 602], sawo: [260, 273], divider: [300, 28] } as const);
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
  couple: ["Bismillah", "Kedua Mempelai"],
  count: ["Menghitung Hari", "Menuju Akad"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Waktu & Tempat", "Rangkaian Acara"],
  story: ["Perjalanan", "Kisah Kami"],
  gallery: ["Galeri", "Momen Bahagia"],
  wishes: ["Doa & Kehadiran", "Ucapan & Konfirmasi"],
  gifts: ["Tanda Kasih", "Amplop Digital"],
  closing: { thanks: "Matur Nuwun", text: "Atas kehadiran dan doa restu Bapak/Ibu/Saudara/i, kami sekeluarga mengucapkan terima kasih. Jazakumullah khairan katsiran.", salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh" },
  sent: "Jazakumullah khairan, doa dan ucapan Anda sudah terkirim.",
};

export default function MasjidTajugTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const hero = data.gallery[0] ?? data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#d9bf8a"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <p className={s.arabicCover} lang="ar" dir="rtl">{BISMILLAH}</p>
          <p className={s.kicker}>Assalamu&apos;alaikum Wr. Wb.</p>
          <p className={s.coverLabel}>Undangan {label}</p>
          <h1 className={s.coverNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <Art name="masjid" eager className={s.coverScene} />
          <div className={s.yard}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#fbf0dc" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#f2d29a"
        dark="#4a2c18"
        copy={COPY}
        hero={(
          <header className={s.hero}>
            <p className={s.heroKicker}>Undangan {label}</p>
            <h1 className={s.heroNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {hero && (
              <div className={s.serambi}>
                <span className={s.eave} aria-hidden />
                <div className={s.bay}>
                  <span className={s.pillar} aria-hidden />
                  <div className={s.heroPhoto}><Photo src={hero} alt="" /></div>
                  <span className={s.pillar} aria-hidden />
                </div>
                <div className={s.umpak} aria-hidden><span /><span /><span /></div>
              </div>
            )}
            {note && <p className={s.heroNote}>{note}</p>}
            <Art name="divider" className={s.heroDivider} />
          </header>
        )}
        slots={{
          divider: <Art name="divider" className={s.divider} />,
          node: <span className={s.nodeRoof} />,
          closingDecor: <div className={s.closingTrees} aria-hidden><Art name="sawo" /><Art name="sawo" /></div>,
          closingEmblem: <Art name="gapura" className={s.closingGate} />,
          sentArt: <Art name="sawo" />,
        }}
      />
    </ThemeShell>
  );
}
