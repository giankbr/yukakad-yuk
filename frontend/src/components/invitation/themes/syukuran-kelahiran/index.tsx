"use client";
// Theme "Syukuran Kelahiran" — menyambut bayi mungil: mainan gantung ring kayu dengan bulan, bintang & awan flanel
// berjahit yang berayun pelan, jejak kaki kecil, selimut rajut, ranting baby's breath; sage, krem, kuning mentega.
import { Lucide, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import type { Attendance } from "../kit";
import s from "./styles.module.css";

const FONTS = ["Comfortaa:wght@500;600;700", "Mulish:wght@400;600;700;800", "Sacramento"];
// Painted by /tmp/pen/art/themes/syukuran-kelahiran.py (tools/art/themes in the repo).
const Art = makeArt("syukuran-kelahiran", {
  hoop: [460, 217], moon: [170, 245], star: [110, 136], star2: [92, 161], cloud: [160, 202], feet: [160, 154], sprig: [220, 260], divider: [300, 40],
} as const);

const WISHES = [
  { id: "w1", name: "Eyang Putri Wicaksono", attendance: "yes" as Attendance, message: "Sugeng rawuh, Lintang cucu Eyang. Semoga sehat, tumbuh cerdas, dan menjadi anak yang berbakti serta membawa terang bagi keluarga." },
  { id: "w2", name: "Wulan & Arif", attendance: "yes" as Attendance, message: "Selamat atas kelahiran putri pertamanya! Semoga Ibu cepat pulih dan Lintang selalu sehat, tidurnya nyenyak, tangisnya merdu." },
  { id: "w3", name: "Rekan Kantor Dimas", attendance: "maybe" as Attendance, message: "Selamat menjadi Ayah, Mas Dimas! Doa terbaik untuk Lintang dan keluarga kecil yang baru." },
];

function Mobile() {
  return (
    <div className={s.mobile} aria-hidden>
      <Art name="moon" eager className={`${s.hang} ${s.hangMoon}`} />
      <Art name="star" eager className={`${s.hang} ${s.hangStar}`} />
      <Art name="star2" eager className={`${s.hang} ${s.hangStar2}`} />
      <Art name="cloud" eager className={`${s.hang} ${s.hangCloud}`} />
      <Art name="hoop" eager className={s.hoop} />
    </div>
  );
}

export default function SyukuranKelahiranTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Syukuran Kelahiran";
  const child = data.extras?.child?.enabled !== false && data.extras?.child?.name?.trim() ? data.extras.child : undefined;
  const nick = child?.nickname?.trim() || child?.name.trim() || data.couple.bride;
  const full = child?.name.trim() || data.couple.brideFull || "";
  const names = child ? nick : [data.couple.bride, data.couple.groom?.trim()].filter(Boolean).join(" & ");
  const born = child?.birthDate ? formatDate(child.birthDate) : undefined;
  const meaning = child?.meaning?.trim();
  const note = data.couple.note?.trim();
  const table = tableLabel(data.guestTable);
  const copy = {
    ...DEFAULT_COPY,
    opening: {
      kicker: "Dengan Penuh Syukur",
      title: "Selamat Datang, Sayang",
      intro: `Puji syukur kepada Tuhan Yang Maha Esa atas kelahiran buah hati kami, ${names}. Dengan sukacita kami mengundang Bapak/Ibu/Saudara/i untuk hadir dalam ${label.toLowerCase()} dan memberikan doa terbaik bagi si kecil.`,
    },
    roles: ["Buah Hati Kami", "Bersama"] as [string, string],
    couple: ["Perkenalkan", child ? "Si Kecil yang Dinanti" : "Yang Kami Syukuri"] as [string, string],
    count: ["Hitung Mundur", "Menuju Hari Syukuran"] as [string, string],
    units: ["Hari", "Jam", "Menit", "Detik"] as [string, string, string, string],
    events: ["Waktu & Tempat", "Acara Syukuran"] as [string, string],
    story: ["Perjalanan Kecil", `Menanti ${nick}`] as [string, string],
    gallery: ["Galeri", "Hari-Hari Pertama"] as [string, string],
    wishes: ["Doa untuk Si Kecil", "Ucapan & Kehadiran"] as [string, string],
    gifts: ["Tanda Kasih", "Kado & Amplop Digital"] as [string, string],
    closing: { thanks: "Terima Kasih", text: `Doa dan kehadiran Bapak/Ibu/Saudara/i adalah hadiah pertama yang paling berharga bagi ${names}.` },
    sent: "Terima kasih, doa untuk si kecil sudah terkirim.",
    attend: { maybe: "Mungkin" },
    wishPlaceholder: `Tuliskan doa terbaik untuk ${names}…`,
    closedNote: "Terima kasih atas doa dan perhatiannya. Ucapan untuk si kecil masih bisa dikirim lewat form ini.",
  };

  return (
    <ThemeShell
      fonts={FONTS}
      background="#f7f1e1"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Mobile />
          <p className={s.kicker}>{label}</p>
          <p className={s.welcome}>Selamat datang,</p>
          <h1 className={s.coverName}>{names}</h1>
          {child && full !== nick && <p className={s.coverFull}>{full}</p>}
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.guestWrap}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={17} color="#fffcf3" />Buka Undangan</button>
          </div>
          <div className={s.blanket} aria-hidden />
          <Art name="feet" eager className={s.coverFeet} />
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        celebrant
        noPhotos={!child?.photo && !data.couple.bridePhoto}
        light="#fffcf3"
        dark="#3f4a3a"
        copy={copy}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            <Art name="sprig" className={`${s.heroSprig} ${s.heroSprigL}`} />
            <Art name="sprig" className={`${s.heroSprig} ${s.heroSprigR}`} />
            <Mobile />
            <p className={s.heroKicker}>Halo, dunia!</p>
            <h1 className={s.heroName}>{names}</h1>
            {child && full !== nick && <p className={s.heroFull}>{full}</p>}
            {(born || note) && (
              <div className={s.birth}>
                <Art name="feet" />
                <p>{born && <b>Lahir {born}</b>}{note}</p>
              </div>
            )}
            {meaning && (
              <div className={s.meaning}>
                <small>Arti Nama</small>
                <p>{meaning}</p>
              </div>
            )}
          </header>
        )}
        slots={{
          divider: <Art name="divider" className={s.divider} />,
          node: <Art name="feet" />,
          portrait: <Art name="star" className={s.peekStar} />,
          countDecor: <><Art name="sprig" className={`${s.countSprig} ${s.countSprigL}`} /><Art name="sprig" className={`${s.countSprig} ${s.countSprigR}`} /></>,
          closingEmblem: <Art name="moon" className={s.closingEmblemArt} />,
          sentArt: <Art name="cloud" />,
        }}
      />
    </ThemeShell>
  );
}
