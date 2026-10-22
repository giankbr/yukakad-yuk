"use client";
// Theme "Tegel Kunci" — teras rumah lama Nusantara (desain orisinal): tegel kunci bermotif bunga bintang delapan dan
// lingkar bergerigi dalam toska, bata, dan kunyit yang pudar dimakan langkah (aus, gompal, nat kotor), dinding kapur krem,
// jendela krepyak toska yang catnya mengelupas dan membuka pelan, serta kursi rotan di teras. Tanpa makhluk bernyawa,
// tanpa kaligrafi yang dilukis (basmalah diketik).
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Young Serif", "Petrona:ital,wght@0,400;0,600;1,400", "Sorts Mill Goudy:ital@0;1", "Amiri:wght@400"];
// Painted by /tmp/pen/art/themes/tegel-kunci.py (tools/art/themes in the repo).
const Art = makeArt("tegel-kunci", { ubin: [220, 220], lis: [360, 59], jendela: [170, 464], kursi: [320, 356] } as const);
const BISMILLAH = "بِسْمِ اللّٰهِ الرَّحْمٰنِ الرَّحِيْمِ";

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    arabic: BISMILLAH,
    kicker: "Assalamu'alaikum Warahmatullahi Wabarakatuh",
    title: "Mampirlah ke Teras Kami",
    intro: "Dengan memohon rahmat dan rida Allah SWT, kami bermaksud menyelenggarakan walimah pernikahan putra-putri kami. Merupakan kehormatan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"],
  couple: ["dua tegel, satu lantai", "Kedua Mempelai"],
  count: ["menghitung hari", "Menuju Hari Akad"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["waktu & tempat", "Rangkaian Acara"],
  story: ["dari teras yang sama", "Kisah Kami"],
  gallery: ["album lama", "Momen Bahagia"],
  wishes: ["doa & kehadiran", "Ucapan & Konfirmasi"],
  gifts: ["tanda kasih", "Amplop Digital"],
  closing: {
    thanks: "Matur Nuwun",
    text: "Atas kehadiran dan doa restu Bapak/Ibu/Saudara/i, kami sekeluarga mengucapkan terima kasih. Jazakumullah khairan, semoga Allah membalas setiap kebaikan.",
    salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh",
  },
  sent: "Jazakumullah khairan, doa dan ucapan Anda sudah terkirim.",
};

const WISHES = [
  { id: "w1", name: "Eyang Putri Hadiwiryo", attendance: "yes" as Attendance, message: "Barakallahu lakuma. Teras ini sudah menunggu kalian sejak kecil. Rukun selalu, saling ngemong, dan jangan lupa salat berjamaah." },
  { id: "w2", name: "Komunitas Rumah Lawas Kotagede", attendance: "yes" as Attendance, message: "Selamat Laras dan Ihsan! Semoga rumah tangganya kokoh seperti tegel kunci: makin tua makin indah." },
  { id: "w3", name: "Keluarga Pakde Harno", attendance: "maybe" as Attendance, message: "Insyaallah kami usahakan pulang dari Surabaya. Doa terbaik untuk kalian berdua." },
];

export default function TegelKunciTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Walimatul 'Ursy";
  const photo = data.gallery[0] ?? data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#ede2cc"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <p className={s.arabicCover} lang="ar" dir="rtl">{BISMILLAH}</p>
          <p className={s.kicker}>Assalamu&apos;alaikum Wr. Wb.</p>
          <p className={s.coverLabel}>Undangan {label}</p>
          <h1 className={s.coverNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.window}>
            <span className={`${s.shutter} ${s.shutterL}`}><Art name="jendela" eager /></span>
            <div className={s.kusen}>
              <div>{photo ? <Photo src={photo} alt="" /> : null}</div>
            </div>
            <span className={`${s.shutter} ${s.shutterR}`}><Art name="jendela" eager /></span>
          </div>
          <span className={s.sill} aria-hidden />
          <div className={s.terrace}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#fbf6ec" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#f2d9a0"
        dark="#2f6664"
        copy={COPY}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            <p className={s.heroKicker}>{label}</p>
            <h1 className={s.heroNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {photo && (
              <div className={s.panel}>
                <div className={s.heroPhoto}><Photo src={photo} alt="" /></div>
                <Art name="ubin" className={s.heroTile} />
              </div>
            )}
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="lis" className={s.divider} />,
          node: <Art name="ubin" />,
          amp: <Art name="ubin" />,
          portrait: <Art name="ubin" className={s.pTile} />,
          closingDecor: <div className={s.closingDecor} aria-hidden><Art name="jendela" /><Art name="jendela" /></div>,
          closingEmblem: <Art name="kursi" className={s.closingKursi} />,
          sentArt: <Art name="ubin" />,
        }}
      />
    </ThemeShell>
  );
}
