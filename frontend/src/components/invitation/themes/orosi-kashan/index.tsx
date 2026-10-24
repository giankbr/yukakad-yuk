"use client";
// Theme "Orosi Kashan" — Islami: jendela geser orosi dari rumah tua berhalaman tengah di Kashan. Kisi kayu walnut
// berkaca merah delima, kobalt, kunyit, dan zamrud; kipas cahaya di atasnya; cahaya berwarna jatuh perlahan di lantai
// plester; halaman bata lumpur dengan kolam dangkal. Hanya arsitektur: tanpa figur, tanpa kaligrafi lukis (bismillah
// sebagai teks). Tanpa foto.
import { Lucide, ThemeShell, formatDate, guestLabel, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Prata", "Lora:ital,wght@0,400;0,700;1,400", "Amiri:wght@400"];
// Painted by /tmp/pen/art/themes/orosi-kashan.py
const Art = makeArt("orosi-kashan", { orosi: [460, 719], pane: [180, 180], divider: [320, 27], courtyard: [720, 512] } as const);
const BISMILLAH = "بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ";

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    arabic: BISMILLAH,
    kicker: "Assalamu'alaikum Warahmatullahi Wabarakatuh",
    title: "Dengan Rahmat Allah",
    intro: "Dengan memohon rahmat dan ridha Allah Subhanahu wa Ta'ala, kami bermaksud menyelenggarakan walimah pernikahan kami. Merupakan kehormatan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan mendoakan.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"],
  couple: ["Dua warna, satu cahaya", "Kedua Mempelai"],
  count: ["Matahari bergeser perlahan", "Menuju Hari Akad"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Halaman kami terbuka", "Waktu & Tempat"],
  story: ["Kaca demi kaca", "Perjalanan Kami"],
  gallery: ["Kenangan", "Galeri"],
  wishes: ["Doa untuk kami", "Doa & Konfirmasi"],
  gifts: ["Tanda kasih", "Hadiah Pernikahan"],
  closing: {
    thanks: "Jazakumullahu Khairan",
    text: "Terima kasih atas doa dan kehadiran Bapak/Ibu/Saudara/i. Semoga Allah membalas setiap kebaikan dengan cahaya dan keberkahan.",
    salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh",
  },
  sent: "Jazakallahu khairan, doa Anda sudah kami terima.",
  wishPlaceholder: "Tuliskan doa terbaik untuk kedua mempelai…",
  giftIntro: "Doa Anda adalah hadiah terbaik bagi kami. Bila berkenan berbagi tanda kasih, dapat melalui:",
};

const WISHES = [
  { id: "w1", name: "Keluarga Bapak H. Mansur", attendance: "yes" as Attendance, message: "Barakallahu lakuma wa baraka 'alaikuma wa jama'a bainakuma fi khair. Semoga rumah tangga kalian terang dan hangat." },
  { id: "w2", name: "Teman Studio Arsitektur 2017", attendance: "yes" as Attendance, message: "Akhirnya denah dan strukturnya bersatu juga! Selamat Zahra dan Fikri, semoga sakinah, mawaddah, warahmah." },
  { id: "w3", name: "Annisa Rahmawati", attendance: "maybe" as Attendance, message: "Insyaallah aku usahakan datang. Doa terbaik untuk kalian berdua, semoga selalu saling menjaga." },
];

export default function OrosiKashanTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const { bride, groom } = data.couple;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const label = data.eventLabel?.trim() || "Walimatul 'Urs";

  return (
    <ThemeShell
      fonts={FONTS}
      background="#efe2c9"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.pools} aria-hidden><span /><span /><span /><span /><span /><span /></div>
          <p className={s.coverArabic} lang="ar" dir="rtl">{BISMILLAH}</p>
          <div className={s.window} aria-hidden><Art name="orosi" eager /></div>
          <p className={s.kicker}>{label}</p>
          <h1 className={s.coverNames}>{bride}<em>&amp; {groom}</em></h1>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.guestWrap}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#f1c65a" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        noPhotos
        copy={COPY}
        demoWishes={WISHES}
        light="#f1c65a"
        dark="#2f1a0e"
        hero={(
          <header className={s.hero}>
            <span className={s.lightPool} style={{ left: "6%", top: "20%", background: "#b8233a" }} aria-hidden />
            <span className={s.lightPool} style={{ right: "4%", top: "34%", background: "#2a4fa8" }} aria-hidden />
            <div className={s.heroArch}><Art name="courtyard" /></div>
            <p className={s.heroKicker}>{label}</p>
            <h1 className={s.heroNames}>{bride}<em>&amp; {groom}</em></h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="divider" className={s.divider} />,
          node: <Art name="pane" />,
          amp: <Art name="pane" />,
          closingEmblem: <Art name="courtyard" className={s.closingScene} />,
          sentArt: <Art name="pane" />,
        }}
      />
    </ThemeShell>
  );
}
