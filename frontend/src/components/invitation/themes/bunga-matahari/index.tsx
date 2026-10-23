"use client";
// Theme "Bunga Matahari" — lukisan guas tebal: sampul berupa satu kanvas penuh ladang bunga matahari di bawah langit
// musim panas (awan kumulus, deretan bunga yang mengecil ke cakrawala, kepala bunga raksasa di depan), nama besar di
// langit dan tanggal dalam pil kuning. Di dalam: foto berbingkai lengkung dengan seikat bunga, potret di tengah
// kelopak bunga matahari yang berputar pelan, hitung mundur dalam "piringan biji", awan yang berarak di langit kobalt.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Gloock", "Figtree:wght@400;500;600;700;800"];
// Painted by /tmp/pen/art/themes/bunga-matahari.py (field.webp is the cover's CSS background).
const Art = makeArt("bunga-matahari", { head: [300, 290], stem: [240, 662], bunch: [460, 443], clouds: [800, 169], sprig: [420, 83] } as const);

const WISHES = [
  { id: "w1", name: "Keluarga Pak Darto, tetangga ladang", attendance: "yes" as const, message: "Bunga matahari yang dulu dibagikan masih kami tanam lagi tiap musim. Selamat menempuh hidup baru, Mentari dan Bayu!" },
  { id: "w2", name: "Rekan Lab Agronomi", attendance: "yes" as const, message: "Akhirnya penelitian paling panjang Bayu berbuah juga. Semoga selalu tumbuh subur dan saling menguatkan." },
  { id: "w3", name: "Yohana & Daniel", attendance: "maybe" as const, message: "Kami usahakan datang dari Surabaya. Kalau belum bisa, doa terhangat kami kirim dari jauh." },
];

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    kicker: "Di bawah langit yang sama",
    title: "Menghadap Cahaya",
    intro: "Dengan sukacita dan rasa syukur kepada Tuhan Yang Maha Esa, kami mengundang Bapak/Ibu/Saudara/i untuk merayakan hari pernikahan kami di tengah ladang yang sedang mekar.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"],
  couple: ["Dua Hati", "Kedua Mempelai"],
  count: ["Musim Mekar", "Menuju Hari Bahagia"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Hari yang Cerah", "Waktu & Tempat"],
  story: ["Dari Benih", "Kisah Kami"],
  gallery: ["Di Bawah Matahari", "Galeri"],
  wishes: ["Kirim Kehangatan", "Ucapan & Kehadiran"],
  gifts: ["Tanda Kasih", "Amplop Digital"],
  closing: { thanks: "Terima Kasih", text: "Kehadiran dan doa Bapak/Ibu/Saudara/i adalah sinar hangat yang kami nantikan." },
  sent: "Terima kasih, ucapan hangat Anda sudah kami terima.",
  attend: { maybe: "Mungkin" },
  wishPlaceholder: "Tuliskan ucapan hangat untuk Mentari & Bayu…",
};

export default function BungaMatahariTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const photo = data.gallery[0] ?? data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);

  return (
    <ThemeShell
      fonts={FONTS}
      background="#fbf3df"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Art name="head" eager className={s.coverSun} />
          <p className={s.kicker}>Undangan {label}</p>
          <h1 className={s.coverNames}><span>{data.couple.bride}</span><em>&amp;</em><span>{data.couple.groom}</span></h1>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.guestWrap}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#ffffff" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        copy={COPY}
        demoWishes={WISHES}
        light="#fff3c8"
        dark="#234d8a"
        hero={(
          <header className={s.hero}>
            {photo && <div className={s.heroArch}><Photo src={photo} alt="" /></div>}
            <Art name="bunch" className={s.heroBunch} />
            <p className={s.heroKicker}>{label}</p>
            <h1 className={s.heroNames}>{data.couple.bride} <em>&amp;</em> {data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {data.couple.note && <p className={s.heroNote}>{data.couple.note}</p>}
          </header>
        )}
        slots={{
          divider: <span className={s.divider} aria-hidden><Art name="sprig" /></span>,
          node: <Art name="head" />,
          amp: <Art name="head" />,
          portrait: <Art name="head" className={s.portraitArt} />,
          countDecor: <Art name="clouds" className={s.countClouds} />,
          closingDecor: <><Art name="stem" className={s.closingStemL} /><Art name="stem" className={s.closingStemR} /></>,
          closingEmblem: <Art name="head" className={s.closingHead} />,
          sentArt: <Art name="head" />,
        }}
      />
    </ThemeShell>
  );
}
