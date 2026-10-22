"use client";
// Theme "Peranakan Merah" — pernikahan Tionghoa Peranakan (Semarang, Lasem, Tangerang): ruang sutra merah berenda kebaya
// encim, burung hong bersulam benang sutra dan emas melintas di atas potret bulat ala pintu bulan, peoni kasut manik
// yang disematkan, deret tegel nyonya, dan kartu-kartu angpao. Pasangan Kristen: salam kasih dan pemberkatan nikah.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Bodoni Moda:ital,wght@0,400;0,500;0,600;1,400;1,500", "Nunito Sans:wght@400;600;700;800", "Allura"];
// Painted by /tmp/pen/art/themes/peranakan-merah.py (tools/art/themes in the repo).
const Art = makeArt("peranakan-merah", { hong: [640, 531], peony: [380, 380], divider: [300, 19] } as const);

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    kicker: "Salam Kasih",
    title: "Damai Sejahtera",
    intro: "Dengan penuh syukur atas kasih karunia Tuhan, kami bermaksud mempersatukan putra-putri kami dalam ikatan pernikahan kudus. Merupakan sukacita bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"],
  couple: ["Dua Keluarga, Satu Rumah", "Kedua Mempelai"],
  count: ["Hari Baik", "Menuju Hari Bahagia"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Waktu & Tempat", "Rangkaian Acara"],
  story: ["Perjalanan Kasih", "Kisah Kami"],
  gallery: ["Galeri", "Kenangan Bahagia"],
  wishes: ["Doa & Kehadiran", "Ucapan & Konfirmasi"],
  gifts: ["Angpao", "Tanda Kasih"],
  closing: { thanks: "Terima Kasih", text: "Kehadiran dan doa restu Bapak/Ibu/Saudara/i adalah berkat yang sangat berarti bagi kami sekeluarga. Tuhan memberkati.", salam: "Salam kasih dalam Tuhan" },
  sent: "Terima kasih, doa dan ucapan Anda sudah terkirim.",
  attend: { maybe: "Mungkin" },
  wishPlaceholder: "Tuliskan doa dan ucapan untuk kedua mempelai…",
};

const WISHES = [
  { id: "w1", name: "Ie Tjoa Siok Lan", attendance: "yes" as Attendance, message: "Selamat ya Lian dan Kevin! Semoga rumah tangga kalian penuh kasih, rukun, dan diberkati Tuhan sampai tua." },
  { id: "w2", name: "Keluarga Hartanto", attendance: "yes" as Attendance, message: "Turut berbahagia. Semoga saling menjaga dan selalu pulang ke rumah yang hangat." },
  { id: "w3", name: "Steven & Monica", attendance: "maybe" as Attendance, message: "Maaf kalau belum bisa datang ke Semarang. Doa kami menyertai kalian berdua." },
];

export default function PeranakanMerahTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const hero = data.gallery[0] ?? data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#3a060b"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <span className={s.lace} aria-hidden data-noreveal />
          <div className={s.moon}>
            {hero && <div className={s.moonFrame}><Photo src={hero} alt="" /></div>}
            <Art name="peony" eager />
            <span className={s.hongWrap} aria-hidden data-noreveal><Art name="hong" eager className={s.coverHong} /></span>
          </div>
          <p className={s.kicker}>Undangan {label}</p>
          <h1 className={s.coverNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.guestWrap}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#5c0910" />Buka Undangan</button>
          </div>
          <span className={s.tiles} aria-hidden />
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#f1d58c"
        dark="#5c0910"
        copy={COPY}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            <Art name="hong" className={s.heroHong} />
            {hero && <div className={s.heroPhoto}><Photo src={hero} alt="" /></div>}
            <p className={s.heroKicker}>The Wedding of</p>
            <h1 className={s.heroNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="divider" className={s.divider} />,
          node: <Art name="peony" />,
          amp: <Art name="divider" />,
          portrait: <Art name="peony" />,
          closingEmblem: <Art name="hong" className={s.closingHong} />,
          sentArt: <Art name="peony" />,
        }}
      />
    </ThemeShell>
  );
}
