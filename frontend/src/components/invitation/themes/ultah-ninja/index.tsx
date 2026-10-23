"use client";
// Theme "Ultah Ninja" — ulang tahun anak bertema ninja cilik: atap genteng di bawah bulan purnama dengan bambu dan
// lampion (lukisan gouache buku cerita), nama si kecil di gulungan kertas, dua ninja cilik orisinal (tudung bulat, mata
// besar, ikat kepala berkibar) yang melompat-lompat, dan bintang lempar dari busa lembut yang berputar. Riang dan aman,
// tanpa senjata tajam.
import { Lucide, ThemeShell, formatDate, guestLabel, toDate, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Lilita One", "Baloo 2:wght@500;600;700;800"];
// Painted by /tmp/pen/art/themes/ultah-ninja.py (night is a CSS background).
const Art = makeArt("ultah-ninja", {
  ninjaA: [255, 257], ninjaB: [238, 231], star: [110, 111], scroll: [480, 225], bamboo: [140, 509], divider: [300, 53],
} as const);

const WISHES = [
  { id: "w1", name: "Kayla & Mama", attendance: "yes" as const, message: "Selamat ulang tahun, Ninja Raka! Kayla sudah latihan lempar bintang busa. Semoga sehat, makin pintar, dan makin berani." },
  { id: "w2", name: "Keluarga Om Bayu", attendance: "yes" as const, message: "Selamat tujuh tahun, jagoan! Semoga selalu jadi ninja yang baik hati dan suka menolong teman." },
  { id: "w3", name: "Tante Sari, Bandung", attendance: "maybe" as const, message: "Maaf belum tentu bisa datang, Sayang. Kadonya menyusul lewat pos ya. Peluk jauh!" },
];

function ageAt(birth?: string, at?: string) {
  const b = toDate(birth);
  const d = toDate(at);
  if (!b || !d) return undefined;
  let age = d.getFullYear() - b.getFullYear();
  if (d.getMonth() < b.getMonth() || (d.getMonth() === b.getMonth() && d.getDate() < b.getDate())) age -= 1;
  return age > 0 && age < 30 ? age : undefined;
}

export default function UltahNinjaTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Ulang Tahun";
  const child = data.extras?.child?.enabled !== false && data.extras?.child?.name?.trim() ? data.extras.child : undefined;
  const nick = child?.nickname?.trim() || child?.name.trim() || data.couple.bride;
  const names = child ? nick : [data.couple.bride, data.couple.groom?.trim()].filter(Boolean).join(" & ");
  const age = ageAt(child?.birthDate, data.date);
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#1d2459"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Art name="star" eager className={`${s.fly} ${s.flyA}`} />
          <Art name="star" eager className={`${s.fly} ${s.flyB}`} />
          <Art name="star" eager className={`${s.fly} ${s.flyC}`} />
          <div className={s.scrollWrap}>
            <Art name="scroll" eager className={s.scrollImg} />
            <div className={s.scrollText}>
              <p className={s.kicker}>Undangan {label}</p>
              <h1 className={s.coverNames}>{names}</h1>
              <p className={s.coverDate}>{formatDate(data.date)}</p>
            </div>
            {age && <span className={s.ageStar}><Art name="star" eager /><b>{age}</b><small>tahun</small></span>}
          </div>
          <div className={s.guestCard}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={18} color="#ffffff" />Buka Undangan</button>
          </div>
          <div className={s.roof} aria-hidden>
            <Art name="ninjaB" eager className={s.ninjaB} />
            <Art name="ninjaA" eager className={s.ninjaA} />
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
        dark="#1d2459"
        demoWishes={WISHES}
        copy={{
          opening: {
            kicker: "Halo, ninja-ninja cilik!",
            title: "Misi Rahasia: Pesta Ulang Tahun",
            intro: `Dengan penuh sukacita, kami mengundang teman-teman dan keluarga untuk merayakan ${label.toLowerCase()} ${names}${age ? ` yang ke-${age}` : ""}. Siapkan ikat kepalamu, kita berlatih jurus lompat, lempar bintang busa, lalu tiup lilin bersama!`,
          },
          roles: ["Ninja yang Berulang Tahun", "Bersama"],
          couple: ["Kenalan dulu", child ? "Si Ninja Cilik" : "Yang Merayakan"],
          count: ["Bersiap-siap", "Menuju Hari Misi"],
          units: ["Hari", "Jam", "Menit", "Detik"],
          events: ["Lokasi markas", "Waktu & Tempat"],
          story: ["Gulungan cerita", `Cerita ${nick}`],
          gallery: ["Album", "Foto Ceria"],
          wishes: ["Kirim pesan rahasia", "Ucapan & Kehadiran"],
          gifts: ["Tanda sayang", "Kado & Amplop Digital"],
          closing: { thanks: "Terima Kasih!", text: `Kehadiran dan doa teman-teman membuat hari ${names} makin seru. Sampai jumpa di markas ninja!` },
          sent: "Pesan rahasiamu sudah sampai. Terima kasih, Ninja!",
          attend: { maybe: "Mungkin" },
          wishPlaceholder: "Tulis ucapan dan doa untuk si kecil…",
          closedNote: "Terima kasih sudah ikut merayakan! Ucapan masih bisa dikirim lewat form ini.",
          giftIntro: "Kehadiran teman-teman sudah jadi hadiah paling indah. Bila ingin memberi tanda sayang, dapat melalui:",
          familyLabel: "Dengan sayang,",
        }}
        hero={(
          <header className={s.hero}>
            <Art name="bamboo" className={s.bambooL} />
            <Art name="bamboo" className={s.bambooR} />
            <p className={s.heroKicker}>Pesta {label}</p>
            <div className={s.heroStage}>
              <Art name="ninjaA" className={s.heroNinja} />
              {age && <span className={s.heroAge} aria-hidden><Art name="star" /><b>{age}</b></span>}
            </div>
            <h1 className={s.heroNames}>{names}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="divider" className={s.divider} />,
          node: <Art name="star" />,
          amp: <Art name="star" />,
          portrait: <Art name="star" className={s.portraitArt} />,
          countDecor: <><Art name="ninjaB" className={`${s.countNinja} ${s.countNinjaB}`} /><Art name="ninjaA" className={`${s.countNinja} ${s.countNinjaA}`} /></>,
          closingDecor: <div className={s.closingRoof} aria-hidden><Art name="ninjaB" /><Art name="ninjaA" /></div>,
          closingEmblem: <Art name="star" className={s.closingEmblem} />,
          sentArt: <Art name="star" />,
        }}
      />
    </ThemeShell>
  );
}
