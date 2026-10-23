"use client";
// Theme "Muaro Jambi" — adat Melayu Jambi: fajar di situs candi bata merah Muaro Jambi di tepi Batanghari (hanya
// arsitektur: teras bata, tangga, tembok keliling yang runtuh; tanpa arca), hutan dan sungai dengan perahu ketek,
// batik Jambi duren pecah dan kapal sanggat biru nila. Gouache orisinal. Pembuka Islami (basmalah, salam).
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Marcellus", "Alegreya:ital,wght@0,400;0,500;0,600;0,700;1,400", "Amiri:wght@400;700"];
const BISMILLAH = "بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ";
// Painted by /tmp/pen/art/themes/muaro-jambi.py.
const Art = makeArt("muaro-jambi", {
  scene: [780, 768], boat: [240, 102], divider: [360, 50], arch: [390, 495], leaves: [360, 292],
} as const);

const WISHES = [
  { id: "w1", name: "Keluarga Datuk H. Ismail", attendance: "yes" as const, message: "Barakallahu lakuma wa baraka 'alaikuma. Semoga menjadi keluarga sakinah, mawaddah, warahmah, kokoh seperti candi di tepi Batanghari." },
  { id: "w2", name: "Rina & Teman Relawan Situs", attendance: "yes" as const, message: "Dari kuliah lapangan sampai pelaminan! Ikut bahagia, Nadia dan Fikri. Sampai jumpa di Kota Jambi." },
  { id: "w3", name: "Bang Hendra Sekeluarga", attendance: "maybe" as const, message: "Insyaallah kami usahakan hadir. Doa terbaik untuk kalian berdua, semoga lancar sampai hari H." },
];

export default function MuaroJambiTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const { couple } = data;
  const table = tableLabel(data.guestTable);
  const label = data.eventLabel ?? "Walimatul 'Ursy";
  const heroPhoto = data.gallery[0] ?? couple.bridePhoto ?? couple.groomPhoto;
  const note = couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#f4d6ae"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.coverTop}>
            <p className={s.coverArabic} lang="ar" dir="rtl">{BISMILLAH}</p>
            <p className={s.kicker}>{label}</p>
            <h1 className={s.coverNames}><span>{couple.bride}</span><i>&amp;</i><span>{couple.groom}</span></h1>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
          </div>
          <div className={s.coverScene}>
            <Art name="scene" eager />
            <Art name="boat" eager className={s.boat} />
          </div>
          <div className={s.coverFoot}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={17} color="#fff7ea" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#f3d58e"
        dark="#23305a"
        demoWishes={WISHES}
        copy={{
          opening: {
            arabic: BISMILLAH,
            kicker: "Assalamu'alaikum Wr. Wb.",
            title: "Dengan Rahmat Allah",
            sub: "Tepak sirih terbuka, kami menjemput Bapak/Ibu",
            intro: "Dengan memohon rahmat dan ridha Allah Subhanahu wa Ta'ala, kami bermaksud menyelenggarakan walimah pernikahan putra-putri kami. Merupakan kehormatan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
          },
          roles: ["Mempelai Wanita", "Mempelai Pria"],
          couple: ["Bismillah, Kami Bersatu", "Kedua Mempelai"],
          count: ["Menghitung Hari", "Menuju Hari Bahagia"],
          units: ["Hari", "Jam", "Menit", "Detik"],
          events: ["Waktu & Tempat", "Rangkaian Acara"],
          story: ["Sepanjang Batanghari", "Kisah Kami"],
          gallery: ["Galeri", "Jejak Bahagia"],
          wishes: ["Doa & Restu", "Ucapan & Kehadiran"],
          gifts: ["Tanda Kasih", "Amplop Digital"],
          closing: { thanks: "Terimo Kasih", text: "Atas kehadiran dan doa restu Bapak/Ibu/Saudara/i, kami sekeluarga mengucapkan terima kasih. Semoga Allah membalas setiap kebaikan dengan keberkahan.", salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh" },
          sent: "Terimo kasih, doa dan ucapan Anda sudah kami terima.",
          wishPlaceholder: "Tuliskan doa restu untuk kedua mempelai…",
        }}
        hero={(
          <header className={s.hero}>
            <div className={s.heroBand} aria-hidden />
            <span className={s.coping} aria-hidden style={{ width: "100%" }} />
            <div className={s.heroWin}>
              <div className={s.heroPhotoWrap}>
                {heroPhoto ? <Photo src={heroPhoto} alt={`${couple.bride} & ${couple.groom}`} /> : <span className={s.heroMono} aria-hidden>{couple.bride.slice(0, 1)}</span>}
              </div>
              <Art name="arch" className={s.heroArch} />
              <Art name="leaves" className={s.heroLeaf} />
            </div>
            <p className={s.heroKicker}>{label}</p>
            <h1 className={s.heroNames}>{couple.bride} <i>&amp;</i> {couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="divider" className={s.divider} />,
          node: <Art name="boat" />,
          amp: <Art name="divider" />,
          portrait: <Art name="arch" className={s.portraitArch} />,
          closingDecor: <><Art name="leaves" className={s.closingLeaves} /><Art name="leaves" className={s.closingLeaves} /></>,
          closingEmblem: <Art name="boat" className={s.closingEmblem} />,
          sentArt: <Art name="boat" />,
        }}
      />
    </ThemeShell>
  );
}
