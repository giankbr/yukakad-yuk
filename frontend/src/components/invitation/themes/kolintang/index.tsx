"use client";
// Theme "Kolintang" — dataran tinggi Tomohon saat senja (desain orisinal, cat air + gouache): Gunung Lokon dan Empung
// dengan asap tipis, kabut, petak kebun krisan, rumah panggung kayu, dan sebuah kolintang melodi berbilah kayu di sampul
// hijau hutan. Nama di langit, kartu tamu bertepi bilah kayu; potret dan foto dibingkai bilah kayu berpaku, hitung mundur
// berupa empat bilah bertingkat yang dipukul bergiliran, alur kisah di atas rel merah alat musik. Salam "Syalom" dan
// "Pakatuan wo Pakalawiren" untuk pasangan Kristen Minahasa.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Young Serif", "Hanken Grotesk:wght@400;600;700;800"];
// Painted by /tmp/pen/art/themes/kolintang.py
const Art = makeArt("kolintang", { kolintang: [760, 273], krisan: [326, 277], bilah: [360, 78] } as const);

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    kicker: "Syalom",
    title: "Pakatuan wo Pakalawiren",
    sub: "Panjang umur dan sejahtera bagi kita semua",
    intro: "Dengan penuh syukur atas kasih Tuhan Yesus Kristus, kami bermaksud menyelenggarakan pemberkatan nikah dan resepsi putra-putri kami. Merupakan sukacita bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan turut mendoakan.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"],
  couple: ["Dua nada, satu lagu", "Kedua Mempelai"],
  count: ["Menanti nada pertama", "Menuju Hari Bahagia"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Waktu & Tempat", "Rangkaian Acara"],
  story: ["Dari latihan ke pelaminan", "Kisah Kami"],
  gallery: ["Dari Tomohon", "Galeri Kami"],
  wishes: ["Doa & Kehadiran", "Ucapan & Konfirmasi"],
  gifts: ["Tanda Kasih", "Amplop Digital"],
  closing: {
    thanks: "Makase Banyak",
    text: "Kehadiran dan doa Bapak/Ibu/Saudara/i adalah berkat bagi kami sekeluarga. Kiranya Tuhan memberkati setiap langkah kita.",
    salam: "Tuhan Yesus memberkati",
  },
  sent: "Makase banyak, doa dan ucapan Anda sudah sampai.",
  attend: { maybe: "Mungkin" },
  wishPlaceholder: "Tuliskan doa dan ucapan untuk kedua mempelai…",
};

const WISHES = [
  { id: "w1", name: "Oma Nelly Kawengian", attendance: "yes" as Attendance, message: "Pakatuan wo pakalawiren, Mikha deng Rey. Tuhan Yesus memberkati rumah tangga kalian, jadi terang dan berkat bagi banyak orang." },
  { id: "w2", name: "Ansambel Kolintang Jemaat", attendance: "yes" as Attendance, message: "Bas deng melodi so jadi satu lagu! Torang sudah siap latihan lagu pengiring. Sampai ketemu di Kakaskasen." },
  { id: "w3", name: "Tante Vera, Jakarta", attendance: "maybe" as Attendance, message: "Mudah-mudahan bisa pulang ke Tomohon. Doa terbaik dari kami sekeluarga, selamat menempuh hidup baru." },
];

export default function KolintangTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const hero = data.gallery[0] ?? data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#10281d"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <span className={s.scene} aria-hidden />
          <p className={s.syalom}>Syalom</p>
          <p className={s.kicker}>Undangan {label}</p>
          <h1 className={s.names}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <span className={s.spacer} aria-hidden />
          <div className={s.instrument} aria-hidden>
            <Art name="kolintang" eager />
            <span className={s.strike} />
          </div>
          <div className={s.guestCard}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={17} color="#fff8ea" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#fff8ea"
        dark="#173828"
        copy={COPY}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            <p className={s.heroKicker}>Syalom &middot; {label}</p>
            <h1 className={s.heroNames}>{data.couple.bride} <em>&amp;</em> {data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {hero && (
              <div className={s.heroFrame}>
                <div className={s.heroPhoto}><Photo src={hero} alt={`${data.couple.bride} dan ${data.couple.groom}`} /></div>
                <Art name="krisan" className={s.heroKrisan} />
              </div>
            )}
            <Art name="bilah" className={s.heroBilah} />
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="bilah" className={s.divider} />,
          amp: <Art name="krisan" />,
          portrait: <Art name="krisan" className={s.pSprig} />,
          countDecor: <Art name="krisan" className={s.countKrisan} />,
          closingEmblem: <Art name="kolintang" className={s.closingKol} />,
          sentArt: <Art name="krisan" />,
        }}
      />
    </ThemeShell>
  );
}
