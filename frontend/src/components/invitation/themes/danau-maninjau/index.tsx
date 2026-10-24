"use client";
// Theme "Danau Maninjau" — Danau Maninjau dilihat dari tikungan Kelok 44, dilukis cat air di atas kertas (desain
// orisinal): dinding kawah hijau berkabut, danau biru ultramarin dengan keramba dan jukung, sawah dan rumah gadang
// bergonjong di tepi air, jalan berkelok di lereng depan. Sampul menaruh nama di langit pagi dan kartu tamu sebagai rambu
// petunjuk jalan hijau; hitung mundur di patok kelok putih bertopi merah, acara bernomor "Kelok", kisah sebagai jalan
// aspal bergaris, amplop berupa rambu, penutup rumah gadang di tepi danau. Basmalah diketik, tanpa kaligrafi lukis.
import { Icon, Lucide, Photo, ThemeShell, formatDate, guestLabel, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Vollkorn:ital,wght@0,500;0,600;0,700;1,500;1,600", "Mulish:wght@400;600;700;800", "Amiri:wght@400"];
// Painted by /tmp/pen/art/themes/danau-maninjau.py
const Art = makeArt("danau-maninjau", { house: [560, 333], padi: [160, 230], road: [420, 79], mist: [900, 81] } as const);
const BISMILLAH = "بِسْمِ اللّٰهِ الرَّحْمٰنِ الرَّحِيْمِ";
const ARROW = ["M5 12h14", "m13 6 6 6-6 6"];

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    arabic: BISMILLAH,
    kicker: "Assalamu'alaikum Warahmatullahi Wabarakatuh",
    title: "Dari Tepi Danau Maninjau",
    intro: "Dengan memohon rahmat dan rida Allah SWT, kami bermaksud menyelenggarakan akad nikah dan baralek putra-putri kami di kampung halaman. Merupakan kehormatan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
  },
  roles: ["Anak Daro", "Marapulai"],
  couple: ["Sehiliran Sejalan", "Kedua Mempelai"],
  count: ["Kelok demi kelok", "Menuju Hari Baralek"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Waktu & Tempat", "Rangkaian Acara"],
  story: ["Jalan yang kami tempuh", "Kisah Kami"],
  gallery: ["Kartu pos", "Galeri Kami"],
  wishes: ["Doa & Kehadiran", "Ucapan & Konfirmasi"],
  gifts: ["Tanda Kasih", "Amplop Digital"],
  closing: {
    thanks: "Tarimo Kasih",
    text: "Kehadiran dan doa restu Bapak/Ibu/Saudara/i adalah kebahagiaan bagi kami sekeluarga. Semoga Allah membalas setiap kebaikan dengan berlipat ganda.",
    salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh",
  },
  sent: "Jazakumullah khairan, doa dan ucapan Anda sudah sampai.",
};

const WISHES = [
  { id: "w1", name: "Mamak Datuak Sinaro", attendance: "yes" as Attendance, message: "Barakallahu lakuma. Samoga rumah tanggo kalian sakato, saiyo sakato, dan salalu dalam lindungan Allah." },
  { id: "w2", name: "Komunitas Gowes Kelok 44", attendance: "yes" as Attendance, message: "Dari kelok ke-27 sampai pelaminan! Kami turun bersepeda dari Ambun Pagi, insyaallah sampai sebelum makan bajamba." },
  { id: "w3", name: "Uni Fitri, Pekanbaru", attendance: "maybe" as Attendance, message: "Insyaallah kami usahakan pulang kampung. Doa terbaik untuk Salsa dan Reza, semoga sakinah mawaddah wa rahmah." },
];

export default function DanauManinjauTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Walimatul 'Ursy";
  const hero = data.gallery[0] ?? data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#173f6a"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <span className={s.scene} aria-hidden />
          <Art name="mist" eager className={s.coverMist} />
          <p className={s.arabicCover} lang="ar" dir="rtl">{BISMILLAH}</p>
          <p className={s.kicker}>Undangan {label}</p>
          <h1 className={s.names}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <span className={s.spacer} aria-hidden />
          <div className={s.sign}>
            <p className={s.signRow}><span>Danau Maninjau</span><Icon d={ARROW} size={18} stroke="#fff" strokeWidth={2.4} /></p>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={17} color="#0b4a30" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#fbf7ee"
        dark="#17334f"
        copy={COPY}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            <p className={s.heroKicker}>{label}</p>
            <h1 className={s.heroNames}>{data.couple.bride} <em>&amp;</em> {data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {hero && (
              <div className={s.postcard}>
                <div className={s.heroPhoto}><Photo src={hero} alt={`${data.couple.bride} dan ${data.couple.groom}`} /></div>
                <span className={s.postLine} aria-hidden>Salam dari tepi danau</span>
                <span className={s.stamp} aria-hidden>Maninjau<br />Agam</span>
              </div>
            )}
            <Art name="road" className={s.heroRoad} />
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="road" className={s.divider} />,
          node: <Art name="padi" />,
          amp: <Art name="padi" />,
          portrait: <Art name="padi" className={s.pSprig} />,
          countDecor: <Art name="mist" className={s.countMist} />,
          closingEmblem: <div className={s.closingScene} aria-hidden><Art name="house" /></div>,
          sentArt: <Art name="padi" />,
        }}
      />
    </ThemeShell>
  );
}
