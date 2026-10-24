"use client";
// Theme "Dermaga Kayu" — dermaga kayu panjang menjorok ke laut tenang saat matahari terbit, dalam cat air pastel. Sampul
// berupa lukisan dermaga satu halaman penuh dengan nama di langit fajar dan kartu tamu di ujung papan; tata letak rata kiri
// seperti catatan yang disematkan di tiang, kartu acara beratap papan kayu, tali tambang bersimpul, kerang, dan camar.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["DM Serif Display", "Spectral:ital,wght@0,400;0,600;1,400", "Josefin Sans:wght@600"];
// Painted by /tmp/pen/art/themes/dermaga-kayu.py.
const Art = makeArt("dermaga-kayu", { dermaga: [760, 1360], camar: [200, 52], kerang: [90, 60], ombak: [780, 171], tali: [440, 43] } as const);

const WISHES = [
  { id: "w1", name: "Keluarga Yohanes Gunawan", attendance: "yes" as Attendance, message: "Selamat menempuh hidup baru, Alya dan Dimas. Semoga perjalanan kalian setenang laut pagi dan sehangat matahari terbitnya." },
  { id: "w2", name: "Teman Snorkeling Lengkuas", attendance: "yes" as Attendance, message: "Akhirnya! Kami siap bangun subuh demi kalian. Sampai jumpa di ujung dermaga!" },
  { id: "w3", name: "Sekar & Bima", attendance: "maybe" as Attendance, message: "Semoga bisa terbang ke Belitung. Kalaupun belum, doa terbaik kami ikut berlayar bersama kalian." },
];

export default function DermagaKayuTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const heroPhoto = data.gallery[0] ?? data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  const copy: ThemeCopy = {
    ...DEFAULT_COPY,
    opening: {
      kicker: "Salam hangat dari tepi laut",
      title: "Di Ujung Dermaga, Kami Berjanji",
      intro: "Dengan penuh syukur, kami mengundang Bapak/Ibu/Saudara/i untuk menyaksikan janji kami saat matahari terbit. Kehadiran dan doa restu Anda akan menjadi cahaya pertama dalam perjalanan kami berdua.",
    },
    roles: ["Mempelai Wanita", "Mempelai Pria"],
    couple: ["Dua penumpang, satu perahu", "Kami Berdua"],
    count: ["Menunggu fajar", "Hitung Mundur"],
    units: ["Hari", "Jam", "Menit", "Detik"],
    events: ["Waktu & tempat", "Rangkaian Acara"],
    story: ["Catatan perjalanan", "Kisah Kami"],
    gallery: ["Galeri", "Pagi-pagi Kami"],
    wishes: ["Pesan dalam botol", "Ucapan & Kehadiran"],
    gifts: ["Tanda kasih", "Hadiah Pernikahan"],
    closing: { thanks: "Terima Kasih", text: "Terima kasih telah menjadi bagian dari pagi terindah kami. Sampai jumpa di ujung dermaga." },
    sent: "Terima kasih, pesanmu sudah sampai ke dermaga kami.",
    attend: { maybe: "Mungkin" },
    wishPlaceholder: "Tuliskan pesan dan doa untuk kami berdua…",
    giftIntro: "Kehadiran Anda adalah hadiah terbaik. Jika berkenan memberi tanda kasih, dapat melalui:",
  };

  return (
    <ThemeShell
      fonts={FONTS}
      background="#f3d4cc"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Art name="dermaga" eager className={s.scene} />
          <Art name="camar" eager className={s.gulls} />
          <p className={s.kicker}>The Wedding of</p>
          <h1 className={s.coverNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.guestWrap}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#fffaf6" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#f8dcc0"
        dark="#263c52"
        copy={copy}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            {heroPhoto && <div className={s.heroPhoto}><Photo src={heroPhoto} alt="" /></div>}
            <p className={s.heroKicker}>{label}</p>
            <h1 className={s.heroNames}>{data.couple.bride} <em>&amp;</em> {data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            <Art name="tali" className={s.heroTali} />
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="tali" className={s.divider} />,
          node: <Art name="kerang" />,
          amp: <Art name="kerang" />,
          countDecor: <Art name="ombak" className={s.countOmbak} />,
          closingDecor: <Art name="ombak" className={s.closingDecor} />,
          closingEmblem: <Art name="camar" className={s.closingEmblem} />,
          sentArt: <Art name="kerang" />,
        }}
      />
    </ThemeShell>
  );
}
