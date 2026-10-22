"use client";
// Theme "Delft Biru" — ubin Delft biru-putih lukisan tangan dengan sentuhan warisan Hindia: foto pengantin dibingkai ubin
// berornamen sudut, deretan ubin kincir, kapal layar, dan vas tulip (kobalt di atas glasir timah retak halus), dinding ubin.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["IM Fell English:ital@0;1", "EB Garamond:ital,wght@0,400;0,600;1,400"];
// Painted by /tmp/pen/art/themes/delft-biru.py (tools/art/themes in the repo).
const Art = makeArt("delft-biru", {
  mill: [320, 320], ship: [320, 320], flower: [320, 320], border: [400, 36], vase: [300, 479],
} as const);

const COPY = {
  ...DEFAULT_COPY,
  opening: {
    kicker: "Syalom",
    title: "Dua Ubin, Satu Lukisan",
    sub: "Salam sejahtera dalam kasih Tuhan Yesus Kristus",
    intro: "Atas kasih karunia Tuhan, kami bermaksud mempersatukan putra-putri kami dalam ikatan pernikahan kudus. Merupakan sukacita bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"] as [string, string],
  couple: ["Dipertemukan Tuhan", "Kedua Mempelai"] as [string, string],
  count: ["Menghitung Hari", "Menuju Hari Bahagia"] as [string, string],
  units: ["Hari", "Jam", "Menit", "Detik"] as [string, string, string, string],
  events: ["Waktu & Tempat", "Rangkaian Acara"] as [string, string],
  story: ["Ubin demi Ubin", "Kisah Kami"] as [string, string],
  gallery: ["Galeri", "Lembar Kenangan"] as [string, string],
  wishes: ["Doa & Kehadiran", "Ucapan & Konfirmasi"] as [string, string],
  gifts: ["Tanda Kasih", "Amplop Digital"] as [string, string],
  closing: {
    thanks: "Terima Kasih",
    text: "Kehadiran dan doa restu Bapak/Ibu/Saudara/i adalah berkat yang melengkapi sukacita kami. Tuhan memberkati.",
    salam: "Soli Deo Gloria",
  },
  attend: { maybe: "Mungkin" },
  sent: "Terima kasih, doa dan ucapan Anda sudah terkirim. Tuhan memberkati.",
};

export default function DelftBiruTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const photo = data.gallery[0] ?? data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#f7f6f0"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <p className={s.coverKicker}>{label}</p>
          {photo && <div className={s.photoTile}><Photo src={photo} alt="" /></div>}
          <h1 className={s.coverNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.guestWrap}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#f7f6f0" />Buka Undangan</button>
          </div>
          <div className={s.tileRow} aria-hidden>
            <Art name="mill" eager />
            <Art name="ship" eager />
            <Art name="flower" eager />
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#f7f6f0"
        dark="#13368a"
        copy={COPY}
        hero={(
          <header className={s.hero}>
            <p className={s.coverKicker}>{label}</p>
            <h1 className={s.coverNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
            <div className={s.heroTiles} aria-hidden>
              <Art name="ship" />
              <Art name="flower" />
              <Art name="mill" />
            </div>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="border" className={s.divider} />,
          node: <Art name="flower" />,
          amp: <Art name="flower" />,
          portrait: <span className={s.portraitTile} aria-hidden />,
          countDecor: (
            <>
              <span className={`${s.countTiles} ${s.countTilesT}`} aria-hidden><Art name="mill" /><Art name="flower" /></span>
              <span className={`${s.countTiles} ${s.countTilesB}`} aria-hidden><Art name="flower" /><Art name="ship" /></span>
            </>
          ),
          closingDecor: (
            <div className={s.closingRow} aria-hidden>
              <Art name="ship" />
              <Art name="flower" />
              <Art name="mill" />
            </div>
          ),
          closingEmblem: <Art name="vase" className={s.closingVase} />,
          sentArt: <Art name="vase" />,
        }}
      />
    </ThemeShell>
  );
}
