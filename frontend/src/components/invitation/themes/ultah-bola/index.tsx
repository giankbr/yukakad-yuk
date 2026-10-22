"use client";
// Theme "Ultah Bola" — ulang tahun anak di hari pertandingan: lapangan rumput gouache bergaris potong dengan garis kapur,
// jersi merah polos yang diberi nama & nomor umur si anak (teks, bukan gambar), bola jahit memantul, papan skor, tiket
// masuk, gawang berjaring, piala emas, bendera segitiga. Tanpa logo klub atau merek apa pun.
import type { CSSProperties } from "react";
import { Lucide, ThemeShell, formatDate, guestLabel, toDate, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Bowlby One", "Graduate", "Nunito:wght@500;600;700;800"];
// Painted by /tmp/pen/art/themes/ultah-bola.py (tools/art/themes in the repo).
const Art = makeArt("ultah-bola", { chalk: [560, 376], ball: [220, 220], jersey: [360, 376], trophy: [260, 328], net: [520, 268], bunting: [640, 104] } as const);

const WISHES = [
  { id: "w1", name: "Keluarga Om Bayu", attendance: "yes" as const, message: "Selamat ulang tahun, jagoan! Semoga makin sehat, makin pintar, dan terus semangat berlatih. Sampai ketemu di lapangan!" },
  { id: "w2", name: "Kenzo & Mama", attendance: "yes" as const, message: "Kenzo sudah siap adu penalti! Selamat ulang tahun, semoga jadi kapten tim yang baik hati." },
  { id: "w3", name: "Tante Sari", attendance: "maybe" as const, message: "Maaf kalau belum bisa datang, ya. Doa Tante, semoga sehat selalu dan jadi anak yang soleh dan sportif." },
];

function ageAt(birth?: string, at?: string) {
  const b = toDate(birth);
  const d = toDate(at);
  if (!b || !d) return undefined;
  let age = d.getFullYear() - b.getFullYear();
  if (d.getMonth() < b.getMonth() || (d.getMonth() === b.getMonth() && d.getDate() < b.getDate())) age -= 1;
  return age > 0 && age < 30 ? age : undefined;
}

function Divider() {
  return <span className={s.divider} aria-hidden><i /><Art name="ball" /><i /></span>;
}

export default function UltahBolaTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Ulang Tahun";
  const child = data.extras?.child?.enabled !== false && data.extras?.child?.name?.trim() ? data.extras.child : undefined;
  const nick = child?.nickname?.trim() || child?.name.trim() || data.couple.bride;
  const names = child ? nick : [data.couple.bride, data.couple.groom?.trim()].filter(Boolean).join(" & ");
  const age = ageAt(child?.birthDate, data.date);
  const shirtNo = age ? String(age) : nick.slice(0, 1).toUpperCase();
  const shirtName = nick.split(/\s+/)[0] ?? nick;
  const nameSize: CSSProperties = { fontSize: Math.max(12, Math.min(22, Math.floor(170 / Math.max(shirtName.length, 1)))) };
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const copy = {
    ...DEFAULT_COPY,
    opening: {
      kicker: "Peluit Dibunyikan",
      title: "Ayo ke Lapangan!",
      intro: `Dengan penuh sukacita, kami mengundang teman-teman dan keluarga untuk merayakan ${label.toLowerCase()} ${names}${age ? ` yang ke-${age}` : ""}. Datang, bermain, dan bersorak bersama, kehadiran kalian membuat hari ini jadi kemenangan besar!`,
    },
    roles: ["Yang Berulang Tahun", "Bersama"] as [string, string],
    couple: ["Kenalan, Yuk", child ? "Pemain Bintang" : "Yang Merayakan"] as [string, string],
    count: ["Papan Skor", "Menuju Hari Pertandingan"] as [string, string],
    units: ["Hari", "Jam", "Menit", "Detik"] as [string, string, string, string],
    events: ["Jadwal Laga", "Waktu & Tempat"] as [string, string],
    story: ["Perjalanan Karier", `Cerita ${nick}`] as [string, string],
    gallery: ["Album", "Momen Seru"] as [string, string],
    wishes: ["Sorakan & Doa", "Ucapan & Kehadiran"] as [string, string],
    gifts: ["Tanda Sayang", "Kado & Amplop Digital"] as [string, string],
    closing: { thanks: "Terima Kasih!", text: `Sampai jumpa di lapangan! Sorakan, kehadiran, dan doa teman-teman adalah piala paling berharga untuk ${names}.` },
    sent: "Gol! Ucapanmu sudah terkirim. Terima kasih banyak.",
  };

  return (
    <ThemeShell
      fonts={FONTS}
      background="#3f9a48"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Art name="bunting" eager className={s.bunting} />
          <div className={s.board}><i /><p>Undangan {label}</p><i /></div>
          <h1 className={s.coverName}>{names}</h1>
          <div className={s.kit} aria-hidden>
            <Art name="chalk" eager className={s.chalk} />
            <div className={s.shirt}>
              <Art name="jersey" eager />
              <span className={s.shirtName} style={nameSize}>{shirtName}</span>
              <span className={s.shirtNo}>{shirtNo}</span>
            </div>
            <span className={s.ballShadow} />
            <Art name="ball" eager className={s.ball} />
          </div>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.ticket}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
          </div>
          <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={17} color="#22336b" />Buka Undangan</button>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        celebrant
        noPhotos={!child?.photo && !data.couple.bridePhoto}
        light="#ffffff"
        dark="#22336b"
        copy={copy}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            <Art name="net" className={s.net} />
            <Art name="ball" className={s.heroBall} />
            <p className={s.heroKicker}>Hari Pertandingan</p>
            <h1 className={s.heroName}>{names}</h1>
            {age && <p className={s.heroAge}>genap <b>{age}</b> tahun</p>}
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Divider />,
          node: <Art name="ball" />,
          portrait: <Art name="ball" className={s.peek} />,
          countDecor: <Art name="bunting" className={s.countBunting} />,
          closingDecor: <Art name="bunting" className={s.closingBunting} />,
          closingEmblem: <div className={s.trophyWrap} aria-hidden><Art name="trophy" className={s.trophy} /></div>,
          sentArt: <Art name="trophy" />,
        }}
      />
    </ThemeShell>
  );
}
