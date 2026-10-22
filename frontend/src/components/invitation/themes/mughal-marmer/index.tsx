"use client";
// Theme "Mughal Marmer" — marmer putih bertatah batu (pietra dura): kelopak akik merah, lapis lazuli berbintik emas, daun
// giok yang dibelah dua batu, garis oniks; lengkung Mughal berlekuk membingkai foto, jali marmer di atas batu pasir merah.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Prata", "Spectral:ital,wght@0,400;0,500;0,600;1,400", "Amiri"];
// Painted by /tmp/pen/art/themes/mughal-marmer.py (tools/art/themes in the repo).
const Art = makeArt("mughal-marmer", { arch: [560, 718], jali: [320, 427], spray: [349, 526], border: [460, 44], flower: [128, 128] } as const);

const COPY = {
  ...DEFAULT_COPY,
  opening: {
    arabic: "بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ",
    kicker: "Assalamu'alaikum Warahmatullahi Wabarakatuh",
    title: "Walimatul 'Ursy",
    intro: "Dengan memohon rahmat dan ridha Allah Subhanahu wa Ta'ala, kami bermaksud menyelenggarakan pernikahan putra-putri kami. Merupakan kehormatan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"] as [string, string],
  couple: ["Dua Batu, Satu Tatahan", "Kedua Mempelai"] as [string, string],
  count: ["Menghitung Hari", "Menuju Hari Bahagia"] as [string, string],
  units: ["Hari", "Jam", "Menit", "Detik"] as [string, string, string, string],
  events: ["Waktu & Tempat", "Rangkaian Acara"] as [string, string],
  story: ["Perjalanan", "Kisah Kami"] as [string, string],
  gallery: ["Galeri", "Momen Bahagia"] as [string, string],
  wishes: ["Doa & Kehadiran", "Ucapan & Konfirmasi"] as [string, string],
  gifts: ["Tanda Kasih", "Amplop Digital"] as [string, string],
  closing: {
    thanks: "Jazakumullah Khairan",
    text: "Atas kehadiran dan doa restu Bapak/Ibu/Saudara/i, kami ucapkan terima kasih. Semoga Allah membalas kebaikan Anda dengan sebaik-baik balasan.",
    salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh",
  },
  sent: "Jazakumullah khairan, doa dan ucapan Anda sudah terkirim.",
};

export default function MughalMarmerTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Walimatul 'Ursy";
  const hero = data.gallery[0] ?? data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#8a3a28"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.archBox}>
            <div className={s.archPhoto}><Photo src={hero} alt="" /></div>
            <Art name="arch" eager className={s.arch} />
            <span className={s.glint} aria-hidden />
          </div>
          <div className={s.coverText}>
            <p className={s.kicker}>{label}</p>
            <h1 className={s.coverNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
            <Art name="border" eager className={s.coverRule} />
            <div className={s.guestWrap}>
              <div className={s.guest}>
                <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
                <strong>{guestLabel(data)}</strong>
                {table && <span className={s.table}>{table}</span>}
              </div>
              <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#fcfaf5" />Buka Undangan</button>
            </div>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#ead7ae"
        dark="#29467f"
        copy={COPY}
        hero={(
          <header className={s.hero}>
            <div className={s.heroPanel}>
              <Art name="spray" className={s.heroSpray} />
              <p className={s.kickerDark}>{label}</p>
              <h1 className={s.heroNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
              <p className={s.heroDate}>{formatDate(data.date)}</p>
              {note && <p className={s.heroNote}>{note}</p>}
            </div>
          </header>
        )}
        slots={{
          divider: <Art name="border" className={s.divider} />,
          node: <Art name="flower" />,
          amp: <Art name="flower" />,
          countDecor: <><Art name="jali" className={`${s.countJali} ${s.countJaliL}`} /><Art name="jali" className={`${s.countJali} ${s.countJaliR}`} /></>,
          closingEmblem: <Art name="spray" className={s.emblem} />,
          sentArt: <Art name="flower" />,
        }}
      />
    </ThemeShell>
  );
}
