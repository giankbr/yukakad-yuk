"use client";
// Theme "Kebun Apel" — kebun apel di lereng Batu dalam gouache rakyat yang ceria: pohon sarat apel merah, tangga kayu,
// keranjang bambu, gunung biru berpuncak kembar. Sampul berupa label peti buah dengan pita "panen" di atas lukisan
// kebun dan papan kayu untuk nama tamu; hitung mundur di atas peti kayu dengan angka di stiker apel; kartu acara
// seperti label bertali; galeri polaroid. Dilukis oleh /tmp/pen/art/themes/kebun-apel.py.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Young Serif", "Nunito:wght@400;600;700;800", "Lilita One"];
const Art = makeArt("kebun-apel", { apel: [180, 213], keranjang: [400, 345], dahan: [640, 196], garis: [350, 70] } as const);

const WISHES = [
  { id: "w1", name: "Bu Darmi, Kelompok Tani", attendance: "yes" as Attendance, message: "Selamat ya, Nduk Tari dan Mas Yudha. Semoga rumah tangganya subur dan berbuah manis seperti apel di kebun." },
  { id: "w2", name: "Anak-anak Pemandu Wisata", attendance: "yes" as Attendance, message: "Akhirnya! Kami siap bantu petik apel buat tamu. Bahagia terus kalian berdua!" },
  { id: "w3", name: "Rizky & Ayu, Surabaya", attendance: "maybe" as Attendance, message: "Semoga bisa naik ke Batu tepat waktu. Kalau belum sempat, titip satu keranjang apel ya!" },
];

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    kicker: "Musim panen tiba",
    title: "Ayo Panen Bahagia Bersama",
    intro: "Dengan penuh sukacita kami mengundang Bapak/Ibu/Saudara/i untuk hadir di hari pernikahan kami, di tengah kebun apel yang sedang berbuah. Kehadiran dan doa restu Anda akan membuat hari kami semakin manis.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"],
  couple: ["Si pemetik", "Kedua Mempelai"],
  count: ["Musim petik", "Tinggal Sebentar Lagi"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Catat ya", "Waktu & Tempat"],
  story: ["Dari musim ke musim", "Kisah Kami"],
  gallery: ["Album", "Potret Kebun"],
  wishes: ["Ucapan & RSVP", "Isi Keranjang Doa"],
  gifts: ["Tanda kasih", "Amplop Digital"],
  closing: { thanks: "Terima Kasih!", text: "Sampai jumpa di kebun. Kehadiran dan doa Anda adalah panen terbaik bagi kami berdua." },
  sent: "Terima kasih! Ucapan Anda sudah masuk keranjang kami.",
  attend: { maybe: "Mungkin" },
  wishPlaceholder: "Tulis ucapan dan doa untuk kami…",
  giftIntro: "Kehadiran Anda sudah lebih dari cukup. Jika ingin memberi tanda kasih, bisa melalui:",
};

export default function KebunApelTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel?.trim() || "Pernikahan";
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const bride = data.couple.bride?.trim();
  const groom = data.couple.groom?.trim();
  const photo = data.gallery[0];
  const year = /^(\d{4})/.exec(data.date ?? "")?.[1];

  return (
    <ThemeShell
      fonts={FONTS}
      background="#7bb04a"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.crate}>
            <span className={s.ribbon}>Panen Cinta{year ? ` ${year}` : ""}</span>
            <Art name="apel" className={s.crateApple} eager />
            <p className={s.crateKicker}>Undangan {label}</p>
            <h1 className={s.crateNames}>{bride}{groom && <><span aria-hidden>&amp;</span>{groom}</>}</h1>
            <p className={s.crateDate}>{formatDate(data.date)}</p>
            {data.place && <p className={s.cratePlace}>{data.place}</p>}
          </div>
          <div className={s.coverFoot}>
            <div className={s.plank}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={18} color="#fff7e6" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        copy={COPY}
        demoWishes={WISHES}
        light="#fff7e6"
        dark="#8f1a22"
        hero={(
          <header className={s.hero}>
            <Art name="dahan" className={s.heroBranch} eager />
            <div className={s.heroFrame}>
              {photo ? <Photo src={photo} alt={`${bride} & ${groom}`} /> : <div className={s.heroArt} style={{ background: "var(--scene) 50% 100% / cover" }} />}
            </div>
            <p className={s.heroLabel}>{label}</p>
            <h1 className={s.heroNames}>{bride}{groom && <> <i>&amp;</i> {groom}</>}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="garis" className={s.divider} />,
          node: <Art name="apel" />,
          amp: <Art name="apel" />,
          portrait: <Art name="apel" className={s.portraitArt} />,
          countDecor: <Art name="dahan" className={s.countDeco} />,
          closingEmblem: <Art name="keranjang" className={s.closeBasket} />,
          sentArt: <Art name="keranjang" />,
        }}
      />
    </ThemeShell>
  );
}
