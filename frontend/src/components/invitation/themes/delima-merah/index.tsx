"use client";
// Theme "Delima Merah" — buah, biji dan bunga delima dalam ragam hias tekstil dan keramik dunia Islam (botanis, tanpa
// figur dan tanpa kaligrafi lukis): lengkung runcing bersulur delima pada sampul, kisi ogee emas di pita merah tua,
// bingkai lengkung runcing untuk potret dan galeri, buah delima terbelah sebagai lambang.
import { Lucide, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Prata", "EB Garamond:ital,wght@0,400;0,600;0,700;1,400", "Amiri:wght@400;700"];
// Painted by /tmp/pen/art/themes/delima-merah.py.
const Art = makeArt("delima-merah", { arch: [616, 889], sprig: [440, 54], blossom: [110, 150], split: [224, 241] } as const);

const WISHES = [
  { id: "w1", name: "Ibu Hj. Fatimah Az-Zahra", attendance: "yes" as const, message: "Barakallahu lakuma wa baraka 'alaikuma wa jama'a bainakuma fi khair. Semoga menjadi keluarga sakinah, mawaddah, wa rahmah." },
  { id: "w2", name: "Teman Kajian Ar-Rahman", attendance: "yes" as const, message: "MasyaAllah, ikut bahagia. Semoga Allah mudahkan segala urusan kalian dan berkahi setiap langkah ke depan." },
  { id: "w3", name: "Keluarga Ustaz Ridwan", attendance: "maybe" as const, message: "Insyaallah kami usahakan hadir. Doa terbaik dari kami sekeluarga di Garut." },
];

export default function DelimaMerahTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#62101a"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.archBox}>
            <Art name="arch" eager className={s.archArt} />
            <div className={s.archText}>
              <p className={s.bismillah} lang="ar" dir="rtl">بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ</p>
              <p className={s.kicker}>{label}</p>
              <h1 className={s.coverNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
              <p className={s.coverDate}>{formatDate(data.date)}</p>
            </div>
          </div>
          <div className={s.coverFoot}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#62101a" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#ecd39a"
        dark="#62101a"
        demoWishes={WISHES}
        copy={{
          opening: {
            arabic: "بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ",
            kicker: "Assalamu'alaikum Warahmatullahi Wabarakatuh",
            title: "Dengan Memohon Rahmat Allah",
            intro: "Maha Suci Allah yang menciptakan makhluk-Nya berpasang-pasangan. Dengan memohon rahmat dan ridha Allah Subhanahu wa Ta'ala, kami bermaksud menyelenggarakan pernikahan putra-putri kami. Merupakan kebahagiaan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
          },
          roles: ["Mempelai Wanita", "Mempelai Pria"],
          couple: ["Dua insan, satu niat", "Kedua Mempelai"],
          count: ["Menanti hari bahagia", "Hitung Mundur"],
          units: ["Hari", "Jam", "Menit", "Detik"],
          events: ["Insyaallah dilaksanakan pada", "Waktu & Tempat"],
          story: ["Takdir yang dirajut", "Kisah Kami"],
          gallery: ["Lembar kenangan", "Galeri"],
          wishes: ["Doa dan ucapan", "Doa & Kehadiran"],
          gifts: ["Tanda kasih", "Amplop Digital"],
          closing: { thanks: "Jazakumullahu Khairan", text: "Atas kehadiran dan doa restu Bapak/Ibu/Saudara/i, kami ucapkan terima kasih. Semoga Allah membalas dengan kebaikan yang berlipat.", salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh" },
          sent: "Jazakumullahu khairan, doa Anda sudah kami terima.",
          wishPlaceholder: "Tuliskan doa terbaik untuk kedua mempelai…",
          giftIntro: "Doa restu Anda adalah hadiah terindah bagi kami. Bila berkenan memberi tanda kasih, dapat melalui:",
        }}
        hero={(
          <header className={s.hero}>
            <Art name="split" className={s.heroSplit} />
            <p className={s.heroKicker}>{label}</p>
            <h1 className={s.heroNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="sprig" className={s.divider} />,
          node: <Art name="blossom" />,
          amp: <Art name="blossom" />,
          portrait: <Art name="blossom" />,
          countDecor: <span className={s.countDecor} aria-hidden><Art name="split" /></span>,
          closingEmblem: <Art name="split" className={s.closingEmblem} />,
          sentArt: <Art name="split" />,
        }}
      />
    </ThemeShell>
  );
}
