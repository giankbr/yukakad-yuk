"use client";
// Theme "Safir Malam" — tanpa foto: langit safir yang tenang dengan sedikit bintik perak, satu roset khatam 8 sudut
// dari jalinan garis perak tipis yang berputar sangat pelan, bulan sabit perak; nama huruf kapital berjarak lebar,
// rata kiri pada satu garis perak; bingkai monogram segi delapan. Sunyi dan lapang.
import { Lucide, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Bellefair", "Crimson Pro:ital,wght@0,400;0,500;1,400", "Tenor Sans", "Amiri"];
// Painted by /tmp/pen/art/themes/safir-malam.py (tools/art/themes in the repo).
const Art = makeArt("safir-malam", {
  rosette: [520, 521], crescent: [240, 259], star: [96, 96], divider: [440, 30],
} as const);

const BISMILLAH = "بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ";

const COPY = {
  ...DEFAULT_COPY,
  opening: {
    arabic: BISMILLAH,
    kicker: "Assalamu'alaikum Warahmatullahi Wabarakatuh",
    title: "Walimatul 'Ursy",
    intro: "Dengan memohon rahmat dan ridha Allah Subhanahu wa Ta'ala, kami bermaksud menyelenggarakan pernikahan putra-putri kami. Merupakan kehormatan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"] as [string, string],
  couple: ["dengan izin Allah", "Kedua Mempelai"] as [string, string],
  count: ["menanti", "Hari yang Dijanjikan"] as [string, string],
  units: ["Hari", "Jam", "Menit", "Detik"] as [string, string, string, string],
  events: ["waktu & tempat", "Rangkaian Acara"] as [string, string],
  story: ["perjalanan", "Kisah Kami"] as [string, string],
  gallery: ["galeri", "Momen Kami"] as [string, string],
  wishes: ["doa & kehadiran", "Ucapan"] as [string, string],
  gifts: ["tanda kasih", "Amplop Digital"] as [string, string],
  closing: {
    thanks: "Jazakumullah Khairan",
    text: "Atas kehadiran dan doa restu Bapak/Ibu/Saudara/i, kami ucapkan terima kasih. Semoga Allah memberkahi kita semua dan mengumpulkan kita dalam kebaikan.",
    salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh",
  },
  sent: "Jazakumullah khairan, doa Anda sudah kami terima.",
  wishPlaceholder: "Tuliskan doa terbaik untuk kedua mempelai…",
};

export default function SafirMalamTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Walimatul 'Ursy";
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#0b1733"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Art name="rosette" eager className={s.coverRosette} />
          <Art name="crescent" eager className={s.coverMoon} />
          <div className={s.coverText}>
            <p className={s.coverArabic} lang="ar" dir="rtl">{BISMILLAH}</p>
            <p className={s.kicker}>{label}</p>
            <h1 className={s.coverNames}>{data.couple.bride}<em>dan</em>{data.couple.groom}</h1>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={15} color="currentColor" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        noPhotos
        light="#eef1f6"
        dark="#13254a"
        copy={COPY}
        hero={(
          <header className={s.hero}>
            <Art name="rosette" className={s.heroRosette} />
            <Art name="star" className={s.heroStar} />
            <p className={s.heroKicker}>{label}</p>
            <h1 className={s.heroNames}>{data.couple.bride}<em>dan</em>{data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="divider" className={s.divider} />,
          node: <Art name="star" />,
          amp: <Art name="star" />,
          portrait: <Art name="star" className={s.octStar} />,
          countDecor: <Art name="rosette" className={s.countDecor} />,
          closingEmblem: <Art name="crescent" className={s.closingMoon} />,
          sentArt: <Art name="star" />,
        }}
      />
    </ThemeShell>
  );
}
