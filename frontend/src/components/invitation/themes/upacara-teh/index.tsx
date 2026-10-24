"use client";
// Theme "Upacara Teh" — upacara teh Jepang yang tenang: dinding shoji berkisi kayu, gulungan kakejiku berbingkai kain
// matcha berisi nama, satu kamelia dalam vas seladon, dan lantai tatami dengan ketel besi, mangkuk matcha, pengaduk
// bambu, sendok, dan wadah lak (garis sumi + cat air). Uap tipis naik pelan; cap merah berinisial. Netral.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Shippori Mincho:wght@500;600;700", "Zen Kaku Gothic New:wght@400;500;700"];
// Painted by /tmp/pen/art/themes/upacara-teh.py (tatami + washi are CSS background tiles).
const Art = makeArt("upacara-teh", { tea: [760, 214], flower: [170, 513], steam: [80, 384], stroke: [360, 21], bowl: [120, 72], whisk: [70, 162] } as const);

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    kicker: "Salam hangat",
    title: "Satu Pertemuan, Satu Kesempatan",
    sub: "ichi-go ichi-e",
    intro: "Seperti tuan rumah yang menyiapkan teh untuk tamunya dengan sepenuh hati, kami ingin menyambut Bapak/Ibu/Saudara/i di hari pernikahan kami. Kehadiran dan doa restu Anda adalah kehormatan bagi kami.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"],
  couple: ["Tuan Rumah", "Kedua Mempelai"],
  count: ["Air mulai dijerang", "Hitung Mundur"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Jamuan", "Waktu & Tempat"],
  story: ["Perlahan", "Kisah Kami"],
  gallery: ["Kenangan", "Galeri"],
  wishes: ["Buku Tamu", "Ucapan & Kehadiran"],
  gifts: ["Tanda Kasih", "Hadiah"],
  closing: { thanks: "Terima Kasih", text: "Semoga setiap pertemuan kita, sekecil apa pun, selalu terasa hangat seperti semangkuk teh yang disajikan dengan tulus." },
  sent: "Terima kasih, ucapan Anda sudah kami terima dengan hangat.",
  attend: { maybe: "Mungkin" },
  wishPlaceholder: "Tuliskan ucapan dan doa untuk kedua mempelai…",
  giftIntro: "Kehadiran Anda adalah hadiah terbaik. Bagi yang ingin memberi tanda kasih, dapat melalui:",
};

const WISHES = [
  { id: "w1", name: "Komunitas Teh Sabtu Sore", attendance: "yes" as const, message: "Dari teman sekelas yang dulu menyaksikan Arya menjatuhkan pengaduk berkali-kali: selamat, semoga rumah kalian selalu tenang dan hangat." },
  { id: "w2", name: "Ibu Sri Handayani", attendance: "yes" as const, message: "Selamat menempuh hidup baru, Nadia dan Arya. Semoga saling sabar dan saling menjaga." },
  { id: "w3", name: "Tante Wulan & Om Felix", attendance: "maybe" as const, message: "Kami usahakan datang dari Surabaya. Doa terbaik kami untuk kalian berdua." },
];

export default function UpacaraTehTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const photo = data.gallery[0];
  const seal = `${data.couple.bride.trim().charAt(0)}${data.couple.groom?.trim().charAt(0) ?? ""}`;

  return (
    <ThemeShell
      fonts={FONTS}
      background="#e6dfcd"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.room}>
            <div className={s.scroll}>
              <span className={s.cord} aria-hidden />
              <div className={s.paper}>
                <p className={s.kicker}>{label}</p>
                <h1 className={s.coverNames}><span>{data.couple.bride}</span><em>&amp;</em><span>{data.couple.groom}</span></h1>
                <Art name="stroke" eager className={s.coverStroke} />
                <p className={s.coverDate}>{formatDate(data.date)}</p>
                {seal && <span className={s.seal} aria-hidden>{seal}</span>}
              </div>
            </div>
            <Art name="flower" eager className={s.coverFlower} />
          </div>
          <div className={s.floor}>
            <div className={s.teaset} aria-hidden>
              <Art name="steam" eager className={`${s.steam} ${s.steam1}`} />
              <Art name="steam" eager className={`${s.steam} ${s.steam2}`} />
              <Art name="tea" eager />
            </div>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#fbf8ef" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        copy={COPY}
        demoWishes={WISHES}
        light="#f4f1e2"
        dark="#3d4c1d"
        hero={(
          <header className={s.hero}>
            <p className={s.heroSide}>{label}</p>
            <h1 className={s.heroNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <Art name="stroke" className={s.heroStroke} />
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
            <div className={s.tray} aria-hidden><Art name="bowl" /><Art name="whisk" /></div>
            {photo && <div className={s.heroPhoto}><Photo src={photo} alt="" /></div>}
          </header>
        )}
        slots={{
          divider: <Art name="stroke" className={s.divider} />,
          node: <Art name="bowl" />,
          amp: <Art name="whisk" />,
          closingEmblem: <Art name="flower" className={s.closingFlower} />,
          closingDecor: <div className={s.closingFloor} aria-hidden><Art name="tea" /></div>,
          sentArt: <Art name="bowl" />,
        }}
      />
    </ThemeShell>
  );
}
