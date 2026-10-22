"use client";
// Theme "Bromo Tengger" — pernikahan adat Hindu Tengger dengan lukisan cat air kaldera Bromo saat fajar: kerucut Batok
// berlekuk, kawah berasap, Semeru di kejauhan, lautan pasir berkabut, dan bukit hijau berlipat. Kartu tamu dibungkus
// kain sarung Tengger bermotif kotak, foto pembuka dipotong mengikuti siluet kaldera, hitung mundur berupa kerucut
// gunung kecil, dan edelweis (tana layu) sebagai penanda.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Castoro:ital@0;1", "Manrope:wght@400;500;600;700"];
// Painted by /tmp/pen/art/themes/bromo-tengger.py (tools/art/themes in the repo).
const Art = makeArt("bromo-tengger", { mist: [700, 154], divider: [340, 62], edelweiss: [120, 127] } as const);

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  attend: { maybe: "Mungkin" },
  opening: {
    kicker: "Salam Sejahtera",
    title: "Om Swastyastu",
    intro: "Atas asung kertha wara nugraha Ida Sang Hyang Widhi Wasa, kami bermaksud melangsungkan upacara pernikahan putra-putri kami di Desa Ngadisari. Merupakan kehormatan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
  },
  roles: ["Mempelai Putri", "Mempelai Putra"],
  couple: ["Dua Hati di Kaki Bromo", "Kedua Mempelai"],
  count: ["Menanti Fajar", "Hari Bahagia"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Waktu & Tempat", "Rangkaian Upacara"],
  story: ["Perjalanan Kami", "Dari Kasada ke Walagara"],
  gallery: ["Galeri", "Kenangan di Lautan Pasir"],
  wishes: ["Doa & Kehadiran", "Ucapan & Konfirmasi"],
  gifts: ["Tanda Kasih", "Amplop Digital"],
  closing: { thanks: "Matur Suksma", text: "Kehadiran dan doa restu Bapak/Ibu/Saudara/i merupakan kebahagiaan yang tak ternilai bagi kami sekeluarga.", salam: "Om Shanti Shanti Shanti Om" },
  sent: "Matur suksma, doa dan ucapan Anda sudah terkirim.",
  wishPlaceholder: "Tuliskan doa restu untuk kedua mempelai…",
  closedNote: "Matur suksma atas doa dan perhatiannya. Ucapan masih bisa dikirim lewat form ini.",
};

const WISHES = [
  { id: "w1", name: "Bapak Sugiyanto & Keluarga", attendance: "yes" as Attendance, message: "Rahajeng nganten anyar. Semoga rumah tangga kalian kokoh seperti Batok dan hangat seperti tungku di dapur Tengger." },
  { id: "w2", name: "Mas Darmaji, Paguyuban Jip Cemorolawang", attendance: "yes" as Attendance, message: "Selamat, Wahyu! Hari itu rombongan jip siap mengantar tamu dari Cemorolawang. Bahagia selalu." },
  { id: "w3", name: "Bu Guru Endang, SDN Ngadisari", attendance: "maybe" as Attendance, message: "Ikut bahagia, Bu Rahayu. Semoga bisa hadir, doa terbaik dari kami semua di sekolah." },
];

export default function BromoTenggerTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const table = tableLabel(data.guestTable);
  const photo = data.gallery[0] ?? data.couple.bridePhoto;
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#34356a"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Art name="mist" className={s.mistA} eager />
          <Art name="mist" className={s.mistB} eager />
          <p className={s.salam}>Om Swastyastu</p>
          <p className={s.kicker}>Undangan {label}</p>
          <h1 className={s.coverNames}><span>{data.couple.bride}</span><em>dan</em><span>{data.couple.groom}</span></h1>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.wrap}>
            <span className={s.shawl} aria-hidden />
            <div className={s.wrapBody}>
              <div className={s.guest}>
                <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
                <strong>{guestLabel(data)}</strong>
                {table && <span className={s.table}>{table}</span>}
              </div>
              <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#ffffff" />Buka Undangan</button>
            </div>
            <span className={s.fringe} aria-hidden />
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#f7e6c2"
        dark="#34356a"
        copy={COPY}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            <p className={s.heroKicker}>The Wedding of</p>
            <h1 className={s.heroNames}>{data.couple.bride} <em>&amp;</em> {data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            <div className={s.heroPhotoWrap}>
              <div className={s.heroPhoto}>{photo ? <Photo src={photo} alt={`${data.couple.bride} & ${data.couple.groom}`} /> : <span aria-hidden>{data.couple.bride.slice(0, 1)}</span>}</div>
              <span className={s.heroRidge} aria-hidden />
            </div>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="divider" className={s.divider} />,
          node: <Art name="edelweiss" />,
          amp: <Art name="edelweiss" />,
          portrait: <Art name="edelweiss" className={s.portraitArt} />,
          closingEmblem: <Art name="edelweiss" className={s.closingEmblem} />,
          sentArt: <Art name="edelweiss" />,
        }}
      />
    </ThemeShell>
  );
}
