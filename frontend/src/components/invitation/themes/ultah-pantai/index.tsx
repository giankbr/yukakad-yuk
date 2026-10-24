"use client";
// Theme "Ultah Pantai" — a kids' beach-party birthday in sunny gouache with a warm brown crayon contour (original
// designs): the cover is sky, sea and sand, with the child's name written in the sand, a sandcastle flying a pennant
// with the age, a striped umbrella, a bobbing beach ball, a bucket and spade and a crab scuttling along. Inside: towel
// cards, a life-ring portrait, beach-ball countdown, footprints for the story, wishes on the shallow water.
import { Lucide, ThemeShell, formatDate, guestLabel, toDate, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Lilita One", "Quicksand:wght@500;600;700"];
// Painted by /tmp/pen/art/themes/ultah-pantai.py (tools/art/themes in the repo).
const Art = makeArt("ultah-pantai", {
  castle: [440, 363], flag: [200, 109], umbrella: [300, 367], ball: [120, 121], crab: [180, 137], bucket: [220, 261], waves: [780, 300], shells: [280, 64],
} as const);

const WISHES = [
  { id: "w1", name: "Tante Sari & Om Bayu", attendance: "yes" as Attendance, message: "Selamat ulang tahun, Kayla sayang! Semoga makin ceria, sehat, dan istana pasirmu makin tinggi tahun ini." },
  { id: "w2", name: "Bu Guru Wulan (TK Pelangi)", attendance: "yes" as Attendance, message: "Selamat ulang tahun yang ke-5, Kayla. Tetap rajin, suka berbagi, dan jadi teman yang baik, ya." },
  { id: "w3", name: "Keluarga Om Hendra", attendance: "maybe" as Attendance, message: "Maaf kami belum tentu bisa datang. Selamat ulang tahun, semoga semua mimpimu terwujud!" },
];

function ageAt(birth?: string, at?: string) {
  const b = toDate(birth);
  const d = toDate(at);
  if (!b || !d) return undefined;
  let age = d.getFullYear() - b.getFullYear();
  if (d.getMonth() < b.getMonth() || (d.getMonth() === b.getMonth() && d.getDate() < b.getDate())) age -= 1;
  return age > 0 && age < 30 ? age : undefined;
}

export default function UltahPantaiTheme(props: ThemeProps) {
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
      kicker: "Halo, teman-teman!",
      title: "Ayo ke Pantai!",
      intro: `Matahari bersinar, ombak berkejaran, dan istana pasir menunggu dibangun! ${names} mau merayakan ${label.toLowerCase()}${age ? ` yang ke-${age}` : ""} di pantai. Bawa topi, senyum, dan semangat bermainmu, ya!`,
    },
    roles: ["Yang Berulang Tahun", "Bersama"],
    couple: ["Si Bintang Pantai", child ? `Kenalan dengan ${nick}` : "Yang Merayakan"],
    count: ["Sebentar lagi", "Hitung Mundur ke Pantai"],
    units: ["Hari", "Jam", "Menit", "Detik"],
    events: ["Catat, ya!", "Waktu & Tempat Pesta"],
    story: ["Jejak kaki kecil", `Cerita ${nick}`],
    gallery: ["Album", "Foto-Foto Ceria"],
    wishes: ["Kirim pesan", "Ucapan untuk " + nick],
    gifts: ["Ember hadiah", "Kado & Amplop Digital"],
    closing: { thanks: "Terima Kasih!", text: `Sampai jumpa di pantai! Kehadiran dan doa teman-teman adalah hadiah paling indah untuk ${names}.` },
    sent: "Hore, pesanmu sudah terbawa ombak sampai ke sini! Terima kasih.",
    wishPlaceholder: `Tulis ucapan & doa untuk ${nick}…`,
    giftIntro: "Kehadiran teman-teman sudah jadi hadiah terbesar. Jika ingin memberi tanda sayang, bisa melalui:",
    familyLabel: "Salam hangat dari keluarga",
  };

  return (
    <ThemeShell
      fonts={FONTS}
      background="#a9e2f2"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <span className={s.sun} aria-hidden />
          <p className={s.kicker}>Undangan {label}</p>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.coverSea} aria-hidden>
            <Art name="waves" eager className={s.waves} />
            <Art name="ball" eager className={s.seaBall} />
          </div>
          <div className={s.sandArea}>
            <h1 className={s.coverName}>{names}</h1>
            {age && <p className={s.ageRow}>ulang tahun ke <span className={s.age}>{age}</span></p>}
            <div className={s.towel}>
              <div className={s.guest}>
                <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
                <strong>{guestLabel(data)}</strong>
                {table && <span className={s.table}>{table}</span>}
              </div>
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={17} color="#ffffff" />Ayo ke Pantai!</button>
          </div>
          <div className={s.beach} aria-hidden>
            <Art name="umbrella" eager className={s.umbrella} />
            <Art name="castle" eager className={s.castle} />
            <span className={s.flag}><Art name="flag" eager />{age && <span>{age}</span>}</span>
            <Art name="bucket" eager className={s.bucket} />
            <Art name="crab" eager className={s.crab} />
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
        dark="#4a2c1c"
        copy={copy}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            <p className={s.heroKicker}>Hore, {label.toLowerCase()}!</p>
            <h1 className={s.heroName}>{names}{age && <span className={s.heroAge}>{age} Tahun</span>}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
            <div className={s.heroBeach} aria-hidden>
              <Art name="waves" className={s.waves} />
              <Art name="crab" className={s.heroCrab} />
            </div>
          </header>
        )}
        slots={{
          divider: <Art name="shells" className={s.divider} />,
          node: <Art name="ball" />,
          portrait: <Art name="crab" className={s.portraitCrab} />,
          countDecor: <Art name="ball" className={s.countBall} />,
          closingDecor: (
            <div className={s.closingBeach} aria-hidden>
              <Art name="waves" className={s.waves} />
              <Art name="umbrella" className={s.closingUmbrella} />
              <Art name="castle" className={s.closingCastle} />
            </div>
          ),
          sentArt: <Art name="crab" />,
        }}
      />
    </ThemeShell>
  );
}
