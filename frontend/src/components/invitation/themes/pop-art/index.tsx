"use client";
// Theme "Pop Art" — halaman komik pop art orisinal. Sampul berupa tiga panel bertinta tebal: foto pasangan dicetak
// halftone dua warna dengan balon kata "Kami menikah!", ledakan bintang berisi tanggal, panel nama, dan panel tamu.
// Hero seperti sampul majalah komik edisi spesial. Panel tokoh untuk mempelai, kotak keterangan "Sementara itu…"
// untuk acara, kisah sebagai strip komik, ucapan sebagai balon kata, ledakan "Sampai jumpa!" di penutup.
import { Lucide, Photo, ThemeShell, dateParts, formatDate, guestLabel, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Bangers", "Comic Neue:ital,wght@0,400;0,700;1,700"];
// Painted by /tmp/pen/art/themes/pop-art.py (tools/art/themes in the repo).
const Art = makeArt("pop-art", {
  bubble: [210, 160], thought: [320, 263], burst: [190, 171], heart: [100, 90], rings: [160, 122],
} as const);

const COPY = {
  ...DEFAULT_COPY,
  opening: {
    kicker: "Halo, para pembaca setia!",
    title: "Kabar Gembira!",
    sub: "Edisi spesial yang sudah lama ditunggu",
    intro: "Setelah sekian episode penuh tawa, salah paham kecil, dan petualangan bersama, kisah kami sampai di babak terbaik. Kami mengundang Bapak/Ibu/Saudara/i untuk hadir, ikut merayakan, dan menjadi bagian dari halaman ini.",
  },
  roles: ["Tokoh Utama", "Tokoh Utama "] as [string, string],
  couple: ["Perkenalkan", "Para Pemeran"] as [string, string],
  count: ["Episode berikutnya dalam", "Hitung Mundur!"] as [string, string],
  units: ["Hari", "Jam", "Menit", "Detik"] as [string, string, string, string],
  events: ["Catat tanggalnya!", "Jadwal Acara"] as [string, string],
  story: ["Episode sebelumnya", "Kisah Kami"] as [string, string],
  gallery: ["Panel favorit", "Galeri"] as [string, string],
  wishes: ["Tulis di balon kata", "Ucapan & Konfirmasi"] as [string, string],
  gifts: ["Kalau berkenan", "Tanda Kasih"] as [string, string],
  closing: {
    thanks: "Terima Kasih!",
    text: "Kehadiran dan doa Bapak/Ibu/Saudara/i adalah panel terindah dalam kisah kami. Sampai bertemu di hari bahagia!",
  },
  attend: { yes: "Hadir!", maybe: "Mungkin", no: "Absen" } as Partial<Record<Attendance, string>>,
  sent: "Mantap! Ucapanmu sudah masuk ke halaman kami.",
  wishPlaceholder: "Tulis ucapan dan doa untuk Laras & Gilang…",
  giftIntro: "Kehadiranmu sudah jadi hadiah terbaik. Kalau ingin memberi tanda kasih, bisa lewat:",
};

const WISHES = [
  { id: "w1", name: "Nadia & Partner", attendance: "yes" as Attendance, message: "Akhirnya! Dari rebutan komik sampai rebutan hati. Kami datang dengan kostum polkadot!" },
  { id: "w2", name: "Tim Zine Jumat Sore", attendance: "yes" as Attendance, message: "Selamat untuk duo kreator favorit kami. Semoga setiap edisi berikutnya makin seru dan penuh tawa." },
  { id: "w3", name: "Om Bram sekeluarga", attendance: "maybe" as Attendance, message: "Selamat menempuh hidup baru. Semoga rukun, sehat, dan bahagia selalu." },
];

export default function PopArtTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const photo = data.gallery[0] ?? data.couple.bridePhoto;
  const d = dateParts(data.date);

  return (
    <ThemeShell
      fonts={FONTS}
      background="#1d5fc4"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={`${s.pane} ${s.paneA}`}>
            <span className={s.caption}>Undangan {label}</span>
            {/* eslint-disable-next-line @next/next/no-img-element -- couple photo printed as halftone */}
            {photo && <img className={s.photo} src={photo} alt="" aria-hidden data-nolightbox loading="eager" />}
            <span className={s.coverBubble} aria-hidden><Art name="bubble" eager /><p>Kami menikah!</p></span>
          </div>
          <div className={`${s.pane} ${s.paneB}`}>
            <Art name="burst" eager className={s.burstImg} />
            {d.day ? <p>{d.weekday}<b>{d.day} {d.monthShort}</b>{d.year}</p> : <p>{formatDate(data.date)}</p>}
          </div>
          <div className={`${s.pane} ${s.paneC}`}>
            <h1 className={s.coverNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
          </div>
          <div className={`${s.pane} ${s.paneD}`}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={18} color="currentColor" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#fffdf6"
        dark="#15121a"
        copy={COPY}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            <div className={s.mast}><span>Edisi Spesial</span><b>{d.year || "No. 1"}</b></div>
            <h1 className={s.heroTitle}>{data.couple.bride}<span>&amp;</span>{data.couple.groom}</h1>
            <Art name="rings" className={s.heroRings} />
            {photo && (
              <div className={`${s.heroPanel} ${s.halftone}`}>
                <Photo src={photo} alt={`${data.couple.bride} & ${data.couple.groom}`} />
                <span className={s.heroBubble} aria-hidden><Art name="bubble" /><p>Kami menikah!</p></span>
              </div>
            )}
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <div className={s.heroThought}><Art name="thought" /><p>{note}</p></div>}
          </header>
        )}
        slots={{
          divider: <Art name="heart" className={s.divider} />,
          node: <Art name="burst" />,
          amp: <Art name="heart" />,
          portrait: <span className={s.badge} aria-hidden><Art name="heart" /></span>,
          closingEmblem: <div className={s.closeBurst} aria-hidden><Art name="burst" /><p>Sampai jumpa!</p></div>,
          sentArt: <Art name="burst" />,
        }}
      />
    </ThemeShell>
  );
}
