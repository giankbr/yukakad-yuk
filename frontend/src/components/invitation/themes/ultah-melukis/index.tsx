"use client";
// Theme "Ultah Melukis" — pesta ulang tahun melukis, gouache di kertas: kuda-kuda dengan kanvas yang "dilukisi" nama
// anak berwarna pelangi, palet penuh gumpalan cat, toples kuas, deret krayon, dan cipratan cat yang meletup masuk.
// Kartu-kartu berupa kanvas yang ditempel selotip; penghitung waktu berupa gumpalan cat.
import { Lucide, ThemeShell, formatDate, guestLabel, toDate, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Sniglet:wght@400;800", "Quicksand:wght@500;600;700", "Caveat Brush"];
// Painted by /tmp/pen/art/themes/ultah-melukis.py (tools/art/themes in the repo).
const Art = makeArt("ultah-melukis", {
  easel: [400, 500], palette: [360, 256], jar: [214, 412], crayons: [320, 20], squiggle: [300, 30],
  splatPink: [150, 160], splatBlue: [150, 137], splatYellow: [150, 143],
} as const);

const WISHES = [
  { id: "w1", name: "Tante Dewi & Om Arif", attendance: "yes" as Attendance, message: "Selamat ulang tahun, Kirana! Semoga makin pintar, sehat selalu, dan lukisannya makin warna-warni." },
  { id: "w2", name: "Raka (teman TK)", attendance: "yes" as Attendance, message: "Kirana, aku mau melukis kucing yang besar! Sampai ketemu di pestamu ya." },
  { id: "w3", name: "Keluarga Pak Hendra", attendance: "maybe" as Attendance, message: "Maaf kalau belum bisa datang. Selamat ulang tahun yang keenam, semoga jadi anak yang baik hati." },
];

function ageAt(birth?: string, at?: string) {
  const b = toDate(birth);
  const d = toDate(at);
  if (!b || !d) return undefined;
  let age = d.getFullYear() - b.getFullYear();
  if (d.getMonth() < b.getMonth() || (d.getMonth() === b.getMonth() && d.getDate() < b.getDate())) age -= 1;
  return age > 0 && age < 30 ? age : undefined;
}

export default function UltahMelukisTheme(props: ThemeProps) {
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
      kicker: "Halo, Teman-teman!",
      title: "Ayo Melukis Bersama!",
      intro: `Dengan penuh sukacita, kami mengundang teman-teman dan keluarga untuk merayakan ${label.toLowerCase()} ${names}${age ? ` yang ke-${age}` : ""}. Bawa senyum terbaikmu, kuas dan catnya sudah kami siapkan!`,
    },
    roles: ["Yang Berulang Tahun", "Bersama"] as [string, string],
    couple: ["Kenalan Dulu, Yuk", child ? "Si Pelukis Cilik" : "Yang Merayakan"] as [string, string],
    count: ["Siapkan Kuasmu", "Menuju Hari Pesta"] as [string, string],
    units: ["Hari", "Jam", "Menit", "Detik"] as [string, string, string, string],
    events: ["Catat Tanggalnya", "Waktu & Tempat"] as [string, string],
    story: ["Goresan Demi Goresan", `Cerita ${nick}`] as [string, string],
    gallery: ["Album", "Momen Seru"] as [string, string],
    wishes: ["Kirim Doa", "Ucapan & Kehadiran"] as [string, string],
    gifts: ["Tanda Sayang", "Kado & Amplop Digital"] as [string, string],
    closing: { thanks: "Terima Kasih!", text: `Sampai jumpa di pesta melukis! Kehadiran dan doa teman-teman adalah hadiah paling berwarna untuk ${names}.` },
    sent: "Hore, ucapanmu sudah terkirim! Terima kasih banyak.",
    attend: { maybe: "Mungkin" },
    wishPlaceholder: `Tulis ucapan dan doa untuk ${names}…`,
    closedNote: "Terima kasih! Konfirmasi sudah ditutup, tapi ucapan untuk si pelukis cilik masih bisa dikirim.",
    giftIntro: "Kehadiranmu sudah jadi hadiah terindah. Kalau ingin memberi tanda sayang, bisa melalui:",
    familyLabel: "Dengan sayang,",
  };

  return (
    <ThemeShell
      fonts={FONTS}
      background="#fdf6e9"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Art name="splatPink" eager className={`${s.coverSplat} ${s.coverSplatA}`} />
          <Art name="splatBlue" eager className={`${s.coverSplat} ${s.coverSplatB}`} />
          <Art name="splatYellow" eager className={`${s.coverSplat} ${s.coverSplatC}`} />
          <p className={s.coverPill}>Undangan {label}</p>
          <div className={s.easel}>
            <Art name="easel" eager />
            <div className={s.canvasText}>
              <small>Pesta melukis</small>
              <h1 className={s.coverName}>{names}</h1>
              {age && <span className={s.age} aria-label={`${age} tahun`}>{age}</span>}
              <p className={s.coverDate}>{formatDate(data.date)}</p>
            </div>
          </div>
          <Art name="palette" eager className={s.coverPalette} />
          <Art name="jar" eager className={s.coverJar} />
          <div className={s.guestCard}>
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
        demoWishes={WISHES}
        light="#ffffff"
        dark="#2b2d5c"
        copy={copy}
        hero={(
          <header className={s.hero}>
            <Art name="splatYellow" className={`${s.heroSplat} ${s.heroSplatA}`} />
            <Art name="splatPink" className={`${s.heroSplat} ${s.heroSplatB}`} />
            <Art name="palette" className={s.heroPalette} />
            <p className={s.heroKicker}>Hore! {label}</p>
            <h1 className={s.heroName}>{names}</h1>
            {age && <p className={s.heroAge}>{age} Tahun</p>}
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            <Art name="crayons" className={s.heroCrayons} />
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="squiggle" className={s.divider} />,
          node: <Art name="splatYellow" />,
          portrait: <Art name="splatBlue" className={s.peekSplat} />,
          countDecor: <><Art name="splatYellow" className={`${s.countSplat} ${s.countSplatA}`} /><Art name="splatPink" className={`${s.countSplat} ${s.countSplatB}`} /></>,
          closingEmblem: <div className={s.closingStage} aria-hidden><Art name="jar" /><Art name="palette" /></div>,
          sentArt: <Art name="palette" />,
        }}
      />
    </ThemeShell>
  );
}
