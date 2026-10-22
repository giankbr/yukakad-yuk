"use client";
// Theme "Mashrabiya Kayu" — jendela mashrabiya dari kayu bubut (jeruji, manik, simpul kubus, serat walnut) di dinding
// plester yang tersiram cahaya madu; bayangan kisi-kisinya jatuh miring di dinding. Foto pengantin terlihat dari balik
// lengkung jendela.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["El Messiri:wght@400;500;600", "Crimson Pro:ital,wght@0,400;0,500;0,600;1,400", "Amiri"];
// Painted by /tmp/pen/art/themes/mashrabiya-kayu.py (tools/art/themes in the repo).
const Art = makeArt("mashrabiya-kayu", { screen: [640, 800], panel: [380, 529], band: [440, 47], rosette: [220, 220] } as const);

const COPY = {
  ...DEFAULT_COPY,
  opening: {
    arabic: "بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ",
    kicker: "Assalamu'alaikum Warahmatullahi Wabarakatuh",
    title: "Walimatul 'Ursy",
    intro: "Dengan memohon rahmat dan ridha Allah Subhanahu wa Ta'ala, kami bermaksud menyelenggarakan pernikahan putra-putri kami. Merupakan kehormatan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"] as [string, string],
  couple: ["Di Balik Kisi-Kisi", "Kedua Mempelai"] as [string, string],
  count: ["Menanti Cahaya Pagi", "Menuju Hari Bahagia"] as [string, string],
  units: ["Hari", "Jam", "Menit", "Detik"] as [string, string, string, string],
  events: ["Waktu & Tempat", "Rangkaian Acara"] as [string, string],
  story: ["Perjalanan", "Kisah Kami"] as [string, string],
  gallery: ["Galeri", "Momen Bahagia"] as [string, string],
  wishes: ["Doa & Kehadiran", "Ucapan & Konfirmasi"] as [string, string],
  gifts: ["Tanda Kasih", "Amplop Digital"] as [string, string],
  closing: {
    thanks: "Jazakumullah Khairan",
    text: "Atas kehadiran dan doa restu Bapak/Ibu/Saudara/i, kami ucapkan terima kasih. Semoga Allah membalas setiap kebaikan dengan berlipat.",
    salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh",
  },
  sent: "Jazakumullah khairan, doa dan ucapan Anda sudah terkirim.",
};

export default function MashrabiyaKayuTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Walimatul 'Ursy";
  const hero = data.gallery[0] ?? data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#33200f"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <span className={s.wallBg} aria-hidden />
          <span className={s.sun} aria-hidden />
          <div className={s.bay}>
            <div className={s.bayPhoto}><Photo src={hero} alt="" /></div>
            <Art name="screen" eager className={s.screen} />
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
              <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#f3d39c" />Buka Undangan</button>
            </div>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#f3d39c"
        dark="#5a3118"
        copy={COPY}
        hero={(
          <header className={s.hero}>
            <span className={s.heroRay} aria-hidden />
            <Art name="panel" className={s.heroPanel} />
            <p className={s.kickerDark}>{label}</p>
            <h1 className={s.heroNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="band" className={s.divider} />,
          node: <Art name="rosette" />,
          amp: <Art name="rosette" />,
          countDecor: <><Art name="panel" className={`${s.countPanel} ${s.countPanelL}`} /><Art name="panel" className={`${s.countPanel} ${s.countPanelR}`} /></>,
          closingDecor: <Art name="panel" className={s.closingPanel} />,
          closingEmblem: <Art name="rosette" className={s.emblem} />,
          sentArt: <Art name="rosette" />,
        }}
      />
    </ThemeShell>
  );
}
