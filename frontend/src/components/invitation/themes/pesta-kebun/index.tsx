"use client";
// Theme "Pesta Kebun" — pesta ulang tahun dewasa di kebun saat senja, dilukis dengan cat air dan gouache: langit
// lavender-jingga dengan barisan pohon di kejauhan, meja panjang berlinen dengan stoples bunga liar, lilin dalam kaca
// dan kue bertingkat, lampu bohlam yang berayun, pohon dengan lampion kertas, dan buket bunga liar dalam stoples.
// Nama tamu ditulis tangan di label kertas kraft; foto yang berulang tahun berupa polaroid yang tergantung di tali
// lampu; hero berupa buket di depan angka umur yang besar.
import { Lucide, ThemeShell, formatDate, guestLabel, toDate, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Petrona:ital,wght@0,400;0,500;0,600;1,400;1,500", "Karla:wght@400;500;700", "Homemade Apple"];
// Painted by /tmp/pen/art/themes/pesta-kebun.py (tools/art/themes in the repo).
const Art = makeArt("pesta-kebun", {
  lights: [420, 100], tree: [280, 430], table: [420, 175], bouquet: [180, 267], sprig: [200, 34],
} as const);

const WISHES = [
  { id: "w1", name: "Sekar & Dimas", attendance: "yes" as const, message: "Selamat ulang tahun ke-30, Laras! Sudah tidak sabar duduk di meja panjangmu. Semoga kebun dan hatimu selalu berbunga." },
  { id: "w2", name: "Geng Kos Dago", attendance: "yes" as const, message: "Dari mi instan tengah malam sampai makan malam di kebun. Bangga sama kamu! Sehat dan bahagia selalu, Ras." },
  { id: "w3", name: "Mbak Wulan", attendance: "maybe" as const, message: "Semoga bisa menyusul dari Solo. Selamat berkepala tiga, semoga tahun-tahun terbaikmu baru dimulai." },
];

function ageAt(birth?: string, at?: string) {
  const b = toDate(birth);
  const d = toDate(at);
  if (!b || !d) return undefined;
  let age = d.getFullYear() - b.getFullYear();
  if (d.getMonth() < b.getMonth() || (d.getMonth() === b.getMonth() && d.getDate() < b.getDate())) age -= 1;
  return age > 0 && age < 120 ? age : undefined;
}

export default function PestaKebunTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pesta Ulang Tahun";
  const child = data.extras?.child?.enabled !== false && data.extras?.child?.name?.trim() ? data.extras.child : undefined;
  const nick = child?.nickname?.trim() || child?.name.trim() || data.couple.bride;
  const names = child ? nick : [data.couple.bride, data.couple.groom?.trim()].filter(Boolean).join(" & ");
  const age = ageAt(child?.birthDate, data.date);
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const copy = {
    ...DEFAULT_COPY,
    opening: {
      kicker: "Halo, sahabat!",
      title: "Mari rayakan bersama",
      intro: `Dengan hati yang penuh syukur, kami mengundang Anda untuk merayakan ulang tahun ${names}${age ? ` yang ke-${age}` : ""} dalam makan malam sederhana di kebun, di bawah lampu-lampu kecil dan langit senja. Kehadiran Anda adalah hadiah yang paling kami nantikan.`,
    },
    roles: ["Yang Berulang Tahun", "Bersama"] as [string, string],
    couple: ["Bintang malam ini", "Yang Berulang Tahun"] as [string, string],
    count: ["Saat lampu dinyalakan", "Menuju Malam Perayaan"] as [string, string],
    units: ["Hari", "Jam", "Menit", "Detik"] as [string, string, string, string],
    events: ["Di bawah lampu", "Waktu & Tempat"] as [string, string],
    story: [age ? `${age} tahun perjalanan` : "Perjalanan", `Cerita ${nick}`] as [string, string],
    gallery: ["Kenangan", "Galeri"] as [string, string],
    wishes: ["Angkat gelas", "Ucapan & Kehadiran"] as [string, string],
    gifts: ["Tanda sayang", "Kado & Amplop Digital"] as [string, string],
    closing: { thanks: "Terima kasih", text: "Terima kasih sudah menjadi bagian dari perjalanan ini. Sampai jumpa di meja panjang, di bawah lampu-lampu kecil." },
    attend: { maybe: "Mungkin" },
    sent: "Terima kasih! Ucapanmu sudah sampai di meja panjang.",
    wishPlaceholder: `Tuliskan ucapan dan doa untuk ${nick}…`,
    giftIntro: "Kehadiran Anda sudah lebih dari cukup. Bila ingin memberi tanda sayang, dapat melalui:",
    familyLabel: "Salam hangat,",
  };

  return (
    <ThemeShell
      fonts={FONTS}
      background="#2f2c4a"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Art name="tree" eager className={`${s.coverTree} ${s.coverTreeL}`} />
          <Art name="tree" eager className={`${s.coverTree} ${s.coverTreeR}`} />
          <Art name="lights" eager className={`${s.coverLights} ${s.coverLights1}`} />
          <Art name="lights" eager className={`${s.coverLights} ${s.coverLights2}`} />
          <Art name="table" eager className={s.coverTable} />
          <p className={s.kicker}>Undangan {label}</p>
          <h1 className={s.coverName}>{names}</h1>
          {age && <p className={s.ageLine}>merayakan <b>{age}</b> tahun</p>}
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.tag}>
            <div className={s.guest}>
              <small>Untuk</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
          </div>
          <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#2e2a3a" />Buka Undangan</button>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        celebrant
        light="#fbf2e2"
        dark="#2e2a3a"
        copy={copy}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            <p className={s.heroKicker}>{label}</p>
            <div className={s.heroStage}>
              {age && <span className={s.heroAge} aria-hidden>{age}</span>}
              <span className={s.heroJar} aria-hidden><Art name="bouquet" /></span>
            </div>
            <h1 className={s.heroName}>{names}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <span className={s.divider} aria-hidden><Art name="sprig" /></span>,
          node: null,
          amp: <Art name="sprig" />,
          portrait: <span className={s.portraitLights} aria-hidden><Art name="lights" /></span>,
          countDecor: <Art name="lights" className={s.countLights} />,
          closingDecor: (
            <>
              <Art name="lights" className={s.closeLights} />
              <Art name="tree" className={`${s.closeTree} ${s.closeTreeL}`} />
              <Art name="tree" className={`${s.closeTree} ${s.closeTreeR}`} />
              <Art name="table" className={s.closeTable} />
            </>
          ),
          closingEmblem: <Art name="bouquet" className={s.closingEmblem} />,
          sentArt: <Art name="bouquet" />,
        }}
      />
    </ThemeShell>
  );
}
