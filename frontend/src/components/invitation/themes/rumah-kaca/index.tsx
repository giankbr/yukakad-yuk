"use client";
// Theme "Rumah Kaca" — rumah kaca botani bergaya Victoria di cahaya pagi (desain orisinal): fasad kubah kaca berangka
// besi verdigris dengan palem kentia dan pakis Boston di balik kaca berkabut, sinar pagi menyorot miring, keranjang
// pakis tergantung berayun, dan plakat label botani berbingkai besi. Dilukis cat air + gouache oleh
// /tmp/pen/art/themes/rumah-kaca.py. Bodoni Moda, Petrona, Pinyon Script.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Bodoni Moda:ital,wght@0,400;0,600;1,400", "Petrona:ital,wght@0,400;0,600;1,400;1,600", "Pinyon Script"];
const Art = makeArt("rumah-kaca", {
  house: [350, 449], fern: [110, 173], palm: [160, 154], divider: [200, 21], sprig: [45, 51],
} as const);

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    kicker: "Dengan penuh sukacita",
    title: "Kami akan menikah",
    sub: "di bawah atap kaca yang terang",
    intro: "Dengan memohon berkat dan rahmat Tuhan, kami mengundang Bapak/Ibu/Saudara/i untuk hadir dan menjadi bagian dari pagi bahagia kami. Kehadiran dan doa Anda adalah cahaya yang membuat segalanya tumbuh.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"],
  couple: ["Koleksi paling berharga", "Kami Berdua"],
  count: ["Menanti pagi itu", "Hitung Mundur"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Waktu & tempat", "Rangkaian Acara"],
  story: ["Catatan kebun", "Kisah Kami Tumbuh"],
  gallery: ["Album", "Potret di Antara Palem"],
  wishes: ["Doa & kehadiran", "Ucapan & Konfirmasi"],
  gifts: ["Tanda kasih", "Hadiah Pernikahan"],
  closing: {
    thanks: "Terima kasih",
    text: "Kehadiran dan doa restu Anda adalah sinar pagi bagi kami. Sampai jumpa di bawah kubah kaca.",
  },
  sent: "Terima kasih, ucapan Anda sudah kami simpan seperti tanaman kesayangan.",
  attend: { maybe: "Mungkin" },
  wishPlaceholder: "Tuliskan ucapan dan doa untuk kami berdua…",
};

const WISHES = [
  { id: "w1", name: "Tante Wulan & Om Bayu", attendance: "yes" as const, message: "Selamat Laras dan Adrian! Semoga rumah tangga kalian selalu terang dan hangat, seperti rumah kaca di pagi hari." },
  { id: "w2", name: "Klub Tanaman Hias Bogor", attendance: "yes" as const, message: "Akhirnya! Kami datang membawa stek pakis untuk kebun kalian yang baru. Bahagia selalu." },
  { id: "w3", name: "Nadia Kusuma", attendance: "maybe" as const, message: "Semoga bisa menyusul dari Surabaya. Doa terbaik untuk kalian berdua, tumbuh bersama selamanya." },
];

export default function RumahKacaTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const photo = data.gallery[0] ?? data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const groom = data.couple.groom?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#eef0e8"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Art name="fern" eager className={`${s.hang} ${s.hangL}`} />
          <Art name="fern" eager className={`${s.hang} ${s.hangR}`} />
          <Art name="house" eager className={s.house} />
          <div className={s.plaque}>
            <p className={s.kicker}>Undangan {label}</p>
            <h1 className={s.coverNames}><span>{data.couple.bride}</span>{groom && <><em>&amp;</em><span>{groom}</span></>}</h1>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#f3f1e6" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        demoWishes={WISHES}
        light="#ead6a3"
        dark="#1a2a25"
        copy={COPY}
        hero={(
          <header className={s.hero}>
            <div className={s.heroWin}>
              <div className={s.heroPhoto}>{photo ? <Photo src={photo} alt={`${data.couple.bride}${groom ? ` dan ${groom}` : ""}`} /> : <span className={s.heroMono} aria-hidden>{data.couple.bride.slice(0, 1)}</span>}</div>
              <span className={s.heroBars} aria-hidden />
              <Art name="palm" className={`${s.heroPalm} ${s.heroPalmL}`} />
              <Art name="palm" className={`${s.heroPalm} ${s.heroPalmR}`} />
            </div>
            <p className={s.heroKicker}>The Wedding of</p>
            <h1 className={s.heroNames}><span>{data.couple.bride}</span>{groom && <><em>&amp;</em><span>{groom}</span></>}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="divider" className={s.divider} />,
          node: <Art name="sprig" />,
          amp: <Art name="sprig" />,
          countDecor: <Art name="fern" className={s.countFern} />,
          closingEmblem: <Art name="palm" className={s.closingEmblem} />,
          sentArt: <Art name="palm" />,
        }}
      />
    </ThemeShell>
  );
}
