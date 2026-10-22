"use client";
// Theme "Khataman Quran" — syukuran khatam Al-Qur'an anak dalam hijau tenang, krem dan emas: rehal kayu walnut (gouache)
// dengan mushaf tertutup bersampul polos berbingkai foil dan medali geometri (tanpa kaligrafi), lentera kaca hijau yang
// bergoyang pelan, bintang delapan foil, ranting melati cat air, kartu bersudut potong dan 30 belah ketupat "30 juz".
import type { CSSProperties } from "react";
import { Lucide, ThemeShell, formatDate, guestLabel, toDate, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Gilda Display", "Lora:ital,wght@0,400;0,500;1,400", "Amiri:wght@400"];
// Painted by /tmp/pen/art/themes/khataman-quran.py (tile.webp is a CSS background)
const Art = makeArt("khataman-quran", { rehal: [513, 585], lantern: [200, 352], star: [96, 96], divider: [360, 30], sprig: [400, 239] } as const);
const BISMILLAH = "بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ";
const HAMDALAH = "الْحَمْدُ لِلَّهِ";
const JUZ = Array.from({ length: 30 }, (_, i) => i);

function ageAt(birth?: string, at?: string) {
  const b = toDate(birth);
  const d = toDate(at);
  if (!b || !d) return undefined;
  let age = d.getFullYear() - b.getFullYear();
  if (d.getMonth() < b.getMonth() || (d.getMonth() === b.getMonth() && d.getDate() < b.getDate())) age -= 1;
  return age > 0 && age < 40 ? age : undefined;
}

function Lamp({ className, eager }: { className: string; eager?: boolean }) {
  return <span className={`${s.lamp} ${className}`} aria-hidden><Art name="lantern" eager={eager} /></span>;
}

export default function KhatamanQuranTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Khataman Al-Qur'an";
  const child = data.extras?.child?.enabled !== false && data.extras?.child?.name?.trim() ? data.extras.child : undefined;
  const nick = child?.nickname?.trim() || child?.name.trim() || data.couple.bride;
  const names = child ? nick : [data.couple.bride, data.couple.groom?.trim()].filter(Boolean).join(" & ");
  const age = ageAt(child?.birthDate, data.date);
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#f5efe1"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Lamp className={s.lampL} eager />
          <Lamp className={s.lampR} eager />
          <p className={s.bism} lang="ar" dir="rtl">{BISMILLAH}</p>
          <p className={s.kicker}>Undangan {label}</p>
          <div className={s.rehalWrap} aria-hidden><Art name="rehal" eager /></div>
          <h1 className={s.coverName}>{names}</h1>
          <p className={s.coverSub}>Alhamdulillah, telah khatam 30 juz{age ? ` di usia ${age} tahun` : ""}</p>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.guestWrap}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#f3e2b4" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        celebrant
        noPhotos={!child?.photo && !data.couple.bridePhoto}
        light="#f3e2b4"
        dark="#1d4a3e"
        demoWishes={[
          { id: "w1", name: "Ustazah Maryam", attendance: "yes", message: "Masyaallah, barakallahu fiik Aisyah. Semoga Al-Qur'an menjadi cahaya hidupmu dan kelak menjadi syafaat bagi Ayah dan Bunda." },
          { id: "w2", name: "Keluarga Bapak Hendra", attendance: "yes", message: "Alhamdulillah, ikut bahagia. Semoga istiqamah membaca dan mengamalkan, dan menjadi anak salihah kebanggaan keluarga." },
          { id: "w3", name: "Tante Nisa & Om Yusuf", attendance: "maybe", message: "Mohon maaf bila belum bisa hadir. Doa kami menyertai, semoga khatam berikutnya disertai hafalan yang makin banyak." },
        ]}
        copy={{
          ...DEFAULT_COPY,
          opening: {
            arabic: BISMILLAH,
            kicker: "Assalamu'alaikum Warahmatullahi Wabarakatuh",
            title: "Syukur atas Khatamnya Al-Qur'an",
            intro: `Dengan memohon rahmat dan ridha Allah Subhanahu wa Ta'ala, kami mengundang Bapak/Ibu/Saudara/i untuk hadir dalam syukuran ${label} ananda tercinta kami, ${names}. Mohon doakan agar ${names} istiqamah membaca, memahami dan mengamalkan Al-Qur'an sepanjang hidupnya.`,
          },
          roles: ["Yang Mengkhatamkan", "Bersama"],
          couple: ["Ananda Tercinta", child ? "Sang Pembaca Al-Qur'an" : "Yang Mengkhatamkan"],
          count: ["Menuju Hari Syukur", "Hitung Mundur"],
          units: ["Hari", "Jam", "Menit", "Detik"],
          events: ["Waktu & Tempat", "Rangkaian Acara"],
          story: ["Dari Iqra' hingga Khatam", `Perjalanan Mengaji ${nick}`],
          gallery: ["Galeri", "Kenangan"],
          wishes: ["Titip Doa", "Doa & Kehadiran"],
          gifts: ["Tanda Kasih", "Amplop Digital"],
          closing: {
            thanks: "Jazakumullah Khairan",
            text: `Terima kasih atas doa dan kehadiran Bapak/Ibu/Saudara/i. Semoga keberkahan Al-Qur'an melimpah untuk ${names} dan untuk kita semua.`,
            salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh",
          },
          sent: "Jazakumullah khairan, doa Anda sudah kami terima.",
          wishPlaceholder: `Tuliskan doa untuk ${names}…`,
          closedNote: "Terima kasih atas doa dan perhatiannya. Doa masih bisa dikirim lewat form ini.",
        }}
        hero={(
          <header className={s.hero}>
            <p className={s.heroAr} lang="ar" dir="rtl">{HAMDALAH}</p>
            <p className={s.heroKicker}>{label}</p>
            <h1 className={s.heroName}>{names}</h1>
            <div className={s.juz} aria-hidden>{JUZ.map(i => <i key={i} style={{ "--i": i } as CSSProperties} />)}</div>
            <p className={s.juzLabel}>Telah membaca 30 juz Al-Qur&apos;an</p>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
            <Art name="sprig" className={s.heroSprig} />
          </header>
        )}
        slots={{
          divider: <span className={s.divider} aria-hidden><Art name="divider" /></span>,
          node: <Art name="star" />,
          portrait: <Art name="star" className={s.portraitStar} />,
          countDecor: <><Lamp className={`${s.countLamp} ${s.countLampL}`} /><Lamp className={`${s.countLamp} ${s.countLampR}`} /></>,
          closingDecor: <><Art name="sprig" className={`${s.closingSprig} ${s.closingSprigL}`} /><Art name="sprig" className={`${s.closingSprig} ${s.closingSprigR}`} /></>,
          closingEmblem: <Art name="star" className={s.closingStar} />,
          sentArt: <Art name="star" />,
        }}
      />
    </ThemeShell>
  );
}
