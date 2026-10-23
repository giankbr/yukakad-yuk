"use client";
// Theme "Brokat Emas" — Islami, kain brokat marun bertenun benang emas timbul: tirai brokat berlipit diikat tali emas
// dengan rumbai, panel sutra gading, galon emas, dan bunga delima damask dalam bingkai ogee. Tanpa foto, tanpa makhluk
// bernyawa, tanpa kaligrafi yang digambar (teks Arab diketik).
import { Lucide, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Bodoni Moda:ital,wght@0,400;0,500;1,400;1,500", "Cormorant Garamond:ital,wght@0,400;0,500;0,600;1,400", "Monsieur La Doulaise", "Amiri:wght@400"];
// Painted by /tmp/pen/art/themes/brokat-emas.py.
const Art = makeArt("brokat-emas", { drape: [230, 588], tassel: [80, 277], medallion: [170, 199], divider: [260, 31] } as const);
const BISMILLAH = "بِسْمِ اللّٰهِ الرَّحْمٰنِ الرَّحِيْمِ";

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    arabic: "بَارَكَ اللّٰهُ لَكُمَا وَبَارَكَ عَلَيْكُمَا وَجَمَعَ بَيْنَكُمَا فِيْ خَيْرٍ",
    kicker: "Assalamu'alaikum Warahmatullahi Wabarakatuh",
    title: "Walimatul 'Urs",
    sub: "Semoga Allah memberkahi kalian berdua dan mengumpulkan kalian dalam kebaikan",
    intro: "Dengan memohon rahmat dan ridha Allah SWT, kami bermaksud menyelenggarakan pernikahan putra-putri kami. Merupakan kehormatan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"],
  couple: ["Dengan Izin Allah", "Kedua Mempelai"],
  count: ["Menuju Akad", "Hitung Mundur"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Waktu & Tempat", "Rangkaian Acara"],
  story: ["Perjalanan Kami", "Kisah Kami"],
  gallery: ["Galeri", "Momen Bahagia"],
  wishes: ["Doa & Kehadiran", "Ucapan & Konfirmasi"],
  gifts: ["Tanda Kasih", "Amplop Digital"],
  closing: {
    thanks: "Jazakumullah Khairan",
    text: "Merupakan kebahagiaan dan kehormatan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu. Atas kehadiran dan doanya, kami ucapkan terima kasih.",
    salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh",
  },
  sent: "Jazakumullah khairan, doa dan ucapan Anda sudah kami terima.",
};

const WISHES = [
  { id: "w1", name: "Keluarga Ustaz Hasan Basri", attendance: "yes" as const, message: "Barakallahu lakuma wa baraka 'alaikuma wa jama'a bainakuma fii khair. Semoga menjadi keluarga sakinah, mawaddah, warahmah." },
  { id: "w2", name: "Alumni Rohis Teknik ITS", attendance: "yes" as const, message: "Masyaallah, ikut bahagia! Semoga Allah mudahkan setiap langkah kalian berdua menuju jannah-Nya." },
  { id: "w3", name: "Tante Mariam & Keluarga, Gresik", attendance: "maybe" as const, message: "Insyaallah kami usahakan hadir. Doa terbaik untuk Nadhira dan Rayyan, semoga berkah dunia akhirat." },
];

export default function BrokatEmasTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const groom = data.couple.groom?.trim();
  const names = <><span>{data.couple.bride}</span>{groom && <><em>&amp;</em><span>{groom}</span></>}</>;

  return (
    <ThemeShell
      fonts={FONTS}
      background="#24040c"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Art name="drape" eager className={`${s.drape} ${s.drapeL}`} />
          <Art name="drape" eager className={`${s.drape} ${s.drapeR}`} />
          <Art name="tassel" eager className={`${s.tassel} ${s.tasselL}`} />
          <Art name="tassel" eager className={`${s.tassel} ${s.tasselR}`} />
          <div className={s.card}>
            <span className={s.cardMedalBg} aria-hidden />
            <Art name="medallion" eager className={s.cardMedal} />
            <p className={s.coverArabic} lang="ar" dir="rtl">{BISMILLAH}</p>
            <p className={s.kicker}>Walimatul &apos;Urs</p>
            <h1 className={s.coverNames}>{names}</h1>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
            <Art name="divider" eager className={s.coverDivider} />
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#f0d58e" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        noPhotos
        demoWishes={WISHES}
        light="#f0d58e"
        dark="#5a1023"
        copy={COPY}
        hero={(
          <header className={s.hero}>
            <Art name="medallion" className={s.heroMedal} />
            <p className={s.heroKicker}>Undangan {label}</p>
            <h1 className={s.heroNames}>{names}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="divider" className={s.divider} />,
          node: <Art name="medallion" />,
          amp: <Art name="divider" />,
          closingDecor: <><Art name="drape" className={`${s.closeDrape} ${s.closeDrapeL}`} /><Art name="drape" className={`${s.closeDrape} ${s.closeDrapeR}`} /></>,
          closingEmblem: <Art name="medallion" className={s.closingEmblem} />,
          sentArt: <Art name="medallion" />,
        }}
      />
    </ThemeShell>
  );
}
