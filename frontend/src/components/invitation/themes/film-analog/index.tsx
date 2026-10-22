"use client";
// Theme "Film Analog" — kenangan 35mm yang hangat. Sampul: sepotong strip film (lubang sprocket, angka tepi oranye)
// berisi tiga frame foto dengan cap tanggal oranye bercahaya, label selotip kertas bertulisan tangan, dan amplop
// cuci-cetak berisi nama tamu; kebocoran cahaya yang dilukis bergeser pelan di atas butiran film. Hero: satu cetakan
// besar berbingkai putih yang ditempel selotip, dengan potongan negatif di bawahnya. Hitung mundur di dalam frame film,
// acara sebagai amplop cetak foto, kisah di sepanjang strip negatif, galeri sebagai contact sheet dengan lingkaran pensil
// minyak merah, penutup dengan kamera rangefinder bergouache tanpa merek. Untuk pasangan umum (netral).
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Instrument Serif:ital@0;1", "Hanken Grotesk:wght@400;500;700", "Space Mono:wght@400;700", "Caveat Brush"];
// Painted by /tmp/pen/art/themes/film-analog.py (tools/art/themes in the repo).
const Art = makeArt("film-analog", {
  camera: [340, 202], canister: [180, 158], leak: [280, 380], circle: [150, 104], tape: [160, 39], snip: [210, 46],
} as const);

const COPY = {
  ...DEFAULT_COPY,
  opening: {
    kicker: "Roll 01",
    title: "Satu Frame Bahagia",
    sub: "ISO 400 · 36 eksposur · cuci cetak bersama",
    intro: "Dengan memohon rahmat dan restu Tuhan Yang Maha Esa, kami mengundang Bapak/Ibu/Saudara/i untuk hadir di hari pernikahan kami, dan ikut mengabadikan satu frame bahagia yang akan kami simpan seumur hidup.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"] as [string, string],
  couple: ["Frame 04 · 05", "Kedua Mempelai"] as [string, string],
  count: ["Sisa eksposur", "Menuju Hari H"] as [string, string],
  units: ["Hari", "Jam", "Menit", "Detik"] as [string, string, string, string],
  events: ["Pesanan Cetak", "Waktu & Tempat"] as [string, string],
  story: ["Dari Roll ke Roll", "Kisah Kami"] as [string, string],
  gallery: ["Contact Sheet", "Galeri"] as [string, string],
  wishes: ["Tulis di Balik Foto", "Ucapan & Kehadiran"] as [string, string],
  gifts: ["Tanda Kasih", "Amplop Digital"] as [string, string],
  closing: {
    thanks: "Terima kasih",
    text: "Kehadiran dan doa Bapak/Ibu/Saudara/i adalah frame terindah dalam roll kenangan kami.",
    salam: "Sampai jumpa di depan kamera",
  },
  attend: { maybe: "Mungkin" } as Partial<Record<Attendance, string>>,
  sent: "Terima kasih! Ucapan Anda sudah kami simpan bersama cetakan foto.",
  wishPlaceholder: "Tulis ucapan seperti di balik selembar foto…",
  closedNote: "Terima kasih atas doa dan perhatiannya. Ucapan masih bisa dikirim lewat form ini.",
  giftIntro: "Doa dan kehadiran Anda sudah lebih dari cukup. Bila berkenan memberi tanda kasih, dapat melalui:",
  familyLabel: "Dengan cinta, keluarga",
};

const WISHES = [
  { id: "w1", name: "Mas Yoga", attendance: "yes" as Attendance, message: "Selamat Nadia & Bagas! Kamera sudah diisi film baru, siap memotret kalian seharian." },
  { id: "w2", name: "Klub Film Kamar Gelap", attendance: "yes" as Attendance, message: "Dari double exposure jadi satu frame. Bahagia selalu, semoga hasil cetaknya selalu terang!" },
  { id: "w3", name: "Tante Wulan", attendance: "maybe" as Attendance, message: "Semoga bisa datang dari Semarang. Doa terbaik untuk kalian berdua, langgeng sampai tua." },
];

function stamp(value?: string) {
  const m = /^(\d{2})(\d{2})-(\d{2})-(\d{2})/.exec(value ?? "");
  return m ? `'${m[2]} ${m[3]} ${m[4]}` : "";
}

export default function FilmAnalogTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const shots = data.gallery.length ? data.gallery : [data.couple.bridePhoto, data.couple.groomPhoto].filter((x): x is string => !!x);
  const frames = [shots[0], shots[1] ?? shots[0], shots[2] ?? shots[0]];
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const groom = data.couple.groom?.trim();
  const names = [data.couple.bride, groom].filter(Boolean).join(" & ");
  const date = stamp(data.date);

  return (
    <ThemeShell
      fonts={FONTS}
      background="#120e0b"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Art name="leak" eager className={s.coverLeak} />
          <p className={s.coverKicker}>Roll 01 · Undangan {label}</p>
          <div className={`${s.strip} ${s.coverStrip}`} aria-hidden data-nolightbox>
            <span className={`${s.edge} ${s.edgeL}`}><i>▸ 11</i><i>11A</i><i>▸ 12</i><i>12A</i><i>▸ 13</i></span>
            <span className={`${s.edge} ${s.edgeR}`}><i>ANALOG 400</i><i>ANALOG 400</i></span>
            {frames.map((src, i) => (
              <div key={i} className={s.frame}>
                <Photo src={src} alt="" />
                {i === 1 && date && <span className={s.stamp}>{date}</span>}
              </div>
            ))}
          </div>
          <div className={`${s.label} ${s.coverLabel}`}>
            <Art name="tape" eager />
            <h1><span>{names}</span></h1>
          </div>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.envelope}>
            <div className={s.guest}>
              <small>Untuk Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
          </div>
          <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#231a14" />Buka Undangan</button>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#f1e8d6"
        dark="#231a14"
        copy={COPY}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            <Art name="leak" className={s.heroLeak} />
            <figure className={s.print}>
              <Art name="tape" className={s.tapeL} />
              <Art name="tape" className={s.tapeR} />
              <div className={s.printPhoto}>
                <Photo src={frames[0]} alt={names} />
                {date && <span className={s.stamp}>{date}</span>}
              </div>
              <figcaption className={s.printCaption}>
                <h1 className={s.heroNames}>{names}</h1>
                <p className={s.heroDate}>{label} · {formatDate(data.date)}</p>
              </figcaption>
            </figure>
            {note && <p className={s.heroNote}>{note}</p>}
            {shots.length > 1 && (
              <div className={s.heroStrip} aria-hidden data-nolightbox>
                {[shots[1], shots[2] ?? shots[0], shots[3] ?? shots[1]].map((src, i) => <span key={i}><Photo src={src} alt="" /></span>)}
              </div>
            )}
          </header>
        )}
        slots={{
          divider: <Art name="snip" className={s.divider} />,
          amp: <Art name="snip" />,
          portrait: <span className={s.portraitTape} aria-hidden><Art name="tape" /></span>,
          countDecor: <Art name="leak" className={s.countLeak} />,
          closingDecor: <Art name="leak" className={s.closeLeak} />,
          closingEmblem: <Art name="camera" className={s.closingEmblem} />,
          sentArt: <Art name="canister" />,
        }}
      />
    </ThemeShell>
  );
}
