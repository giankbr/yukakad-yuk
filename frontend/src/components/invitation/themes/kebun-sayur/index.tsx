"use client";
// Theme "Kebun Sayur" — pernikahan farm-to-table bergaya gouache ceria. Sampulnya bungkus benih dari kertas kraft
// bertepi gerigi dengan jendela ilustrasi keranjang panen (wortel, tomat, kubis, terung, lobak); nama tamu tertulis di
// papan tanam kayu yang tertancap di bedeng sayur, gembor seng menyiram dari pojok, seikat bunga liar di sisi lain.
// Acara menjadi label bedeng kayu, hitung mundur di atas tanah dengan bedeng, amplop seperti bungkus benih.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Young Serif:wght@400", "Work Sans:wght@400;500;600;700", "Gochi Hand:wght@400"];
// Painted by /tmp/pen/art/themes/kebun-sayur.py
const Art = makeArt("kebun-sayur", {
  basket: [520, 414], bed: [780, 174], can: [300, 189], stake: [300, 555], wild: [260, 152], carrot: [96, 103], tomato: [96, 105], pea: [96, 79],
} as const);

const WISHES = [
  { id: "w1", name: "Bu Siti, Pasar Tani Batu", attendance: "yes" as const, message: "Selamat ya, Mbak Wulan dan Mas Bima! Semoga rumah tangganya subur, rukun, dan panennya melimpah terus." },
  { id: "w2", name: "Teman Kebun Kampus", attendance: "yes" as const, message: "Dari petak sebelahan sampai pelaminan di kebun. Kami bawa bibit cabai sebagai kado, ya!" },
  { id: "w3", name: "Mas Dodi & Keluarga", attendance: "maybe" as const, message: "Semoga bisa naik ke Selecta hari itu. Bahagia selalu untuk kalian berdua." },
];

export default function KebunSayurTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const { bride, groom } = data.couple;
  const label = data.eventLabel ?? "Pernikahan";
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const hero = data.gallery[0];
  const year = data.date ? new Date(data.date).getFullYear() : undefined;

  return (
    <ThemeShell
      fonts={FONTS}
      background="#e9dfc6"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Art name="wild" eager className={s.wild} />
          <Art name="can" eager className={s.can} />
          <div className={s.packet}>
            <p className={s.packetHead}><span>Benih Pilihan</span><span>{year && !Number.isNaN(year) ? `Panen ${year}` : "Panen Raya"}</span></p>
            <div className={s.packetWin} aria-hidden><Art name="basket" eager /></div>
            <p className={s.kicker}>Undangan {label}</p>
            <h1 className={s.coverNames}>{bride}{groom && <><i>&amp;</i>{groom}</>}</h1>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
          </div>
          <div className={s.stakeWrap}>
            <div className={s.stake}>
              <Art name="stake" eager />
              <div className={s.stakeText}>
                <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
                <strong>{guestLabel(data)}</strong>
                {table && <span className={s.table}>{table}</span>}
              </div>
              <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#fff6e4" />Buka Undangan</button>
            </div>
          </div>
          <Art name="bed" eager className={s.bed} />
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#fff6e4"
        dark="#3d6427"
        demoWishes={WISHES}
        copy={{
          ...DEFAULT_COPY,
          opening: {
            kicker: "Halo, sahabat kebun!",
            title: "Mari panen bahagia bersama",
            intro: "Dengan penuh syukur, kami mengundang Bapak/Ibu/Saudara/i ke hari pernikahan kami: sebuah pesta sederhana di tengah kebun, dengan makanan dari ladang, tawa, dan doa baik untuk musim-musim di depan.",
          },
          roles: ["Mempelai Wanita", "Mempelai Pria"],
          couple: ["Petani muda kita", "Kedua Mempelai"],
          count: ["Sebentar lagi panen", "Hitung Mundur"],
          units: ["Hari", "Jam", "Menit", "Detik"],
          events: ["Catat di kalender kebun", "Waktu & Tempat"],
          story: ["Dari benih sampai panen", "Kisah Kami"],
          gallery: ["Hasil kebun", "Galeri"],
          wishes: ["Tanam doa baikmu", "Ucapan & Kehadiran"],
          gifts: ["Tanda kasih", "Amplop Digital"],
          closing: { thanks: "Terima kasih!", text: "Kehadiran dan doa Bapak/Ibu/Saudara/i adalah pupuk terbaik untuk rumah tangga kami. Sampai jumpa di kebun!" },
          sent: "Terima kasih! Doa baikmu sudah kami tanam.",
          attend: { maybe: "Mungkin" },
          wishPlaceholder: "Tuliskan ucapan untuk Wulan & Bima…",
        }}
        hero={(
          <header className={s.hero}>
            {hero ? (
              <div className={s.heroFrame}>
                <div className={s.heroPhoto}><Photo src={hero} alt={`${bride} & ${groom}`} /></div>
                <Art name="basket" className={s.heroBasket} />
              </div>
            ) : <Art name="basket" className={s.heroBasketSolo} />}
            <p className={s.heroKicker}>{label}</p>
            <h1 className={s.heroNames}>{bride}{groom && <><i>&amp;</i>{groom}</>}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
            <div className={s.stickers} aria-hidden>
              <span><Art name="carrot" />Dari kebun</span>
              <span><Art name="tomato" />Ke meja</span>
              <span><Art name="pea" />Untuk semua</span>
            </div>
          </header>
        )}
        slots={{
          divider: <span className={s.divider} aria-hidden><Art name="carrot" /></span>,
          node: <Art name="pea" />,
          amp: <Art name="tomato" />,
          portrait: <Art name="tomato" className={s.portraitVeg} />,
          countDecor: <Art name="bed" className={s.countBed} />,
          closingDecor: <Art name="bed" className={s.closingBed} />,
          closingEmblem: <Art name="basket" className={s.closingBasket} />,
          sentArt: <Art name="basket" />,
        }}
      />
    </ThemeShell>
  );
}
