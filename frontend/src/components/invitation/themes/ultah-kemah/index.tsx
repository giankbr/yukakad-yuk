"use client";
// Theme "Ultah Kemah" — pesta ulang tahun anak berkemah di halaman belakang: papan kayu bergantung di bawah lampu untai,
// burung hantu bertopi pesta, tenda oranye yang menyala dari dalam, api unggun berkedip dengan marshmallow, langit malam
// berbintang (semua lukisan gouache orisinal bergaya buku cerita), kartu badge berjahit ala pramuka.
import { Lucide, ThemeShell, formatDate, guestLabel, toDate, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Titan One", "Baloo 2:wght@500;600;700;800", "Caveat Brush"];
// Painted by /tmp/pen/art/themes/ultah-kemah.py.
const Art = makeArt("ultah-kemah", {
  lights: [780, 149], scene: [800, 396], flame: [140, 168], owl: [200, 196], marsh: [400, 35], pines: [800, 199],
} as const);

const WISHES = [
  { id: "w1", name: "Kirana & Mama", attendance: "yes" as const, message: "Selamat ulang tahun, Elang! Kirana sudah siapkan senter paling terang. Semoga sehat, berani, dan makin pintar." },
  { id: "w2", name: "Keluarga Om Fajar", attendance: "yes" as const, message: "Tujuh tahun, sudah jadi kepala regu! Semoga harimu hangat seperti api unggun dan seru seperti cerita malam." },
  { id: "w3", name: "Tante Dinda", attendance: "maybe" as const, message: "Tante usahakan datang sebelum api unggun dinyalakan. Peluk jauh dulu ya, Sayang!" },
];

function ageAt(birth?: string, at?: string) {
  const b = toDate(birth);
  const d = toDate(at);
  if (!b || !d) return undefined;
  let age = d.getFullYear() - b.getFullYear();
  if (d.getMonth() < b.getMonth() || (d.getMonth() === b.getMonth() && d.getDate() < b.getDate())) age -= 1;
  return age > 0 && age < 30 ? age : undefined;
}

export default function UltahKemahTheme(props: ThemeProps) {
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
      background="#14203a"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Art name="lights" eager className={s.lights} />
          <Art name="owl" eager className={s.owl} />
          <div className={s.sign}>
            <p className={s.kicker}>Undangan {label}</p>
            <h1 className={s.coverNames}>{names}</h1>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
            {age && <p className={s.age}><span><b>{age}</b>tahun</span></p>}
          </div>
          <div className={s.scene}>
            <Art name="scene" eager />
            <Art name="flame" eager className={s.flame} />
          </div>
          <div className={s.coverFoot}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={18} color="#ffffff" />Buka Undangan</button>
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
        dark="#1f3f3a"
        demoWishes={WISHES}
        copy={{
          opening: {
            kicker: "Halo, para petualang cilik!",
            title: "Ayo Berkemah Bersama",
            intro: `Dengan penuh sukacita, kami mengundang teman-teman dan keluarga untuk merayakan ${label.toLowerCase()} ${names}${age ? ` yang ke-${age}` : ""}. Kita pasang tenda, bakar marshmallow, dan menghitung bintang di sekitar api unggun!`,
          },
          roles: ["Yang Berulang Tahun", "Bersama"],
          couple: ["Kenalan yuk", child ? "Si Kepala Regu" : "Yang Merayakan"],
          count: ["Siapkan senter", "Menuju Malam Kemah"],
          units: ["Hari", "Jam", "Menit", "Detik"],
          events: ["Catat tanggalnya", "Waktu & Tempat"],
          story: ["Cerita di api unggun", `Cerita ${nick}`],
          gallery: ["Album", "Foto Ceria"],
          wishes: ["Kirim doa terbaik", "Ucapan & Kehadiran"],
          gifts: ["Tanda sayang", "Kado & Amplop Digital"],
          closing: { thanks: "Terima Kasih!", text: `Kehadiran dan doa teman-teman membuat malam kemah ${names} makin hangat. Sampai jumpa di api unggun!` },
          sent: "Hore! Ucapanmu sudah sampai di tenda. Terima kasih!",
          attend: { maybe: "Mungkin" },
          wishPlaceholder: "Tulis ucapan dan doa untuk si kecil…",
          closedNote: "Terima kasih sudah ikut merayakan! Ucapan masih bisa dikirim lewat form ini.",
          giftIntro: "Kehadiran teman-teman sudah jadi hadiah paling indah. Bila ingin memberi tanda sayang, dapat melalui:",
          familyLabel: "Dengan sayang,",
        }}
        hero={(
          <header className={s.hero}>
            <Art name="lights" className={s.heroLights} />
            <div className={s.heroPatch}>
              <p className={s.heroKicker}>Pesta {label}</p>
              <h1 className={s.heroNames}>{names}</h1>
              {age && <span className={s.heroAge}>{age} tahun</span>}
            </div>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
            <Art name="marsh" className={s.heroMarsh} />
          </header>
        )}
        slots={{
          divider: <Art name="marsh" className={s.divider} />,
          node: <Art name="flame" />,
          amp: <Art name="flame" />,
          portrait: <Art name="owl" />,
          countDecor: <span className={s.countDecor} aria-hidden><Art name="lights" /></span>,
          closingDecor: <span className={s.closingPines} aria-hidden><Art name="pines" /></span>,
          closingEmblem: <Art name="owl" className={s.closingEmblem} />,
          sentArt: <Art name="flame" />,
        }}
      />
    </ThemeShell>
  );
}
