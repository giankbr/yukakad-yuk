"use client";
// Theme "Oasis Kurma" — oasis di siang yang terang, dilukis gouache: langit biru pucat, bukit pasir aprikot, kolam toska
// yang memantulkan kebun kurma, dan pohon kurma dengan tandan buah keemasan di depan foto pengantin.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Yeseva One", "Karla:ital,wght@0,400;0,500;0,700;1,400", "Amiri"];
// Painted by /tmp/pen/art/themes/oasis-kurma.py (tools/art/themes in the repo).
const Art = makeArt("oasis-kurma", { palm: [300, 801], dates: [180, 153], sprig: [440, 87], dune: [640, 176] } as const);

const COPY = {
  ...DEFAULT_COPY,
  opening: {
    arabic: "بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ",
    kicker: "Assalamu'alaikum Warahmatullahi Wabarakatuh",
    title: "Walimatul 'Ursy",
    intro: "Dengan memohon rahmat dan ridha Allah Subhanahu wa Ta'ala, kami bermaksud menyelenggarakan pernikahan putra-putri kami. Merupakan kehormatan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"] as [string, string],
  couple: ["Teduh Berdua", "Kedua Mempelai"] as [string, string],
  count: ["Menghitung Hari", "Menuju Hari Bahagia"] as [string, string],
  units: ["Hari", "Jam", "Menit", "Detik"] as [string, string, string, string],
  events: ["Waktu & Tempat", "Rangkaian Acara"] as [string, string],
  story: ["Perjalanan", "Kisah Kami"] as [string, string],
  gallery: ["Galeri", "Momen Bahagia"] as [string, string],
  wishes: ["Doa & Kehadiran", "Ucapan & Konfirmasi"] as [string, string],
  gifts: ["Tanda Kasih", "Amplop Digital"] as [string, string],
  closing: {
    thanks: "Jazakumullah Khairan",
    text: "Atas kehadiran dan doa restu Bapak/Ibu/Saudara/i, kami ucapkan terima kasih. Semoga Allah melimpahkan keberkahan seperti air yang tak pernah kering di oasis.",
    salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh",
  },
  sent: "Jazakumullah khairan, doa dan ucapan Anda sudah terkirim.",
};

export default function OasisKurmaTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Walimatul 'Ursy";
  const hero = data.gallery[0] ?? data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#86bde3"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.capsule}><Photo src={hero} alt="" /></div>
          <Art name="palm" eager className={s.palmL} />
          <Art name="palm" eager className={s.palmR} />
          <div className={s.coverText}>
            <p className={s.kicker}>{label}</p>
            <h1 className={s.coverNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
            <div className={s.guestWrap}>
              <div className={s.guest}>
                <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
                <strong>{guestLabel(data)}</strong>
                {table && <span className={s.table}>{table}</span>}
              </div>
              <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#fffbf3" />Buka Undangan</button>
            </div>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#f6d58e"
        dark="#1f6670"
        copy={COPY}
        hero={(
          <header className={s.hero}>
            <span className={s.heroSun} aria-hidden />
            <Art name="sprig" className={s.heroSprig} />
            <p className={s.kickerDark}>{label}</p>
            <h1 className={s.heroNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
            <Art name="dune" className={s.heroDune} />
          </header>
        )}
        slots={{
          divider: <Art name="sprig" className={s.divider} />,
          node: <Art name="dates" />,
          amp: <Art name="dates" />,
          portrait: <Art name="dates" className={s.portraitDates} />,
          countDecor: <><Art name="dune" className={`${s.countDune} ${s.countDuneT}`} /><Art name="dune" className={`${s.countDune} ${s.countDuneB}`} /></>,
          closingDecor: <><Art name="dune" className={s.closingDune} /><Art name="palm" className={`${s.closingPalm} ${s.closingPalmL}`} /><Art name="palm" className={`${s.closingPalm} ${s.closingPalmR}`} /></>,
          closingEmblem: <Art name="dates" className={s.emblem} />,
          sentArt: <Art name="dates" />,
        }}
      />
    </ThemeShell>
  );
}
