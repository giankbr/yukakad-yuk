"use client";
// Theme "Banten Surosowan" — adat Banten (desain orisinal, arsitektur saja): panorama Banten Lama dengan atap tumpang
// lima Masjid Agung Banten, menara putih yang ramping, dan reruntuhan tembok bata Keraton Surosowan di depannya; latar
// batik Banten berwarna pastel (ungu, abu kebiruan, merah bata) dan roset kelopak delapan. Tipografi tegak seperti
// prasasti (Forum). Tanpa figur makhluk bernyawa dan tanpa kaligrafi yang digambar: basmalah diketik dengan huruf Amiri.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Forum", "Lustria", "Amiri:wght@400"];
// Painted by /tmp/pen/art/themes/banten-surosowan.py (tools/art/themes in the repo).
const Art = makeArt("banten-surosowan", { scene: [780, 640], wall: [780, 150], rosette: [160, 160] } as const);
const BISMILLAH = "بِسْمِ اللّٰهِ الرَّحْمٰنِ الرَّحِيْمِ";

const COPY: ThemeCopy = {
  opening: {
    arabic: BISMILLAH,
    kicker: "Assalamu'alaikum Warahmatullahi Wabarakatuh",
    title: "Dengan Rahmat Allah",
    intro: "Dengan memohon rahmat dan rida Allah SWT, kami bermaksud menyelenggarakan akad nikah dan walimatul 'ursy putra-putri kami. Merupakan kehormatan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"],
  couple: ["Bismillah, Kami Menikah", "Kedua Mempelai"],
  count: ["Menghitung Hari", "Menuju Akad"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Waktu & Tempat", "Rangkaian Acara"],
  story: ["Dari Banten Lama", "Kisah Kami"],
  gallery: ["Kenangan", "Galeri Foto"],
  wishes: ["Doa & Kehadiran", "Ucapan & Konfirmasi"],
  gifts: ["Tanda Kasih", "Amplop Digital"],
  closing: {
    thanks: "Terima Kasih",
    text: "Atas kehadiran dan doa restu Bapak/Ibu/Saudara/i, kami sekeluarga mengucapkan terima kasih. Semoga Allah membalas setiap kebaikan dengan keberkahan.",
    salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh",
  },
  sent: "Jazakumullah khairan, doa dan ucapan Anda sudah kami terima.",
  wishPlaceholder: "Tuliskan doa restu untuk kedua mempelai…",
  closedNote: "Terima kasih atas doa dan perhatiannya. Ucapan untuk kedua mempelai masih bisa dikirim lewat form ini.",
};

const WISHES = [
  { id: "w1", name: "K.H. Abdul Hamid & Keluarga", attendance: "yes" as Attendance, message: "Barakallahu lakuma wa baraka 'alaikuma wa jama'a bainakuma fi khair. Semoga menjadi keluarga sakinah, mawaddah, wa rahmah." },
  { id: "w2", name: "Teman KKN Kasemen 2020", attendance: "yes" as Attendance, message: "Dari posko dekat menara sampai pelaminan! Selamat Nabila dan Ilham, kami datang rombongan." },
  { id: "w3", name: "Keluarga Kang Asep, Cilegon", attendance: "maybe" as Attendance, message: "Insyaallah kami usahakan hadir. Doa terbaik dari Cilegon untuk kalian berdua." },
];

export default function BantenSurosowanTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel?.trim() || "Walimatul 'Ursy";
  const hero = data.gallery[0] ?? data.couple.bridePhoto ?? data.couple.groomPhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#f4efec"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.coverTop}>
            <p className={s.arabicCover} lang="ar" dir="rtl">{BISMILLAH}</p>
            <p className={s.salam}>Assalamu&apos;alaikum Wr. Wb.</p>
            <p className={s.coverLabel}>{label}</p>
            <h1 className={s.coverNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
          </div>
          <div className={s.panorama} aria-hidden><Art name="scene" eager /></div>
          <div className={s.coverPanel}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#8a4232" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#f1dfc2"
        dark="#8a4232"
        copy={COPY}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            <Art name="rosette" className={s.heroRose} />
            <p className={s.heroKicker}>{label}</p>
            <h1 className={s.heroNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {hero && <div className={s.parapet}><div className={s.heroPhoto}><Photo src={hero} alt="" /></div></div>}
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <span className={s.divider} aria-hidden><i /><Art name="rosette" /><i /></span>,
          node: <Art name="rosette" />,
          portrait: <Art name="rosette" className={s.pRose} />,
          closingDecor: <div className={s.closingWall} aria-hidden><Art name="wall" /></div>,
          closingEmblem: <Art name="rosette" className={s.closingRose} />,
          sentArt: <Art name="rosette" />,
        }}
      />
    </ThemeShell>
  );
}
