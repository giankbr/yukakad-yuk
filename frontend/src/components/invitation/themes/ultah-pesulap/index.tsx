"use client";
// Theme "Ultah Pesulap" — ulang tahun anak bertema pertunjukan sulap, gouache: panggung malam nila dengan tirai
// beludru ungu berumbai emas, topi tinggi dengan kelinci putih yang mengintip (desain asli), tongkat ajaib berbintang,
// kartu remi berkipas tanpa gambar wajah. Kartu acara seperti kartu remi, bingkai potret berlampu panggung.
import { Lucide, ThemeShell, formatDate, guestLabel, toDate, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Cherry Swash:wght@400;700", "Baloo 2:wght@400;500;600;700;800"];
// Painted by /tmp/pen/art/themes/ultah-pesulap.py (valance is a CSS background)
const Art = makeArt("ultah-pesulap", { stage: [380, 334], curtain: [150, 1150], cards: [210, 160], wand: [180, 65], star: [96, 92] } as const);

const WISHES = [
  { id: "w1", name: "Keluarga Om Bayu", attendance: "yes" as Attendance, message: "Selamat ulang tahun, pesulap kecil! Semoga makin sehat, makin pintar, dan selalu bikin semua orang tersenyum. Kami siap jadi penonton paling heboh!" },
  { id: "w2", name: "Kayla & Mama", attendance: "yes" as Attendance, message: "Kayla sudah latihan tepuk tangan dari kemarin! Selamat ulang tahun, semoga semua keinginanmu muncul seperti kelinci dari topi." },
  { id: "w3", name: "Tante Dewi", attendance: "maybe" as Attendance, message: "Maaf belum tentu bisa datang, Sayang. Doa Tante, tumbuh jadi anak yang baik hati, berani, dan penuh keajaiban." },
];

function ageAt(birth?: string, at?: string) {
  const b = toDate(birth);
  const d = toDate(at);
  if (!b || !d) return undefined;
  let age = d.getFullYear() - b.getFullYear();
  if (d.getMonth() < b.getMonth() || (d.getMonth() === b.getMonth() && d.getDate() < b.getDate())) age -= 1;
  return age > 0 && age < 30 ? age : undefined;
}

export default function UltahPesulapTheme(props: ThemeProps) {
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
      kicker: "Hadirin yang Terhormat",
      title: "Abrakadabra!",
      sub: "Pertunjukan sebentar lagi dimulai",
      intro: `Dengan gembira kami mengundang teman-teman dan keluarga untuk merayakan ${label.toLowerCase()} ${names}${age ? ` yang ke-${age}` : ""}. Ada sulap, kelinci, kartu ajaib, dan kue ulang tahun. Kehadiran kalian adalah trik paling menakjubkan!`,
    },
    roles: ["Pesulap Cilik", "Bersama"],
    couple: ["Perkenalkan", child ? "Sang Pesulap Cilik" : "Yang Berulang Tahun"],
    count: ["Tirai Segera Dibuka", "Menuju Hari Pertunjukan"],
    units: ["Hari", "Jam", "Menit", "Detik"],
    events: ["Jadwal Pertunjukan", "Waktu & Tempat"],
    story: ["Di Balik Topi", `Cerita ${nick}`],
    gallery: ["Album Foto", "Momen Ajaib"],
    wishes: ["Tepuk Tangan & Doa", "Ucapan & Kehadiran"],
    gifts: ["Tanda Sayang", "Kado & Amplop Digital"],
    closing: { thanks: "Terima Kasih!", text: `Tepuk tangan, tawa, dan doa teman-teman adalah keajaiban paling indah untuk ${names}. Sampai jumpa di depan panggung!` },
    sent: "Tada! Ucapanmu sudah sampai. Terima kasih banyak.",
    attend: { maybe: "Belum Pasti" },
    wishPlaceholder: "Tulis ucapan dan doa untuk si pesulap cilik…",
    giftIntro: "Kehadiranmu sudah jadi hadiah terbaik. Kalau ingin memberi kado, bisa melalui:",
    giftAddressTitle: "Kirim Kado",
    familyLabel: "Salam hangat dari keluarga",
  };

  return (
    <ThemeShell
      fonts={FONTS}
      background="#1d1a45"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <span className={s.valance} aria-hidden />
          <Art name="curtain" eager className={s.curtainL} />
          <Art name="curtain" eager className={s.curtainR} />
          <p className={s.marquee}>Undangan {label}</p>
          <h1 className={s.coverName}>{names}</h1>
          {age && <p className={s.coverAge}>yang ke<span className={s.ageStar}><Art name="star" eager /><b>{age}</b></span>tahun</p>}
          <div className={s.stage} aria-hidden><Art name="stage" eager /></div>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={`${s.ticket} ${s.guest}`}>
            <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
            <strong>{guestLabel(data)}</strong>
            {table && <span className={s.table}>{table}</span>}
          </div>
          <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={17} color="#1d1a45" />Mulai Pertunjukan</button>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        celebrant
        noPhotos={!child?.photo && !data.couple.bridePhoto}
        light="#fbf7f2"
        dark="#1d1a45"
        copy={copy}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            <div className={s.bill}>
              <p className={s.heroKicker}>Pertunjukan Spesial</p>
              <h1 className={s.heroName}>{names}</h1>
              {age && <p className={s.heroAge}>genap <b>{age}</b> tahun</p>}
              <p className={s.heroDate}>{formatDate(data.date)}</p>
              <Art name="cards" className={s.heroCards} />
            </div>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <span className={s.divider} aria-hidden><Art name="wand" /></span>,
          node: <Art name="star" />,
          portrait: <Art name="cards" className={s.portraitArt} />,
          countDecor: <span className={s.countValance} aria-hidden />,
          closingDecor: <span className={s.closingValance} aria-hidden />,
          closingEmblem: <Art name="stage" className={s.closingEmblem} />,
          sentArt: <Art name="stage" />,
        }}
      />
    </ThemeShell>
  );
}
