"use client";
// Theme "Cyanotype Biru" — cetak matahari cyanotype: lembar kertas berlapis biru prusia dengan tepi sapuan kuas,
// siluet putih paku-pakuan, rumput liar, dan Queen Anne's lace yang lembut di tepinya, foto duotone biru-putih,
// serta label spesimen bergaya mesin ketik.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Libre Caslon Display", "Spectral:ital,wght@0,400;0,600;1,400", "Courier Prime:wght@400;700", "Amiri:wght@400;700"];
// Painted by /tmp/pen/art/themes/cyanotype-biru.py (tools/art/themes in the repo).
const Art = makeArt("cyanotype-biru", {
  fern: [300, 853], lace: [320, 605], grass: [340, 391], sprig: [120, 153], divider: [320, 49], card: [230, 276],
} as const);

const COPY = {
  ...DEFAULT_COPY,
  opening: {
    arabic: "بِسْمِ اللّٰهِ الرَّحْمٰنِ الرَّحِيْمِ",
    kicker: "Assalamu'alaikum Warahmatullahi Wabarakatuh",
    title: "Tercetak oleh Cahaya",
    intro: "Dengan memohon rahmat dan ridha Allah SWT, kami bermaksud menyelenggarakan pernikahan putra-putri kami. Merupakan kehormatan dan kebahagiaan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"] as [string, string],
  couple: ["Dua Lembar, Satu Cahaya", "Kedua Mempelai"] as [string, string],
  count: ["Waktu Penyinaran", "Menuju Hari Bahagia"] as [string, string],
  units: ["Hari", "Jam", "Menit", "Detik"] as [string, string, string, string],
  events: ["Catatan Lapangan", "Waktu & Tempat"] as [string, string],
  story: ["Arsip Kami", "Kisah Perjalanan"] as [string, string],
  gallery: ["Cetakan Kenangan", "Galeri"] as [string, string],
  wishes: ["Doa & Kehadiran", "Ucapan & Konfirmasi"] as [string, string],
  gifts: ["Tanda Kasih", "Amplop Digital"] as [string, string],
  closing: {
    thanks: "Terima Kasih",
    text: "Kehadiran dan doa restu Bapak/Ibu/Saudara/i adalah cahaya yang membuat lembar baru kami tercetak sempurna.",
    salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh",
  },
  sent: "Terima kasih, doa dan ucapan Anda sudah tercetak di sini.",
};

export default function CyanotypeBiruTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const photo = data.gallery[0] ?? data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#eef1ee"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <span className={`${s.sheet} ${s.print}`} aria-hidden />
          <span className={s.coverLace} aria-hidden><Art name="lace" eager /></span>
          <span className={s.coverFern} aria-hidden><Art name="fern" eager /></span>
          <span className={s.coverGrass} aria-hidden><Art name="grass" eager /></span>
          <div className={s.coverInner}>
            <p className={s.coverKicker}>{label}</p>
            {photo && <div className={`${s.coverPhoto} ${s.duo}`}><Photo src={photo} alt="" /></div>}
            <h1 className={s.coverNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
            <div className={s.guestWrap}>
              <div className={s.guest}>
                <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
                <strong>{guestLabel(data)}</strong>
                {table && <span className={s.table}>{table}</span>}
              </div>
              <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#1f4a80" />Buka Undangan</button>
            </div>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#eef3f6"
        dark="#1f4a80"
        copy={COPY}
        hero={(
          <header className={s.hero}>
            {photo && (
              <div className={s.heroPrint}>
                <span className={s.print} aria-hidden />
                <div className={`${s.heroPhoto} ${s.duo}`}><Photo src={photo} alt={`${data.couple.bride} & ${data.couple.groom}`} /></div>
                <span className={s.heroSprig} aria-hidden><Art name="sprig" /></span>
              </div>
            )}
            {photo && <p className={s.heroCaption}>Cyanotype · disinari 12 menit di bawah matahari</p>}
            <p className={s.coverKicker}>{label}</p>
            <h1 className={s.coverNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="divider" className={s.divider} />,
          node: <Art name="sprig" />,
          amp: <Art name="divider" />,
          portrait: <span className={s.portraitSprig} aria-hidden><Art name="sprig" /></span>,
          countDecor: (
            <>
              <span className={`${s.countGrass} ${s.countGrassL}`} aria-hidden><Art name="grass" /></span>
              <span className={`${s.countGrass} ${s.countGrassR}`} aria-hidden><Art name="grass" /></span>
            </>
          ),
          closingDecor: (
            <>
              <span className={s.closingFern} aria-hidden><Art name="fern" /></span>
              <span className={s.closingLace} aria-hidden><Art name="lace" /></span>
            </>
          ),
          closingEmblem: <Art name="card" className={s.closingCard} />,
          sentArt: <Art name="card" />,
        }}
      />
    </ThemeShell>
  );
}
