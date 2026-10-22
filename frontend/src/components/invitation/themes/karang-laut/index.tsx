"use client";
// Theme "Karang Laut" — taman karang bawah laut bergaya cat air: karang bercabang, karang otak, kipas laut ungu,
// rumput laut dan ikan karang kecil, gelembung yang naik, serta cahaya kaustik yang menari di air biru. Untuk pasangan
// Hindu Bali (Om Swastiastu).
import type { CSSProperties } from "react";
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,600;1,9..144,400", "Nunito Sans:wght@400;600;700;800"];
// Painted by /tmp/pen/art/themes/karang-laut.py (tools/art/themes in the repo).
const Art = makeArt("karang-laut", {
  reef: [560, 213], fan: [230, 225], brain: [150, 79], fish: [220, 88], branch: [300, 137], bubble: [96, 96],
} as const);

const BUBBLES = [
  { l: "8%", s: 10, d: 13, w: 0 }, { l: "22%", s: 16, d: 17, w: 4 }, { l: "41%", s: 8, d: 11, w: 2 }, { l: "63%", s: 14, d: 15, w: 7 },
  { l: "78%", s: 9, d: 12, w: 1 }, { l: "90%", s: 18, d: 19, w: 9 },
];

function Bubbles() {
  return (
    <span className={s.bubbles} aria-hidden>
      {BUBBLES.map(b => <i key={b.l} style={{ left: b.l, "--s": `${b.s}px`, "--d": `${b.d}s`, "--w": `-${b.w}s` } as CSSProperties} />)}
    </span>
  );
}

const COPY = {
  ...DEFAULT_COPY,
  opening: {
    kicker: "Om Swastiastu",
    title: "Tumbuh Bersama, Seperti Terumbu",
    intro: "Atas Asung Kertha Wara Nugraha Ida Sang Hyang Widhi Wasa, kami bermaksud menyelenggarakan Upacara Manusa Yadnya Pawiwahan putra-putri kami. Merupakan kebahagiaan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"] as [string, string],
  couple: ["Dua Arus, Satu Lautan", "Kedua Mempelai"] as [string, string],
  count: ["Menyelam Menuju", "Hari Bahagia"] as [string, string],
  units: ["Hari", "Jam", "Menit", "Detik"] as [string, string, string, string],
  events: ["Waktu & Tempat", "Rangkaian Acara"] as [string, string],
  story: ["Arus Kisah", "Perjalanan Kami"] as [string, string],
  gallery: ["Dari Tepi Pantai", "Galeri"] as [string, string],
  wishes: ["Doa & Kehadiran", "Ucapan & Konfirmasi"] as [string, string],
  gifts: ["Tanda Kasih", "Amplop Digital"] as [string, string],
  closing: {
    thanks: "Suksma",
    text: "Merupakan kebahagiaan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu kepada kedua mempelai.",
    salam: "Om Shanti Shanti Shanti Om",
  },
  attend: { maybe: "Mungkin" },
  sent: "Suksma, doa dan ucapan Anda sudah terkirim.",
};

export default function KarangLautTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const photo = data.gallery[0] ?? data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#eef8f6"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <span className={s.caustics} aria-hidden />
          <Bubbles />
          <span className={s.coverFish} aria-hidden><Art name="fish" eager /></span>
          <span className={s.coverFan} aria-hidden><Art name="fan" eager /></span>
          <span className={s.coverReef} aria-hidden><Art name="reef" eager /></span>
          <p className={s.coverKicker}>{label}</p>
          {photo && <div className={s.bubblePhoto}><Photo src={photo} alt="" /></div>}
          <h1 className={s.coverNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.guestWrap}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#ffffff" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#f4fbfa"
        dark="#0d3a63"
        copy={COPY}
        hero={(
          <header className={s.hero}>
            <span className={s.caustics} aria-hidden />
            <Bubbles />
            {photo && <div className={s.bubblePhoto}><Photo src={photo} alt={`${data.couple.bride} & ${data.couple.groom}`} /></div>}
            <p className={s.coverKicker}>{label}</p>
            <h1 className={s.coverNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
            <div className={s.heroReef} aria-hidden><Art name="reef" /></div>
          </header>
        )}
        slots={{
          divider: <Art name="branch" className={s.divider} />,
          node: <Art name="bubble" />,
          amp: <Art name="bubble" />,
          portrait: <span className={s.portraitCoral} aria-hidden><Art name="brain" /></span>,
          countDecor: (
            <>
              <span className={s.caustics} aria-hidden />
              <Bubbles />
              <span className={s.countFish} aria-hidden><Art name="fish" /></span>
            </>
          ),
          closingDecor: (
            <>
              <span className={s.caustics} aria-hidden />
              <Bubbles />
              <span className={s.closingFish} aria-hidden><Art name="fish" /></span>
              <span className={s.closingReef} aria-hidden><Art name="reef" /></span>
            </>
          ),
          closingEmblem: <Art name="fan" className={s.closingFan} />,
          sentArt: <Art name="fan" />,
        }}
      />
    </ThemeShell>
  );
}
