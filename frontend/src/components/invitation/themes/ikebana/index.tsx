"use client";
// Theme "Ikebana" — rangkaian moribana yang lapang: ranting quince bertinta sumi, dua kuntum iris dengan daun pedang
// di kenzan, suiban keramik biru nila. Layar washi bergaris shoji, banyak ruang kosong, tipografi mincho rata kiri,
// potret seperti gulungan kakejiku; bayangan ranting bergeser pelan di layar.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Shippori Mincho:wght@400;500;600;700", "Tenor Sans"];
// Painted by /tmp/pen/art/themes/ikebana.py (washi.webp is the CSS paper texture).
const Art = makeArt("ikebana", { arrangement: [520, 780], iris: [151, 526], sprig: [360, 53] } as const);

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    kicker: "Dengan penuh syukur",
    title: "Dua Tangkai, Satu Vas",
    intro: "Seperti rangkaian yang hanya memerlukan sedikit tangkai untuk menjadi utuh, kami memulai hidup bersama dengan sederhana. Kami mengundang Bapak/Ibu/Saudara/i untuk hadir dan merayakannya bersama kami.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"],
  couple: ["Kami berdua", "Mempelai"],
  count: ["Menunggu musimnya", "Hari Pernikahan"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Waktu & tempat", "Acara"],
  story: ["Perlahan", "Cerita Kami"],
  gallery: ["Potret", "Galeri"],
  wishes: ["Kabar & ucapan", "Ucapan & Kehadiran"],
  gifts: ["Tanda kasih", "Hadiah"],
  closing: {
    thanks: "Terima Kasih",
    text: "Kehadiran dan doa Bapak/Ibu/Saudara/i adalah bunga terindah dalam rangkaian hari kami.",
  },
  sent: "Terima kasih, ucapan Anda sudah kami terima.",
  attend: { maybe: "Mungkin" },
  wishPlaceholder: "Tuliskan ucapan dan doa untuk kedua mempelai…",
  wishLabel: "Ucapan",
  giftIntro: "Kehadiran Anda sudah lebih dari cukup. Bila ingin memberi tanda kasih, dapat melalui:",
};

const WISHES = [
  { id: "w1", name: "Studio Ranting & Daun", attendance: "yes" as Attendance, message: "Selamat Kinanti dan Arya! Murid yang dulu rangkaiannya miring kini merangkai hidup bersama gurunya. Kami ikut bahagia." },
  { id: "w2", name: "Dimas Prakoso", attendance: "yes" as Attendance, message: "Selamat menempuh hidup baru. Semoga rumah kalian selalu tenang, lapang, dan penuh tawa." },
  { id: "w3", name: "Tante Wulan & Om Hadi", attendance: "maybe" as Attendance, message: "Mohon maaf kalau belum tentu bisa datang. Doa kami menyertai kalian berdua, semoga langgeng dan saling menjaga." },
];

export default function IkebanaTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const { bride, groom } = data.couple;
  const label = data.eventLabel?.trim() || "Pernikahan";
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const heroPic = data.gallery[0];

  return (
    <ThemeShell
      fonts={FONTS}
      background="#f1ebde"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.shoji} aria-hidden />
          <Art name="arrangement" eager className={s.kage} />
          <p className={s.kicker}>Undangan {label}</p>
          <h1 className={s.coverNames}>{bride}<em>dan</em>{groom}</h1>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <Art name="arrangement" eager className={s.arrangement} />
          <div className={s.guestWrap}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={15} color="#f1ebde" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        copy={COPY}
        demoWishes={WISHES}
        light="#f1ebde"
        dark="#2b2622"
        hero={(
          <header className={s.hero}>
            <div className={s.heroText}>
              <p className={s.heroKicker}>{label}</p>
              <h1 className={s.heroNames}>{bride}<em>dan</em>{groom}</h1>
              <p className={s.heroDate}>{formatDate(data.date)}</p>
              {note && <p className={s.heroNote}>{note}</p>}
            </div>
            <Art name="iris" className={s.heroIris} />
            {heroPic && <div className={s.heroPhoto}><Photo src={heroPic} alt="" /></div>}
          </header>
        )}
        slots={{
          divider: <Art name="sprig" className={s.divider} />,
          countDecor: <Art name="iris" className={s.countIris} />,
          closingDecor: <Art name="arrangement" className={s.closingArt} />,
          sentArt: <Art name="sprig" />,
        }}
      />
    </ThemeShell>
  );
}
