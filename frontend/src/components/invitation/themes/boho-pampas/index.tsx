"use client";
// Theme "Boho Pampas" — bohemian neutrals on oat linen: dry-brushed pampas plumes sway beside a rattan hoop arch with a
// cotton macramé swag, bunny tails and dried palm spears; portraits are arch doors set beside their names, and cocoa
// bands hang under a knotted macramé fringe.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, toDate, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,500;1,9..144,400", "Jost:wght@400;500", "Homemade Apple"];
// Painted by /tmp/pen/art/themes/boho-pampas.py (tools/art/themes in the repo).
const Art = makeArt("boho-pampas", { arch: [700, 633], plume: [170, 800], sprig: [360, 61], tail: [55, 212], fringe: [450, 44] } as const);

const COPY = {
  ...DEFAULT_COPY,
  attend: { maybe: "Mungkin" },
  opening: {
    kicker: "Salam Pembuka",
    title: "Om Swastyastu",
    intro: "Atas Asung Kertha Wara Nugraha Ida Sang Hyang Widhi Wasa, kami bermaksud mengundang Bapak/Ibu/Saudara/i untuk hadir dan memberikan doa restu pada upacara pawiwahan putra-putri kami.",
  },
  roles: ["Sang Mempelai Wanita", "Sang Mempelai Pria"] as [string, string],
  couple: ["Dua Hati", "Mempelai"] as [string, string],
  count: ["Menghitung Hari", "Menuju Senja Kami"] as [string, string],
  units: ["Hari", "Jam", "Menit", "Detik"] as [string, string, string, string],
  events: ["Waktu & Tempat", "Rangkaian Acara"] as [string, string],
  story: ["Perjalanan", "Kisah Kami"] as [string, string],
  gallery: ["Galeri", "Potret di Tepi Tebing"] as [string, string],
  wishes: ["Doa & Kehadiran", "Kirim Ucapan"] as [string, string],
  gifts: ["Tanda Kasih", "Amplop Digital"] as [string, string],
  closing: {
    thanks: "Suksma",
    text: "Merupakan kebahagiaan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu. Atas kehadiran dan doanya, kami ucapkan terima kasih.",
    salam: "Om Shanti Shanti Shanti Om",
  },
  sent: "Suksma, doa dan ucapan Anda sudah kami terima.",
  wishPlaceholder: "Tuliskan doa dan harapan untuk kedua mempelai…",
};

export default function BohoPampasTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const photo = data.gallery[0] ?? data.couple.bridePhoto ?? data.couple.groomPhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const year = toDate(data.date)?.getFullYear();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#e6dac8"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Art name="plume" eager className={`${s.plume} ${s.plumeL}`} />
          <Art name="plume" eager className={`${s.plume} ${s.plumeR}`} />
          <p className={s.kicker}>The Wedding of</p>
          <div className={s.stage} aria-hidden>
            <div className={s.archPhoto}>{photo ? <Photo src={photo} alt="" /> : <div />}</div>
            <Art name="arch" eager className={s.archArt} />
          </div>
          <h1 className={s.coverNames}><span>{data.couple.bride}</span><em>&amp;</em><span>{data.couple.groom}</span></h1>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.guest}>
            <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
            <strong>{guestLabel(data)}</strong>
            {table && <span className={s.table}>{table}</span>}
          </div>
          <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={15} color="#f3e4cb" />Buka Undangan</button>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#f3e4cb"
        dark="#46372b"
        copy={COPY}
        hero={(
          <header className={s.hero}>
            <p className={s.heroKicker}>{year ? `${label} · ${year}` : label}</p>
            <div className={s.heroFrame}>
              {photo && <div className={s.heroPhoto}><Photo src={photo} alt={`${data.couple.bride} & ${data.couple.groom}`} /></div>}
              <Art name="plume" className={`${s.heroPlume} ${s.heroPlumeL}`} />
              <Art name="plume" className={`${s.heroPlume} ${s.heroPlumeR}`} />
            </div>
            <h1 className={s.heroNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="sprig" className={s.divider} />,
          node: <Art name="tail" />,
          amp: <Art name="sprig" />,
          portrait: <Art name="tail" className={s.tailArt} />,
          countDecor: <Art name="fringe" className={s.fringe} />,
          closingDecor: (<><Art name="fringe" className={s.fringe} /><Art name="plume" className={s.closeLeft} /><Art name="plume" className={s.closeRight} /></>),
          sentArt: <Art name="tail" />,
        }}
      />
    </ThemeShell>
  );
}
