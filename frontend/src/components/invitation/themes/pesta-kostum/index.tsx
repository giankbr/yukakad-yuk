"use client";
// Theme "Pesta Kostum" — ulang tahun anak bertema pesta kostum dalam kolase kertas guntingan (desain orisinal): rak baju
// dandan berisi jubah, jubah bintang, rok tutu, tunik ksatria karton, dan baju beruang; topeng kertas bertelinga kucing,
// mahkota karton, tongkat bintang, dan tiga anak berkostum buatan sendiri di panggung kecil berbendera (tokoh orisinal).
// Kartu tamu berupa stiker nama, usia di dalam mahkota, potret di cermin dandan, hitung mundur dan acara sebagai label
// baju bergantung, form bertepi jahitan.
import { Lucide, ThemeShell, formatDate, guestLabel, toDate, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Titan One", "Lexend:wght@400;600;700;800"];
// Painted by /tmp/pen/art/themes/pesta-kostum.py
const Art = makeArt("pesta-kostum", { rak: [780, 439], anak: [752, 501], mahkota: [240, 153], topeng: [220, 111], tongkat: [110, 258] } as const);

function ageAt(birth?: string, at?: string) {
  const b = toDate(birth);
  const d = toDate(at);
  if (!b || !d) return undefined;
  let age = d.getFullYear() - b.getFullYear();
  if (d.getMonth() < b.getMonth() || (d.getMonth() === b.getMonth() && d.getDate() < b.getDate())) age -= 1;
  return age > 0 && age < 30 ? age : undefined;
}

const WISHES = [
  { id: "w1", name: "Adik Bima & Keluarga", attendance: "yes" as Attendance, message: "Selamat ulang tahun, Gendis! Bima mau datang jadi ksatria karton, sudah latihan pakai tameng dari kardus." },
  { id: "w2", name: "Bu Guru Wulan, TK Kuncup Melati", attendance: "yes" as Attendance, message: "Selamat ulang tahun ke-6, kucing ungu kesayangan kami. Semoga makin pintar, berani, dan suka menolong teman." },
  { id: "w3", name: "Om Dani & Tante Rini", attendance: "maybe" as Attendance, message: "Happy birthday, Gendis! Kalau sempat, Tante bawakan sayap peri. Doa terbaik dari kami." },
];

export default function PestaKostumTheme(props: ThemeProps) {
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
      title: "Ayo Datang Berkostum!",
      intro: `Siapkan jubah, mahkota, atau topeng kertasmu. Dengan penuh sukacita kami mengundang teman-teman dan keluarga untuk merayakan ${label.toLowerCase()} ${names}${age ? ` yang ke-${age}` : ""}. Kita akan berdandan, berparade di panggung kecil, dan tiup lilin bersama!`,
    },
    roles: ["Bintang Pesta", "Bersama"],
    couple: ["Kenalan yuk", child ? "Si Bintang Pesta" : "Yang Merayakan"],
    count: ["Pesta dimulai dalam", "Hitung Mundur"],
    units: ["Hari", "Jam", "Menit", "Detik"],
    events: ["Label pesta", "Waktu & Tempat"],
    story: ["Lemari kenangan", `Tumbuh Bersama ${nick}`],
    gallery: ["Galeri", "Momen Berkostum"],
    wishes: ["Titip pesan", "Ucapan & Kehadiran"],
    gifts: ["Tanda sayang", "Kado & Amplop Digital"],
    closing: { thanks: "Terima Kasih!", text: `Sampai jumpa di pesta kostum! Kehadiran dan doa teman-teman membuat hari ${names} makin meriah.` },
    attend: { maybe: "Mungkin" },
    wishPlaceholder: `Tuliskan ucapan dan doa untuk ${names}…`,
    sent: "Hore! Ucapanmu sudah ditempel di rak kostum. Terima kasih ya.",
    closedNote: "Terima kasih atas doa dan perhatiannya. Ucapan masih bisa dikirim lewat form ini.",
    giftIntro: `Kehadiranmu sudah jadi hadiah terbaik. Jika ingin memberi tanda sayang untuk ${names}, dapat melalui:`,
    familyLabel: "Salam sayang",
  };

  return (
    <ThemeShell
      fonts={FONTS}
      background="#f6e6c8"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Art name="rak" eager className={s.rack} />
          <Art name="topeng" eager className={`${s.mask} ${s.maskA}`} />
          <Art name="tongkat" eager className={s.wand} />
          <p className={s.kicker}>Undangan Pesta Kostum</p>
          <h1 className={s.name}>{names}</h1>
          <div className={s.ageRow}>
            {age && <div className={s.crownAge}><Art name="mahkota" eager /><b>{age}</b></div>}
            <p className={s.ageText}><small>yuk rayakan</small>{age ? `${label.toLowerCase()} ke-${age}` : label.toLowerCase()}</p>
          </div>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <span className={s.spacer} aria-hidden />
          <div className={s.sticker}>
            <div className={s.stickerHead}><b>HALO!</b><small>tamu istimewa kami</small></div>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
          </div>
          <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={18} color="#2d2440" />Buka Undangan</button>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        celebrant
        noPhotos={!child?.photo && !data.couple.bridePhoto}
        light="#ffffff"
        dark="#2d2440"
        copy={copy}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            <p className={s.heroKicker}>Hore! {label}</p>
            <h1 className={s.heroName}>{names}</h1>
            {age && <p className={s.heroAge}>{age} Tahun</p>}
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            <Art name="anak" className={s.heroStage} />
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="topeng" className={s.divider} />,
          node: <Art name="tongkat" />,
          amp: <Art name="topeng" />,
          portrait: <Art name="mahkota" className={s.pCrown} />,
          countDecor: <><Art name="topeng" className={`${s.countMask} ${s.countMaskL}`} /><Art name="topeng" className={`${s.countMask} ${s.countMaskR}`} /></>,
          closingEmblem: <Art name="anak" className={s.closingStage} />,
          sentArt: <Art name="mahkota" />,
        }}
      />
    </ThemeShell>
  );
}
