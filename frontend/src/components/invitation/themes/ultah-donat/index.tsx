"use client";
// Theme "Ultah Donat" — pesta ulang tahun anak bertema donat, gouache ceria dengan garis pensil warna. Sampulnya
// dinding donat berpasak di bawah kanopi garis pastel; usia si kecil duduk di lubang donat stroberi yang berputar
// pelan. Di dalam: kue menara lima donat berglasir dengan lilin belang, potret berbingkai donat, hitung mundur empat
// donat di pita cokelat, kartu krem dengan glasir menetes, dan taburan meses di latar mint.
// Dilukis oleh /tmp/pen/art/themes/ultah-donat.py.
import { Lucide, ThemeShell, formatDate, guestLabel, toDate, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Fredoka:wght@500;600;700", "Nunito:wght@600;700;800"];
const Art = makeArt("ultah-donat", {
  menara: [400, 670], dinding: [756, 466], donat: [180, 180], donat2: [180, 180], donat3: [180, 180], pita: [404, 96],
} as const);

const WISHES = [
  { id: "w1", name: "Kayla & Bunda", attendance: "yes" as Attendance, message: "Selamat ulang tahun, Danish! Kayla mau donat cokelat yang mesesnya paling banyak. Semoga sehat, pintar, dan makin sayang Kak Nara." },
  { id: "w2", name: "Keluarga Om Bima", attendance: "yes" as Attendance, message: "Selamat enam tahun, Danish sayang. Semoga hari-harimu selalu manis dan penuh tawa seperti donat yang baru digoreng." },
  { id: "w3", name: "Tante Wulan", attendance: "maybe" as Attendance, message: "Tante usahakan datang ya, Sayang. Kadonya sudah dibungkus kertas bergambar donat, peluk dari jauh!" },
];

function ageAt(birth?: string, at?: string) {
  const b = toDate(birth);
  const d = toDate(at);
  if (!b || !d) return undefined;
  let age = d.getFullYear() - b.getFullYear();
  if (d.getMonth() < b.getMonth() || (d.getMonth() === b.getMonth() && d.getDate() < b.getDate())) age -= 1;
  return age > 0 && age < 30 ? age : undefined;
}

export default function UltahDonatTheme(props: ThemeProps) {
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
      background="#c9efe0"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.wall} aria-hidden><Art name="dinding" eager /></div>
          <p className={s.kicker}>Undangan {label}</p>
          <div className={s.nameRow}>
            <h1 className={s.coverNames}>{names}</h1>
            {age && <span className={s.ageDonut} aria-label={`${age} tahun`}><Art name="donat" eager /><b>{age}</b></span>}
          </div>
          {age && <p className={s.ageText}>{age} tahun, semanis donat!</p>}
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.guest}>
            <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
            <strong>{guestLabel(data)}</strong>
            {table && <span className={s.table}>{table}</span>}
          </div>
          <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={18} color="#ffffff" />Buka Undangan</button>
          <Art name="donat2" eager className={`${s.peek} ${s.peekL}`} />
          <Art name="donat3" eager className={`${s.peek} ${s.peekR}`} />
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        celebrant
        noPhotos={!child?.photo && !data.couple.bridePhoto}
        light="#ffffff"
        dark="#5b2f22"
        demoWishes={WISHES}
        copy={{
          opening: {
            kicker: "Halo, teman-teman!",
            title: "Ayo Pesta Donat!",
            intro: `Dengan penuh sukacita, kami mengundang teman-teman dan keluarga untuk merayakan ${label.toLowerCase()} ${names}${age ? ` yang ke-${age}` : ""}. Kita hias donat sendiri, tabur meses warna-warni, lalu tiup lilin di kue menara donat bersama!`,
          },
          roles: ["Yang Berulang Tahun", "Bersama"],
          couple: ["Kenalan yuk", child ? "Si Manis yang Berulang Tahun" : "Yang Merayakan"],
          count: ["Sebentar lagi", "Menuju Hari Pesta"],
          units: ["Hari", "Jam", "Menit", "Detik"],
          events: ["Catat tanggalnya", "Waktu & Tempat"],
          story: ["Gigitan demi gigitan", `Cerita ${nick}`],
          gallery: ["Album", "Foto Ceria"],
          wishes: ["Kirim doa terbaik", "Ucapan & Kehadiran"],
          gifts: ["Tanda sayang", "Kado & Amplop Digital"],
          closing: { thanks: "Terima Kasih!", text: `Kehadiran dan doa teman-teman membuat hari ${names} semanis donat bertabur meses. Sampai jumpa di pesta!` },
          sent: "Hore! Ucapanmu sudah terkirim. Terima kasih!",
          attend: { maybe: "Mungkin" },
          wishPlaceholder: "Tulis ucapan dan doa untuk si kecil…",
          closedNote: "Terima kasih sudah ikut merayakan! Ucapan masih bisa dikirim lewat form ini.",
          giftIntro: "Kehadiran teman-teman sudah jadi hadiah paling manis. Bila ingin memberi tanda sayang, dapat melalui:",
          familyLabel: "Dengan sayang,",
        }}
        hero={(
          <header className={s.hero}>
            <p className={s.heroKicker}>Pesta {label}</p>
            <h1 className={s.heroNames}>{names}</h1>
            {age && <p className={s.heroAge}>yang ke-{age}</p>}
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            <div className={s.heroCake} aria-hidden><Art name="menara" /></div>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="pita" className={s.divider} />,
          node: <Art name="donat3" />,
          amp: <Art name="donat" />,
          portrait: <Art name="donat2" className={s.portraitArt} />,
          closingDecor: <Art name="dinding" className={s.closingScene} />,
          closingEmblem: <Art name="donat" className={s.closingEmblem} />,
          sentArt: <Art name="donat" />,
        }}
      />
    </ThemeShell>
  );
}
