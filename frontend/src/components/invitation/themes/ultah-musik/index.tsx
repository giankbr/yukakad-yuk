"use client";
// Theme "Ultah Musik" — konser mini ulang tahun anak: panggung ungu bertirai merah, dua lampu sorot warna-warni, drum
// mainan, gitar kecil, xilofon pelangi dan terompet (gouache), not balok yang menari, dan hitung mundur di tuts xilofon.
import { Lucide, ThemeShell, formatDate, guestLabel, toDate, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Lilita One", "Nunito:wght@400;600;700;800;900", "Gochi Hand"];
// Painted by /tmp/pen/art/themes/ultah-musik.py (tools/art/themes in the repo).
const Art = makeArt("ultah-musik", {
  band: [720, 490], not1: [90, 145], not2: [90, 115], not3: [59, 167], lampu: [110, 147], paranada: [280, 55],
} as const);

function ageAt(birth?: string, at?: string) {
  const b = toDate(birth);
  const d = toDate(at);
  if (!b || !d) return undefined;
  let age = d.getFullYear() - b.getFullYear();
  if (d.getMonth() < b.getMonth() || (d.getMonth() === b.getMonth() && d.getDate() < b.getDate())) age -= 1;
  return age > 0 && age < 30 ? age : undefined;
}

const WISHES = [
  { id: "w1", name: "Keira & Mama", attendance: "yes" as const, message: "Selamat ulang tahun, Shaka! Keira mau main drum bareng. Semoga sehat, pintar, dan makin suka bernyanyi." },
  { id: "w2", name: "Om Rizal", attendance: "yes" as const, message: "Happy birthday, rocker cilik! Semoga jadi anak yang soleh, ceria, dan selalu bikin orang tua bangga." },
  { id: "w3", name: "Tante Sinta & Keluarga", attendance: "maybe" as const, message: "Maaf kalau belum bisa datang, ya. Doa terbaik untuk Shaka di usia enam tahun!" },
];

export default function UltahMusikTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Ulang Tahun";
  const child = data.extras?.child?.enabled !== false && data.extras?.child?.name?.trim() ? data.extras.child : undefined;
  const nick = child?.nickname?.trim() || child?.name.trim() || data.couple.bride;
  const names = child ? nick : [data.couple.bride, data.couple.groom?.trim()].filter(Boolean).join(" & ");
  const age = ageAt(child?.birthDate, data.date);
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const copy = {
    ...DEFAULT_COPY,
    opening: {
      kicker: "Halo, Teman-teman!",
      title: "Ayo Ikut Konser Ulang Tahunku!",
      intro: `Dengan penuh sukacita, kami mengundang teman-teman dan keluarga untuk merayakan ${label.toLowerCase()} ${names}${age ? ` yang ke-${age}` : ""}. Bawa suara terbaikmu, kita bernyanyi dan bermain musik bersama!`,
    },
    roles: ["Bintang Panggung", "Bersama"] as [string, string],
    couple: ["Kenalan Dulu, Yuk", child ? "Si Musisi Cilik" : "Yang Merayakan"] as [string, string],
    count: ["Siap-siap, ya!", "Menuju Hari Konser"] as [string, string],
    units: ["Hari", "Jam", "Menit", "Detik"] as [string, string, string, string],
    events: ["Catat Jadwalnya", "Waktu & Tempat"] as [string, string],
    story: ["Lagu Kehidupan", `Cerita ${nick}`] as [string, string],
    gallery: ["Album", "Momen Seru"] as [string, string],
    wishes: ["Kirim Doa", "Ucapan & Kehadiran"] as [string, string],
    gifts: ["Tanda Sayang", "Kado & Amplop Digital"] as [string, string],
    closing: { thanks: "Terima Kasih!", text: `Sampai jumpa di konser kecil kami! Kehadiran dan doa teman-teman adalah musik paling indah untuk ${names}.` },
    sent: "Hore, ucapanmu sudah terkirim! Terima kasih banyak.",
    wishPlaceholder: `Tulis ucapan dan doa untuk ${names}…`,
    giftIntro: "Kehadiran teman-teman sudah jadi kado terbaik. Jika ingin memberi tanda sayang, bisa melalui:",
  };

  const notes = (
    <>
      <Art name="not1" eager className={s.n1} />
      <Art name="not2" eager className={s.n2} />
      <Art name="not3" eager className={s.n3} />
    </>
  );

  return (
    <ThemeShell
      fonts={FONTS}
      background="#3b1d5e"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <span className={s.beams} aria-hidden />
          <Art name="lampu" eager className={s.lampL} />
          <Art name="lampu" eager className={s.lampR} />
          <p className={s.pill}>Undangan {label}</p>
          <h1 className={s.coverName}>{names}</h1>
          {age && <p className={s.age}>ulang tahun ke <b>{age}</b></p>}
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
            {notes}
            <Art name="band" eager className={s.band} />
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        celebrant
        noPhotos={!child?.photo && !data.couple.bridePhoto}
        light="#fff6e6"
        dark="#2d1846"
        copy={copy}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            <span className={s.beams} aria-hidden />
            <p className={s.heroKicker}>Hore! {label}</p>
            <h1 className={s.heroName}>{names}{age ? ` ${age} Tahun` : ""}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            <Art name="band" className={s.heroBand} />
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="paranada" className={s.divider} />,
          node: <Art name="not3" />,
          portrait: <Art name="not2" />,
          closingEmblem: (
            <>
              <p className={s.closingName}>{names}</p>
              <Art name="band" className={s.closingBand} />
            </>
          ),
          sentArt: <Art name="band" />,
        }}
      />
    </ThemeShell>
  );
}
