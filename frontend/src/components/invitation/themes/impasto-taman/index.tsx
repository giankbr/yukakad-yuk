"use client";
// Theme "Impasto Taman" — an impressionist garden in thick oil impasto (lily pond, rose banks, dappled light), hung as a
// painting in a gilt frame on a sage gallery wall with a museum placard; painted gilt frames around every photo,
// palette-knife dividers, water-lily nodes. Christian demo couple (salam damai sejahtera).
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, toDate, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Instrument Serif:ital@0;1", "Spectral:ital,wght@0,400;0,600;1,400", "Monsieur La Doulaise"];
// Painted by /tmp/pen/art/themes/impasto-taman.py (tools/art/themes in the repo).
const Art = makeArt("impasto-taman", { roses: [520, 322], lily: [180, 111], stroke: [360, 39] } as const);

const COPY = {
  ...DEFAULT_COPY,
  opening: {
    kicker: "Salam Damai Sejahtera",
    title: "Dengan Penuh Sukacita",
    intro: "Atas berkat dan kasih karunia Tuhan, kami bermaksud meneguhkan janji pernikahan kami di hadapan-Nya. Merupakan sukacita bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir, mendoakan, dan ikut merayakan di taman.",
  },
  attend: { maybe: "Mungkin" },
  roles: ["Mempelai Wanita", "Mempelai Pria"] as [string, string],
  couple: ["Dua Potret", "Kedua Mempelai"] as [string, string],
  count: ["Cat Hampir Kering", "Menuju Hari Bahagia"] as [string, string],
  units: ["Hari", "Jam", "Menit", "Detik"] as [string, string, string, string],
  events: ["Waktu & Tempat", "Rangkaian Acara"] as [string, string],
  story: ["Sketsa Perjalanan", "Kisah Kami"] as [string, string],
  gallery: ["Ruang Pamer", "Galeri Kami"] as [string, string],
  wishes: ["Buku Tamu", "Ucapan & Kehadiran"] as [string, string],
  gifts: ["Tanda Kasih", "Amplop Digital"] as [string, string],
  closing: {
    thanks: "Terima kasih",
    text: "Kehadiran dan doa Bapak/Ibu/Saudara/i adalah warna terindah di kanvas hari bahagia kami. Tuhan memberkati.",
  },
  sent: "Terima kasih, ucapan Anda sudah tergantung di dinding galeri kami.",
  wishPlaceholder: "Tuliskan doa dan ucapan untuk kedua mempelai…",
};

export default function ImpastoTamanTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const photo = data.gallery[0] ?? data.couple.bridePhoto ?? data.couple.groomPhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const year = toDate(data.date)?.getFullYear();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#d9dccb"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <span className={s.hook} aria-hidden />
          <div className={s.painting} aria-hidden>
            <div className={s.paintingInner}><span className={s.scene} /><span className={s.dapple} /></div>
          </div>
          <div className={s.placard}>
            <p className={s.kicker}>Undangan {label}</p>
            <h1 className={s.coverNames}>{data.couple.bride} <em>&amp;</em> {data.couple.groom}</h1>
            <p className={s.medium}>Cat minyak di atas kanvas{year ? `, ${year}` : ""}</p>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
          </div>
          <div className={s.guest}>
            <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
            <strong>{guestLabel(data)}</strong>
            {table && <span className={s.table}>{table}</span>}
          </div>
          <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#fbf8f1" />Buka Undangan</button>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#fbf8f1"
        dark="#264a3c"
        copy={COPY}
        hero={(
          <header className={s.hero}>
            <p className={s.heroKicker}>{year ? `${label} · ${year}` : label}</p>
            <h1 className={s.heroNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <Art name="stroke" className={s.divider} />
            {photo && (
              <div className={s.heroArt}>
                <div className={s.heroFrame}><Photo src={photo} alt={`${data.couple.bride} & ${data.couple.groom}`} /></div>
                <Art name="roses" className={s.heroRoses} />
                <Art name="lily" className={s.heroLily} />
              </div>
            )}
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="stroke" className={s.divider} />,
          node: <Art name="lily" />,
          amp: <Art name="lily" />,
          portrait: <Art name="roses" className={s.portraitRoses} />,
          countDecor: <span className={s.countScene} aria-hidden />,
          closingDecor: <span className={s.closingScene} aria-hidden />,
          closingEmblem: <Art name="roses" className={s.closingRoses} />,
          sentArt: <Art name="lily" />,
        }}
      />
    </ThemeShell>
  );
}
