"use client";
// Theme "Retro 70an" — gaya groovy 1970-an: pelangi matahari terbit yang dicat kuas kering (mustard, jingga, karat,
// cokelat) memeluk foto berbingkai lengkung, sinar sunburst, pita bergelombang tiga warna, bunga daisy flower-power
// yang berputar pelan, huruf bulat dengan bayangan bertumpuk, dan foto bertekstur butiran film. Untuk pasangan Muslim.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Shrikhand", "Righteous", "Figtree:ital,wght@0,400;0,600;0,700;0,800;1,400"];
// Painted by /tmp/pen/art/themes/retro-70an.py (tools/art/themes in the repo).
const Art = makeArt("retro-70an", {
  sunrise: [760, 378], daisy: [180, 174], "daisy-o": [180, 185], sun: [200, 197], divider: [260, 40],
} as const);

const COPY = {
  ...DEFAULT_COPY,
  opening: {
    arabic: "بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ",
    kicker: "Assalamu'alaikum Warahmatullahi Wabarakatuh",
    title: "Kami Menikah!",
    sub: "Dua lagu favorit akhirnya diputar dalam satu piringan.",
    intro: "Dengan memohon rahmat dan ridha Allah SWT, kami bermaksud menyelenggarakan pernikahan putra-putri kami. Merupakan kebahagiaan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
  },
  roles: ["Sang Mempelai Wanita", "Sang Mempelai Pria"] as [string, string],
  couple: ["Duet Kami", "Kedua Mempelai"] as [string, string],
  count: ["Siap-siap berdansa", "Menuju Hari H"] as [string, string],
  units: ["Hari", "Jam", "Menit", "Detik"] as [string, string, string, string],
  events: ["Catat tanggalnya", "Waktu & Tempat"] as [string, string],
  story: ["Sisi A, Lagu Kami", "Perjalanan Cinta"] as [string, string],
  gallery: ["Rol film kami", "Galeri"] as [string, string],
  wishes: ["Kirim salam", "Ucapan & Kehadiran"] as [string, string],
  gifts: ["Tanda kasih", "Amplop Digital"] as [string, string],
  closing: {
    thanks: "Terima Kasih!",
    text: "Kehadiran dan doa restu Bapak/Ibu/Saudara/i adalah lagu terindah di hari bahagia kami.",
    salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh",
  },
  sent: "Asyik! Doa dan ucapan Anda sudah terkirim. Terima kasih banyak.",
  wishPlaceholder: "Tulis doa dan ucapan untuk Laras & Bayu…",
};

export default function Retro70anTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const photo = data.gallery[0] ?? data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const copy = { ...COPY, wishPlaceholder: `Tulis doa dan ucapan untuk ${data.couple.bride} & ${data.couple.groom}…` };

  const stage = (eager: boolean, alt: string) => (
    <div className={s.stage}>
      <span className={s.sunrise} aria-hidden><Art name="sunrise" eager={eager} /></span>
      {photo
        ? <div className={`${s.coverPhoto} ${s.filmed}`}><Photo src={photo} alt={alt} /></div>
        : <span className={s.coverDaisy} style={{ left: "calc(50% - 60px)", bottom: 20, width: 120 }} aria-hidden><Art name="sun" eager={eager} /></span>}
      <span className={`${s.coverDaisy} ${s.dA}`} aria-hidden><Art name="daisy" eager={eager} /></span>
      <span className={`${s.coverDaisy} ${s.dB}`} aria-hidden><Art name="daisy-o" eager={eager} /></span>
    </div>
  );

  return (
    <ThemeShell
      fonts={FONTS}
      background="#f3e3c3"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <p className={s.kickerPill}>{label}</p>
          {stage(true, "")}
          <h1 className={s.coverNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.guestWrap}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#fbf2df" />Buka Undangan</button>
          </div>
          <span className={s.coverWave} aria-hidden />
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#fbf2df"
        dark="#5b3220"
        copy={copy}
        hero={(
          <header className={s.hero}>
            <p className={s.kickerPill}>{label}</p>
            {stage(false, `${data.couple.bride} & ${data.couple.groom}`)}
            <h1 className={s.coverNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="divider" className={s.divider} />,
          node: <Art name="sun" />,
          amp: <Art name="daisy" />,
          portrait: <span className={s.portraitDaisy} aria-hidden><Art name="daisy-o" /></span>,
          closingDecor: <span className={s.closingSun} aria-hidden><Art name="sunrise" /></span>,
          closingEmblem: <Art name="sun" className={s.closingEmblem} />,
          sentArt: <Art name="daisy" />,
        }}
      />
    </ThemeShell>
  );
}
