"use client";
// Theme "Ultah Balap" — ulang tahun anak bertema balap mobil dalam gouache: sirkuit dilihat dari atas (rumput, kerb
// merah-putih, grid start) dengan dua mobil balap kartun yang melaju, papan pit berisi umur di tengah lapangan, piala
// emas dan bendera kotak-kotak; hitung mundur di papan waktu lap, garis finis di penutup.
import { Lucide, ThemeShell, formatDate, guestLabel, toDate, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Bowlby One", "Exo 2:ital,wght@0,500;0,700;0,800;1,700;1,800"];
// Painted by /tmp/pen/art/themes/ultah-balap.py
const Art = makeArt("ultah-balap", {
  track: [560, 761], cartop: [120, 216], cartop2: [120, 216], carside: [440, 135], carside2: [440, 135],
  trophy: [200, 243], flags: [260, 155], board: [180, 223],
} as const);

const WISHES = [
  { id: "w1", name: "Kiano & Mama", attendance: "yes" as const, message: "Selamat ulang tahun, Rafka! Kiano sudah siap balapan, tapi nanti kita finis bareng ya. Sehat dan ceria selalu!" },
  { id: "w2", name: "Keluarga Om Bayu", attendance: "yes" as const, message: "Selamat lima tahun, jagoan! Semoga makin pintar, berani, dan selalu sayang teman." },
  { id: "w3", name: "Tante Rara", attendance: "maybe" as const, message: "Tante usahakan datang, Sayang. Kadonya sudah siap di garasi Tante. Tancap gas terus, Rafka!" },
];

function ageAt(birth?: string, at?: string) {
  const b = toDate(birth);
  const d = toDate(at);
  if (!b || !d) return undefined;
  let age = d.getFullYear() - b.getFullYear();
  if (d.getMonth() < b.getMonth() || (d.getMonth() === b.getMonth() && d.getDate() < b.getDate())) age -= 1;
  return age > 0 && age < 30 ? age : undefined;
}

export default function UltahBalapTheme(props: ThemeProps) {
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
      background="#4caf50"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.circuit}>
            <Art name="cartop" eager className={`${s.car} ${s.carL}`} />
            <Art name="cartop2" eager className={`${s.car} ${s.carR}`} />
            <div className={s.infield}>
              <span className={s.tag}>Undangan {label}</span>
              <div className={s.pit} aria-hidden>
                <Art name="board" eager />
                <span className={s.pitText}><b>{age ?? "GO"}</b><small>{age ? "tahun" : "start!"}</small></span>
              </div>
              <h1 className={s.coverName}>{names}</h1>
            </div>
          </div>
          <div className={s.coverMeta}>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
            <div className={`${s.ticket} ${s.guest}`}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={17} color="#ffffff" />Ayo Balapan!</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        celebrant
        noPhotos={!child?.photo && !data.couple.bridePhoto}
        light="#ffd23f"
        dark="#22252d"
        demoWishes={WISHES}
        copy={{
          opening: {
            kicker: "Mesin menyala!",
            title: "Siap di Garis Start",
            intro: `Dengan penuh sukacita, kami mengundang teman-teman dan keluarga untuk merayakan ${label.toLowerCase()} ${names}${age ? ` yang ke-${age}` : ""}. Pakai helm semangatmu, kita balapan, bersorak, dan tiup lilin bersama di garis finis!`,
          },
          roles: ["Pembalap Utama", "Bersama"],
          couple: ["Kenalan dengan", child ? "Sang Juara Hari Ini" : "Yang Merayakan"],
          count: ["Lampu start", "Hitung Mundur Balapan"],
          units: ["Hari", "Jam", "Menit", "Detik"],
          events: ["Catat jadwalnya", "Lintasan & Waktu"],
          story: ["Lap demi lap", `Cerita ${nick}`],
          gallery: ["Album", "Foto Balapan"],
          wishes: ["Sorakan untuk juara", "Ucapan & Kehadiran"],
          gifts: ["Tanda sayang", "Kado & Amplop Digital"],
          closing: { thanks: "Sampai di Garis Finis!", text: `Kehadiran dan doa teman-teman membuat hari ${names} jadi juara. Sampai jumpa di lintasan!` },
          sent: "Hore! Sorakanmu sudah terkirim. Terima kasih!",
          attend: { yes: "Ikut Balapan", maybe: "Mungkin", no: "Belum Bisa" },
          wishPlaceholder: "Tulis ucapan dan doa untuk si kecil…",
          closedNote: "Terima kasih sudah ikut merayakan! Ucapan masih bisa dikirim lewat form ini.",
          giftIntro: "Kehadiran teman-teman sudah jadi hadiah paling seru. Bila ingin memberi tanda sayang, dapat melalui:",
          familyLabel: "Salam hangat dari tim pit,",
        }}
        hero={(
          <header className={s.hero}>
            <Art name="flags" className={s.heroFlags} />
            <p className={s.heroKicker}>Grand Prix {label}</p>
            <h1 className={s.heroName}>{names}</h1>
            {age && <p className={s.heroAge}>yang ke<b>{age}</b>tahun</p>}
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
            <div className={s.heroTrack} aria-hidden><Art name="carside" className={s.heroCar} /></div>
          </header>
        )}
        slots={{
          divider: <span className={s.divider} aria-hidden><Art name="flags" /></span>,
          node: <Art name="cartop2" />,
          portrait: <Art name="trophy" className={s.peek} />,
          closingDecor: <Art name="trophy" className={s.closingTrophy} />,
          closingEmblem: <div className={s.closingRace} aria-hidden><Art name="carside" /><Art name="carside2" /></div>,
          sentArt: <Art name="trophy" />,
        }}
      />
    </ThemeShell>
  );
}
