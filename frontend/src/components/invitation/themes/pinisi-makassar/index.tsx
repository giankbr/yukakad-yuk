"use client";
// Theme "Pinisi Makassar" — pernikahan Islami Bugis-Makassar: pinisi bertiang dua dengan tujuh layar melintas di senja
// Pantai Losari (cat air), lipa' sabbe kotak sutra Makassar sebagai lunas kartu dan latar hitung mundur, potret berbentuk
// layar gaff yang terpasang di tiangnya, dan kapal kecil yang mengangguk di atas ombak sebagai pemisah.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Young Serif", "Hanken Grotesk:ital,wght@0,400;0,600;0,700;0,800;1,400", "Allura", "Amiri:wght@400;700"];
// Painted by /tmp/pen/art/themes/pinisi-makassar.py (tools/art/themes in the repo).
const Art = makeArt("pinisi-makassar", { losari: [780, 1080], pinisi: [320, 294] } as const);

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    arabic: "بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ",
    kicker: "Assalamu'alaikum Wr. Wb.",
    title: "Dengan Rahmat Allah",
    intro: "Dengan memohon rahmat dan rida Allah Subhanahu wa Ta'ala, kami bermaksud menyelenggarakan pernikahan putra-putri kami. Merupakan kehormatan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"],
  couple: ["Kedua Mempelai", "Satu Bahtera"],
  count: ["Menghitung Hari", "Menuju Hari Bahagia"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Waktu & Tempat", "Rangkaian Acara"],
  story: ["Kisah Kami", "Berlayar Bersama"],
  gallery: ["Galeri", "Momen Bahagia"],
  wishes: ["Doa & Kehadiran", "Ucapan & Konfirmasi"],
  gifts: ["Tanda Kasih", "Amplop Digital"],
  closing: { thanks: "Terima Kasih", text: "Atas kehadiran dan doa restu Bapak/Ibu/Saudara/i, kami sekeluarga mengucapkan terima kasih. Semoga Allah membalas setiap kebaikan.", salam: "Wassalamu'alaikum Wr. Wb." },
  sent: "Terima kasih, doa dan ucapan Anda sudah terkirim.",
  wishPlaceholder: "Tuliskan doa terbaik untuk kedua mempelai…",
};

const WISHES = [
  { id: "w1", name: "Keluarga H. Abdul Rahman Daeng Sila", attendance: "yes" as Attendance, message: "Barakallahu lakuma. Selamat berlayar di bahtera baru, Firah dan Ilham. Semoga sakinah sampai tujuan." },
  { id: "w2", name: "Alumni Psikologi UNM", attendance: "yes" as Attendance, message: "Selamat Firah! Kami datang ramai-ramai ke Losari, siapkan coto yang banyak ya." },
  { id: "w3", name: "Daeng Tiro & Keluarga, Bulukumba", attendance: "maybe" as Attendance, message: "Insyaallah kami berangkat dari Bira. Doa terbaik untuk kalian berdua." },
];

export default function PinisiMakassarTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const hero = data.gallery[0] ?? data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#2e1d3c"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.coverTop}>
            <p className={s.bismillah} lang="ar" dir="rtl">بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ</p>
            <p className={s.salam}>Assalamu&apos;alaikum Wr. Wb.</p>
            <p className={s.kicker}>Undangan {label}</p>
            <h1 className={s.coverNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
          </div>
          <div className={s.sea} aria-hidden><Art name="losari" eager className={s.seaArt} /></div>
          <div className={s.guestWrap}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#3b2448" />Buka Undangan</button>
          </div>
          <div className={s.coverPad} />
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#f6d29a"
        dark="#3b2448"
        copy={COPY}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            <div className={s.heroSail}>
              {hero && <div className={s.heroPhoto}><Photo src={hero} alt="" /></div>}
            </div>
            <p className={s.heroKicker}>Walimatul &apos;Ursy</p>
            <h1 className={s.heroNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
            <Art name="pinisi" className={s.heroShip} />
          </header>
        )}
        slots={{
          divider: <span className={s.divider} aria-hidden><Art name="pinisi" /><i /></span>,
          node: <Art name="pinisi" />,
          amp: <Art name="pinisi" />,
          closingDecor: <div className={s.closingSea} aria-hidden><Art name="losari" /></div>,
          sentArt: <Art name="pinisi" />,
        }}
      />
    </ThemeShell>
  );
}
