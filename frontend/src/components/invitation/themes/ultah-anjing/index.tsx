"use client";
// Theme "Ultah Anjing" — kids' birthday puppy party in gouache + crayon: a tricolour pup peeking out of a red-roofed
// doghouse, a corgi-like pup in a party hat hopping, a spotted pup with a red ball, bunting with paw prints, bones,
// balls and a bone-decorated cake on a sunny backyard. Name in a chunky cartoon outline, age on a swinging dog tag.
import { Lucide, ThemeShell, formatDate, guestLabel, toDate, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Lilita One", "Nunito:wght@400;600;700;800;900"];
// Painted by /tmp/pen/art/themes/ultah-anjing.py (tools/art/themes in the repo).
const Art = makeArt("ultah-anjing", {
  house: [400, 395], corgi: [210, 352], spotty: [240, 254], ball: [90, 90], bone: [120, 52], paw: [50, 49], bunting: [840, 82], cake: [240, 193],
} as const);

const TRAIL = [
  { bottom: "340px", left: "12%", rotate: "20deg" }, { bottom: "376px", left: "20%", rotate: "35deg" }, { bottom: "410px", left: "9%", rotate: "15deg" },
  { bottom: "350px", right: "10%", rotate: "-20deg" }, { bottom: "390px", right: "18%", rotate: "-30deg" },
];

const WISHES = [
  { id: "w1", name: "Naura & Mama", attendance: "yes" as const, message: "Selamat ulang tahun, Arka! Semoga sehat selalu, makin pintar, dan makin sayang sama Cokelat dan Belang." },
  { id: "w2", name: "Om Rizal", attendance: "yes" as const, message: "Happy birthday, jagoan! Om sudah siapkan bola baru, sampai ketemu di pesta anak anjing ya." },
  { id: "w3", name: "Keluarga Tante Sasa", attendance: "maybe" as const, message: "Selamat lima tahun, Arka! Semoga jadi anak yang saleh, berani, dan baik hati. Kami usahakan datang." },
];

function ageAt(birth?: string, at?: string) {
  const b = toDate(birth);
  const d = toDate(at);
  if (!b || !d) return undefined;
  let age = d.getFullYear() - b.getFullYear();
  if (d.getMonth() < b.getMonth() || (d.getMonth() === b.getMonth() && d.getDate() < b.getDate())) age -= 1;
  return age > 0 && age < 30 ? age : undefined;
}

export default function UltahAnjingTheme(props: ThemeProps) {
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
      kicker: "Halo, Teman-teman!",
      title: "Guk Guk, Ayo ke Pestaku!",
      intro: `Dengan penuh sukacita, kami mengundang teman-teman dan keluarga untuk merayakan ${label.toLowerCase()} ${names}${age ? ` yang ke-${age}` : ""}. Datang, ya! Kehadiran dan doa kalian akan membuat hari ini makin seru.`,
    },
    roles: ["Yang Berulang Tahun", "Bersama"],
    couple: ["Kenalan Dulu, Yuk", child ? "Si Anak Anjing Kecil" : "Yang Merayakan"],
    count: ["Hitung Mundur", "Menuju Hari Pesta"],
    units: ["Hari", "Jam", "Menit", "Detik"],
    events: ["Catat Tanggalnya", "Waktu & Tempat"],
    story: ["Jejak Kaki Kecil", `Cerita ${nick}`],
    gallery: ["Album", "Momen Seru"],
    wishes: ["Kirim Doa", "Ucapan & Kehadiran"],
    gifts: ["Tanda Sayang", "Kado & Amplop Digital"],
    closing: { thanks: "Terima Kasih!", text: `Sampai jumpa di pesta anak anjing! Kehadiran dan doa teman-teman adalah hadiah paling seru untuk ${names}.` },
    sent: "Hore, ucapanmu sudah terkirim! Terima kasih banyak.",
    wishPlaceholder: `Tuliskan doa dan ucapan untuk ${names}…`,
    closedNote: "Terima kasih atas doa dan perhatiannya. Ucapan untuk yang berulang tahun masih bisa dikirim lewat form ini.",
    giftIntro: "Kehadiran teman-teman sudah jadi hadiah terbaik. Jika ingin memberi tanda sayang, dapat melalui:",
  };

  return (
    <ThemeShell
      fonts={FONTS}
      background="#a9dcf6"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Art name="bunting" eager className={s.bunting} />
          <span className={`${s.cloud} ${s.cloudA}`} aria-hidden />
          <span className={`${s.cloud} ${s.cloudB}`} aria-hidden />
          {TRAIL.map((p, i) => (
            <span key={i} className={s.pawTrail} style={p} aria-hidden><Art name="paw" eager /></span>
          ))}
          <p className={s.pill}>Undangan {label}</p>
          <h1 className={s.coverName}>{names}</h1>
          {age && <p className={s.age}>ulang tahun ke <span className={s.tag}>{age}</span></p>}
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.guest}>
            <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
            <strong>{guestLabel(data)}</strong>
            {table && <span className={s.table}>{table}</span>}
          </div>
          <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={18} color="#ffffff" />Buka Undangan</button>
          <div className={s.yard} aria-hidden>
            <Art name="house" eager className={s.house} />
            <Art name="corgi" eager className={s.corgi} />
            <Art name="spotty" eager className={s.spotty} />
            <Art name="bone" eager className={s.bone} />
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
        light="#ffffff"
        dark="#263247"
        copy={copy}
        hero={(
          <header className={s.hero}>
            <Art name="bunting" className={s.heroBunting} />
            <p className={s.heroKicker}>Hore! {label}</p>
            <h1 className={s.heroName}>{names}{age ? ` ${age} Tahun` : ""}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            <div className={s.heroStage} aria-hidden>
              <Art name="ball" className={s.ballL} />
              <Art name="cake" className={s.cake} />
              <Art name="bone" className={s.boneR} />
            </div>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="bone" className={s.divider} />,
          node: <Art name="paw" />,
          portrait: <Art name="ball" className={s.portraitBall} />,
          closingEmblem: (
            <div className={s.closingYard} aria-hidden>
              <Art name="house" className={s.closingHouse} />
              <Art name="corgi" className={s.closingCorgi} />
            </div>
          ),
          sentArt: <Art name="corgi" />,
        }}
      />
    </ThemeShell>
  );
}
