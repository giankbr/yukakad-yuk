"use client";
// Theme "Origami Bangau" — kerajinan kertas: untaian senbazuru menggantung di sisi sampul, foto pada lembar kertas bersudut
// terlipat, bangau origami berbidang tajam (serat washi, lipatan, bayangan lembut), bukit kertas berlapis warna pastel.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Shippori Mincho:wght@400;600", "Zen Kaku Gothic New:wght@400;700"];
// Painted by /tmp/pen/art/themes/origami-bangau.py (tools/art/themes in the repo).
const Art = makeArt("origami-bangau", {
  "crane-blush": [240, 167], "crane-mint": [240, 167], "crane-butter": [240, 167], "crane-lilac": [240, 167],
  "string-0": [120, 1000], "string-1": [120, 992], garland: [420, 58], layers: [640, 214],
} as const);

const COPY = {
  ...DEFAULT_COPY,
  opening: {
    kicker: "Namo Buddhaya",
    title: "Seribu Bangau, Satu Harapan",
    sub: "Dengan penuh sukacita dan cinta kasih",
    intro: "Dengan memohon restu Sang Tiratana, kami bermaksud melangsungkan pemberkatan pernikahan putra-putri kami. Merupakan kebahagiaan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"] as [string, string],
  couple: ["Dua Lembar Kertas", "Kedua Mempelai"] as [string, string],
  count: ["Melipat Hari", "Menuju Hari Bahagia"] as [string, string],
  units: ["Hari", "Jam", "Menit", "Detik"] as [string, string, string, string],
  events: ["Waktu & Tempat", "Rangkaian Acara"] as [string, string],
  story: ["Lipatan demi Lipatan", "Kisah Kami"] as [string, string],
  gallery: ["Galeri", "Momen Bahagia"] as [string, string],
  wishes: ["Tulis Harapan", "Ucapan & Konfirmasi"] as [string, string],
  gifts: ["Tanda Kasih", "Amplop Digital"] as [string, string],
  closing: {
    thanks: "Terima Kasih",
    text: "Setiap doa yang Bapak/Ibu/Saudara/i titipkan akan kami simpan seperti bangau kertas: dilipat dengan hati-hati, dijaga selamanya.",
    salam: "Sabbe Satta Bhavantu Sukhitatta",
  },
  attend: { maybe: "Mungkin" },
  wishPlaceholder: "Tuliskan harapan untuk kedua mempelai…",
  sent: "Terima kasih, harapan Anda sudah kami lipat dan simpan.",
};

export default function OrigamiBangauTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const photo = data.gallery[0] ?? data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#f8f3ea"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Art name="string-0" eager className={`${s.string} ${s.stringL}`} />
          <Art name="string-1" eager className={`${s.string} ${s.stringR}`} />
          <p className={s.coverKicker}>{label}</p>
          {photo && <div className={s.photoSheet}><Photo src={photo} alt="" /></div>}
          <h1 className={s.coverNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.guestWrap}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#fff6ef" />Buka Undangan</button>
          </div>
          <Art name="layers" eager className={s.hills} />
          <Art name="crane-butter" eager className={s.coverCrane} />
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#fff6ef"
        dark="#3d3340"
        copy={COPY}
        hero={(
          <header className={s.hero}>
            <div className={s.heroCranes} aria-hidden>
              <Art name="crane-mint" />
              <Art name="crane-blush" />
              <Art name="crane-lilac" />
            </div>
            <p className={s.coverKicker}>{label}</p>
            <h1 className={s.coverNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
            {note && <p className={`${s.paperCard} ${s.heroNote}`}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="garland" className={s.divider} />,
          node: <Art name="crane-lilac" />,
          amp: <Art name="crane-butter" />,
          portrait: <Art name="crane-blush" className={s.portraitCrane} />,
          countDecor: <><Art name="crane-blush" className={`${s.countCrane} ${s.countCraneL}`} /><Art name="crane-butter" className={`${s.countCrane} ${s.countCraneR}`} /></>,
          closingDecor: <Art name="layers" className={s.closingHills} />,
          closingEmblem: <Art name="crane-blush" className={s.closingCrane} />,
          sentArt: <Art name="crane-mint" />,
        }}
      />
    </ThemeShell>
  );
}
