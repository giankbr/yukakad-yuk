"use client";
// Theme "Bengkulu Rafflesia" — rimba Bengkulu dalam gouache: bunga rafflesia raksasa (lima kelopak merah bata bertotol
// krem, cawan diafragma, cakram berduri) yang mekar dari lantai hutan di sampul, daun-daun hijau tua di pojok, senja
// Pantai Panjang dengan cemara laut dan rumah adat Bubungan Lima di hero dan penutup, potret bundar berbingkai "cawan".
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Gloock", "Work Sans:ital,wght@0,400;0,500;0,600;0,700;1,400", "Amiri:wght@400;700"];
// Painted by /tmp/pen/art/themes/bengkulu-rafflesia.py (tools/art/themes in the repo).
const Art = makeArt("bengkulu-rafflesia", { bloom: [620, 628], leaves: [420, 430], scene: [720, 513], vine: [380, 72] } as const);

const BISMILLAH = "بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ";

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    arabic: BISMILLAH,
    kicker: "Assalamu'alaikum Wr. Wb.",
    title: "Mekar pada Waktunya",
    sub: "Seperti rafflesia di rimba Bumi Raflesia, cinta yang dirawat dengan sabar akan mekar sempurna.",
    intro: "Dengan memohon rahmat dan ridha Allah SWT, kami bermaksud menyelenggarakan pernikahan putra-putri kami. Merupakan kehormatan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"],
  couple: ["Dengan Izin Allah", "Kedua Mempelai"],
  count: ["Menanti Senja", "Menuju Hari Bahagia"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Waktu & Tempat", "Rangkaian Acara"],
  story: ["Dari Rimba ke Pantai", "Perjalanan Kami"],
  gallery: ["Galeri", "Potret Bahagia"],
  wishes: ["Doa & Kehadiran", "Ucapan & Konfirmasi"],
  gifts: ["Tanda Kasih", "Amplop Digital"],
  closing: { thanks: "Terima Kasih", text: "Atas kehadiran dan doa restu Bapak/Ibu/Saudara/i, kami sekeluarga mengucapkan terima kasih. Semoga Allah membalas segala kebaikan.", salam: "Wassalamu'alaikum Wr. Wb." },
  sent: "Terima kasih, doa dan ucapan Anda sudah terkirim.",
};

export default function BengkuluRafflesiaTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const hero = data.gallery[0] ?? data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#17301f"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Art name="leaves" eager className={`${s.coverLeaf} ${s.coverLeafL}`} />
          <Art name="leaves" eager className={`${s.coverLeaf} ${s.coverLeafR}`} />
          <div className={s.coverText}>
            <p className={s.coverArabic} lang="ar" dir="rtl">{BISMILLAH}</p>
            <p className={s.coverKicker}>Assalamu&apos;alaikum Wr. Wb.</p>
            <p className={s.coverLabel}>Undangan {label}</p>
            <h1 className={s.coverNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
          </div>
          <div className={s.coverGuest}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={17} color="#fff7ea" />Buka Undangan</button>
          </div>
          <div className={s.coverBloomWrap}><Art name="bloom" eager className={s.coverBloom} /></div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#f5ead8"
        dark="#1f3d2a"
        copy={COPY}
        hero={(
          <header className={s.hero}>
            <Art name="scene" eager className={s.heroScene} />
            <div className={s.heroCard}>
              <p className={s.heroKicker}>Undangan {label}</p>
              <h1 className={s.heroNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
              <p className={s.heroDate}>{formatDate(data.date)}</p>
            </div>
            {hero && (
              <div className={s.heroPhotoWrap}>
                <Art name="leaves" className={`${s.heroLeaf} ${s.heroLeafL}`} />
                <Art name="leaves" className={`${s.heroLeaf} ${s.heroLeafR}`} />
                <div className={s.heroPhoto}><Photo src={hero} alt="" /></div>
              </div>
            )}
            {note && <p className={s.heroNote}>{note}</p>}
            <Art name="vine" className={s.heroVine} />
          </header>
        )}
        slots={{
          divider: <Art name="vine" className={s.divider} />,
          node: <Art name="bloom" />,
          amp: <Art name="bloom" />,
          countDecor: <Art name="bloom" className={s.countDecor} />,
          closingEmblem: <Art name="bloom" className={s.closingBloom} />,
          closingDecor: <Art name="scene" className={s.closingScene} />,
          sentArt: <Art name="bloom" />,
        }}
      />
    </ThemeShell>
  );
}
