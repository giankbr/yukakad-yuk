"use client";
// Theme "Kebun Tropis" — taman tropis di siang yang cerah: rimbun daun pisang, strelitzia, kamboja, dan kembang sepatu
// bergaya gouache segar, cakram matahari yang dilukis di belakang foto bundar, kartu membulat berwarna koral-mint-kuning.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,600;1,9..144,400;1,9..144,600", "Plus Jakarta Sans:wght@400;500;600;700;800"];
// Painted by /tmp/pen/art/themes/kebun-tropis.py (tools/art/themes in the repo).
const Art = makeArt("kebun-tropis", {
  "rimbun-a": [440, 459], "rimbun-b": [440, 590], kamboja: [150, 126], sprig: [300, 54], matahari: [320, 314],
} as const);

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    arabic: "بِسْمِ اللّٰهِ الرَّحْمٰنِ الرَّحِيْمِ",
    kicker: "Assalamu'alaikum Wr. Wb.",
    title: "Dengan Penuh Syukur",
    intro: "Maha suci Allah yang menciptakan makhluk-Nya berpasang-pasangan. Dengan memohon rahmat dan ridha-Nya, kami mengundang Bapak/Ibu/Saudara/i untuk hadir di hari bahagia kami.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"],
  couple: ["Bertemu & Bertumbuh", "Kedua Mempelai"],
  count: ["Sebentar Lagi", "Menuju Hari Bahagia"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Catat Tanggalnya", "Waktu & Tempat"],
  story: ["Dari Benih", "Kisah Kami"],
  gallery: ["Galeri", "Cerah Bersama"],
  wishes: ["Doa & Kehadiran", "Ucapan & Konfirmasi"],
  gifts: ["Tanda Kasih", "Amplop Digital"],
  closing: { thanks: "Terima Kasih", text: "Atas kehadiran dan doa restu Bapak/Ibu/Saudara/i, kami ucapkan terima kasih dari lubuk hati yang paling dalam.", salam: "Wassalamu'alaikum Wr. Wb." },
  sent: "Terima kasih, doa dan ucapan Anda sudah terkirim.",
};

export default function KebunTropisTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const table = tableLabel(data.guestTable);
  const photo = data.gallery[0] ?? data.couple.bridePhoto;
  const note = data.couple.note?.trim();
  const initials = `${data.couple.bride.slice(0, 1)}${data.couple.groom.slice(0, 1)}`;

  return (
    <ThemeShell
      fonts={FONTS}
      background="#fff1d2"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Art name="rimbun-a" eager className={s.leafA} />
          <Art name="rimbun-b" eager className={s.leafB} />
          <div className={s.sunWrap}>
            <Art name="matahari" eager className={s.sun} />
            <div className={s.coverPhoto}>{photo ? <Photo src={photo} alt="" /> : <span className={s.coverMono} aria-hidden>{initials}</span>}</div>
          </div>
          <p className={s.kicker}>Undangan {label}</p>
          <h1 className={s.coverNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.guestWrap}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#fffaf0" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        copy={COPY}
        light="#ffe7a3"
        dark="#1d3b2c"
        hero={(
          <header className={s.hero}>
            <Art name="matahari" className={s.heroSun} />
            {photo && <div className={s.heroPhoto}><Photo src={photo} alt="" /></div>}
            <Art name="rimbun-a" className={s.leafA} />
            <p className={s.kickerDark}>Undangan {label}</p>
            <h1 className={s.heroNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="sprig" className={s.divider} />,
          node: <Art name="kamboja" />,
          amp: <Art name="kamboja" />,
          portrait: <Art name="kamboja" className={s.portraitKamboja} />,
          countDecor: <><Art name="rimbun-a" className={`${s.countLeaf} ${s.countLeafL}`} /><Art name="rimbun-a" className={`${s.countLeaf} ${s.countLeafR}`} /></>,
          closingDecor: <><Art name="rimbun-a" className={`${s.closingLeaf} ${s.closingLeafA}`} /><Art name="rimbun-b" className={`${s.closingLeaf} ${s.closingLeafB}`} /></>,
          closingEmblem: <Art name="matahari" className={s.closingSun} />,
          sentArt: <Art name="kamboja" />,
        }}
      />
    </ThemeShell>
  );
}
