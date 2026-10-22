"use client";
// Theme "Sajadah Beludru" — Islami, terinspirasi bahasa desain sajadah beludru: sampul berupa sehelai permadani dengan
// rumbai di kedua ujung, pita tepi berbordir, dan relung mihrab emas (sudut hijau tua, bunga bordir) dengan lentera
// gantung; foto dan kartu berbentuk lengkung mihrab. Tanpa figur dan tanpa kaligrafi lukis.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Gloock", "EB Garamond:ital,wght@0,400;0,500;0,600;1,400", "Amiri:wght@400;700"];
// Painted by /tmp/pen/art/themes/sajadah-beludru.py (tools/art/themes in the repo).
const Art = makeArt("sajadah-beludru", { mihrab: [632, 891], lamp: [180, 320], rosette: [172, 173] } as const);

const WISHES = [
  { id: "w1", name: "Ustadzah Rahmawati", attendance: "yes" as const, message: "Barakallahu laka wa baraka 'alaika wa jama'a bainakuma fi khair. Semoga menjadi keluarga sakinah, mawaddah, warahmah." },
  { id: "w2", name: "Keluarga Bapak H. Ridwan", attendance: "yes" as const, message: "Selamat Zahra & Fadhil. Semoga Allah mudahkan setiap langkah dan berkahi rumah tangga kalian." },
  { id: "w3", name: "Annisa & Suami", attendance: "maybe" as const, message: "Insyaallah kami usahakan hadir. Doa terbaik untuk kalian berdua." },
];

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    arabic: "بِسْمِ اللّٰهِ الرَّحْمٰنِ الرَّحِيْمِ",
    kicker: "Assalamu'alaikum Wr. Wb.",
    title: "Dengan Memohon Ridha Allah",
    intro: "Maha Suci Allah yang telah menciptakan makhluk-Nya berpasang-pasangan. Dengan memohon rahmat dan ridha-Nya, kami bermaksud menyelenggarakan pernikahan putra-putri kami. Merupakan kehormatan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"],
  couple: ["Bismillah", "Kedua Mempelai"],
  count: ["Insyaallah", "Menuju Hari Akad"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Waktu & Tempat", "Rangkaian Acara"],
  story: ["Takdir yang Indah", "Kisah Kami"],
  gallery: ["Kenangan", "Galeri"],
  wishes: ["Doa & Ucapan", "Ucapan & Kehadiran"],
  gifts: ["Tanda Kasih", "Amplop Digital"],
  closing: { thanks: "Jazakumullah Khairan", text: "Atas kehadiran dan doa restu Bapak/Ibu/Saudara/i, kami ucapkan terima kasih. Semoga Allah membalas dengan kebaikan.", salam: "Wassalamu'alaikum Wr. Wb." },
  sent: "Jazakumullah khairan, doa dan ucapan Anda sudah terkirim.",
  wishPlaceholder: "Tuliskan doa terbaik untuk kedua mempelai…",
};

function Divider() {
  return <span className={s.divider} aria-hidden><Art name="rosette" /></span>;
}

export default function SajadahBeludruTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const hero = data.gallery[0] ?? data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#2a0610"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.field2}>
            <Art name="mihrab" eager className={s.mihrab} />
            <Art name="lamp" eager className={s.lamp} />
            <div className={s.inside}>
              <p className={s.coverArabic} lang="ar" dir="rtl">بِسْمِ اللّٰهِ الرَّحْمٰنِ الرَّحِيْمِ</p>
              <p className={s.kicker}>{/walim|nikah|perni/i.test(label) ? label : `Undangan ${label}`}</p>
              <h1 className={s.coverNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
              <p className={s.coverDate}>{formatDate(data.date)}</p>
            </div>
            <div className={s.guestWrap}>
              <div className={s.guest}>
                <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
                <strong>{guestLabel(data)}</strong>
                {table && <span className={s.table}>{table}</span>}
              </div>
              <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#3c0915" />Buka Undangan</button>
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
        light="#f1dc9c"
        dark="#3c0915"
        hero={(
          <header className={s.hero}>
            {hero && (
              <div className={s.heroArch}>
                <div className={s.heroPhoto}><Photo src={hero} alt="" /></div>
                <Art name="lamp" className={s.heroLamp} />
              </div>
            )}
            <p className={s.heroKicker}>{label}</p>
            <h1 className={s.heroNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Divider />,
          node: <Art name="rosette" />,
          amp: <Art name="rosette" />,
          closingEmblem: <Art name="lamp" className={s.closingLamp} />,
          sentArt: <Art name="rosette" />,
        }}
      />
    </ThemeShell>
  );
}
