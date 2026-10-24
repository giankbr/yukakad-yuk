"use client";
// Theme "Ayunan Pohon" — buku cerita gouache saat golden hour. Sampulnya satu halaman lukisan penuh: pohon tua
// raksasa di bukit, ayunan tali yang berayun pelan dari dahan panjangnya, padang rumput berbunga liar, matahari
// rendah di balik bukit jauh, dan kunang-kunang yang mulai menyala. Nama di langit senja, kartu tamu di atas rumput.
// Hitung mundur saat senja turun, penutup kembali ke bukit lalu malam. Semua dilukis ulang.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["DM Serif Display", "Literata:ital,wght@0,400;0,600;0,700;1,400", "Patrick Hand"];
// Painted by /tmp/pen/art/themes/ayunan-pohon.py (the swing is separate so it can sway).
const Art = makeArt("ayunan-pohon", { bukit: [780, 1400], ayunan: [200, 340], ranting: [400, 54], bunga: [126, 184] } as const);

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    kicker: "Pada suatu senja…",
    title: "Kisah Kami Berlanjut",
    sub: "di bawah pohon yang sama",
    intro: "Dengan penuh syukur dan sukacita, kami mengundang Bapak/Ibu/Saudara/i untuk hadir dan menjadi bagian dari halaman baru kisah kami: hari ketika kami saling berjanji untuk berjalan, dan berayun, bersama.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"],
  couple: ["Tokoh Utama", "Kedua Mempelai"],
  count: ["Sebelum matahari terbenam", "Menuju Hari Bahagia"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Halaman Berikutnya", "Waktu & Tempat"],
  story: ["Bab demi Bab", "Kisah Kami"],
  gallery: ["Ilustrasi Nyata", "Galeri"],
  wishes: ["Tulis di Buku Kami", "Ucapan & Kehadiran"],
  gifts: ["Tanda Kasih", "Kado Digital"],
  closing: { thanks: "Terima Kasih", text: "Kehadiran dan doa Bapak/Ibu/Saudara/i akan jadi bagian paling hangat dari kisah ini. Sampai jumpa di bawah pohon." },
  sent: "Terima kasih, ucapanmu sudah kami simpan di buku cerita kami.",
  attend: { maybe: "Mungkin" },
  wishPlaceholder: "Tuliskan ucapan dan doa untuk kedua mempelai…",
  wishLabel: "Ucapan",
  giftIntro: "Kehadiranmu adalah hadiah terindah. Jika ingin memberi tanda kasih, dapat melalui:",
};

const WISHES = [
  { id: "w1", name: "Mas Raka & Mbak Tia", attendance: "yes" as Attendance, message: "Akhirnya! Dari rebutan ayunan sampai berayun berdua. Selamat ya, semoga bahagia selamanya." },
  { id: "w2", name: "Tante Wulan, Cimahi", attendance: "yes" as Attendance, message: "Selamat menempuh hidup baru, Kirana dan Gilang. Semoga rumah tangganya teduh seperti pohon tua itu." },
  { id: "w3", name: "Teman SMA Gilang", attendance: "maybe" as Attendance, message: "Kalau jadwal kerja aman kami datang. Doa terbaik buat kalian berdua, semoga langgeng." },
];

export default function AyunanPohonTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const groom = data.couple.groom?.trim();
  const photo = data.gallery[0] ?? data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#2f3358"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.scene} aria-hidden>
            <Art name="bukit" eager className={s.sceneImg} />
            <div className={s.swing}><Art name="ayunan" eager /></div>
            <div className={s.coverFlies}><i /><i /><i /><i /></div>
          </div>
          <p className={s.kicker}>Undangan {label}</p>
          <h1 className={s.coverNames}><span>{data.couple.bride}</span>{groom && <><em>&amp;</em><span>{groom}</span></>}</h1>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.card}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={17} color="#fffaf0" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        demoWishes={WISHES}
        light="#fbefd8"
        dark="#4e6a35"
        copy={COPY}
        hero={(
          <header className={s.hero}>
            <p className={s.heroKicker}>Sebuah kisah tentang</p>
            <h1 className={s.heroNames}><span>{data.couple.bride}</span>{groom && <><em>&amp;</em><span>{groom}</span></>}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {photo && (
              <div className={s.heroWindow}>
                <Photo src={photo} alt={[data.couple.bride, groom].filter(Boolean).join(" dan ")} className={s.heroPic} />
                <div className={s.heroPosy} aria-hidden><Art name="bunga" /></div>
              </div>
            )}
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="ranting" className={s.divider} />,
          node: <Art name="bunga" />,
          amp: <Art name="bunga" />,
          portrait: <Art name="bunga" className={s.portraitArt} />,
          countDecor: <div className={s.fireflies} aria-hidden><i /><i /><i /><i /><i /><i /></div>,
          closingDecor: <Art name="bukit" className={s.closingScene} />,
          closingEmblem: <Art name="bunga" className={s.closingEmblem} />,
          sentArt: <Art name="bunga" />,
        }}
      />
    </ThemeShell>
  );
}
