"use client";
// Theme "Paisley Kashmir" — Islami, selendang kani Kashmir yang ditenun: sampul bertata letak chand-dar (medalion bundar
// di tengah dengan nama di ruang gadingnya, seperempat medalion di keempat sudut, pinggiran boteh rapat di keliling),
// foto pembuka berbingkai boteh tenun, kartu acara berpinggir selvedge. Semua ornamen bunga dan boteh; tanpa figur,
// tanpa kaligrafi lukis.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Rozha One", "Vollkorn:ital,wght@0,400;0,500;0,600;1,400;1,500", "Amiri:wght@400;700"];
// Painted (woven) by /tmp/pen/art/themes/paisley-kashmir.py; weave/border/border-v/mask are CSS backgrounds or masks.
const Art = makeArt("paisley-kashmir", { medallion: [640, 640], corner: [320, 320], boteh: [220, 328], frame: [480, 720] } as const);
const BISMILLAH = "بِسْمِ اللّٰهِ الرَّحْمٰنِ الرَّحِيْمِ";

const WISHES = [
  { id: "w1", name: "Ibu Hj. Ratna Dewi", attendance: "yes" as const, message: "Barakallahu lakuma wa baraka 'alaikuma wa jama'a bainakuma fi khair. Semoga rumah tangga kalian hangat seperti selendang yang ditenun dengan sabar." },
  { id: "w2", name: "Komunitas Wastra Muda", attendance: "yes" as const, message: "Selamat Zahira & Ilham! Dari pameran kain sampai pelaminan. Kami datang pakai selendang terbaik." },
  { id: "w3", name: "Faisal & Keluarga", attendance: "maybe" as const, message: "Insyaallah kami hadir selepas akad. Semoga sakinah, mawaddah, warahmah." },
];

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    arabic: BISMILLAH,
    kicker: "Assalamu'alaikum Wr. Wb.",
    title: "Dengan Memohon Ridha Allah",
    intro: "Dengan memohon rahmat dan ridha Allah Subhanahu wa Ta'ala, kami bermaksud menyelenggarakan pernikahan putra-putri kami. Merupakan kehormatan dan kebahagiaan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"],
  couple: ["Dua Helai Benang", "Kedua Mempelai"],
  count: ["Insyaallah", "Menuju Hari Akad"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Waktu & Tempat", "Rangkaian Acara"],
  story: ["Ditenun Perlahan", "Kisah Kami"],
  gallery: ["Kenangan", "Galeri"],
  wishes: ["Doa & Ucapan", "Ucapan & Kehadiran"],
  gifts: ["Tanda Kasih", "Amplop Digital"],
  closing: { thanks: "Jazakumullah Khairan", text: "Atas kehadiran dan doa restu Bapak/Ibu/Saudara/i, kami ucapkan terima kasih. Semoga Allah membalas setiap kebaikan dengan berlipat.", salam: "Wassalamu'alaikum Wr. Wb." },
  sent: "Jazakumullah khairan, doa dan ucapan Anda sudah terkirim.",
  wishPlaceholder: "Tuliskan doa terbaik untuk kedua mempelai…",
};

function Divider() {
  return <span className={s.divider} aria-hidden><Art name="boteh" /></span>;
}

export default function PaisleyKashmirTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const hero = data.gallery[0] ?? data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#f2e7cf"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Art name="corner" eager className={`${s.coverCorner} ${s.cornerTL}`} />
          <Art name="corner" eager className={`${s.coverCorner} ${s.cornerTR}`} />
          <Art name="corner" eager className={`${s.coverCorner} ${s.cornerBL}`} />
          <Art name="corner" eager className={`${s.coverCorner} ${s.cornerBR}`} />
          <p className={s.coverArabic} lang="ar" dir="rtl">{BISMILLAH}</p>
          <p className={s.kicker}>{/walim|nikah|perni/i.test(label) ? label : `Undangan ${label}`}</p>
          <div className={s.chand}>
            <Art name="medallion" eager className={s.chandArt} />
            <h1 className={s.coverNames}><span>{data.couple.bride}</span><em>dan</em><span>{data.couple.groom}</span></h1>
          </div>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.guestWrap}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#f8f0dc" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        copy={COPY}
        demoWishes={WISHES}
        light="#efc56c"
        dark="#6e1d1b"
        hero={(
          <header className={s.hero}>
            <div className={s.heroBoteh}>
              <div className={s.heroPhoto}>{hero && <Photo src={hero} alt="" />}</div>
              <Art name="frame" className={s.heroFrame} />
            </div>
            <p className={s.heroKicker}>{label}</p>
            <h1 className={s.heroNames}>{data.couple.bride}<em>dan</em>{data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Divider />,
          node: <Art name="boteh" />,
          amp: <Art name="boteh" />,
          closingDecor: <span aria-hidden><Art name="corner" className={s.closingCorner} /><Art name="corner" className={s.closingCorner} /></span>,
          closingEmblem: <Art name="boteh" className={s.closingBoteh} />,
          sentArt: <Art name="boteh" />,
        }}
      />
    </ThemeShell>
  );
}
