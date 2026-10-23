"use client";
// Theme "Manggarai Lingko" — Flores barat dari ketinggian: sawah lingko jaring laba-laba (seperti di Cancar) yang
// berputar pelan mengelilingi foto pasangan, kain songke hitam bermotif merah-kuning-hijau sebagai pita dan ruang gelap,
// kampung mbaru niang berkabut ala Wae Rebo, dan bingkai foto berbentuk atap kerucut. Pasangan Katolik.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const WISHES = [
  { id: "w1", name: "Om Lambert & Tanta Ros", attendance: "yes" as const, message: "Proficiat untuk Yuli dan Frengky! Tuhan memberkati rumah tangga kalian, rukun seperti lingko yang semua petaknya bertemu di satu titik." },
  { id: "w2", name: "Teman OMK Katedral Ruteng", attendance: "yes" as const, message: "Selamat menempuh hidup baru, kakak berdua. Kami tunggu di misa dan di acara danding nanti!" },
  { id: "w3", name: "Keluarga Nggarang, Kupang", attendance: "maybe" as const, message: "Mohon maaf kalau belum bisa pulang ke Ruteng. Doa kami menyertai, semoga Bunda Maria selalu menuntun keluarga baru ini." },
];

const FONTS = ["Kurale", "Alegreya Sans:ital,wght@0,400;0,500;0,700;0,800;1,400"];
// Painted by /tmp/pen/art/themes/manggarai-lingko.py (songke band and weave are CSS backgrounds).
const Art = makeArt("manggarai-lingko", { lingko: [640, 640], niang: [720, 384], cone: [120, 138], divider: [382, 30] } as const);

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    kicker: "Salam Damai dalam Kristus",
    title: "Ase Kae",
    sub: "Saudara-saudari terkasih, keluarga dan sahabat",
    intro: "Dengan penuh syukur atas kasih Tuhan, kami mengundang Bapak/Ibu/Saudara/i untuk hadir dan mendoakan kami saat menerima Sakramen Perkawinan dan menjalani adat wagal bersama keluarga besar di Ruteng.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"],
  couple: ["Dua Keluarga, Satu Lingko", "Kedua Mempelai"],
  count: ["Menghitung Hari", "Menuju Hari Bahagia"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Waktu & Tempat", "Rangkaian Acara"],
  story: ["Jalan Setapak", "Kisah Kami"],
  gallery: ["Galeri", "Momen Bersama"],
  wishes: ["Doa & Kehadiran", "Ucapan & Konfirmasi"],
  gifts: ["Tanda Kasih", "Amplop Digital"],
  closing: { thanks: "Terima Kasih", text: "Kehadiran dan doa Bapak/Ibu/Saudara/i adalah berkat bagi kami. Tuhan memberkati setiap langkah kita bersama.", salam: "Salam damai, Tuhan memberkati" },
  sent: "Terima kasih, doa dan ucapan Anda sudah terkirim. Tuhan memberkati.",
  attend: { maybe: "Mungkin" },
  wishPlaceholder: "Tuliskan doa dan harapan untuk kedua mempelai…",
};

export default function ManggaraiLingkoTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const hero = data.gallery[0] ?? data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#16120e"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <span className={s.bandTop} aria-hidden />
          <p className={s.coverKicker}>Undangan {label}</p>
          <p className={s.coverSalam}>Salam damai dalam kasih Kristus</p>
          <div className={s.lingkoWrap}>
            <Art name="lingko" eager className={s.lingkoArt} />
            {hero && <div className={s.lingkoPhoto}><Photo src={hero} alt="" /></div>}
          </div>
          <h1 className={s.coverNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.guestWrap}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#fff6e4" />Buka Undangan</button>
          </div>
          <span className={s.bandBottom} aria-hidden />
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        demoWishes={WISHES}
        light="#f0d27a"
        dark="#16120e"
        copy={COPY}
        hero={(
          <header className={s.hero}>
            <p className={s.heroKicker}>Undangan {label}</p>
            <h1 className={s.heroNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {hero && <div className={s.heroPhoto}><Photo src={hero} alt="" /></div>}
            {note && <p className={s.heroNote}>{note}</p>}
            <Art name="niang" className={s.heroNiang} />
          </header>
        )}
        slots={{
          divider: <Art name="divider" className={s.divider} />,
          node: <Art name="cone" />,
          amp: <Art name="cone" />,
          countDecor: <Art name="lingko" className={s.countLingko} />,
          closingEmblem: <Art name="niang" className={s.closingNiang} />,
          sentArt: <Art name="cone" />,
        }}
      />
    </ThemeShell>
  );
}
