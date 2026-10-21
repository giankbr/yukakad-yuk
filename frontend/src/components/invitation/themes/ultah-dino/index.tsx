"use client";
// Theme "Ultah Dino" — ulang tahun anak di lembah dinosaurus: Moli si leher panjang hijau dan Teri si triceratops oranye
// (gouache, tokoh orisinal), kue gunung api dengan lima lilin, pakis purba, jejak kaki sebagai garis waktu, telur berbintik.
import { Lucide, ThemeShell, formatDate, guestLabel, toDate, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Fredoka:wght@400;500;600;700", "Nunito:wght@400;600;700;800"];
// Painted by /tmp/pen/art/themes/ultah-dino.py (tools/art/themes in the repo).
const Art = makeArt("ultah-dino", {
  longneck: [429, 533], trike: [400, 289], cake: [320, 367], fern: [220, 386], foot: [72, 98], egg: [300, 389], ground: [600, 147], sun: [160, 159],
} as const);

function ageAt(birth?: string, at?: string) {
  const b = toDate(birth);
  const d = toDate(at);
  if (!b || !d) return undefined;
  let age = d.getFullYear() - b.getFullYear();
  if (d.getMonth() < b.getMonth() || (d.getMonth() === b.getMonth() && d.getDate() < b.getDate())) age -= 1;
  return age > 0 && age < 30 ? age : undefined;
}

function Trail({ className }: { className?: string }) {
  return <span className={className ?? s.divider} aria-hidden><Art name="foot" /><Art name="foot" /><Art name="foot" /></span>;
}

export default function UltahDinoTheme(props: ThemeProps) {
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
      title: "Ayo Datang ke Pestaku!",
      intro: `Dengan penuh sukacita, kami mengundang teman-teman dan keluarga untuk merayakan ${label.toLowerCase()} ${names}${age ? ` yang ke-${age}` : ""}. Kehadiran dan doa kalian akan membuat hari ini makin seru!`,
    },
    roles: ["Yang Berulang Tahun", "Bersama"] as [string, string],
    couple: ["Kenalan Dulu, Yuk", child ? "Si Dino Kecil" : "Yang Merayakan"] as [string, string],
    count: ["Hitung Mundur", "Menuju Hari Pesta"] as [string, string],
    units: ["Hari", "Jam", "Menit", "Detik"] as [string, string, string, string],
    events: ["Catat Tanggalnya", "Waktu & Tempat"] as [string, string],
    story: ["Jejak Langkah", `Cerita ${nick}`] as [string, string],
    gallery: ["Album", "Momen Seru"] as [string, string],
    wishes: ["Kirim Doa", "Ucapan & Kehadiran"] as [string, string],
    gifts: ["Tanda Sayang", "Kado & Amplop Digital"] as [string, string],
    closing: { thanks: "Terima Kasih!", text: `Sampai jumpa di lembah dinosaurus! Kehadiran dan doa teman-teman adalah hadiah paling seru untuk ${names}.` },
    sent: "Hore, ucapanmu sudah terkirim! Terima kasih banyak.",
  };

  return (
    <ThemeShell
      fonts={FONTS}
      background="#eef6d9"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Art name="sun" eager className={s.sun} />
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
            <Art name="fern" eager className={s.fernL} />
            <Art name="fern" eager className={s.fernR} />
            <Art name="ground" eager className={s.ground} />
            <Art name="longneck" eager className={s.neck} />
            <Art name="cake" eager className={s.cake} />
            <Art name="trike" eager className={s.trike} />
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        celebrant
        noPhotos={!child?.photo && !data.couple.bridePhoto}
        light="#fff4d6"
        dark="#3b2a1e"
        copy={copy}
        hero={(
          <header className={s.hero}>
            <Art name="sun" className={s.sun} />
            <p className={s.heroKicker}>Hore! {label}</p>
            <h1 className={s.heroName}>{names}{age ? ` ${age} Tahun` : ""}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            <div className={s.heroCake} aria-hidden>
              <Art name="fern" className={s.fernL} />
              <Art name="fern" className={s.fernR} />
              <Art name="cake" className={s.cake} />
            </div>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Trail />,
          node: <Art name="foot" />,
          portrait: <Art name="trike" className={s.peek} />,
          countDecor: <><Art name="fern" className={`${s.countFern} ${s.countFernL}`} /><Art name="fern" className={`${s.countFern} ${s.countFernR}`} /></>,
          closingEmblem: (
            <>
              <p className={s.closingName}>{names}</p>
              <div className={s.closingStage} aria-hidden>
                <Art name="ground" className={s.ground} />
                <Art name="longneck" className={s.neck} />
                <Art name="trike" className={s.trike} />
              </div>
            </>
          ),
          sentArt: <Art name="cake" />,
        }}
      />
    </ThemeShell>
  );
}
