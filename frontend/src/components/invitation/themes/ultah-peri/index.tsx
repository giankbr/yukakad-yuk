"use client";
// Theme "Ultah Peri" — ulang tahun anak di hutan peri saat senja: jamur merah bertotol yang bercahaya, bunga lonceng,
// pakis dan batang pohon lembayung (cat air + gouache), Kiki si peri kecil (tokoh orisinal) yang melayang, dan
// kunang-kunang yang berkedip di sampul, hitung mundur, dan penutup.
import type { CSSProperties } from "react";
import { Lucide, ThemeShell, formatDate, guestLabel, toDate, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Cherry Swash:wght@400;700", "Nunito:wght@400;600;700;800"];
// Painted by /tmp/pen/art/themes/ultah-peri.py (tools/art/themes in the repo).
const Art = makeArt("ultah-peri", { hutan: [720, 604], peri: [260, 312], jamur: [220, 194], sulur: [420, 70] } as const);

const FLIES: [number, number, number][] = [[12, 18, 0], [82, 30, 1.1], [24, 52, 2.3], [70, 64, .6], [46, 12, 1.8], [90, 78, 2.9], [6, 84, 1.4], [58, 40, 3.4]];

function Flies({ className }: { className?: string }) {
  return (
    <span className={className} aria-hidden>
      {FLIES.map(([x, y, d]) => <span key={`${x}-${y}`} className={s.fly} style={{ left: `${x}%`, top: `${y}%`, animationDelay: `${d}s, ${d / 2}s` } as CSSProperties} />)}
    </span>
  );
}

const WISHES = [
  { id: "w1", name: "Tante Rini & Om Yoga", attendance: "yes" as const, message: "Selamat ulang tahun kelima, Naura sayang! Semoga tumbuh sehat, ceria, dan baik hati seperti peri di cerita kesukaanmu." },
  { id: "w2", name: "Raisa (teman TK)", attendance: "yes" as const, message: "Naura, aku datang pakai sayap ungu ya! Selamat ulang tahun!" },
  { id: "w3", name: "Keluarga Om Bagas", attendance: "maybe" as const, message: "Maaf belum pasti bisa datang. Doa terbaik untuk Naura, semoga harinya penuh tawa." },
];

function ageAt(birth?: string, at?: string) {
  const b = toDate(birth);
  const d = toDate(at);
  if (!b || !d) return undefined;
  let age = d.getFullYear() - b.getFullYear();
  if (d.getMonth() < b.getMonth() || (d.getMonth() === b.getMonth() && d.getDate() < b.getDate())) age -= 1;
  return age > 0 && age < 30 ? age : undefined;
}

export default function UltahPeriTheme(props: ThemeProps) {
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
      kicker: "Halo, Teman-teman Peri!",
      title: "Ayo Datang ke Pestaku!",
      intro: `Dengan penuh sukacita, kami mengundang teman-teman dan keluarga untuk merayakan ${label.toLowerCase()} ${names}${age ? ` yang ke-${age}` : ""}. Kehadiran dan doa kalian akan membuat hari ini makin ajaib!`,
    },
    roles: ["Yang Berulang Tahun", "Bersama"],
    couple: ["Kenalan Dulu, Yuk", child ? "Si Peri Kecil" : "Yang Merayakan"],
    count: ["Kunang-kunang Menghitung", "Menuju Hari Pesta"],
    units: ["Hari", "Jam", "Menit", "Detik"],
    events: ["Catat Tanggalnya", "Waktu & Tempat"],
    story: ["Dongeng Kecil", `Cerita ${nick}`],
    gallery: ["Album", "Momen Ajaib"],
    wishes: ["Kirim Doa", "Ucapan & Kehadiran"],
    gifts: ["Tanda Sayang", "Kado & Amplop Digital"],
    closing: { thanks: "Terima Kasih!", text: `Sampai jumpa di hutan peri! Kehadiran dan doa teman-teman adalah hadiah paling ajaib untuk ${names}.` },
    sent: "Hore, ucapanmu sudah sampai ke hutan peri! Terima kasih banyak.",
    attend: { maybe: "Mungkin" },
    wishPlaceholder: `Tuliskan doa dan ucapan untuk ${names}…`,
    giftIntro: "Kehadiran teman-teman sudah jadi kado terindah. Jika ingin memberi tanda sayang, dapat melalui:",
    familyLabel: "Salam sayang dari keluarga",
  };

  return (
    <ThemeShell
      fonts={FONTS}
      background="#2a2452"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <span className={s.moon} aria-hidden />
          <Flies className={s.flies} />
          <p className={s.pill}>Undangan {label}</p>
          <h1 className={s.coverName}>{names}</h1>
          {age && <p className={s.age}>ulang tahun ke <b>{age}</b></p>}
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.guestWrap}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={17} color="#ffffff" />Buka Undangan</button>
          </div>
          <div className={s.stage} aria-hidden>
            <span className={s.periWrap}><Art name="peri" eager className={s.peri} /></span>
            <Art name="hutan" eager className={s.hutan} />
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        celebrant
        noPhotos={!child?.photo && !data.couple.bridePhoto}
        demoWishes={WISHES}
        light="#ffe3a3"
        dark="#553896"
        copy={copy}
        hero={(
          <header className={s.hero}>
            <p className={s.heroKicker}>Hore! {label}</p>
            <h1 className={s.heroName}>{names}{age ? ` ${age} Tahun` : ""}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
            <div className={s.heroStage} aria-hidden>
              <Art name="jamur" className={s.heroJamur} />
              <Art name="peri" className={s.heroPeri} />
            </div>
          </header>
        )}
        slots={{
          divider: <Art name="sulur" className={s.divider} />,
          node: <Art name="jamur" />,
          portrait: <Art name="jamur" className={s.peek} />,
          countDecor: <Flies />,
          closingEmblem: (
            <>
              <Art name="peri" className={s.closingPeri} />
              <p className={s.closingName}>{names}</p>
            </>
          ),
          sentArt: <Art name="jamur" />,
        }}
      />
    </ThemeShell>
  );
}
