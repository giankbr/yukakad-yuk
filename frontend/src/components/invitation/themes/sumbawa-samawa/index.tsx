"use client";
// Theme "Sumbawa Samawa" — kain kre alang (dasar sutra marun-hitam dengan pakan tambahan benang emas: gigi pucuk rebung
// dan belah ketupat lonto engal) ditenun sampai ke benang menjadi latar sampul, pita tenun sebagai pembatas, Istana Dalam
// Loka dilukis gouache di sabana keemasan dengan biru Pulau Moyo. Bahasa bentuk: sudut terpancung (chamfer) seperti
// bidang tenun.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Libre Caslon Display", "Alegreya Sans:ital,wght@0,400;0,500;0,700;0,800;1,400", "Amiri:wght@400;700"];
// Painted by /tmp/pen/art/themes/sumbawa-samawa.py (tools/art/themes in the repo).
const Art = makeArt("sumbawa-samawa", { istana: [720, 534], band: [384, 48], medal: [160, 160] } as const);

const BISMILLAH = "بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ";

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    arabic: BISMILLAH,
    kicker: "Assalamu'alaikum Wr. Wb.",
    title: "Sabalong Samalewa",
    sub: "Membangun bersama dengan seimbang dan serasi, untuk dunia dan akhirat.",
    intro: "Dengan memohon rahmat dan ridha Allah SWT, kami bermaksud menyelenggarakan pernikahan putra-putri kami. Merupakan kehormatan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"],
  couple: ["Dengan Izin Allah", "Kedua Mempelai"],
  count: ["Helai demi Helai", "Menuju Hari Bahagia"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Waktu & Tempat", "Rangkaian Acara"],
  story: ["Tenunan Kisah", "Perjalanan Kami"],
  gallery: ["Galeri", "Potret Bahagia"],
  wishes: ["Doa & Kehadiran", "Ucapan & Konfirmasi"],
  gifts: ["Tanda Kasih", "Amplop Digital"],
  closing: { thanks: "Terima Kasih", text: "Atas kehadiran dan doa restu Bapak/Ibu/Saudara/i, kami sekeluarga mengucapkan terima kasih. Semoga Allah membalas segala kebaikan.", salam: "Wassalamu'alaikum Wr. Wb." },
  sent: "Terima kasih, doa dan ucapan Anda sudah terkirim.",
};

export default function SumbawaSamawaTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const hero = data.gallery[0] ?? data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#3a0c15"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.coverMedalWrap}><Art name="medal" eager className={s.coverMedal} /></div>
          <div className={s.coverPanel}>
            <p className={s.coverArabic} lang="ar" dir="rtl">{BISMILLAH}</p>
            <p className={s.coverKicker}>Assalamu&apos;alaikum Wr. Wb.</p>
            <p className={s.coverLabel}>Undangan {label}</p>
            <h1 className={s.coverNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
            <span className={s.coverBand} aria-hidden />
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={17} color="#f0d48a" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#f0d48a"
        dark="#6e1424"
        copy={COPY}
        hero={(
          <header className={s.hero}>
            <Art name="istana" eager className={s.heroIstana} />
            <div className={s.heroSash}>
              <p className={s.heroKicker}>Undangan {label}</p>
              <h1 className={s.heroNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
              <p className={s.heroDate}>{formatDate(data.date)}</p>
            </div>
            {hero && <div className={s.heroPhotoWrap}><div className={s.heroPhoto}><Photo src={hero} alt="" /></div></div>}
            {note && <p className={s.heroNote}>{note}</p>}
            <Art name="medal" className={s.heroMedal} />
          </header>
        )}
        slots={{
          divider: <Art name="band" className={s.divider} />,
          node: <Art name="medal" />,
          amp: <Art name="medal" />,
          closingEmblem: <Art name="medal" className={s.closingMedal} />,
          closingDecor: <Art name="istana" className={s.closingIstana} />,
          sentArt: <Art name="medal" />,
        }}
      />
    </ThemeShell>
  );
}
