"use client";
// Theme "Perpustakaan Tua" — ruang baca tua yang dilukis dengan gouache: dinding rak kenari penuh punggung buku kulit
// dan kain bersepuh, tangga perpustakaan di rel kuningan, lampu meja hijau yang cahayanya bernapas pelan, dan bingkai
// ex-libris berukir tempat nama mempelai tertulis. Hero adalah halaman judul sebuah buku, acara tampil sebagai kartu
// katalog di laci beledu hijau, hitung mundur sebagai empat jilid di rak, kisah sebagai daftar isi, ucapan sebagai buku
// tamu bergaris. Untuk pasangan umum (netral).
import type { CSSProperties } from "react";
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Sorts Mill Goudy:ital@0;1", "Vollkorn:ital,wght@0,400;0,600;1,400", "Mrs Saint Delafield"];
// Painted by /tmp/pen/art/themes/perpustakaan-tua.py (tools/art/themes in the repo).
const Art = makeArt("perpustakaan-tua", {
  lamp: [230, 199], plate: [320, 478], spines: [310, 122], fleuron: [210, 27],
} as const);

const COPY = {
  ...DEFAULT_COPY,
  opening: {
    kicker: "Prakata",
    title: "Sebuah Bab Baru",
    intro: "Dengan penuh syukur kepada Tuhan Yang Maha Esa, kami mengundang Bapak/Ibu/Saudara/i untuk hadir dan menjadi saksi ketika dua kisah kami dijilid menjadi satu buku. Kehadiran dan doa restu Anda akan menjadi halaman paling berharga di dalamnya.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"] as [string, string],
  couple: ["Para Tokoh", "Kedua Mempelai"] as [string, string],
  count: ["Halaman demi halaman", "Menuju Hari Bahagia"] as [string, string],
  units: ["Hari", "Jam", "Menit", "Detik"] as [string, string, string, string],
  events: ["Katalog Acara", "Waktu & Tempat"] as [string, string],
  story: ["Daftar Isi", "Kisah Kami"] as [string, string],
  gallery: ["Lampiran", "Galeri Foto"] as [string, string],
  wishes: ["Buku Tamu", "Ucapan & Kehadiran"] as [string, string],
  gifts: ["Tanda Kasih", "Amplop Digital"] as [string, string],
  closing: {
    thanks: "Tamat",
    text: "Namun kisah ini baru dimulai. Terima kasih telah menjadi bagian dari halaman-halamannya. Kehadiran dan doa Bapak/Ibu/Saudara/i sangat berarti bagi kami.",
    salam: "Dengan hormat dan terima kasih",
  },
  attend: { maybe: "Mungkin" } as Partial<Record<Attendance, string>>,
  sent: "Terima kasih, ucapan Anda sudah tercatat di buku tamu kami.",
  wishPlaceholder: "Tuliskan satu kalimat untuk buku tamu kami…",
  closedNote: "Terima kasih atas doa dan perhatiannya. Buku tamu masih terbuka untuk ucapan.",
  giftIntro: "Doa restu Anda adalah hadiah terindah. Bila berkenan mengirim tanda kasih, dapat melalui:",
  familyLabel: "Dengan hormat, kami yang berbahagia",
};

const WISHES = [
  { id: "w1", name: "Bu Sekar", attendance: "yes" as Attendance, message: "Selamat, Anindya dan Raka! Semoga rumah tangga kalian seperti perpustakaan yang baik: selalu ada tempat untuk cerita baru." },
  { id: "w2", name: "Komunitas Baca Kamisan", attendance: "yes" as Attendance, message: "Kami datang membawa buku untuk ditukar. Bahagia selalu, pasangan pembaca favorit kami!" },
  { id: "w3", name: "Dimas & Laila", attendance: "maybe" as Attendance, message: "Masih menunggu jadwal dinas, semoga bisa menyusul ke resepsi. Doa terbaik dari Yogyakarta." },
];

// Lucide "book-open" (ISC license).
const BOOK_OPEN = "<path d=\"M12 7v14\" /> <path d=\"M3 18a1 1 0 0 1-1-1V4a1 1 0 0 1 1-1h5a4 4 0 0 1 4 4 4 4 0 0 1 4-4h5a1 1 0 0 1 1 1v13a1 1 0 0 1-1 1h-6a3 3 0 0 0-3 3 3 3 0 0 0-3-3z\" />";

const MOTES = [[18, 64, 0], [32, 74, 3.5], [44, 58, 7], [26, 50, 9.5], [52, 70, 5]] as const;

function Lamp({ className, eager, motes }: { className?: string; eager?: boolean; motes?: boolean }) {
  return (
    <span className={`${s.lamp} ${className ?? ""}`} aria-hidden>
      <Art name="lamp" eager={eager} />
      {motes && MOTES.map(([x, y, d]) => <span key={d} className={s.mote} style={{ left: `${x}%`, top: `${y}%`, animationDelay: `${d}s` } as CSSProperties} />)}
    </span>
  );
}

export default function PerpustakaanTuaTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const photo = data.gallery[0] ?? data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const groom = data.couple.groom?.trim();
  const names = [data.couple.bride, groom].filter(Boolean).join(" & ");

  return (
    <ThemeShell
      fonts={FONTS}
      background="#1c100a"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.plate}>
            <p className={s.exLibris}>Ex Libris</p>
            <p className={s.coverKicker}>Undangan {label}</p>
            <h1 className={s.coverNames}>
              <span>{data.couple.bride}</span>
              {groom && <><em>&amp;</em><span>{groom}</span></>}
            </h1>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
            <span className={s.coverRule} aria-hidden />
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
          </div>
          <button type="button" className={s.openBtn} onClick={open}><Lucide icon={BOOK_OPEN} size={16} color="#f3e8cf" />Buka Undangan</button>
          <span className={s.coverDesk} aria-hidden />
          <Lamp className={s.coverLamp} eager motes />
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#f3e8cf"
        dark="#2e1f15"
        copy={COPY}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            <div className={s.page}>
              <p className={s.pageKicker}>{label}</p>
              <div className={s.pagePhoto}>
                {photo ? <Photo src={photo} alt={names} /> : <span aria-hidden />}
              </div>
              <h1 className={s.heroNames}>{data.couple.bride}{groom && <><em>&amp;</em>{groom}</>}</h1>
              {note && <p className={s.heroNote}>{note}</p>}
              <p className={s.colophon}><span>Cetakan Pertama</span><span>{formatDate(data.date)}</span></p>
            </div>
          </header>
        )}
        slots={{
          divider: <Art name="fleuron" className={s.divider} />,
          amp: <Art name="fleuron" />,
          countDecor: <span className={s.countShelf} aria-hidden />,
          closingDecor: <Lamp className={s.closingLamp} motes />,
          closingEmblem: <Art name="spines" className={s.closingEmblem} />,
          sentArt: <Art name="spines" />,
        }}
      />
    </ThemeShell>
  );
}
