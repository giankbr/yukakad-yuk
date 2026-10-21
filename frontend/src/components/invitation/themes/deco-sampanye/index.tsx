"use client";
// Theme "Deco Sampanye" — 1920s art deco in champagne, ivory and black: a stepped skyscraper window on letterpress
// ivory holds a pressed-foil sunburst and a painted champagne-coupe tower; black lacquer bands carry the fan scales.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, toDate, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Poiret One", "Bodoni Moda:ital,wght@0,400;0,500;0,600;1,400", "Josefin Sans:wght@400;600"];
// Painted by /tmp/pen/art/themes/deco-sampanye.py (tools/art/themes in the repo).
const Art = makeArt("deco-sampanye", { sunburst: [620, 312], coupe: [440, 325], corner: [150, 150], fan: [320, 61] } as const);

const COPY = {
  ...DEFAULT_COPY,
  attend: { maybe: "Mungkin" },
  opening: {
    kicker: "Salam Sejahtera",
    title: "Dengan Sukacita",
    intro: "Atas kasih karunia Tuhan Yang Maha Kasih, kami mengundang Bapak/Ibu/Saudara/i untuk hadir, berbagi sukacita, dan mengangkat gelas bersama kami di hari pernikahan kami.",
  },
  roles: ["The Bride", "The Groom"] as [string, string],
  couple: ["Mempelai", "Sang Pengantin"] as [string, string],
  count: ["Hitung Mundur", "Menuju Hari Bahagia"] as [string, string],
  units: ["Hari", "Jam", "Menit", "Detik"] as [string, string, string, string],
  events: ["Susunan Acara", "Waktu & Tempat"] as [string, string],
  story: ["Kisah Kami", "Sebelum Toast Ini"] as [string, string],
  gallery: ["Galeri", "Potret Kami"] as [string, string],
  wishes: ["Ucapan & Kehadiran", "Kirim Doa Restu"] as [string, string],
  gifts: ["Tanda Kasih", "Amplop Digital"] as [string, string],
  closing: { thanks: "Terima Kasih", text: "Kehadiran dan doa restu Bapak/Ibu/Saudara/i adalah hadiah terindah bagi kami. Sampai jumpa di malam toast kami." },
  sent: "Terima kasih, ucapan dan doa Anda sudah kami terima.",
};

export default function DecoSampanyeTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const photo = data.gallery[0] ?? data.couple.bridePhoto ?? data.couple.groomPhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const year = toDate(data.date)?.getFullYear();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#191613"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <span className={s.frame} aria-hidden />
          <Art name="corner" eager className={`${s.corner} ${s.cTL}`} />
          <Art name="corner" eager className={`${s.corner} ${s.cTR}`} />
          <Art name="corner" eager className={`${s.corner} ${s.cBL}`} />
          <Art name="corner" eager className={`${s.corner} ${s.cBR}`} />
          <p className={s.kicker}>The Wedding of</p>
          <h1 className={s.coverNames}><span>{data.couple.bride}</span><em><i>&amp;</i></em><span>{data.couple.groom}</span></h1>
          <p className={s.coverDate}><span aria-hidden />{formatDate(data.date)}<span aria-hidden /></p>
          <div className={s.window} aria-hidden>
            <div className={s.windowIn}>
              <Art name="sunburst" eager className={s.burst} />
              <span className={s.bubbles}><i /><i /><i /><i /><i /></span>
              <Art name="coupe" eager className={s.coupe} />
            </div>
          </div>
          <div className={s.guest}>
            <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
            <strong>{guestLabel(data)}</strong>
            {table && <span className={s.table}>{table}</span>}
          </div>
          <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={15} color="#e9d7b0" />Buka Undangan</button>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#e9d7b0"
        dark="#1a1714"
        copy={COPY}
        hero={(
          <header className={s.hero}>
            <p className={s.heroKicker}>{year ? `${label} · ${year}` : label}</p>
            <div className={s.heroStage}>
              <Art name="sunburst" className={s.heroBurst} />
              {photo && <div className={s.heroPhoto}><Photo src={photo} alt={`${data.couple.bride} & ${data.couple.groom}`} /></div>}
            </div>
            <h1 className={s.heroNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
            <Art name="fan" className={s.heroFan} />
          </header>
        )}
        slots={{
          divider: <Art name="fan" className={s.divider} />,
          amp: <Art name="fan" />,
          countDecor: <Art name="sunburst" className={s.countDeco} />,
          closingEmblem: <Art name="sunburst" className={s.closingBurst} />,
          sentArt: <Art name="coupe" />,
        }}
      />
    </ThemeShell>
  );
}
