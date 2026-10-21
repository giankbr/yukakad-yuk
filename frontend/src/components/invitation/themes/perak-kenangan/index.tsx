"use client";
// Theme "Perak Kenangan" — ulang tahun pernikahan perak/emas: dinding kenangan berisi cetakan foto lama bertepi sobek
// (deckled) dengan sudut perak, untaian mawar blush & champagne dengan eukaliptus, karangan laurel perak untuk angka
// tahun, dan garis waktu dari tahun ke tahun.
import { Lucide, Photo, ThemeShell, dateParts, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["IM Fell English:ital@0;1", "Cormorant Garamond:ital,wght@0,400;0,500;0,600;0,700;1,400", "Italianno"];
// Painted by /tmp/pen/art/themes/perak-kenangan.py (wall is a CSS background)
const Art = makeArt("perak-kenangan", { frameP: [380, 480], frameL: [480, 400], garland: [780, 268], wreath: [300, 291], divider: [320, 28] } as const);

function Print({ src, kind, caption, eager }: { src?: string; kind: "P" | "L"; caption?: string; eager?: boolean }) {
  return (
    <div className={`${s.print} ${kind === "P" ? s.printP : s.printL}`}>
      <Photo src={src} alt="" className={s.ph} />
      {caption && <span className={s.cap}>{caption}</span>}
      <Art name={kind === "P" ? "frameP" : "frameL"} eager={eager} />
    </div>
  );
}

function Wreath({ years }: { years?: string }) {
  return (
    <div className={s.wreathBox}>
      <Art name="wreath" eager />
      <div className={s.wreathNum}>{years ? <><b>{years}</b><small>tahun</small></> : <small>bersama</small>}</div>
    </div>
  );
}

export default function PerakKenanganTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Ulang Tahun Pernikahan";
  const years = /(\d{1,2})\s*$|ke-?\s*(\d{1,2})/i.exec(label)?.slice(1).find(Boolean);
  const together = years ? `${years} Tahun Bersama` : "Merayakan Kebersamaan";
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const pics = [...data.gallery, data.couple.bridePhoto, data.couple.groomPhoto].filter((p): p is string => !!p);
  const pic = (i: number) => pics.length ? pics[i % pics.length] : undefined;
  // The print's handwritten caption: the original wedding date (same day and month, N years back).
  const day = dateParts(data.date);
  const caption = years && day.day ? `${day.day} ${day.month} ${Number(day.year) - Number(years)}` : undefined;

  return (
    <ThemeShell
      fonts={FONTS}
      background="#f1ece4"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Art name="garland" eager className={s.garland} />
          <Wreath years={years} />
          <div className={s.wall} aria-hidden>
            <Print src={pic(1)} kind="L" eager />
            <Print src={pic(0)} kind="P" eager />
            <Print src={pic(2)} kind="L" eager />
          </div>
          <p className={s.kicker}>{label}</p>
          <h1 className={s.coverNames}>{data.couple.bride}{data.couple.groom && <><em>&amp;</em>{data.couple.groom}</>}</h1>
          <p className={s.together}>{together}</p>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.guestWrap}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#2f3238" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#e9ecef"
        dark="#2f3238"
        copy={{
          ...DEFAULT_COPY,
          opening: {
            kicker: "Dengan Penuh Syukur",
            title: together,
            intro: "Atas karunia Tuhan Yang Maha Esa, kami merayakan perjalanan pernikahan kami. Merupakan kebahagiaan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir, berbagi cerita, dan mendoakan tahun-tahun yang akan datang.",
          },
          roles: ["Sang Istri", "Sang Suami"],
          couple: ["Masih Berdua", "Kami"],
          count: ["Menghitung Hari", "Menuju Hari Perayaan"],
          units: ["Hari", "Jam", "Menit", "Detik"],
          events: ["Waktu & Tempat", "Perayaan"],
          story: ["Dari Tahun ke Tahun", "Jejak Kenangan"],
          gallery: ["Dinding Kenangan", "Album Kami"],
          wishes: ["Doa & Kehadiran", "Ucapan & Konfirmasi"],
          gifts: ["Tanda Kasih", "Amplop Digital"],
          closing: {
            thanks: "Terima Kasih",
            text: "Terima kasih telah menjadi bagian dari perjalanan kami. Doa dan kehadiran Bapak/Ibu/Saudara/i adalah hadiah terindah di hari jadi ini.",
          },
          sent: "Terima kasih, ucapan Anda sudah kami simpan bersama kenangan lainnya.",
        }}
        hero={(
          <header className={s.hero}>
            <Art name="garland" className={s.garland} />
            <div className={s.heroWall}>
              <Print src={pic(1)} kind="P" />
              <Print src={pic(2)} kind="P" />
              <Print src={pic(0)} kind="P" caption={caption} />
            </div>
            <p className={s.heroTitle}>{together}</p>
            <h1 className={s.heroNames}>{data.couple.bride}{data.couple.groom && <><em>&amp;</em>{data.couple.groom}</>}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="divider" className={s.divider} />,
          amp: <Art name="divider" />,
          portrait: <Art name="frameP" className={s.portraitPrint} />,
          closingDecor: <Art name="garland" className={s.closingGarland} />,
          closingEmblem: <Wreath years={years} />,
          sentArt: <Art name="wreath" />,
        }}
      />
    </ThemeShell>
  );
}
