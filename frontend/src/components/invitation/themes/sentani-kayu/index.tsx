"use client";
// Theme "Sentani Kayu" — pernikahan Kristen di Danau Sentani dengan gaya lukisan kulit kayu kombouw: garis hitam tebal,
// isian putih kapur dan merah oker di atas kain kulit kayu cokelat, motif ikan dan spiral orisinal. Sampul berupa lukisan
// kulit kayu yang digantung, kartu bergaris tebal dengan bayangan oker, dan pemandangan Danau Sentani berpulau di bawah
// Pegunungan Cycloop di pembuka dan penutup.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Zilla Slab:ital,wght@0,500;0,600;0,700;1,500", "Karla:wght@400;500;600;700"];
// Painted by /tmp/pen/art/themes/sentani-kayu.py (tools/art/themes in the repo).
const Art = makeArt("sentani-kayu", { panel: [560, 743], fish: [150, 78], spiral: [96, 97], divider: [360, 45] } as const);

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  attend: { maybe: "Mungkin" },
  opening: {
    kicker: "Salam Sejahtera",
    title: "Syalom",
    intro: "Dengan sukacita dan syukur atas kasih karunia Tuhan, kami mengundang Bapak/Ibu/Saudara/i, ade-kaka sekalian, untuk hadir dan turut memberkati pernikahan kami di tepi Danau Sentani.",
  },
  roles: ["Mempelai Perempuan", "Mempelai Laki-laki"],
  couple: ["Ikan & Air", "Kedua Mempelai"],
  count: ["Menuju Hari", "Pemberkatan Nikah"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Waktu & Tempat", "Ibadah & Pesta"],
  story: ["Perjalanan Kami", "Kisah dari Danau"],
  gallery: ["Galeri", "Cerita dalam Foto"],
  wishes: ["Doa & Kehadiran", "Ucapan & Konfirmasi"],
  gifts: ["Tanda Kasih", "Amplop Digital"],
  closing: { thanks: "Terima Kasih", text: "Kehadiran dan doa Bapak/Ibu/Saudara/i adalah berkat yang tak ternilai bagi kami dan keluarga besar di Sentani.", salam: "Tuhan Yesus memberkati" },
  sent: "Terima kasih, doa dan ucapan Anda sudah terkirim.",
  wishPlaceholder: "Tuliskan doa dan berkat untuk kedua mempelai…",
};

const WISHES = [
  { id: "w1", name: "Bapak Daniel Wally & Keluarga", attendance: "yes" as Attendance, message: "Syalom! Tuhan memberkati rumah tangga kalian, kokoh seperti tiang rumah di atas danau dan selalu penuh berkat." },
  { id: "w2", name: "Mama-mama Sanggar Asei", attendance: "yes" as Attendance, message: "Ade Retha, Ade Yohan, selamat e! Kami siapkan papeda dan kain kulit kayu untuk hari bahagia kalian." },
  { id: "w3", name: "Kaka Frans Kabey", attendance: "maybe" as Attendance, message: "Masih tugas di Wamena minggu itu, semoga bisa turun. Doa terbaik dari kami sekeluarga." },
];

export default function SentaniKayuTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const table = tableLabel(data.guestTable);
  const photo = data.gallery[0] ?? data.couple.bridePhoto;
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#3b2718"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Art name="panel" className={s.panel} eager />
          <p className={s.salam}>Syalom</p>
          <p className={s.kicker}>Undangan {label}</p>
          <h1 className={s.coverNames}><span>{data.couple.bride}</span><em>&amp;</em><span>{data.couple.groom}</span></h1>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.card}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#ffffff" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#eee3cf"
        dark="#1d1612"
        copy={COPY}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            <div className={s.heroLake} aria-hidden />
            <div className={s.heroText}>
              <p className={s.heroKicker}>The Wedding of</p>
              <h1 className={s.heroNames}>{data.couple.bride} <em>&amp;</em> {data.couple.groom}</h1>
            </div>
            <div className={s.heroPhotoWrap}>
              <div className={s.heroPhoto}>{photo ? <Photo src={photo} alt={`${data.couple.bride} & ${data.couple.groom}`} /> : <span aria-hidden>{data.couple.bride.slice(0, 1)}</span>}</div>
              <Art name="fish" className={s.heroFish} />
            </div>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="divider" className={s.divider} />,
          node: <Art name="spiral" />,
          amp: <Art name="fish" />,
          portrait: <Art name="spiral" className={s.portraitArt} />,
          closingDecor: <div className={s.closingLake} aria-hidden />,
          closingEmblem: <Art name="fish" className={s.closingEmblem} />,
          sentArt: <Art name="fish" />,
        }}
      />
    </ThemeShell>
  );
}
