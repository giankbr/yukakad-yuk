"use client";
// Theme "Kaca Patri" — art nouveau stained glass: hand-rolled cathedral glass in ruby, amber, cobalt and opal held by
// dark lead came, light glowing through a lancet window of whiplash lilies under a rising sun (original design).
// Vellum pages carry leaded cards with a transom of coloured panes; night-blue bands hold the lit glass.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, toDate, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Federant", "EB Garamond:ital,wght@0,400;0,500;1,400", "Marcellus SC"];
// Leaded and glazed by /tmp/pen/art/themes/kaca-patri.py (tools/art/themes in the repo).
const Art = makeArt("kaca-patri", { window: [500, 856], lunette: [420, 212], rondel: [220, 220], border: [380, 47], jewel: [56, 56] } as const);

const COPY = {
  ...DEFAULT_COPY,
  attend: { maybe: "Mungkin" },
  opening: {
    kicker: "Salam Damai dalam Kristus",
    title: "Dipersatukan dalam Kasih",
    intro: "Dengan penuh syukur atas kasih karunia Tuhan, kami mengundang Bapak/Ibu/Saudara/i untuk hadir dan mendoakan kami dalam Sakramen Perkawinan serta berbagi sukacita bersama kami.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"] as [string, string],
  couple: ["Dua Jiwa", "Mempelai"] as [string, string],
  count: ["Hitung Mundur", "Menuju Hari Kudus Kami"] as [string, string],
  units: ["Hari", "Jam", "Menit", "Detik"] as [string, string, string, string],
  events: ["Waktu & Tempat", "Rangkaian Acara"] as [string, string],
  story: ["Kisah Kami", "Panel demi Panel"] as [string, string],
  gallery: ["Galeri", "Potret dalam Cahaya"] as [string, string],
  wishes: ["Doa & Kehadiran", "Kirim Ucapan"] as [string, string],
  gifts: ["Tanda Kasih", "Amplop Digital"] as [string, string],
  closing: {
    thanks: "Terima Kasih",
    text: "Kehadiran dan doa Bapak/Ibu/Saudara/i adalah cahaya yang melengkapi hari bahagia kami.",
    salam: "Tuhan memberkati.",
  },
  sent: "Terima kasih, doa dan ucapan Anda sudah kami terima. Tuhan memberkati.",
};

export default function KacaPatriTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const photo = data.gallery[0] ?? data.couple.bridePhoto ?? data.couple.groomPhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const year = toDate(data.date)?.getFullYear();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#12141e"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <p className={s.kicker}>The Wedding of</p>
          <div className={s.windowWrap} aria-hidden>
            <Art name="window" eager className={s.windowArt} />
            <span className={s.sunbeam} />
          </div>
          <h1 className={s.coverNames}><span>{data.couple.bride}</span><em>&amp;</em><span>{data.couple.groom}</span></h1>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.guest}>
            <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
            <strong>{guestLabel(data)}</strong>
            {table && <span className={s.table}>{table}</span>}
          </div>
          <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={15} color="#26221f" />Buka Undangan</button>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#f5d993"
        dark="#26221f"
        copy={COPY}
        hero={(
          <header className={s.hero}>
            <p className={s.heroKicker}>{year ? `${label} · ${year}` : label}</p>
            <div className={s.heroFrame}>
              <Art name="lunette" className={s.heroLunette} />
              {photo && <div className={s.heroPhoto}><Photo src={photo} alt={`${data.couple.bride} & ${data.couple.groom}`} /></div>}
            </div>
            <h1 className={s.heroNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="border" className={s.divider} />,
          node: <Art name="jewel" />,
          amp: <Art name="jewel" />,
          portrait: <Art name="jewel" className={s.apex} />,
          countDecor: <Art name="lunette" className={s.lunette} />,
          closingEmblem: <Art name="rondel" className={s.rondel} />,
          sentArt: <Art name="rondel" />,
        }}
      />
    </ThemeShell>
  );
}
