"use client";
// Theme "Ultah Robot" — ulang tahun anak bertema robot (karakter orisinal): Bip, robot toska-oranye yang melambai dengan
// layar dada yang menampilkan umur, drone kuning berbaling-baling, roda gigi yang berputar, lampu antena berkedip, dan
// kue kepala robot berlilin (gouache). Kertas cetak biru bergaris, panel bermur, layar LCD bergaya terminal.
import { Lucide, ThemeShell, formatDate, guestLabel, toDate, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Righteous", "Lexend:wght@400;500;600", "VT323"];
// Painted by /tmp/pen/art/themes/ultah-robot.py (tools/art/themes in the repo).
const Art = makeArt("ultah-robot", {
  robot: [440, 641], drone: [200, 178], gear: [160, 160], gear2: [120, 120], cake: [320, 299],
} as const);

const WISHES = [
  { id: "w1", name: "Nadia & Mama", attendance: "yes" as Attendance, message: "Selamat ulang tahun, Gibran! Semoga sehat selalu, makin pintar, dan nanti benar-benar bisa bikin robot penanam pohon." },
  { id: "w2", name: "Om Bayu", attendance: "yes" as Attendance, message: "Bip bup, selamat tujuh tahun jagoan! Om sudah siapkan kado, sampai ketemu di bengkel robot kardus ya." },
  { id: "w3", name: "Keluarga Tante Rina", attendance: "maybe" as Attendance, message: "Happy birthday, Gibran! Semoga jadi anak yang saleh, ceria, dan suka menolong. Kami usahakan datang." },
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
  return <span className={s.divider} aria-hidden><i /><Art name="gear2" /><i /></span>;
}

export default function UltahRobotTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel?.trim() || "Ulang Tahun";
  const child = data.extras?.child?.enabled !== false && data.extras?.child?.name?.trim() ? data.extras.child : undefined;
  const nick = child?.nickname?.trim() || child?.name.trim() || data.couple.bride;
  const names = child ? nick : [data.couple.bride, data.couple.groom?.trim()].filter(Boolean).join(" & ");
  const age = ageAt(child?.birthDate, data.date);
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const copy: ThemeCopy = {
    opening: {
      kicker: "halo_teman.exe",
      title: "Bip Bup! Ayo ke Pestaku!",
      intro: `Dengan penuh sukacita, kami mengundang teman-teman dan keluarga untuk merayakan ${label.toLowerCase()} ${names}${age ? ` yang ke-${age}` : ""}. Datang, ya! Kehadiran dan doa kalian akan membuat semua lampu pesta menyala terang.`,
    },
    roles: ["Yang Berulang Tahun", "Bersama"],
    couple: ["kenalan_dulu", child ? "Si Insinyur Cilik" : "Yang Merayakan"],
    count: ["hitung_mundur", "Menuju Hari Pesta"],
    units: ["Hari", "Jam", "Menit", "Detik"],
    events: ["catat_tanggal", "Waktu & Tempat"],
    story: ["log_perjalanan", `Cerita ${nick}`],
    gallery: ["album", "Momen Seru"],
    wishes: ["kirim_doa", "Ucapan & Kehadiran"],
    gifts: ["tanda_sayang", "Kado & Amplop Digital"],
    closing: { thanks: "Terima Kasih!", text: `Sampai jumpa di pesta robot! Kehadiran dan doa teman-teman adalah hadiah paling keren untuk ${names}.` },
    sent: "Hore, ucapanmu sudah terkirim! Terima kasih banyak.",
    wishPlaceholder: `Tuliskan doa dan ucapan untuk ${names}…`,
    closedNote: "Terima kasih atas doa dan perhatiannya. Ucapan untuk yang berulang tahun masih bisa dikirim lewat form ini.",
    giftIntro: "Kehadiran teman-teman sudah jadi hadiah terbaik. Jika ingin memberi tanda sayang, dapat melalui:",
  };

  return (
    <ThemeShell
      fonts={FONTS}
      background="#e8f5f6"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Art name="gear" eager className={s.gearA} />
          <Art name="gear2" eager className={s.gearB} />
          <Art name="drone" eager className={s.coverDrone} />
          <p className={s.pill}>Undangan {label}</p>
          <h1 className={s.coverName}>{names}</h1>
          {age && <p className={s.coverAge}>ulang tahun ke-{age}</p>}
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.bot} aria-hidden>
            <div className={s.botInner}>
              <Art name="robot" eager />
              <span className={s.screen}>{age ?? <small>HAI!</small>}</span>
              <span className={s.antenna} />
            </div>
          </div>
          <div className={s.coverPanel}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={17} color="#ffffff" />Buka Undangan</button>
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
        dark="#2c3a5e"
        copy={copy}
        hero={(
          <header className={s.hero}>
            <p className={s.heroKicker}>&gt; hore! {label.toLowerCase()}</p>
            <h1 className={s.heroName}>{names}{age ? ` ${age} Tahun` : ""}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            <div className={s.heroStage} aria-hidden>
              <Art name="gear" className={s.heroGearL} />
              <Art name="gear2" className={s.heroGearR} />
              <Art name="cake" className={s.heroCake} />
            </div>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Divider />,
          node: <Art name="gear2" />,
          portrait: <Art name="drone" className={s.pDrone} />,
          countDecor: <><Art name="gear" className={s.countGear} /><Art name="gear2" className={s.countGear} /></>,
          closingEmblem: (
            <div className={s.closingStage} aria-hidden>
              <Art name="robot" className={s.closingBot} />
              <Art name="cake" className={s.closingCake} />
            </div>
          ),
          sentArt: <Art name="cake" />,
        }}
      />
    </ThemeShell>
  );
}
