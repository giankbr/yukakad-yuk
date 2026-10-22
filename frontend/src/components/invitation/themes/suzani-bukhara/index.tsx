"use client";
// Theme "Suzani Bukhara" — walimah bertema sulaman suzani: setiap ornamen dilukis setingkat benang, baris demi baris
// tusuk rantai merah delima, nila dan kunyit di atas katun tenun gading. Sampul berpusat pada medali bunga besar dengan
// pita sulur di atas dan bawah, foto pembuka dijahit di jantung medali, tepi kartu memakai jahitan jelujur, dan buah
// delima sebagai lambang penutup. Tanpa ornamen makhluk hidup, basmalah sebagai teks.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Kurale", "Gentium Book Plus:ital,wght@0,400;0,700;1,400", "Amiri:wght@400;700"];
const BISMILLAH = "بِسْمِ اللّٰهِ الرَّحْمٰنِ الرَّحِيْمِ";
// Embroidered (chain stitch, thread level) by /tmp/pen/art/themes/suzani-bukhara.py (tools/art/themes in the repo).
const Art = makeArt("suzani-bukhara", { medallion: [420, 420], sprig: [90, 141], divider: [320, 40], pomegranate: [130, 147] } as const);

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    arabic: BISMILLAH,
    kicker: "Assalamu'alaikum",
    title: "Warahmatullahi Wabarakatuh",
    intro: "Dengan memohon rahmat dan ridha Allah SWT, kami bermaksud menyelenggarakan walimatul 'ursy putra-putri kami. Merupakan kehormatan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"],
  couple: ["Dua Benang, Satu Sulaman", "Kedua Mempelai"],
  count: ["Menghitung Hari", "Menuju Hari Bahagia"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Waktu & Tempat", "Akad & Resepsi"],
  story: ["Perjalanan", "Kisah Kami"],
  gallery: ["Galeri", "Momen Bahagia"],
  wishes: ["Doa & Kehadiran", "Ucapan & Konfirmasi"],
  gifts: ["Tanda Kasih", "Amplop Digital"],
  closing: { thanks: "Terima Kasih", text: "Atas kehadiran dan doa restu Bapak/Ibu/Saudara/i, kami sekeluarga mengucapkan terima kasih. Semoga Allah membalas setiap kebaikan.", salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh" },
  sent: "Jazakumullahu khairan, doa dan ucapan Anda sudah terkirim.",
};

export default function SuzaniBukharaTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Walimatul 'Ursy";
  const table = tableLabel(data.guestTable);
  const photo = data.gallery[0] ?? data.couple.bridePhoto;
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#f1e7d3"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <span className={s.vineBand} aria-hidden />
          <p className={s.coverArabic} lang="ar" dir="rtl">{BISMILLAH}</p>
          <p className={s.salam}>Assalamu&apos;alaikum Wr. Wb.</p>
          <p className={s.kicker}>Undangan {label}</p>
          <h1 className={s.coverNames}><span>{data.couple.bride}</span><em>&amp;</em><span>{data.couple.groom}</span></h1>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <Art name="medallion" className={s.medal} eager />
          <div className={s.card}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#ffffff" />Buka Undangan</button>
          </div>
          <span className={s.vineBand} aria-hidden />
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#f6dc9c"
        dark="#262f69"
        copy={COPY}
        hero={(
          <header className={s.hero}>
            <span className={s.vineBand} aria-hidden />
            <p className={s.heroKicker}>Walimatul &apos;Ursy</p>
            <h1 className={s.heroNames}>{data.couple.bride} <em>&amp;</em> {data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            <div className={s.heroMedal}>
              <Art name="medallion" />
              <div className={s.heroPhoto}>{photo ? <Photo src={photo} alt={`${data.couple.bride} & ${data.couple.groom}`} /> : <span aria-hidden>{data.couple.bride.slice(0, 1)}</span>}</div>
            </div>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="divider" className={s.divider} />,
          node: <Art name="sprig" />,
          amp: <Art name="sprig" />,
          portrait: <Art name="pomegranate" className={s.portraitArt} />,
          closingEmblem: <Art name="pomegranate" className={s.closingEmblem} />,
          sentArt: <Art name="pomegranate" />,
        }}
      />
    </ThemeShell>
  );
}
