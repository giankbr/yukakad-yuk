"use client";
// Theme "Danau Angsa" — danau tenang di pagi merah muda dalam cat air romantis: tirai daun dedalu yang berayun di atas
// sampul, nama bersambung di tengah kabut, sepasang angsa putih yang lehernya membentuk hati, ilalang dan ekor kucing di
// tepi air; foto dalam bingkai oval, hitung mundur di dalam riak, bulu angsa sebagai pembatas.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Pinyon Script", "Gilda Display", "Lora:ital,wght@0,400;0,600;1,400", "Tenor Sans"];
// Painted by /tmp/pen/art/themes/danau-angsa.py (tools/art/themes in the repo).
const Art = makeArt("danau-angsa", { danau: [720, 544], tirai: [360, 316], angsa: [300, 128], bulu: [220, 35], ilalang: [120, 227] } as const);

const WISHES = [
  { id: "w1", name: "Tante Yuliana & Om Robert", attendance: "yes" as Attendance, message: "Selamat menempuh hidup baru, Kirana dan Bima. Semoga cinta kalian tetap tenang dan dalam seperti danau itu." },
  { id: "w2", name: "Sahabat Klub Foto Bandung", attendance: "yes" as Attendance, message: "Dari satu perjalanan memotret jadi perjalanan seumur hidup. Kami siap jadi saksi di dermaga!" },
  { id: "w3", name: "Dewi & Arif", attendance: "maybe" as Attendance, message: "Semoga bisa menyusul ke Ciwidey. Kalau belum sempat, doa dan peluk hangat kami kirim dari jauh." },
];

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    kicker: "Dengan Penuh Sukacita",
    title: "Kami Mengundang Anda",
    intro: "Dengan bahagia kami mengabarkan bahwa kami akan mengikat janji dalam pernikahan. Merupakan kehormatan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu di tepi danau.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"],
  couple: ["Sepasang", "Kedua Mempelai"],
  count: ["Hari yang Dinanti", "Menuju Hari Bahagia"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Waktu & Tempat", "Rangkaian Acara"],
  story: ["Kisah Kami", "Bermula di Tepi Danau"],
  gallery: ["Galeri", "Potret Kami"],
  wishes: ["Ucapan & Kehadiran", "Kirim Ucapan"],
  gifts: ["Tanda Kasih", "Hadiah Pernikahan"],
  closing: { thanks: "Terima Kasih", text: "Kehadiran dan doa restu Bapak/Ibu/Saudara/i adalah hadiah yang paling berarti bagi kami berdua." },
  sent: "Terima kasih, ucapan Anda sudah terkirim.",
  attend: { maybe: "Mungkin" },
  wishPlaceholder: "Tuliskan ucapan dan doa untuk kedua mempelai…",
  giftIntro: "Kehadiran Anda sudah lebih dari cukup. Jika ingin memberi tanda kasih, dapat melalui:",
};

export default function DanauAngsaTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const heroPhoto = data.gallery[0] ?? data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#46566b"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Art name="tirai" eager className={s.willowL} />
          <Art name="tirai" eager className={s.willowR} />
          <div className={s.coverText}>
            <p className={s.kicker}>{label}</p>
            <h1 className={s.coverNames}>{data.couple.bride}<em>dan</em>{data.couple.groom}</h1>
            <Art name="bulu" eager className={s.feather} />
            <p className={s.coverDate}>{formatDate(data.date)}</p>
          </div>
          <div className={s.guestWrap}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#ffffff" />Buka Undangan</button>
          </div>
          <div className={s.lake} aria-hidden>
            <Art name="danau" eager />
            <span className={s.lakeMist} />
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#f9f2ef"
        dark="#4f5a78"
        copy={COPY}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            <Art name="tirai" className={s.heroWillow} />
            <Art name="tirai" className={s.heroWillowR} />
            {heroPhoto && <div className={s.heroPhoto}><Photo src={heroPhoto} alt="" /></div>}
            <p className={s.heroKicker}>{label}</p>
            <h1 className={s.heroNames}>{data.couple.bride} <em>&amp;</em> {data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="bulu" className={s.divider} />,
          node: <Art name="bulu" />,
          amp: <Art name="bulu" />,
          portrait: <Art name="ilalang" className={s.portraitArt} />,
          closingEmblem: <div className={s.closingSwans} aria-hidden><Art name="angsa" /></div>,
          sentArt: <Art name="angsa" />,
        }}
      />
    </ThemeShell>
  );
}
