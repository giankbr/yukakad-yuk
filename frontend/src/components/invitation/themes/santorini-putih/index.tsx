"use client";
// Theme "Santorini Putih" — sunny gouache Cyclades: whitewashed cubic houses stacked on a caldera cliff, cobalt domes
// and doors, magenta bougainvillea spilling over a white terrace wall above a sparkling Aegean (original design, no
// landmarks or religious symbols). Crisp white pages, cube cards with cobalt dome caps and door-shaped gift cards.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, toDate, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Gilda Display", "Karla:ital,wght@0,400;0,500;0,700;1,400", "Josefin Sans:wght@400;600"];
// Painted by /tmp/pen/art/themes/santorini-putih.py (tools/art/themes in the repo).
const Art = makeArt("santorini-putih", { village: [780, 911], bougain: [440, 392], sprig: [340, 37], bloom: [80, 68], domes: [280, 215] } as const);

const COPY = {
  ...DEFAULT_COPY,
  attend: { maybe: "Mungkin" },
  opening: {
    kicker: "Salam Damai",
    title: "Om Swastyastu",
    intro: "Atas Asung Kertha Wara Nugraha Ida Sang Hyang Widhi Wasa, kami bermaksud mengundang Bapak/Ibu/Saudara/i pada upacara pawiwahan putra-putri kami. Merupakan kebahagiaan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"] as [string, string],
  couple: ["Dua Hati, Satu Dermaga", "Mempelai"] as [string, string],
  count: ["Menghitung Ombak", "Menuju Hari Bahagia"] as [string, string],
  units: ["Hari", "Jam", "Menit", "Detik"] as [string, string, string, string],
  events: ["Waktu & Tempat", "Rangkaian Acara"] as [string, string],
  story: ["Perjalanan Kami", "Kisah di Tepi Laut"] as [string, string],
  gallery: ["Galeri", "Putih, Biru, dan Kita"] as [string, string],
  wishes: ["Doa & Kehadiran", "Kirim Ucapan"] as [string, string],
  gifts: ["Tanda Kasih", "Amplop Digital"] as [string, string],
  closing: {
    thanks: "Suksma",
    text: "Merupakan kebahagiaan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
    salam: "Om Shanti Shanti Shanti Om",
  },
  sent: "Suksma, doa dan ucapan Anda sudah kami terima.",
  wishPlaceholder: "Tuliskan doa restu untuk kedua mempelai…",
};

export default function SantoriniPutihTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const photo = data.gallery[0] ?? data.couple.bridePhoto ?? data.couple.groomPhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const year = toDate(data.date)?.getFullYear();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#dfe9f5"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.scene} aria-hidden>
            <Art name="village" eager className={s.sceneArt} />
          </div>
          <div className={s.coverBody}>
            <p className={s.kicker}>The Wedding of</p>
            <h1 className={s.coverNames}><span>{data.couple.bride}</span><em>&amp;</em><span>{data.couple.groom}</span></h1>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={15} color="#ffffff" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#ffffff"
        dark="#1f4fa8"
        copy={COPY}
        hero={(
          <header className={s.hero}>
            <p className={s.heroKicker}>{year ? `${label} · ${year}` : label}</p>
            <div className={s.heroWall}>
              {photo && <div className={s.heroPhoto}><Photo src={photo} alt={`${data.couple.bride} & ${data.couple.groom}`} /></div>}
              <span className={s.step2} aria-hidden />
              <Art name="bougain" className={s.heroBougain} />
            </div>
            <h1 className={s.heroNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="sprig" className={s.divider} />,
          node: <Art name="bloom" />,
          amp: <Art name="bloom" />,
          portrait: <Art name="bloom" className={s.bloomCap} />,
          closingEmblem: <Art name="domes" className={s.domesEmblem} />,
          sentArt: <Art name="domes" />,
        }}
      />
    </ThemeShell>
  );
}
