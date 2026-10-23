"use client";
// Theme "Kristal Es" — pernikahan musim dingin di balik jendela berembun: bunga es tumbuh dari keempat sudut kaca,
// sebatang ranting bersalju melintang di atas, salju turun pelan di luar, dan nama berada di lingkar kaca yang
// dihangatkan napas. Bingkai foto dan hitung mundur berbentuk kristal heksagonal; perak-biru dan putih es.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Tenor Sans", "Spectral:ital,wght@0,400;0,500;0,600;1,400;1,500"];
// Painted by /tmp/pen/art/themes/kristal-es.py (pane.webp and snow.webp are CSS backgrounds).
const Art = makeArt("kristal-es", { frost: [420, 378], branch: [760, 189], flake: [240, 263], flake2: [130, 130], flake3: [120, 131] } as const);

const COPY = {
  ...DEFAULT_COPY,
  opening: {
    kicker: "Dengan penuh sukacita",
    title: "Undangan Pernikahan",
    sub: "Di musim yang paling sejuk, kami memilih untuk saling menghangatkan.",
    intro: "Dengan penuh syukur kami mengundang Bapak/Ibu/Saudara/i untuk hadir dan menjadi bagian dari hari bahagia kami. Kehadiran Anda adalah kehangatan terindah di tengah udara yang dingin.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"] as [string, string],
  couple: ["Dua hati", "Kedua Mempelai"] as [string, string],
  count: ["Menuju hari kami", "Hitung Mundur"] as [string, string],
  units: ["Hari", "Jam", "Menit", "Detik"] as [string, string, string, string],
  events: ["Waktu & tempat", "Rangkaian Acara"] as [string, string],
  story: ["Dari salju pertama", "Kisah Kami"] as [string, string],
  gallery: ["Potret", "Galeri"] as [string, string],
  wishes: ["Ucapan & kehadiran", "Kirim Ucapan"] as [string, string],
  gifts: ["Tanda kasih", "Hadiah"] as [string, string],
  closing: {
    thanks: "Terima Kasih",
    text: "Terima kasih atas doa dan kehadiran Bapak/Ibu/Saudara/i. Sampai jumpa di hari kami, bawalah jaket dan senyum yang hangat.",
  },
  sent: "Terima kasih, ucapan hangat Anda sudah terkirim.",
  attend: { maybe: "Mungkin" },
  wishPlaceholder: "Tuliskan ucapan dan doa untuk kedua mempelai…",
  familyLabel: "Kami yang berbahagia",
};

const WISHES = [
  { id: "w1", name: "Keluarga Gunadi", attendance: "yes" as const, message: "Selamat Kirana dan Elvan! Semoga cinta kalian selalu hangat, seperti teh jahe di halte Sapporo itu." },
  { id: "w2", name: "Teman PPI Hokkaido", attendance: "yes" as const, message: "Dari badai salju ke pelaminan. Ikut bahagia, kami sudah siapkan jaket tebal untuk ke Lembang!" },
  { id: "w3", name: "Tante Lies & Om Benny", attendance: "maybe" as const, message: "Semoga dimudahkan semuanya. Doa terbaik dari kami untuk keluarga baru kalian." },
];

export default function KristalEsTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const photo = data.gallery[0] ?? data.couple.bridePhoto;

  return (
    <ThemeShell
      fonts={FONTS}
      background="#eef3f7"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <span className={s.snow2} aria-hidden />
          <Art name="frost" eager className={`${s.frost} ${s.frostTL}`} />
          <Art name="frost" eager className={`${s.frost} ${s.frostTR}`} />
          <Art name="frost" eager className={`${s.frost} ${s.frostBL}`} />
          <Art name="frost" eager className={`${s.frost} ${s.frostBR}`} />
          <Art name="branch" eager className={s.branch} />
          <span className={s.snow} aria-hidden />
          <div className={s.breath}>
            <Art name="flake2" eager className={s.coverFlake} />
            <p className={s.kicker}>{label}</p>
            <h1 className={s.coverNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
            <span className={s.coverRule} aria-hidden />
            <div className={s.guestWrap}>
              <div className={s.guest}>
                <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
                <strong>{guestLabel(data)}</strong>
                {table && <span className={s.table}>{table}</span>}
              </div>
              <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#f3f8fc" />Buka Undangan</button>
            </div>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#f3f8fc"
        dark="#23405e"
        copy={COPY}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            <Art name="branch" className={s.heroBranch} />
            {photo ? <div className={s.heroPhoto}><Photo src={photo} alt="" /></div> : <Art name="flake" className={s.heroFlake} />}
            <p className={s.kickerDark}>{label}</p>
            <h1 className={s.heroNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="flake3" className={s.divider} />,
          node: <Art name="flake2" />,
          amp: <Art name="flake3" />,
          portrait: <Art name="flake2" />,
          countDecor: <><span className={s.snow2} aria-hidden /><span className={s.snow} aria-hidden /></>,
          closingEmblem: <><Art name="branch" className={s.closingBranch} /><Art name="flake" className={s.closingFlake} /></>,
          sentArt: <Art name="flake" />,
        }}
      />
    </ThemeShell>
  );
}
