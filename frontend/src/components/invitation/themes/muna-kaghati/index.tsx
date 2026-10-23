"use client";
// Theme "Muna Kaghati" — a bright day over Muna (Sulawesi Tenggara): the kaghati kolope, a kite of dried kolope leaves
// stitched with bamboo pins over a bamboo frame, rides the wind top-right with its line running off the page; below, the
// coral coast, karst hills and coconut palms (painted gouache). Tenun Muna weft stripes are the ribbon language: card
// selvedges, the countdown cloth, a diamond of tenun behind each round portrait. Left-aligned cover typography.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Young Serif", "Hanken Grotesk:ital,wght@0,400;0,500;0,600;0,700;0,800;1,400", "Allura", "Amiri:wght@400;700"];
// Painted by /tmp/pen/art/themes/muna-kaghati.py (tools/art/themes in the repo).
const Art = makeArt("muna-kaghati", { kite: [360, 466], coast: [780, 469], clouds: [773, 203], leaf: [110, 101], divider: [260, 24] } as const);

const BISMILLAH = "بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ";

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    arabic: BISMILLAH,
    kicker: "Assalamu'alaikum Wr. Wb.",
    title: "Mohon Doa Restu",
    intro: "Dengan memohon rahmat dan ridha Allah SWT, kami bermaksud menyelenggarakan pernikahan putra-putri kami di Raha, Bumi Sowite. Merupakan kehormatan dan kebahagiaan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"],
  couple: ["Dua Benang, Satu Layang", "Kedua Mempelai"],
  count: ["Menunggu Angin Baik", "Hitung Mundur"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Waktu & Tempat", "Rangkaian Acara"],
  story: ["Jejak Kami", "Kisah Kami"],
  gallery: ["Galeri", "Potret Kami"],
  wishes: ["Doa & Kehadiran", "Ucapan & Konfirmasi"],
  gifts: ["Tanda Kasih", "Amplop Digital"],
  closing: { thanks: "Terima Kasih", text: "Kehadiran dan doa restu Bapak/Ibu/Saudara/i adalah angin baik yang menerbangkan langkah pertama kami. Semoga Allah membalas setiap kebaikan.", salam: "Wassalamu'alaikum Wr. Wb." },
  sent: "Terima kasih, doa dan ucapan Anda sudah terkirim.",
};

export default function MunaKaghatiTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const hero = data.gallery[0] ?? data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#cfe6ea"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.sky} aria-hidden>
            <Art name="clouds" eager className={s.clouds} />
            <div className={s.kiteBox}><Art name="kite" eager /></div>
            <Art name="coast" eager className={s.coast} />
          </div>
          <p className={s.coverArabic} lang="ar" dir="rtl">{BISMILLAH}</p>
          <p className={s.coverKicker}>Assalamu&apos;alaikum Wr. Wb.</p>
          <p className={s.coverLabel}>Undangan {label}</p>
          <h1 className={s.coverNames}><span>{data.couple.bride}</span><em>&amp;</em><span>{data.couple.groom}</span></h1>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <span className={s.coverSpacer} aria-hidden />
          <div className={s.guestCard}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#fff4e2" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#fff4e2"
        dark="#6d1a2a"
        copy={COPY}
        hero={(
          <header className={s.hero}>
            <div className={s.heroKite}>
              {hero ? <div className={s.heroPhoto}><Photo src={hero} alt="" /></div> : null}
              <span className={s.heroString} aria-hidden />
            </div>
            <p className={s.heroKicker}>Undangan {label}</p>
            <h1 className={s.heroNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="divider" className={s.divider} />,
          node: <Art name="leaf" />,
          amp: <Art name="leaf" />,
          portrait: <Art name="leaf" />,
          closingDecor: <Art name="coast" className={s.closingCoast} />,
          closingEmblem: <Art name="kite" className={s.closingKite} />,
          sentArt: <Art name="kite" />,
        }}
      />
    </ThemeShell>
  );
}
