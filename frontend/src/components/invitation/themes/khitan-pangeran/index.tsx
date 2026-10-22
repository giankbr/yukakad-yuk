"use client";
// Theme "Khitan Pangeran" — khitanan for a little prince, painted in gouache with gold foil: a domed palace on a royal-
// blue star-lattice night, a jewelled crown that bobs above the name, pennant bunting, a crescent moon and 8-point
// stars. Islamic: bismillah + salam, no figurative ornament (architecture, crown, stars only).
import { Lucide, ThemeShell, formatDate, guestLabel, toDate, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Lilita One", "Nunito:wght@500;600;700;800", "Cinzel Decorative:wght@700", "Amiri"];
// Painted by /tmp/pen/art/themes/khitan-pangeran.py (tools/art/themes in the repo).
const Art = makeArt("khitan-pangeran", { palace: [780, 545], crown: [300, 190], bunting: [780, 108], star: [72, 72], moon: [140, 153] } as const);

const WISHES = [
  { id: "w1", name: "Om Bayu & Tante Rani", attendance: "yes" as Attendance, message: "Barakallahu fiik, Pangeran Arkan! Semoga jadi anak saleh yang berani, pintar, dan sayang ayah bunda." },
  { id: "w2", name: "Ustazah Maryam", attendance: "yes" as Attendance, message: "Semoga Arkan makin rajin mengaji dan salat, menjadi penyejuk hati orang tua. Aamiin." },
  { id: "w3", name: "Keluarga Pak RT Hasan", attendance: "maybe" as Attendance, message: "Mohon maaf kalau belum bisa hadir. Selamat ya Arkan, cepat pulih dan tetap ceria!" },
];

function ageAt(birth?: string, at?: string) {
  const b = toDate(birth);
  const d = toDate(at);
  if (!b || !d) return undefined;
  let age = d.getFullYear() - b.getFullYear();
  if (d.getMonth() < b.getMonth() || (d.getMonth() === b.getMonth() && d.getDate() < b.getDate())) age -= 1;
  return age > 0 && age < 20 ? age : undefined;
}

export default function KhitanPangeranTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Khitanan";
  const child = data.extras?.child?.enabled !== false && data.extras?.child?.name?.trim() ? data.extras.child : undefined;
  const name = child ? (child.nickname?.trim() || child.name.trim()) : [data.couple.bride, data.couple.groom?.trim()].filter(Boolean).join(" & ");
  const age = ageAt(child?.birthDate, data.date);
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const star = <span className={s.divider} aria-hidden><Art name="star" /></span>;
  const copy: ThemeCopy = {
    ...DEFAULT_COPY,
    opening: {
      arabic: "بِسْمِ اللّٰهِ الرَّحْمٰنِ الرَّحِيْمِ",
      kicker: "Assalamu'alaikum Warahmatullahi Wabarakatuh",
      title: "Walimatul Khitan",
      intro: `Dengan memohon rahmat dan ridha Allah SWT, kami bermaksud menyelenggarakan tasyakuran ${label.toLowerCase()} putra kami, ${name}. Merupakan kehormatan bagi kami apabila Bapak/Ibu/Saudara/i dan teman-teman berkenan hadir dan mendoakan sang pangeran kecil.`,
    },
    roles: ["Sang Pangeran Kecil", "Bersama"],
    couple: ["Perkenalkan", child ? "Pangeran Kita" : "Yang Dikhitan"],
    count: ["Hitung Mundur", "Menuju Hari Istimewa"],
    units: ["Hari", "Jam", "Menit", "Detik"],
    events: ["Titah Undangan", "Waktu & Tempat"],
    story: ["Hikayat Kecil", `Perjalanan ${name}`],
    gallery: ["Album Istana", "Momen Bahagia"],
    wishes: ["Doa untuk Pangeran", "Ucapan & Kehadiran"],
    gifts: ["Tanda Kasih", "Amplop Digital"],
    closing: {
      thanks: "Jazakumullah Khairan",
      text: `Terima kasih atas doa dan kehadiran Bapak/Ibu/Saudara/i. Semoga ${name} tumbuh menjadi anak saleh yang membanggakan.`,
      salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh",
    },
    sent: "Jazakumullah khairan, doa Anda sudah sampai ke istana!",
    wishPlaceholder: `Tuliskan doa terbaik untuk ${name}…`,
  };

  return (
    <ThemeShell
      fonts={FONTS}
      background="#12245e"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Art name="bunting" eager className={s.bunting} />
          <Art name="moon" eager className={s.moon} />
          <Art name="star" eager className={`${s.twinkle} ${s.t1}`} />
          <Art name="star" eager className={`${s.twinkle} ${s.t2}`} />
          <Art name="star" eager className={`${s.twinkle} ${s.t3}`} />
          <p className={s.bismillah} lang="ar" dir="rtl">بِسْمِ اللّٰهِ الرَّحْمٰنِ الرَّحِيْمِ</p>
          <p className={s.kicker}>Undangan {label}</p>
          <Art name="crown" eager className={s.crown} />
          <h1 className={s.coverName}>{name}</h1>
          <p className={s.ribbon}>{age ? `Sang Pangeran Kecil · ${age} Tahun` : "Sang Pangeran Kecil"}</p>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.guestWrap}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={17} color="#12245e" />Buka Undangan</button>
          </div>
          <div className={s.stage} aria-hidden><Art name="palace" eager className={s.palace} /></div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        celebrant
        noPhotos={!child?.photo && !data.couple.bridePhoto}
        light="#fff6e2"
        dark="#1d3f97"
        copy={copy}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            <Art name="bunting" className={s.heroBunting} />
            <Art name="crown" className={s.heroCrown} />
            <p className={s.heroKicker}>{label}</p>
            <h1 className={s.heroName}>{name}</h1>
            {age && <p className={s.heroAge}>{age} tahun · putra yang gagah</p>}
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: star,
          node: <Art name="star" />,
          portrait: <Art name="crown" className={s.portraitCrown} />,
          countDecor: <Art name="moon" className={s.countMoon} />,
          closingEmblem: (
            <>
              <p className={s.closingName}>{name}</p>
              <div className={s.closingStage} aria-hidden>
                <Art name="moon" className={s.closingMoon} />
                <Art name="palace" className={s.closingPalace} />
              </div>
            </>
          ),
          sentArt: <Art name="crown" />,
        }}
      />
    </ThemeShell>
  );
}
