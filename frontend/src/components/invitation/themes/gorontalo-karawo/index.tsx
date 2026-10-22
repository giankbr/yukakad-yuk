"use client";
// Theme "Gorontalo Karawo" — lila, mint, dan krem: sulaman kerawang karawo yang dilukis benang demi benang (kisi
// benang tercabut, sulaman terhitung membentuk bunga), jahitan putus-putus sebagai bahasa garis, dan rumah adat
// Dulohupa dalam cat air. Sampul: foto di balik bingkai kain karawo berjendela lengkung.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Allura", "Gilda Display", "Nunito Sans:ital,wght@0,400;0,600;0,700;0,800;1,400", "Amiri:wght@400;700"];
// Painted by /tmp/pen/art/themes/gorontalo-karawo.py (tools/art/themes in the repo).
const Art = makeArt("gorontalo-karawo", { frame: [432, 522], divider: [264, 72], dulohupa: [820, 508] } as const);

const BISMILLAH = "بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ";

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    arabic: BISMILLAH,
    kicker: "Assalamu'alaikum Wr. Wb.",
    title: "Mohon Doa Restu",
    intro: "Dengan memohon rahmat dan ridha Allah SWT, kami bermaksud menyelenggarakan pernikahan putra-putri kami. Merupakan kehormatan dan kebahagiaan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"],
  couple: ["Dengan Izin Allah", "Kedua Mempelai"],
  count: ["Menuju Hari Bahagia", "Hitung Mundur"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Waktu & Tempat", "Rangkaian Acara"],
  story: ["Sulaman Kisah", "Perjalanan Kami"],
  gallery: ["Galeri", "Potret Kami"],
  wishes: ["Doa & Kehadiran", "Ucapan & Konfirmasi"],
  gifts: ["Tanda Kasih", "Amplop Digital"],
  closing: { thanks: "Odu Olo", text: "Terima kasih atas kehadiran dan doa restu Bapak/Ibu/Saudara/i. Semoga Allah membalas kebaikan dengan keberkahan.", salam: "Wassalamu'alaikum Wr. Wb." },
  sent: "Odu olo, doa dan ucapan Anda sudah terkirim.",
};

export default function GorontaloKarawoTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const hero = data.gallery[0] ?? data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#f1e8f4"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <p className={s.coverArabic} lang="ar" dir="rtl">{BISMILLAH}</p>
          <p className={s.coverKicker}>Assalamu&apos;alaikum Wr. Wb.</p>
          <div className={s.coverFrame}>
            {hero ? <div className={s.coverPhoto}><Photo src={hero} alt="" /></div> : <span className={s.coverEmpty} aria-hidden />}
            <Art name="frame" eager />
          </div>
          <p className={s.coverLabel}>Undangan {label}</p>
          <h1 className={s.coverNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.guestCard}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={17} color="#fff" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#fffaf3"
        dark="#3f3150"
        copy={COPY}
        hero={(
          <header className={s.hero}>
            <Art name="dulohupa" className={s.heroHouse} />
            <p className={s.heroKicker}>Undangan {label}</p>
            <h1 className={s.heroNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="divider" className={s.divider} />,
          closingEmblem: <Art name="divider" className={s.closingMotif} />,
          sentArt: <Art name="divider" />,
        }}
      />
    </ThemeShell>
  );
}
