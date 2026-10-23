"use client";
// Theme "Porselen Ming" — porselen biru-putih bergaya Ming, digambar orisinal: sapuan kobalt bawah-glasir (garis dan
// sapuan bergradasi dengan bintik kobalt menumpuk) di bawah glasir putih berkretak. Piring besar berbingkai ombak dan
// panel teratai yang berputar pelan di sampul, bingkai bibir piring untuk foto, vas meiping dengan peoni dan awan ruyi.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Zen Old Mincho:wght@400;700", "Noto Serif:ital,wght@0,400;0,600;1,400"];
// Painted by /tmp/pen/art/themes/porselen-ming.py (glaze tile and wave border are CSS backgrounds).
const Art = makeArt("porselen-ming", { plate: [640, 640], vase: [360, 612], ring: [480, 480], cloud: [220, 88] } as const);

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    kicker: "Dengan penuh sukacita",
    title: "Kami Mengundang Anda",
    sub: "Dua warna, satu glasir",
    intro: "Dengan penuh syukur kami mengundang Bapak/Ibu/Saudara/i untuk hadir dan berbagi kebahagiaan di hari pernikahan kami. Kehadiran dan doa restu Anda adalah hadiah yang paling berarti.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"],
  couple: ["Sepasang Cawan", "Kedua Mempelai"],
  count: ["Menuju Hari Bahagia", "Hitung Hari"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Waktu & Tempat", "Rangkaian Acara"],
  story: ["Lembar demi Lembar", "Kisah Kami"],
  gallery: ["Galeri", "Potret Kami"],
  wishes: ["Ucapan & Kehadiran", "Kirim Doa Restu"],
  gifts: ["Tanda Kasih", "Hadiah Pernikahan"],
  closing: {
    thanks: "Terima Kasih",
    text: "Merupakan kebahagiaan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu. Sampai jumpa di hari bahagia kami.",
  },
  sent: "Terima kasih, ucapan dan doa Anda sudah kami terima.",
  attend: { maybe: "Mungkin" },
  wishPlaceholder: "Tuliskan ucapan dan doa untuk kedua mempelai…",
  giftIntro: "Kehadiran Anda sudah lebih dari cukup. Bila berkenan memberi tanda kasih, dapat melalui:",
};

const WISHES = [
  { id: "w1", name: "Keluarga Bapak Steven Halim", attendance: "yes" as const, message: "Selamat menempuh hidup baru, Livia dan Adrian. Semoga rumah tangga kalian sejernih glasir dan sekuat porselen yang dibakar sempurna." },
  { id: "w2", name: "Tim Restorasi Museum", attendance: "yes" as const, message: "Dari ruang restorasi sampai pelaminan! Kami ikut bahagia, sampai jumpa di Balai Kartika." },
  { id: "w3", name: "Ci Vivian & Ko Darren", attendance: "maybe" as const, message: "Semoga bisa hadir, masih menunggu jadwal penerbangan. Bahagia selalu untuk kalian berdua." },
];

export default function PorselenMingTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const photo = data.gallery[0] ?? data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const groom = data.couple.groom?.trim();
  const initials = [data.couple.bride, groom].filter(Boolean).map(name => name!.slice(0, 1)).join("");

  return (
    <ThemeShell
      fonts={FONTS}
      background="#f3f4f0"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <p className={s.kicker}>Undangan {label}</p>
          <div className={s.plateWrap} aria-hidden><Art name="plate" eager className={s.plate} /></div>
          <h1 className={s.coverNames}><span>{data.couple.bride}</span>{groom && <><em>&amp;</em><span>{groom}</span></>}</h1>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.guest}>
            <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
            <strong>{guestLabel(data)}</strong>
            {table && <span className={s.table}>{table}</span>}
          </div>
          <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#ffffff" />Buka Undangan</button>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        demoWishes={WISHES}
        light="#ffffff"
        dark="#1b3480"
        copy={COPY}
        hero={(
          <header className={s.hero}>
            <div className={s.heroDish}>
              <div className={s.heroPhoto}>{photo ? <Photo src={photo} alt={`${data.couple.bride} dan ${groom ?? ""}`.trim()} /> : <span className={s.heroMono} aria-hidden>{initials}</span>}</div>
              <Art name="ring" className={s.heroRing} />
            </div>
            <p className={s.heroKicker}>The Wedding of</p>
            <h1 className={s.heroNames}><span>{data.couple.bride}</span>{groom && <><em>&amp;</em><span>{groom}</span></>}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="cloud" className={s.divider} />,
          node: <Art name="cloud" />,
          amp: <Art name="cloud" />,
          portrait: <Art name="ring" className={s.portraitRing} />,
          closingEmblem: <Art name="vase" className={s.closingVase} />,
          sentArt: <Art name="cloud" />,
        }}
      />
    </ThemeShell>
  );
}
