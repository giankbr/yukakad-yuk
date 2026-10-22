"use client";
// Theme "Ultah Balerina" — ulang tahun anak bertema balet, dilukis dengan gouache dan pensil warna: panggung kecil
// bertirai beludru merah muda dengan tali emas dan rumbai, sepatu pointe satin yang tergantung pada pitanya, tutu tule
// berlapis, kotak musik dengan penari kecil yang berputar, dan pita satin. Tanpa tokoh terkenal. Kartu undangan
// pertunjukan untuk tamu, poster berbingkai proscenium emas untuk hero, foto bulat yang "memakai" tutu.
import { Lucide, ThemeShell, formatDate, guestLabel, toDate, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Cherry Swash:wght@400;700", "Comfortaa:wght@400;500;700"];
// Painted by /tmp/pen/art/themes/ultah-balerina.py (tools/art/themes in the repo).
const Art = makeArt("ultah-balerina", {
  curtain: [190, 656], valance: [780, 174], shoes: [230, 401], tutu: [230, 154], skirt: [230, 86], musicbox: [260, 260], dancer: [120, 268], bow: [130, 91],
} as const);

const WISHES = [
  { id: "w1", name: "Shakira & Mama", attendance: "yes" as const, message: "Selamat ulang tahun, Kirana! Shakira sudah siap pakai tutu. Semoga makin pintar menari dan selalu ceria." },
  { id: "w2", name: "Keluarga Om Bayu", attendance: "yes" as const, message: "Selamat enam tahun, balerina kecil! Semoga sehat, penyayang, dan selalu berani tampil." },
  { id: "w3", name: "Tante Rina", attendance: "maybe" as const, message: "Maaf belum tentu bisa datang, Sayang. Doa Tante dari Malang, semoga semua impian Kirana terwujud." },
];

function ageAt(birth?: string, at?: string) {
  const b = toDate(birth);
  const d = toDate(at);
  if (!b || !d) return undefined;
  let age = d.getFullYear() - b.getFullYear();
  if (d.getMonth() < b.getMonth() || (d.getMonth() === b.getMonth() && d.getDate() < b.getDate())) age -= 1;
  return age > 0 && age < 30 ? age : undefined;
}

function MusicBox({ className, eager }: { className?: string; eager?: boolean }) {
  return (
    <span className={`${s.box} ${className ?? ""}`} aria-hidden>
      <Art name="musicbox" eager={eager} />
      <span className={s.dancer}><Art name="dancer" eager={eager} /></span>
    </span>
  );
}

function Divider() {
  return <span className={s.divider} aria-hidden><i /><Art name="bow" /><i /></span>;
}

export default function UltahBalerinaTheme(props: ThemeProps) {
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
      kicker: "Halo, teman-teman!",
      title: "Ayo Menari Bersama!",
      intro: `Dengan penuh sukacita, kami mengundang teman-teman dan keluarga untuk merayakan ${label.toLowerCase()} ${names}${age ? ` yang ke-${age}` : ""}. Tirai sudah terbuka, kotak musik sudah berputar, dan panggung kecil ini menunggu kalian. Kehadiranmu membuat pertunjukannya makin indah!`,
    },
    roles: ["Bintang Pertunjukan", "Bersama"] as [string, string],
    couple: ["Perkenalkan", child ? "Si Balerina Kecil" : "Yang Merayakan"] as [string, string],
    count: ["Tirai segera dibuka", "Menuju Hari Pertunjukan"] as [string, string],
    units: ["Hari", "Jam", "Menit", "Detik"] as [string, string, string, string],
    events: ["Program acara", "Waktu & Tempat"] as [string, string],
    story: ["Langkah demi langkah", `Cerita ${nick}`] as [string, string],
    gallery: ["Album", "Foto Kenangan"] as [string, string],
    wishes: ["Tepuk tangan", "Ucapan & Kehadiran"] as [string, string],
    gifts: ["Kado kecil", "Kado & Amplop Digital"] as [string, string],
    closing: { thanks: "Terima Kasih!", text: `Kehadiran dan doa teman-teman adalah tepuk tangan paling meriah untuk ${names}. Sampai jumpa di panggung kecil kami!` },
    sent: "Hore! Ucapanmu sudah sampai di belakang panggung. Terima kasih!",
    wishPlaceholder: "Tulis ucapan dan doa untuk si balerina kecil…",
    giftIntro: "Kehadiran teman-teman sudah jadi hadiah paling indah. Bila ingin memberi tanda sayang, dapat melalui:",
  };

  return (
    <ThemeShell
      fonts={FONTS}
      background="#f6dbe2"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Art name="valance" eager className={s.valance} />
          <span className={`${s.curtain} ${s.curtainL}`} aria-hidden><Art name="curtain" eager /></span>
          <span className={`${s.curtain} ${s.curtainR}`} aria-hidden><Art name="curtain" eager /></span>
          <p className={s.kicker}>Undangan {label}</p>
          <h1 className={s.coverName}>{names}</h1>
          {age && <p className={s.age}>yang ke- <b>{age}</b></p>}
          <MusicBox className={s.coverBox} eager />
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.invite}>
            <span className={s.inviteBow} aria-hidden><Art name="bow" eager /></span>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
          </div>
          <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={17} color="#fffafb" />Buka Tirai</button>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        celebrant
        noPhotos={!child?.photo && !data.couple.bridePhoto}
        light="#fffafb"
        dark="#4a2236"
        copy={copy}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            <span className={s.shoes} aria-hidden><Art name="shoes" /></span>
            <div className={s.poster}>
              <p className={s.heroKicker}>Pertunjukan {label}</p>
              <span className={s.heroTutu} aria-hidden><Art name="tutu" /></span>
              <h1 className={s.heroName}>{names}</h1>
              {age && <p className={s.heroAge}>genap <b>{age}</b> tahun</p>}
              <p className={s.heroDate}>{formatDate(data.date)}</p>
              {note && <p className={s.heroNote}>{note}</p>}
            </div>
          </header>
        )}
        slots={{
          divider: <Divider />,
          node: <Art name="bow" />,
          amp: <Art name="bow" />,
          portrait: <span className={s.tutuSkirt} aria-hidden><Art name="skirt" /></span>,
          countDecor: <Art name="valance" className={s.countValance} />,
          closingDecor: (
            <>
              <Art name="valance" className={s.closeValance} />
              <span className={`${s.closeCurtain} ${s.closeL}`} aria-hidden><Art name="curtain" /></span>
              <span className={`${s.closeCurtain} ${s.closeR}`} aria-hidden><Art name="curtain" /></span>
              <MusicBox className={s.closeBox} />
            </>
          ),
          closingEmblem: <Art name="shoes" className={s.closingEmblem} />,
          sentArt: <Art name="shoes" />,
        }}
      />
    </ThemeShell>
  );
}
