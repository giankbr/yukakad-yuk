"use client";
// Theme "Mutiara Teluk" — warisan penyelam mutiara di Teluk saat senja keemasan: laut senja dan kota batu karang
// bermenara angin di cakrawala, kapal dhow berlayar lateen yang terayun pelan, kerang terbuka berisi mutiara, dan
// untaian mutiara. Arsitektur, kapal, dan kerang saja (tanpa figur), bismillah dan salam diketik.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Prata", "Petrona:ital,wght@0,400;0,600;0,700;1,400", "Monsieur La Doulaise", "Amiri:wght@400"];
// Painted by /tmp/pen/art/themes/mutiara-teluk.py.
const Art = makeArt("mutiara-teluk", {
  dhow: [240, 186], oyster: [210, 181], barjeel: [640, 253], pearls: [280, 31], pearl: [60, 61],
} as const);
const BISMILLAH = "بِسْمِ اللّٰهِ الرَّحْمٰنِ الرَّحِيْمِ";

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    arabic: "السَّلَامُ عَلَيْكُمْ وَرَحْمَةُ اللّٰهِ وَبَرَكَاتُهُ",
    kicker: "Assalamu'alaikum Warahmatullahi Wabarakatuh",
    title: "Walimatul 'Urs",
    sub: "Dua lautan bertemu, dan dari keduanya lahir mutiara",
    intro: "Dengan memohon rahmat dan ridha Allah SWT, kami bermaksud menyelenggarakan akad nikah dan walimah putra-putri kami. Merupakan kebahagiaan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan mendoakan.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"],
  couple: ["Dengan Izin Allah", "Kedua Mempelai"],
  count: ["Menuju Hari Bahagia", "Hitung Mundur"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Waktu & Tempat", "Rangkaian Acara"],
  story: ["Perjalanan", "Kisah Kami"],
  gallery: ["Galeri", "Momen Bahagia"],
  wishes: ["Doa & Kehadiran", "Ucapan & Konfirmasi"],
  gifts: ["Tanda Kasih", "Amplop Digital"],
  closing: {
    thanks: "Jazakumullahu Khairan",
    text: "Atas kehadiran dan doa restu Bapak/Ibu/Saudara/i, kami ucapkan terima kasih. Semoga Allah membalas setiap kebaikan dengan kebaikan yang berlipat.",
    salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh",
  },
  sent: "Barakallahu fiikum, doa dan ucapan Anda sudah kami terima.",
  wishPlaceholder: "Tuliskan doa terbaik untuk kedua mempelai…",
};

const WISHES = [
  { id: "w1", name: "Keluarga Habib Ali Assegaf", attendance: "yes" as const, message: "Barakallahu lakuma wa baraka 'alaikuma wa jama'a bainakuma fi khair. Semoga menjadi keluarga sakinah, mawaddah, warahmah." },
  { id: "w2", name: "Sahabat PPI Qatar", attendance: "yes" as const, message: "Dari corniche Doha sampai pelaminan! Ikut bahagia, Nadhira dan Fahmi. Kami datang membawa doa terbaik." },
  { id: "w3", name: "Ustadzah Rahmah", attendance: "maybe" as const, message: "Insyaallah hadir selepas kajian. Semoga Allah menjadikan pernikahan kalian ladang pahala." },
];

export default function MutiaraTelukTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const photo = data.gallery[0] ?? data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const groom = data.couple.groom?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#0d2236"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <p className={s.coverArabic} lang="ar" dir="rtl">{BISMILLAH}</p>
          <p className={s.kicker}>Undangan {label}</p>
          <h1 className={s.coverNames}><span>{data.couple.bride}</span>{groom && <><em>&amp;</em><span>{groom}</span></>}</h1>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <Art name="dhow" eager className={s.dhow} />
          <div className={s.coverFoot}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#14304a" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        demoWishes={WISHES}
        light="#f6d79a"
        dark="#14304a"
        copy={COPY}
        hero={(
          <header className={s.hero}>
            <div className={s.heroDrop}>
              <div className={s.heroPhoto}>{photo ? <Photo src={photo} alt={`${data.couple.bride}${groom ? ` dan ${groom}` : ""}`} /> : <span className={s.heroMono} aria-hidden>{data.couple.bride.slice(0, 1)}</span>}</div>
              <span aria-hidden><Art name="oyster" className={s.heroOyster} /></span>
            </div>
            <p className={s.heroKicker}>Walimatul &apos;Urs</p>
            <h1 className={s.heroNames}><span>{data.couple.bride}</span>{groom && <><em>&amp;</em><span>{groom}</span></>}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="pearls" className={s.divider} />,
          node: <Art name="pearl" />,
          amp: <Art name="pearl" />,
          countDecor: <><span className={s.countSea} aria-hidden /><Art name="dhow" className={s.countDhow} /></>,
          closingDecor: <Art name="barjeel" className={s.closingTown} />,
          closingEmblem: <Art name="oyster" className={s.closingEmblem} />,
          sentArt: <Art name="oyster" />,
        }}
      />
    </ThemeShell>
  );
}
