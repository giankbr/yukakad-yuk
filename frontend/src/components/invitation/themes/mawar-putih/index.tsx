"use client";
// Theme "Mawar Putih" — syar'i, putih gading dan hijau tua: bulan sabit rangkaian mawar putih cat air-gouache yang
// keluar dari tepi kiri sampul, teks rata kiri bergaris emas tipis, kartu bersudut daun, dan pita hijau tua.
// Hanya flora (tanpa figur makhluk hidup), basmalah sebagai teks. Dilukis oleh /tmp/pen/art/themes/mawar-putih.py.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Italiana", "Gentium Book Plus:ital,wght@0,400;0,700;1,400", "Monsieur La Doulaise", "Amiri"];
const Art = makeArt("mawar-putih", {
  wreath: [711, 732], cluster: [520, 375], sprig: [420, 62], rose: [185, 172], corner: [360, 344],
} as const);
const BISMILLAH = "بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ";

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    arabic: BISMILLAH,
    kicker: "Assalamu'alaikum Warahmatullahi Wabarakatuh",
    title: "Walimatul 'Ursy",
    sub: "dengan rahmat Allah",
    intro: "Dengan memohon rahmat dan rida Allah Subhanahu wa Ta'ala, kami bermaksud menyelenggarakan pernikahan putra-putri kami. Merupakan kehormatan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"],
  couple: ["Dipertemukan dalam rida-Nya", "Kedua Mempelai"],
  count: ["Menanti hari yang diberkahi", "Hitung Mundur"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Waktu dan tempat", "Rangkaian Acara"],
  story: ["Perjalanan kami", "Kisah Ta'aruf"],
  gallery: ["Sekilas kenangan", "Galeri"],
  wishes: ["Doa dan kehadiran", "Ucapan & Konfirmasi"],
  gifts: ["Tanda kasih", "Amplop Digital"],
  closing: {
    thanks: "Jazakumullahu Khairan",
    text: "Kehadiran dan doa restu Bapak/Ibu/Saudara/i merupakan kehormatan serta kebahagiaan bagi kami sekeluarga.",
    salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh",
  },
  sent: "Jazakumullahu khairan, doa dan ucapan Anda sudah kami terima.",
  wishPlaceholder: "Tuliskan doa terbaik untuk kedua mempelai…",
  giftIntro: "Doa restu Anda adalah hadiah terindah. Bila berkenan memberi tanda kasih, dapat melalui:",
  familyLabel: "Kami yang berbahagia",
};

const WISHES = [
  { id: "w1", name: "Ustazah Rahmah & Keluarga", attendance: "yes" as const, message: "Barakallahu lakuma wa baraka 'alaikuma wa jama'a bainakuma fi khair. Semoga menjadi keluarga yang sakinah, mawaddah, warahmah." },
  { id: "w2", name: "Rekan Apoteker RS Salak", attendance: "yes" as const, message: "MasyaAllah, ikut berbahagia, Salsa! Semoga Allah mudahkan sampai hari akad dan seterusnya." },
  { id: "w3", name: "Keluarga Om Hasan, Sukabumi", attendance: "maybe" as const, message: "Mohon maaf bila berhalangan hadir. Doa terbaik kami untuk Salsabila dan Fathan." },
];

export default function MawarPutihTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const kicker = label === "Pernikahan" ? "Undangan Walimatul 'Ursy" : `Undangan ${label}`;
  const bride = data.couple.bride;
  const groom = data.couple.groom?.trim();
  const photo = data.gallery[0];
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#e9e3d3"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.wreathWrap}>
            <Art name="wreath" eager className={s.wreath} />
            <p className={s.coverArabic} lang="ar" dir="rtl">{BISMILLAH}</p>
            <p className={s.coverSalam}>Assalamu&apos;alaikum Wr. Wb.</p>
          </div>
          <div className={s.coverText}>
            <p className={s.kicker}>{kicker}</p>
            <h1 className={s.coverNames}><span>{bride}</span>{groom && <><em>&amp;</em><span>{groom}</span></>}</h1>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
          </div>
          <div className={s.coverFoot}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#1f3d2c" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        copy={COPY}
        demoWishes={WISHES}
        light="#ece3c9"
        dark="#1f3d2c"
        hero={(
          <header className={s.hero}>
            <div className={s.heroPhoto}>{photo ? <Photo src={photo} alt={`${bride}${groom ? ` dan ${groom}` : ""}`} /> : <span className={s.heroMono} aria-hidden>{bride.slice(0, 1)}</span>}</div>
            <Art name="cluster" className={s.heroCluster} />
            <p className={s.heroKicker}>{kicker}</p>
            <h1 className={s.heroNames}>{bride}{groom && <> <em>&amp;</em> {groom}</>}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="sprig" className={s.divider} />,
          node: <Art name="rose" />,
          amp: <Art name="rose" />,
          portrait: <Art name="rose" className={s.portraitArt} />,
          countDecor: <><Art name="corner" className={`${s.countLeaf} ${s.countLeafL}`} /><Art name="corner" className={`${s.countLeaf} ${s.countLeafR}`} /></>,
          closingEmblem: <Art name="cluster" className={s.closingEmblem} />,
          sentArt: <Art name="rose" />,
        }}
      />
    </ThemeShell>
  );
}
