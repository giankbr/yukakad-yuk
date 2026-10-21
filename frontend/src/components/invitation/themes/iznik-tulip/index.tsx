"use client";
// Theme "Iznik Tulip" — keramik Iznik: foto pengantin di tengah piring berlukis tulip, anyelir, dan daun saz
// (kobalt, toska, merah tomat di atas slip putih berglasir retak halus), rangkaian bunga di sisi, dan pita ubin.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["DM Serif Display:ital@0;1", "Noto Serif:ital,wght@0,400;0,600;1,400", "Amiri"];
// Painted by /tmp/pen/art/themes/iznik-tulip.py (tools/art/themes in the repo).
const Art = makeArt("iznik-tulip", { border: [640, 93], dish: [620, 620], flower: [140, 197], spray: [300, 483] } as const);

const COPY = {
  ...DEFAULT_COPY,
  opening: {
    arabic: "بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ",
    kicker: "Assalamu'alaikum Warahmatullahi Wabarakatuh",
    title: "Dengan Penuh Syukur",
    intro: "Dengan memohon rahmat dan ridha Allah Subhanahu wa Ta'ala, kami bermaksud menyelenggarakan walimah pernikahan putra-putri kami. Kehadiran dan doa Bapak/Ibu/Saudara/i adalah kebahagiaan bagi kami.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"] as [string, string],
  couple: ["Dua Tangkai, Satu Taman", "Kedua Mempelai"] as [string, string],
  count: ["Menanti", "Hari yang Dinanti"] as [string, string],
  units: ["Hari", "Jam", "Menit", "Detik"] as [string, string, string, string],
  events: ["Waktu & Tempat", "Rangkaian Acara"] as [string, string],
  story: ["Cerita Kami", "Perjalanan Cinta"] as [string, string],
  gallery: ["Galeri", "Momen Bahagia"] as [string, string],
  wishes: ["Doa & Kehadiran", "Ucapan & Konfirmasi"] as [string, string],
  gifts: ["Tanda Kasih", "Amplop Digital"] as [string, string],
  closing: {
    thanks: "Terima Kasih",
    text: "Atas doa dan kehadiran Bapak/Ibu/Saudara/i, kami sekeluarga mengucapkan terima kasih. Semoga Allah membalas dengan kebaikan berlipat.",
    salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh",
  },
  sent: "Jazakumullah khairan, doa dan ucapan Anda sudah terkirim.",
};

export default function IznikTulipTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Walimatul 'Ursy";
  const hero = data.gallery[0] ?? data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#1f3f9a"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Art name="spray" eager className={s.sprayL} />
          <Art name="spray" eager className={s.sprayR} />
          <p className={s.kicker}>{label}</p>
          <div className={s.dishBox}>
            <div className={s.dishPhoto}><Photo src={hero} alt="" /></div>
            <Art name="dish" eager className={s.dish} />
          </div>
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
        light="#f7f4ec"
        dark="#1f3f9a"
        copy={COPY}
        hero={(
          <header className={s.hero}>
            <div className={s.heroSprays} aria-hidden>
              <Art name="flower" />
              <Art name="spray" />
              <Art name="flower" />
            </div>
            <p className={s.kickerDark}>{label}</p>
            <h1 className={s.heroNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="border" className={s.divider} />,
          node: <Art name="flower" />,
          amp: <Art name="flower" />,
          portrait: <Art name="dish" />,
          countDecor: <><Art name="border" className={`${s.izStrip} ${s.izStripT}`} /><Art name="border" className={`${s.izStrip} ${s.izStripB}`} /></>,
          closingEmblem: <Art name="spray" className={s.closingSpray} />,
          sentArt: <Art name="flower" />,
        }}
      />
    </ThemeShell>
  );
}
