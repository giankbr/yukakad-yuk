"use client";
// Theme "Pandai Sikek" — pernikahan Islami Minang: songket Pandai Sikek bertabur benang emas rapat sebagai latar sampul,
// panel hitam berukir kaluak paku berlapis emas di atas merah, Ngarai Sianok cat air di atas foto pembuka, dan bingkai
// potret tiga warna marawa (hitam, merah, emas).
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Yeseva One", "Gentium Book Plus:ital,wght@0,400;0,700;1,400", "Parisienne", "Amiri:wght@400;700"];
// Painted by /tmp/pen/art/themes/minang-pandai-sikek.py (tools/art/themes in the repo).
const Art = makeArt("minang-pandai-sikek", { kaluak: [150, 149], ngarai: [720, 480] } as const);

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    arabic: "بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ",
    kicker: "Assalamu'alaikum Wr. Wb.",
    title: "Dengan Rahmat Allah",
    intro: "Dengan memohon rahmat dan rida Allah Subhanahu wa Ta'ala, serta restu ninik mamak dan alim ulama, kami bermaksud menyelenggarakan pernikahan putra-putri kami. Merupakan kehormatan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
  },
  roles: ["Anak Daro", "Marapulai"],
  couple: ["Kedua Mempelai", "Anak Daro & Marapulai"],
  count: ["Menghitung Hari", "Menuju Hari Baralek"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Waktu & Tempat", "Rangkaian Acara"],
  story: ["Kisah Kami", "Helai demi Helai"],
  gallery: ["Galeri", "Momen Bahagia"],
  wishes: ["Doa & Kehadiran", "Ucapan & Konfirmasi"],
  gifts: ["Tanda Kasih", "Amplop Digital"],
  closing: { thanks: "Terima Kasih", text: "Atas kehadiran dan doa restu Bapak/Ibu/Saudara/i, kami sekeluarga mengucapkan terima kasih. Semoga Allah membalas setiap kebaikan dengan berlipat ganda.", salam: "Wassalamu'alaikum Wr. Wb." },
  sent: "Terima kasih, doa dan ucapan Anda sudah terkirim.",
  wishPlaceholder: "Tuliskan doa terbaik untuk anak daro dan marapulai…",
};

const WISHES = [
  { id: "w1", name: "Keluarga H. Asril Datuak Bandaro", attendance: "yes" as Attendance, message: "Barakallahu lakuma wa baraka 'alaikuma. Semoga Rahmi dan Fadhlan menjadi keluarga yang sakinah, mawaddah, warahmah." },
  { id: "w2", name: "Kawan-kawan DKV ISI Padang Panjang", attendance: "yes" as Attendance, message: "Selamat Rahmi! Kami datang ke baralek, sudah tidak sabar makan bajamba dan dengar talempong." },
  { id: "w3", name: "Uda Rizal & Keluarga, Pekanbaru", attendance: "maybe" as Attendance, message: "Insyaallah kami pulang kampung. Doa terbaik dari rantau untuk kalian berdua." },
];

export default function MinangPandaiSikekTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const hero = data.gallery[0] ?? data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#1c1412"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.panel}>
            <div className={s.frieze} aria-hidden />
            <Art name="kaluak" eager className={s.medal} />
            <p className={s.bismillah} lang="ar" dir="rtl">بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ</p>
            <p className={s.salam}>Assalamu&apos;alaikum Wr. Wb.</p>
            <p className={s.kicker}>Undangan {label}</p>
            <h1 className={s.coverNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
            <div className={`${s.frieze} ${s.friezeLow}`} aria-hidden />
            <div className={s.guestWrap}>
              <div className={s.guest}>
                <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
                <strong>{guestLabel(data)}</strong>
                {table && <span className={s.table}>{table}</span>}
              </div>
              <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#1c1412" />Buka Undangan</button>
            </div>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#f1d488"
        dark="#1c1412"
        copy={COPY}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            <div className={s.heroScene} aria-hidden><Art name="ngarai" /></div>
            {hero && <div className={s.heroPhoto}><Photo src={hero} alt="" /></div>}
            <p className={s.heroKicker}>Walimatul &apos;Ursy</p>
            <h1 className={s.heroNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <span className={s.divider} aria-hidden><i /><Art name="kaluak" /><i /></span>,
          node: <Art name="kaluak" />,
          amp: <Art name="kaluak" />,
          closingDecor: <div className={s.closingFrieze} aria-hidden />,
          closingEmblem: <Art name="kaluak" className={s.closingEmblem} />,
          sentArt: <Art name="kaluak" />,
        }}
      />
    </ThemeShell>
  );
}
