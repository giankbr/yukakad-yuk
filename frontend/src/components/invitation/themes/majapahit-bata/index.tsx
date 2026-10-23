"use client";
// Theme "Majapahit Bata" — adat Jawa Timur ala Trowulan, Mojokerto: gapura bata merah terbelah (candi bentar) dilukis
// gouache bata demi bata, cakram surya bergaya Majapahit (sinar dan bintang, tanpa figur) yang terbit di celah gapura,
// kolam teratai berbibir bata, pita padma bata ekspos, dan bingkai foto berprofil candi bertingkat.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Forum", "Spectral:ital,wght@0,400;0,600;1,400", "Amiri:wght@400"];
// Painted by /tmp/pen/art/themes/majapahit-bata.py (bata.webp and frieze.webp are also CSS backgrounds).
const Art = makeArt("majapahit-bata", { gapura: [720, 663], surya: [420, 421], kolam: [800, 262], teratai: [160, 93], frieze: [380, 36] } as const);

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    arabic: "بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ",
    kicker: "Assalamu'alaikum Warahmatullahi Wabarakatuh",
    title: "Walimatul 'Ursy",
    intro: "Dengan memohon rahmat dan ridha Allah SWT, kami bermaksud menyelenggarakan pernikahan putra-putri kami. Merupakan kehormatan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"],
  couple: ["Dua insan, satu gapura", "Kedua Mempelai"],
  count: ["Menuju hari bahagia", "Hitung Mundur"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Waktu & tempat", "Rangkaian Acara"],
  story: ["Bata demi bata", "Perjalanan Kami"],
  gallery: ["Kenangan", "Galeri"],
  wishes: ["Doa & kehadiran", "Ucapan & Konfirmasi"],
  gifts: ["Tanda kasih", "Amplop Digital"],
  closing: {
    thanks: "Terima Kasih",
    text: "Atas kehadiran dan doa restu Bapak/Ibu/Saudara/i, kami ucapkan terima kasih. Semoga Allah membalas setiap kebaikan dengan keberkahan.",
    salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh",
  },
  sent: "Terima kasih, doa dan ucapan Anda sudah kami terima.",
  wishPlaceholder: "Tuliskan doa restu untuk kedua mempelai…",
};

const WISHES = [
  { id: "w1", name: "Keluarga Bapak H. Mulyono", attendance: "yes" as const, message: "Barakallahu lakuma wa baraka 'alaikuma. Semoga menjadi keluarga sakinah, mawaddah, warahmah, kokoh seperti gapura Wringin Lawang." },
  { id: "w2", name: "Rekan Guru SMAN 1 Sooko", attendance: "yes" as const, message: "Selamat Bu Kartika dan Mas Bagas! Kami sekantor insyaallah datang ke pendopo." },
  { id: "w3", name: "Dimas & Laila", attendance: "maybe" as const, message: "Mohon maaf kalau belum bisa hadir dari Surabaya. Doa terbaik untuk kalian berdua." },
];

export default function MajapahitBataTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const { bride, groom } = data.couple;
  const table = tableLabel(data.guestTable);
  const heroSrc = data.gallery[0] || data.couple.bridePhoto || data.couple.groomPhoto;
  const note = data.couple.note?.trim();
  const label = data.eventLabel?.trim() || "Pernikahan";

  return (
    <ThemeShell
      fonts={FONTS}
      background="#3a160e"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.gateWrap} aria-hidden>
            <Art name="surya" eager className={s.coverSurya} />
            <Art name="gapura" eager className={s.gateL} />
            <Art name="gapura" eager className={s.gateR} />
          </div>
          <div className={s.coverBody}>
            <p className={s.kicker}>Undangan {label}</p>
            <h1 className={s.coverNames}>{bride}<em>&amp;</em>{groom}</h1>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#fbf4e8" />Buka Undangan</button>
          </div>
          <Art name="kolam" eager className={s.coverPond} />
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        copy={COPY}
        demoWishes={WISHES}
        light="#f1d2a2"
        dark="#4a1c12"
        hero={(
          <header className={s.hero}>
            <Art name="surya" className={s.heroSurya} />
            {heroSrc && <div className={s.heroFrame}><div><Photo src={heroSrc} alt={`${bride} & ${groom}`} /></div></div>}
            <p className={s.heroKicker}>{label}</p>
            <h1 className={s.heroNames}>{bride}<em>&amp;</em>{groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="frieze" className={s.divider} />,
          node: <Art name="teratai" />,
          amp: <Art name="teratai" />,
          closingDecor: <Art name="kolam" className={s.closingPond} />,
          closingEmblem: <Art name="surya" className={s.closingSurya} />,
          sentArt: <Art name="teratai" />,
        }}
      />
    </ThemeShell>
  );
}
