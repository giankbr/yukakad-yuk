"use client";
// Theme "Osing Gajah Oling" — pernikahan Osing Banyuwangi: pagi berkabut di kaki Ijen dengan rumah Osing di antara
// kebun kopi, lalu kain batik gajah oling (motif lengkung tanya, bukan sosok hewan) bermalam krem di atas sogan hitam,
// potret beratap tikel balung, ranting kopi cat air, kartu bertepi kain. Pembuka Islami (basmalah + salam).
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Fraunces:ital,wght@0,400;0,500;0,600;1,400;1,500", "Figtree:wght@400;500;600;700;800", "Amiri:wght@400;700"];
// Painted by /tmp/pen/art/themes/osing-gajah-oling.py (tools/art/themes in the repo).
const Art = makeArt("osing-gajah-oling", {
  scene: [720, 469], curl: [300, 348], kopi: [320, 171], divider: [300, 95], "divider-ink": [300, 95],
} as const);
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
  couple: ["Loro Dadi Siji", "Kedua Mempelai"],
  count: ["Menghitung Hari", "Menuju Hari Bahagia"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Waktu & Tempat", "Rangkaian Acara"],
  story: ["Perjalanan", "Kisah Kami"],
  gallery: ["Galeri", "Momen Bahagia"],
  wishes: ["Doa & Kehadiran", "Ucapan & Konfirmasi"],
  gifts: ["Tanda Kasih", "Amplop Digital"],
  closing: { thanks: "Matur Nuwun", text: "Atas kehadiran dan doa restu Bapak/Ibu/Saudara/i, kami sekeluarga mengucapkan terima kasih. Semoga Allah membalas setiap kebaikan.", salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh" },
  sent: "Matur nuwun, doa dan ucapan Anda sudah terkirim.",
  wishPlaceholder: "Tuliskan doa restu untuk kedua mempelai…",
};

const WISHES = [
  { id: "w1", name: "Keluarga H. Abdul Rohim", attendance: "yes" as Attendance, message: "Barakallahu lakuma wa baraka 'alaikuma. Semoga menjadi keluarga sakinah, mawaddah, warahmah." },
  { id: "w2", name: "Mbak Ratna (Kemiren)", attendance: "yes" as Attendance, message: "Selamat Sekar dan Bayu! Sampai ketemu di balai adat, kopinya sudah disiapkan." },
  { id: "w3", name: "Rizal & Dewi", attendance: "maybe" as Attendance, message: "Insyaallah menyusul dari Jember. Doa terbaik untuk kalian berdua." },
];

export default function OsingGajahOlingTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const hero = data.gallery[0] ?? data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const divider = <span className={s.divider}><Art name="divider-ink" /><Art name="divider" /></span>;

  return (
    <ThemeShell
      fonts={FONTS}
      background="#1d1712"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.coverScene} aria-hidden data-noreveal><Art name="scene" eager /></div>
          <span className={s.coverCurl} aria-hidden data-noreveal><Art name="curl" eager /></span>
          <span className={s.coverCurl} aria-hidden data-noreveal><Art name="curl" eager /></span>
          {hero && <div className={s.coverPhoto}><Photo src={hero} alt="" /></div>}
          <p className={s.kicker}>Undangan {label}</p>
          <h1 className={s.coverNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.guestWrap}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#fbf6ea" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#efe2c6"
        dark="#1d1712"
        copy={COPY}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            <p className={s.heroKicker}>The Wedding of</p>
            <h1 className={s.heroNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            {hero && <div className={s.heroPhoto}><Photo src={hero} alt="" /></div>}
            <span className={s.heroKopi} aria-hidden><Art name="kopi" /></span>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider,
          node: <i className={s.nodeMark} />,
          amp: <Art name="divider-ink" />,
          portrait: <span className={s.portraitArt} aria-hidden><Art name="kopi" /></span>,
          closingEmblem: <Art name="kopi" className={s.closingKopi} />,
          closingDecor: <div className={s.closingScene} aria-hidden><Art name="scene" /></div>,
          sentArt: <Art name="kopi" />,
        }}
      />
    </ThemeShell>
  );
}
