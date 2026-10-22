"use client";
// Theme "Gurun Kaktus" — boho gurun dengan cat gouache kuas kering: langit senja yang dilukis, mesa berlapis dan bukit
// pasir tempat foto pasangan tenggelam seperti matahari, saguaro berusuk dengan duri, kaktus pir berbuah merah, dan
// sukulen echeveria; terakota, pasir, dan hijau sage. Untuk pasangan Hindu Bali (pawiwahan).
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Gloock", "Literata:ital,wght@0,400;0,600;1,400", "Mea Culpa"];
// Painted by /tmp/pen/art/themes/gurun-kaktus.py (tools/art/themes in the repo).
const Art = makeArt("gurun-kaktus", {
  land: [780, 600], saguaro: [150, 391], pear: [180, 237], succulent: [130, 73], dunes: [860, 186], divider: [240, 44],
} as const);

const COPY = {
  ...DEFAULT_COPY,
  opening: {
    kicker: "Om Swastyastu",
    title: "Atas Asung Kertha Wara Nugraha",
    sub: "Ida Sang Hyang Widhi Wasa / Tuhan Yang Maha Esa",
    intro: "Kami bermaksud menyelenggarakan upacara pawiwahan putra-putri kami. Merupakan suatu kehormatan dan kebahagiaan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"] as [string, string],
  couple: ["Dua hati, satu taman", "Kedua Mempelai"] as [string, string],
  count: ["Menuju senja kami", "Hitung Mundur"] as [string, string],
  units: ["Hari", "Jam", "Menit", "Detik"] as [string, string, string, string],
  events: ["Waktu & tempat", "Rangkaian Acara"] as [string, string],
  story: ["Tumbuh pelan", "Kisah Kami"] as [string, string],
  gallery: ["Senja-senja kami", "Galeri"] as [string, string],
  wishes: ["Doa & restu", "Ucapan & Kehadiran"] as [string, string],
  gifts: ["Tanda kasih", "Amplop Digital"] as [string, string],
  closing: {
    thanks: "Suksma",
    text: "Merupakan kebahagiaan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
    salam: "Om Shanti Shanti Shanti Om",
  },
  attend: { maybe: "Mungkin" },
  sent: "Suksma, doa dan ucapan Anda sudah terkirim.",
};

export default function GurunKaktusTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const photo = data.gallery[0] ?? data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  const scene = (eager: boolean, alt: string) => (
    <div className={s.scene}>
      <p className={s.sceneKicker}>{label}</p>
      {photo ? <div className={s.sunPhoto}><Photo src={photo} alt={alt} /></div> : <span className={s.sunBlank} aria-hidden />}
      <span className={s.land} aria-hidden><Art name="land" eager={eager} /></span>
    </div>
  );

  return (
    <ThemeShell
      fonts={FONTS}
      background="#efd6b5"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          {scene(true, "")}
          <h1 className={s.coverNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.guestWrap}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#fbf1e2" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#fbf1e2"
        dark="#b5532f"
        copy={COPY}
        hero={(
          <header className={s.hero}>
            {scene(false, `${data.couple.bride} & ${data.couple.groom}`)}
            <h1 className={s.coverNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="divider" className={s.divider} />,
          node: <Art name="succulent" />,
          amp: <Art name="succulent" />,
          portrait: <span className={s.portraitCactus} aria-hidden><Art name="pear" /></span>,
          countDecor: (
            <>
              <span className={`${s.countSag} ${s.sL}`} aria-hidden><Art name="saguaro" /></span>
              <span className={`${s.countSag} ${s.sR}`} aria-hidden><Art name="saguaro" /></span>
              <span className={s.countDunes} aria-hidden><Art name="dunes" /></span>
            </>
          ),
          closingDecor: <span className={s.closingLand} aria-hidden><Art name="land" /></span>,
          closingEmblem: <Art name="succulent" className={s.closingEmblem} />,
          sentArt: <Art name="pear" />,
        }}
      />
    </ThemeShell>
  );
}
