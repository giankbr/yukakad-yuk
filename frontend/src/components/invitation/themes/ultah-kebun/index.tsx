"use client";
// Theme "Ultah Kebun" — ulang tahun tukang kebun cilik dalam cat gouache: papan nama kayu berpaku, usia di dalam pot tanah
// liat, gembor yang menyiram tetes air, pagar kebun dengan wortel, tomat, terong, dan lobak yang tersenyum, sekop kecil,
// hitung mundur di bedeng tanah dengan tunas, kartu acara seperti penanda tanaman, dan teman wortel yang melompat.
import { Lucide, ThemeShell, formatDate, guestLabel, toDate, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Sniglet:wght@400;800", "Nunito:wght@400;700;800", "Gochi Hand"];
// Painted by /tmp/pen/art/themes/ultah-kebun.py (papan is the CSS background of the name sign).
const Art = makeArt("ultah-kebun", { kebun: [780, 341], siram: [298, 221], pot: [150, 228], tunas: [420, 74], wortel: [170, 258] } as const);

function ageAt(birth?: string, at?: string) {
  const b = toDate(birth);
  const d = toDate(at);
  if (!b || !d) return undefined;
  let age = d.getFullYear() - b.getFullYear();
  if (d.getMonth() < b.getMonth() || (d.getMonth() === b.getMonth() && d.getDate() < b.getDate())) age -= 1;
  return age > 0 && age < 30 ? age : undefined;
}

const WISHES = [
  { id: "w1", name: "Adik Raka & Keluarga", attendance: "yes" as Attendance, message: "Selamat ulang tahun, Naya! Semoga makin sehat, makin pintar, dan tanamanmu tumbuh subur semua." },
  { id: "w2", name: "Bu Guru Ratih, TK Bunga Bangsa", attendance: "yes" as Attendance, message: "Selamat ulang tahun ke-5, tukang kebun kecil kami. Tetap rajin menyiram dan menyayangi teman ya, Nak." },
  { id: "w3", name: "Om Bayu & Tante Sari", attendance: "maybe" as Attendance, message: "Happy birthday, Naya! Kalau sempat Om bawakan bibit stroberi. Doa terbaik dari kami." },
];

export default function UltahKebunTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Ulang Tahun";
  const child = data.extras?.child?.enabled !== false && data.extras?.child?.name?.trim() ? data.extras.child : undefined;
  const nick = child?.nickname?.trim() || child?.name.trim() || data.couple.bride;
  const names = child ? nick : [data.couple.bride, data.couple.groom?.trim()].filter(Boolean).join(" & ");
  const age = ageAt(child?.birthDate, data.date);
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  const copy: ThemeCopy = {
    ...DEFAULT_COPY,
    opening: {
      kicker: "Halo, Teman Kebun!",
      title: "Ayo Berkebun di Pestaku!",
      intro: `Dengan penuh sukacita, kami mengundang teman-teman dan keluarga untuk merayakan ${label.toLowerCase()} ${names}${age ? ` yang ke-${age}` : ""}. Kita akan menanam bibit, menyiram bunga, memetik sayur, dan tentu saja tiup lilin bersama!`,
    },
    roles: ["Tukang Kebun Cilik", "Bersama"],
    couple: ["Kenalan Yuk", child ? "Si Tukang Kebun" : "Yang Merayakan"],
    count: ["Bibit Bertunas Dalam", "Hitung Mundur Pesta"],
    units: ["Hari", "Jam", "Menit", "Detik"],
    events: ["Jadwal Berkebun", "Waktu & Tempat"],
    story: ["Buku Tanam", `Tumbuh Bersama ${nick}`],
    gallery: ["Galeri", "Momen di Kebun"],
    wishes: ["Tanam Ucapanmu", "Ucapan & Kehadiran"],
    gifts: ["Tanda Sayang", "Kado & Amplop Digital"],
    closing: { thanks: "Terima Kasih!", text: `Sampai jumpa di kebun! Kehadiran dan doa teman-teman adalah pupuk terbaik untuk ${names}.` },
    wishPlaceholder: `Tuliskan ucapan dan doa untuk ${names}…`,
    sent: "Ucapanmu sudah ditanam! Terima kasih ya.",
    closedNote: "Terima kasih atas doa dan perhatiannya. Ucapan masih bisa dikirim lewat form ini.",
    giftIntro: `Kehadiranmu sudah jadi hadiah terbaik. Jika ingin memberi tanda sayang untuk ${names}, dapat melalui:`,
    familyLabel: "Salam sayang",
  };

  return (
    <ThemeShell
      fonts={FONTS}
      background="#e8f2d9"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.can} aria-hidden><Art name="siram" eager /></div>
          <div className={s.drops} aria-hidden><i /><i /><i /></div>
          <p className={s.kicker}>Undangan {label}</p>
          <div className={s.sign}>
            <p className={s.signLabel}>Kebun kecil milik</p>
            <h1 className={s.coverName}>{names}</h1>
            <div className={s.ageRow}>
              {age && <div className={s.agePot}><Art name="pot" eager /><b>{age}</b></div>}
              <p className={s.ageText}><small>yuk rayakan</small>{age ? `ulang tahun ke-${age}` : "pesta ulang tahun"}</p>
            </div>
          </div>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.guestWrap}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={17} color="#ffffff" />Buka Undangan</button>
          </div>
          <Art name="kebun" eager className={s.scene} />
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        celebrant
        noPhotos={!child?.photo && !data.couple.bridePhoto}
        light="#fff3d6"
        dark="#4e3121"
        copy={copy}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            <Art name="wortel" className={s.heroWortel} />
            <p className={s.heroKicker}>Hore! {label}</p>
            <h1 className={s.heroName}>{names}</h1>
            {age && <p className={s.heroAge}>{age} Tahun</p>}
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            <Art name="tunas" className={s.heroTunas} />
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="tunas" className={s.divider} />,
          node: <Art name="pot" />,
          amp: <Art name="pot" />,
          portrait: <Art name="wortel" className={s.portraitArt} />,
          countDecor: <Art name="tunas" className={s.countTunas} />,
          closingDecor: <Art name="kebun" className={s.closingScene} />,
          closingEmblem: <Art name="siram" className={s.closingEmblem} />,
          sentArt: <Art name="pot" />,
        }}
      />
    </ThemeShell>
  );
}
