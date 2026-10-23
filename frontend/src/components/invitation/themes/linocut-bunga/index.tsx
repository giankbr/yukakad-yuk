"use client";
// Theme "Linocut Bunga" — cetak cukil lino dua warna. Sampul berupa satu lembar cetakan di atas kertas krem: blok
// merah (bunga madat, kosmos, matahari berukir) dan blok hitam (batang, daun bergurat, rumput, payung bunga liar)
// yang sedikit meleset registrasinya, lengkap dengan catatan pensil di margin seperti edisi cetak seni. Di dalam:
// frieze blok hitam berukir, potret sebagai pelat cetak dengan bayangan merah, kartu acara seperti lembar uji cetak.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Alegreya:ital,wght@0,400;0,700;0,800;1,400;1,700", "Alegreya Sans:wght@400;500;700", "Caveat:wght@500;600"];
// Painted by /tmp/pen/art/themes/linocut-bunga.py (paper.webp is a CSS background).
const Art = makeArt("linocut-bunga", { print: [520, 666], sprig: [423, 68], bloom: [220, 223], stalks: [260, 563], frieze: [780, 187] } as const);

const WISHES = [
  { id: "w1", name: "Teman-teman Kelas Cetak Sabtu", attendance: "yes" as const, message: "Dari meja kerja yang belepotan tinta sampai pelaminan. Selamat, Wulan dan Gema! Kami bawa rol cadangan." },
  { id: "w2", name: "Tante Ivonne & Om Rudi", attendance: "yes" as const, message: "Semoga rumah tangga kalian seperti cetakan yang baik: rapi, jujur, dan makin indah setiap kali dicetak ulang." },
  { id: "w3", name: "Kak Sarah Malau", attendance: "maybe" as const, message: "Masih menunggu jadwal dari kantor, semoga bisa hadir. Doa terbaik untuk kalian berdua." },
];

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    kicker: "Dengan sukacita",
    title: "Dicetak dengan Cinta",
    intro: "Atas berkat Tuhan Yang Maha Esa, kami mengundang Bapak/Ibu/Saudara/i untuk hadir dan berbagi bahagia di hari pernikahan kami. Seperti dua blok warna yang dicetak di satu lembar, kami memulai cerita yang sama.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"],
  couple: ["Dua Warna", "Kedua Mempelai"],
  count: ["Menunggu Tinta Kering", "Menuju Hari Bahagia"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Lembar Acara", "Waktu & Tempat"],
  story: ["Dari Meja Cetak", "Cerita Kami"],
  gallery: ["Lembar Uji", "Galeri"],
  wishes: ["Buku Tamu", "Ucapan & Kehadiran"],
  gifts: ["Tanda Kasih", "Amplop Digital"],
  closing: { thanks: "Terima Kasih", text: "Kehadiran dan doa Bapak/Ibu/Saudara/i adalah warna yang melengkapi lembar bahagia kami." },
  sent: "Terima kasih, ucapan Anda sudah tercetak di buku tamu kami.",
  attend: { maybe: "Mungkin" },
  wishPlaceholder: "Tuliskan ucapan dan doa untuk Wulan & Gema…",
};

export default function LinocutBungaTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const hero = data.gallery[0] ?? data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);
  const year = /^(\d{4})/.exec(data.date ?? "")?.[1];
  const initials = [data.couple.bride, data.couple.groom].map(n => n?.trim().slice(0, 1)).filter(Boolean).join(" & ");

  return (
    <ThemeShell
      fonts={FONTS}
      background="#f2e8d5"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.sheetTop} aria-hidden><span>no. 1/150</span><span>cukil lino, dua warna</span></div>
          <div className={s.plate}><Art name="print" eager className={s.coverPrint} /></div>
          <div className={s.caption} aria-hidden><span>&ldquo;Bunga Liar&rdquo;{year && `, ${year}`}</span><b>{initials}</b></div>
          <p className={s.kicker}>Undangan {label}</p>
          <h1 className={s.coverNames}>{data.couple.bride} <em>&amp;</em> {data.couple.groom}</h1>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.guestWrap}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#f8f1e3" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        copy={COPY}
        demoWishes={WISHES}
        light="#f2e8d5"
        dark="#1d1a17"
        hero={(
          <header className={s.hero}>
            <Art name="frieze" className={s.heroFrieze} />
            <p className={s.heroKicker}>{label}</p>
            <h1 className={s.heroNames}><span>{data.couple.bride}</span><em>&amp;</em><span>{data.couple.groom}</span></h1>
            {hero && <div className={s.heroPlate}><Photo src={hero} alt="" /></div>}
            <Art name="stalks" className={s.heroStalks} />
            <Art name="stalks" className={s.heroStalksL} />
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {data.couple.note && <p className={s.heroNote}>{data.couple.note}</p>}
          </header>
        )}
        slots={{
          divider: <span className={s.divider} aria-hidden><Art name="sprig" /></span>,
          node: <Art name="bloom" />,
          amp: <Art name="bloom" />,
          portrait: <Art name="bloom" className={s.portraitArt} />,
          countDecor: <Art name="frieze" className={s.countFrieze} />,
          closingDecor: <Art name="frieze" className={s.closingFrieze} />,
          closingEmblem: <Art name="bloom" className={s.closingBloom} />,
          sentArt: <Art name="bloom" />,
        }}
      />
    </ThemeShell>
  );
}
