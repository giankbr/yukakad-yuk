"use client";
// Theme "Hujan Kota" — malam kota yang hujan, dilukis dengan gouache dan sapuan cat air: deret ruko berjendela kuning,
// papan nama menyala tanpa tulisan (bukan merek), lampu jalan, sepasang payung dilihat dari belakang, dan jalan basah
// yang memantulkan semua cahaya. Sampul berlapis: lukisan jalan, gerimis yang turun, titik air di kaca (diam saat gerak
// dikurangi). Hero berupa jendela berbingkai dengan foto di balik kaca basah. Lukisan: /tmp/pen/art/themes/hujan-kota.py.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Instrument Serif:ital@0;1", "Hanken Grotesk:wght@400;500;600;700", "Homemade Apple"];
const Art = makeArt("hujan-kota", { pair: [411, 428], roofs: [780, 329], ripple: [330, 44], node: [96, 96] } as const);

const COPY = {
  ...DEFAULT_COPY,
  opening: {
    kicker: "Dengan penuh sukacita",
    title: "Di Bawah Payung yang Sama",
    intro: "Kami mengundang Bapak/Ibu/Saudara/i untuk merayakan hari pernikahan kami. Hujan boleh turun, lampu kota boleh redup; kehadiran dan doa Anda yang akan membuat malam itu terasa hangat.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"] as [string, string],
  couple: ["Dua orang, satu payung", "Kami Berdua"] as [string, string],
  count: ["Sampai hujan berikutnya", "Menuju Hari Bahagia"] as [string, string],
  units: ["Hari", "Jam", "Menit", "Detik"] as [string, string, string, string],
  events: ["Simpan alamatnya", "Waktu & Tempat"] as [string, string],
  story: ["Catatan musim hujan", "Kisah Kami"] as [string, string],
  gallery: ["Dari balik jendela", "Galeri"] as [string, string],
  wishes: ["Titip pesan", "Ucapan & Kehadiran"] as [string, string],
  gifts: ["Tanda kasih", "Amplop Digital"] as [string, string],
  closing: { thanks: "Terima kasih", text: "Atas doa, ucapan, dan kehadiran Anda. Sampai bertemu di bawah lampu-lampu kota, hujan atau tidak." },
  sent: "Terima kasih, pesan Anda sudah sampai sebelum hujan reda.",
  attend: { maybe: "Mungkin" },
  wishPlaceholder: "Tuliskan ucapan dan doa untuk kami berdua…",
  giftIntro: "Kehadiran Anda sudah lebih dari cukup. Bila ingin mengirim tanda kasih, dapat melalui:",
};

export default function HujanKotaTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const photo = data.gallery[0] ?? data.couple.bridePhoto ?? data.couple.groomPhoto;

  return (
    <ThemeShell
      fonts={FONTS}
      background="#10161f"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <span className={s.coverScene} aria-hidden />
          <span className={s.coverRain} aria-hidden />
          <span className={s.coverGlass} aria-hidden />
          <div className={s.coverTop}>
            <p className={s.coverKicker}>Undangan {label}</p>
            <h1 className={s.coverNames}><span>{data.couple.bride}</span><em>dan</em><span>{data.couple.groom}</span></h1>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
          </div>
          <div className={s.coverFoot}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#241a10" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#ffdcaa"
        dark="#241a10"
        copy={COPY}
        hero={(
          <header className={s.hero}>
            <div className={s.heroWindow}>
              {photo ? <Photo src={photo} alt={`${data.couple.bride} dan ${data.couple.groom}`} /> : <span className={s.heroPair}><Art name="pair" /></span>}
              <span className={s.heroDrops} aria-hidden />
            </div>
            <p className={s.heroKicker}>{label}</p>
            <h1 className={s.heroNames}>{data.couple.bride}<em>dan</em>{data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
            <Art name="roofs" className={s.heroRoofs} />
          </header>
        )}
        slots={{
          divider: <Art name="ripple" className={s.divider} />,
          node: <Art name="node" />,
          amp: <Art name="ripple" />,
          countDecor: <><span className={s.countRain} aria-hidden /><Art name="roofs" className={s.countRoofs} /></>,
          closingDecor: <><span className={s.closeRain} aria-hidden /><Art name="roofs" className={s.closeRoofs} /></>,
          closingEmblem: <Art name="pair" className={s.closePair} />,
          sentArt: <Art name="pair" />,
        }}
      />
    </ThemeShell>
  );
}
