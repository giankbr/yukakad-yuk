"use client";
// Theme "Pakpak Dairi" — adat Pakpak, Sumatera Utara (desain orisinal): perbukitan Dairi yang hijau berkabut di sekitar
// Sidikalang, rumah adat Pakpak berkolong dengan atap ijuk melengkung dan tampuk muka berlukis merah-putih-hitam, kain
// oles bergaris, serta ranting kopi yang sedang berbunga. Tata letak asimetris: oles menjulur di tepi kiri sampul, judul
// rata kiri di dalam kabut, foto dan potret dipotong seperti rumah adat (bubungan runcing). Pembuka Kristen, salam Pakpak.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Young Serif", "Petrona:ital,wght@0,400;0,600;1,400", "Jost:wght@400;500;600"];
// Painted by /tmp/pen/art/themes/pakpak-dairi.py (tools/art/themes in the repo).
const Art = makeArt("pakpak-dairi", { scene: [780, 1120], gable: [240, 160], sprig: [420, 186] } as const);

const COPY: ThemeCopy = {
  opening: {
    kicker: "Njuah-njuah!",
    title: "Salam Sejahtera dalam Kasih Kristus",
    intro: "Dengan penuh syukur kepada Tuhan Yang Maha Kasih, kami bermaksud melangsungkan pemberkatan nikah dan pesta adat Pakpak (merbayo) putra-putri kami. Merupakan sukacita bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
  },
  roles: ["Pengantin Perempuan", "Pengantin Laki-laki"],
  couple: ["Dua Marga, Satu Rumah", "Kedua Mempelai"],
  count: ["Menghitung Hari", "Menuju Hari Pemberkatan"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Waktu & Tempat", "Rangkaian Acara"],
  story: ["Dari Perbukitan Dairi", "Kisah Kami"],
  gallery: ["Kenangan", "Galeri Foto"],
  wishes: ["Doa & Kehadiran", "Ucapan & Konfirmasi"],
  gifts: ["Tanda Kasih", "Amplop Digital"],
  closing: {
    thanks: "Mejuah-juah, Terima Kasih",
    text: "Atas kehadiran dan doa restu Bapak/Ibu/Saudara/i, kami sekeluarga mengucapkan terima kasih. Kiranya Tuhan memberkati kita sekalian.",
    salam: "Tuhan Yesus memberkati",
  },
  sent: "Terima kasih, doa dan ucapan Anda sudah kami terima. Tuhan memberkati.",
  attend: { maybe: "Mungkin" },
  wishPlaceholder: "Tuliskan doa dan ucapan untuk kedua mempelai…",
  closedNote: "Terima kasih atas doa dan perhatiannya. Ucapan untuk kedua mempelai masih bisa dikirim lewat form ini.",
  giftIntro: "Doa restu Bapak/Ibu/Saudara/i adalah berkat terbesar bagi kami. Jika berkenan memberi tanda kasih, dapat melalui:",
};

const WISHES = [
  { id: "w1", name: "Pdt. Marulam Berutu & Keluarga", attendance: "yes" as Attendance, message: "Njuah-njuah! Selamat menempuh hidup baru. Kiranya rumah tangga kalian dibangun di atas kasih Kristus, kokoh seperti tiang rumah adat kita." },
  { id: "w2", name: "Koor Pemuda GKPPD Sidikalang", attendance: "yes" as Attendance, message: "Selamat Sinta dan Rikardo! Kami siap bernyanyi di pemberkatan. Semoga suara kalian berdua selalu seirama." },
  { id: "w3", name: "Keluarga Bang Tumpal, Medan", attendance: "maybe" as Attendance, message: "Mudah-mudahan kami bisa naik ke Sidikalang. Kalau belum sempat, doa kami menyertai dari Medan." },
];

export default function PakpakDairiTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel?.trim() || "Pernikahan";
  const hero = data.gallery[0] ?? data.couple.bridePhoto ?? data.couple.groomPhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#eef1ea"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.coverArt} aria-hidden><Art name="scene" eager /></div>
          <span className={s.coverMist} aria-hidden />
          <span className={s.coverStrip} aria-hidden />
          <div className={s.coverTop}>
            <p className={s.njuah}>Njuah-njuah!</p>
            <p className={s.coverLabel}>Undangan {label}</p>
            <h1 className={s.coverNames}><span>{data.couple.bride}</span><em>&amp;</em><span>{data.couple.groom}</span></h1>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
          </div>
          <div className={s.coverCard}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#f2ece0" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#f2ece0"
        dark="#2c5236"
        copy={COPY}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            <p className={s.heroKicker}>{label}</p>
            <h1 className={s.heroNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {hero && (
              <div className={s.house}>
                <Art name="gable" className={s.houseGable} />
                <div className={s.heroPhoto}><Photo src={hero} alt="" /></div>
                <span className={s.houseSash} aria-hidden />
                <Art name="sprig" className={s.heroSprig} />
              </div>
            )}
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <span className={s.divider} aria-hidden><i /><Art name="gable" /><i /></span>,
          node: <Art name="gable" />,
          amp: <Art name="gable" />,
          portrait: <><Art name="gable" className={s.pGable} /><span className={s.pSash} aria-hidden /></>,
          closingDecor: <div className={s.closingHills} aria-hidden><Art name="sprig" className={s.closingSprig} /></div>,
          closingEmblem: <Art name="gable" className={s.closingGable} />,
          sentArt: <Art name="gable" />,
        }}
      />
    </ThemeShell>
  );
}
