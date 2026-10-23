"use client";
// Theme "Arabesk Perak" — filigri perak arabesk di atas beludru hitam: sulur islimi yang menggulung, palmet terbelah
// (rumi), dan dua batang yang saling menganyam atas-bawah membentuk kartusy lengkung runcing tempat nama berada.
// Tenang dan mewah; tanpa figur dan tanpa kaligrafi (basmalah hanya teks).
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Forum", "Cormorant Garamond:ital,wght@0,400;0,500;0,600;0,700;1,400;1,500;1,600", "Amiri"];
// Painted by /tmp/pen/art/themes/arabesk-perak.py (velvet.webp is the CSS background tile).
const Art = makeArt("arabesk-perak", { arch: [780, 1290], band: [520, 50], rosette: [240, 240], finial: [144, 174] } as const);

const COPY = {
  ...DEFAULT_COPY,
  opening: {
    arabic: "بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ",
    kicker: "Assalamu'alaikum Warahmatullahi Wabarakatuh",
    title: "Dengan Memohon Ridha-Nya",
    intro: "Dengan memohon rahmat dan ridha Allah Subhanahu wa Ta'ala, kami bermaksud menyelenggarakan walimah pernikahan putra-putri kami. Merupakan kehormatan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"] as [string, string],
  couple: ["Bismillah, kami berdua", "Kedua Mempelai"] as [string, string],
  count: ["Menanti hari yang dijanjikan", "Hitung Mundur"] as [string, string],
  units: ["Hari", "Jam", "Menit", "Detik"] as [string, string, string, string],
  events: ["Waktu dan tempat", "Rangkaian Acara"] as [string, string],
  story: ["Sulur yang bertemu", "Kisah Kami"] as [string, string],
  gallery: ["Sekilas", "Galeri"] as [string, string],
  wishes: ["Doa dan kehadiran", "Ucapan & Konfirmasi"] as [string, string],
  gifts: ["Tanda kasih", "Amplop Digital"] as [string, string],
  closing: {
    thanks: "Jazakumullah Khairan",
    text: "Atas kehadiran dan doa restu Bapak/Ibu/Saudara/i, kami ucapkan terima kasih. Semoga Allah membalas setiap kebaikan dengan keberkahan.",
    salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh",
  },
  sent: "Jazakumullah khairan, doa dan ucapan Anda sudah terkirim.",
  familyLabel: "Kami yang berbahagia",
};

const WISHES = [
  { id: "w1", name: "Keluarga H. Anwar Zulkarnain", attendance: "yes" as const, message: "Barakallahu lakuma wa baraka 'alaikuma wa jama'a bainakuma fi khair. Semoga menjadi keluarga sakinah, mawaddah, wa rahmah." },
  { id: "w2", name: "Teman Studio Arsitektur 2016", attendance: "yes" as const, message: "Dari meja maket sampai pelaminan! Ikut bahagia untuk Khalisa dan Fariz, sampai jumpa di walimah." },
  { id: "w3", name: "Ustadzah Laila & Keluarga", attendance: "maybe" as const, message: "Mohon maaf jika belum bisa hadir. Doa terbaik kami untuk kedua mempelai, semoga dilancarkan segala urusannya." },
];

export default function ArabeskPerakTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Walimatul 'Ursy";
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const photo = data.gallery[0] ?? data.couple.bridePhoto;

  return (
    <ThemeShell
      fonts={FONTS}
      background="#0c0b0e"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.cartouche}>
            <Art name="arch" eager className={s.archArt} />
            <div className={s.archIn}>
              <p className={s.arabicTop} lang="ar" dir="rtl">بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ</p>
              <p className={s.kicker}>{label}</p>
              <h1 className={s.coverNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
              <p className={s.coverDate}>{formatDate(data.date)}</p>
              <Art name="band" eager className={s.coverRule} />
              <div className={s.guestWrap}>
                <div className={s.guest}>
                  <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
                  <strong>{guestLabel(data)}</strong>
                  {table && <span className={s.table}>{table}</span>}
                </div>
                <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#121116" />Buka Undangan</button>
              </div>
            </div>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#e7eaf0"
        dark="#121116"
        copy={COPY}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            <Art name="finial" className={s.heroFinial} />
            {photo ? <div className={s.heroArch}><Photo src={photo} alt="" /></div> : <Art name="rosette" className={s.heroEmblem} />}
            <p className={s.kickerDark}>{label}</p>
            <h1 className={s.heroNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
            <Art name="band" className={s.heroBand} />
          </header>
        )}
        slots={{
          divider: <Art name="band" className={s.divider} />,
          node: <Art name="rosette" />,
          amp: <Art name="finial" />,
          portrait: <Art name="finial" />,
          countDecor: <Art name="rosette" className={s.countRosette} />,
          closingEmblem: <Art name="rosette" className={s.closingEmblem} />,
          sentArt: <Art name="rosette" />,
        }}
      />
    </ThemeShell>
  );
}
