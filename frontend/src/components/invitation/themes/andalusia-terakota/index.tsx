"use client";
// Theme "Andalusia Terakota" — terinspirasi Alhambra: tiga lengkung berlobus dari plester berukir (yeseria) di atas
// tiang marmer, frieze muqarnas, jaring sebka, dan ubin cuerda seca terakota-kobalt yang membingkai nama pengantin.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["IM Fell English:ital@0;1", "EB Garamond:ital,wght@0,400;0,500;0,600;1,400", "Italianno", "Amiri"];
// Painted by /tmp/pen/art/themes/andalusia-terakota.py (tools/art/themes in the repo).
const Art = makeArt("andalusia-terakota", { arcade: [640, 623], muqarnas: [640, 105], rosette: [180, 180] } as const);

const COPY = {
  ...DEFAULT_COPY,
  opening: {
    arabic: "بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ",
    kicker: "Assalamu'alaikum Warahmatullahi Wabarakatuh",
    title: "Undangan Walimah",
    intro: "Maha Suci Allah yang telah menciptakan makhluk-Nya berpasang-pasangan. Dengan memohon ridha-Nya, kami mengundang Bapak/Ibu/Saudara/i untuk hadir dan mendoakan pernikahan putra-putri kami.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"] as [string, string],
  couple: ["Bismillah, Kami Menikah", "Kedua Mempelai"] as [string, string],
  count: ["Hitung Mundur", "Menuju Hari Akad"] as [string, string],
  units: ["Hari", "Jam", "Menit", "Detik"] as [string, string, string, string],
  events: ["Waktu & Tempat", "Rangkaian Acara"] as [string, string],
  story: ["Lembar demi Lembar", "Kisah Kami"] as [string, string],
  gallery: ["Galeri", "Potret Bahagia"] as [string, string],
  wishes: ["Doa & Kehadiran", "Ucapan & Konfirmasi"] as [string, string],
  gifts: ["Tanda Kasih", "Hadiah & Amplop"] as [string, string],
  closing: {
    thanks: "Terima Kasih",
    text: "Merupakan kebahagiaan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu. Barakallahu lakuma wa baraka 'alaikuma.",
    salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh",
  },
  sent: "Jazakumullah khairan, doa dan ucapan Anda sudah kami terima.",
};

export default function AndalusiaTerakotaTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Walimatul 'Ursy";
  const hero = data.gallery[0] ?? data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#5a2414"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.arcadeBox}>
            <div className={s.arcadePhoto}><Photo src={hero} alt="" /></div>
            <Art name="arcade" eager className={s.arcade} />
          </div>
          <div className={s.cartouche}>
            <div className={s.cartoucheIn}>
              <p className={s.kicker}>{label}</p>
              <h1 className={s.coverNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
              <p className={s.coverDate}>{formatDate(data.date)}</p>
            </div>
          </div>
          <div className={s.guestWrap}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#f8efe0" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#f1d9a6"
        dark="#9c4326"
        copy={COPY}
        hero={(
          <header className={s.hero}>
            <Art name="rosette" className={s.heroRosette} />
            <p className={s.kickerDark}>{label}</p>
            <h1 className={s.heroNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="muqarnas" className={s.divider} />,
          node: <Art name="rosette" />,
          amp: <Art name="rosette" />,
          closingEmblem: <Art name="rosette" className={s.closingEmblem} />,
          sentArt: <Art name="rosette" />,
        }}
      />
    </ThemeShell>
  );
}
