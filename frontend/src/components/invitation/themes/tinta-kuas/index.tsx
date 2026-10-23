"use client";
// Theme "Tinta Kuas" — modern, hitam-putih dan berani: goresan kuas tinta hitam berekor kuas kering, cipratan tinta
// emas, banyak ruang putih. Nama diset dengan huruf kuas (Kaushan Script), label Archivo berspasi lebar, aksen
// Instrument Serif miring; tata letak rata kiri ala label galeri. Dilukis oleh /tmp/pen/art/themes/tinta-kuas.py.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Kaushan Script", "Archivo:wght@400;500;600;700;800", "Instrument Serif:ital@0;1"];
const Art = makeArt("tinta-kuas", {
  swash: [820, 185], sweep: [480, 473], ring: [340, 330], splat: [420, 264], rule: [360, 24], dab: [160, 105],
} as const);

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    kicker: "Salam hangat",
    title: "Dengan sukacita",
    sub: "kami mengundang Anda",
    intro: "Dengan penuh syukur, kami mengundang Bapak/Ibu/Saudara/i untuk hadir dan merayakan hari pernikahan kami. Kehadiran dan doa Anda akan menjadi goresan terindah di halaman pertama cerita kami.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"],
  couple: ["Dua goresan", "Kami Berdua"],
  count: ["Tinta hampir kering", "Hitung Mundur"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Catat di agenda", "Waktu & Tempat"],
  story: ["Sketsa perjalanan", "Cerita Kami"],
  gallery: ["Cetakan hitam-putih", "Galeri"],
  wishes: ["Tinggalkan jejak", "Ucapan & RSVP"],
  gifts: ["Tanda kasih", "Hadiah"],
  closing: {
    thanks: "Terima kasih",
    text: "Kehadiran dan doa restu Anda adalah sapuan warna yang melengkapi hari bahagia kami.",
  },
  sent: "Terima kasih, ucapan Anda sudah tergores di buku tamu kami.",
  attend: { maybe: "Mungkin" },
  wishPlaceholder: "Tulis ucapan untuk kami berdua…",
  giftIntro: "Kehadiran Anda sudah lebih dari cukup. Bila ingin memberi tanda kasih, dapat melalui:",
};

const WISHES = [
  { id: "w1", name: "Studio Garis Kanan", attendance: "yes" as const, message: "Dari kelas lettering ke pelaminan! Selamat Nadia dan Kevin, kami siap bawa kuas untuk live painting-nya." },
  { id: "w2", name: "Tante Lina & Om Ferry", attendance: "yes" as const, message: "Selamat menempuh hidup baru. Semoga rumah tangga kalian selalu hangat dan penuh warna." },
  { id: "w3", name: "Aldo Pranata", attendance: "maybe" as const, message: "Masih menunggu jadwal dinas, semoga bisa datang. Kalau tidak, selamat dari jauh, langgeng terus!" },
];

export default function TintaKuasTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const bride = data.couple.bride;
  const groom = data.couple.groom?.trim();
  const photo = data.gallery[0];
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#e8e6e0"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Art name="sweep" eager className={s.coverSweep} />
          <Art name="splat" eager className={s.coverSplat} />
          <p className={s.kicker}>Undangan {label}</p>
          <p className={s.kickerSub}>dengan hormat, dari kami berdua</p>
          <h1 className={s.coverNames}><span>{bride}</span>{groom && <><em>&amp;</em><span>{groom}</span></>}</h1>
          <div className={s.dateBand}>
            <Art name="swash" eager />
            <p className={s.coverDate}>{formatDate(data.date)}</p>
          </div>
          {data.place && <p className={s.coverPlace}>{data.place}</p>}
          <div className={s.coverFoot}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#fdfcf9" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        copy={COPY}
        demoWishes={WISHES}
        light="#e6cc8a"
        dark="#141414"
        hero={(
          <header className={s.hero}>
            <div className={s.heroPhoto}>{photo ? <Photo src={photo} alt={`${bride}${groom ? ` dan ${groom}` : ""}`} /> : <span className={s.heroMono} aria-hidden>{bride.slice(0, 1)}</span>}</div>
            <Art name="splat" className={s.heroSplat} />
            <Art name="swash" className={s.heroStroke} />
            <p className={s.heroKicker}>The Wedding of</p>
            <h1 className={s.heroNames}>{bride}{groom && <> <em>&amp;</em> {groom}</>}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="rule" className={s.divider} />,
          amp: <Art name="splat" />,
          portrait: <Art name="ring" />,
          countDecor: <Art name="splat" className={s.countSplat} />,
          closingDecor: <Art name="sweep" className={s.closingSweep} />,
          sentArt: <Art name="splat" />,
        }}
      />
    </ThemeShell>
  );
}
