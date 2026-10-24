"use client";
// Theme "Pasar Bunga" — kios pasar bunga yang ceria: buket besar terbungkus kertas kraft bertali merah dengan kartu nama
// mempelai yang diikat di bungkusnya, papan kapur untuk nama tamu, deretan ember seng berisi tulip, bunga matahari,
// krisan dan lavender, tenda bergaris hijau di pita hitung mundur dan penutup. Cat air dan gouache, gerak yang ceria.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Young Serif:wght@400", "DM Sans:wght@400;500;700", "Caveat Brush:wght@400"];
// Painted by /tmp/pen/art/themes/pasar-bunga.py (kraft tile and awning stripe are CSS backgrounds)
const Art = makeArt("pasar-bunga", { bouquet: [560, 676], buckets: [764, 291], posy: [220, 169], sprig: [300, 45] } as const);

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    kicker: "Halo, kamu!",
    title: "Satu Ikat Kabar Bahagia",
    intro: "Dengan penuh sukacita, kami mengundang Bapak/Ibu/Saudara/i untuk merayakan hari pernikahan kami. Datanglah, bawa senyum terbaikmu, dan pulanglah membawa seikat bunga dari kebun kami.",
  },
  roles: ["Mempelai Perempuan", "Mempelai Laki-laki"],
  couple: ["Penjual & Pembeli Pertama", "Kedua Mempelai"],
  count: ["Bunga mekar dalam", "Hitung Mundur"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Catat di kalender", "Rangkaian Acara"],
  story: ["Dari kios kecil", "Kisah Kami"],
  gallery: ["Album kami", "Galeri"],
  wishes: ["Tulis di kartu", "Ucapan & Konfirmasi"],
  gifts: ["Tanda kasih", "Amplop Digital"],
  closing: {
    thanks: "Terima Kasih",
    text: "Terima kasih sudah menjadi bagian dari kisah kami. Kehadiran dan doa kalian adalah buket terindah hari itu.",
    salam: "Sampai jumpa di kebun!",
  },
  sent: "Terima kasih! Ucapanmu sudah kami selipkan di buket.",
  attend: { maybe: "Mungkin" },
  wishPlaceholder: "Tulis ucapan dan doa untuk kami berdua…",
};

const WISHES = [
  { id: "w1", name: "Kak Anindya & Partner", attendance: "yes" as Attendance, message: "Dari pelanggan setia kios Kirana: selamat ya! Semoga rumah tangga kalian selalu segar dan wangi seperti ember mawar hari Sabtu." },
  { id: "w2", name: "Bu Darsih (Kios Melati)", attendance: "yes" as Attendance, message: "Ibu ikut bahagia, Nak. Nanti melati untuk kalian Ibu siapkan yang paling bagus." },
  { id: "w3", name: "Rizal, teman kantor Dimas", attendance: "maybe" as Attendance, message: "Masih menunggu jadwal dinas luar kota, semoga bisa datang. Selamat menempuh hidup baru!" },
];

export default function PasarBungaTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const hero = data.gallery[0] ?? data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#f7f1e6"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <p className={s.kicker}>Undangan {label}</p>
          <div className={s.bouquetWrap}>
            <Art name="bouquet" eager className={s.coverBouquet} />
            <div className={s.card}>
              <h1 className={s.coverNames}><span>{data.couple.bride}</span><em>&amp;</em><span>{data.couple.groom}</span></h1>
              <p className={s.coverDate}>{formatDate(data.date)}</p>
            </div>
          </div>
          <div className={s.board}>
            <small>Untuk yang tersayang,</small>
            <strong>{guestLabel(data)}</strong>
            {table && <span className={s.table}>{table}</span>}
          </div>
          <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#ffffff" />Buka Undangan</button>
          <Art name="buckets" eager className={s.coverBuckets} />
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        copy={COPY}
        demoWishes={WISHES}
        light="#f4f1e8"
        dark="#2f5a3f"
        hero={(
          <header className={s.hero}>
            <div className={s.heroAwning} aria-hidden />
            <div className={s.heroFrame}>
              <div className={s.heroPhoto}><Photo src={hero} alt="" /></div>
              <span aria-hidden><Art name="posy" className={s.heroPosy} /></span>
            </div>
            <p className={s.heroKicker}>Undangan {label}</p>
            <h1 className={s.heroNames}>{data.couple.bride} <em>&amp;</em> {data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="sprig" className={s.divider} />,
          node: <Art name="posy" />,
          amp: <Art name="sprig" />,
          portrait: <Art name="posy" className={s.portraitPosy} />,
          closingDecor: <Art name="buckets" className={s.closingBuckets} />,
          closingEmblem: <Art name="posy" className={s.closingEmblem} />,
          sentArt: <Art name="posy" />,
        }}
      />
    </ThemeShell>
  );
}
