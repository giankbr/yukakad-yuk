"use client";
// Theme "Ultah Koki" — pesta ulang tahun koki cilik di dapur ubin mint: rel gantungan sendok, kocokan, sarung tangan
// oven dan wajan, kartu resep bergaris dengan selotip, meja dapur dengan mangkuk adonan, rolling pin, karung tepung,
// telur, dan Kiki si cupcake bertopi koki (tokoh orisinal). Gouache buku cerita anak dengan garis tinta goyang.
import { Lucide, ThemeShell, formatDate, guestLabel, toDate, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Lilita One", "Baloo 2:wght@400;500;600;700;800", "Caveat Brush"];
// Painted by /tmp/pen/art/themes/ultah-koki.py (tools/art/themes in the repo).
const Art = makeArt("ultah-koki", { counter: [720, 265], rail: [720, 203], hat: [191, 158], cupcake: [160, 261], pin: [300, 52] } as const);

const WISHES = [
  { id: "w1", name: "Tante Rini & Om Bayu", attendance: "yes" as Attendance, message: "Selamat ulang tahun, Chef kecil! Semoga sehat selalu, makin pintar, dan masakannya makin enak." },
  { id: "w2", name: "Bilqis (teman TK)", attendance: "yes" as Attendance, message: "Aku mau bikin cupcake yang paling tinggi! Selamat ulang tahun ya!" },
  { id: "w3", name: "Eyang Putri", attendance: "maybe" as Attendance, message: "Doa Eyang selalu menyertai cucu tersayang. Panjang umur, sehat, dan jadi anak yang baik hati." },
];

function ageAt(birth?: string, at?: string) {
  const b = toDate(birth);
  const d = toDate(at);
  if (!b || !d) return undefined;
  let age = d.getFullYear() - b.getFullYear();
  if (d.getMonth() < b.getMonth() || (d.getMonth() === b.getMonth() && d.getDate() < b.getDate())) age -= 1;
  return age > 0 && age < 30 ? age : undefined;
}

export default function UltahKokiTheme(props: ThemeProps) {
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
      kicker: "Halo, Koki Kecil!",
      title: "Ayo Masak Bersama!",
      intro: `Celemek sudah disiapkan, oven sudah hangat. Dengan penuh sukacita kami mengundang teman-teman dan keluarga untuk merayakan ${label.toLowerCase()} ${names}${age ? ` yang ke-${age}` : ""}. Kehadiran dan doa kalian adalah bahan rahasia pesta ini!`,
    },
    roles: ["Koki yang Berulang Tahun", "Bersama"],
    couple: ["Kenalan dengan Koki", child ? "Koki Hari Ini" : "Yang Merayakan"],
    count: ["Oven Sudah Menyala", "Hitung Mundur Pesta"],
    units: ["Hari", "Jam", "Menit", "Detik"],
    events: ["Catat di Buku Resep", "Waktu & Tempat"],
    story: ["Resep Tumbuh Besar", `Cerita ${nick}`],
    gallery: ["Album", "Momen di Dapur"],
    wishes: ["Kirim Doa", "Ucapan & Kehadiran"],
    gifts: ["Tanda Sayang", "Kado & Amplop Digital"],
    closing: { thanks: "Terima Kasih!", text: `Sampai jumpa di dapur ceria! Kehadiran dan doa teman-teman adalah hadiah paling lezat untuk ${names}.` },
    sent: "Hore, ucapanmu sudah masuk oven! Terima kasih banyak.",
    attend: { maybe: "Mungkin" },
    familyLabel: "Salam hangat dari keluarga",
  };

  return (
    <ThemeShell
      fonts={FONTS}
      background="#bfe3d6"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Art name="rail" eager className={s.rail} />
          <div className={s.card}>
            <p className={s.kicker}>Resep Pesta {label}</p>
            <h1 className={s.coverName}>{names}</h1>
            {age && <p className={s.age}>ulang tahun ke <b>{age}</b></p>}
            <p className={s.coverDate}>{formatDate(data.date)}</p>
            <div className={s.guestWrap}>
              <div className={s.guest}>
                <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
                <strong>{guestLabel(data)}</strong>
                {table && <span className={s.table}>{table}</span>}
              </div>
              <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={18} color="#ffffff" />Buka Undangan</button>
            </div>
          </div>
          <Art name="counter" eager className={s.coverCounter} />
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
        dark="#2f3a5a"
        copy={copy}
        hero={(
          <header className={s.hero}>
            <span className={s.heroBand} aria-hidden />
            <div className={s.heroCard}>
              <Art name="hat" className={s.heroHat} />
              <p className={s.heroKicker}>Hore! {label}</p>
              <h1 className={s.heroName}>{names}{age ? ` ${age} Tahun` : ""}</h1>
              <p className={s.heroDate}>{formatDate(data.date)}</p>
              {note && <p className={s.heroNote}>{note}</p>}
            </div>
            <Art name="counter" className={s.heroCounter} />
          </header>
        )}
        slots={{
          divider: <Art name="pin" className={s.divider} />,
          node: <Art name="cupcake" />,
          portrait: <Art name="hat" />,
          closingDecor: <span className={s.closingCard} aria-hidden />,
          closingEmblem: <Art name="hat" className={s.closingHat} />,
          sentArt: <Art name="cupcake" />,
        }}
      />
    </ThemeShell>
  );
}
