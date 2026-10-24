"use client";
// Theme "Angklung Saung" — saung Sunda terbuka dalam cat air dan guas: teritis atap kirai dengan balok bambu berikat
// rotan tempat lima angklung tergantung dan berayun pelan, kartu tamu di tengah nyiru anyaman bambu, rumpun awi
// berkabut di dasar sampul; hitung mundur di tabung angklung yang makin pendek seperti tangga nada, kartu acara berpita
// bilik, garis waktu berupa tiang bambu beruas, dan penutup di tepi kebun bambu.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Kurale", "Literata:ital,wght@0,400;0,600;1,400", "Karla:wght@500;700;800", "Amiri"];
// Painted by /tmp/pen/art/themes/angklung-saung.py
const Art = makeArt("angklung-saung", { saung: [860, 300], angklung: [240, 431], rumpun: [680, 505], daun: [399, 61] } as const);

const WISHES = [
  { id: "w1", name: "Ceu Euis & Kang Dedi", attendance: "yes" as Attendance, message: "Wilujeng nempuh hirup anyar, Nisa sareng Fajar. Mugia janten kulawarga sakinah, mawaddah, warahmah, sauyunan dugi ka pupus." },
  { id: "w2", name: "Barudak Angklung Kampus", attendance: "yes" as Attendance, message: "Akhirnya do dan sol satu nada! Kami siap mengiringi di resepsi, sampai jumpa di Dipati Ukur." },
  { id: "w3", name: "Keluarga H. Nanang, Garut", attendance: "maybe" as Attendance, message: "Hapunten upami teu tiasa sumping. Doa terbaik kami untuk kalian berdua, semoga acaranya lancar dan berkah." },
];

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    arabic: "السَّلَامُ عَلَيْكُمْ وَرَحْمَةُ اللهِ وَبَرَكَاتُهُ",
    kicker: "Sampurasun",
    title: "Neda Pangdu'a",
    sub: "Kami mohon doa restu",
    intro: "Dengan memohon rahmat dan ridho Allah SWT, kami bermaksud menyelenggarakan pernikahan putra-putri kami. Merupakan kehormatan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"],
  couple: ["Dua Nada, Satu Lagu", "Kedua Mempelai"],
  count: ["Ngitung Poé", "Menuju Hari Bahagia"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Waktu & Tempat", "Rangkaian Acara"],
  story: ["Lalakon Urang", "Kisah Kami"],
  gallery: ["Galeri", "Momen Bahagia"],
  wishes: ["Du'a & Kahadiran", "Ucapan & Konfirmasi"],
  gifts: ["Tanda Asih", "Amplop Digital"],
  closing: {
    thanks: "Hatur Nuhun",
    text: "Atas kehadiran dan doa restu Bapak/Ibu/Saudara/i, kami sekeluarga mengucapkan terima kasih. Semoga Allah membalas setiap kebaikan.",
    salam: "Wassalamu'alaikum Wr. Wb.",
  },
  sent: "Hatur nuhun, doa dan ucapan Anda sudah terkirim.",
  closedNote: "Hatur nuhun atas doa dan perhatiannya. Ucapan masih bisa dikirim lewat form ini.",
};

export default function AngklungSaungTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const heroPhoto = data.gallery[0] ?? data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#2f4a2b"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.eave} aria-hidden><Art name="saung" eager /></div>
          <div className={s.chimes} aria-hidden>
            {[0, 1, 2, 3, 4].map(i => <Art key={i} name="angklung" eager className={s.chime} />)}
          </div>
          <div className={s.coverText}>
            <p className={s.sampurasun}>Sampurasun</p>
            <p className={s.kicker}>Undangan {label}</p>
            <h1 className={s.coverNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
          </div>
          <div className={s.nyiru}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
          </div>
          <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={17} color="#f7efd8" />Buka Undangan</button>
          <Art name="rumpun" eager className={s.grove} />
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#f7efd8"
        dark="#34552e"
        copy={COPY}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            <Art name="saung" className={s.heroEave} />
            {heroPhoto && <div className={s.heroWindow}><div className={s.heroPhoto}><Photo src={heroPhoto} alt="" /></div></div>}
            <p className={s.heroKicker}>{label}</p>
            <h1 className={s.heroNames}>{data.couple.bride} <em>&amp;</em> {data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="daun" className={s.divider} />,
          node: <Art name="angklung" />,
          amp: <Art name="daun" />,
          portrait: <Art name="angklung" className={s.portraitArt} />,
          closingDecor: <Art name="rumpun" className={s.closingGrove} />,
          closingEmblem: <Art name="angklung" className={s.closingEmblem} />,
          sentArt: <Art name="angklung" />,
        }}
      />
    </ThemeShell>
  );
}
