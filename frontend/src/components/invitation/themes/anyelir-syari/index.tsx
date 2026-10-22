"use client";
// Theme "Anyelir Syari" — tanpa foto: anyelir digambar dengan pena tinta halus (kelopak berumbai, kelopak tabung panjang,
// daun ramping), disapu cat air mauve yang sedikit keluar garis di atas kertas krem; medali monogram di sampul dan
// di tempat potret. Tenang, lapang, minimal.
import { Lucide, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Allura", "Cormorant SC:wght@400;500;600", "Alegreya:ital,wght@0,400;0,500;1,400", "Amiri"];
// Painted by /tmp/pen/art/themes/anyelir-syari.py (tools/art/themes in the repo).
const Art = makeArt("anyelir-syari", { spray: [420, 578], medallion: [400, 400], sprig: [420, 83], bloom: [120, 109] } as const);

const COPY = {
  ...DEFAULT_COPY,
  opening: {
    arabic: "بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ",
    kicker: "Assalamu'alaikum Warahmatullahi Wabarakatuh",
    title: "Walimatul 'Ursy",
    intro: "Dengan memohon rahmat dan ridha Allah Subhanahu wa Ta'ala, kami bermaksud menyelenggarakan pernikahan putra-putri kami. Merupakan kehormatan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"] as [string, string],
  couple: ["dengan izin Allah", "Kedua Mempelai"] as [string, string],
  count: ["menanti hari", "Menuju Hari Bahagia"] as [string, string],
  units: ["hari", "jam", "menit", "detik"] as [string, string, string, string],
  events: ["waktu & tempat", "Rangkaian Acara"] as [string, string],
  story: ["perjalanan", "Kisah Kami"] as [string, string],
  gallery: ["galeri", "Momen Bahagia"] as [string, string],
  wishes: ["doa & kehadiran", "Ucapan & Konfirmasi"] as [string, string],
  gifts: ["tanda kasih", "Amplop Digital"] as [string, string],
  closing: {
    thanks: "Jazakumullah Khairan",
    text: "Atas kehadiran dan doa restu Bapak/Ibu/Saudara/i, kami ucapkan terima kasih. Semoga Allah membalas setiap kebaikan dengan kebaikan yang lebih baik.",
    salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh",
  },
  sent: "Jazakumullah khairan, doa dan ucapan Anda sudah terkirim.",
  wishPlaceholder: "Tuliskan doa terbaik untuk kedua mempelai…",
};

const initial = (name?: string) => name?.trim().slice(0, 1).toUpperCase() ?? "";

export default function AnyelirSyariTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Walimatul 'Ursy";
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const mono = (
    <span>{initial(data.couple.bride)}<i>&amp;</i>{initial(data.couple.groom)}</span>
  );

  return (
    <ThemeShell
      fonts={FONTS}
      background="#efe6da"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Art name="spray" eager className={s.sprayTR} />
          <Art name="spray" eager className={s.sprayBL} />
          <div className={s.medal}>
            <Art name="medallion" eager />
            {mono}
          </div>
          <p className={s.kicker}>{label}</p>
          <h1 className={s.coverNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.guestWrap}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="currentColor" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        noPhotos
        light="#4a3843"
        dark="#fbf7f0"
        copy={COPY}
        hero={(
          <header className={s.hero}>
            <Art name="sprig" className={s.heroSprig} />
            <p className={s.kickerDark}>{label}</p>
            <h1 className={s.heroNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="sprig" className={s.divider} />,
          node: <Art name="bloom" />,
          amp: <Art name="bloom" />,
          closingDecor: <Art name="spray" className={s.closingSpray} />,
          closingEmblem: <div className={s.emblem}><Art name="medallion" />{mono}</div>,
          sentArt: <Art name="bloom" />,
        }}
      />
    </ThemeShell>
  );
}
