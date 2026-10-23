"use client";
// Theme "Kristal Syari" — syari tanpa foto: kristal bening bersegi dilukis cat air abu perak di atas kertas gading,
// pelangi cahaya lembut yang jatuh miring, cincin kristal segi enam berisi monogram, dan kilau kecil yang berkedip pelan.
// Tata letak editorial rata kiri di sampul, sangat bersih dan tenang.
import type { CSSProperties } from "react";
import { Lucide, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Italiana", "Jost:wght@300;400;500", "Amiri:wght@400"];
// Painted by /tmp/pen/art/themes/kristal-syari.py (spill is a CSS background)
const Art = makeArt("kristal-syari", { cluster: [440, 475], ring: [300, 292], prism: [320, 45], glint: [64, 64] } as const);
const BISMILLAH = "بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ";

// [left %, top %, delay s, size px]
const CLUSTER_GLINTS: [number, number, number, number][] = [[49, 25, 0, 30], [22, 40, 1.8, 22], [80, 48, 3.1, 24], [55, 62, 4.4, 18], [34, 84, 2.5, 20]];
const BAND_GLINTS: [number, number, number, number][] = [[10, 22, .6, 22], [90, 30, 2.4, 26], [20, 80, 3.6, 18], [80, 76, 1.4, 20]];

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

export default function KristalSyariTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const { bride, groom } = data.couple;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#f7f4ee"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <p className={s.bism} lang="ar" dir="rtl">{BISMILLAH}</p>
          <div className={s.crystals} aria-hidden>
            <Art name="cluster" eager />
            <Glints at={CLUSTER_GLINTS} />
          </div>
          <div className={s.coverBody}>
            <p className={s.kicker}>{data.eventLabel ?? "Walimatul 'Ursy"}</p>
            <h1 className={s.coverNames}><span>{bride}</span><i>&amp;</i><span>{groom}</span></h1>
            <span className={s.coverRule} aria-hidden />
            <p className={s.coverDate}>{formatDate(data.date)}</p>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={15} color="#ffffff" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        noPhotos
        light="#ffffff"
        dark="#3d4a5a"
        demoWishes={[
          { id: "w1", name: "Ibu Hj. Siti Romlah", attendance: "yes", message: "Barakallahu lakuma wa baraka 'alaikuma wa jama'a bainakuma fi khair. Semoga menjadi keluarga sakinah, mawaddah, wa rahmah." },
          { id: "w2", name: "Teman Kajian Manarul Ilmi", attendance: "yes", message: "MasyaAllah, turut berbahagia. Semoga rumah tangga kalian jernih dan menerangi sekitar." },
          { id: "w3", name: "Ustazah Rahmah", attendance: "maybe", message: "Insyaallah hadir bila tidak ada halangan. Doa terbaik untuk Aisyah dan Fathan." },
        ]}
        copy={{
          opening: {
            arabic: BISMILLAH,
            kicker: "Assalamu'alaikum Warahmatullahi Wabarakatuh",
            title: "Dengan Memohon Rida Allah",
            intro: "Maha Suci Allah yang menciptakan segala sesuatu berpasang-pasangan. Dengan memohon rahmat dan rida-Nya, kami bermaksud menyelenggarakan pernikahan putra-putri kami. Merupakan kehormatan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
          },
          roles: ["Mempelai Wanita", "Mempelai Pria"],
          couple: ["Dua Insan", "Kedua Mempelai"],
          count: ["Menuju Hari Akad", "Hitung Mundur"],
          units: ["Hari", "Jam", "Menit", "Detik"],
          events: ["Waktu & Tempat", "Rangkaian Acara"],
          story: ["Perjalanan Kami", "Kisah Kami"],
          gallery: ["Galeri", "Kenangan"],
          wishes: ["Doa Restu", "Ucapan & Kehadiran"],
          gifts: ["Tanda Kasih", "Amplop Digital"],
          closing: {
            thanks: "Jazakumullah Khairan",
            text: "Kehadiran dan doa restu Bapak/Ibu/Saudara/i merupakan kehormatan dan kebahagiaan bagi kami sekeluarga.",
            salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh",
          },
          sent: "Jazakumullah khairan, doa dan ucapan Anda sudah terkirim.",
          wishPlaceholder: "Tuliskan doa restu untuk kedua mempelai…",
          familyLabel: "Keluarga Besar",
        }}
        hero={(
          <header className={s.hero}>
            <p className={s.heroKicker}>Insyaallah Kami Menikah</p>
            <div className={s.heroRing}>
              <Art name="ring" />
              <p className={s.heroInitials} aria-hidden>{bride.slice(0, 1)}<i>&amp;</i>{groom.slice(0, 1)}</p>
            </div>
            <h1 className={s.heroNames}>{bride} <i>&amp;</i> {groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <span className={s.divider} aria-hidden><Art name="prism" /></span>,
          node: <Art name="ring" />,
          amp: <Art name="prism" />,
          portrait: <Art name="ring" className={s.portraitRing} />,
          countDecor: <span className={s.countGlints} aria-hidden><Glints at={BAND_GLINTS} /></span>,
          closingEmblem: <Art name="cluster" className={s.closingCluster} />,
          sentArt: <Art name="prism" />,
        }}
      />
    </ThemeShell>
  );
}
