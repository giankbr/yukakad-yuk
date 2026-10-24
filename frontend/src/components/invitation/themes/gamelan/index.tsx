"use client";
// Theme "Gamelan" — seperangkat gamelan perunggu di pendopo malam: gong ageng tergantung di gayor berukir merah-emas,
// bonang dan saron di atas rancakan, kendang berlapis kulit. Potret dan hitung mundur berbentuk gong dan pencon
// perunggu; riak bunyi gong menyebar perlahan dari pencu.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import type { Attendance } from "../kit";
import s from "./styles.module.css";

const FONTS = ["Gloock", "Alegreya:ital,wght@0,400;0,700;1,400", "Marcellus SC", "Amiri:wght@400"];
// Painted by /tmp/pen/art/themes/gamelan.py (pendopo.webp is the CSS backdrop).
const Art = makeArt("gamelan", { gong: [560, 652], bonang: [760, 218], saron: [620, 210], kendang: [360, 239], pencu: [130, 83], divider: [320, 24] } as const);

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    arabic: "بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ",
    kicker: "Assalamu'alaikum Warahmatullahi Wabarakatuh",
    title: "Gendhing Tresna",
    intro: "Dengan memohon rahmat dan ridha Allah Subhanahu wa Ta'ala, kami bermaksud menyelenggarakan pernikahan putra-putri kami. Merupakan kehormatan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
  },
  roles: ["Mempelai Putri", "Mempelai Putra"],
  couple: ["Kalih dados setunggal", "Kedua Mempelai"],
  count: ["Sebentar lagi gong ditabuh", "Menuju Hari Bahagia"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Titi wanci", "Waktu & Tempat"],
  story: ["Gendhing lelakon", "Perjalanan Kami"],
  gallery: ["Pigura", "Galeri Kenangan"],
  wishes: ["Donga pangestu", "Ucapan & Kehadiran"],
  gifts: ["Tanda asih", "Amplop Digital"],
  closing: {
    thanks: "Matur Sembah Nuwun",
    text: "Kehadiran dan doa restu Bapak/Ibu/Saudara/i adalah gendhing terindah yang mengiringi langkah pertama kami.",
    salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh",
  },
  sent: "Matur nuwun, doa dan ucapan Anda sudah kami terima.",
  wishPlaceholder: "Tuliskan doa restu untuk kedua mempelai…",
};

const WISHES = [
  { id: "w1", name: "Bu Sri Hastuti, Sanggar Ngesti Laras", attendance: "yes" as Attendance, message: "Barakallah, Sekar lan Damar. Mugi tansah rukun kados laras pelog lan slendro ingkang saged nyawiji. Kami siap menabuh untuk kalian." },
  { id: "w2", name: "Anggit Prasetyo", attendance: "yes" as Attendance, message: "Akhirnya pemain kendang kita punya pasangan tetap! Selamat ya, semoga sakinah mawaddah warahmah sampai kaken-kaken ninen-ninen." },
  { id: "w3", name: "Keluarga Pakde Harjono, Klaten", attendance: "maybe" as Attendance, message: "Insyaallah kami datang. Doa kami menyertai, semoga menjadi keluarga yang ayem, tentrem, dan penuh berkah." },
];

function Gong({ eager }: { eager?: boolean }) {
  return (
    <div className={s.gongWrap} aria-hidden>
      <div className={s.gongSwing}><Art name="gong" eager={eager} /></div>
      <span className={s.ripple} /><span className={s.ripple} /><span className={s.ripple} />
    </div>
  );
}

export default function GamelanTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const { bride, groom } = data.couple;
  const label = data.eventLabel?.trim() || "Pernikahan";
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const heroPic = data.gallery[0] ?? data.couple.bridePhoto ?? data.couple.groomPhoto;

  return (
    <ThemeShell
      fonts={FONTS}
      background="#1b110c"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <p className={s.kicker}>Pahargyan {label}</p>
          <Gong eager />
          <h1 className={s.coverNames}>{bride}<em>&amp;</em>{groom}</h1>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.guestWrap}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#24120a" />Buka Undangan</button>
          </div>
          <Art name="bonang" eager className={s.coverBonang} />
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        copy={COPY}
        demoWishes={WISHES}
        light="#efcd85"
        dark="#2b1a12"
        hero={(
          <header className={s.hero}>
            <div className={s.hangBar} aria-hidden />
            <div className={s.heroGong}>{heroPic ? <div className={s.heroPhoto}><Photo src={heroPic} alt="" /></div> : <div className={s.heroPhoto} />}</div>
            <p className={s.heroKicker}>{label}</p>
            <h1 className={s.heroNames}>{bride}<em>&amp;</em>{groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
            <Art name="saron" className={s.heroSaron} />
          </header>
        )}
        slots={{
          divider: <Art name="divider" className={s.divider} />,
          node: <Art name="pencu" />,
          amp: <Art name="pencu" />,
          countDecor: <Art name="bonang" className={s.countBonang} />,
          closingDecor: <div className={s.closingInstr} aria-hidden><Art name="kendang" /><Art name="saron" /></div>,
          closingEmblem: <Gong />,
          sentArt: <Art name="pencu" />,
        }}
      />
    </ThemeShell>
  );
}
