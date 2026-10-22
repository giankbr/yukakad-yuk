"use client";
// Theme "Kintsugi Emas" — piring keramik krem beretak halus yang disambung garis emas, dilukis sendiri: seberkas cahaya
// pelan berjalan di sepanjang sambungan emasnya. Mangkuk arang dengan lelehan glasir, sapuan tinta sumi, foto hitam-putih
// berpasse-partout, tata letak rata kiri dengan banyak ruang kosong. Undangan netral (tanpa salam keagamaan).
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Shippori Mincho:wght@400;500;600", "Zen Kaku Gothic New:wght@400;500;700"];
// Painted by /tmp/pen/art/themes/kintsugi-emas.py (tools/art/themes in the repo).
const Art = makeArt("kintsugi-emas", {
  piring: [380, 380], emas: [380, 380], mangkuk: [360, 236], tinta: [560, 199], retak: [320, 28], pecahan: [64, 67],
} as const);

function Plate({ className, eager }: { className?: string; eager?: boolean }) {
  return (
    <div className={className ? `${s.plate} ${className}` : s.plate} aria-hidden>
      <Art name="piring" eager={eager} />
      <Art name="emas" eager={eager} />
      <span className={s.shine} />
    </div>
  );
}

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    kicker: "Dengan penuh sukacita",
    title: "Yang retak tidak harus dibuang. Ia bisa disatukan, dan menjadi lebih indah.",
    intro: "Dengan penuh rasa syukur, kami mengundang Bapak/Ibu/Saudara/i untuk hadir dan menjadi saksi di hari pernikahan kami. Kehadiran dan doa baik Anda adalah garis emas yang menyempurnakan hari itu.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"],
  couple: ["Dua Kepingan", "Kedua Mempelai"],
  count: ["Menunggu Hari", "Menuju Hari Bahagia"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Waktu & Tempat", "Rangkaian Acara"],
  story: ["Retak & Pulih", "Cerita Kami"],
  gallery: ["Galeri", "Potret Kami"],
  wishes: ["Kehadiran & Ucapan", "Ucapan & Konfirmasi"],
  gifts: ["Tanda Kasih", "Amplop Digital"],
  closing: {
    thanks: "Terima Kasih",
    text: "Terima kasih telah menjadi bagian dari perjalanan kami. Kehadiran dan doa baik Anda akan selalu kami simpan, seperti garis emas yang tak pernah pudar.",
  },
  sent: "Terima kasih, ucapan Anda sudah kami terima.",
  attend: { maybe: "Mungkin" },
  wishPlaceholder: "Tuliskan ucapan dan doa baik untuk kami…",
};

const WISHES = [
  { id: "w1", name: "Teman Kelas Keramik Kasongan", attendance: "yes" as Attendance, message: "Dari mangkuk yang miring sampai pelaminan. Selamat, Kirana dan Dimas! Semoga selalu sabar saling menyatukan." },
  { id: "w2", name: "Keluarga Om Bram, Semarang", attendance: "yes" as Attendance, message: "Selamat menempuh hidup baru. Semoga rumah tangga kalian hangat, tenang, dan penuh tawa." },
  { id: "w3", name: "Laras & Yudha", attendance: "maybe" as Attendance, message: "Semoga bisa datang ke resepsi malamnya. Bahagia selalu untuk kalian berdua." },
];

export default function KintsugiEmasTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const { bride, groom } = data.couple;
  const photo = data.gallery[0] ?? data.couple.bridePhoto;

  return (
    <ThemeShell
      fonts={FONTS}
      background="#e6e0d3"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Plate eager />
          <div className={s.coverTop}>
            <p className={s.kicker}>Undangan {label}</p>
            <h1 className={s.coverNames}><span>{bride}</span>{groom && <><em>&amp;</em><span>{groom}</span></>}</h1>
            <p className={s.coverDate}><Art name="retak" eager />{formatDate(data.date)}</p>
          </div>
          <div className={s.coverFoot}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={15} color="#efe9dd" />Buka Undangan</button>
          </div>
          <Art name="tinta" eager className={s.coverMist} />
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#efe9dd"
        dark="#2b2926"
        copy={COPY}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            <div className={s.heroFrame}>
              <div className={s.heroPhoto}><Photo src={photo} alt={`${bride} & ${groom}`} /></div>
              <Art name="retak" className={s.heroSeam} />
            </div>
            <p className={s.heroKicker}>{label}</p>
            <h1 className={s.heroNames}>{bride}{groom && <> <em>&amp;</em> {groom}</>}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="retak" className={s.divider} />,
          node: <Art name="pecahan" />,
          amp: <Art name="retak" />,
          portrait: <Art name="retak" className={s.pSeam} />,
          countDecor: <Art name="tinta" className={s.countMist} />,
          closingEmblem: <Plate className={s.closingPlate} />,
          sentArt: <Art name="mangkuk" />,
        }}
      />
    </ThemeShell>
  );
}
