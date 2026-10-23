"use client";
// Theme "Alpen Chalet" — gouache cerah pegunungan Alpen: langit biru dengan nama mempelai, puncak bersalju, chalet kayu
// berbalkon hati ukir dan kotak bunga geranium merah di padang bunga liar. Foto mempelai menjadi jendela chalet dengan
// daun jendela hijau dan kotak bunga; kartu acara seperti papan kayu dengan pita kotak merah-putih.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Fraunces:ital,opsz,wght,SOFT,WONK@0,9..144,400..700,0..100,0..1;1,9..144,400..700,0..100,0..1", "Figtree:ital,wght@0,400;0,600;0,700;0,800;1,400"];
// Painted by /tmp/pen/art/themes/alpen-chalet.py (tools/art/themes in the repo).
const Art = makeArt("alpen-chalet", {
  peaks: [780, 405], chalet: [780, 503], flowers: [780, 209], shutter: [110, 271], box: [400, 86], garland: [320, 36], bloom: [80, 79],
} as const);

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    kicker: "Salam hangat dari ketinggian",
    title: "Di antara padang bunga dan puncak bersalju",
    intro: "Dengan penuh sukacita, kami mengundang Bapak/Ibu/Saudara/i untuk hadir dan berbagi kebahagiaan di hari pernikahan kami. Kehadiran dan doa Anda akan membuat hari itu semakin hangat.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"],
  couple: ["Dua Pendaki, Satu Jalan", "Kedua Mempelai"],
  count: ["Menuju Puncak", "Hitung Mundur"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Waktu & Tempat", "Rangkaian Acara"],
  story: ["Jejak Langkah", "Kisah Kami"],
  gallery: ["Album", "Momen di Ketinggian"],
  wishes: ["Ucapan & Kehadiran", "Kirim Doa Terbaik"],
  gifts: ["Tanda Kasih", "Hadiah Pernikahan"],
  closing: {
    thanks: "Terima Kasih",
    text: "Kehadiran dan doa Bapak/Ibu/Saudara/i adalah hadiah terindah bagi kami. Sampai jumpa di padang bunga.",
  },
  sent: "Terima kasih, ucapan Anda sudah sampai ke pondok kami.",
  attend: { maybe: "Mungkin" },
  wishPlaceholder: "Tuliskan ucapan dan doa untuk kedua mempelai…",
  giftIntro: "Kehadiran Anda sudah lebih dari cukup. Bila ingin memberi tanda kasih, dapat melalui:",
};

const WISHES = [
  { id: "w1", name: "Komunitas Pendaki Bandung", attendance: "yes" as Attendance, message: "Dari Papandayan sampai pelaminan! Selamat Aurelia dan Kevin, semoga perjalanan berdua selalu menemukan jalur terbaik." },
  { id: "w2", name: "Tante Lanny & Om Hendra", attendance: "yes" as Attendance, message: "Selamat menempuh hidup baru. Semoga rumah tangga kalian hangat seperti pondok kayu di musim dingin." },
  { id: "w3", name: "Grace Natalia", attendance: "maybe" as Attendance, message: "Masih menunggu jadwal cuti, semoga bisa menyusul ke Lembang. Bahagia selalu, kalian berdua!" },
];

export default function AlpenChaletTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const { bride, groom } = data.couple;
  const hero = data.gallery[0] ?? data.couple.bridePhoto;

  return (
    <ThemeShell
      fonts={FONTS}
      background="#fbf7ee"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.coverText}>
            <p className={s.kicker}>{label}</p>
            <h1 className={s.coverNames}><span>{bride}</span>{groom && <><em>&amp;</em><span>{groom}</span></>}</h1>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
          </div>
          <div className={s.scene} aria-hidden>
            <Art name="peaks" eager className={s.peaks} />
            <Art name="chalet" eager className={s.chalet} />
            <Art name="flowers" eager className={s.flowers} />
          </div>
          <div className={s.coverFoot}>
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
        light="#ffffff"
        dark="#1f3a5c"
        copy={COPY}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            <div className={s.window}>
              <Art name="shutter" className={s.shutter} />
              {hero ? <div className={s.heroPhoto}><Photo src={hero} alt="" /></div> : <div className={s.heroPhoto} aria-hidden />}
              <Art name="shutter" className={`${s.shutter} ${s.shutterR}`} />
              <Art name="box" className={s.heroBox} />
            </div>
            <p className={s.heroKicker}>{label}</p>
            <h1 className={s.heroNames}>{bride}{groom && <> <em>&amp;</em> {groom}</>}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="garland" className={s.divider} />,
          node: <Art name="bloom" />,
          amp: <Art name="bloom" />,
          portrait: <Art name="box" className={s.pBox} />,
          countDecor: <Art name="peaks" className={s.countPeaks} />,
          closingDecor: <Art name="flowers" className={s.clFlowers} />,
          closingEmblem: <Art name="bloom" className={s.clEmblem} />,
          sentArt: <Art name="garland" />,
        }}
      />
    </ThemeShell>
  );
}
