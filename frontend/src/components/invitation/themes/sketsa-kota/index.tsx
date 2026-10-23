"use client";
// Theme "Sketsa Kota" — halaman buku sketsa ala urban sketcher: garis pena longgar yang melewati sudut dan cat air yang
// meluber di pojok jalan kota lama (ruko berfasad lengkung, jendela krepyak hijau, lampu jalan, kabel listrik, pohon
// flamboyan). Cover berupa halaman berjilid spiral dengan catatan tulisan tangan dan cap, kartu tamu ditempel selotip,
// foto-foto sebagai cetakan berselotip, bingkai bergaris pena, dan bintik uji warna sebagai penanda.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Instrument Serif:ital@0;1", "Archivo:wght@400;500;600;700", "Architects Daughter"];
// Painted by /tmp/pen/art/themes/sketsa-kota.py (tools/art/themes in the repo).
const Art = makeArt("sketsa-kota", {
  scene: [780, 820], skyline: [600, 173], window: [150, 218], swatches: [340, 34], swatch: [56, 64],
} as const);

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  attend: { maybe: "Mungkin" },
  opening: {
    kicker: "Halo, teman-teman!",
    title: "Satu Halaman Baru",
    intro: "Setelah banyak jalan kaki dan banyak halaman sketsa, kami memutuskan untuk melanjutkan cerita berdua. Dengan penuh sukacita, kami mengundang Bapak/Ibu/Saudara/i untuk hadir dan merayakan hari pernikahan kami.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"],
  couple: ["yang menggambar", "Kedua Mempelai"],
  count: ["sebentar lagi…", "Hitung Mundur"],
  units: ["hari", "jam", "menit", "detik"],
  events: ["catat tanggalnya", "Waktu & Tempat"],
  story: ["dari buku sketsa", "Cerita Kami"],
  gallery: ["tempelan foto", "Galeri"],
  wishes: ["tinggalkan catatan", "Ucapan & Kehadiran"],
  gifts: ["tanda kasih", "Amplop Digital"],
  closing: { thanks: "Terima Kasih", text: "Kehadiran dan doa Bapak/Ibu/Saudara/i akan menjadi warna terindah di halaman baru kami." },
  sent: "Terima kasih, catatanmu sudah kami simpan.",
  wishPlaceholder: "Tulis ucapan dan doa untuk kami berdua…",
  closedNote: "Terima kasih atas doa dan perhatiannya. Ucapan masih bisa dikirim lewat form ini.",
  familyLabel: "Dengan hormat kami",
};

const WISHES = [
  { id: "w1", name: "Mbak Sekar & Partner", attendance: "yes" as Attendance, message: "Akhirnya! Dari sketchwalk Minggu pagi sampai pelaminan. Bahagia selalu, kalian berdua." },
  { id: "w2", name: "Komunitas Sketsa Semarang", attendance: "yes" as Attendance, message: "Kami datang bawa buku sketsa ya. Siap menggambar resepsi kalian langsung di tempat!" },
  { id: "w3", name: "Om Budi & Tante Wati", attendance: "maybe" as Attendance, message: "Selamat menempuh hidup baru, Kirana dan Damar. Semoga rukun dan saling melengkapi seperti garis dan warna." },
];

export default function SketsaKotaTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const table = tableLabel(data.guestTable);
  const photo = data.gallery[0] ?? data.couple.bridePhoto;
  const note = data.couple.note?.trim();
  const year = formatDate(data.date).match(/\d{4}/)?.[0];

  return (
    <ThemeShell
      fonts={FONTS}
      background="#34494c"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <p className={s.caption}><span>pojok kota lama, Minggu pagi</span><span className={s.stamp}>Sketsa<br />{year ?? "No. 1"}</span></p>
          <div className={s.coverSketch}><Art name="scene" className={s.sketch} eager /></div>
          <div className={s.coverText}>
            <p className={s.kicker}>Undangan {label}</p>
            <h1 className={s.coverNames}>{data.couple.bride} <em>&amp;</em> {data.couple.groom}</h1>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
          </div>
          <div className={s.note}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#fffcf5" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#fffcf5"
        dark="#2b2a30"
        copy={COPY}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            <p className={s.heroKicker}>kami akan menikah</p>
            <h1 className={s.heroNames}>{data.couple.bride} <em>&amp;</em> {data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            <div className={s.print}>
              <div className={s.heroPhoto}>{photo ? <Photo src={photo} alt={`${data.couple.bride} & ${data.couple.groom}`} /> : <span aria-hidden>{data.couple.bride.slice(0, 1)}</span>}</div>
              <p className={s.printCap}>{data.couple.bride} &amp; {data.couple.groom}</p>
              <Art name="window" className={s.heroWindow} />
            </div>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="swatches" className={s.divider} />,
          node: <Art name="swatch" />,
          amp: <Art name="swatch" />,
          portrait: <Art name="swatch" className={s.portraitArt} />,
          closingDecor: <Art name="skyline" className={s.closingSky} />,
          closingEmblem: <Art name="window" className={s.closingEmblem} />,
          sentArt: <Art name="window" />,
        }}
      />
    </ThemeShell>
  );
}
