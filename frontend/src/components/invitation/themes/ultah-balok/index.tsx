"use client";
// Theme "Ultah Balok" — pesta ulang tahun anak di kota balok mainan: balok kayu polos warna-warni (kubus, atap segitiga,
// tiang silinder, jembatan lengkung; mainan generik tanpa merek), nama si kecil tersusun dari balok huruf yang jatuh satu
// per satu, kota balok di lantai kayu dengan bendera segitiga. Lukisan gouache orisinal bergaya buku cerita.
import type { CSSProperties } from "react";
import { Lucide, ThemeShell, formatDate, guestLabel, toDate, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Bowlby One", "Fredoka:wght@400;500;600;700"];
// Painted by /tmp/pen/art/themes/ultah-balok.py.
const Art = makeArt("ultah-balok", {
  city: [780, 446], tower: [181, 358], divider: [330, 46], "cube-r": [140, 140],
} as const);
const KEYS = ["r", "y", "b", "g"] as const;

const WISHES = [
  { id: "w1", name: "Nayla & Bunda", attendance: "yes" as const, message: "Selamat ulang tahun, Arsya! Nayla sudah latihan bikin menara paling tinggi. Semoga sehat, pintar, dan selalu ceria." },
  { id: "w2", name: "Om Fikri & Tante Rani", attendance: "yes" as const, message: "Empat tahun, sudah jadi arsitek cilik! Semoga cita-citamu setinggi menara balok dan sekuat jembatannya." },
  { id: "w3", name: "Keluarga Pak RT", attendance: "maybe" as const, message: "Kami usahakan mampir sore nanti. Peluk sayang untuk si kecil, semoga pestanya seru!" },
];

function ageAt(birth?: string, at?: string) {
  const b = toDate(birth);
  const d = toDate(at);
  if (!b || !d) return undefined;
  let age = d.getFullYear() - b.getFullYear();
  if (d.getMonth() < b.getMonth() || (d.getMonth() === b.getMonth() && d.getDate() < b.getDate())) age -= 1;
  return age > 0 && age < 30 ? age : undefined;
}

/** Split a name into rows of letter blocks (max 8 per row). */
function blockRows(name: string) {
  const rows: string[][] = [];
  for (const word of name.toUpperCase().split(/\s+/).filter(Boolean)) {
    const chars = Array.from(word);
    for (let i = 0; i < chars.length; i += 8) rows.push(chars.slice(i, i + 8));
  }
  return rows.slice(0, 3);
}

function LetterBlocks({ name }: { name: string }) {
  const rows = blockRows(name);
  const longest = Math.max(1, ...rows.map(r => r.length));
  const size = Math.min(76, Math.floor(340 / longest));
  const starts = rows.map((_, r) => rows.slice(0, r).reduce((sum, row) => sum + row.length, 0));
  return (
    <div className={s.blocks} style={{ "--bs": `${size}px` } as CSSProperties} aria-hidden>
      {rows.map((row, r) => (
        <div key={r} className={s.blockRow}>
          {row.map((ch, i) => {
            const n = starts[r] + i;
            const k = KEYS[n % 4];
            const style = { "--i": n, "--tilt": `${((n * 37) % 7) - 3}deg` } as CSSProperties;
            return <span key={i} className={`${s.block} ${s[`b${k}`]}`} style={style}><b>{ch}</b></span>;
          })}
        </div>
      ))}
    </div>
  );
}

export default function UltahBalokTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Ulang Tahun";
  const child = data.extras?.child?.enabled !== false && data.extras?.child?.name?.trim() ? data.extras.child : undefined;
  const nick = child?.nickname?.trim() || child?.name.trim() || data.couple.bride;
  const names = child ? nick : [data.couple.bride, data.couple.groom?.trim()].filter(Boolean).join(" & ");
  const age = ageAt(child?.birthDate, data.date);
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#fdf6e8"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <p className={s.kicker}>Undangan {label}</p>
          <h1 className={s.srName}>{names}</h1>
          <LetterBlocks name={names.replace(/&/g, " ")} />
          {age && <p className={s.age}><span className={`${s.block} ${s.by} ${s.ageBlock}`}><b>{age}</b></span><span>tahun</span></p>}
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <Art name="divider" eager className={s.coverDiv} />
          <div className={s.coverCity}><Art name="city" eager /></div>
          <div className={s.coverFoot}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={18} color="#ffffff" />Ayo Main ke Pesta!</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        celebrant
        noPhotos={!child?.photo && !data.couple.bridePhoto}
        light="#ffffff"
        dark="#2a2a3a"
        demoWishes={WISHES}
        copy={{
          opening: {
            kicker: "Halo, teman-teman pembangun!",
            title: "Ayo Bangun Kota Bersama",
            intro: `Dengan penuh sukacita, kami mengundang teman-teman dan keluarga untuk merayakan ${label.toLowerCase()} ${names}${age ? ` yang ke-${age}` : ""}. Kita susun balok, bangun menara setinggi-tingginya, lalu tiup lilin bersama!`,
          },
          roles: ["Yang Berulang Tahun", "Bersama"],
          couple: ["Kenalan, yuk", child ? "Si Arsitek Cilik" : "Yang Merayakan"],
          count: ["Balok demi balok", "Menuju Hari Pesta"],
          units: ["Hari", "Jam", "Menit", "Detik"],
          events: ["Catat tanggalnya", "Waktu & Tempat"],
          story: ["Cerita si kecil", `Cerita ${nick}`],
          gallery: ["Album", "Foto Ceria"],
          wishes: ["Kirim doa terbaik", "Ucapan & Kehadiran"],
          gifts: ["Tanda sayang", "Kado & Amplop Digital"],
          closing: { thanks: "Terima Kasih!", text: `Kehadiran dan doa teman-teman membuat kota balok ${names} makin ramai dan ceria. Sampai jumpa di pesta!` },
          sent: "Hore! Ucapanmu sudah tersusun rapi. Terima kasih!",
          attend: { maybe: "Mungkin" },
          wishPlaceholder: "Tulis ucapan dan doa untuk si kecil…",
          closedNote: "Terima kasih sudah ikut merayakan! Ucapan masih bisa dikirim lewat form ini.",
          giftIntro: "Kehadiran teman-teman sudah jadi hadiah paling indah. Bila ingin memberi tanda sayang, dapat melalui:",
          familyLabel: "Dengan sayang,",
        }}
        hero={(
          <header className={s.hero}>
            <Art name="tower" className={s.heroTower} />
            <div className={s.heroCard}>
              <p className={s.heroKicker}>Selamat {label}</p>
              <h1 className={s.heroNames}>
                {Array.from(names).map((ch, i) => <span key={i} className={s[`c${KEYS[i % 4]}`]}>{ch}</span>)}
              </h1>
              {age && <span className={s.heroAge}>ke-{age}</span>}
              <p className={s.heroDate}>{formatDate(data.date)}</p>
            </div>
            {note && <p className={s.heroNote}>{note}</p>}
            <Art name="divider" className={s.heroDiv} />
          </header>
        )}
        slots={{
          divider: <Art name="divider" className={s.divider} />,
          node: <span className={s.nodeBlock} aria-hidden />,
          amp: <Art name="cube-r" />,
          portrait: <Art name="tower" className={s.portraitTower} />,
          countDecor: <span className={s.countDecor} aria-hidden />,
          closingDecor: <span className={s.closingCity} aria-hidden><Art name="city" /></span>,
          closingEmblem: <Art name="tower" className={s.closingEmblem} />,
          sentArt: <Art name="tower" />,
        }}
      />
    </ThemeShell>
  );
}
