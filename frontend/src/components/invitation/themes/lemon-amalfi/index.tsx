"use client";
// Theme "Lemon Amalfi" — sunny watercolour of a cliffside village (pastel houses, a maiolica-tiled dome, lemon terraces,
// turquoise sea) seen through a white arched window set into a wall of hand-painted blue-yellow maiolica tiles; lemon
// branches sway over the frames, portraits sit on ceramic plates, countdown digits on little plates, maiolica bands on
// every card. Catholic couple from Flores & Manado (Salam damai Kristus, Sakramen Perkawinan).
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, toDate, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,500;0,9..144,600;1,9..144,400;1,9..144,500", "Figtree:wght@400;500;600;700;800"];
// Painted by /tmp/pen/art/themes/lemon-amalfi.py (tools/art/themes in the repo).
const Art = makeArt("lemon-amalfi", { lemons: [480, 305], lemon: [150, 146], band: [240, 64] } as const);

const COPY = {
  ...DEFAULT_COPY,
  opening: {
    kicker: "Salam Damai dalam Kristus",
    title: "Dengan Penuh Sukacita",
    intro: "Atas berkat dan rahmat Tuhan, kami bermaksud menerimakan Sakramen Perkawinan. Merupakan sukacita bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir, mendoakan, dan merayakan bersama kami di tepi laut.",
  },
  attend: { maybe: "Mungkin" },
  roles: ["Mempelai Wanita", "Mempelai Pria"] as [string, string],
  couple: ["Sepasang Lemon", "Kedua Mempelai"] as [string, string],
  count: ["Di Bawah Matahari", "Menuju Hari Bahagia"] as [string, string],
  units: ["Hari", "Jam", "Menit", "Detik"] as [string, string, string, string],
  events: ["Waktu & Tempat", "Rangkaian Acara"] as [string, string],
  story: ["Dari Pelabuhan", "Kisah Kami"] as [string, string],
  gallery: ["Album Musim Panas", "Galeri"] as [string, string],
  wishes: ["Kartu Ucapan", "Ucapan & Kehadiran"] as [string, string],
  gifts: ["Tanda Kasih", "Amplop Digital"] as [string, string],
  closing: {
    thanks: "Grazie!",
    text: "Terima kasih atas kehadiran dan doa Bapak/Ibu/Saudara/i. Sampai jumpa di tebing, di bawah pohon-pohon lemon.",
    salam: "Tuhan memberkati",
  },
  sent: "Terima kasih, ucapan Anda sudah kami terima dengan sukacita.",
  wishPlaceholder: "Tuliskan doa dan ucapan untuk kedua mempelai…",
};

const WISHES = [
  { id: "w1", name: "Keluarga Bapak Petrus Seda", attendance: "yes" as const, message: "Selamat menerimakan Sakramen Perkawinan. Tuhan memberkati rumah tangga kalian dengan damai dan sukacita." },
  { id: "w2", name: "Tim Kapal Wisata Komodo", attendance: "yes" as const, message: "Akhirnya topi jerami itu kembali ke pemiliknya, plus bonus suami! Proficiat Gaby & Rafa!" },
  { id: "w3", name: "Opa & Oma Lumentut", attendance: "maybe" as const, message: "Torang doakan dari Manado. Semoga langgeng dan diberkati selalu." },
];

export default function LemonAmalfiTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const photo = data.gallery[0] ?? data.couple.bridePhoto ?? data.couple.groomPhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const year = toDate(data.date)?.getFullYear();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#e9eef6"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.panel}>
            <div className={s.coast} aria-hidden><span /></div>
            <span className={s.bandStrip} aria-hidden />
            <Art name="lemons" className={s.coverBranch} eager />
            <p className={s.kicker}>{label}</p>
            <h1 className={s.coverNames}>{data.couple.bride} <em>&amp;</em> {data.couple.groom}</h1>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#163c79" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#ffffff"
        dark="#163c79"
        copy={COPY}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            <Art name="lemons" className={s.heroBranch} />
            <p className={s.heroKicker}>{year ? `${label} · ${year}` : label}</p>
            <h1 className={s.heroNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <Art name="band" className={s.divider} />
            {photo && (
              <div className={s.heroArt}>
                <div className={s.heroFrame}><Photo src={photo} alt={`${data.couple.bride} & ${data.couple.groom}`} /></div>
                <span className={s.heroBand} aria-hidden />
                <Art name="lemon" className={s.heroLemon} />
              </div>
            )}
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="band" className={s.divider} />,
          node: <Art name="lemon" />,
          amp: <Art name="lemon" />,
          portrait: <Art name="lemon" className={s.portraitLemon} />,
          closingDecor: <Art name="lemons" className={s.closingBranch} />,
          sentArt: <Art name="lemon" />,
        }}
      />
    </ThemeShell>
  );
}
