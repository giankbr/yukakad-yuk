"use client";
// Theme "Ultah Istana" — a kids' birthday in a storybook: an original pen-and-watercolour fairy-tale castle (crooked
// pastel towers with bent witch-hat roofs, heart window, round wooden door, climbing roses) whose pennants flutter, a
// flower-garden border, drifting clouds and butterflies; "Bab" chapter ribbons, scalloped page edges, tilted page cards.
import { Lucide, ThemeShell, formatDate, guestLabel, toDate, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Cherry Swash:wght@400;700", "Fredoka:wght@400;500;600"];
// Painted by /tmp/pen/art/themes/ultah-istana.py (tools/art/themes in the repo).
const Art = makeArt("ultah-istana", { castle: [560, 560], garden: [780, 168], pennant: [80, 45], cloud: [220, 99], butterfly: [80, 65], tiara: [160, 67], cake: [180, 179] } as const);

const WISHES = [
  { id: "w1", name: "Tante Mira & Kak Sasa", attendance: "yes" as Attendance, message: "Selamat ulang tahun, Putri Alya! Semoga makin pintar, sehat, dan selalu ceria seperti taman bunga." },
  { id: "w2", name: "Bu Guru Wulan", attendance: "yes" as Attendance, message: "Selamat ulang tahun, Alya sayang. Semoga makin rajin membaca dan suka berbagi dengan teman." },
  { id: "w3", name: "Keluarga Om Hendra", attendance: "maybe" as Attendance, message: "Maaf belum tentu bisa datang. Selamat ulang tahun ya, Alya, semoga semua mimpimu terwujud!" },
];

function ageAt(birth?: string, at?: string) {
  const b = toDate(birth);
  const d = toDate(at);
  if (!b || !d) return undefined;
  let age = d.getFullYear() - b.getFullYear();
  if (d.getMonth() < b.getMonth() || (d.getMonth() === b.getMonth() && d.getDate() < b.getDate())) age -= 1;
  return age > 0 && age < 30 ? age : undefined;
}

function Castle({ eager, className }: { eager?: boolean; className?: string }) {
  return (
    <div className={className ?? s.castleBox} aria-hidden>
      <Art name="castle" eager={eager} className={s.castle} />
      <Art name="pennant" eager={eager} className={`${s.pennant} ${s.p1}`} />
      <Art name="pennant" eager={eager} className={`${s.pennant} ${s.p2}`} />
      <Art name="pennant" eager={eager} className={`${s.pennant} ${s.p3}`} />
      <Art name="pennant" eager={eager} className={`${s.pennant} ${s.p4}`} />
    </div>
  );
}

export default function UltahIstanaTheme(props: ThemeProps) {
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
      kicker: "Bab Satu",
      title: "Pada Suatu Hari…",
      intro: `Di sebuah istana yang dikelilingi taman bunga, ${names} akan merayakan ${label.toLowerCase()}${age ? ` yang ke-${age}` : ""}. Gerbang istana dibuka untuk teman-teman dan keluarga tercinta. Datanglah, bawa senyum terbaikmu, dan jadilah bagian dari dongeng hari ini!`,
    },
    roles: ["Yang Berulang Tahun", "Bersama"],
    couple: ["Bab Dua", child ? "Sang Putri Istana" : "Yang Merayakan"],
    count: ["Bab Tiga", "Menuju Hari Pesta"],
    units: ["Hari", "Jam", "Menit", "Detik"],
    events: ["Bab Empat", "Waktu & Tempat"],
    story: ["Bab Lima", `Kisah ${nick}`],
    gallery: ["Album", "Momen Istana"],
    wishes: ["Surat untuk Sang Putri", "Ucapan & Kehadiran"],
    gifts: ["Tanda Sayang", "Kado & Amplop Digital"],
    closing: { thanks: "Terima Kasih!", text: `…dan pesta di istana pun berlangsung bahagia. Kehadiran dan doa teman-teman adalah hadiah terindah untuk ${names}.` },
    sent: "Hore, suratmu sudah sampai di istana! Terima kasih banyak.",
  };

  return (
    <ThemeShell
      fonts={FONTS}
      background="#f3e6f3"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Art name="cloud" eager className={`${s.cloud} ${s.cloudA}`} />
          <Art name="cloud" eager className={`${s.cloud} ${s.cloudB}`} />
          <Art name="butterfly" eager className={`${s.fly} ${s.flyA}`} />
          <Art name="butterfly" eager className={`${s.fly} ${s.flyB}`} />
          <p className={s.once}>Pada suatu hari, di sebuah istana…</p>
          <p className={s.kicker}>Undangan {label}</p>
          <h1 className={s.coverName}>{names}</h1>
          {age && <p className={s.age}>berulang tahun ke <b>{age}</b></p>}
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.guestWrap}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={17} color="#ffffff" />Buka Undangan</button>
          </div>
          <div className={s.stage} aria-hidden>
            <Castle eager />
            <Art name="garden" eager className={s.garden} />
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
        dark="#6a4f74"
        copy={copy}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            <Art name="butterfly" className={s.heroFly} />
            <Art name="cake" className={s.heroCake} />
            <p className={s.heroKicker}>Hore, {label.toLowerCase()}!</p>
            <h1 className={s.heroName}>{names}{age && <span className={s.heroAge}>{age} Tahun</span>}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            <Art name="tiara" className={s.divider} />
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="tiara" className={s.divider} />,
          node: <Art name="butterfly" />,
          portrait: <Art name="butterfly" className={s.portraitFly} />,
          countDecor: <><Art name="cloud" className={`${s.countCloud} ${s.countCloudA}`} /><Art name="cloud" className={`${s.countCloud} ${s.countCloudB}`} /></>,
          closingEmblem: (
            <>
              <p className={s.closingName}>{names}</p>
              <div className={s.closingStage} aria-hidden>
                <Art name="cloud" className={s.closingCloud} />
                <Castle className={s.closingCastle} />
                <Art name="garden" className={s.closingGarden} />
              </div>
            </>
          ),
          sentArt: <Art name="cake" />,
        }}
      />
    </ThemeShell>
  );
}
