"use client";
// Theme "Bunga Rampai" — walimah syar'i tanpa foto dalam cat air: bokor kuningan berisi irisan pandan, kelopak mawar,
// melati, dan cempaka; kelopak yang gugur perlahan di sampul, segel monogram merah mawar, kartu acara bertepi kerang
// seperti bibir bokor, dan amplop hijau pandan.
import { Lucide, ThemeShell, formatDate, guestLabel, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Fraunces:ital,wght@0,400;0,500;0,600;1,400;1,500", "Lora:ital,wght@0,400;0,600;1,400", "Amiri"];
// Painted by /tmp/pen/art/themes/bunga-rampai.py (kelopak and melati are CSS backgrounds of the falling petals).
const Art = makeArt("bunga-rampai", { bokor: [606, 437], cempaka: [100, 93], tabur: [271, 266], untai: [480, 44] } as const);

const WISHES = [
  { id: "w1", name: "Ummi Fatimah & Keluarga", attendance: "yes" as Attendance, message: "Barakallahu lakuma wa baraka 'alaikuma wa jama'a bainakuma fi khair. Semoga menjadi keluarga sakinah, mawaddah, warahmah." },
  { id: "w2", name: "Teman Halaqah Salma", attendance: "yes" as Attendance, message: "Masyaallah, ikut bahagia ukhti. Semoga Allah menjadikan rumah tangga kalian harum seperti bunga rampai, penuh ketaatan." },
  { id: "w3", name: "Ustadz Ridho & Keluarga", attendance: "maybe" as Attendance, message: "Insyaallah kami usahakan hadir. Doa terbaik kami untuk Hafiz dan Salma." },
];

function Fall() {
  return <div className={s.fall} aria-hidden><i /><i /><i /><i /><i /><i /></div>;
}

export default function BungaRampaiTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Walimatul 'Urs";
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const initials = [data.couple.bride, data.couple.groom].map(n => n.trim().slice(0, 1)).filter(Boolean);

  const copy: ThemeCopy = {
    ...DEFAULT_COPY,
    opening: {
      arabic: "بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيم",
      kicker: "Assalamu'alaikum Warahmatullahi Wabarakatuh",
      title: "Dengan Memohon Ridha Allah",
      intro: "Maha Suci Allah yang telah menciptakan makhluk-Nya berpasang-pasangan. Dengan memohon rahmat dan ridha-Nya, kami bermaksud menyelenggarakan walimah pernikahan putra-putri kami. Kehadiran dan doa Bapak/Ibu/Saudara/i merupakan kehormatan bagi kami.",
    },
    roles: ["Mempelai Wanita", "Mempelai Pria"],
    couple: ["Dua insan dirangkai dalam ridha-Nya", "Kedua Mempelai"],
    count: ["Menghitung hari", "Menuju Akad Suci"],
    units: ["Hari", "Jam", "Menit", "Detik"],
    events: ["Waktu & tempat", "Rangkaian Walimah"],
    story: ["Perjalanan", "Kisah Kami"],
    gallery: ["Galeri", "Momen"],
    wishes: ["Doa untuk mempelai", "Ucapan & Kehadiran"],
    gifts: ["Tanda kasih", "Amplop Digital"],
    closing: { thanks: "Jazakumullahu Khairan", text: "Atas kehadiran dan doa restu Bapak/Ibu/Saudara/i, kami ucapkan terima kasih. Semoga Allah membalas dengan kebaikan yang berlipat.", salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh" },
    sent: "Jazakallahu khairan, doa Anda sudah kami terima.",
    giftIntro: "Doa Anda adalah hadiah terindah bagi kami. Jika berkenan memberi tanda kasih, dapat melalui:",
  };

  return (
    <ThemeShell
      fonts={FONTS}
      background="#fbf5ec"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Fall />
          <Art name="tabur" eager className={s.taburTL} />
          <Art name="tabur" eager className={s.taburBR} />
          <p className={s.coverArabic} lang="ar" dir="rtl">بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيم</p>
          <p className={s.kicker}>{label}</p>
          {initials.length > 0 && <div className={s.seal} aria-hidden>{initials[0]}{initials[1] && <><span>&amp;</span>{initials[1]}</>}</div>}
          <h1 className={s.coverNames}>{data.couple.bride}<em>dan</em>{data.couple.groom}</h1>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <Art name="bokor" eager className={s.bokor} />
          <div className={s.guestWrap}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#fffbf4" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        noPhotos
        light="#f3dfb4"
        dark="#6e2532"
        copy={copy}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            <Fall />
            <Art name="bokor" className={s.heroBokor} />
            <p className={s.heroKicker}>{label}</p>
            <h1 className={s.heroNames}>{data.couple.bride} <em>&amp;</em> {data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="untai" className={s.divider} />,
          node: <Art name="cempaka" />,
          amp: <Art name="cempaka" />,
          portrait: <Art name="cempaka" className={s.portraitArt} />,
          countDecor: <><Art name="tabur" className={`${s.countTabur} ${s.countTaburL}`} /><Art name="tabur" className={`${s.countTabur} ${s.countTaburR}`} /></>,
          closingDecor: <Fall />,
          closingEmblem: <Art name="bokor" className={s.closingEmblem} />,
          sentArt: <Art name="cempaka" />,
        }}
      />
    </ThemeShell>
  );
}
