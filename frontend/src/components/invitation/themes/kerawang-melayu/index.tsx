"use client";
// Theme "Kerawang Melayu" — panel kerawang tebuk tembus dari kayu cengal (desain orisinal, gouache): sulur awan larat
// berdaun dan bunga kecil yang dilubangi, ditembus cahaya petang keemasan. Sampul berupa dinding kayu gelap dengan panel
// ambang menyala di atas, berkas cahaya miring, dan genangan cahaya bercorak ukiran di lantai; isi undangan krem hangat
// dengan potret berbingkai jendela Melayu berjejala, hitung mundur seperti kaca jendela bercahaya, roset berukir yang
// menyala di penutup, serta pantun pembuka. Tanpa figur makhluk hidup dan tanpa kaligrafi lukis (basmalah diketik).
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Marcellus", "Lustria", "Amiri:wght@400"];
// Painted by /tmp/pen/art/themes/kerawang-melayu.py
const Art = makeArt("kerawang-melayu", { frieze: [780, 296], lantai: [780, 300], awan: [420, 52], bunga: [300, 300] } as const);
const BISMILLAH = "بِسْمِ اللّٰهِ الرَّحْمٰنِ الرَّحِيْمِ";
const PANTUN = ["Kayu cengal diukir halus,", "tebuk tembus disinari suria;", "doa restu kami harap tulus,", "hadirlah tuan ke majlis bahagia."];

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    arabic: BISMILLAH,
    kicker: "Assalamu'alaikum Warahmatullahi Wabarakatuh",
    title: "Dengan Hati yang Terbuka",
    intro: "Dengan memohon rahmat dan rida Allah SWT, kami bermaksud menyelenggarakan akad nikah dan majlis bersanding putera-puteri kami. Merupakan suatu penghormatan apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
  },
  roles: ["Pengantin Perempuan", "Pengantin Lelaki"],
  couple: ["Seukir sejalan", "Kedua Mempelai"],
  count: ["Menanti hari bersanding", "Hitung Mundur"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Tarikh & Tempat", "Rangkaian Majlis"],
  story: ["Ukiran perjalanan", "Kisah Kami"],
  gallery: ["Dari balik jendela", "Galeri Kami"],
  wishes: ["Doa & Kehadiran", "Ucapan & Konfirmasi"],
  gifts: ["Tanda Kasih", "Amplop Digital"],
  closing: {
    thanks: "Terima Kasih",
    text: "Kehadiran dan doa restu Bapak/Ibu/Saudara/i ibarat cahaya yang menembus ukiran: menerangi rumah tangga kami. Semoga Allah membalas setiap kebaikan.",
    salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh",
  },
  sent: "Jazakumullah khairan, doa dan ucapan Anda sudah kami terima.",
};

const WISHES = [
  { id: "w1", name: "Datuk H. Ismail Saleh", attendance: "yes" as Attendance, message: "Barakallahu lakuma wa baraka 'alaikuma. Semoga rumah tangga Aina dan Faris kukuh seperti tiang cengal, lapang seperti serambi." },
  { id: "w2", name: "Kawan-kawan Bengkel Ukir Siak", attendance: "yes" as Attendance, message: "Dari pahat kecil jadi pelaminan! Kami datang membawa kompang, insyaallah sampai sebelum berarak." },
  { id: "w3", name: "Kak Rahmah, Tanjungpinang", attendance: "maybe" as Attendance, message: "Insyaallah kami usahakan hadir. Doa terbaik dari seberang, semoga sakinah, mawaddah, wa rahmah." },
];

export default function KerawangMelayuTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Walimatul 'Urus";
  const hero = data.gallery[0] ?? data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#22100a"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <span className={s.beams} aria-hidden />
          <div className={s.floor} aria-hidden><Art name="lantai" eager /></div>
          <div className={s.frieze} aria-hidden><Art name="frieze" eager /></div>
          <p className={s.arabicCover} lang="ar" dir="rtl">{BISMILLAH}</p>
          <p className={s.kicker}>Undangan {label}</p>
          <h1 className={s.names}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <Art name="bunga" eager className={s.coverRose} />
          <span className={s.spacer} aria-hidden />
          <div className={s.guestCard}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
          </div>
          <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={17} color="#3a1a08" />Buka Undangan</button>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#fff6df"
        dark="#3a1a08"
        copy={COPY}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            <p className={s.heroKicker}>{label}</p>
            <h1 className={s.heroNames}>{data.couple.bride} <em>&amp;</em> {data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {hero && (
              <div className={s.window}>
                <Art name="frieze" className={s.windowTop} />
                <div className={s.heroPhoto}><Photo src={hero} alt={`${data.couple.bride} dan ${data.couple.groom}`} /></div>
              </div>
            )}
            <p className={s.pantun}>{PANTUN.map(line => <span key={line}>{line}<br /></span>)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="awan" className={s.divider} />,
          node: <Art name="bunga" />,
          amp: <Art name="bunga" />,
          portrait: <span className={s.jejala} aria-hidden><Art name="awan" /></span>,
          countDecor: <Art name="bunga" className={s.countRose} />,
          closingEmblem: <Art name="bunga" className={s.closingRose} />,
          sentArt: <Art name="bunga" />,
        }}
      />
    </ThemeShell>
  );
}
