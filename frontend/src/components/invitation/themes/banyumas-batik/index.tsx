"use client";
// Theme "Banyumas Batik" — pernikahan bernuansa Banyumasan. Sampul: lanskap cat air Gunung Slamet, kebun kelapa dan
// Kali Serayu yang turun ke selembar kain batik sogan-hitam (daun lumbon, jahe srimpang, cecek, retak malam) berpinggir
// tumpal, dengan label nama krem bergaris sogan dan daun lumbon yang bergoyang. Hero: pinggiran kain batik vertikal,
// nama rata kiri, foto berbingkai kain. Kartu acara berpunggung batik, potret selang-seling kiri-kanan, hitung mundur
// di atas kain batik, penutup kembali ke lanskap Slamet.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Gloock", "Alegreya:ital,wght@0,400;0,700;1,400;1,700", "Mrs Saint Delafield", "Amiri:wght@400;700"];
// Painted by /tmp/pen/art/themes/banyumas-batik.py (tools/art/themes in the repo).
const Art = makeArt("banyumas-batik", {
  slamet: [680, 554], lumbon: [240, 415], jahe: [320, 82], palm: [220, 409],
} as const);

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    arabic: "بِسْمِ اللّٰهِ الرَّحْمٰنِ الرَّحِيْمِ",
    kicker: "Assalamu'alaikum Warahmatullahi Wabarakatuh",
    title: "Monggo, Sedulur",
    intro: "Dengan memohon rahmat dan ridha Allah SWT, kami bermaksud menyelenggarakan pernikahan putra-putri kami di Purwokerto. Kehadiran serta doa restu Bapak/Ibu/Saudara/i merupakan kebahagiaan bagi kami sekeluarga.",
  },
  roles: ["Pengantin Putri", "Pengantin Putra"],
  couple: ["Loro dadi siji", "Kedua Mempelai"],
  count: ["Wis cedhak", "Menuju Hari Bahagia"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Papan lan wektu", "Rangkaian Acara"],
  story: ["Critane kita", "Perjalanan Kami"],
  gallery: ["Kenangan", "Galeri Foto"],
  wishes: ["Donga lan pangestu", "Ucapan & Kehadiran"],
  gifts: ["Tanda kasih", "Amplop Digital"],
  closing: {
    thanks: "Matur Suwun",
    text: "Atas kehadiran dan doa restu Bapak/Ibu/Saudara/i, kami ucapkan terima kasih. Semoga Allah membalas kebaikan panjenengan semua.",
    salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh",
  },
  sent: "Matur suwun, doa dan ucapan Anda sudah kami terima.",
  wishPlaceholder: "Tuliskan doa untuk kedua mempelai…",
  giftIntro: "Doa restu Anda adalah hadiah terindah. Bila berkenan memberi tanda kasih, dapat melalui:",
};

const WISHES = [
  { id: "w1", name: "Lik Warsini sekeluarga", attendance: "yes" as Attendance, message: "Selamat ya Laras lan Bayu! Muga dadi keluarga sakinah, mawaddah, warahmah. Bulikmu mesti teka, wis nyiapna mendoan sing akeh." },
  { id: "w2", name: "Teman KKN Ketenger 2020", attendance: "yes" as Attendance, message: "Barakallahu lakuma wa baraka 'alaikuma. Dari pipa air desa sampai pelaminan, kami ikut bahagia!" },
  { id: "w3", name: "Mas Gilang (Jakarta)", attendance: "no" as Attendance, message: "Ngapura ya, durung bisa mulih ke Purwokerto. Doa terbaik dari jauh, semoga lancar sampai hari H." },
];

export default function BanyumasBatikTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const photo = data.gallery[0] ?? data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#f3ead6"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.coverSky}>
            <Art name="slamet" eager className={s.coverScene} />
            <p className={s.coverKicker}>Undangan {label}</p>
          </div>
          <div className={s.kain}>
            <Art name="lumbon" eager className={s.coverLeaf} />
            <div className={s.label}>
              <p className={s.labelTop}>Purwokerto, Banyumas</p>
              <h1 className={s.coverNames}>{data.couple.bride}<span>&amp;</span>{data.couple.groom}</h1>
              <p className={s.coverDate}>{formatDate(data.date)}</p>
              <div className={s.guest}>
                <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
                <strong>{guestLabel(data)}</strong>
                {table && <span className={s.table}>{table}</span>}
              </div>
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#1c1612" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#ecd6a6"
        dark="#1c1612"
        copy={COPY}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            <span className={s.heroSelvedge} aria-hidden />
            <Art name="palm" className={s.heroPalm} />
            <p className={s.heroKicker}>Walimatul &lsquo;Ursy &middot; {label}</p>
            <h1 className={s.heroNames}>{data.couple.bride}<i>&amp;</i>{data.couple.groom}</h1>
            {photo && <div className={s.heroPhoto}><Photo src={photo} alt={`${data.couple.bride} & ${data.couple.groom}`} /></div>}
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="jahe" className={s.divider} />,
          node: <Art name="lumbon" />,
          amp: <Art name="lumbon" />,
          portrait: <span className={s.portraitLeaf} aria-hidden><Art name="lumbon" /></span>,
          closingDecor: <Art name="slamet" className={s.closingScene} />,
          closingEmblem: <Art name="lumbon" className={s.closingEmblem} />,
          sentArt: <Art name="jahe" />,
        }}
      />
    </ThemeShell>
  );
}
