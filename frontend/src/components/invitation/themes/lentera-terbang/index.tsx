"use client";
// Theme "Lentera Terbang" — malam di telaga dataran tinggi: langit nila menghangat ke cakrawala bara, perbukitan
// berlapis, ratusan lentera kertas terbang dari tepi telaga dan terpantul di air. Sampul lukisan penuh dengan lapisan
// lentera yang naik perlahan (diam saat gerak dikurangi), nama rata kiri di langit; halaman biru malam dengan bingkai
// potret dan foto berbentuk lentera yang berpendar. Dilukis oleh /tmp/pen/art/themes/lentera-terbang.py.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Cormorant Garamond:ital,wght@0,600;0,700;1,600", "Jost:wght@400;500;600"];
const Art = makeArt("lentera-terbang", { lentera: [265, 304], garis: [320, 60] } as const);

const WISHES = [
  { id: "w1", name: "Keluarga Om Hendra, Surabaya", attendance: "yes" as Attendance, message: "Selamat menempuh hidup baru, Aruna dan Bastian. Semoga cinta kalian terus menyala dan menerangi satu sama lain." },
  { id: "w2", name: "Teman Paduan Suara St. Yosef", attendance: "yes" as Attendance, message: "Sudah tidak sabar ikut menerbangkan lentera! Bahagia selalu, kalian berdua." },
  { id: "w3", name: "Clara & Dimas", attendance: "maybe" as Attendance, message: "Semoga kami bisa menyusul ke Sarangan. Kalau belum sempat, doa kami ikut terbang bersama lenteranya." },
];

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    kicker: "Dengan penuh sukacita",
    title: "Satu Malam, Ratusan Harapan",
    intro: "Dengan kasih dan sukacita, kami mengundang Bapak/Ibu/Saudara/i untuk hadir pada hari pernikahan kami, lalu menerbangkan lentera bersama di tepi telaga sebagai tanda harapan bagi perjalanan yang baru dimulai.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"],
  couple: ["Dua hati", "Mempelai"],
  count: ["Lentera dinyalakan dalam", "Hitung Mundur"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Catat tanggalnya", "Waktu & Tempat"],
  story: ["Perjalanan", "Kisah Kami"],
  gallery: ["Galeri", "Cahaya Kami"],
  wishes: ["Ucapan & kehadiran", "Titip Harapan"],
  gifts: ["Tanda kasih", "Amplop Digital"],
  closing: { thanks: "Terima Kasih", text: "Kehadiran dan doa Bapak/Ibu/Saudara/i akan menjadi lentera paling terang di malam bahagia kami." },
  sent: "Terima kasih, harapan Anda sudah ikut terbang bersama lentera kami.",
  attend: { maybe: "Mungkin" },
  wishLabel: "Ucapan & Harapan",
  wishPlaceholder: "Tuliskan harapan untuk kedua mempelai…",
  giftIntro: "Kehadiran Anda adalah hadiah terindah. Jika berkenan memberi tanda kasih, dapat melalui:",
};

export default function LenteraTerbangTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel?.trim() || "Pernikahan";
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const bride = data.couple.bride?.trim();
  const groom = data.couple.groom?.trim();
  const photo = data.gallery[0];

  return (
    <ThemeShell
      fonts={FONTS}
      background="#0b0d2b"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <span className={`${s.rise} ${s.riseFar}`} aria-hidden />
          <span className={s.rise} aria-hidden />
          <p className={s.coverKicker}>{label}</p>
          <div className={s.coverNames}>
            <h1>{bride}</h1>
            {groom && <><span aria-hidden>dan</span><h1>{groom}</h1></>}
          </div>
          <p className={s.coverDate}>{formatDate(data.date)}{data.place && <small>{data.place}</small>}</p>
          <div className={s.coverFoot}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#2a1430" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        copy={COPY}
        demoWishes={WISHES}
        light="#ffd59a"
        dark="#2a1430"
        hero={(
          <header className={s.hero}>
            <span className={s.rise} aria-hidden />
            <div className={s.heroWin}>
              {photo ? <Photo src={photo} alt={`${bride} & ${groom}`} /> : <div className={s.heroArt}><Art name="lentera" /></div>}
            </div>
            <p className={s.heroLabel}>{label}</p>
            <h1 className={s.heroNames}>{bride}{groom && <> <i>&amp;</i> {groom}</>}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="garis" className={s.divider} />,
          node: <Art name="lentera" />,
          amp: <Art name="lentera" />,
          portrait: <Art name="lentera" className={s.portraitArt} />,
          closingEmblem: <Art name="lentera" className={s.closeLantern} />,
          sentArt: <Art name="lentera" />,
        }}
      />
    </ThemeShell>
  );
}
