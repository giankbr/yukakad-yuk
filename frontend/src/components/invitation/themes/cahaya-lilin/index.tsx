"use client";
// Theme "Cahaya Lilin" — makan malam romantis bercahaya lilin, dilukis dengan gouache di atas latar gelap: sekelompok
// lilin pilar dengan puncak yang meleleh dan tetesan lilin (nyala apinya terpisah dan bergetar), dua gelas anggur yang
// beradu, kaki lilin kuningan, kelopak mawar, dan bokeh hangat. Sampul adalah meja makan dengan kartu tempat duduk
// bertuliskan nama tamu; hero berupa kartu menu di antara dua lilin; acara disajikan sebagai kartu menu krem; hitung
// mundur di atas empat piring saji. Untuk pasangan Katolik.
import type { CSSProperties } from "react";
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Libre Caslon Display", "Castoro:ital@0;1", "Imperial Script"];
// Painted by /tmp/pen/art/themes/cahaya-lilin.py (tools/art/themes in the repo).
const Art = makeArt("cahaya-lilin", {
  candles: [320, 380], flame: [100, 160], glasses: [280, 342], taper: [110, 369], petals: [150, 31],
} as const);
// Wick positions inside candles.webp (percent of its width / height), printed by the art script.
const WICKS = [[51.56, 33.17, 2.3], [26.56, 55.5, 2.9], [74.06, 64.17, 2.6]] as const;

const COPY = {
  ...DEFAULT_COPY,
  opening: {
    kicker: "Salam damai sejahtera",
    title: "Dalam Kasih-Nya",
    intro: "Dengan penuh syukur atas rahmat Tuhan, kami mengundang Bapak/Ibu/Saudara/i untuk hadir dan turut mendoakan Sakramen Perkawinan putra-putri kami, lalu bersantap malam bersama dalam cahaya lilin.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"] as [string, string],
  couple: ["Dua hati, satu meja", "Kedua Mempelai"] as [string, string],
  count: ["Hingga lilin dinyalakan", "Hitung Mundur"] as [string, string],
  units: ["Hari", "Jam", "Menit", "Detik"] as [string, string, string, string],
  events: ["Menu malam ini", "Rangkaian Acara"] as [string, string],
  story: ["Cerita di balik cahaya", "Kisah Kami"] as [string, string],
  gallery: ["Kenangan", "Galeri"] as [string, string],
  wishes: ["Mari bersulang", "Ucapan & Kehadiran"] as [string, string],
  gifts: ["Tanda kasih", "Amplop Digital"] as [string, string],
  closing: {
    thanks: "Terima Kasih",
    text: "Kehadiran dan doa Bapak/Ibu/Saudara/i adalah cahaya yang menghangatkan meja kami malam itu.",
    salam: "Tuhan memberkati.",
  },
  attend: { maybe: "Mungkin" },
  sent: "Terima kasih, ucapan Anda sudah kami terima. Mari bersulang!",
  wishPlaceholder: "Tuliskan doa dan ucapan untuk kedua mempelai…",
  giftIntro: "Doa dan kehadiran Anda adalah hadiah terindah. Bila berkenan memberi tanda kasih, dapat melalui:",
};

const WISHES = [
  { id: "w1", name: "Ibu Veronika & Keluarga", attendance: "yes" as const, message: "Selamat Clara dan Adrian. Semoga Tuhan memberkati rumah tangga kalian dan cinta kalian tetap menyala seperti lilin malam ini." },
  { id: "w2", name: "Paduan Suara St. Caecilia", attendance: "yes" as const, message: "Kami siap bernyanyi di misa pemberkatan! Selamat menempuh hidup baru, Tuhan Yesus memberkati." },
  { id: "w3", name: "Bram & Nadia", attendance: "maybe" as const, message: "Semoga bisa menyusul ke Lembang. Cheers untuk kalian berdua, bahagia selalu!" },
];

function Cluster({ className, eager }: { className?: string; eager?: boolean }) {
  return (
    <span className={`${s.cluster} ${className ?? ""}`} aria-hidden>
      <span className={s.glow} />
      <Art name="candles" eager={eager} />
      {WICKS.map(([x, y, d]) => (
        <span key={x} className={s.flame} style={{ "--x": `${x}%`, "--y": `${y}%`, "--d": `${d}s` } as CSSProperties}><Art name="flame" eager={eager} /></span>
      ))}
    </span>
  );
}

function Divider() {
  return <span className={s.divider} aria-hidden><i /><Art name="petals" /><i /></span>;
}

export default function CahayaLilinTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const photo = data.gallery[0] ?? data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const groom = data.couple.groom?.trim();
  const names = [data.couple.bride, groom].filter(Boolean).join(" & ");

  return (
    <ThemeShell
      fonts={FONTS}
      background="#140a09"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <p className={s.coverKicker}>Undangan {label} &amp; Jamuan Makan Malam</p>
          <h1 className={s.coverNames}>
            <span>{data.couple.bride}</span>
            {groom && <><em>&amp;</em><span>{groom}</span></>}
          </h1>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <Cluster className={s.coverCluster} eager />
          <div className={s.placeCard}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
          </div>
          <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#f3d79a" />Buka Undangan</button>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#f3d79a"
        dark="#2b1812"
        copy={COPY}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            <span className={`${s.taper} ${s.taperL}`} aria-hidden><Art name="taper" /></span>
            <span className={`${s.taper} ${s.taperR}`} aria-hidden><Art name="taper" /></span>
            <div className={s.menu}>
              <p className={s.menuKicker}>{label}</p>
              <div className={s.menuPhoto}>
                {photo ? <Photo src={photo} alt={names} /> : <span className={s.menuPhotoArt} aria-hidden><Art name="glasses" /></span>}
              </div>
              <h1 className={s.heroNames}>{data.couple.bride}{groom && <><em>&amp;</em>{groom}</>}</h1>
              <p className={s.heroDate}>{formatDate(data.date)}</p>
              {note && <><span className={s.heroRule} aria-hidden /><p className={s.heroNote}>{note}</p></>}
            </div>
          </header>
        )}
        slots={{
          divider: <Divider />,
          node: <Art name="flame" />,
          amp: <Art name="flame" />,
          portrait: <span className={s.portraitPetals} aria-hidden><Art name="petals" /></span>,
          countDecor: <Art name="glasses" className={s.countGlasses} />,
          closingDecor: <Cluster className={s.closeTable} />,
          closingEmblem: <Art name="glasses" className={s.closingEmblem} />,
          sentArt: <Art name="glasses" />,
        }}
      />
    </ThemeShell>
  );
}
