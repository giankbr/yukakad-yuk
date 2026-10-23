"use client";
// Theme "Memphis 80an" — gaya Memphis 80-an yang jenaka dan orisinal: sampul kertas grafik bertabur konfeti dengan pita
// teks berjalan, susunan benda geometri sablon (pilar squiggle, setengah lingkaran bergaris, bola halftone, kerucut
// bertitik, balok papan catur) yang bergoyang pelan, nama besar berbayang merah muda, tombol berbayangan keras. Hero:
// foto miring dengan stiker geometri, bingkai potret melengkung atas/bawah, hitung mundur berupa balok pastel di pita
// hitam, kartu acara bertepi tebal. Lukisan dari /tmp/pen/art/themes/memphis-80an.py.
import { Lucide, Photo, ThemeShell, dateParts, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Rubik Mono One", "Space Grotesk:wght@400;500;700", "Caveat Brush"];
const Art = makeArt("memphis-80an", {
  totem: [598, 673], squig: [376, 38], zig: [392, 37], tri: [163, 159], half: [179, 96], ring: [156, 156], bolt: [199, 101],
} as const);

const COPY = {
  ...DEFAULT_COPY,
  opening: {
    kicker: "Halo, teman-teman!",
    title: "Kami Menikah!",
    sub: "dan kamu wajib datang",
    intro: "Dengan penuh syukur kepada Tuhan Yang Maha Esa, kami mengundang Bapak/Ibu/Saudara/i untuk merayakan hari pernikahan kami. Datanglah dengan senyum terbaik, warna paling berani, dan langkah dansa yang sudah disiapkan.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"] as [string, string],
  couple: ["kenalan dulu", "Duo Kami"] as [string, string],
  count: ["siap-siap", "Menuju Hari-H"] as [string, string],
  units: ["Hari", "Jam", "Menit", "Detik"] as [string, string, string, string],
  events: ["catat jadwalnya", "Acara"] as [string, string],
  story: ["dari kelas tipografi", "Cerita Kami"] as [string, string],
  gallery: ["jepret!", "Galeri"] as [string, string],
  wishes: ["kirim pesan", "Ucapan & RSVP"] as [string, string],
  gifts: ["tanda sayang", "Hadiah"] as [string, string],
  closing: {
    thanks: "Terima Kasih!",
    text: "Kehadiran dan doa Bapak/Ibu/Saudara/i adalah warna paling cerah di hari kami. Sampai jumpa di lantai dansa!",
  },
  attend: { maybe: "Mungkin" },
  sent: "Yay! Pesanmu sudah sampai. Terima kasih banyak!",
  wishPlaceholder: "Tulis ucapan dan doa untuk kami berdua…",
  giftIntro: "Kehadiranmu sudah jadi hadiah terbaik. Kalau ingin mengirim tanda sayang, bisa lewat:",
};

export default function Memphis80anTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const heroPhoto = data.gallery[0] ?? data.couple.bridePhoto;
  const parts = dateParts(data.date);
  const stamp = parts.day ? `${parts.day} ${parts.monthShort} ${parts.year}` : "Segera";
  const line = `SAVE THE DATE  ✦  ${stamp}  ✦  ${data.couple.bride} + ${data.couple.groom}  ✦  `.toUpperCase();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#fff6ea"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.ticker} aria-hidden><span>{line}{line}{line}{line}</span></div>
          <Art name="totem" eager className={s.totem} />
          <p className={s.coverKicker}>Undangan {label}</p>
          <h1 className={s.coverNames}><span>{data.couple.bride}</span><em>&amp;</em><span>{data.couple.groom}</span></h1>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.guest}>
            <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
            <strong>{guestLabel(data)}</strong>
            {table && <span className={s.table}>{table}</span>}
          </div>
          <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#151515" />Buka Undangan</button>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#151515"
        dark="#ffd54a"
        copy={COPY}
        hero={(
          <header className={s.hero}>
            <p className={s.heroKicker}>{label}</p>
            <div className={s.heroShot}>
              <div>{heroPhoto ? <Photo src={heroPhoto} alt={`${data.couple.bride} & ${data.couple.groom}`} /> : null}</div>
              <Art name="half" className={`${s.stk} ${s.stkHalf}`} />
              <Art name="tri" className={`${s.stk} ${s.stkTri}`} />
              <Art name="bolt" className={`${s.stk} ${s.stkBolt}`} />
            </div>
            <h1 className={s.heroNames}><span>{data.couple.bride}</span><em>&amp;</em><span>{data.couple.groom}</span></h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="squig" className={s.divider} />,
          node: <Art name="tri" />,
          amp: <Art name="ring" />,
          portrait: <span className={s.portStk} aria-hidden><Art name="half" /><Art name="ring" /></span>,
          closingEmblem: <Art name="totem" className={s.closeArt} />,
          sentArt: <Art name="bolt" />,
        }}
      />
    </ThemeShell>
  );
}
