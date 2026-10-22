"use client";
// Theme "Ultah Safari" — ulang tahun anak di padang savana saat matahari sore: jerapah jangkung, gajah kecil bertopi
// pesta, anak singa yang duduk manis, pohon akasia berpayung dan jip safari terbuka (gouache + krayon, karakter asli).
// Cap paspor untuk umur, tiket ekspedisi untuk tamu, halaman buku lapangan, jejak kaki untuk cerita, langit senja untuk
// hitung mundur.
import { Lucide, ThemeShell, formatDate, guestLabel, toDate, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Chewy", "Lexend:wght@400;500;600;700"];
// Painted by /tmp/pen/art/themes/ultah-safari.py (tools/art/themes in the repo).
const Art = makeArt("ultah-safari", { giraffe: [230, 479], elephant: [300, 266], lion: [210, 262], acacia: [320, 229], jeep: [320, 195], grass: [640, 115] } as const);

const WISHES = [
  { id: "w1", name: "Naira & Bunda", attendance: "yes" as const, message: "Selamat ulang tahun, Alesha! Naira sudah siap pakai topi petualang. Semoga sehat selalu dan makin berani menjelajah." },
  { id: "w2", name: "Keluarga Om Hendra", attendance: "yes" as const, message: "Selamat lima tahun, anak singa kecil! Semoga tumbuh jadi anak yang penyayang, pintar, dan selalu ceria." },
  { id: "w3", name: "Tante Dewi", attendance: "maybe" as const, message: "Maaf belum tentu bisa datang, Sayang. Doa Tante dari jauh, semoga cita-cita jadi dokter hewan tercapai." },
];

function ageAt(birth?: string, at?: string) {
  const b = toDate(birth);
  const d = toDate(at);
  if (!b || !d) return undefined;
  let age = d.getFullYear() - b.getFullYear();
  if (d.getMonth() < b.getMonth() || (d.getMonth() === b.getMonth() && d.getDate() < b.getDate())) age -= 1;
  return age > 0 && age < 30 ? age : undefined;
}

function Divider() {
  return <span className={s.divider} aria-hidden><i /><Art name="acacia" /><i /></span>;
}

export default function UltahSafariTheme(props: ThemeProps) {
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
      kicker: "Halo, Para Penjelajah!",
      title: "Ayo Berpetualang!",
      intro: `Dengan penuh sukacita, kami mengundang teman-teman dan keluarga untuk merayakan ${label.toLowerCase()} ${names}${age ? ` yang ke-${age}` : ""}. Jerapah, gajah, dan anak singa sudah menunggu di padang rumput. Kehadiranmu membuat petualangan ini makin seru!`,
    },
    roles: ["Ketua Ekspedisi", "Bersama"] as [string, string],
    couple: ["Kenalan Yuk", child ? "Si Penjelajah Kecil" : "Yang Merayakan"] as [string, string],
    count: ["Matahari Hampir Terbenam", "Menuju Hari Petualangan"] as [string, string],
    units: ["Hari", "Jam", "Menit", "Detik"] as [string, string, string, string],
    events: ["Peta Ekspedisi", "Waktu & Tempat"] as [string, string],
    story: ["Jejak Langkah", `Cerita ${nick}`] as [string, string],
    gallery: ["Album", "Foto Petualangan"] as [string, string],
    wishes: ["Pesan Penjelajah", "Ucapan & Kehadiran"] as [string, string],
    gifts: ["Bekal Petualangan", "Kado & Amplop Digital"] as [string, string],
    closing: { thanks: "Terima Kasih!", text: `Kehadiran dan doa teman-teman adalah oleh-oleh terbaik dari petualangan ${names}. Sampai jumpa di padang rumput!` },
    sent: "Hore! Pesanmu sudah sampai di perkemahan. Terima kasih!",
    wishPlaceholder: "Tulis ucapan dan doa untuk si penjelajah kecil…",
    giftIntro: "Kehadiran teman-teman sudah jadi hadiah paling seru. Bila ingin memberi tanda sayang, dapat melalui:",
  };

  return (
    <ThemeShell
      fonts={FONTS}
      background="#fbefd9"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <span className={s.sun} aria-hidden />
          <p className={s.kicker}>Undangan {label}</p>
          <h1 className={s.coverName}>{names}</h1>
          {age && <p className={s.stamp}><small>ke</small><b>{age}</b><small>tahun</small></p>}
          <div className={s.plain} aria-hidden>
            <Art name="acacia" eager className={s.coverTree} />
            <Art name="giraffe" eager className={s.coverGir} />
            <Art name="grass" eager className={s.coverGrass} />
            <Art name="lion" eager className={s.coverLion} />
            <Art name="jeep" eager className={s.coverJeep} />
          </div>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.ticket}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
          </div>
          <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={17} color="#fff8ea" />Mulai Petualangan</button>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        celebrant
        noPhotos={!child?.photo && !data.couple.bridePhoto}
        light="#fff8ea"
        dark="#3a2618"
        copy={copy}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            <div className={s.journal}>
              <p className={s.heroKicker}>Catatan Ekspedisi</p>
              <h1 className={s.heroName}>{names}</h1>
              {age && <p className={s.heroAge}>genap <b>{age}</b> tahun</p>}
              <p className={s.heroDate}>{formatDate(data.date)}</p>
              {note && <p className={s.heroNote}>{note}</p>}
            </div>
            <div className={s.heroPlain} aria-hidden>
              <Art name="grass" className={s.heroGrass} />
              <Art name="elephant" className={s.heroEle} />
              <Art name="jeep" className={s.heroJeep} />
            </div>
          </header>
        )}
        slots={{
          divider: <Divider />,
          node: <Art name="lion" />,
          portrait: <Art name="lion" className={s.peek} />,
          countDecor: <><Art name="acacia" className={s.countTree} /><Art name="grass" className={s.countGrass} /></>,
          closingDecor: <><Art name="grass" className={s.closingGrass} /><Art name="elephant" className={s.closingEle} /><Art name="giraffe" className={s.closingGir} /></>,
          closingEmblem: <Art name="jeep" className={s.closingEmblem} />,
          sentArt: <Art name="lion" />,
        }}
      />
    </ThemeShell>
  );
}
