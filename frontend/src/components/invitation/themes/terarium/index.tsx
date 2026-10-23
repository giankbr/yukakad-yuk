"use client";
// Theme "Terarium" — taman mini dalam kaca, botanical-modern: terarium bola berisi lumut, ekeveria, pakis dan
// kerikil, terarium geometris berangka kuningan yang tergantung dan berayun pelan, serta sungkup kaca kecil di atas
// rak kayu, dilukis cat air. Tata letak editorial rata kiri, Instrument Serif dan Hanken Grotesk.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Instrument Serif:ital@0;1", "Hanken Grotesk:wght@400;500;600;700"];
// Painted by /tmp/pen/art/themes/terarium.py.
const Art = makeArt("terarium", {
  globe: [320, 284], geo: [200, 408], cloche: [170, 185], fern: [280, 32], sprig: [72, 53],
} as const);

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    kicker: "Dengan penuh sukacita",
    title: "Kami akan menikah",
    sub: "Dua hati, satu taman kecil yang kami rawat bersama",
    intro: "Dengan penuh syukur kami mengundang Bapak/Ibu/Saudara/i untuk hadir dan menjadi bagian dari hari bahagia kami. Kehadiran dan doa Anda adalah cahaya yang membuat taman kecil ini tumbuh.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"],
  couple: ["Yang berbahagia", "Kami Berdua"],
  count: ["Menghitung hari", "Sampai Bertemu"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Waktu & tempat", "Rangkaian Acara"],
  story: ["Cerita kami", "Tumbuh Perlahan"],
  gallery: ["Galeri", "Potret Kami"],
  wishes: ["Doa & kehadiran", "Ucapan & RSVP"],
  gifts: ["Tanda kasih", "Hadiah"],
  closing: {
    thanks: "Terima kasih",
    text: "Terima kasih telah menjadi bagian dari perjalanan kami. Sampai jumpa di antara pakis dan cahaya rumah kaca.",
  },
  sent: "Terima kasih, ucapan Anda sudah kami terima dengan hangat.",
  attend: { maybe: "Mungkin" },
  wishPlaceholder: "Tuliskan ucapan dan doa untuk kami berdua…",
};

const WISHES = [
  { id: "w1", name: "Tante Yuliana & Om Bram", attendance: "yes" as const, message: "Selamat Anin dan Bas! Semoga rumah tangga kalian selalu hijau, sejuk, dan penuh pertumbuhan seperti terarium kalian." },
  { id: "w2", name: "Komunitas Lumut Bandung", attendance: "yes" as const, message: "Dari kelas terarium ke pelaminan! Kami datang, dan sudah menyiapkan toples paling bagus sebagai kado." },
  { id: "w3", name: "Gita Prameswari", attendance: "maybe" as const, message: "Semoga bisa menyusul dari Jakarta. Bahagia selalu, kalian berdua pasangan yang paling sabar merawat sesuatu." },
];

export default function TerariumTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const photo = data.gallery[0] ?? data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const groom = data.couple.groom?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#f4f3ed"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Art name="geo" eager className={s.hang} />
          <p className={s.kicker}>Undangan {label}</p>
          <h1 className={s.coverNames}><span>{data.couple.bride}</span>{groom && <><em>&amp;</em><span>{groom}</span></>}</h1>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.shelf} aria-hidden>
            <Art name="cloche" eager className={s.cloche} />
            <Art name="globe" eager className={s.globe} />
          </div>
          <div className={s.coverFoot}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#f4f3ed" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        demoWishes={WISHES}
        light="#e3c98f"
        dark="#1d3a2a"
        copy={COPY}
        hero={(
          <header className={s.hero}>
            <div className={s.heroJar}>
              <div className={s.heroPhoto}>{photo ? <Photo src={photo} alt={`${data.couple.bride}${groom ? ` dan ${groom}` : ""}`} /> : <span className={s.heroMono} aria-hidden>{data.couple.bride.slice(0, 1)}</span>}</div>
              <span className={s.heroShine} aria-hidden />
            </div>
            <p className={s.heroKicker}>The Wedding of</p>
            <h1 className={s.heroNames}><span>{data.couple.bride}</span>{groom && <><em>&amp;</em><span>{groom}</span></>}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="fern" className={s.divider} />,
          node: <Art name="sprig" />,
          amp: <Art name="sprig" />,
          countDecor: <Art name="cloche" className={s.countJar} />,
          closingEmblem: <Art name="globe" className={s.closingEmblem} />,
          sentArt: <Art name="cloche" />,
        }}
      />
    </ThemeShell>
  );
}
