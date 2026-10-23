"use client";
// Theme "Sanaa Qamariya" — senja di kota tua Sana'a: rumah-rumah menara bata dan batu basal berbingkai gipsum putih,
// jendela kaca qamariya berwarna yang menyala dari dalam, langit ungu dengan bulan sabit. Arsitektur dan geometri saja:
// tanpa makhluk bernyawa, tanpa kaligrafi yang dilukis (basmalah diketik sebagai teks).
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["El Messiri:wght@400;500;600", "Karla:ital,wght@0,400;0,700;1,400", "Amiri:wght@400;700"];
// Painted by /tmp/pen/art/themes/sanaa-qamariya.py (tools/art/themes in the repo).
const Art = makeArt("sanaa-qamariya", { city: [720, 585], lights: [360, 292], qamariya: [360, 360], fan: [260, 139] } as const);
const BISMILLAH = "بِسْمِ اللّٰهِ الرَّحْمٰنِ الرَّحِيْمِ";

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    arabic: BISMILLAH,
    kicker: "Assalamu'alaikum Warahmatullahi Wabarakatuh",
    title: "Dengan Rahmat Allah",
    intro: "Dengan memohon rahmat dan ridha Allah SWT, kami bermaksud menyelenggarakan akad dan walimah pernikahan putra-putri kami. Merupakan kehormatan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"],
  couple: ["Dengan Ridha-Nya", "Kedua Mempelai"],
  count: ["Menghitung Hari", "Menuju Hari Akad"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Waktu & Tempat", "Akad & Walimah"],
  story: ["Perjalanan", "Kisah Kami"],
  gallery: ["Galeri", "Jendela Kenangan"],
  wishes: ["Doa & Restu", "Ucapan & Kehadiran"],
  gifts: ["Tanda Kasih", "Amplop Digital"],
  closing: {
    thanks: "Jazakumullah Khairan",
    text: "Atas kehadiran dan doa restu Bapak/Ibu/Saudara/i, kami mengucapkan terima kasih. Semoga Allah membalas setiap kebaikan dengan cahaya dan keberkahan.",
    salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh",
  },
  sent: "Jazakumullah khairan, doa dan ucapan Anda sudah terkirim.",
};

function City({ className, eager }: { className: string; eager?: boolean }) {
  return (
    <div className={className} aria-hidden>
      <Art name="city" eager={eager} />
      <Art name="lights" eager={eager} className={s.glow} />
    </div>
  );
}

export default function SanaaQamariyaTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const hero = data.gallery[0] ?? data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#12142e"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Art name="qamariya" eager className={s.coverQ} />
          <p className={s.arabicCover} lang="ar" dir="rtl">{BISMILLAH}</p>
          <p className={s.kicker}>{label}</p>
          <h1 className={s.coverNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.guestWrap}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#6a3f2b" />Buka Undangan</button>
          </div>
          <City className={s.coverCity} eager />
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#ffd99a"
        dark="#2a1a14"
        copy={COPY}
        hero={(
          <header className={s.hero}>
            <p className={s.heroKicker}>{label}</p>
            <h1 className={s.heroNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {hero && (
              <div className={s.heroWindow}>
                <Art name="fan" className={s.heroFan} />
                <div className={s.heroPhoto}><Photo src={hero} alt="" /></div>
              </div>
            )}
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="fan" className={s.divider} />,
          node: <Art name="fan" />,
          amp: <Art name="fan" />,
          portrait: <Art name="fan" />,
          closingDecor: <City className={s.closingSky} />,
          closingEmblem: <Art name="qamariya" className={s.closingQ} />,
          sentArt: <Art name="qamariya" />,
        }}
      />
    </ThemeShell>
  );
}
