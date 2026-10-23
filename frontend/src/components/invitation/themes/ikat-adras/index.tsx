"use client";
// Theme "Ikat Adras" — walimatul 'ursy bernuansa kain ikat sutra adras Asia Tengah. Sampul asimetris: lajur kain adras
// (sisir, awan, almond, belah ketupat berpengait) bertepi kabur khas ikat lungsin yang bergeser pelan seperti kain
// ditarik dari gulungan, medali almond yang menjembatani kain dan kertas gading, lalu basmalah, nama dan kartu tamu
// rata kiri. Isi halaman bertepi selvedge sutra di kiri, potret bersudut takik di samping nama, hitung mundur di atas
// kain bernila. Hanya geometri; tanpa figur dan tanpa kaligrafi lukis (teks Arab diketik).
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Rozha One", "Spectral:ital,wght@0,400;0,600;0,700;1,400", "Amiri:wght@400;700"];
// Painted by /tmp/pen/art/themes/ikat-adras.py (tools/art/themes in the repo).
const Art = makeArt("ikat-adras", { medallion: [105, 177], band: [160, 25], node: [30, 36] } as const);
const BISMILLAH = "بِسْمِ اللّٰهِ الرَّحْمٰنِ الرَّحِيْمِ";

const COPY = {
  ...DEFAULT_COPY,
  opening: {
    arabic: BISMILLAH,
    kicker: "Assalamu'alaikum Warahmatullahi Wabarakatuh",
    title: "Dengan memohon rahmat dan rida Allah SWT",
    intro: "Kami bermaksud menyelenggarakan akad nikah dan walimatul 'ursy putra-putri kami. Merupakan kehormatan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"] as [string, string],
  couple: ["Dua benang, satu tenunan", "Kedua Mempelai"] as [string, string],
  count: ["Menuju hari akad", "Hitung Mundur"] as [string, string],
  units: ["Hari", "Jam", "Menit", "Detik"] as [string, string, string, string],
  events: ["Waktu & Tempat", "Rangkaian Acara"] as [string, string],
  story: ["Ditenun perlahan", "Kisah Kami"] as [string, string],
  gallery: ["Galeri", "Momen Bahagia"] as [string, string],
  wishes: ["Doa & Restu", "Ucapan & Kehadiran"] as [string, string],
  gifts: ["Tanda Kasih", "Amplop Digital"] as [string, string],
  closing: {
    thanks: "Jazakumullah Khairan",
    text: "Atas kehadiran dan doa restu Bapak/Ibu/Saudara/i, kami ucapkan terima kasih. Semoga Allah SWT membalas kebaikan Anda dengan keberkahan.",
    salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh",
  },
  sent: "Jazakumullah khairan, doa dan ucapan Anda sudah kami terima.",
  wishPlaceholder: "Tuliskan doa restu untuk kedua mempelai…",
  giftIntro: "Doa restu Anda adalah hadiah terindah. Jika berkenan memberi tanda kasih, dapat melalui:",
  familyLabel: "Kami yang berbahagia, keluarga besar",
};

const WISHES = [
  { id: "w1", name: "Ibu Dr. Hj. Laila Fitriani", attendance: "yes" as Attendance, message: "Barakallahu lakuma wa baraka 'alaikuma wa jama'a bainakuma fi khair. Semoga sakinah, mawaddah, warahmah." },
  { id: "w2", name: "Teman Studio Wastra", attendance: "yes" as Attendance, message: "Akhirnya kain kalian selesai ditenun! Selamat Salma dan Fikri, kami datang dengan baju paling berwarna." },
  { id: "w3", name: "Keluarga Bapak Hasan (Tashkent)", attendance: "no" as Attendance, message: "Mohon maaf belum bisa pulang. Doa terbaik dari jauh, semoga menjadi keluarga yang penuh berkah." },
];

export default function IkatAdrasTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Walimatul 'Ursy";
  const heroPhoto = data.gallery[0] ?? data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#23306e"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.cloth} aria-hidden />
          <Art name="medallion" eager className={s.coverMedal} />
          <div className={s.coverText}>
            <p className={s.coverArabic} lang="ar" dir="rtl">{BISMILLAH}</p>
            <p className={s.kicker}>{label}</p>
            <h1 className={s.coverNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
            <Art name="band" eager className={s.coverBand} />
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#f7c95a" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#f7c95a"
        dark="#23306e"
        copy={COPY}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            {heroPhoto && <div className={s.heroFrame}><Photo src={heroPhoto} alt={`${data.couple.bride} & ${data.couple.groom}`} /></div>}
            <p className={s.heroKicker}>{label}</p>
            <h1 className={s.heroNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="band" className={s.divider} />,
          node: <Art name="node" />,
          amp: <Art name="node" />,
          closingEmblem: <Art name="medallion" className={s.closingMedal} />,
          sentArt: <Art name="medallion" />,
        }}
      />
    </ThemeShell>
  );
}
