"use client";
// Theme "Ultah Sepuh" — ulang tahun ke-60/70 yang anggun: gading & emas, pohon keluarga cat air yang cabangnya
// berujung pada potret berbingkai emas (foto dari galeri), peoni & krisan, angka usia bersinar emas, nada penuh syukur.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, toDate, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import type { Attendance } from "../kit";
import s from "./styles.module.css";

const FONTS = ["Gilda Display", "EB Garamond:ital,wght@0,400;0,500;0,600;1,400", "Italianno"];
// Painted by /tmp/pen/art/themes/ultah-sepuh.py (tools/art/themes in the repo).
const Art = makeArt("ultah-sepuh", {
  tree: [600, 647], frame: [240, 326], bouquet: [440, 303], mum: [160, 152], divider: [320, 26],
} as const);

const WISHES = [
  { id: "w1", name: "Keluarga Bapak Haryanto", attendance: "yes" as Attendance, message: "Selamat ulang tahun ke-70, Bu Sri. Semoga senantiasa sehat, panjang umur, dan selalu dikelilingi kasih anak, cucu, dan cicit." },
  { id: "w2", name: "Murid SDN Kemirirejo angkatan 1990", attendance: "yes" as Attendance, message: "Bu Guru Sri, terima kasih sudah sabar mengajari kami membaca. Sugeng ambal warsa, sehat dan bahagia selalu." },
  { id: "w3", name: "Tante Lies & Om Harto", attendance: "maybe" as Attendance, message: "Mohon maaf bila belum dapat hadir. Doa kami menyertai Mbakyu Sri, semoga diberi kesehatan dan sukacita setiap hari." },
];

function ageAt(birth?: string, at?: string) {
  const b = toDate(birth);
  const d = toDate(at);
  if (!b || !d) return undefined;
  let age = d.getFullYear() - b.getFullYear();
  if (d.getMonth() < b.getMonth() || (d.getMonth() === b.getMonth() && d.getDate() < b.getDate())) age -= 1;
  return age > 0 && age < 130 ? age : undefined;
}

export default function UltahSepuhTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Ulang Tahun";
  const child = data.extras?.child?.enabled !== false && data.extras?.child?.name?.trim() ? data.extras.child : undefined;
  const nick = child?.nickname?.trim() || child?.name.trim() || data.couple.bride;
  const full = child?.name.trim() || data.couple.brideFull || "";
  const names = child ? nick : [data.couple.bride, data.couple.groom?.trim()].filter(Boolean).join(" & ");
  const fromLabel = /ke-?\s*(\d{2,3})/i.exec(label)?.[1];
  const age = fromLabel ? Number(fromLabel) : ageAt(child?.birthDate, data.date);
  const note = data.couple.note?.trim();
  const table = tableLabel(data.guestTable);
  const family = data.gallery.slice(0, 5);
  const copy = {
    ...DEFAULT_COPY,
    opening: {
      kicker: "Dengan Penuh Syukur",
      title: age ? `${age} Tahun Penuh Kasih` : "Usia yang Diberkati",
      intro: `Puji syukur kepada Tuhan Yang Maha Esa atas usia${age ? ` ke-${age}` : ""} yang dianugerahkan kepada orang tua, eyang, dan buyut kami tercinta, ${names}. Dengan hormat kami mengundang Bapak/Ibu/Saudara/i untuk hadir merayakan dan mendoakan beliau bersama keluarga besar.`,
    },
    roles: ["Yang Berulang Tahun", "Bersama"] as [string, string],
    couple: ["Dengan Kasih", "Sosok Tercinta"] as [string, string],
    count: ["Menghitung Hari", "Menuju Hari Bahagia"] as [string, string],
    units: ["Hari", "Jam", "Menit", "Detik"] as [string, string, string, string],
    events: ["Waktu & Tempat", "Rangkaian Acara"] as [string, string],
    story: ["Lintasan Kenangan", `Perjalanan ${nick}`] as [string, string],
    gallery: ["Album Keluarga", "Kenangan Bersama"] as [string, string],
    wishes: ["Doa & Ucapan", `Untuk ${nick}`] as [string, string],
    gifts: ["Tanda Kasih", "Amplop Digital"] as [string, string],
    closing: { thanks: "Terima Kasih", text: `Kehadiran dan doa Bapak/Ibu/Saudara/i adalah hadiah terindah bagi ${names} dan seluruh keluarga besar.` },
    sent: "Terima kasih, doa dan ucapan Anda sudah kami terima dengan haru.",
    attend: { maybe: "Mungkin" },
    wishPlaceholder: `Tuliskan doa dan ucapan untuk ${names}…`,
    closedNote: "Terima kasih atas doa dan kasihnya. Ucapan untuk beliau masih dapat dikirim melalui form ini.",
  };

  return (
    <ThemeShell
      fonts={FONTS}
      background="#f8f2e4"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Art name="bouquet" eager className={s.bqTop} />
          <Art name="bouquet" eager className={s.bqBottom} />
          <p className={s.kicker}>Syukuran {label}</p>
          {age && <p className={s.age} aria-hidden>{age}</p>}
          <h1 className={s.coverName}>{names}</h1>
          {child && full !== nick && <p className={s.coverFull}>{full}</p>}
          <Art name="divider" eager className={s.coverRule} />
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.guestWrap}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#f3e2b5" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        celebrant
        light="#f3e2b5"
        dark="#3a2c20"
        copy={copy}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            <p className={s.heroKicker}>{label}</p>
            <h2 className={s.heroName}>{names}</h2>
            {note && <p className={s.heroNote}>{note}</p>}
            <div className={s.tree}>
              <Art name="tree" className={s.treeArt} />
              {[0, 1, 2, 3, 4].map(i => (
                <div key={i} className={`${s.leaf} ${s[`leaf${i}`]}`}>
                  <div className={s.ph}>
                    {family[i] ? <Photo src={family[i]} alt={`Potret keluarga ${i + 1}`} /> : <div aria-hidden />}
                  </div>
                  <Art name="frame" className={s.leafFrame} />
                </div>
              ))}
            </div>
            <p className={s.treeCaption}>Satu hati, empat generasi</p>
          </header>
        )}
        slots={{
          divider: <Art name="divider" className={s.divider} />,
          node: <Art name="mum" />,
          portrait: <Art name="frame" className={s.portraitArt} />,
          countDecor: <><Art name="mum" className={`${s.countMum} ${s.countMumL}`} /><Art name="mum" className={`${s.countMum} ${s.countMumR}`} /></>,
          closingDecor: <Art name="bouquet" className={s.closingBouquet} />,
          sentArt: <Art name="mum" />,
        }}
      />
    </ThemeShell>
  );
}
