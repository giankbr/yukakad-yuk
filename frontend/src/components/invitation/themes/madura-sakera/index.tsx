"use client";
// Theme "Madura Sakera" — poster tegas merah-hitam-putih: garis baju Sakera melintang miring, batik tulis Madura
// (bunga merah-kuning di atas hitam, garis malam canting) sebagai latar, foto bergeser dengan bayangan keras, dan
// deretan rumah tanean lanjang dengan langgar saat senja.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Bebas Neue", "Lora:ital,wght@0,400;0,600;0,700;1,400"];
// Painted by /tmp/pen/art/themes/madura-sakera.py (tools/art/themes in the repo).
const Art = makeArt("madura-sakera", { flower: [260, 275], tanean: [780, 250], divider: [320, 43] } as const);

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    kicker: "Assalamu'alaikum Wr. Wb.",
    title: "Salam Taretan",
    intro: "Dengan memohon rahmat dan ridha Allah SWT, kami mengundang Bapak/Ibu/Saudara/i, para taretan sekalian, untuk hadir dan memberikan doa restu pada pernikahan putra-putri kami. Kehadiran sampeyan adalah kehormatan bagi keluarga besar kami.",
  },
  roles: ["Pangantan Bini'", "Pangantan Lake'"],
  couple: ["Pangantan", "Kedua Mempelai"],
  count: ["Hitung Mundur", "Menuju Hari H"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Waktu & Tempat", "Rangkaian Acara"],
  story: ["Perjalanan", "Kisah Kami"],
  gallery: ["Galeri", "Potret Bahagia"],
  wishes: ["Doa & Kehadiran", "Ucapan & Konfirmasi"],
  gifts: ["Tanda Kasih", "Amplop Digital"],
  closing: { thanks: "Mator Sakalangkong", text: "Atas kehadiran dan doa restu sampeyan, kami sekeluarga mengucapkan terima kasih yang sebesar-besarnya.", salam: "Wassalamu'alaikum Wr. Wb." },
  sent: "Mator sakalangkong, doa dan ucapan sampeyan sudah terkirim.",
};

export default function MaduraSakeraTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const hero = data.gallery[0] ?? data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#160d0b"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <span className={s.coverBatik} aria-hidden />
          <span className={s.coverStripe} aria-hidden />
          <div className={s.coverTop}>
            <p className={s.kicker}>Assalamu&apos;alaikum</p>
            <p className={s.coverLabel}>{label}</p>
          </div>
          {hero
            ? <div className={s.coverPhoto}><Photo src={hero} alt="" /></div>
            : <div className={s.coverFlower}><Art name="flower" eager /></div>}
          <h1 className={s.coverNames}><span>{data.couple.bride}</span><em>&amp;</em><span>{data.couple.groom}</span></h1>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.guestRow}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={18} color="#fff" />Buka Undangan</button>
          </div>
          <Art name="tanean" eager className={s.coverTanean} />
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#f8efe0"
        dark="#160d0b"
        copy={COPY}
        hero={(
          <header className={s.hero}>
            <p className={s.heroKicker}>Undangan {label}</p>
            <h1 className={s.heroNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {hero && <div className={s.heroPhoto}><Photo src={hero} alt="" /></div>}
            {note && <p className={s.heroNote}>{note}</p>}
            <Art name="tanean" className={s.heroTanean} />
          </header>
        )}
        slots={{
          divider: <Art name="divider" className={s.divider} />,
          closingEmblem: <Art name="flower" className={s.closingFlower} />,
          sentArt: <Art name="flower" />,
        }}
      />
    </ThemeShell>
  );
}
