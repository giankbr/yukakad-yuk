"use client";
// Theme "Ultah Unicorn" — ulang tahun anak bersama Lulu, unicorn pastel orisinal (gouache): surai pelangi enam warna,
// tanduk bergaris permen, mata terpejam bahagia. Pelangi lembut, awan permen kapas, bintang mentega, tepi awan bergelombang.
import { Lucide, ThemeShell, formatDate, guestLabel, toDate, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Baloo 2:wght@500;600;700;800", "Quicksand:wght@500;600;700"];
// Painted by /tmp/pen/art/themes/ultah-unicorn.py (tools/art/themes in the repo).
const Art = makeArt("ultah-unicorn", { unicorn: [420, 452], head: [200, 275], rainbow: [760, 371], cloud: [220, 137], star: [64, 61] } as const);

function ageAt(birth?: string, at?: string) {
  const b = toDate(birth);
  const d = toDate(at);
  if (!b || !d) return undefined;
  let age = d.getFullYear() - b.getFullYear();
  if (d.getMonth() < b.getMonth() || (d.getMonth() === b.getMonth() && d.getDate() < b.getDate())) age -= 1;
  return age > 0 && age < 30 ? age : undefined;
}

function Stars({ className }: { className?: string }) {
  return <span className={className ?? s.divider} aria-hidden><Art name="star" /><Art name="star" /><Art name="star" /></span>;
}

export default function UltahUnicornTheme(props: ThemeProps) {
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
      title: "Yuk, Naik Pelangi!",
      intro: `Dengan penuh sukacita, kami mengundang teman-teman dan keluarga untuk merayakan ${label.toLowerCase()} ${names}${age ? ` yang ke-${age}` : ""}. Kehadiran dan doa kalian akan membuat hari ini seindah pelangi!`,
    },
    roles: ["Yang Berulang Tahun", "Bersama"] as [string, string],
    couple: ["Kenalan, Yuk", child ? "Si Bintang Pesta" : "Yang Merayakan"] as [string, string],
    count: ["Hitung Mundur", "Menuju Hari Pesta"] as [string, string],
    units: ["Hari", "Jam", "Menit", "Detik"] as [string, string, string, string],
    events: ["Catat, Ya!", "Waktu & Tempat"] as [string, string],
    story: ["Cerita Kecil", `Perjalanan ${nick}`] as [string, string],
    gallery: ["Album", "Momen Ceria"] as [string, string],
    wishes: ["Kirim Doa", "Ucapan & Kehadiran"] as [string, string],
    gifts: ["Tanda Sayang", "Kado & Amplop Digital"] as [string, string],
    closing: { thanks: "Terima Kasih!", text: `Sampai jumpa di ujung pelangi! Kehadiran dan doa teman-teman adalah hadiah paling indah untuk ${names}.` },
    sent: "Yeay, ucapanmu sudah terkirim! Terima kasih banyak.",
  };

  return (
    <ThemeShell
      fonts={FONTS}
      background="#efe4fb"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Art name="cloud" eager className={`${s.floatCloud} ${s.cloudA}`} />
          <Art name="cloud" eager className={`${s.floatCloud} ${s.cloudB}`} />
          <Art name="star" eager className={`${s.sparkle} ${s.s1}`} />
          <Art name="star" eager className={`${s.sparkle} ${s.s2}`} />
          <Art name="star" eager className={`${s.sparkle} ${s.s3}`} />
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
            <Art name="rainbow" eager className={s.stageRainbow} />
            <Art name="unicorn" eager className={s.stageLulu} />
            <Art name="cloud" eager className={`${s.bank} ${s.bankL}`} />
            <Art name="cloud" eager className={`${s.bank} ${s.bankR}`} />
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
        dark="#4d3a74"
        copy={copy}
        hero={(
          <header className={s.hero}>
            <Art name="rainbow" className={s.heroRainbow} />
            <p className={s.heroKicker}>Hore! {label}</p>
            <h1 className={s.heroName}>{names}{age ? ` ${age} Tahun` : ""}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            <Stars />
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Stars />,
          node: <Art name="star" />,
          portrait: <Art name="head" className={s.peek} />,
          countDecor: <><Art name="cloud" className={`${s.countCloud} ${s.countCloudA}`} /><Art name="cloud" className={`${s.countCloud} ${s.countCloudB}`} /></>,
          closingEmblem: (
            <>
              <p className={s.closingName}>{names}</p>
              <div className={s.closingStage} aria-hidden>
                <Art name="rainbow" className={s.rainbowImg} />
                <Art name="unicorn" className={s.lulu} />
              </div>
            </>
          ),
          sentArt: <Art name="unicorn" />,
        }}
      />
    </ThemeShell>
  );
}
