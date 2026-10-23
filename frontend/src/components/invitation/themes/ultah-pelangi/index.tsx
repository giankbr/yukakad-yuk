"use client";
// Theme "Ultah Pelangi" — ulang tahun anak dalam gouache lembut: pelangi besar dengan awan empuk di kakinya, matahari
// tersenyum yang sinarnya berputar pelan, seikat balon yang mengambang, awan yang melayang. Nama si kecil di atas papan
// awan putih; kartu bulat berpita pelangi dan hitung mundur berbentuk balon.
import { Lucide, ThemeShell, formatDate, guestLabel, toDate, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Shrikhand", "Comfortaa:wght@400;600;700", "Patrick Hand"];
// Painted by /tmp/pen/art/themes/ultah-pelangi.py
const Art = makeArt("ultah-pelangi", {
  rainbow: [640, 340], sun: [180, 179], rays: [260, 260], balloons: [260, 448], balloon: [80, 184], cloud: [320, 145], divider: [240, 97],
} as const);

const WISHES = [
  { id: "w1", name: "Raffa & Mama", attendance: "yes" as const, message: "Selamat ulang tahun, Kirana! Raffa sudah pilih topi warna hijau. Semoga sehat selalu, ceria, dan makin pintar." },
  { id: "w2", name: "Keluarga Om Dimas", attendance: "yes" as const, message: "Selamat empat tahun, Kirana sayang. Semoga hari-harimu selalu seterang pelangi." },
  { id: "w3", name: "Tante Sari", attendance: "maybe" as const, message: "Maaf belum tentu bisa datang, Sayang. Bukunya sudah Tante bungkus, peluk jauh dari Jakarta!" },
];

function ageAt(birth?: string, at?: string) {
  const b = toDate(birth);
  const d = toDate(at);
  if (!b || !d) return undefined;
  let age = d.getFullYear() - b.getFullYear();
  if (d.getMonth() < b.getMonth() || (d.getMonth() === b.getMonth() && d.getDate() < b.getDate())) age -= 1;
  return age > 0 && age < 30 ? age : undefined;
}

export default function UltahPelangiTheme(props: ThemeProps) {
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
      background="#bfe3f5"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <span className={s.sunWrap} aria-hidden><Art name="rays" eager className={s.rays} /><Art name="sun" eager className={s.sunFace} /></span>
          <span className={`${s.drifter} ${s.drifterA}`} aria-hidden><Art name="cloud" eager /></span>
          <Art name="rainbow" eager className={s.coverRainbow} />
          <span className={`${s.drifter} ${s.drifterB}`} aria-hidden><Art name="cloud" eager /></span>
          <span className={s.balloons} aria-hidden><Art name="balloons" eager /></span>
          <span className={s.balloonR} aria-hidden><Art name="balloon" eager /></span>
          <div className={s.board}>
            <p className={s.kicker}>Undangan {label}</p>
            <h1 className={s.coverNames}>{names}</h1>
            {age && <p className={s.age}><b>{age}</b>tahun ceria</p>}
            <p className={s.coverDate}>{formatDate(data.date)}</p>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
          </div>
          <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={17} color="#ffffff" />Buka Undangan</button>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        celebrant
        noPhotos={!child?.photo && !data.couple.bridePhoto}
        light="#ffffff"
        dark="#2d3a5a"
        demoWishes={WISHES}
        copy={{
          opening: {
            kicker: "Halo, teman-teman!",
            title: "Ayo Warnai Hari Bahagia",
            intro: `Dengan penuh sukacita, kami mengundang teman-teman dan keluarga untuk merayakan ${label.toLowerCase()} ${names}${age ? ` yang ke-${age}` : ""}. Bawa senyum paling cerah, kita melukis awan, bermain balon, dan tiup lilin bersama!`,
          },
          roles: ["Yang Berulang Tahun", "Bersama"],
          couple: ["Kenalan yuk", child ? "Si Kecil yang Berulang Tahun" : "Yang Merayakan"],
          count: ["Sebentar lagi", "Menuju Hari Pesta"],
          units: ["Hari", "Jam", "Menit", "Detik"],
          events: ["Catat tanggalnya", "Waktu & Tempat"],
          story: ["Warna demi warna", `Cerita ${nick}`],
          gallery: ["Album", "Foto Ceria"],
          wishes: ["Kirim doa terbaik", "Ucapan & Kehadiran"],
          gifts: ["Tanda sayang", "Kado & Amplop Digital"],
          closing: { thanks: "Terima Kasih!", text: `Kehadiran dan doa teman-teman membuat hari ${names} makin berwarna. Sampai jumpa di pesta pelangi!` },
          sent: "Yay! Ucapanmu sudah terkirim. Terima kasih!",
          attend: { maybe: "Mungkin" },
          wishPlaceholder: "Tulis ucapan dan doa untuk si kecil…",
          closedNote: "Terima kasih sudah ikut merayakan! Ucapan masih bisa dikirim lewat form ini.",
          giftIntro: "Kehadiran teman-teman sudah jadi hadiah paling indah. Bila ingin memberi tanda sayang, dapat melalui:",
          familyLabel: "Dengan sayang,",
        }}
        hero={(
          <header className={s.hero}>
            <p className={s.heroKicker}>Pesta {label}</p>
            <div className={s.heroArt}>
              <Art name="divider" />
              {age && <span className={s.heroAge} aria-hidden>{age}</span>}
            </div>
            <h1 className={s.heroNames}>{names}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <span className={s.divider} aria-hidden><Art name="divider" /></span>,
          node: <Art name="balloon" />,
          portrait: <Art name="balloon" className={s.portraitArt} />,
          countDecor: <span className={s.countClouds} aria-hidden><span><Art name="cloud" /></span><span><Art name="cloud" /></span></span>,
          closingEmblem: <Art name="rainbow" className={s.closingRainbow} />,
          sentArt: <Art name="balloon" />,
        }}
      />
    </ThemeShell>
  );
}
