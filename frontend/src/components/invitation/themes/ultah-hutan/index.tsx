"use client";
// Theme "Ultah Hutan" — pesta ulang tahun penjelajah cilik di hutan, dalam cat gouache: dua batang pohon tinggi membingkai
// sampul dengan untaian bendera di antaranya, burung hantu bertengger yang sesekali bergoyang, usia di atas irisan kayu,
// serta rubah, anak rusa, landak, dan jamur merah di lantai hutan. Hitung mundur di lingkaran tahun kayu, kartu acara
// seperti papan petunjuk berpaku.
import { Lucide, ThemeShell, formatDate, guestLabel, toDate, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Lilita One", "Baloo 2:wght@500;700;800", "Patrick Hand"];
// Painted by /tmp/pen/art/themes/ultah-hutan.py.
const Art = makeArt("ultah-hutan", { batang: [150, 829], bendera: [780, 107], burung: [200, 180], hutan: [780, 295], irisan: [260, 263], jamur: [90, 98], pakis: [400, 86] } as const);

function ageAt(birth?: string, at?: string) {
  const b = toDate(birth);
  const d = toDate(at);
  if (!b || !d) return undefined;
  let age = d.getFullYear() - b.getFullYear();
  if (d.getMonth() < b.getMonth() || (d.getMonth() === b.getMonth() && d.getDate() < b.getDate())) age -= 1;
  return age > 0 && age < 30 ? age : undefined;
}

const WISHES = [
  { id: "w1", name: "Adik Kirana & Keluarga", attendance: "yes" as Attendance, message: "Selamat ulang tahun, Rafa! Semoga makin sehat, makin berani, dan selalu sayang sama hewan-hewan hutan." },
  { id: "w2", name: "Bu Guru Sinta, TK Pelangi Dago", attendance: "yes" as Attendance, message: "Selamat ulang tahun ke-6, penjelajah kecil kami. Terus semangat belajar dan bermain bersama teman ya, Nak." },
  { id: "w3", name: "Om Fajar & Tante Dewi", attendance: "maybe" as Attendance, message: "Happy birthday, Rafa! Kalau sempat, Om bawakan senter untuk berkemah. Doa terbaik dari kami." },
];

export default function UltahHutanTheme(props: ThemeProps) {
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
      kicker: "Halo, Teman Hutan!",
      title: "Ayo Berpetualang di Pestaku!",
      intro: `Burung hantu sudah bangun, rubah dan rusa sudah menunggu. Dengan penuh sukacita kami mengundang teman-teman dan keluarga untuk merayakan ${label.toLowerCase()} ${names}${age ? ` yang ke-${age}` : ""} di tengah hutan. Kita akan menjelajah, bermain, dan tiup lilin bersama!`,
    },
    roles: ["Penjelajah Cilik", "Bersama"],
    couple: ["Kenalan Yuk", child ? "Si Penjelajah" : "Yang Merayakan"],
    count: ["Petualangan Dimulai Dalam", "Hitung Mundur Pesta"],
    units: ["Hari", "Jam", "Menit", "Detik"],
    events: ["Peta Pesta", "Waktu & Tempat"],
    story: ["Buku Jelajah", `Tumbuh Bersama ${nick}`],
    gallery: ["Galeri", "Momen di Hutan"],
    wishes: ["Titip Pesan", "Ucapan & Kehadiran"],
    gifts: ["Tanda Sayang", "Kado & Amplop Digital"],
    closing: { thanks: "Terima Kasih!", text: `Sampai jumpa di hutan! Kehadiran dan doa teman-teman membuat petualangan ${names} makin seru.` },
    wishPlaceholder: `Tuliskan ucapan dan doa untuk ${names}…`,
    sent: "Hore! Ucapanmu sudah dibawa burung hantu. Terima kasih ya.",
    closedNote: "Terima kasih atas doa dan perhatiannya. Ucapan masih bisa dikirim lewat form ini.",
    giftIntro: `Kehadiranmu sudah jadi hadiah terbaik. Jika ingin memberi tanda sayang untuk ${names}, dapat melalui:`,
    familyLabel: "Salam sayang",
  };

  return (
    <ThemeShell
      fonts={FONTS}
      background="#eef3e0"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Art name="batang" eager className={`${s.trunk} ${s.trunkL}`} />
          <Art name="batang" eager className={`${s.trunk} ${s.trunkR}`} />
          <Art name="bendera" eager className={s.bunting} />
          <Art name="burung" eager className={s.owl} />
          <p className={s.kicker}>Undangan {label}</p>
          <p className={s.coverLead}>ayo ke pesta hutan</p>
          <h1 className={s.coverName}>{names}</h1>
          <div className={s.ageRow}>
            {age && <div className={s.slice}><Art name="irisan" eager /><b>{age}</b></div>}
            <p className={s.ageText}><small>yuk rayakan</small>{age ? `ulang tahun ke-${age}` : "pesta ulang tahun"}</p>
          </div>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.guestWrap}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={17} color="#ffffff" />Buka Undangan</button>
          </div>
          <Art name="hutan" eager className={s.scene} />
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        celebrant
        noPhotos={!child?.photo && !data.couple.bridePhoto}
        light="#fff3d6"
        dark="#553823"
        copy={copy}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            <Art name="bendera" className={s.heroBunting} />
            <Art name="burung" className={s.heroOwl} />
            <p className={s.heroKicker}>Hore! {label}</p>
            <h1 className={s.heroName}>{names}</h1>
            {age && <p className={s.heroAge}>{age} Tahun</p>}
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="pakis" className={s.divider} />,
          node: <Art name="jamur" />,
          amp: <Art name="jamur" />,
          portrait: <Art name="burung" className={s.portraitArt} />,
          countDecor: <><Art name="jamur" className={`${s.countJamur} ${s.countJamurL}`} /><Art name="jamur" className={`${s.countJamur} ${s.countJamurR}`} /></>,
          closingDecor: <Art name="hutan" className={s.closingScene} />,
          closingEmblem: <Art name="burung" className={s.closingEmblem} />,
          sentArt: <Art name="jamur" />,
        }}
      />
    </ThemeShell>
  );
}
