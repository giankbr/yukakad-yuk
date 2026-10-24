"use client";
// Theme "Sape Dayak" — pernikahan Kristen keluarga Dayak dari hulu Mahakam: sape berukir bergaya gouache (badan
// perahu bercat sulur kelawit hitam-merah) berdiri di tepi sungai berkabut dengan hutan hujan dan lamin di
// kejauhan. Teks rata kiri di dalam kabut, potret berbentuk badan sape, kartu acara bergaris fret, kabut berarak
// pelan dan sape yang bergoyang lembut.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Young Serif", "Alegreya:ital,wght@0,400;0,700;1,400", "Alegreya Sans:wght@500;700"];
// Painted by /tmp/pen/art/themes/sape-dayak.py (the river scene is a CSS background).
const Art = makeArt("sape-dayak", { sape: [240, 1058], divider: [440, 39], curl: [178, 178] } as const);

const WISHES = [
  { id: "w1", name: "Keluarga Pdt. Markus Lenjau", attendance: "yes" as const, message: "Selamat menempuh hidup baru, Lusi dan Daniel. Kiranya kasih Tuhan menjadi dasar rumah tangga kalian, teguh seperti tiang lamin." },
  { id: "w2", name: "Yosef & Teman Kehutanan", attendance: "yes" as const, message: "Akhirnya! Selamat ya, Bro Daniel. Jangan lupa bawa sape ke resepsi, kami mau dengar lagu yang dulu itu." },
  { id: "w3", name: "Tante Lidia, Balikpapan", attendance: "maybe" as const, message: "Tante usahakan datang ya, Sayang. Kalau belum bisa, doa Tante menyertai kalian berdua. Tuhan memberkati." },
];

export default function SapeDayakTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const hero = data.gallery[0];
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#dfe5df"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <span className={s.mist} aria-hidden />
          <div className={s.coverText}>
            <p className={s.kicker}>Undangan {label}</p>
            <h1 className={s.coverNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
            <Art name="curl" eager className={s.coverCurl} />
          </div>
          <div className={s.sapeWrap} aria-hidden><Art name="sape" eager className={s.sape} /></div>
          <div className={s.guestWrap}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#f3e6c8" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#f3e6c8"
        dark="#1f3a30"
        demoWishes={WISHES}
        copy={{
          opening: {
            kicker: "Salam Sejahtera",
            title: "Dalam Kasih Tuhan",
            intro: "Dengan penuh syukur atas kasih karunia Tuhan Yesus Kristus, kami mengundang Bapak/Ibu/Saudara/i untuk hadir dan turut berbahagia pada pemberkatan nikah dan syukuran adat putra-putri kami.",
          },
          roles: ["Mempelai Perempuan", "Mempelai Laki-laki"],
          couple: ["Dua dawai, satu lagu", "Kedua Mempelai"],
          count: ["Menanti petikan pertama", "Menuju Hari Bahagia"],
          units: ["Hari", "Jam", "Menit", "Detik"],
          events: ["Kami menanti di", "Waktu & Tempat"],
          story: ["Alunan kisah", "Perjalanan Kami"],
          gallery: ["Galeri", "Dari Hulu ke Hilir"],
          wishes: ["Doa & restu", "Ucapan & Kehadiran"],
          gifts: ["Tanda kasih", "Amplop Digital"],
          closing: {
            thanks: "Terima Kasih",
            text: "Kehadiran serta doa Bapak/Ibu/Saudara/i adalah berkat yang sangat berarti bagi kami dan kedua keluarga besar.",
            salam: "Tuhan Yesus memberkati",
          },
          sent: "Terima kasih, doa dan ucapan Anda sudah terkirim.",
          attend: { maybe: "Mungkin" },
          wishPlaceholder: "Tuliskan doa dan ucapan untuk kedua mempelai…",
          giftIntro: "Doa dan kehadiran Anda adalah hadiah terindah. Bila ingin memberi tanda kasih, dapat melalui:",
        }}
        hero={(
          <header className={s.hero}>
            {hero && (
              <div className={s.heroPhotoWrap}>
                <div className={s.heroPhoto}><Photo src={hero} alt="" /></div>
                <Art name="curl" className={s.heroCurl} />
              </div>
            )}
            <p className={s.heroKicker}>{label}</p>
            <h1 className={s.heroNames}>{data.couple.bride} <em>&amp;</em> {data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="divider" className={s.divider} />,
          node: <Art name="curl" />,
          amp: <Art name="curl" />,
          countDecor: <><Art name="curl" className={`${s.countDecor} ${s.countDecorL}`} /><Art name="curl" className={`${s.countDecor} ${s.countDecorR}`} /></>,
          closingEmblem: <span className={s.medal} aria-hidden><Art name="curl" /></span>,
          sentArt: <Art name="curl" />,
        }}
      />
    </ThemeShell>
  );
}
