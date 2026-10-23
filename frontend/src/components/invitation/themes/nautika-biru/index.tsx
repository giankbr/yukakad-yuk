"use client";
// Theme "Nautika Biru" — nuansa bahari. Sampul: panel garis biru-putih lukisan tangan dengan untaian bendera isyarat
// (pola dekoratif, bukan pesan), foto di balik jendela kapal berbingkai kuningan berbaut, nama bergaya Bodoni miring,
// simpul tali di bawah nama, dan kompas yang berputar pelan. Di dalam: pelabuhan pagi (perahu layar, mercusuar
// merah-putih) dengan papan nama kuningan, potret bundar sebagai jendela kapal, hitung mundur dalam lingkaran pelampung.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Bodoni Moda:ital,opsz,wght@0,6..96,400;0,6..96,500;0,6..96,700;1,6..96,400;1,6..96,500", "Josefin Sans:wght@400;600;700"];
// Painted by /tmp/pen/art/themes/nautika-biru.py (stripe.webp is a CSS background).
const Art = makeArt("nautika-biru", {
  harbour: [700, 556], compass: [360, 360], anchor: [240, 316], flags: [820, 119], knot: [420, 56], ring: [480, 480],
} as const);

const WISHES = [
  { id: "w1", name: "Klub Layar Teluk Jakarta", attendance: "yes" as const, message: "Nakhoda dan awak kapal paling kompak di dermaga! Selamat berlayar ke samudra baru, Ines dan Arka." },
  { id: "w2", name: "Om Benny & Tante Grace", attendance: "yes" as const, message: "Semoga rumah tangga kalian selalu punya pelabuhan yang tenang, apa pun cuacanya di luar sana." },
  { id: "w3", name: "Dewi Anggraini", attendance: "maybe" as const, message: "Sedang dinas di Makassar, semoga sempat pulang. Doa terbaik dari seberang laut." },
];

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    kicker: "Selamat Datang di Geladak",
    title: "Berlayar Bersama",
    intro: "Dengan penuh syukur kepada Tuhan Yang Maha Esa, kami mengundang Bapak/Ibu/Saudara/i untuk menjadi saksi saat kami memulai pelayaran hidup yang baru. Kehadiran Anda adalah angin baik bagi layar kami.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"],
  couple: ["Nakhoda & Awak", "Kedua Mempelai"],
  count: ["Menuju Pelabuhan", "Hitung Mundur"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Rute Pelayaran", "Waktu & Tempat"],
  story: ["Buku Log", "Catatan Pelayaran"],
  gallery: ["Dari Tepi Laut", "Galeri"],
  wishes: ["Pesan dalam Botol", "Ucapan & Kehadiran"],
  gifts: ["Tanda Kasih", "Amplop Digital"],
  closing: { thanks: "Terima Kasih", text: "Terima kasih telah menjadi bagian dari pelayaran kami. Sampai jumpa di dermaga." },
  sent: "Terima kasih, pesan Anda sudah berlayar sampai ke kami.",
  attend: { maybe: "Mungkin" },
  wishPlaceholder: "Tuliskan pesan dan doa untuk Ines & Arka…",
};

export default function NautikaBiruTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const photo = data.gallery[0] ?? data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);

  return (
    <ThemeShell
      fonts={FONTS}
      background="#f5f2ea"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <span className={s.stripes} aria-hidden />
          <Art name="flags" eager className={s.coverFlags} />
          <div className={s.porthole}>
            <div className={s.portholeGlass}><Photo src={photo} alt="" /></div>
            <Art name="ring" eager className={s.portholeRing} />
          </div>
          <p className={s.kicker}>Undangan {label}</p>
          <h1 className={s.coverNames}><span>{data.couple.bride}</span><em>&amp;</em><span>{data.couple.groom}</span></h1>
          <Art name="knot" eager className={s.coverKnot} />
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <Art name="compass" eager className={s.coverCompass} />
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
        light="#f5f2ea"
        dark="#1b2a4a"
        hero={(
          <header className={s.hero}>
            <div className={s.heroScene}><Art name="harbour" /><span className={s.heroBoatGlint} aria-hidden /></div>
            <div className={s.plaque}>
              <p className={s.heroKicker}>{label}</p>
              <h1 className={s.heroNames}>{data.couple.bride} &amp; {data.couple.groom}</h1>
            </div>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {data.couple.note && <p className={s.heroNote}>{data.couple.note}</p>}
            <Art name="anchor" className={s.heroAnchor} />
          </header>
        )}
        slots={{
          divider: <span className={s.divider} aria-hidden><Art name="knot" /></span>,
          node: <Art name="compass" />,
          amp: <Art name="knot" />,
          portrait: <Art name="ring" className={s.portraitArt} />,
          countDecor: <Art name="compass" className={s.countCompass} />,
          closingEmblem: <Art name="anchor" className={s.closingAnchor} />,
          sentArt: <Art name="compass" />,
        }}
      />
    </ThemeShell>
  );
}
