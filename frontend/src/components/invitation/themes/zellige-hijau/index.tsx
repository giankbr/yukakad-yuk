"use client";
// Theme "Zellige Hijau" — riad Maroko: foto pengantin terlihat dari balik lengkung tapal kuda berlapis mosaik zellige
// (setiap keping berglasir tak rata, nat, dan tepi yang sedikit gompal), air mancur halaman, dan dahan pohon jeruk.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Josefin Sans:wght@300;400;600", "Lora:ital,wght@0,400;0,500;0,600;1,400", "Parisienne", "Amiri"];
// Painted by /tmp/pen/art/themes/zellige-hijau.py (tools/art/themes in the repo).
const Art = makeArt("zellige-hijau", { arch: [640, 738], band: [760, 134], fountain: [420, 316], orange: [360, 274], star: [200, 200] } as const);

const COPY = {
  ...DEFAULT_COPY,
  opening: {
    arabic: "بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ",
    kicker: "Assalamu'alaikum Warahmatullahi Wabarakatuh",
    title: "Walimatul 'Ursy",
    intro: "Dengan memohon rahmat dan ridha Allah Subhanahu wa Ta'ala, kami bermaksud menyelenggarakan pernikahan putra-putri kami. Merupakan kehormatan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"] as [string, string],
  couple: ["Dua Keping Satu Pola", "Kedua Mempelai"] as [string, string],
  count: ["Menghitung Hari", "Menuju Hari Bahagia"] as [string, string],
  units: ["Hari", "Jam", "Menit", "Detik"] as [string, string, string, string],
  events: ["Waktu & Tempat", "Rangkaian Acara"] as [string, string],
  story: ["Perjalanan", "Kisah Kami"] as [string, string],
  gallery: ["Galeri", "Momen Bahagia"] as [string, string],
  wishes: ["Doa & Kehadiran", "Ucapan & Konfirmasi"] as [string, string],
  gifts: ["Tanda Kasih", "Amplop Digital"] as [string, string],
  closing: {
    thanks: "Jazakumullah Khairan",
    text: "Atas kehadiran dan doa restu Bapak/Ibu/Saudara/i, kami ucapkan terima kasih. Semoga Allah membalas kebaikan Anda semua.",
    salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh",
  },
  sent: "Jazakumullah khairan, doa dan ucapan Anda sudah terkirim.",
};

export default function ZelligeHijauTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Walimatul 'Ursy";
  const hero = data.gallery[0] ?? data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#0f3b31"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.archBox}>
            <div className={s.archPhoto}><Photo src={hero} alt="" /></div>
            <Art name="arch" eager className={s.arch} />
            <Art name="orange" eager className={s.orangeL} />
            <Art name="orange" eager className={s.orangeR} />
          </div>
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
              <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#f4efe4" />Buka Undangan</button>
            </div>
          </div>
          <Art name="band" eager className={s.dado} />
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#f0dca8"
        dark="#155443"
        copy={COPY}
        hero={(
          <header className={s.hero}>
            <Art name="star" className={s.heroStar} />
            <p className={s.kickerDark}>{label}</p>
            <h1 className={s.heroNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
            <Art name="fountain" className={s.heroFountain} />
          </header>
        )}
        slots={{
          divider: <Art name="band" className={s.divider} />,
          node: <Art name="star" />,
          amp: <Art name="star" />,
          countDecor: <><Art name="band" className={`${s.zStrip} ${s.zStripT}`} /><Art name="band" className={`${s.zStrip} ${s.zStripB}`} /></>,
          closingDecor: <Art name="orange" className={s.closingOrange} />,
          closingEmblem: <Art name="fountain" className={s.fountain} />,
          sentArt: <Art name="star" />,
        }}
      />
    </ThemeShell>
  );
}
