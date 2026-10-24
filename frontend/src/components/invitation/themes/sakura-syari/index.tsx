"use client";
// Theme "Sakura Syari" — ranting sakura merah muda dalam cat air lembut di atas kertas krem pucat. Sampul berupa jendela
// bulan (lingkaran cat air bergaris tipis) berisi nama, ranting yang melintas di depannya, dan kelopak yang berguguran
// pelan; hero rata kiri dengan garis mawar tegak. Syar'i: tanpa foto wajib, tanpa figur, Bismillah ditata sebagai teks.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,500;0,9..144,600;1,9..144,400;1,9..144,500", "Figtree:wght@400;500;600;700", "Ephesis", "Amiri:wght@400"];
// Painted by /tmp/pen/art/themes/sakura-syari.py (petal + moon wash are also CSS backgrounds).
const Art = makeArt("sakura-syari", { branch: [760, 525], wash: [400, 408], spray: [360, 264], bloom: [160, 131], sprig: [380, 55] } as const);
const BISMILLAH = "بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ";

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    arabic: BISMILLAH,
    kicker: "Assalamu'alaikum Warahmatullahi Wabarakatuh",
    title: "Maha Suci Allah",
    intro: "Yang telah menciptakan makhluk-Nya berpasang-pasangan. Dengan memohon rahmat dan ridha Allah Subhanahu wa Ta'ala, kami bermaksud menyelenggarakan walimah pernikahan putra-putri kami. Merupakan kehormatan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan mendoakan.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"],
  couple: ["Bismillah", "Kedua Mempelai"],
  count: ["Menanti musim mekar", "Hitung Mundur"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Insyaallah", "Waktu & Tempat"],
  story: ["Perjalanan", "Kisah Kami"],
  gallery: ["Kenangan", "Galeri"],
  wishes: ["Doa & Restu", "Ucapan & Kehadiran"],
  gifts: ["Tanda Kasih", "Amplop Digital"],
  closing: {
    thanks: "Jazakumullah khairan",
    text: "Atas kehadiran dan doa restu Bapak/Ibu/Saudara/i, kami ucapkan terima kasih. Semoga Allah membalas setiap kebaikan dengan yang lebih baik.",
    salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh",
  },
  sent: "Jazakallah khairan, doa Anda sudah kami terima.",
  wishPlaceholder: "Tuliskan doa terbaik untuk kedua mempelai…",
  giftIntro: "Doa Anda adalah hadiah terindah bagi kami. Bagi yang ingin berbagi tanda kasih, dapat melalui:",
};

const WISHES = [
  { id: "w1", name: "Ustadzah Maryam & Keluarga", attendance: "yes" as const, message: "Barakallahu lakuma wa baraka 'alaikuma wa jama'a bainakuma fii khair. Semoga menjadi keluarga yang sakinah, mawaddah, wa rahmah." },
  { id: "w2", name: "Teman Kajian Remaja Al-Ukhuwwah", attendance: "yes" as const, message: "Masyaallah, ikut bahagia untuk Hanum dan Fathan. Semoga Allah mudahkan sampai hari H dan seterusnya." },
  { id: "w3", name: "Keluarga Om Hasan, Cirebon", attendance: "maybe" as const, message: "Insyaallah kami usahakan hadir. Doa terbaik dari kami sekeluarga." },
];

export default function SakuraSyariTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Walimatul 'Ursy";
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const photo = data.gallery[0];

  return (
    <ThemeShell
      fonts={FONTS}
      background="#f6e9e3"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Art name="spray" eager className={s.coverSpray} />
          <p className={s.bismillah} lang="ar" dir="rtl">{BISMILLAH}</p>
          <div className={s.moon}>
            <Art name="wash" eager className={s.moonWash} />
            <div className={s.moonText}>
              <p className={s.kicker}>{label}</p>
              <h1 className={s.coverNames}><span>{data.couple.bride}</span><em>&amp;</em><span>{data.couple.groom}</span></h1>
              <p className={s.coverDate}>{formatDate(data.date)}</p>
            </div>
          </div>
          <div className={s.coverFoot}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#ffffff" />Buka Undangan</button>
          </div>
          <Art name="branch" eager className={s.coverBranch} />
          <div className={s.petals} aria-hidden><span /><span /><span /><span /><span /><span /><span /></div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        copy={COPY}
        demoWishes={WISHES}
        light="#ffffff"
        dark="#8e3a51"
        hero={(
          <header className={s.hero}>
            <Art name="branch" className={s.heroBranch} />
            <p className={s.heroKicker}>{label}</p>
            <h1 className={s.heroNames}><span>{data.couple.bride}</span><em>&amp;</em><span>{data.couple.groom}</span></h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
            {photo && <div className={s.heroPhoto}><Photo src={photo} alt="" /></div>}
          </header>
        )}
        slots={{
          divider: <Art name="sprig" className={s.divider} />,
          node: <Art name="bloom" />,
          amp: <Art name="bloom" />,
          portrait: <Art name="bloom" className={s.portraitArt} />,
          countDecor: <><Art name="spray" className={`${s.countSpray} ${s.countSprayL}`} /><Art name="spray" className={`${s.countSpray} ${s.countSprayR}`} /></>,
          closingDecor: <><Art name="wash" className={s.closingMoon} /><Art name="spray" className={s.closingSpray} /></>,
          closingEmblem: <Art name="bloom" className={s.closingEmblem} />,
          sentArt: <Art name="bloom" />,
        }}
      />
    </ThemeShell>
  );
}
