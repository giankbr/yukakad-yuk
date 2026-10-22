"use client";
// Theme "Ultah Antariksa" — ulang tahun anak di luar angkasa: langit malam gouache, roket krem-merah yang melayang dengan
// api berkedip, planet bercincin, bulan tersenyum, helm astronaut sebagai bingkai foto/monogram, bintang sebagai pemisah.
import { Lucide, ThemeShell, formatDate, guestLabel, toDate, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Exo 2:wght@600;700;800", "Quicksand:wght@500;600;700"];
// Painted by /tmp/pen/art/themes/ultah-antariksa.py (tools/art/themes in the repo).
const Art = makeArt("ultah-antariksa", {
  rocket: [220, 397], flame: [113, 235], planet: [300, 157], planet2: [130, 131], moon: [220, 220], helmet: [260, 280], star: [72, 69],
} as const);

function ageAt(birth?: string, at?: string) {
  const b = toDate(birth);
  const d = toDate(at);
  if (!b || !d) return undefined;
  let age = d.getFullYear() - b.getFullYear();
  if (d.getMonth() < b.getMonth() || (d.getMonth() === b.getMonth() && d.getDate() < b.getDate())) age -= 1;
  return age > 0 && age < 30 ? age : undefined;
}

function Stars() {
  return <span className={s.divider} aria-hidden><Art name="star" /><Art name="star" /><Art name="star" /></span>;
}

export default function UltahAntariksaTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Ulang Tahun";
  const child = data.extras?.child?.enabled !== false && data.extras?.child?.name?.trim() ? data.extras.child : undefined;
  const nick = child?.nickname?.trim() || child?.name.trim() || data.couple.bride;
  const names = child ? nick : [data.couple.bride, data.couple.groom?.trim()].filter(Boolean).join(" & ");
  const age = ageAt(child?.birthDate, data.date);
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const copy = {
    ...DEFAULT_COPY,
    opening: {
      kicker: "Halo, Kru Cilik!",
      title: "Ayo Terbang ke Pestaku!",
      intro: `Dengan penuh sukacita, kami mengundang teman-teman dan keluarga untuk merayakan ${label.toLowerCase()} ${names}${age ? ` yang ke-${age}` : ""}. Kehadiran dan doa kalian akan membuat misi kali ini makin seru!`,
    },
    roles: ["Kapten Misi", "Bersama"] as [string, string],
    couple: ["Kenalan dengan Kapten", child ? "Si Astronaut Kecil" : "Yang Merayakan"] as [string, string],
    count: ["Hitung Mundur Peluncuran", "Menuju Hari Pesta"] as [string, string],
    units: ["Hari", "Jam", "Menit", "Detik"] as [string, string, string, string],
    events: ["Jadwal Misi", "Waktu & Tempat"] as [string, string],
    story: ["Catatan Perjalanan", `Cerita ${nick}`] as [string, string],
    gallery: ["Album", "Momen Seru"] as [string, string],
    wishes: ["Kirim Sinyal", "Ucapan & Kehadiran"] as [string, string],
    gifts: ["Tanda Sayang", "Kado & Amplop Digital"] as [string, string],
    closing: { thanks: "Terima Kasih!", text: `Sampai jumpa di landasan peluncuran! Kehadiran dan doa teman-teman adalah hadiah paling seru untuk ${names}.` },
    wishPlaceholder: `Tuliskan ucapan dan doa untuk ${names}…`,
    sent: "Sinyal diterima! Terima kasih atas ucapannya.",
  };

  return (
    <ThemeShell
      fonts={FONTS}
      background="#1b2452"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Art name="planet" eager className={s.planet} />
          <Art name="moon" eager className={s.moon} />
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
          <div className={s.pad} aria-hidden>
            <Art name="planet2" eager className={s.planet2} />
            <Art name="flame" eager className={s.flame} />
            <Art name="rocket" eager className={s.rocket} />
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        celebrant
        noPhotos={!child?.photo && !data.couple.bridePhoto}
        light="#fff1c8"
        dark="#1b2452"
        copy={copy}
        hero={(
          <header className={s.hero}>
            <Art name="moon" className={s.moon} />
            <p className={s.heroKicker}>Hore! {label}</p>
            <h1 className={s.heroName}>{names}{age ? ` ${age} Tahun` : ""}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            <Art name="planet" className={s.heroPlanet} />
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Stars />,
          node: <Art name="star" />,
          portrait: <Art name="helmet" className={s.helmet} />,
          countDecor: <><Art name="planet" className={`${s.countPlanet} ${s.countPlanetA}`} /><Art name="planet2" className={`${s.countPlanet} ${s.countPlanetB}`} /></>,
          closingDecor: <Art name="moon" className={s.closingMoon} />,
          closingEmblem: (
            <div className={s.launch} aria-hidden>
              <Art name="flame" className={s.flame} />
              <Art name="rocket" className={s.rocket} />
            </div>
          ),
          sentArt: <Art name="rocket" />,
        }}
      />
    </ThemeShell>
  );
}
