"use client";
// Theme "Baby Shower Awan" — cat air pastel untuk calon ayah & bunda: balon udara bergaris mint-peach-lilac yang
// melayang, awan-awan empuk, bulan sabit pucat, bintang kecil, langit basah-basah di atas kertas cat air.
import { Lucide, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Fraunces:ital,wght@0,400;0,600;1,400;1,600", "Quicksand:wght@400;500;600;700"];
// Painted by /tmp/pen/art/themes/baby-shower-awan.py (tools/art/themes in the repo).
const Art = makeArt("baby-shower-awan", {
  balloon: [340, 515], cloud: [360, 148], cloud2: [280, 111], moon: [170, 180], stars: [260, 169], star: [64, 64], divider: [210, 44],
} as const);

function Clouds({ l, r }: { l: string; r: string }) {
  return <><Art name="cloud" className={l} /><Art name="cloud2" className={r} /></>;
}

export default function BabyShowerAwanTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Baby Shower";
  const groom = data.couple.groom?.trim();
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const copy = {
    ...DEFAULT_COPY,
    opening: {
      kicker: "Untuk Sahabat & Keluarga",
      title: "Menanti Si Kecil",
      intro: "Dengan hati yang penuh syukur, kami mengundang Bapak/Ibu/Saudara/i untuk berbagi kebahagiaan menyambut buah hati kami. Doa dan kehadiran Anda akan menjadi pelukan pertama yang hangat untuknya.",
    },
    roles: ["Calon Bunda", "Calon Ayah"] as [string, string],
    couple: ["Yang Menanti", groom ? "Calon Ayah & Bunda" : "Calon Bunda"] as [string, string],
    count: ["Sebentar Lagi", "Menuju Hari Bahagia"] as [string, string],
    units: ["Hari", "Jam", "Menit", "Detik"] as [string, string, string, string],
    events: ["Simpan Tanggalnya", "Waktu & Tempat"] as [string, string],
    story: ["Perjalanan Kecil", "Cerita Penantian"] as [string, string],
    gallery: ["Galeri", "Potret Penantian"] as [string, string],
    wishes: ["Doa untuk Si Kecil", "Ucapan & Kehadiran"] as [string, string],
    gifts: ["Tanda Kasih", "Kado untuk Si Kecil"] as [string, string],
    closing: { thanks: "Terima Kasih", text: "Atas doa, kasih, dan kehadiran Anda. Semoga si kecil lahir sehat, selamat, dan tumbuh dikelilingi cinta." },
    sent: "Terima kasih, doa manis Anda sudah terkirim untuk si kecil.",
  };

  return (
    <ThemeShell
      fonts={FONTS}
      background="#efe8f6"
      skipCover={skipCover}
      className={groom ? s.root : `${s.root} ${s.solo}`}
      cover={open => (
        <section className={s.cover}>
          <Art name="stars" eager className={s.stars} />
          <Art name="moon" eager className={s.moon} />
          <div className={s.balloonWrap} aria-hidden>
            <Art name="cloud2" eager className={s.cloudB} />
            <Art name="balloon" eager className={s.balloon} />
            <Art name="cloud" eager className={s.cloudA} />
          </div>
          <p className={s.kicker}>{label}</p>
          <h1 className={s.coverNames}>{data.couple.bride}{groom && <><em>&amp;</em>{groom}</>}</h1>
          <p className={s.coverSub}>menanti kehadiran buah hati</p>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.guestWrap}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#fffdfb" />Buka Undangan</button>
          </div>
          <Art name="cloud" eager className={s.cloudC} />
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        celebrant
        noPhotos={!data.couple.bridePhoto && !data.couple.groomPhoto}
        light="#fff6ef"
        dark="#4a4060"
        copy={copy}
        hero={(
          <header className={s.hero}>
            <Art name="stars" className={s.stars} />
            <Art name="balloon" className={s.balloon} />
            <p className={s.heroKicker}>{label}</p>
            <h1 className={s.heroNames}>{data.couple.bride}{groom && <><em>&amp;</em>{groom}</>}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
            <Clouds l={`${s.heroCloud} ${s.heroCloudL}`} r={`${s.heroCloud} ${s.heroCloudR}`} />
          </header>
        )}
        slots={{
          divider: <Art name="divider" className={s.divider} />,
          node: <Art name="star" />,
          amp: <Art name="divider" />,
          portrait: <Art name="cloud2" className={s.portraitCloud} />,
          countDecor: <><Art name="moon" className={s.countMoon} /><Art name="stars" className={s.countStars} /><Clouds l={`${s.countCloud} ${s.countCloudL}`} r={`${s.countCloud} ${s.countCloudR}`} /></>,
          closingDecor: <Clouds l={`${s.closingCloud} ${s.closingCloudL}`} r={`${s.closingCloud} ${s.closingCloudR}`} />,
          closingEmblem: <Art name="balloon" className={s.closingBalloon} />,
          sentArt: <Art name="balloon" />,
        }}
      />
    </ThemeShell>
  );
}
