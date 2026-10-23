"use client";
// Theme "Latte Syari" — tanpa foto, hangat seperti kopi susu. Sampul: secangkir latte dilihat dari atas (busa bertumpuk
// yang abstrak, tanpa figur) menyembul dari tepi kanan dan bergoyang pelan, nama rata kiri di sampingnya, lapisan susu,
// karamel dan espresso bergelombang di bawah. Hero espresso dengan monogram di atas busa cangkir yang berputar pelan;
// monogram mempelai di atas busa, kartu acara berbentuk mug, biji kopi di garis kisah, amplop seperti sleeve kraft.
// Semua lukisan dari /tmp/pen/art/themes/latte-syari.py.
import { Lucide, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Gloock", "Literata:ital,wght@0,400;0,600;1,400", "Ephesis", "Amiri"];
const Art = makeArt("latte-syari", {
  cup: [611, 614], mini: [332, 332], swirl: [366, 48], waves: [778, 359], beans: [175, 74], stain: [358, 331],
} as const);

const COPY = {
  ...DEFAULT_COPY,
  opening: {
    arabic: "بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ",
    kicker: "Assalamu'alaikum Warahmatullahi Wabarakatuh",
    title: "Walimatul 'Ursy",
    intro: "Dengan memohon rahmat dan ridha Allah Subhanahu wa Ta'ala, kami bermaksud menyelenggarakan pernikahan putra-putri kami. Merupakan kehormatan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"] as [string, string],
  couple: ["atas izin Allah", "Kedua Mempelai"] as [string, string],
  count: ["menanti hari", "Menuju Akad"] as [string, string],
  units: ["Hari", "Jam", "Menit", "Detik"] as [string, string, string, string],
  events: ["waktu & tempat", "Rangkaian Acara"] as [string, string],
  story: ["perjalanan", "Kisah Kami"] as [string, string],
  gallery: ["galeri", "Momen Kami"] as [string, string],
  wishes: ["doa & kehadiran", "Ucapan & Konfirmasi"] as [string, string],
  gifts: ["tanda kasih", "Amplop Digital"] as [string, string],
  closing: {
    thanks: "Jazakumullah Khairan",
    text: "Atas kehadiran dan doa restu Bapak/Ibu/Saudara/i, kami ucapkan terima kasih. Semoga Allah menjadikan pernikahan ini sakinah, mawaddah, wa rahmah.",
    salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh",
  },
  sent: "Jazakumullah khairan, doa dan ucapan Anda sudah kami terima.",
  wishPlaceholder: "Tuliskan doa terbaik untuk kedua mempelai…",
  giftIntro: "Doa restu Anda adalah hadiah terindah. Bila berkenan memberi tanda kasih, dapat melalui:",
};

export default function LatteSyariTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Walimatul 'Ursy";
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const b = data.couple.bride.slice(0, 1);
  const g = data.couple.groom?.slice(0, 1) ?? "";

  return (
    <ThemeShell
      fonts={FONTS}
      background="#efe0cb"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Art name="stain" eager className={s.coverStain} />
          <p className={s.coverArabic} lang="ar" dir="rtl">بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ</p>
          <p className={s.coverSalam}>Assalamu&apos;alaikum Wr. Wb.</p>
          <div className={s.coverCup} aria-hidden><Art name="cup" eager /></div>
          <p className={s.coverKicker}>{label}</p>
          <h1 className={s.coverNames}><span>{data.couple.bride}</span><em>&amp;</em><span>{data.couple.groom}</span></h1>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.guest}>
            <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
            <strong>{guestLabel(data)}</strong>
            {table && <span className={s.table}>{table}</span>}
          </div>
          <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#fffaf2" />Buka Undangan</button>
          <Art name="waves" eager className={s.coverWaves} />
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        noPhotos
        light="#f3dcc0"
        dark="#3b2419"
        copy={COPY}
        hero={(
          <header className={s.hero}>
            <p className={s.heroKicker}>{label}</p>
            <div className={s.heroCup} aria-hidden>
              <Art name="mini" />
              <b>{b}{g && <i>&amp;</i>}{g}</b>
            </div>
            <h1 className={s.heroNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
            <Art name="waves" className={s.heroWaves} />
          </header>
        )}
        slots={{
          divider: <Art name="swirl" className={s.divider} />,
          node: <Art name="beans" />,
          amp: <Art name="beans" />,
          portrait: <span className={s.cupArt} aria-hidden><Art name="mini" /></span>,
          closingDecor: <Art name="waves" className={s.closeWaves} />,
          closingEmblem: <Art name="mini" className={s.closeCup} />,
          sentArt: <Art name="mini" />,
        }}
      />
    </ThemeShell>
  );
}
