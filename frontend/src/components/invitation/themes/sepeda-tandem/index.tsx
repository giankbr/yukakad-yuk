"use client";
// Theme "Sepeda Tandem" — buku cerita gouache yang ceria: sepeda tandem merah berkeranjang bunga dengan balon terikat
// di sadel, melaju di jalan desa berkelok di antara ladang bunga matahari dan lavender, bendera segitiga melintang.
// Hitung mundur berupa patok kilometer, potret di dalam roda sepeda. Dilukis oleh /tmp/pen/art/themes/sepeda-tandem.py.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Young Serif", "Nunito:wght@400;600;700;800", "Gochi Hand"];
const Art = makeArt("sepeda-tandem", {
  scene: [780, 724], bike: [556, 349], balloons: [212, 428], bunting: [380, 50], flowers: [180, 147], wheel: [340, 341],
} as const);

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    kicker: "Halo, teman seperjalanan!",
    title: "Kami mau menikah!",
    sub: "ayo ikut mengayuh ke hari bahagia kami",
    intro: "Dengan penuh syukur, kami mengundang Bapak/Ibu/Saudara/i untuk merayakan hari pernikahan kami di tengah kebun dan ladang. Bawa senyum terbaik, kami siapkan teh hangat dan jalan desa yang berbunga.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"],
  couple: ["Satu sepeda, dua pengayuh", "Kami Berdua"],
  count: ["Tinggal beberapa kilometer lagi", "Hitung Mundur"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Catat rutenya", "Jadwal Acara"],
  story: ["Jalan yang kami lalui", "Kisah Kami"],
  gallery: ["Foto-foto di perjalanan", "Galeri"],
  wishes: ["Titip pesan di keranjang", "Ucapan & RSVP"],
  gifts: ["Tanda kasih", "Kado Pernikahan"],
  closing: {
    thanks: "Terima kasih!",
    text: "Kehadiran dan doa Anda adalah angin sepoi yang membuat kayuhan kami terasa ringan. Sampai jumpa di kebun!",
  },
  sent: "Asyik, pesanmu sudah masuk keranjang! Terima kasih banyak.",
  attend: { maybe: "Mungkin" },
  wishPlaceholder: "Tulis ucapan dan doa untuk kami berdua…",
};

const WISHES = [
  { id: "w1", name: "Komunitas Gowes Minggu Pagi", attendance: "yes" as const, message: "Akhirnya pasangan paling tidak kompak di tanjakan menikah juga! Kami datang naik sepeda, siapkan parkiran ya." },
  { id: "w2", name: "Bu Dedeh & Pak Asep", attendance: "yes" as const, message: "Wilujeng nikah, Sekar sareng Bayu. Semoga rumah tangganya rukun dan selalu searah seperti kayuhan tandem." },
  { id: "w3", name: "Gilang Ramadhan", attendance: "maybe" as const, message: "Masih di Surabaya, semoga bisa menyusul. Kalau tidak, doa terbaik dari jauh. Langgeng terus!" },
];

export default function SepedaTandemTheme(props: ThemeProps) {
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
      background="#cfe3e6"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <span className={`${s.cloud} ${s.cloudA}`} aria-hidden />
          <span className={`${s.cloud} ${s.cloudB}`} aria-hidden />
          <p className={s.kicker}>Undangan {label}</p>
          <h1 className={s.coverNames}><span>{bride}</span>{groom && <><em>&amp;</em><span>{groom}</span></>}</h1>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.coverFoot}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#fffaf0" />Buka Undangan</button>
          </div>
          <div className={s.land}>
            <Art name="scene" eager className={s.scene} />
            <div className={s.bikeRig}>
              <Art name="balloons" eager className={s.balloons} />
              <Art name="bike" eager className={s.bike} />
            </div>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        copy={COPY}
        demoWishes={WISHES}
        light="#fffaf0"
        dark="#3a2c26"
        hero={(
          <header className={s.hero}>
            <Art name="bunting" className={s.heroBunting} />
            <div className={s.heroPhoto}>{photo ? <Photo src={photo} alt={`${bride}${groom ? ` dan ${groom}` : ""}`} /> : <span className={s.heroMono} aria-hidden>{bride.slice(0, 1)}</span>}</div>
            <Art name="flowers" className={s.heroFlowers} />
            <p className={s.heroKicker}>The Wedding of</p>
            <h1 className={s.heroNames}>{bride}{groom && <> <em>&amp;</em> {groom}</>}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="bunting" className={s.divider} />,
          node: <Art name="flowers" />,
          amp: <Art name="flowers" />,
          portrait: <Art name="wheel" />,
          countDecor: <Art name="balloons" className={s.countBalloons} />,
          closingDecor: <span className={s.closingField} aria-hidden />,
          closingEmblem: <Art name="bike" className={s.closingEmblem} />,
          sentArt: <Art name="balloons" />,
        }}
      />
    </ThemeShell>
  );
}
