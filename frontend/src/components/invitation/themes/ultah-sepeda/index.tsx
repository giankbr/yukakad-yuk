"use client";
// Theme "Ultah Sepeda" — ulang tahun anak bertema gowes bareng di taman lalu lintas, cat poster gouache bergaris pensil.
// Sampul: untaian bendera segitiga, nama besar bergaya stiker, seikat balon terikat di setang sepeda kecil (usia di
// balon kuning) dengan helm tergantung dan pita di pegangan, lalu lintasan taman dengan cone, bendera, dan teman-teman
// bersepeda. Hitung mundur di dalam empat roda yang melaju di lintasan, linimasa berupa jalan kecil, kartu stiker.
import { Lucide, ThemeShell, formatDate, guestLabel, toDate, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Lilita One", "Baloo 2:wght@400;600;700;800"];
// Painted by /tmp/pen/art/themes/ultah-sepeda.py (balloons are separate so they can bob).
const Art = makeArt("ultah-sepeda", { sepeda: [506, 318], balon: [270, 390], taman: [780, 523], bendera: [800, 130], panji: [320, 43], helm: [120, 58] } as const);

function ageAt(birth?: string, at?: string) {
  const b = toDate(birth);
  const d = toDate(at);
  if (!b || !d) return undefined;
  let age = d.getFullYear() - b.getFullYear();
  if (d.getMonth() < b.getMonth() || (d.getMonth() === b.getMonth() && d.getDate() < b.getDate())) age -= 1;
  return age > 0 && age < 30 ? age : undefined;
}

const WISHES = [
  { id: "w1", name: "Adik Naufal & Keluarga", attendance: "yes" as Attendance, message: "Selamat ulang tahun, Arka! Semoga makin sehat, makin berani, dan gowesnya makin jauh. Sampai ketemu di lintasan!" },
  { id: "w2", name: "Bu Guru Sinta, TK Pelangi", attendance: "yes" as Attendance, message: "Selamat ulang tahun ke-6, Arka sayang. Tetap rajin pakai helm dan selalu menolong teman ya." },
  { id: "w3", name: "Om Reza & Tante Mira", attendance: "maybe" as Attendance, message: "Happy birthday, jagoan! Kalau sempat kami mampir bawa bel sepeda baru. Doa terbaik untukmu." },
];

export default function UltahSepedaTheme(props: ThemeProps) {
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
      kicker: "Halo, Teman Gowes!",
      title: "Ayo Gowes Bareng di Pestaku!",
      intro: `Dengan penuh sukacita, kami mengundang teman-teman dan keluarga untuk merayakan ${label.toLowerCase()} ${names}${age ? ` yang ke-${age}` : ""}. Kita akan bersepeda keliling taman, main zig-zag cone, lalu tiup lilin bersama!`,
    },
    roles: ["Si Jagoan Gowes", "Bersama"],
    couple: ["Kenalan Yuk", child ? "Yang Berulang Tahun" : "Yang Merayakan"],
    count: ["Siap-siap gowes", "Hitung Mundur Pesta"],
    units: ["Hari", "Jam", "Menit", "Detik"],
    events: ["Titik Kumpul", "Waktu & Tempat"],
    story: ["Jalan Cerita", `Perjalanan ${nick}`],
    gallery: ["Galeri", "Momen Seru"],
    wishes: ["Kirim Semangat", "Ucapan & Kehadiran"],
    gifts: ["Tanda Sayang", "Kado & Amplop Digital"],
    closing: { thanks: "Terima Kasih!", text: `Sampai jumpa di lintasan! Jangan lupa helm, ya. Kehadiran dan doa teman-teman bikin hari ${names} makin seru.` },
    wishPlaceholder: `Tuliskan ucapan dan doa untuk ${names}…`,
    wishLabel: "Ucapan",
    sent: "Ucapanmu sudah sampai garis finis! Terima kasih ya.",
    closedNote: "Terima kasih atas doa dan perhatiannya. Ucapan masih bisa dikirim lewat form ini.",
    giftIntro: `Kehadiranmu sudah jadi hadiah terbaik. Jika ingin memberi tanda sayang untuk ${names}, dapat melalui:`,
    familyLabel: "Salam sayang",
  };

  return (
    <ThemeShell
      fonts={FONTS}
      background="#bfe6f2"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Art name="bendera" eager className={s.bunting} />
          <div className={s.coverHead}>
            <p className={s.kicker}>Undangan {label}</p>
            <h1 className={s.coverName}>{names}</h1>
            <p className={s.ageText}>{age ? `ulang tahun ke-${age}!` : "ayo gowes bareng!"}</p>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
          </div>
          <div className={s.stage} aria-hidden>
            <div className={s.park}><Art name="taman" eager /></div>
            <div className={s.bike}>
              <div className={s.balloons}><Art name="balon" eager />{age && <b className={s.balloonAge}>{age}</b>}</div>
              <Art name="sepeda" eager />
            </div>
          </div>
          <div className={s.card}>
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
        light="#ffffff"
        dark="#233554"
        copy={copy}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            <Art name="bendera" className={s.heroBunting} />
            <p className={s.heroKicker}>Hore! {label}</p>
            <h1 className={s.heroName}>{names}</h1>
            {age && <p className={s.heroAge}>{age} Tahun</p>}
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            <Art name="sepeda" className={s.heroBike} />
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="panji" className={s.divider} />,
          node: <Art name="helm" />,
          amp: <Art name="helm" />,
          portrait: <Art name="helm" className={s.portraitArt} />,
          closingDecor: <Art name="taman" className={s.closingScene} />,
          closingEmblem: <Art name="helm" className={s.closingEmblem} />,
          sentArt: <Art name="helm" />,
        }}
      />
    </ThemeShell>
  );
}
