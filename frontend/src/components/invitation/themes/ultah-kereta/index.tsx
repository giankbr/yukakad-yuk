"use client";
// Theme "Ultah Kereta" — ulang tahun anak bertema kereta mainan kayu (desain asli, tanpa wajah/karakter terkenal):
// lokomotif kayu bercat merah-biru-hijau menarik gerbong yang masing-masing membawa satu balok huruf nama si anak,
// gerbong kue dengan balon, stasiun kecil berjam dinding, rel kayu, dan tiket berlubang. Gouache di atas serat kayu.
import type { CSSProperties } from "react";
import { Lucide, ThemeShell, formatDate, guestLabel, toDate, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Sniglet:wght@400;800", "Outfit:wght@400;500;600;700"];
// Painted by /tmp/pen/art/themes/ultah-kereta.py
const Art = makeArt("ultah-kereta", {
  loco: [500, 320], carA: [280, 260], carB: [280, 260], carC: [280, 260], carD: [280, 260],
  cake: [240, 363], station: [320, 226], track: [240, 64], puff: [160, 116],
} as const);
const CARS = ["carA", "carB", "carC", "carD"] as const;

const WISHES = [
  { id: "w1", name: "Naya & Bunda", attendance: "yes" as const, message: "Selamat ulang tahun, Damar! Naya sudah siap pakai topi masinis. Semoga sehat selalu, makin pintar, dan makin sayang Mas Bima." },
  { id: "w2", name: "Keluarga Om Arif", attendance: "yes" as const, message: "Tut tut! Selamat lima tahun, jagoan. Semoga perjalananmu selalu lancar dan penuh hal baik." },
  { id: "w3", name: "Tante Dewi", attendance: "maybe" as const, message: "Maaf belum tentu bisa datang, Sayang. Bukunya sudah Tante siapkan, peluk jauh dari Jakarta!" },
];

function ageAt(birth?: string, at?: string) {
  const b = toDate(birth);
  const d = toDate(at);
  if (!b || !d) return undefined;
  let age = d.getFullYear() - b.getFullYear();
  if (d.getMonth() < b.getMonth() || (d.getMonth() === b.getMonth() && d.getDate() < b.getDate())) age -= 1;
  return age > 0 && age < 30 ? age : undefined;
}

function Train({ letters, className, eager }: { letters: string[]; className?: string; eager?: boolean }) {
  return (
    <div className={`${s.train} ${className ?? ""}`} style={{ "--n": letters.length } as CSSProperties} aria-hidden>
      {letters.map((letter, i) => (
        <span key={i} className={s.car} style={{ "--i": i } as CSSProperties}>
          <Art name={CARS[i % CARS.length]} eager={eager} />
          <b>{letter}</b>
        </span>
      ))}
      <span className={s.loco}>
        <Art name="loco" eager={eager} />
        <span className={s.steam}><Art name="puff" eager={eager} /></span>
      </span>
    </div>
  );
}

export default function UltahKeretaTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Ulang Tahun";
  const child = data.extras?.child?.enabled !== false && data.extras?.child?.name?.trim() ? data.extras.child : undefined;
  const nick = child?.nickname?.trim() || child?.name.trim() || data.couple.bride;
  const names = child ? nick : [data.couple.bride, data.couple.groom?.trim()].filter(Boolean).join(" & ");
  const chars = Array.from(nick.replace(/[^\p{L}\p{N}]/gu, "").toUpperCase());
  const letters = chars.length > 0 && chars.length <= 8 ? chars : ["H", "O", "R", "E"];
  const age = ageAt(child?.birthDate, data.date);
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const copy = {
    ...DEFAULT_COPY,
    opening: {
      kicker: "Semua penumpang, harap naik!",
      title: "Kereta Pesta Berangkat",
      intro: `Dengan penuh sukacita, kami mengundang teman-teman dan keluarga untuk ikut merayakan ${label.toLowerCase()} ${names}${age ? ` yang ke-${age}` : ""}. Siapkan tiket dan semangat: kita susun rel, keliling taman, dan tiup lilin bersama!`,
    },
    roles: ["Masinis Cilik", "Bersama"] as [string, string],
    couple: ["Kenalan dengan masinis", child ? "Si Masinis Cilik" : "Yang Merayakan"] as [string, string],
    count: ["Kereta segera tiba", "Menuju Hari Pesta"] as [string, string],
    units: ["Hari", "Jam", "Menit", "Detik"] as [string, string, string, string],
    events: ["Jadwal keberangkatan", "Waktu & Tempat"] as [string, string],
    story: ["Stasiun demi stasiun", `Perjalanan ${nick}`] as [string, string],
    gallery: ["Album", "Foto Perjalanan"] as [string, string],
    wishes: ["Titip pesan untuk masinis", "Ucapan & Kehadiran"] as [string, string],
    gifts: ["Paket bagasi", "Kado & Amplop Digital"] as [string, string],
    closing: { thanks: "Terima Kasih!", text: `Kehadiran dan doa teman-teman membuat perjalanan ${names} makin seru. Sampai jumpa di stasiun pesta!` },
    sent: "Tut tut! Pesanmu sudah dimuat ke gerbong. Terima kasih!",
    wishPlaceholder: "Tulis ucapan dan doa untuk si masinis cilik…",
    giftIntro: "Kehadiran teman-teman sudah jadi hadiah paling seru. Bila ingin memberi tanda sayang, dapat melalui:",
  };

  return (
    <ThemeShell
      fonts={FONTS}
      background="#fff6e6"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <span className={`${s.cloud} ${s.cloud1}`} aria-hidden><Art name="puff" eager /></span>
          <span className={`${s.cloud} ${s.cloud2}`} aria-hidden><Art name="puff" eager /></span>
          <div className={s.coverTop}>
            <p className={s.tag}>Undangan {label}</p>
            <h1 className={s.coverName}>{names}</h1>
            {age && <p className={s.ageRow}>yang ke <span className={s.ageClock}>{age}</span> tahun</p>}
            <p className={s.coverDate}>{formatDate(data.date)}</p>
          </div>
          <div className={s.line}>
            <Art name="station" eager className={s.coverStation} />
            <Train letters={letters} eager className={s.coverTrain} />
            <span className={s.rails} aria-hidden />
          </div>
          <div className={s.ticket}>
            <span className={s.ticketHead}>Tiket Pesta · Peron 1</span>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={18} color="#fff6e6" />Ayo Naik Kereta!</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        celebrant
        noPhotos={!child?.photo && !data.couple.bridePhoto}
        light="#fff6e6"
        dark="#275ea3"
        copy={copy}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            <p className={s.heroKicker}>Pesta {label}</p>
            <h1 className={s.heroName}>{names}</h1>
            {age && <p className={s.heroAge}>genap <b>{age}</b> tahun</p>}
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
            <div className={s.heroLine} aria-hidden>
              <Art name="station" className={s.heroStation} />
              <Art name="cake" className={s.heroCake} />
              <span className={s.rails} />
            </div>
          </header>
        )}
        slots={{
          divider: <span className={s.divider} aria-hidden />,
          node: <Art name="puff" />,
          portrait: <Art name="cake" className={s.peek} />,
          countDecor: <span className={s.countRails} aria-hidden />,
          closingDecor: <span className={s.closingRails} aria-hidden />,
          closingEmblem: <Train letters={letters} className={s.closingTrain} />,
          sentArt: <Art name="cake" />,
        }}
      />
    </ThemeShell>
  );
}
