"use client";
// Theme "Ultah Kucing" — ulang tahun anak bertema kucing: Oyen si kucing oranye di dalam kardus, Mochi si abu-abu
// memeluk bola benang, Kiko si hitam mengintip, kue berbentuk ikan, bola benang, dan jejak kaki (gouache + krayon).
import { Lucide, ThemeShell, formatDate, guestLabel, toDate, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Chewy", "Baloo 2:wght@400;500;600;700;800"];
// Painted by /tmp/pen/art/themes/ultah-kucing.py (tools/art/themes in the repo).
const Art = makeArt("ultah-kucing", {
  boxcat: [440, 479], yarncat: [460, 192], peek: [161, 149], cake: [360, 228], yarn: [140, 120], yarn2: [140, 118], paw: [60, 54],
} as const);

const TRAIL = [
  { top: "9%", left: "8%", rotate: "-20deg" }, { top: "14%", left: "15%", rotate: "-10deg" }, { top: "20%", left: "9%", rotate: "-25deg" },
  { top: "42%", left: "86%", rotate: "20deg" }, { top: "48%", left: "80%", rotate: "10deg" }, { top: "54%", left: "87%", rotate: "25deg" },
];

const WISHES = [
  { id: "w1", name: "Raka & Bunda", attendance: "yes" as const, message: "Selamat ulang tahun, Kirana! Semoga sehat selalu, makin pintar, dan makin sayang sama semua kucing." },
  { id: "w2", name: "Tante Wulan", attendance: "yes" as const, message: "Happy birthday, sayang! Tante sudah siapkan kado, sampai ketemu di pesta kucing ya." },
  { id: "w3", name: "Keluarga Om Bayu", attendance: "maybe" as const, message: "Selamat enam tahun, Kirana! Semoga jadi anak yang salehah dan ceria. Kami usahakan datang." },
];

function ageAt(birth?: string, at?: string) {
  const b = toDate(birth);
  const d = toDate(at);
  if (!b || !d) return undefined;
  let age = d.getFullYear() - b.getFullYear();
  if (d.getMonth() < b.getMonth() || (d.getMonth() === b.getMonth() && d.getDate() < b.getDate())) age -= 1;
  return age > 0 && age < 30 ? age : undefined;
}

function Yarn() {
  return <span className={s.divider} aria-hidden><Art name="yarn" /></span>;
}

export default function UltahKucingTheme(props: ThemeProps) {
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
      title: "Meong, Ayo ke Pestaku!",
      intro: `Dengan penuh sukacita, kami mengundang teman-teman dan keluarga untuk merayakan ${label.toLowerCase()} ${names}${age ? ` yang ke-${age}` : ""}. Datang, ya! Kehadiran dan doa kalian akan membuat hari ini makin seru.`,
    },
    roles: ["Yang Berulang Tahun", "Bersama"],
    couple: ["Kenalan Dulu, Yuk", child ? "Si Kucing Kecil" : "Yang Merayakan"],
    count: ["Hitung Mundur", "Menuju Hari Pesta"],
    units: ["Hari", "Jam", "Menit", "Detik"],
    events: ["Catat Tanggalnya", "Waktu & Tempat"],
    story: ["Jejak Kaki Kecil", `Cerita ${nick}`],
    gallery: ["Album", "Momen Lucu"],
    wishes: ["Kirim Doa", "Ucapan & Kehadiran"],
    gifts: ["Tanda Sayang", "Kado & Amplop Digital"],
    closing: { thanks: "Terima Kasih!", text: `Sampai jumpa di pesta kucing! Kehadiran dan doa teman-teman adalah hadiah paling manis untuk ${names}.` },
    sent: "Hore, ucapanmu sudah terkirim! Terima kasih banyak.",
    wishPlaceholder: `Tuliskan doa dan ucapan untuk ${names}…`,
    closedNote: "Terima kasih atas doa dan perhatiannya. Ucapan untuk yang berulang tahun masih bisa dikirim lewat form ini.",
    giftIntro: "Kehadiran teman-teman sudah jadi hadiah terbaik. Jika ingin memberi tanda sayang, dapat melalui:",
  };

  return (
    <ThemeShell
      fonts={FONTS}
      background="#ffe9d4"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          {TRAIL.map((p, i) => (
            <span key={i} className={s.pawTrail} style={{ top: p.top, left: p.left, rotate: p.rotate }} aria-hidden><Art name="paw" eager /></span>
          ))}
          <p className={s.pill}>Undangan {label}</p>
          <h1 className={s.coverName}>{names}</h1>
          {age && <p className={s.age}>ulang tahun ke <span className={s.ageBall}><Art name="yarn2" eager /><b>{age}</b></span></p>}
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
            <Art name="yarn" eager className={s.yarn} />
            <Art name="peek" eager className={s.peekC} />
            <span className={s.stageBox} />
            <Art name="boxcat" eager className={s.boxcat} />
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
        light="#fffaf2"
        dark="#3a2a24"
        copy={copy}
        hero={(
          <header className={s.hero}>
            <p className={s.heroKicker}>Hore! {label}</p>
            <h1 className={s.heroName}>{names}{age ? ` ${age} Tahun` : ""}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            <div className={s.heroStage} aria-hidden>
              <Art name="yarn" className={s.yarnL} />
              <Art name="cake" className={s.cake} />
              <Art name="yarn2" className={s.yarnR} />
            </div>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Yarn />,
          node: <Art name="paw" />,
          portrait: <Art name="peek" className={s.peek} />,
          countDecor: <><Art name="yarn2" className={s.countYarnL} /><Art name="yarn" className={s.countYarnR} /></>,
          closingEmblem: (
            <>
              <p className={s.closingName}>{names}</p>
              <div className={s.closingStage} aria-hidden>
                <Art name="yarncat" className={s.yarncat} />
                <Art name="boxcat" className={s.boxcat} />
              </div>
            </>
          ),
          sentArt: <Art name="cake" />,
        }}
      />
    </ThemeShell>
  );
}
