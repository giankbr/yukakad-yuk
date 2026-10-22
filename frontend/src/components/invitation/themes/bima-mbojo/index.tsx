"use client";
// Theme "Bima Mbojo" — pernikahan Islami Bima: lumbung uma lengge beratap ilalang di bukit savana di atas Teluk Bima saat
// senja, dilukis gouache; tenun tembe nggoli kotak-kotak (ditenun per benang) menjadi selempang sampul, cincin bingkai
// kapsul, dan tepi kartu; seikat padi sebagai pemisah. Merah tembe, ungu terong, kuning kunyit, dan pasir senja.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Rozha One", "Kurale", "Amiri:wght@400;700"];
// Painted by /tmp/pen/art/themes/bima-mbojo.py (tools/art/themes in the repo).
const Art = makeArt("bima-mbojo", { lengge: [760, 916], pita: [780, 90], lengge1: [170, 335], padi: [160, 105] } as const);

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    arabic: "بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ",
    kicker: "Assalamu'alaikum Wr. Wb.",
    title: "Dengan Rahmat Allah",
    intro: "Dengan memohon rahmat dan rida Allah Subhanahu wa Ta'ala, kami bermaksud menyelenggarakan akad nikah dan walimah putra-putri kami. Merupakan kehormatan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"],
  couple: ["Kedua Mempelai", "Dua Hati, Satu Lumbung"],
  count: ["Menghitung Hari", "Menuju Hari Bahagia"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Waktu & Tempat", "Rangkaian Acara"],
  story: ["Kisah Kami", "Senja di Teluk Bima"],
  gallery: ["Galeri", "Momen Bahagia"],
  wishes: ["Doa & Kehadiran", "Ucapan & Konfirmasi"],
  gifts: ["Tanda Kasih", "Amplop Digital"],
  closing: { thanks: "Terima Kasih", text: "Atas kehadiran dan doa restu Bapak/Ibu/Saudara/i, kami ucapkan terima kasih. Semoga Allah membalas setiap kebaikan dengan berlipat.", salam: "Wassalamu'alaikum Wr. Wb." },
  sent: "Terima kasih, doa dan ucapan Anda sudah terkirim.",
  wishPlaceholder: "Tuliskan doa terbaik untuk kedua mempelai…",
};

const WISHES = [
  { id: "w1", name: "Keluarga H. Ishaka Abubakar", attendance: "yes" as Attendance, message: "Barakallahu lakuma wa baraka 'alaikuma wa jama'a bainakuma fi khair. Selamat Nurul dan Ikhsan." },
  { id: "w2", name: "Rekan Perawat RSUD Bima", attendance: "yes" as Attendance, message: "Selamat ya Nurul! Semoga menjadi keluarga sakinah, mawaddah, warahmah, dan selalu rukun." },
  { id: "w3", name: "Ompu Ali & Keluarga, Sape", attendance: "maybe" as Attendance, message: "Insyaallah kami datang dari Sape. Doa terbaik untuk kalian berdua." },
];

export default function BimaMbojoTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const hero = data.gallery[0] ?? data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#f0b87e"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Art name="lengge" eager className={s.coverArt} />
          <div className={s.coverTop}>
            <p className={s.bismillah} lang="ar" dir="rtl">بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ</p>
            <p className={s.salam}>Assalamu&apos;alaikum Wr. Wb.</p>
          </div>
          <div className={s.sheet}>
            <Art name="pita" eager className={s.sash} />
            <p className={s.kicker}>Undangan {label}</p>
            <h1 className={s.coverNames}>{data.couple.bride}<em>dan</em>{data.couple.groom}</h1>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
            <div className={s.guestWrap}>
              <div className={s.guest}>
                <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
                <strong>{guestLabel(data)}</strong>
                {table && <span className={s.table}>{table}</span>}
              </div>
              <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#f2cf7a" />Buka Undangan</button>
            </div>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#f2cf7a"
        dark="#8e1f3a"
        copy={COPY}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            {hero && (
              <div className={s.heroCapsule}>
                <div className={s.heroPhoto}><Photo src={hero} alt="" /></div>
                <span className={s.heroBarn} aria-hidden><Art name="lengge1" /></span>
                <span className={s.heroPadi} aria-hidden><Art name="padi" /></span>
              </div>
            )}
            <p className={s.heroKicker}>Walimatul &apos;Ursy</p>
            <h1 className={s.heroNames}>{data.couple.bride}<em>dan</em>{data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <span className={s.divider} aria-hidden><i /><Art name="padi" /><i /></span>,
          node: <Art name="padi" />,
          amp: <Art name="padi" />,
          portrait: <Art name="lengge1" className={s.pl} />,
          closingDecor: <Art name="pita" className={s.closePita} />,
          closingEmblem: <Art name="lengge1" className={s.closingEmblem} />,
          sentArt: <Art name="lengge1" />,
        }}
      />
    </ThemeShell>
  );
}
