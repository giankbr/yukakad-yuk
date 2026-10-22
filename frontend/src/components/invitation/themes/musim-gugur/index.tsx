"use client";
// Theme "Musim Gugur" — daun maple dan oak musim gugur bergaya cat air: tengah keemasan yang memerah bata ke ujung,
// urat yang tembus cahaya, ranting dengan biji ek, tumpukan daun gugur, dan daun yang berjatuhan pelan di atas kertas
// krem hangat. Nuansa rumah yang hangat untuk pasangan Katolik.
import type { CSSProperties } from "react";
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["DM Serif Display", "Lora:ital,wght@0,400;0,600;1,400", "Caveat:wght@500;600"];
// Painted by /tmp/pen/art/themes/musim-gugur.py (tools/art/themes in the repo).
const Art = makeArt("musim-gugur", {
  "maple-red": [110, 106], "maple-amber": [110, 105], "maple-gold": [110, 114], "oak-brown": [110, 169], "oak-olive": [110, 165],
  twig: [340, 227], pile: [560, 138], divider: [260, 64],
} as const);

type LeafName = "maple-red" | "maple-amber" | "maple-gold" | "oak-brown" | "oak-olive";
const LEAVES: { n: LeafName; x: string; w: number; d: number; t: number; dx: number }[] = [
  { n: "maple-red", x: "8%", w: 34, d: 15, t: 0, dx: 60 },
  { n: "oak-olive", x: "30%", w: 22, d: 19, t: 6, dx: -40 },
  { n: "maple-gold", x: "52%", w: 28, d: 17, t: 3, dx: 50 },
  { n: "maple-amber", x: "72%", w: 32, d: 14, t: 9, dx: -60 },
  { n: "oak-brown", x: "88%", w: 20, d: 21, t: 12, dx: 30 },
];

function Falling({ eager }: { eager?: boolean }) {
  return (
    <span className={s.fall} aria-hidden>
      {LEAVES.map(l => (
        <i key={l.x} style={{ "--x": l.x, "--w": `${l.w}px`, "--d": `${l.d}s`, "--t": `-${l.t}s`, "--dx": `${l.dx}px` } as CSSProperties}><Art name={l.n} eager={eager} /></i>
      ))}
    </span>
  );
}

const COPY = {
  ...DEFAULT_COPY,
  opening: {
    kicker: "Salam damai dalam Kristus",
    title: "Musim yang Baru",
    sub: "Apa yang telah dipersatukan Allah, tidak boleh diceraikan manusia (Matius 19:6)",
    intro: "Atas berkat dan kasih Tuhan, kami bermaksud menerimakan Sakramen Perkawinan putra-putri kami. Merupakan sukacita bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir, mendoakan, dan memberikan restu.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"] as [string, string],
  couple: ["Dipersatukan Tuhan", "Kedua Mempelai"] as [string, string],
  count: ["Menghitung hari", "Menuju Hari Bahagia"] as [string, string],
  units: ["hari", "jam", "menit", "detik"] as [string, string, string, string],
  events: ["Simpan tanggalnya", "Waktu & Tempat"] as [string, string],
  story: ["Dari musim ke musim", "Kisah Kami"] as [string, string],
  gallery: ["Kenangan hangat", "Galeri"] as [string, string],
  wishes: ["Doa & kehadiran", "Ucapan & Konfirmasi"] as [string, string],
  gifts: ["Tanda kasih", "Amplop Digital"] as [string, string],
  closing: {
    thanks: "Terima Kasih",
    text: "Kehadiran dan doa Bapak/Ibu/Saudara/i akan menghangatkan hari bahagia kami, seperti secangkir teh di sore yang sejuk.",
    salam: "Tuhan memberkati",
  },
  attend: { maybe: "Mungkin" },
  sent: "Terima kasih, doa dan ucapan Anda sudah terkirim. Tuhan memberkati.",
};

export default function MusimGugurTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const photo = data.gallery[0] ?? data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#f6eddc"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Falling eager />
          <span className={s.coverTwig} aria-hidden><Art name="twig" eager /></span>
          <span className={s.coverPile} aria-hidden><Art name="pile" eager /></span>
          <p className={s.coverKicker}>{label}</p>
          {photo && (
            <div className={s.coverPhoto}>
              <Photo src={photo} alt="" />
              <span className={s.coverLeaf} aria-hidden><Art name="maple-red" eager /></span>
            </div>
          )}
          <h1 className={s.coverNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.guestWrap}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#fbefd8" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#fbefd8"
        dark="#8f3a22"
        copy={COPY}
        hero={(
          <header className={s.hero}>
            <Falling />
            <span className={s.coverTwig} aria-hidden><Art name="twig" /></span>
            {photo && (
              <div className={s.coverPhoto}>
                <Photo src={photo} alt={`${data.couple.bride} & ${data.couple.groom}`} />
                <span className={s.coverLeaf} aria-hidden><Art name="maple-amber" /></span>
              </div>
            )}
            <p className={s.coverKicker}>{label}</p>
            <h1 className={s.coverNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="divider" className={s.divider} />,
          node: <Art name="maple-amber" />,
          amp: <Art name="maple-gold" />,
          portrait: <span className={s.portraitLeaf} aria-hidden><Art name="maple-red" /></span>,
          countDecor: <Falling />,
          closingDecor: (
            <>
              <Falling />
              <span className={s.closingPile} aria-hidden><Art name="pile" /></span>
            </>
          ),
          closingEmblem: <Art name="twig" className={s.closingTwig} />,
          sentArt: <Art name="twig" />,
        }}
      />
    </ThemeShell>
  );
}
