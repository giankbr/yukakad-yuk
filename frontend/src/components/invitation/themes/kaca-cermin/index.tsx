"use client";
// Theme "Kaca Cermin" — Islami, aineh-kari Persia: medali bintang delapan (khatam) dari ribuan keping kaca cermin yang
// dipotong tangan, memantulkan perak, toska tua, dan rose gold; jalur mozaik kaca di tepi ruang, kilau cahaya yang berkedip
// di atas kepingan. Potret segi delapan berbingkai mozaik. Pola geometri murni: tanpa figur, tanpa kaligrafi.
import type { CSSProperties } from "react";
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Federant:wght@400", "Lustria:wght@400", "Amiri:wght@400"];
// Painted by /tmp/pen/art/themes/kaca-cermin.py (wall, tile and frieze are CSS backgrounds)
const Art = makeArt("kaca-cermin", { star: [720, 713], rosette: [120, 122], divider: [360, 30], glint: [64, 64] } as const);
const BISMILLAH = "بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ";

// Glints sit on mirror facets of the medallion: [left %, top %, delay s, size px]
const MEDAL_GLINTS: [number, number, number, number][] = [
  [50, 4, 0, 34], [82, 20, 1.3, 26], [95, 50, 2.6, 30], [80, 80, .7, 24], [50, 95, 3.4, 30], [19, 80, 2, 26], [5, 50, 4, 28], [18, 19, 1.7, 24],
  [66, 15, 3, 18], [86, 66, 4.3, 18], [32, 88, 2.3, 18], [12, 35, 3.8, 18],
];
const BAND_GLINTS: [number, number, number, number][] = [[12, 18, .4, 22], [88, 26, 2.1, 26], [26, 82, 3.2, 20], [76, 78, 1.2, 24], [50, 12, 4.1, 18]];

function Glints({ at }: { at: [number, number, number, number][] }) {
  return (
    <>
      {at.map(([x, y, d, size], i) => (
        <span key={i} className={s.glint} style={{ left: `calc(${x}% - ${size / 2}px)`, top: `calc(${y}% - ${size / 2}px)`, width: size, height: size, animationDelay: `${d}s` } as CSSProperties}>
          <Art name="glint" />
        </span>
      ))}
    </>
  );
}

export default function KacaCerminTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const { bride, groom } = data.couple;
  const table = tableLabel(data.guestTable);
  const heroSrc = data.gallery[0] || data.couple.bridePhoto || data.couple.groomPhoto;
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#0d3a3f"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <span className={s.coverGlow} aria-hidden />
          <p className={s.bism} lang="ar" dir="rtl">{BISMILLAH}</p>
          <p className={s.kicker}>{data.eventLabel ?? "Walimatul 'Ursy"}</p>
          <div className={s.medal}>
            <Art name="star" eager />
            <Glints at={MEDAL_GLINTS} />
            <div className={s.medalText}>
              <h1 className={s.coverNames}><span>{bride}</span><i>&amp;</i><span>{groom}</span></h1>
            </div>
          </div>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.guest}>
            <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
            <strong>{guestLabel(data)}</strong>
            {table && <span className={s.table}>{table}</span>}
          </div>
          <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#072528" />Buka Undangan</button>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#f0cdb9"
        dark="#072528"
        demoWishes={[
          { id: "w1", name: "Keluarga H. Lukman Hakim", attendance: "yes", message: "Barakallahu lakuma wa baraka 'alaikuma wa jama'a bainakuma fi khair. Semoga menjadi keluarga sakinah, mawaddah, wa rahmah." },
          { id: "w2", name: "Teman Halaqah Salman", attendance: "yes", message: "MasyaAllah, ikut bahagia! Semoga rumah tangga kalian selalu memantulkan cahaya kebaikan untuk sekitar." },
          { id: "w3", name: "Ustazah Nurul Aini", attendance: "maybe", message: "Insyaallah hadir bila tidak ada halangan. Doa terbaik untuk Shafira dan Daffa." },
        ]}
        copy={{
          ...DEFAULT_COPY,
          opening: {
            arabic: BISMILLAH,
            kicker: "Assalamu'alaikum Warahmatullahi Wabarakatuh",
            title: "Dengan Memohon Rahmat Allah",
            intro: "Dengan memohon rahmat dan rida Allah Subhanahu wa Ta'ala, kami bermaksud menyelenggarakan pernikahan putra-putri kami. Merupakan kehormatan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
          },
          roles: ["Mempelai Wanita", "Mempelai Pria"],
          couple: ["Dua Cahaya", "Kedua Mempelai"],
          count: ["Menuju Hari Akad", "Hitung Mundur"],
          units: ["Hari", "Jam", "Menit", "Detik"],
          events: ["Waktu & Tempat", "Rangkaian Acara"],
          story: ["Perjalanan Kami", "Kisah Kami"],
          gallery: ["Galeri", "Pantulan Kenangan"],
          wishes: ["Doa Restu", "Ucapan & Kehadiran"],
          gifts: ["Tanda Kasih", "Amplop Digital"],
          closing: {
            thanks: "Jazakumullah Khairan",
            text: "Kehadiran dan doa restu Bapak/Ibu/Saudara/i merupakan kehormatan dan kebahagiaan bagi kami sekeluarga.",
            salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh",
          },
          sent: "Jazakumullah khairan, doa dan ucapan Anda sudah terkirim.",
        }}
        hero={(
          <header className={s.hero}>
            <p className={s.heroKicker}>Insyaallah Kami Menikah</p>
            <div className={s.heroFrame}>
              <div className={s.heroPhoto}>{heroSrc ? <Photo src={heroSrc} alt={`${bride} & ${groom}`} /> : <div />}</div>
            </div>
            <div className={s.heroRoses} aria-hidden><Art name="rosette" className={s.heroRose} /><Art name="rosette" className={s.heroRose} /></div>
            <h1 className={s.heroNames}>{bride} <i>&amp;</i> {groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <span className={s.divider} aria-hidden><Art name="divider" /></span>,
          node: <Art name="rosette" />,
          amp: <Art name="rosette" />,
          portrait: <Art name="rosette" className={s.portraitRose} />,
          countDecor: <span className={s.countGlints} aria-hidden><Glints at={BAND_GLINTS} /></span>,
          closingEmblem: <Art name="rosette" className={s.closingRose} />,
          sentArt: <Art name="rosette" />,
        }}
      />
    </ThemeShell>
  );
}
