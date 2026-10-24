"use client";
// Theme "Lurik Klaten" — adat Jawa dari desa penenun lurik Pedan–Cawas, Klaten. Sampulnya label linen yang dijahit di
// atas sepotong lurik nila (garis benang tenun ATBM), dengan lukisan desa: sawah berundak dan Merapi di kejauhan.
// Pita tenun berumbai jadi pembatas, kain lurik dijemur di bambu, teropong kayu melintas di pita hitung mundur,
// dan kelos benang soga di linimasa. Semua dilukis ulang dengan gouache.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Zilla Slab:wght@500;600", "Alegreya:ital,wght@0,400;0,700;1,400", "Barlow Condensed:wght@500;600", "Amiri"];
// Painted by /tmp/pen/art/themes/lurik-klaten.py (lurik and sogan are CSS background tiles).
const Art = makeArt("lurik-klaten", { desa: [780, 700], kain: [560, 485], pita: [446, 37], teropong: [300, 69], kelos: [82, 130] } as const);

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    arabic: "بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ",
    kicker: "Assalamu'alaikum Warahmatullahi Wabarakatuh",
    title: "Mohon Doa Restu",
    sub: "Lungsin lan pakan, dados satunggal",
    intro: "Dengan memohon rahmat dan ridha Allah Subhanahu wa Ta'ala, kami bermaksud menyelenggarakan pernikahan putra-putri kami. Merupakan kehormatan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
  },
  roles: ["Mempelai Putri", "Mempelai Putra"],
  couple: ["Lungsin & Pakan", "Kedua Mempelai"],
  count: ["Sedikit Lagi", "Menuju Hari Bahagia"],
  units: ["Dina", "Jam", "Menit", "Detik"],
  events: ["Adicara", "Waktu & Tempat"],
  story: ["Benang Perjalanan", "Kisah Kami"],
  gallery: ["Galeri", "Lembar Kenangan"],
  wishes: ["Donga & Rawuh", "Ucapan & Konfirmasi"],
  gifts: ["Tanda Tresna", "Amplop Digital"],
  closing: {
    thanks: "Matur Suwun",
    text: "Kehadiran dan doa restu Bapak/Ibu/Saudara/i adalah benang terindah dalam tenunan hidup baru kami. Atas perhatiannya, kami ucapkan terima kasih.",
    salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh",
  },
  sent: "Matur suwun, doa dan ucapan Anda sudah kami terima.",
  wishPlaceholder: "Tuliskan doa restu untuk kedua mempelai…",
  giftIntro: "Doa restu Anda adalah hadiah terindah bagi kami. Bila berkenan memberi tanda kasih, dapat melalui:",
};

const WISHES = [
  { id: "w1", name: "Bude Sri & Pakde Harjo, Pedan", attendance: "yes" as Attendance, message: "Barakallahu lakuma. Mugi dados kulawarga ingkang ayem tentrem, rukun, lan tansah pinaringan berkah." },
  { id: "w2", name: "Mbak Tutik & Penenun Tlingsing", attendance: "yes" as Attendance, message: "Ikut bungah, Laras. Semoga rumah tangganya rapat dan awet seperti lurik yang ditenun pelan-pelan." },
  { id: "w3", name: "Kelompok Tani Sido Makmur", attendance: "maybe" as Attendance, message: "Selamat Mas Bayu! Insyaallah kami menyusul di ngunduh mantu. Semoga panennya berlimpah, rezekinya juga." },
];

export default function LurikKlatenTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const groom = data.couple.groom?.trim();
  const photo = data.gallery[0] ?? data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#22304f"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.label}>
            <Art name="pita" eager className={s.labelTape} />
            <div className={s.labelScene} aria-hidden><Art name="desa" eager /></div>
            <p className={s.kicker}>Undangan {label}</p>
            <h1 className={s.coverNames}><span>{data.couple.bride}</span>{groom && <><em>&amp;</em><span>{groom}</span></>}</h1>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={17} color="#fbf3e2" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        demoWishes={WISHES}
        light="#f4ead2"
        dark="#2d3b5e"
        copy={COPY}
        hero={(
          <header className={s.hero}>
            <Art name="kain" className={s.heroCloth} />
            <p className={s.heroKicker}>Pawiwahan · Klaten</p>
            <h1 className={s.heroNames}>{data.couple.bride}{groom && <><em>&amp;</em>{groom}</>}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {photo && (
              <div className={s.heroSnap}>
                <Photo src={photo} alt={[data.couple.bride, groom].filter(Boolean).join(" dan ")} className={s.heroPic} />
              </div>
            )}
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="pita" className={s.divider} />,
          node: <Art name="kelos" />,
          amp: <Art name="kelos" />,
          portrait: <Art name="pita" className={s.portraitArt} />,
          countDecor: <Art name="teropong" className={s.shuttle} />,
          closingDecor: <Art name="desa" className={s.closingScene} />,
          closingEmblem: <Art name="teropong" className={s.closingEmblem} />,
          sentArt: <Art name="kelos" />,
        }}
      />
    </ThemeShell>
  );
}
