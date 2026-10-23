"use client";
// Theme "Taman Zen" — taman batu kering (karesansui) dilihat dari atas: pasir bergaris yang melingkari batu berlumut,
// ranting maple merah bertinta sumi yang bergoyang dengan daun gugur, lentera batu; foto bernada batu di ceruk
// tokonoma, potret bundar seperti batu pijakan, kartu acara dua kolom berkepala pasir. Lapang, tenang, minimalis.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import type { Attendance } from "../kit";
import s from "./styles.module.css";

const FONTS = ["Zen Old Mincho:wght@400;600;700", "Jost:wght@300;400;500"];
// Painted by /tmp/pen/art/themes/taman-zen.py (tools/art/themes in the repo).
const Art = makeArt("taman-zen", {
  maple: [480, 260], lantern: [220, 383], leaf: [96, 118], stone: [210, 165], rake: [440, 24],
} as const);

const WISHES = [
  { id: "w1", name: "Keluarga Bapak Hartono", attendance: "yes" as Attendance, message: "Selamat menempuh hidup baru. Semoga rumah kalian selalu tenang seperti taman yang dirawat dengan sabar." },
  { id: "w2", name: "Raka & Dinda", attendance: "yes" as Attendance, message: "Ikut bahagia! Sampai jumpa di Lembang, sudah siap sepatu datar sesuai pesan." },
  { id: "w3", name: "Tante Wulan", attendance: "maybe" as Attendance, message: "Mohon maaf kalau belum bisa datang. Doa terbaik untuk kalian berdua, langgeng sampai tua." },
];

const COPY = {
  ...DEFAULT_COPY,
  opening: {
    kicker: "Dengan Penuh Syukur",
    title: "Kami Akan Menikah",
    intro: "Dengan sukacita dan rasa syukur, kami mengundang Bapak/Ibu/Saudara/i untuk hadir dan berbagi kebahagiaan di hari pernikahan kami. Kehadiran dan doa Anda adalah hadiah yang paling berarti.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"] as [string, string],
  couple: ["dua jalan, satu taman", "Kedua Mempelai"] as [string, string],
  count: ["menunggu dengan tenang", "Menuju Hari Bahagia"] as [string, string],
  units: ["Hari", "Jam", "Menit", "Detik"] as [string, string, string, string],
  events: ["waktu & tempat", "Rangkaian Acara"] as [string, string],
  story: ["perjalanan", "Kisah Kami"] as [string, string],
  gallery: ["galeri", "Potongan Waktu"] as [string, string],
  wishes: ["ucapan & kehadiran", "Kabar dari Anda"] as [string, string],
  gifts: ["tanda kasih", "Amplop Digital"] as [string, string],
  closing: {
    thanks: "Terima Kasih",
    text: "Terima kasih telah menjadi bagian dari hari kami. Semoga setiap langkah pulang Anda terasa ringan dan tenang.",
  },
  sent: "Terima kasih, ucapan Anda sudah kami terima.",
  attend: { maybe: "Mungkin" },
  wishPlaceholder: "Tuliskan ucapan dan doa untuk kami…",
  closedNote: "Terima kasih atas perhatiannya. Ucapan masih bisa dikirim lewat form ini.",
  giftIntro: "Kehadiran Anda sudah lebih dari cukup. Bila ingin memberi tanda kasih, dapat melalui:",
};

export default function TamanZenTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const heroPhoto = data.gallery[0] || data.couple.bridePhoto || data.couple.groomPhoto;

  return (
    <ThemeShell
      fonts={FONTS}
      background="#e2dacb"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <span className={s.coverGarden} aria-hidden />
          <Art name="maple" eager className={s.coverMaple} />
          <Art name="leaf" eager className={`${s.fall} ${s.fall1}`} />
          <Art name="leaf" eager className={`${s.fall} ${s.fall2}`} />
          <div className={s.coverText}>
            <p className={s.kicker}>Undangan {label}</p>
            <h1 className={s.coverNames}><span>{data.couple.bride}</span><em>&amp;</em><span>{data.couple.groom}</span></h1>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={15} color="currentColor" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#efe9dc"
        dark="#2f2d2a"
        copy={COPY}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            <Art name="maple" className={s.heroMaple} />
            {heroPhoto ? (
              <div className={s.niche}>
                <Photo src={heroPhoto} alt={`${data.couple.bride} & ${data.couple.groom}`} />
                <div className={s.nicheFloor} aria-hidden />
              </div>
            ) : null}
            {heroPhoto && <Art name="lantern" className={s.heroLantern} />}
            <div className={s.heroText}>
              <p className={s.heroKicker}>{label}</p>
              <h1 className={s.heroNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
              <p className={s.heroDate}>{formatDate(data.date)}</p>
              {note && <p className={s.heroNote}>{note}</p>}
            </div>
          </header>
        )}
        slots={{
          divider: <Art name="rake" className={s.divider} />,
          node: <Art name="leaf" />,
          amp: <Art name="leaf" />,
          portrait: <Art name="stone" className={s.pebble} />,
          countDecor: <Art name="stone" className={s.countStone} />,
          closingEmblem: <Art name="lantern" className={s.closingLantern} />,
          sentArt: <Art name="leaf" />,
        }}
      />
    </ThemeShell>
  );
}
