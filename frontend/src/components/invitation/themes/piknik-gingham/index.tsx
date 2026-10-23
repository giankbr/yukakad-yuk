"use client";
// Theme "Piknik Gingham" — piknik di padang rumput dilihat dari atas: selimut kotak-kotak merah, keranjang rotan berisi
// serbet, baguette dan apel, piring semangka-stroberi-anggur, dua gelas limun, papan roti lapis, dan seikat bunga liar.
// Gouache matte dengan bayangan lembut di atas kain.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Fraunces:ital,wght@0,400;0,600;0,700;1,400;1,600", "Figtree:wght@400;500;600;700", "Gochi Hand"];
// Painted by /tmp/pen/art/themes/piknik-gingham.py (tools/art/themes in the repo).
const Art = makeArt("piknik-gingham", { basket: [560, 483], fruit: [380, 402], lemonade: [380, 349], sandwich: [380, 254], flowers: [400, 407], chain: [390, 49] } as const);

const WISHES = [
  { id: "w1", name: "Mbak Sarah & Mas Dimas", attendance: "yes" as Attendance, message: "Selamat Kinan dan Bagas! Kami bawa selimut sendiri ya. Semoga rumah tangga kalian selalu hangat seperti sore piknik." },
  { id: "w2", name: "Geng Car Free Day Dago", attendance: "yes" as Attendance, message: "Dari pembeli limun jadi istri penjualnya! Bahagia selalu, kami datang bawa ucapan paling meriah." },
  { id: "w3", name: "Om Hendra sekeluarga", attendance: "maybe" as Attendance, message: "Semoga cuacanya cerah dan langgeng selamanya. Kami usahakan hadir dari Surabaya." },
];

export default function PiknikGinghamTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const hero = data.gallery[0] ?? data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const copy: ThemeCopy = {
    ...DEFAULT_COPY,
    opening: {
      kicker: "Halo, sahabat!",
      title: "Ayo Piknik Bersama Kami",
      intro: "Dengan sukacita dan rasa syukur kepada Tuhan Yang Maha Esa, kami mengundang Bapak/Ibu/Saudara/i untuk duduk bersama di atas selimut, berbagi makanan dan tawa, serta menjadi saksi hari bahagia kami.",
    },
    roles: ["Mempelai Wanita", "Mempelai Pria"],
    couple: ["Yang Berbahagia", "Kedua Mempelai"],
    count: ["Siapkan keranjangmu", "Menuju Hari Piknik"],
    units: ["Hari", "Jam", "Menit", "Detik"],
    events: ["Catat tanggalnya", "Waktu & Tempat"],
    story: ["Dari segelas limun", "Cerita Kami"],
    gallery: ["Album piknik", "Momen Kami"],
    wishes: ["Kirim pesan", "Ucapan & Kehadiran"],
    gifts: ["Tanda kasih", "Kado Pernikahan"],
    closing: { thanks: "Terima kasih!", text: "Sampai jumpa di atas selimut kotak-kotak. Kehadiran dan doa restu Anda adalah bekal terbaik untuk perjalanan kami." },
    sent: "Hore, ucapanmu sudah masuk keranjang! Terima kasih banyak.",
    attend: { maybe: "Mungkin" },
    wishPlaceholder: "Tuliskan ucapan dan doa untuk kedua mempelai…",
    giftIntro: "Kehadiranmu sudah jadi hadiah terindah. Bila ingin mengirim tanda kasih, bisa melalui:",
    familyLabel: "Dengan hangat, keluarga",
  };

  return (
    <ThemeShell
      fonts={FONTS}
      background="#e8d6c0"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Art name="basket" eager className={s.cBasket} />
          <Art name="fruit" eager className={s.cFruit} />
          <Art name="lemonade" eager className={s.cLemon} />
          <Art name="sandwich" eager className={s.cSandwich} />
          <Art name="flowers" eager className={s.cFlowers} />
          <div className={s.card}>
            <p className={s.kicker}>Ayo piknik bersama!</p>
            <p className={s.cardLabel}>Undangan {label}</p>
            <h1 className={s.coverNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={18} color="#ffffff" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        copy={copy}
        demoWishes={WISHES}
        light="#fff3c4"
        dark="#3a2a22"
        hero={(
          <header className={s.hero}>
            <span className={s.heroStrip} aria-hidden />
            <div className={s.heroPlate}>
              <div className={s.heroPhoto}><Photo src={hero} alt="" /></div>
              <Art name="flowers" className={s.heroFlowers} />
            </div>
            <p className={s.heroKicker}>Kami menikah!</p>
            <h1 className={s.heroNames}>{data.couple.bride} <em>&amp;</em> {data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="chain" className={s.divider} />,
          node: <Art name="fruit" />,
          portrait: <Art name="flowers" />,
          closingDecor: <><span className={s.closingCard} aria-hidden /><Art name="basket" className={s.closingBasket} /><Art name="flowers" className={s.closingFlowers} /></>,
          closingEmblem: <Art name="chain" className={s.closingEmblem} />,
          sentArt: <Art name="lemonade" />,
        }}
      />
    </ThemeShell>
  );
}
