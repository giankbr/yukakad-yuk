"use client";
// Theme "Menara Kudus" — terinspirasi arsitektur menara bata merah Kudus dan gapura paduraksa (desain orisinal, hanya
// arsitektur): bata telanjang, piring keramik biru-putih yang ditanam di dinding, tegel hijau berglasir, atap tajug
// bersusun. Tanpa makhluk bernyawa dan tanpa kaligrafi yang dilukis (basmalah diketik).
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Rozha One", "Spectral:ital,wght@0,400;0,600;1,400", "Reem Kufi:wght@400;500", "Amiri:wght@400"];
// Painted by /tmp/pen/art/themes/menara-kudus.py (tools/art/themes in the repo).
const Art = makeArt("menara-kudus", { menara: [360, 931], gate: [380, 410], plate: [100, 100], strip: [320, 30] } as const);
const BISMILLAH = "بِسْمِ اللّٰهِ الرَّحْمٰنِ الرَّحِيْمِ";

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    arabic: BISMILLAH,
    kicker: "Assalamu'alaikum Warahmatullahi Wabarakatuh",
    title: "Dari Kota Menara",
    intro: "Dengan memohon rahmat dan rida Allah SWT, kami bermaksud menyelenggarakan walimatul 'ursy putra-putri kami. Merupakan kehormatan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"],
  couple: ["Bata demi Bata", "Kedua Mempelai"],
  count: ["Hitung Mundur", "Menuju Hari Akad"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Waktu & Tempat", "Rangkaian Acara"],
  story: ["Perjalanan", "Kisah Kami"],
  gallery: ["Kenangan", "Galeri Foto"],
  wishes: ["Doa & Kehadiran", "Ucapan & Konfirmasi"],
  gifts: ["Tanda Kasih", "Amplop Digital"],
  closing: {
    thanks: "Matur Suwun",
    text: "Atas kehadiran dan doa restu Bapak/Ibu/Saudara/i, kami sekeluarga mengucapkan terima kasih. Jazakumullah khairan katsiran.",
    salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh",
  },
  sent: "Jazakumullah khairan, doa dan ucapan Anda sudah terkirim.",
};

const WISHES = [
  { id: "w1", name: "KH. Ma'ruf Asnawi", attendance: "yes" as Attendance, message: "Barakallahu lakuma wa baraka 'alaikuma wa jama'a bainakuma fi khair. Semoga menjadi keluarga yang sakinah dan membawa manfaat bagi umat." },
  { id: "w2", name: "Asatidz Madrasah Qudsiyyah", attendance: "yes" as Attendance, message: "Selamat Ustazah Zahra dan Ustaz Hanif. Semoga ilmunya makin berkah setelah berdua." },
  { id: "w3", name: "Keluarga Mbak Fina, Semarang", attendance: "maybe" as Attendance, message: "Insyaallah kami usahakan hadir ke Kudus. Doa terbaik dari Semarang." },
];

export default function MenaraKudusTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Walimatul 'Ursy";
  const hero = data.gallery[0] ?? data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#f4ece0"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <span className={s.sun} aria-hidden />
          <Art name="menara" eager className={s.coverMenara} />
          <p className={s.arabicCover} lang="ar" dir="rtl">{BISMILLAH}</p>
          <p className={s.kicker}>Assalamu&apos;alaikum Wr. Wb.</p>
          <p className={s.coverLabel}>Undangan {label}</p>
          <h1 className={s.coverNames}><span>{data.couple.bride}</span><em>&amp;</em><span>{data.couple.groom}</span></h1>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.coverFoot}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#fffcf6" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#cfe8d6"
        dark="#1c5240"
        copy={COPY}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            <p className={s.heroKicker}>{label}</p>
            <h1 className={s.heroNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            <div className={s.gateWrap}>
              {hero && <div className={s.heroPhoto}><Photo src={hero} alt="" /></div>}
              <Art name="gate" className={s.gateArt} />
            </div>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="strip" className={s.divider} />,
          node: <Art name="plate" />,
          amp: <Art name="plate" />,
          portrait: <span className={s.pSill} aria-hidden />,
          closingEmblem: <Art name="menara" className={s.closingMenara} />,
          sentArt: <Art name="plate" />,
        }}
      />
    </ThemeShell>
  );
}
