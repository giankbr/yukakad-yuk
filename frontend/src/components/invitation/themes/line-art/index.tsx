"use client";
// Theme "Line Art" — minimalis: satu garis tinta pena-kuas yang tak terputus membentuk sepasang kekasih (profil, mata
// terpejam, tanpa wajah rinci), sapuan cat air biru kobalt sebagai satu-satunya warna, ranting bunga bergaris tunggal,
// tata letak rata kiri bernomor dengan garis rambut, foto hitam-putih, dan ruang putih yang lapang.
import { Lucide, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Cormorant Upright:wght@400;500", "Manrope:wght@400;500;600"];
// Painted by /tmp/pen/art/themes/line-art.py.
const Art = makeArt("line-art", { pasangan: [640, 635], ranting: [166, 490], bunga: [300, 48] } as const);

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    kicker: "Dengan penuh syukur",
    title: "Dua garis, satu cerita",
    intro: "Dengan sukacita kami mengundang Bapak/Ibu/Saudara/i untuk hadir dan menjadi saksi hari ketika dua perjalanan kami bersambung menjadi satu.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"],
  couple: ["Kami berdua", "Mempelai"],
  count: ["Tinggal sebentar lagi", "Hitung Mundur"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Catat tanggalnya", "Acara"],
  story: ["Dari titik pertama", "Cerita Kami"],
  gallery: ["Beberapa momen", "Galeri"],
  wishes: ["Tinggalkan pesan", "Ucapan & Kehadiran"],
  gifts: ["Bila berkenan", "Tanda Kasih"],
  closing: {
    thanks: "Terima kasih",
    text: "Kehadiran dan doa Bapak/Ibu/Saudara/i adalah garis terindah dalam lembar cerita kami.",
  },
  sent: "Terima kasih, pesan Anda sudah kami terima.",
  attend: { maybe: "Mungkin" },
  wishPlaceholder: "Tulis ucapan untuk Alya & Raka…",
  closedNote: "Terima kasih sudah menjadi bagian dari hari kami. Ucapan masih bisa dikirim lewat form ini.",
  giftIntro: "Kehadiran Anda sudah lebih dari cukup. Bila ingin mengirim tanda kasih, dapat melalui:",
};

const WISHES = [
  { id: "w1", name: "Kak Nadine", attendance: "yes" as const, message: "Dari murid yang tidak bisa menggambar garis lurus jadi suami pelukis. Selamat, kalian berdua!" },
  { id: "w2", name: "Keluarga Gunawan", attendance: "yes" as const, message: "Selamat menempuh hidup baru. Semoga selalu saling menemukan di setiap halaman." },
  { id: "w3", name: "Tim Galeri Ruang Putih", attendance: "maybe" as const, message: "Kami siapkan dinding terbaik untuk karya kalian berikutnya. Bahagia selalu!" },
];

export default function LineArtTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const { bride, groom } = data.couple;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const label = data.eventLabel?.trim() || "Pernikahan";
  const year = /\d{4}/.exec(data.date ?? "")?.[0];
  const copy = { ...COPY, wishPlaceholder: `Tulis ucapan untuk ${bride} & ${groom}…` };

  return (
    <ThemeShell
      fonts={FONTS}
      background="#efece4"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.coverTop}><span>{label}</span>{year && <span>{year}</span>}</div>
          <Art name="pasangan" eager className={s.coverArt} />
          <div className={s.coverText}>
            <h1 className={s.coverNames}>{bride}<em>&amp; {groom}</em></h1>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
            <div className={s.coverRow}>
              <div className={s.guest}>
                <small>Kepada Yth.</small>
                <strong>{guestLabel(data)}</strong>
                {table && <span className={s.table}>{table}</span>}
              </div>
              <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={15} color="#ffffff" />Buka</button>
            </div>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        copy={copy}
        demoWishes={WISHES}
        light="#ffffff"
        dark="#1d1b19"
        hero={(
          <header className={s.hero}>
            <Art name="pasangan" className={s.heroArt} />
            <p className={s.heroKicker}>{label}</p>
            <h1 className={s.heroNames}>{bride}<em>&amp; {groom}</em></h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="bunga" className={s.divider} />,
          portrait: <Art name="ranting" />,
          closingEmblem: <Art name="ranting" className={s.closingArt} />,
          sentArt: <Art name="ranting" />,
        }}
      />
    </ThemeShell>
  );
}
