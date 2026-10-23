"use client";
// Theme "Bauhaus Primer" — Modern, poster cetak saring bergaya Bauhaus: matahari merah terpotong tepi, persegi biru yang
// menumpuk (overprint), segitiga kuning, batang hitam, dan arsiran halftone di atas kertas putih tulang. Tata letak
// asimetris rata kiri, huruf geometris besar huruf kecil, grid bergaris tegas; satu mempelai dalam lingkaran, satu
// dalam persegi.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Jost:wght@400;500;600;700", "Space Mono:wght@400;700"];
// Screen-printed by /tmp/pen/art/themes/bauhaus-primer.py (paper.webp is a CSS background).
const Art = makeArt("bauhaus-primer", { poster: [780, 802], circle: [160, 161], tri: [160, 146], square: [160, 160], half: [160, 82], ring: [160, 161] } as const);

const WISHES = [
  { id: "w1", name: "Studio Garis Tegas", attendance: "yes" as const, message: "Selamat Alya & Bima! Dari meja kerja yang sama ke satu rumah. Semoga komposisinya selalu seimbang." },
  { id: "w2", name: "Tante Rosa & Om Daniel", attendance: "yes" as const, message: "Bahagia sekali melihat kalian. Semoga saling menjaga dan tumbuh bersama setiap hari." },
  { id: "w3", name: "Kevin Pratama", attendance: "maybe" as const, message: "Lagi di Bandung, kalau keburu aku datang ke resepsi. Selamat menempuh hidup baru!" },
];

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    kicker: "Salam hangat",
    title: "Kami Mengundang Anda",
    intro: "Dengan penuh sukacita, kami mengundang Bapak/Ibu/Saudara/i untuk hadir dan merayakan hari pernikahan kami. Kehadiran dan doa restu Anda adalah bagian terindah dari perayaan ini.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"],
  couple: ["01 / kami", "Dua Bentuk"],
  count: ["02 / hitung mundur", "Menuju Hari H"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["03 / acara", "Waktu & Tempat"],
  story: ["04 / cerita", "Kisah Kami"],
  gallery: ["05 / galeri", "Momen"],
  wishes: ["06 / ucapan", "Ucapan & Kehadiran"],
  gifts: ["07 / hadiah", "Tanda Kasih"],
  closing: { thanks: "Terima Kasih", text: "Kehadiran dan doa restu Bapak/Ibu/Saudara/i adalah hadiah terbaik bagi kami berdua dan keluarga." },
  sent: "Terima kasih, ucapan Anda sudah terkirim.",
  attend: { maybe: "Mungkin" },
  wishPlaceholder: "Tuliskan ucapan untuk kedua mempelai…",
};

function shortDate(iso?: string) {
  const m = /^(\d{4})-(\d{2})-(\d{2})/.exec(iso ?? "");
  return m ? `${m[3]}.${m[2]}.${m[1]}` : "segera";
}

function Divider() {
  return <span className={s.divider} aria-hidden><Art name="circle" /><Art name="square" /><Art name="tri" /></span>;
}

export default function BauhausPrimerTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const hero = data.gallery[0] ?? data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#f1ece1"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.coverBar}><span>undangan {label.toLowerCase()}</span><span>{shortDate(data.date)}</span></div>
          <Art name="poster" eager className={s.poster} />
          <div className={s.coverText}>
            <p className={s.kicker}>{label}</p>
            <h1 className={s.coverNames}><span>{data.couple.bride}</span><span><em>&amp;</em> {data.couple.groom}</span></h1>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
          </div>
          <div className={s.guestWrap}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={18} color="#f7f3ea" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        copy={COPY}
        demoWishes={WISHES}
        light="#f7f3ea"
        dark="#1b1a19"
        hero={(
          <header className={s.hero}>
            <div className={s.heroComp}>
              <Art name="square" className={s.heroSq} />
              <div className={s.heroPhoto}>{hero && <Photo src={hero} alt="" />}</div>
              <Art name="tri" className={s.heroTri} />
            </div>
            <p className={s.heroKicker}>{label}</p>
            <h1 className={s.heroNames}>{data.couple.bride} <em>&amp;</em> {data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Divider />,
          node: <Art name="square" />,
          closingDecor: <span aria-hidden><Art name="ring" className={s.closingShape} /><Art name="square" className={s.closingShape} /><Art name="tri" className={s.closingShape} /></span>,
          closingEmblem: <Art name="half" className={s.closingHalf} />,
          sentArt: <Art name="circle" />,
        }}
      />
    </ThemeShell>
  );
}
