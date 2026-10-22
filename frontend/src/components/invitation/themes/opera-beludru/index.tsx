"use client";
// Theme "Opera Beludru" — malam gala di gedung opera. Sampul: tirai beludru merah yang dilukis dengan gouache (lipatan
// dalam, kilau pucat di punggung lipatan, rumbai emas) tertutup rapat di bawah valance berumbai, lampu kristal berayun
// pelan, kartu program dan tiket masuk berlubang sobek berisi nama tamu; saat tombol ditekan tirai tersibak ke kedua sisi
// lalu undangan terbuka. Hero: panggung prosenium berbingkai emas dengan tirai terikat. Hitung mundur dalam medali emas
// di depan deretan balkon loge, acara sebagai halaman program per babak, galeri berbingkai sepuh di atas beludru, penutup
// dengan tirai yang turun kembali. Untuk pasangan umum (netral).
import { useState } from "react";
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Rozha One", "Spectral:ital,wght@0,400;0,600;1,400", "Marcellus SC", "Monsieur La Doulaise"];
// Painted by /tmp/pen/art/themes/opera-beludru.py (tools/art/themes in the repo).
const Art = makeArt("opera-beludru", {
  valance: [400, 118], chandelier: [280, 291], tassel: [60, 273], orn: [220, 30],
} as const);

const COPY = {
  ...DEFAULT_COPY,
  opening: {
    kicker: "Ouverture",
    title: "Malam Gala Kami",
    sub: "Sebuah pertunjukan dalam dua babak",
    intro: "Dengan penuh sukacita dan memohon restu Tuhan Yang Maha Esa, kami mengundang Bapak/Ibu/Saudara/i untuk duduk di kursi kehormatan dan menyaksikan babak terindah dalam hidup kami: hari pernikahan kami.",
  },
  roles: ["Sopran · Mempelai Wanita", "Cello · Mempelai Pria"] as [string, string],
  couple: ["Para Pemeran", "Kedua Mempelai"] as [string, string],
  count: ["Menuju tirai dibuka", "Hitung Mundur"] as [string, string],
  units: ["Hari", "Jam", "Menit", "Detik"] as [string, string, string, string],
  events: ["Susunan Pertunjukan", "Waktu & Tempat"] as [string, string],
  story: ["Sinopsis", "Kisah Kami"] as [string, string],
  gallery: ["Dari balik panggung", "Galeri"] as [string, string],
  wishes: ["Tepuk tangan untuk mempelai", "Ucapan & Kehadiran"] as [string, string],
  gifts: ["Tanda kasih", "Amplop Digital"] as [string, string],
  closing: {
    thanks: "Terima Kasih",
    text: "Kehadiran dan doa Bapak/Ibu/Saudara/i adalah tepuk tangan paling meriah untuk kami.",
    salam: "Sampai jumpa saat tirai dibuka",
  },
  attend: { maybe: "Mungkin" } as Partial<Record<Attendance, string>>,
  sent: "Bravo! Terima kasih, ucapan Anda sudah kami terima.",
  wishPlaceholder: "Tuliskan ucapan dan doa untuk kedua mempelai…",
  closedNote: "Terima kasih atas doa dan perhatiannya. Ucapan masih bisa dikirim lewat form ini.",
  giftIntro: "Kehadiran Anda adalah hadiah terindah. Bila berkenan memberi tanda kasih, dapat melalui:",
  familyLabel: "Dengan hormat, kami sekeluarga",
};

const WISHES = [
  { id: "w1", name: "Bapak Antonius Gunawan", attendance: "yes" as Attendance, message: "Bravo, Amara dan Kenzo! Semoga duet kalian selalu selaras, dari babak pertama sampai encore terakhir." },
  { id: "w2", name: "Orkes Kamar Sasmita", attendance: "yes" as Attendance, message: "Kami siap mengiringi malam gala kalian. Selamat menempuh hidup baru, bahagia selalu!" },
  { id: "w3", name: "Clarissa & Daniel", attendance: "maybe" as Attendance, message: "Semoga bisa terbang dari Singapura tepat waktu. Doa terbaik untuk kalian berdua." },
];

function Cover({ open, data }: { open: () => void; data: ThemeProps["data"] }) {
  const [parting, setParting] = useState(false);
  const label = data.eventLabel ?? "Pernikahan";
  const groom = data.couple.groom?.trim();
  const table = tableLabel(data.guestTable);
  const raise = () => {
    if (parting) return;
    const reduce = typeof window !== "undefined" && window.matchMedia?.("(prefers-reduced-motion: reduce)").matches;
    if (reduce) { open(); return; }
    setParting(true);
    window.setTimeout(open, 1150);
  };
  return (
    <section className={parting ? `${s.cover} ${s.parting}` : s.cover}>
      <span className={s.footlight} aria-hidden />
      <span className={`${s.curtain} ${s.curtainL}`} aria-hidden />
      <span className={`${s.curtain} ${s.curtainR}`} aria-hidden />
      <Art name="valance" eager className={s.valance} />
      <span className={s.chandelier} aria-hidden><Art name="chandelier" eager /></span>
      <div className={s.programme}>
        <p className={s.progKicker}>Undangan {label}</p>
        <h1 className={s.coverNames}>
          <span>{data.couple.bride}</span>
          {groom && <><em>&amp;</em><span>{groom}</span></>}
        </h1>
        <Art name="orn" eager className={s.progRule} />
        <p className={s.coverDate}>{formatDate(data.date)}</p>
      </div>
      <div className={s.ticket}>
        <div className={s.guest}>
          <small>Tiket Undangan · Kepada Yth.</small>
          <strong>{guestLabel(data)}</strong>
        </div>
        <div className={s.stub}>{table ? <>Kursi<b>{table}</b></> : <>Masuk<b>I</b></>}</div>
      </div>
      <button type="button" className={s.openBtn} onClick={raise}><Lucide icon={ic.mailOpen} size={16} color="#f0d590" />Buka Tirai</button>
    </section>
  );
}

export default function OperaBeludruTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const photo = data.gallery[0] ?? data.couple.bridePhoto;
  const note = data.couple.note?.trim();
  const groom = data.couple.groom?.trim();
  const names = [data.couple.bride, groom].filter(Boolean).join(" & ");

  return (
    <ThemeShell
      fonts={FONTS}
      background="#14060a"
      skipCover={skipCover}
      className={s.root}
      cover={open => <Cover open={open} data={data} />}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#f0d590"
        dark="#2a1013"
        copy={COPY}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            <Art name="valance" className={s.heroValance} />
            <span className={`${s.heroDrape} ${s.heroDrapeL}`} aria-hidden />
            <span className={`${s.heroDrape} ${s.heroDrapeR}`} aria-hidden />
            <div className={s.stage}>
              <Photo src={photo} alt={names} />
            </div>
            <p className={s.heroKicker}>{label}</p>
            <h1 className={s.heroNames}>{data.couple.bride}{groom && <><em>&amp;</em>{groom}</>}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="orn" className={s.divider} />,
          node: <Art name="tassel" />,
          amp: <Art name="tassel" />,
          closingDecor: <><span className={`${s.closeDrape} ${s.closeDrapeL}`} aria-hidden /><span className={`${s.closeDrape} ${s.closeDrapeR}`} aria-hidden /><Art name="valance" className={s.closeValance} /></>,
          closingEmblem: <Art name="chandelier" className={s.closingEmblem} />,
          sentArt: <Art name="chandelier" />,
        }}
      />
    </ThemeShell>
  );
}
