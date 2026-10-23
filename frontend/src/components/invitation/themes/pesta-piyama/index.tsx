"use client";
// Theme "Pesta Piyama" — pesta menginap anak: tenda selimut tambal-sulam di atas dua kursi dengan lampu peri yang berkelip,
// pintu tenda yang hangat berisi bantal, Momo si beruang bertopi tidur (tokoh orisinal), ember popcorn, bulan sabit yang
// mengantuk, kain piyama bergaris dan bantal berjahit. Gouache buku cerita dengan garis pensil ungu tua.
import { Lucide, ThemeShell, formatDate, guestLabel, toDate, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Fredoka:wght@400;500;600;700", "Nunito:wght@400;600;700;800", "Patrick Hand"];
// Painted by /tmp/pen/art/themes/pesta-piyama.py (tools/art/themes in the repo).
const Art = makeArt("pesta-piyama", { fort: [600, 471], fortglow: [600, 471], bear: [220, 298], popcorn: [170, 213], moon: [220, 207], bulbs: [400, 50] } as const);

const WISHES = [
  { id: "w1", name: "Naira (teman sekelas)", attendance: "yes" as Attendance, message: "Selamat ulang tahun, Aluna! Aku bawa piyama kelinci dan senter. Nanti kita dongeng hantu yang lucu ya!" },
  { id: "w2", name: "Tante Laras & Om Bima", attendance: "yes" as Attendance, message: "Selamat ulang tahun ke-8, sayang. Semoga makin pintar, sehat selalu, dan tidurnya selalu nyenyak penuh mimpi indah." },
  { id: "w3", name: "Eyang Putri", attendance: "maybe" as Attendance, message: "Doa Eyang selalu untuk cucu tersayang. Panjang umur, jadi anak yang baik hati dan berani." },
];

function ageAt(birth?: string, at?: string) {
  const b = toDate(birth);
  const d = toDate(at);
  if (!b || !d) return undefined;
  let age = d.getFullYear() - b.getFullYear();
  if (d.getMonth() < b.getMonth() || (d.getMonth() === b.getMonth() && d.getDate() < b.getDate())) age -= 1;
  return age > 0 && age < 30 ? age : undefined;
}

export default function PestaPiyamaTheme(props: ThemeProps) {
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
      kicker: "Psst, ada undangan!",
      title: "Ayo Pesta Piyama!",
      intro: `Siapkan piyama, bantal, dan boneka kesayanganmu. Dengan gembira kami mengundang teman-teman dan keluarga untuk merayakan ${label.toLowerCase()} ${names}${age ? ` yang ke-${age}` : ""} di dalam tenda selimut. Kehadiran dan doa kalian membuat malam ini makin hangat!`,
    },
    roles: ["Yang Berulang Tahun", "Bersama"],
    couple: ["Kenalan dulu, yuk", child ? "Si Empunya Pesta" : "Yang Merayakan"],
    count: ["Sebentar lagi gelap", "Hitung Mundur Pesta"],
    units: ["Hari", "Jam", "Menit", "Detik"],
    events: ["Catat jadwalnya", "Waktu & Tempat"],
    story: ["Dongeng sebelum tidur", `Cerita ${nick}`],
    gallery: ["Album", "Momen Lucu"],
    wishes: ["Kirim doa", "Ucapan & Kehadiran"],
    gifts: ["Tanda sayang", "Kado & Amplop Digital"],
    closing: { thanks: "Terima Kasih!", text: `Sampai jumpa di dalam tenda selimut! Kehadiran dan doa teman-teman adalah hadiah paling hangat untuk ${names}.` },
    sent: "Hore, ucapanmu sudah sampai di tenda! Terima kasih banyak.",
    attend: { maybe: "Mungkin" },
    wishPlaceholder: "Tuliskan ucapan dan doa untuk yang berulang tahun…",
    closedNote: "Pestanya sudah selesai. Terima kasih sudah ikut bergembira! Ucapan masih bisa dikirim lewat form ini.",
    giftIntro: "Kehadiranmu sudah jadi hadiah terbaik. Bila ingin memberi tanda sayang, bisa melalui:",
    familyLabel: "Salam hangat dari keluarga",
  };

  return (
    <ThemeShell
      fonts={FONTS}
      background="#172741"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Art name="bulbs" eager className={s.cBulbs} />
          <Art name="moon" eager className={s.cMoon} />
          <p className={s.kicker}>Undangan Pesta Piyama</p>
          <h1 className={s.coverName}>{names}</h1>
          {age && <p className={s.age}>{label.toLowerCase()} ke <b>{age}</b></p>}
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.scene}>
            <Art name="fort" eager />
            <Art name="fortglow" eager className={s.glowLayer} />
            <Art name="bear" eager className={s.cBear} />
            <Art name="popcorn" eager className={s.cPop} />
          </div>
          <div className={s.guestPillow}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={18} color="currentColor" />Buka Undangan</button>
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
        light="#ffd36e"
        dark="#22385a"
        copy={copy}
        hero={(
          <header className={s.hero}>
            <Art name="bulbs" className={s.heroBulbs} />
            <div className={s.heroCard}>
              <Art name="bear" className={s.heroBear} />
              <p className={s.heroKicker}>Pesta Piyama {label}</p>
              <h1 className={s.heroName}>{names}{age ? ` ${age} Tahun` : ""}</h1>
              <p className={s.heroDate}>{formatDate(data.date)}</p>
              {note && <p className={s.heroNote}>{note}</p>}
            </div>
          </header>
        )}
        slots={{
          divider: <Art name="bulbs" className={s.divider} />,
          node: <Art name="moon" />,
          portrait: <Art name="popcorn" />,
          countDecor: <Art name="moon" className={s.countMoon} />,
          closingDecor: <Art name="moon" className={s.closingMoon} />,
          closingEmblem: <div className={s.closingFort} aria-hidden><Art name="fort" /><Art name="fortglow" /></div>,
          sentArt: <Art name="bear" />,
        }}
      />
    </ThemeShell>
  );
}
