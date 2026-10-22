"use client";
// Theme "Mandailing Gordang" — pernikahan Islami Mandailing: bagas godang beratap ijuk dengan bidang singap bindu
// merah-putih-hitam dan sopo di sampingnya, di antara bukit hijau dan sawah berundak Tapanuli Selatan (cat air + gouache),
// dilihat lewat jendela berbentuk rumah; sembilan gordang sambilan berdiri di dasar sampul dan penutup, hitung mundur
// yang berdetak seperti gendang. Hijau hutan, merah, hitam, putih, dan emas.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Zilla Slab:wght@400;600;700", "Vollkorn:ital,wght@0,400;0,600;1,400", "Amiri:wght@400;700"];
// Painted by /tmp/pen/art/themes/mandailing-gordang.py (tools/art/themes in the repo).
const Art = makeArt("mandailing-gordang", { bagas: [760, 877], gordang: [640, 233], gendang: [70, 147], bindu: [780, 53] } as const);

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    arabic: "بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ",
    kicker: "Assalamu'alaikum Wr. Wb. · Horas!",
    title: "Dengan Rahmat Allah",
    intro: "Dengan memohon rahmat dan rida Allah Subhanahu wa Ta'ala, kami bermaksud menyelenggarakan akad nikah dan walimah putra-putri kami. Merupakan kehormatan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"],
  couple: ["Kedua Mempelai", "Sembilan Gordang, Satu Irama"],
  count: ["Menghitung Hari", "Menuju Hari Bahagia"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Waktu & Tempat", "Rangkaian Acara"],
  story: ["Kisah Kami", "Dari Tanah Sipirok"],
  gallery: ["Galeri", "Momen Bahagia"],
  wishes: ["Doa & Kehadiran", "Ucapan & Konfirmasi"],
  gifts: ["Tanda Kasih", "Amplop Digital"],
  closing: { thanks: "Terima Kasih", text: "Atas kehadiran dan doa restu Bapak/Ibu/Saudara/i, kami ucapkan terima kasih. Semoga Allah membalas setiap kebaikan.", salam: "Horas tondi madingin, pir tondi matogu.\nWassalamu'alaikum Wr. Wb." },
  sent: "Terima kasih, doa dan ucapan Anda sudah terkirim.",
  wishPlaceholder: "Tuliskan doa terbaik untuk kedua mempelai…",
};

const WISHES = [
  { id: "w1", name: "Keluarga H. Baginda Siregar", attendance: "yes" as Attendance, message: "Barakallahu lakuma wa baraka 'alaikuma wa jama'a bainakuma fi khair. Horas, Aisyah dan Rizki!" },
  { id: "w2", name: "Ikatan Mahasiswa Tapsel Medan", attendance: "yes" as Attendance, message: "Selamat menempuh hidup baru! Semoga menjadi keluarga sakinah, mawaddah, warahmah." },
  { id: "w3", name: "Uda Rahman & Keluarga, Panyabungan", attendance: "maybe" as Attendance, message: "Insyaallah kami datang dari Panyabungan. Doa terbaik untuk kalian berdua." },
];

export default function MandailingGordangTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const hero = data.gallery[0] ?? data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#173a26"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <p className={s.bismillah} lang="ar" dir="rtl">بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ</p>
          <p className={s.salam}>Assalamu&apos;alaikum Wr. Wb. · Horas!</p>
          <div className={s.window} aria-hidden><span className={s.windowIn}><Art name="bagas" eager /></span></div>
          <p className={s.kicker}>Undangan {label}</p>
          <h1 className={s.coverNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.guestWrap}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#fffdf4" />Buka Undangan</button>
          </div>
          <div className={s.drums} aria-hidden><Art name="gordang" eager /></div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#f0d48a"
        dark="#1f5a34"
        copy={COPY}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            <p className={s.heroKicker}>Walimatul &apos;Ursy</p>
            {hero && <div className={s.heroHouse}><div className={s.heroPhoto}><Photo src={hero} alt="" /></div></div>}
            <Art name="bindu" className={s.heroSill} />
            <h1 className={s.heroNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <span className={s.divider} aria-hidden><i /><Art name="gendang" /><i /></span>,
          node: <Art name="gendang" />,
          amp: <Art name="gendang" />,
          portrait: <Art name="gendang" className={s.pg} />,
          closingDecor: <Art name="gordang" className={s.closeDrums} />,
          closingEmblem: <Art name="gendang" className={s.closingEmblem} />,
          sentArt: <Art name="gendang" />,
        }}
      />
    </ThemeShell>
  );
}
