"use client";
// Theme "Batik Semarangan" — batik pesisir Semarang. Sampulnya selembar kain batik tulis bersoga merah di atas nila:
// pohon asem arang berpolong, burung kuntul yang hinggap dan terbang, cecek pitu, dan ombak di kaki kain; nama
// mempelai "dicelup" di bawahnya dan gigi tumpal mengunci tepi. Mempelai di atas kain nila dengan potret bundar,
// hitung mundur di pita merah soga, kartu acara bertali nila. Semua motif dilukis ulang sebagai batik (malam,
// remukan, titik canting) oleh /tmp/pen/art/themes/batik-semarangan.py.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Kurale", "Literata:ital,wght@0,400;0,600;0,700;1,400", "Josefin Sans:wght@600;700", "Amiri"];
const Art = makeArt("batik-semarangan", { kain: [780, 880], ranting: [446, 87], kuntul: [246, 230], kembang: [84, 84] } as const);

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    arabic: "بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ",
    kicker: "Assalamu'alaikum Warahmatullahi Wabarakatuh",
    title: "Mohon Doa Restu",
    sub: "Dari kota asem, dua nama dalam satu kain",
    intro: "Dengan memohon rahmat dan ridha Allah Subhanahu wa Ta'ala, kami bermaksud menyelenggarakan pernikahan putra-putri kami. Merupakan kehormatan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"],
  couple: ["Dua Helai Benang", "Kedua Mempelai"],
  count: ["Menghitung Hari", "Menuju Hari Bahagia"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Catat Tanggalnya", "Waktu & Tempat"],
  story: ["Jejak Canting", "Kisah Kami"],
  gallery: ["Galeri", "Lembar Kenangan"],
  wishes: ["Doa & Kehadiran", "Ucapan & Konfirmasi"],
  gifts: ["Tanda Kasih", "Amplop Digital"],
  closing: {
    thanks: "Terima Kasih",
    text: "Kehadiran dan doa restu Bapak/Ibu/Saudara/i adalah warna terindah di kain hidup baru kami. Atas perhatiannya, kami ucapkan terima kasih.",
    salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh",
  },
  sent: "Terima kasih, doa dan ucapan Anda sudah kami terima.",
  wishPlaceholder: "Tuliskan doa restu untuk kedua mempelai…",
  giftIntro: "Doa restu Anda adalah hadiah terindah bagi kami. Bila berkenan memberi tanda kasih, dapat melalui:",
};

const WISHES = [
  { id: "w1", name: "Bu Lies & Pembatik Bubakan", attendance: "yes" as Attendance, message: "Barakallahu lakuma wa baraka 'alaikuma. Semoga rumah tangganya rindang seperti asem di Jalan Pemuda, adem buat siapa saja yang singgah." },
  { id: "w2", name: "Teman Kantor Tanjung Mas", attendance: "yes" as Attendance, message: "Selamat Rizal & Kinasih! Ditunggu lumpianya di resepsi. Semoga sakinah, mawaddah, warahmah." },
  { id: "w3", name: "Om Tjahjo & Tante Lina", attendance: "maybe" as Attendance, message: "Insyaallah kami menyusul dari Kudus. Doa terbaik untuk kalian berdua, semoga langgeng sampai tua." },
];

export default function BatikSemaranganTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const groom = data.couple.groom?.trim();
  const photo = data.gallery[0] ?? data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#1d2a52"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.coverKain} aria-hidden><Art name="kain" eager /></div>
          <div className={s.coverText}>
            <p className={s.kicker}>Undangan {label}</p>
            <h1 className={s.coverNames}><span>{data.couple.bride}</span>{groom && <><em>&amp;</em><span>{groom}</span></>}</h1>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={17} color="#fbf4e4" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        demoWishes={WISHES}
        light="#f1e5c8"
        dark="#1d2a52"
        copy={COPY}
        hero={(
          <header className={s.hero}>
            <p className={s.heroKicker}>Walimatul &apos;Ursy · Semarang</p>
            <h1 className={s.heroNames}>{data.couple.bride}{groom && <><em>&amp;</em>{groom}</>}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {photo && (
              <div className={s.heroFrame}>
                <Photo src={photo} alt={[data.couple.bride, groom].filter(Boolean).join(" dan ")} className={s.heroPic} />
                <span className={s.heroBird} aria-hidden><Art name="kuntul" /></span>
              </div>
            )}
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="ranting" className={s.divider} />,
          node: <Art name="kembang" />,
          amp: <Art name="kembang" />,
          portrait: <Art name="kembang" className={s.portraitArt} />,
          countDecor: <Art name="kembang" className={s.rosette} />,
          closingEmblem: <Art name="kuntul" className={s.closingEmblem} />,
          sentArt: <Art name="kuntul" />,
        }}
      />
    </ThemeShell>
  );
}
