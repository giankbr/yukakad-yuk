"use client";
// Theme "Taman Persia" — halaman manuskrip bergaya miniatur Persia (tanpa figur): chahar bagh dengan kanal air dan
// kolam segi delapan, cemara, pohon delima, langit lapis berawan emas, shamsa beriluminasi, dan pita kartus lapis-emas.
import { Lucide, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Gilda Display", "Cormorant Garamond:ital,wght@0,400;0,500;0,600;0,700;1,400;1,500", "Amiri"];
// Painted by /tmp/pen/art/themes/taman-persia.py (tools/art/themes in the repo).
const Art = makeArt("taman-persia", { cypress: [61, 498], garden: [640, 793], pomegranate: [320, 240], rule: [420, 46], shamsa: [240, 240] } as const);

const COPY = {
  ...DEFAULT_COPY,
  opening: {
    arabic: "بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ",
    kicker: "Assalamu'alaikum Warahmatullahi Wabarakatuh",
    title: "Undangan Pernikahan",
    intro: "Dengan memohon rahmat dan ridha Allah Subhanahu wa Ta'ala, kami bermaksud menyelenggarakan walimah pernikahan putra-putri kami. Merupakan kehormatan bagi kami atas kehadiran dan doa restu Bapak/Ibu/Saudara/i.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"] as [string, string],
  couple: ["Dua Hati, Satu Taman", "Kedua Mempelai"] as [string, string],
  count: ["Menuju Hari Bahagia", "Hitung Mundur"] as [string, string],
  units: ["Hari", "Jam", "Menit", "Detik"] as [string, string, string, string],
  events: ["Waktu & Tempat", "Rangkaian Acara"] as [string, string],
  story: ["Kisah", "Perjalanan Kami"] as [string, string],
  gallery: ["Galeri", "Momen Bahagia"] as [string, string],
  wishes: ["Doa & Kehadiran", "Ucapan & Konfirmasi"] as [string, string],
  gifts: ["Tanda Kasih", "Amplop Digital"] as [string, string],
  closing: {
    thanks: "Jazakumullah Khairan",
    text: "Kehadiran dan doa restu Bapak/Ibu/Saudara/i adalah kebahagiaan bagi kami. Semoga Allah menghimpun kita dalam kebaikan.",
    salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh",
  },
  sent: "Jazakumullah khairan, doa dan ucapan Anda sudah terkirim.",
};

export default function TamanPersiaTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Walimatul 'Ursy";
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#132560"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Art name="rule" eager className={s.coverRule} />
          <p className={s.kicker}>{label}</p>
          <div className={s.namesRow}>
            <Art name="cypress" eager />
            <h1 className={s.coverNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <Art name="cypress" eager />
          </div>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <Art name="garden" eager className={s.garden} />
          <div className={s.guestWrap}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#ecd48e" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        noPhotos
        light="#ecd48e"
        dark="#1f3a8a"
        copy={COPY}
        hero={(
          <header className={s.hero}>
            <Art name="pomegranate" className={s.heroPomL} />
            <Art name="pomegranate" className={s.heroPomR} />
            <Art name="shamsa" className={s.heroShamsa} />
            <p className={s.kickerDark}>{label}</p>
            <h1 className={s.heroNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
            <Art name="rule" className={s.heroRule} />
          </header>
        )}
        slots={{
          divider: <Art name="rule" className={s.divider} />,
          node: <Art name="shamsa" />,
          amp: <Art name="shamsa" />,
          portrait: <><Art name="cypress" /><Art name="cypress" /></>,
          closingDecor: <Art name="pomegranate" className={s.closingPom} />,
          closingEmblem: <Art name="shamsa" className={s.closingShamsa} />,
          sentArt: <Art name="shamsa" />,
        }}
      />
    </ThemeShell>
  );
}
