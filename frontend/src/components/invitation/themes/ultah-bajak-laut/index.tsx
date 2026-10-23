"use client";
// Theme "Ultah Bajak Laut" — a kids' pirate-adventure birthday drawn as a treasure map (original designs, watercolour
// with a sepia dip-pen line): parchment with a faint map grid, a chunky friendly wooden ship under striped sails (its
// black flag carries a smiling eye-patch face, no skulls), a dotted trail marching to a palm island marked with a red X,
// a parrot perched on the invitation note, a brass telescope and a compass. Countdown numbers sit on gold coins over the
// open sea; the gifts are a treasure chest. Playful, springy motion.
import { Lucide, ThemeShell, formatDate, guestLabel, toDate, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Titan One", "Baloo 2:wght@400;500;600;700;800", "Gochi Hand"];
// Painted by /tmp/pen/art/themes/ultah-bajak-laut.py (tools/art/themes in the repo).
const Art = makeArt("ultah-bajak-laut", {
  ship: [360, 314], island: [320, 210], parrot: [170, 241], telescope: [220, 76], chest: [220, 222], compass: [150, 150], divider: [280, 25],
} as const);

const WISHES = [
  { id: "w1", name: "Tante Mira & Kak Dafa", attendance: "yes" as Attendance, message: "Selamat ulang tahun, Kapten Raka! Semoga makin berani, sehat, dan selalu baik hati pada semua kru kapalnya." },
  { id: "w2", name: "Bu Guru Ani (SD Tunas Bangsa)", attendance: "yes" as Attendance, message: "Selamat ulang tahun yang ke-7, Raka sayang. Teruslah rajin membaca peta dan bertanya tentang dunia, ya." },
  { id: "w3", name: "Keluarga Om Bayu", attendance: "maybe" as Attendance, message: "Kami belum tentu bisa ikut berlayar. Selamat ulang tahun, Raka, semoga semua harta karun mimpimu ketemu!" },
];

function ageAt(birth?: string, at?: string) {
  const b = toDate(birth);
  const d = toDate(at);
  if (!b || !d) return undefined;
  let age = d.getFullYear() - b.getFullYear();
  if (d.getMonth() < b.getMonth() || (d.getMonth() === b.getMonth() && d.getDate() < b.getDate())) age -= 1;
  return age > 0 && age < 30 ? age : undefined;
}

export default function UltahBajakLautTheme(props: ThemeProps) {
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
      kicker: "Ahoy, Teman-Teman!",
      title: "Ayo Berlayar Bersama!",
      intro: `Kapal sudah siap, peta sudah di tangan! ${names} mengajak kamu ikut berlayar merayakan ${label.toLowerCase()}${age ? ` yang ke-${age}` : ""}: mengikuti jejak titik-titik, menyeberangi lautan, dan menemukan harta karun di Pulau Rahasia. Bawa senyum terbaikmu, kru!`,
    },
    roles: ["Kapten yang Berulang Tahun", "Bersama"],
    couple: ["Pos 1 · Dek Kapten", child ? "Kenalan dengan Kapten" : "Yang Merayakan"],
    count: ["Pos 2 · Lautan Lepas", "Hitung Mundur Berlayar"],
    units: ["Hari", "Jam", "Menit", "Detik"],
    events: ["Pos 3 · Tanda X", "Waktu & Tempat Pesta"],
    story: ["Pos 4 · Buku Harian Kapal", `Petualangan ${nick}`],
    gallery: ["Pos 5 · Album", "Foto Petualangan"],
    wishes: ["Pos 6 · Pesan dalam Botol", "Ucapan untuk Kapten"],
    gifts: ["Peti Harta Karun", "Kado & Amplop Digital"],
    closing: { thanks: "Terima Kasih, Kru!", text: `Sampai jumpa di kapal! Kehadiran dan doa teman-teman adalah harta karun paling berharga untuk ${names}.` },
    sent: "Hore, pesan dalam botolmu sudah sampai ke kapal! Terima kasih.",
    wishPlaceholder: `Tulis ucapan & doa untuk ${nick}…`,
    giftIntro: "Kehadiran teman-teman sudah jadi harta karun terbesar. Jika ingin memberi tanda sayang, bisa melalui:",
    familyLabel: "Salam dari kru kapal",
  };

  return (
    <ThemeShell
      fonts={FONTS}
      background="#d9c194"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.mapArt} aria-hidden><Art name="compass" eager className={s.compass} /></div>
          <p className={s.ribbon}>Undangan {label}</p>
          <h1 className={s.coverName}>{names}</h1>
          {age && <p className={s.ageRow}>ulang tahun ke <span className={s.age}>{age}</span></p>}
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.voyage} aria-hidden>
            <svg className={s.trail} viewBox="0 0 390 290" preserveAspectRatio="none"><path d="M120 150 C 150 230, 210 250, 250 210 S 300 170, 320 222" /></svg>
            <Art name="ship" eager className={s.ship} />
            <Art name="island" eager className={s.island} />
            <Art name="telescope" eager className={s.telescope} />
          </div>
          <div className={s.note}>
            <Art name="parrot" eager className={s.parrot} />
            <span>Surat untuk kru kapal</span>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={18} color="#fffaf0" />Ayo Berlayar!</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        celebrant
        noPhotos={!child?.photo && !data.couple.bridePhoto}
        light="#fffaf0"
        dark="#3e2717"
        copy={copy}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            <Art name="ship" className={s.heroShip} />
            <p className={s.heroKicker}>Hore, {label.toLowerCase()}!</p>
            <h1 className={s.heroName}>{names}{age && <span className={s.heroAge}>{age} Tahun</span>}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="divider" className={s.divider} />,
          node: <Art name="compass" />,
          portrait: <Art name="parrot" />,
          countDecor: <Art name="ship" className={s.countShip} />,
          closingEmblem: (
            <>
              <Art name="island" className={s.closingIsland} />
              <p className={s.closingName}>{names}</p>
              <Art name="chest" className={s.giftsChest} />
            </>
          ),
          sentArt: <Art name="chest" />,
        }}
      />
    </ThemeShell>
  );
}
