"use client";
// Theme "Geode Biru" — mewah dan dingin: irisan geode agate biru berpita konsentris dengan rongga kristal berkilau dan
// tepian daun emas, berputar sangat pelan di sudut sampul biru malam. Halaman marmer putih, bingkai foto dan kartu
// bersudut faset seperti batu yang dipotong, garis emas setipis rambut, Bodoni Moda miring.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Bodoni Moda:ital,opsz,wght@0,6..96,400..600;1,6..96,400..600", "Jost:wght@400;500;600"];
// Painted by /tmp/pen/art/themes/geode-biru.py (tools/art/themes in the repo).
const Art = makeArt("geode-biru", { geode: [651, 587], slice: [180, 148], leaf: [340, 25] } as const);

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    kicker: "Dengan penuh sukacita",
    title: "Terbentuk lapis demi lapis, berkilau di dalamnya",
    intro: "Kami mengundang Bapak/Ibu/Saudara/i untuk hadir dan merayakan hari pernikahan kami. Kehadiran serta doa baik Anda adalah kehormatan yang akan kami kenang selamanya.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"],
  couple: ["Sepasang Permata", "Kedua Mempelai"],
  count: ["Hitung Mundur", "Menuju Hari Bahagia"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Waktu & Tempat", "Rangkaian Acara"],
  story: ["Lapis demi Lapis", "Kisah Kami"],
  gallery: ["Galeri", "Momen Berharga"],
  wishes: ["Ucapan & Kehadiran", "Kirim Ucapan"],
  gifts: ["Tanda Kasih", "Hadiah Pernikahan"],
  closing: {
    thanks: "Terima Kasih",
    text: "Merupakan kehormatan dan kebahagiaan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
  },
  sent: "Terima kasih, ucapan Anda sudah kami terima dengan bahagia.",
  attend: { maybe: "Mungkin" },
  wishPlaceholder: "Tuliskan ucapan dan doa untuk kedua mempelai…",
  giftIntro: "Doa dan kehadiran Anda adalah hadiah yang paling berharga. Bila ingin memberi tanda kasih, dapat melalui:",
};

const WISHES = [
  { id: "w1", name: "Keluarga Om Hartanto", attendance: "yes" as Attendance, message: "Selamat Valerie dan Nathaniel. Semoga pernikahan kalian kokoh seperti batu dan indah seperti kristal di dalamnya." },
  { id: "w2", name: "Jessica Tanoto", attendance: "yes" as Attendance, message: "Akhirnya! Dari pameran batu sampai pelaminan. Ikut bahagia, sampai jumpa di ballroom." },
  { id: "w3", name: "Tim Arsitek Studio Lapis", attendance: "maybe" as Attendance, message: "Mohon maaf bila belum bisa hadir. Selamat menempuh hidup baru, bahagia selalu." },
];

export default function GeodeBiruTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const { bride, groom } = data.couple;
  const hero = data.gallery[0] ?? data.couple.bridePhoto;

  return (
    <ThemeShell
      fonts={FONTS}
      background="#0d1a33"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Art name="geode" eager className={s.coverGeode} />
          <Art name="leaf" eager className={s.coverLeaf} />
          <div className={s.coverText}>
            <p className={s.kicker}>The Wedding of</p>
            <h1 className={s.coverNames}><span>{bride}</span>{groom && <><em>&amp;</em><span>{groom}</span></>}</h1>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
          </div>
          <div className={s.coverFoot}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={18} color="#0d1a33" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#ecd79f"
        dark="#0d1a33"
        copy={COPY}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            <div className={s.heroFrame}>
              {hero ? <div className={s.heroPhoto}><Photo src={hero} alt="" /></div> : <div className={s.heroPhoto} aria-hidden />}
              <Art name="slice" className={s.heroSlice} />
            </div>
            <p className={s.heroKicker}>{label}</p>
            <h1 className={s.heroNames}>{bride}{groom && <> <em>&amp;</em> {groom}</>}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="leaf" className={s.divider} />,
          node: <Art name="slice" />,
          amp: <Art name="slice" />,
          portrait: <Art name="slice" className={s.pSlice} />,
          countDecor: <Art name="leaf" className={s.countLeaf} />,
          closingEmblem: <Art name="geode" className={s.clGeode} />,
          sentArt: <Art name="slice" />,
        }}
      />
    </ThemeShell>
  );
}
