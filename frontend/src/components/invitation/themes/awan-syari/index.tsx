"use client";
// Theme "Awan Syari" — syar'i modern berlatar langit biru pucat yang dilukis: cahaya matahari persik yang lembut,
// gumpalan awan putih yang melayang pelan, dan hamparan awan di dasar sampul tempat nama tamu bersandar. Tanpa figur,
// pembuka Islami dengan basmalah, kartu-kartu membulat seperti awan, potret berupa jendela langit (monogram bila tanpa foto).
import { Lucide, ThemeShell, formatDate, guestLabel, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Prata:wght@400", "Nunito Sans:wght@400;600;700;800", "Amiri:wght@400;700"];
// Painted by /tmp/pen/art/themes/awan-syari.py (sky is also a CSS background)
const Art = makeArt("awan-syari", { sun: [320, 318], bank: [780, 400], cloud: [260, 136], wisp: [320, 60] } as const);

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    arabic: "بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ",
    kicker: "Assalamu'alaikum Warahmatullahi Wabarakatuh",
    title: "Dengan memohon rahmat dan rida Allah Subhanahu wa Ta'ala",
    intro: "Kami bermaksud menyelenggarakan akad nikah dan walimah putra-putri kami. Merupakan kehormatan dan kebahagiaan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"],
  couple: ["Dipertemukan oleh-Nya", "Kedua Mempelai"],
  count: ["Menuju Hari Akad", "Hitung Mundur"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Waktu & Tempat", "Rangkaian Acara"],
  story: ["Jalan Menuju Halal", "Kisah Kami"],
  gallery: ["Galeri", "Momen Kami"],
  wishes: ["Doa & Kehadiran", "Ucapan & Konfirmasi"],
  gifts: ["Tanda Kasih", "Amplop Digital"],
  closing: {
    thanks: "Jazakumullahu Khairan",
    text: "Atas kehadiran dan doa restu Bapak/Ibu/Saudara/i, kami ucapkan terima kasih. Semoga Allah membalas setiap kebaikan dengan berlipat.",
    salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh",
  },
  sent: "Jazakumullahu khairan, doa dan ucapan Anda sudah terkirim.",
  wishPlaceholder: "Tuliskan doa untuk kedua mempelai…",
};

const WISHES = [
  { id: "w1", name: "Ibu Hj. Fitriani & Keluarga", attendance: "yes" as Attendance, message: "Barakallahu lakuma wa baraka 'alaikuma wa jama'a bainakuma fii khair. Semoga menjadi keluarga sakinah, mawaddah, wa rahmah." },
  { id: "w2", name: "Ukhti Salma", attendance: "yes" as Attendance, message: "MasyaAllah, ikut bahagia! Semoga dimudahkan sampai hari akad dan seterusnya." },
  { id: "w3", name: "Keluarga Ustaz Hanif", attendance: "maybe" as Attendance, message: "Insyaallah kami usahakan hadir. Doa terbaik untuk Nabila dan Fathan." },
];

export default function AwanSyariTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Walimatul 'Ursy";
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#c6def0"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Art name="sun" eager className={s.coverSun} />
          <Art name="cloud" eager className={s.cloudA} />
          <Art name="cloud" eager className={s.cloudB} />
          <p className={s.coverArabic} lang="ar" dir="rtl">بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ</p>
          <p className={s.kicker}>{label}</p>
          <h1 className={s.coverNames}><span>{data.couple.bride}</span><em>&amp;</em><span>{data.couple.groom}</span></h1>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.coverFoot}>
            <Art name="bank" eager className={s.coverBank} />
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#ffffff" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        copy={COPY}
        demoWishes={WISHES}
        light="#ffffff"
        dark="#233f5c"
        hero={(
          <header className={s.hero}>
            <div className={s.heroWindow} aria-hidden>
              <Art name="sun" className={s.heroSun} />
              <Art name="cloud" className={s.heroCloud1} />
              <Art name="cloud" className={s.heroCloud2} />
            </div>
            <p className={s.heroKicker}>{label}</p>
            <h1 className={s.heroNames}>{data.couple.bride} <em>&amp;</em> {data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="wisp" className={s.divider} />,
          node: <Art name="cloud" />,
          amp: <Art name="wisp" />,
          portrait: <Art name="cloud" className={s.portraitCloud} />,
          countDecor: <Art name="sun" className={s.countSun} />,
          closingDecor: <Art name="bank" className={s.closingBank} />,
          closingEmblem: <Art name="sun" className={s.closingSun} />,
          sentArt: <Art name="cloud" />,
        }}
      />
    </ThemeShell>
  );
}
