"use client";
// Theme "Iluminasi Emas" — walimah Islami bergaya halaman naskah klasik yang beriluminasi emas dan lapis: kepala halaman
// (unwan) dengan mahkota berkelopak biru dan kartus kosong tempat basmalah dan nama diketik, pita sarlawh yang memuat
// setiap judul bagian, medali syamsah yang berputar pelan, medali tepi berbentuk palmet, pinggiran sulur emas di kedua
// sisi halaman. Ornamen hanya bingkai: sulur, bunga, geometri. Tanpa figur, tanpa kaligrafi lukis (semua teks diketik).
import type { ReactNode } from "react";
import { Lucide, ThemeShell, formatDate, guestLabel, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Marcellus", "Marcellus SC", "EB Garamond:ital,wght@0,400;0,500;0,600;1,400", "Amiri:wght@400;700"];
// Painted by /tmp/pen/art/themes/iluminasi-emas.py (tools/art/themes in the repo).
const Art = makeArt("iluminasi-emas", { unwan: [730, 391], sarlawh: [686, 174], shamsa: [240, 240], marginal: [90, 207] } as const);
const BISMILLAH = "بِسْمِ اللّٰهِ الرَّحْمٰنِ الرَّحِيْمِ";

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    arabic: BISMILLAH,
    kicker: "Assalamu'alaikum Warahmatullahi Wabarakatuh",
    title: "Dengan Rahmat Allah",
    intro: "Maha Suci Allah yang menciptakan segala sesuatu berpasang-pasangan. Dengan memohon ridha-Nya, kami bermaksud menyelenggarakan walimatul 'ursy putra-putri kami. Merupakan kehormatan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan mendoakan.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"],
  couple: ["Bismillah, Kami Menikah", "Mempelai"],
  count: ["Menghitung Hari", "Menuju Akad"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Majelis", "Waktu & Tempat"],
  story: ["Lembar demi Lembar", "Kisah Kami"],
  gallery: ["Kenangan", "Galeri"],
  wishes: ["Doa & Kehadiran", "Ucapan"],
  gifts: ["Tanda Kasih", "Amplop Digital"],
  closing: { thanks: "Jazakumullahu Khairan", text: "Atas kehadiran dan doa Bapak/Ibu/Saudara/i, kami sekeluarga menghaturkan terima kasih. Semoga Allah membalas setiap kebaikan dengan yang lebih baik.", salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh" },
  sent: "Jazakumullahu khairan, doa Anda sudah kami terima.",
  wishPlaceholder: "Tuliskan doa untuk kedua mempelai…",
  closedNote: "Terima kasih atas doa dan perhatiannya. Ucapan masih bisa dikirim lewat form ini.",
  giftIntro: "Doa Anda adalah hadiah terindah bagi kami. Jika berkenan memberi tanda kasih, dapat melalui:",
};

const WISHES = [
  { id: "w1", name: "Ustadz H. Muhammad Ridwan", attendance: "yes" as Attendance, message: "Barakallahu lakuma wa baraka 'alaikuma wa jama'a bainakuma fi khair. Semoga menjadi keluarga yang sakinah." },
  { id: "w2", name: "Teman-teman Filologi", attendance: "yes" as Attendance, message: "Dari ruang naskah ke pelaminan. Selamat Zahra dan Hanif, semoga kisahnya seindah halaman beriluminasi." },
  { id: "w3", name: "Keluarga Hj. Rukmini", attendance: "maybe" as Attendance, message: "Insyaallah kami usahakan hadir. Doa terbaik untuk kedua mempelai dan keluarga." },
];

function Unwan({ children, eager }: { children: ReactNode; eager?: boolean }) {
  return (
    <div className={s.unwan}>
      <Art name="unwan" eager={eager} className={s.unwanImg} />
      <div className={s.unwanText}>{children}</div>
    </div>
  );
}

export default function IluminasiEmasTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#172f6e"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Unwan eager>
            <p className={s.bismillah} lang="ar" dir="rtl">{BISMILLAH}</p>
          </Unwan>
          <p className={s.kicker}>Undangan {label === "Pernikahan" ? "Walimatul 'Ursy" : label}</p>
          <div className={s.names}>
            <Art name="marginal" eager className={s.margL} />
            <h1 className={s.coverNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <Art name="marginal" eager className={s.margR} />
          </div>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.guestWrap}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#ffffff" />Buka Undangan</button>
          </div>
          <Art name="shamsa" eager className={s.coverShamsa} />
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#e6c97a"
        dark="#1f3d8f"
        copy={COPY}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            <Unwan>
              <h1 className={s.heroNames}>{data.couple.bride} <em>&amp;</em> {data.couple.groom}</h1>
            </Unwan>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="sarlawh" className={s.divider} />,
          node: <Art name="shamsa" />,
          amp: <Art name="marginal" />,
          portrait: <Art name="shamsa" className={s.portraitSun} />,
          countDecor: <Art name="shamsa" className={s.countDecor} />,
          closingEmblem: <Art name="shamsa" className={s.closingSun} />,
          sentArt: <Art name="shamsa" />,
        }}
      />
    </ThemeShell>
  );
}
