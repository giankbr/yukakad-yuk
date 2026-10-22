"use client";
// Theme "Doyo Benuaq" — pernikahan di tanah Benuaq, Kutai Barat: tenun ulap doyo dari serat daun doyo (ikat lungsin
// hitam-merah di atas serat alam, benang kasar dipintal tangan) menjadi tepi kain di sisi kiri sampul dan kartu,
// lamin panjang bertiang ulin di tepi Mahakam, daun hutan yang bergoyang, tata letak rata kiri yang asimetris.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Kurale", "Gentium Book Plus:ital,wght@0,400;0,700;1,400"];
// Painted by /tmp/pen/art/themes/doyo-benuaq.py (tools/art/themes in the repo).
const Art = makeArt("doyo-benuaq", { lamin: [820, 498], daun: [360, 180], kait: [200, 207] } as const);

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    kicker: "Salam Sejahtera",
    title: "Dengan Penuh Syukur",
    intro: "Atas kasih Tuhan Yang Maha Esa, kami bermaksud menyelenggarakan pernikahan putra-putri kami. Merupakan kebahagiaan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"],
  couple: ["Kedua Mempelai", "Dua Helai, Satu Tenunan"],
  count: ["Menghitung Hari", "Menuju Hari Bahagia"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Waktu & Tempat", "Rangkaian Acara"],
  story: ["Kisah Kami", "Dipintal Perlahan"],
  gallery: ["Galeri", "Dari Hulu Mahakam"],
  wishes: ["Doa & Kehadiran", "Ucapan & Konfirmasi"],
  gifts: ["Tanda Kasih", "Amplop Digital"],
  closing: { thanks: "Terima Kasih", text: "Kehadiran dan doa restu Bapak/Ibu/Saudara/i adalah anugerah bagi kami sekeluarga. Tuhan memberkati.", salam: "Salam sejahtera bagi kita semua" },
  sent: "Terima kasih, doa dan ucapan Anda sudah terkirim.",
  attend: { maybe: "Mungkin" },
};

const WISHES = [
  { id: "w1", name: "Keluarga Bapak Petrus Lahang", attendance: "yes" as Attendance, message: "Selamat menempuh hidup baru, Lusi dan Dodi. Tuhan memberkati rumah tangga kalian, rukun dan kuat seperti tenun doyo." },
  { id: "w2", name: "Teman-teman Kehutanan Unmul", attendance: "yes" as Attendance, message: "Akhirnya! Sampai ketemu di lamin, kami siap ikut menari gantar." },
  { id: "w3", name: "Agnes Tining", attendance: "maybe" as Attendance, message: "Mungkin baru bisa datang sore. Doa terbaik dari Samarinda untuk kalian berdua." },
];

export default function DoyoBenuaqTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const hero = data.gallery[0] ?? data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#2a1d15"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Art name="daun" eager className={s.daun} />
          <p className={s.kicker}>Undangan {label}</p>
          <div className={s.pinned}>
            <Art name="kait" eager className={s.pinKait} />
            <div className={s.pinPhoto}>{hero ? <Photo src={hero} alt="" /> : null}</div>
          </div>
          <h1 className={s.coverNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.guestWrap}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#efe4cb" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#efe4cb"
        dark="#2a1d15"
        copy={COPY}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            <Art name="lamin" className={s.heroLamin} />
            <div className={s.heroText}>
              <p className={s.heroKicker}>The Wedding of</p>
              <h1 className={s.heroNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
              <p className={s.heroDate}>{formatDate(data.date)}</p>
              {note && <p className={s.heroNote}>{note}</p>}
            </div>
          </header>
        )}
        slots={{
          divider: <span className={s.divider} aria-hidden />,
          node: <Art name="kait" />,
          amp: <Art name="kait" />,
          portrait: <Art name="kait" />,
          closingDecor: <div className={s.closingLamin} aria-hidden><Art name="lamin" /></div>,
          closingEmblem: <Art name="kait" className={s.closingEmblem} />,
          sentArt: <Art name="kait" />,
        }}
      />
    </ThemeShell>
  );
}
