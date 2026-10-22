"use client";
// Theme "Kerinci Danau" — alam Kerinci, Jambi, sebagai poster gouache (desain orisinal): Gunung Kerinci di atas kebun
// teh Kayu Aro, Danau Kerinci yang tenang, dan papan ukir rumah larik (keluk paku, bunga empat kelopak) berwarna oker
// dan merah di atas kayu tua. Tanpa makhluk bernyawa, basmalah diketik.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Young Serif", "Lora:ital,wght@0,400;0,600;1,400", "Josefin Sans:wght@400;600", "Amiri:wght@400"];
// Painted by /tmp/pen/art/themes/kerinci-danau.py (tools/art/themes in the repo).
const Art = makeArt("kerinci-danau", { sprig: [140, 197], divider: [320, 98] } as const);
const BISMILLAH = "بِسْمِ اللّٰهِ الرَّحْمٰنِ الرَّحِيْمِ";

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    arabic: BISMILLAH,
    kicker: "Assalamu'alaikum Warahmatullahi Wabarakatuh",
    title: "Dari Kaki Gunung Kerinci",
    intro: "Dengan memohon rahmat dan rida Allah SWT, kami bermaksud menyelenggarakan walimah pernikahan putra-putri kami. Merupakan kehormatan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"],
  couple: ["Seiring Sejalan", "Kedua Mempelai"],
  count: ["Hitung Mundur", "Menuju Hari Bahagia"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Waktu & Tempat", "Rangkaian Acara"],
  story: ["Jejak Langkah", "Kisah Kami"],
  gallery: ["Album", "Galeri Foto"],
  wishes: ["Doa & Kehadiran", "Ucapan & Konfirmasi"],
  gifts: ["Tanda Kasih", "Amplop Digital"],
  closing: {
    thanks: "Terima Kasih",
    text: "Kehadiran dan doa restu Bapak/Ibu/Saudara/i adalah kebahagiaan bagi kami sekeluarga. Semoga Allah membalas setiap kebaikan dengan berlipat ganda.",
    salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh",
  },
  sent: "Jazakumullah khairan, doa dan ucapan Anda sudah terkirim.",
};

const WISHES = [
  { id: "w1", name: "Ninik Mamak Dusun Pondok Tinggi", attendance: "yes" as Attendance, message: "Barakallahu lakuma. Semoga rumah tangga kalian kokoh seperti rumah larik, berdiri bersama dan saling menopang." },
  { id: "w2", name: "Tim Pendaki Kersik Tuo", attendance: "yes" as Attendance, message: "Dari Shelter 2 sampai pelaminan! Selamat Nurul dan Fadhil, kami siap hadir lengkap." },
  { id: "w3", name: "Keluarga Uda Rizal, Padang", attendance: "maybe" as Attendance, message: "Insyaallah kami usahakan datang ke Sungai Penuh. Doa terbaik selalu untuk kalian." },
];

export default function KerinciDanauTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Walimatul 'Ursy";
  const hero = data.gallery[0] ?? data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#6c7aa6"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <span className={s.plume} aria-hidden />
          <p className={s.arabicCover} lang="ar" dir="rtl">{BISMILLAH}</p>
          <p className={s.kicker}>Assalamu&apos;alaikum Wr. Wb.</p>
          <div className={s.board}>
            <span className={s.rope} aria-hidden />
            <span className={s.rope} aria-hidden />
            <p className={s.coverLabel}>Undangan {label}</p>
            <h1 className={s.coverNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
          </div>
          <div className={s.foot}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#faf4e6" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#f0cf86"
        dark="#3f6a32"
        copy={COPY}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            <p className={s.heroKicker}>{label}</p>
            <h1 className={s.heroNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {hero && (
              <div className={s.frame}>
                <div className={s.heroPhoto}><Photo src={hero} alt="" /></div>
                <span className={s.frameRail} aria-hidden />
                <Art name="sprig" className={s.heroSprig} />
              </div>
            )}
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="divider" className={s.divider} />,
          node: <Art name="sprig" />,
          amp: <Art name="sprig" />,
          portrait: <Art name="sprig" className={s.pSprig} />,
          closingEmblem: <Art name="divider" className={s.closingEmblem} />,
          sentArt: <Art name="sprig" />,
        }}
      />
    </ThemeShell>
  );
}
