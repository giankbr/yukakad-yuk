"use client";
// Theme "Ultah Pahlawan" — ulang tahun anak bertema pahlawan super ciptaan sendiri (bukan tokoh mana pun). Sampul langit
// biru bertitik halftone dengan sinar aksi yang berputar pelan, ledakan komik yang berdenyut, anak pahlawan bergouache
// (topeng domino, jubah oranye, sepatu bot kuning) yang melayang di atas siluet kota, inisial anak tercetak di perisai
// dadanya, kotak narasi kuning, balon kata untuk nama tamu, dan lencana usia. Isi halaman berupa panel komik bergaris
// navy berbayang tebal: "Misi" untuk acara, kisah asal-usul, balon ucapan, kartu kado biru, kota malam di penutup.
import type { CSSProperties } from "react";
import { Lucide, ThemeShell, formatDate, guestLabel, toDate, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Bowlby One", "Baloo 2:wght@400;600;700;800"];
// Painted by /tmp/pen/art/themes/ultah-pahlawan.py (tools/art/themes in the repo).
const Art = makeArt("ultah-pahlawan", { hero: [420, 625], city: [780, 241], burst: [220, 235], emblem: [180, 159] } as const);

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    kicker: "Halo, pahlawan cilik!",
    title: "Panggilan Darurat: Ada Pesta!",
    intro: "Kota sedang aman, tapi ada satu misi penting: merayakan ulang tahun sahabat kita. Ayo pakai jubah terbaikmu dan bergabung untuk bermain, tiup lilin, dan bersenang-senang bersama!",
  },
  roles: ["Pahlawan hari ini", "Bersama"],
  couple: ["Kenalan dulu", "Sang Pahlawan"],
  count: ["Hitung mundur misi", "Menuju Hari Pesta"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Lokasi markas", "Detail Misi"],
  story: ["Asal-usul", "Kisah Sang Pahlawan"],
  gallery: ["Dokumentasi", "Galeri"],
  wishes: ["Kirim sinyal", "Ucapan & Kehadiran"],
  gifts: ["Kado untuk pahlawan", "Kirim Kado"],
  closing: {
    thanks: "Terima Kasih, Pahlawan!",
    text: "Terima kasih sudah menjadi bagian dari hari istimewa ini. Sampai jumpa di markas, dan jangan lupa bawa semangat terbaikmu!",
  },
  attend: { yes: "Siap Hadir", maybe: "Mungkin", no: "Absen Dulu" } as Partial<Record<Attendance, string>>,
  sent: "Sinyal diterima! Terima kasih atas ucapan dan doanya.",
  wishPlaceholder: "Tulis ucapan dan doa untuk sang pahlawan…",
  closedNote: "Terima kasih sudah datang! Ucapan masih bisa dikirim lewat form ini.",
  giftIntro: "Kehadiranmu sudah jadi kado terbaik. Kalau ingin mengirim kado, bisa melalui:",
  familyLabel: "Salam hangat dari keluarga",
};

const WISHES = [
  { id: "w1", name: "Kak Naila & Bunda", attendance: "yes" as Attendance, message: "Selamat ulang tahun, Arka! Semoga sehat, makin pemberani, dan selalu suka menolong. Naila datang pakai jubah ungu!" },
  { id: "w2", name: "Om Dimas", attendance: "yes" as Attendance, message: "Pahlawan kesayangan Om sudah enam tahun! Semoga jadi anak yang saleh dan baik hati. Siap jadi penjahat pura-pura di lomba nanti." },
  { id: "w3", name: "Teman TK Pelangi", attendance: "maybe" as Attendance, message: "Selamat ulang tahun Arka! Semoga kuenya enak dan hadiahnya banyak." },
];

function ageOn(birth?: string, on?: string) {
  const b = toDate(birth), d = toDate(on);
  if (!b || !d) return undefined;
  let age = d.getFullYear() - b.getFullYear();
  if (d.getMonth() < b.getMonth() || (d.getMonth() === b.getMonth() && d.getDate() < b.getDate())) age -= 1;
  return age > 0 && age < 30 ? age : undefined;
}

function Kid({ initial, eager, className, size }: { initial: string; eager?: boolean; className?: string; size: number }) {
  return (
    <div className={className} style={{ "--kid": `${size}px` } as CSSProperties}>
      <Art name="hero" eager={eager} />
      {initial && <span className={s.initial} aria-hidden>{initial}</span>}
    </div>
  );
}

export default function UltahPahlawanTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const child = data.extras?.child?.enabled !== false && data.extras?.child?.name?.trim() ? data.extras.child : undefined;
  const name = child ? (child.nickname?.trim() || child.name.trim()) : (data.couple.bride?.trim() || "Sang Pahlawan");
  const initial = name.slice(0, 1).toUpperCase();
  const age = ageOn(child?.birthDate, data.date);
  const label = data.eventLabel ?? "Ulang Tahun";
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#9fd8f0"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <span className={s.rays} aria-hidden />
          <p className={s.caption}>Undangan {label}</p>
          <h1 className={s.coverName}>{name}</h1>
          <p className={s.coverSub}>
            {age ? <>ulang tahun ke-<span className={s.ageBurst} aria-label={`${age} tahun`}><Art name="burst" eager /><b>{age}</b></span></> : label}
          </p>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.stage}>
            <div className={s.bubble}>
              <div className={s.guest}>
                <small>Untuk pahlawan:</small>
                <strong>{guestLabel(data)}</strong>
                {table && <span className={s.table}>{table}</span>}
              </div>
            </div>
            <span className={s.wush} aria-hidden>WUSH!</span>
            <Art name="burst" eager className={s.heroBurst} />
            <Kid initial={initial} eager className={s.heroKid} size={196} />
            <Art name="city" eager className={s.stageCity} />
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={17} color="#ffffff" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        celebrant
        noPhotos
        light="#ffffff"
        dark="#16213e"
        copy={COPY}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            <span className={s.rays} aria-hidden />
            <p className={s.heroCaption}>{age ? `Misi: ulang tahun ke-${age}` : `Misi: ${label}`}</p>
            <h1 className={s.heroName}>{name}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
            <div className={s.heroStage}>
              <Art name="burst" className={s.heroBurst} />
              <Kid initial={initial} className={s.heroKid} size={150} />
              <Art name="city" className={s.stageCity} />
            </div>
          </header>
        )}
        slots={{
          divider: <Art name="burst" className={s.divider} />,
          node: <Art name="emblem" />,
          portrait: <span className={s.portraitShield} aria-hidden><Art name="emblem" /></span>,
          countDecor: <Art name="city" className={s.countCity} />,
          closingDecor: <Art name="city" className={s.closeCity} />,
          closingEmblem: <Kid initial={initial} className={s.closingEmblem} size={130} />,
          sentArt: <Art name="burst" />,
        }}
      />
    </ThemeShell>
  );
}
