"use client";
// Theme "Toko Roti" — toko roti klasik yang hangat dan jenaka: tenda bergaris berlekuk, papan nama cokelat, etalase kayu
// berisi kue bertingkat, makaron, roti, croissant dan label harga kapur, kotak kue berpita tali merah-putih dengan label
// kraft berisi nama tamu. Semua lukisan gouache orisinal, tanpa merek. Salam netral untuk pasangan lintas latar.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Cherry Swash:wght@400;700", "Karla:ital,wght@0,400;0,500;0,700;0,800;1,400", "Gochi Hand"];
// Painted by /tmp/pen/art/themes/toko-roti.py.
const Art = makeArt("toko-roti", {
  awning: [780, 166], window: [680, 567], box: [320, 193], cake: [300, 291], croissant: [140, 80], divider: [380, 62],
} as const);

const WISHES = [
  { id: "w1", name: "Tante Lina & Om Robert", attendance: "yes" as const, message: "Selamat menempuh hidup baru, Anya dan Gilang! Semoga rumah kalian selalu wangi roti hangat dan penuh tawa." },
  { id: "w2", name: "Geng Pelanggan Jam Enam", attendance: "yes" as const, message: "Dari antre roti tawar sampai pelaminan. Kami datang, dan kami mau kotak kuenya dua!" },
  { id: "w3", name: "Mbak Sinta", attendance: "maybe" as const, message: "Semoga bisa mampir sepulang kerja. Bahagia selalu, ya. Resepnya dijaga baik-baik." },
];

export default function TokoRotiTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const { couple } = data;
  const table = tableLabel(data.guestTable);
  const label = data.eventLabel ?? "Pernikahan";
  const heroPhoto = data.gallery[0] ?? couple.bridePhoto ?? couple.groomPhoto;
  const note = couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#9cc5a1"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Art name="awning" eager className={s.awning} />
          <div className={s.sign}>
            <p className={s.kicker}>Undangan {label}</p>
            <h1 className={s.coverNames}>{couple.bride} <i>&amp;</i> {couple.groom}</h1>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
          </div>
          <Art name="window" eager className={s.window} />
          <div className={s.coverFoot}>
            <div className={s.parcel}>
              <Art name="box" eager className={s.boxArt} />
              <div className={s.guest}>
                <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
                <strong>{guestLabel(data)}</strong>
                {table && <span className={s.table}>{table}</span>}
              </div>
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={18} color="#ffffff" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#fde3a0"
        dark="#5a3826"
        demoWishes={WISHES}
        copy={{
          opening: {
            kicker: "Halo, sahabat dan keluarga!",
            title: "Selamat Datang di Toko Kami",
            sub: "Ada kabar hangat, baru keluar dari oven",
            intro: "Dengan penuh syukur dan sukacita, kami mengundang Bapak/Ibu/Saudara/i untuk hadir dan merayakan hari pernikahan kami. Kehadiran dan doa restu Anda adalah bahan terbaik dalam resep kebahagiaan kami.",
          },
          roles: ["Mempelai Wanita", "Mempelai Pria"],
          couple: ["Si pembuat & si pencicip", "Kedua Mempelai"],
          count: ["Oven sedang dipanaskan", "Menuju Hari Bahagia"],
          units: ["Hari", "Jam", "Menit", "Detik"],
          events: ["Catat di buku pesanan", "Waktu & Tempat"],
          story: ["Resep rahasia", "Cerita Kami"],
          gallery: ["Dari etalase", "Album Manis"],
          wishes: ["Tulis di kartu ucapan", "Ucapan & Kehadiran"],
          gifts: ["Bingkisan", "Kado & Amplop Digital"],
          closing: { thanks: "Terima Kasih!", text: "Terima kasih sudah mampir ke toko kecil kebahagiaan kami. Sampai jumpa di meja paling hangat, ada kotak kue untuk setiap tamu." },
          sent: "Terima kasih! Ucapanmu sudah kami simpan di kotak kue.",
          attend: { maybe: "Mungkin" },
          wishPlaceholder: "Tulis ucapan dan doa terbaik untuk kami…",
          giftIntro: "Kehadiran Anda sudah jadi hadiah termanis. Bila ingin memberi tanda kasih, dapat melalui:",
          familyLabel: "Dengan hangat, kami sekeluarga",
        }}
        hero={(
          <header className={s.hero}>
            <span className={s.heroCloth} aria-hidden />
            <div className={s.heroPhoto}>
              <Photo src={heroPhoto} alt={`${couple.bride} & ${couple.groom}`} />
            </div>
            <Art name="cake" className={s.heroCake} />
            <p className={s.heroKicker}>Undangan {label}</p>
            <h1 className={s.heroNames}>{couple.bride} <i>&amp;</i> {couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="divider" className={s.divider} />,
          node: <Art name="croissant" />,
          amp: <Art name="croissant" />,
          portrait: <Art name="croissant" className={s.portraitTag} />,
          closingDecor: <Art name="awning" className={s.closingAwning} />,
          closingEmblem: <Art name="cake" className={s.closingEmblem} />,
          sentArt: <Art name="box" />,
        }}
      />
    </ThemeShell>
  );
}
