"use client";
// Theme "Provence Lavender" — lanskap gouache musim panas: langit hangat, rumah batu beratap terakota di puncak bukit di
// antara pohon cemara dan zaitun, baris-baris lavender berperspektif yang menuntun mata ke sana. Nama berdiri di langit,
// tamu menerima kartu pos berperangko di atas ladang; acara menjadi kartu pos bercap pos, potret berbentuk oval kameo,
// dan penutup kembali ke ladang saat senja.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Bodoni Moda:ital,wght@0,400;0,500;1,400;1,500", "Spectral:ital,wght@0,400;0,500;0,600;1,400", "Mrs Saint Delafield:wght@400"];
// Painted by /tmp/pen/art/themes/provence-lavender.py (sky.webp and rows.webp are also CSS backgrounds)
const Art = makeArt("provence-lavender", { farm: [780, 367], rows: [780, 719], bunch: [240, 344], sprig: [320, 62] } as const);

const WISHES = [
  { id: "w1", name: "Tante Veronika & Om Hendra", attendance: "yes" as const, message: "Selamat menempuh hidup baru, Clarissa dan Raditya. Semoga rumah kalian selalu hangat seperti sore musim panas." },
  { id: "w2", name: "Teman Kelas Gouache", attendance: "yes" as const, message: "Akhirnya cat ungu itu dikembalikan juga, ya! Ikut bahagia, sampai jumpa di kebun." },
  { id: "w3", name: "Keluarga Pak Gunawan", attendance: "maybe" as const, message: "Kami usahakan datang ke Lembang. Tuhan memberkati pernikahan kalian berdua." },
];

export default function ProvenceLavenderTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const { bride, groom } = data.couple;
  const label = data.eventLabel ?? "Pernikahan";
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const hero = data.gallery[0];

  return (
    <ThemeShell
      fonts={FONTS}
      background="#e8e0ec"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Art name="farm" eager className={s.coverFarm} />
          <Art name="rows" eager className={s.coverRows} />
          <p className={s.kicker}>Undangan {label}</p>
          <h1 className={s.coverNames}><span>{bride}</span>{groom && <><i>&amp;</i><span>{groom}</span></>}</h1>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.postcard}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <span className={s.stamp} aria-hidden><Art name="bunch" eager /></span>
            <span className={s.postLines} aria-hidden />
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#fbf6ee" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#fbf6ee"
        dark="#3b2c4a"
        demoWishes={WISHES}
        copy={{
          ...DEFAULT_COPY,
          opening: {
            kicker: "Salam hangat dari kebun lavender",
            title: "Dengan penuh sukacita",
            intro: "Kami mengundang Bapak/Ibu/Saudara/i untuk hadir dan berbagi kebahagiaan di hari pernikahan kami: sebuah sore musim kemarau di antara baris-baris ungu, meja panjang, dan cahaya keemasan.",
          },
          roles: ["Mempelai Wanita", "Mempelai Pria"],
          couple: ["Dua hati, satu jalan setapak", "Kedua Mempelai"],
          count: ["Menuju sore yang dinanti", "Hitung Mundur"],
          units: ["Hari", "Jam", "Menit", "Detik"],
          events: ["Simpan tanggalnya", "Waktu & Tempat"],
          story: ["Dari kanvas ke ladang", "Kisah Kami"],
          gallery: ["Album musim panas", "Galeri"],
          wishes: ["Kirim kabar", "Ucapan & Kehadiran"],
          gifts: ["Tanda kasih", "Amplop Digital"],
          closing: { thanks: "Merci & Terima Kasih", text: "Kehadiran dan doa Bapak/Ibu/Saudara/i adalah hadiah terindah bagi kami berdua dan keluarga." },
          sent: "Terima kasih, ucapan Anda sudah sampai seperti kartu pos yang dinanti.",
          attend: { maybe: "Mungkin" },
          wishPlaceholder: "Tuliskan ucapan dan doa untuk Clarissa & Raditya…",
        }}
        hero={(
          <header className={s.hero}>
            <div className={s.heroCard}>
              {hero ? <div className={s.heroPhoto}><Photo src={hero} alt={`${bride} & ${groom}`} /></div> : <div className={s.heroNoPhoto}><Art name="bunch" /></div>}
              <p className={s.heroCaption}>{data.place || label}</p>
              <Art name="bunch" className={s.heroBunch} />
            </div>
            <p className={s.heroKicker}>{label}</p>
            <h1 className={s.heroNames}>{bride}{groom && <><i>&amp;</i>{groom}</>}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="sprig" className={s.divider} />,
          node: <Art name="bunch" />,
          amp: <Art name="sprig" />,
          portrait: <Art name="sprig" className={s.portraitSprig} />,
          countDecor: <span className={s.countRows} aria-hidden />,
          closingDecor: <div className={s.closingScene} aria-hidden><Art name="farm" /><Art name="rows" /></div>,
          sentArt: <Art name="bunch" />,
        }}
      />
    </ThemeShell>
  );
}
