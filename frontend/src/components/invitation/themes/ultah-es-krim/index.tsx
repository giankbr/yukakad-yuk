"use client";
// Theme "Ultah Es Krim" — pesta ulang tahun anak bertema es krim, gouache ceria: tenda bergaris merah muda,
// menara cone empat rasa dengan saus cokelat meleleh, meses, dan ceri yang bergoyang pelan, gerobak es krim
// berpayung belang, tetesan saus stroberi di tepi setiap bagian, dan hitung mundur berbentuk empat sendok es krim.
import { Lucide, ThemeShell, formatDate, guestLabel, toDate, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Chewy", "Baloo 2:wght@400;500;600;700;800"];
// Painted by /tmp/pen/art/themes/ultah-es-krim.py.
const Art = makeArt("ultah-es-krim", {
  tower: [230, 756], cart: [260, 323], cone: [70, 109], popsicle: [80, 187],
} as const);

const WISHES = [
  { id: "w1", name: "Rafi & Bunda", attendance: "yes" as const, message: "Selamat ulang tahun, Alea! Rafi mau es krim cokelat yang paling tinggi. Semoga sehat selalu dan makin pintar." },
  { id: "w2", name: "Keluarga Om Teguh", attendance: "yes" as const, message: "Selamat lima tahun, Alea sayang. Semoga hari-harimu selalu manis dan penuh tawa seperti sundae dengan ceri." },
  { id: "w3", name: "Tante Rini", attendance: "maybe" as const, message: "Tante usahakan datang ya, Sayang. Bukunya sudah dibungkus pita merah muda, peluk dari jauh!" },
];

function ageAt(birth?: string, at?: string) {
  const b = toDate(birth);
  const d = toDate(at);
  if (!b || !d) return undefined;
  let age = d.getFullYear() - b.getFullYear();
  if (d.getMonth() < b.getMonth() || (d.getMonth() === b.getMonth() && d.getDate() < b.getDate())) age -= 1;
  return age > 0 && age < 30 ? age : undefined;
}

export default function UltahEsKrimTheme(props: ThemeProps) {
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
      background="#fff7ee"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <span className={s.awning} aria-hidden />
          <Art name="tower" eager className={s.tower} />
          <div className={s.menu}>
            <p className={s.kicker}>Undangan {label}</p>
            <h1 className={s.coverNames}>{names}</h1>
            {age && <p className={s.age}><b>{age}</b>tahun yang manis</p>}
            <p className={s.coverDate}>{formatDate(data.date)}</p>
          </div>
          <Art name="cart" eager className={s.cart} />
          <div className={s.coverFoot}>
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
        light="#ffffff"
        dark="#5a2e1e"
        demoWishes={WISHES}
        copy={{
          opening: {
            kicker: "Halo, teman-teman!",
            title: "Ayo Pesta Es Krim!",
            intro: `Dengan penuh sukacita, kami mengundang teman-teman dan keluarga untuk merayakan ${label.toLowerCase()} ${names}${age ? ` yang ke-${age}` : ""}. Kita hias cone sendiri, tabur meses warna-warni, lalu tiup lilin bersama!`,
          },
          roles: ["Yang Berulang Tahun", "Bersama"],
          couple: ["Kenalan yuk", child ? "Si Manis yang Berulang Tahun" : "Yang Merayakan"],
          count: ["Sebentar lagi", "Menuju Hari Pesta"],
          units: ["Hari", "Jam", "Menit", "Detik"],
          events: ["Catat tanggalnya", "Waktu & Tempat"],
          story: ["Sendok demi sendok", `Cerita ${nick}`],
          gallery: ["Album", "Foto Ceria"],
          wishes: ["Kirim doa terbaik", "Ucapan & Kehadiran"],
          gifts: ["Tanda sayang", "Kado & Amplop Digital"],
          closing: { thanks: "Terima Kasih!", text: `Kehadiran dan doa teman-teman membuat hari ${names} jadi semanis es krim. Sampai jumpa di pesta!` },
          sent: "Yay! Ucapanmu sudah terkirim. Terima kasih!",
          attend: { maybe: "Mungkin" },
          wishPlaceholder: "Tulis ucapan dan doa untuk si kecil…",
          closedNote: "Terima kasih sudah ikut merayakan! Ucapan masih bisa dikirim lewat form ini.",
          giftIntro: "Kehadiran teman-teman sudah jadi hadiah paling manis. Bila ingin memberi tanda sayang, dapat melalui:",
          familyLabel: "Dengan sayang,",
        }}
        hero={(
          <header className={s.hero}>
            <div className={s.heroArt} aria-hidden>
              <Art name="cone" />
              <Art name="cart" />
              <Art name="popsicle" />
            </div>
            <p className={s.heroKicker}>Pesta {label}</p>
            <h1 className={s.heroNames}>{names}</h1>
            {age && <p className={s.heroAge}>yang ke-{age}</p>}
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="cone" className={s.divider} />,
          node: <Art name="cone" />,
          portrait: <Art name="popsicle" className={s.portraitArt} />,
          closingEmblem: <Art name="cart" className={s.closingEmblem} />,
          sentArt: <Art name="cone" />,
        }}
      />
    </ThemeShell>
  );
}
