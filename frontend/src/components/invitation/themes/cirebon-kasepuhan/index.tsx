"use client";
// Theme "Cirebon Kasepuhan" — gerbang bentar bata merah ala keraton Cirebon yang ditatah piring porselen biru-putih,
// polikrom, dan Eropa, berdiri di atas batu-batu gua taman sari dan kolam teratai (desain orisinal). Potret dibingkai
// bibir piring porselen, hitung mundur di atas ubin berglasir di dinding bata. Tanpa figur makhluk hidup.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, toDate, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Yeseva One", "Spectral:ital,wght@0,400;0,500;0,600;1,400;1,500", "Amiri:wght@400;700"];
// Painted by /tmp/pen/art/themes/cirebon-kasepuhan.py (tools/art/themes in the repo).
const Art = makeArt("cirebon-kasepuhan", {
  gate: [300, 876], wadas: [780, 322], ring: [460, 460], divider: [340, 67],
  "plate-b": [200, 200], "plate-p": [200, 200], "plate-d": [200, 200],
} as const);

const BISMILLAH = "بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ";

const COPY = {
  ...DEFAULT_COPY,
  opening: {
    arabic: BISMILLAH,
    kicker: "Assalamu'alaikum Warahmatullahi Wabarakatuh",
    title: "Walimatul 'Ursy",
    intro: "Dengan memohon rahmat dan ridha Allah Subhanahu wa Ta'ala, kami bermaksud menyelenggarakan pernikahan putra-putri kami. Merupakan kehormatan bagi kami sekeluarga apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"] as [string, string],
  couple: ["Atas Ridha Allah", "Kedua Mempelai"] as [string, string],
  count: ["Ngitung Dina", "Menuju Hari Bahagia"] as [string, string],
  units: ["hari", "jam", "menit", "detik"] as [string, string, string, string],
  events: ["Gelar Adicara", "Waktu & Tempat"] as [string, string],
  story: ["Jejak Langkah", "Kisah Kami"] as [string, string],
  gallery: ["Pigura", "Galeri Kenangan"] as [string, string],
  wishes: ["Pandonga", "Ucapan & Kehadiran"] as [string, string],
  gifts: ["Tanda Asih", "Amplop Digital"] as [string, string],
  closing: {
    thanks: "Kesuwun",
    text: "Atas kehadiran dan doa restu Bapak/Ibu/Saudara/i, kami sekeluarga mengucapkan terima kasih. Semoga Allah membalas setiap kebaikan dengan berlipat ganda.",
    salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh",
  },
  sent: "Jazakumullah khairan, doa dan ucapan Anda sudah terkirim.",
  wishPlaceholder: "Tuliskan doa terbaik untuk kedua mempelai…",
};

export default function CirebonKasepuhanTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Walimatul 'Ursy";
  const photo = data.gallery[0] ?? data.couple.bridePhoto ?? data.couple.groomPhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const year = toDate(data.date)?.getFullYear();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#f4ede1"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.coverTop}>
            <p className={s.coverArabic} lang="ar" dir="rtl">{BISMILLAH}</p>
            <p className={s.kicker}>{label}</p>
            <h1 className={s.coverNames}><span>{data.couple.bride}</span><em>&amp;</em><span>{data.couple.groom}</span></h1>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
          </div>
          <div className={s.gateZone}>
            <Art name="gate" className={`${s.gate} ${s.gateL}`} eager />
            <Art name="gate" className={`${s.gate} ${s.gateR}`} eager />
            <div className={s.gap}>
              <div className={s.guest}>
                <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
                <strong>{guestLabel(data)}</strong>
                {table && <span className={s.table}>{table}</span>}
              </div>
              <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={15} color="#fbf8f1" />Buka Undangan</button>
            </div>
            <Art name="wadas" className={s.rocks} eager />
            <span className={s.pool} aria-hidden />
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#fbf8f1"
        dark="#23439a"
        copy={COPY}
        hero={(
          <header className={s.hero}>
            <div className={s.plateWrap}>
              <Art name="ring" />
              <div className={s.heroPhoto}>
                {photo ? <Photo src={photo} alt={`${data.couple.bride} & ${data.couple.groom}`} /> : <span className={s.monogram} aria-hidden>{data.couple.bride.slice(0, 1)}</span>}
              </div>
            </div>
            <div className={s.plaque}>
              <p className={s.heroKicker}>{year ? `${label} · ${year}` : label}</p>
              <h1 className={s.heroNames}>{data.couple.bride} <em>&amp;</em> {data.couple.groom}</h1>
              <p className={s.heroDate}>{formatDate(data.date)}</p>
              {note && <p className={s.heroNote}>{note}</p>}
            </div>
          </header>
        )}
        slots={{
          divider: <Art name="divider" className={s.divider} />,
          node: <Art name="plate-d" />,
          amp: <Art name="plate-p" />,
          portrait: <Art name="ring" />,
          closingDecor: <Art name="wadas" className={s.closingDecor} />,
          closingEmblem: <Art name="plate-b" className={s.closingEmblem} />,
          sentArt: <Art name="plate-p" />,
        }}
      />
    </ThemeShell>
  );
}
