"use client";
// Theme "Tatreez Merah" — Islami: sulaman silang tatreez yang dirender setusuk demi setusuk di atas linen gading,
// merah tua dengan aksen hitam dan hijau. Bintang delapan, pohon saru (cemara), pita gigi gergaji, roset anyelir;
// panel dada bersulam di sampul, kartu seperti kain sampler dengan jahitan jelujur. Tanpa makhluk bernyawa, tanpa
// kaligrafi yang digambar (bismillah ditulis sebagai teks).
import { Lucide, ThemeShell, formatDate, guestLabel, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Gloock", "Literata:ital,wght@0,400;0,500;0,600;1,400", "Reem Kufi:wght@400;500;600", "Amiri:wght@400;700"];
// Stitched by /tmp/pen/art/themes/tatreez-merah.py (linen and band are CSS backgrounds)
const Art = makeArt("tatreez-merah", { panel: [616, 497], star: [120, 121], cypress: [96, 276], rose: [100, 100] } as const);
const BISMILLAH = "بِسْمِ اللّٰهِ الرَّحْمٰنِ الرَّحِيْمِ";

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    arabic: BISMILLAH,
    kicker: "Assalamu'alaikum",
    title: "Warahmatullahi Wabarakatuh",
    intro: "Dengan memohon rahmat dan ridha Allah SWT, kami bermaksud menyelenggarakan walimah pernikahan putra-putri kami. Merupakan kehormatan dan kebahagiaan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"],
  couple: ["Setusuk Demi Setusuk", "Kedua Mempelai"],
  count: ["Menghitung Hari", "Menuju Hari Akad"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Waktu & Tempat", "Rangkaian Acara"],
  story: ["Benang Perjalanan", "Kisah Kami"],
  gallery: ["Galeri", "Lembar Kenangan"],
  wishes: ["Doa & Kehadiran", "Ucapan & Konfirmasi"],
  gifts: ["Tanda Kasih", "Amplop Digital"],
  closing: {
    thanks: "Jazakumullah Khairan",
    text: "Atas kehadiran dan doa restu Bapak/Ibu/Saudara/i, kami sekeluarga mengucapkan terima kasih. Semoga Allah membalas setiap kebaikan dengan yang lebih baik.",
    salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh",
  },
  sent: "Jazakallah khairan, doa dan ucapan Anda sudah terkirim.",
  wishPlaceholder: "Tuliskan doa untuk kedua mempelai…",
  giftIntro: "Doa restu Anda adalah hadiah terindah bagi kami. Jika berkenan memberi tanda kasih, dapat melalui:",
  familyLabel: "Kami yang berbahagia",
};

const WISHES = [
  { id: "w1", name: "Ustadzah Hafsah", attendance: "yes" as Attendance, message: "Barakallahu lakuma wa baraka 'alaikuma wa jama'a bainakuma fi khair. Semoga menjadi keluarga yang saling menuntun ke surga." },
  { id: "w2", name: "Keluarga Siregar di Medan", attendance: "yes" as Attendance, message: "Alhamdulillah, ikut berbahagia. Semoga sakinah, mawaddah, warahmah, dan selalu rukun seperti benang yang saling mengikat." },
  { id: "w3", name: "Teman Kriya ITB 2016", attendance: "maybe" as Attendance, message: "Insyaallah hadir bila tidak ada halangan. Selamat Nadia dan Faris, doa terbaik dari kami semua." },
];

export default function TatreezMerahTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const { bride, groom } = data.couple;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const label = data.eventLabel ?? "Walimatul 'Ursy";

  return (
    <ThemeShell
      fonts={FONTS}
      background="#eee4cf"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <span className={s.band} aria-hidden />
          <div className={s.coverInner}>
            <div className={s.coverHead}>
              <p className={s.coverArabic} lang="ar" dir="rtl">{BISMILLAH}</p>
              <p className={s.kicker}>Undangan {label}</p>
              <h1 className={s.coverNames}><span>{bride}</span><i>&amp;</i><span>{groom}</span></h1>
              <p className={s.coverDate}>{formatDate(data.date)}</p>
            </div>
            <Art name="panel" eager className={s.coverPanel} />
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#f6efe0" />Buka Undangan</button>
          </div>
          <span className={s.band} aria-hidden />
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#f6efe0"
        dark="#2a1a17"
        copy={COPY}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            <span className={s.band} aria-hidden />
            <div className={s.sampler}>
              <Art name="cypress" />
              <div className={s.samplerText}>
                <Art name="star" />
                <p className={s.heroKicker}>Insyaallah kami menikah</p>
                <h1 className={s.heroNames}>{bride}<i>dan</i>{groom}</h1>
                <p className={s.heroDate}>{formatDate(data.date)}</p>
              </div>
              <Art name="cypress" />
            </div>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <span className={s.divider} aria-hidden><i /><Art name="star" /><i /></span>,
          node: <Art name="rose" />,
          amp: <Art name="rose" />,
          portrait: <Art name="cypress" className={s.portraitArt} />,
          countDecor: <span className={s.countDeco} aria-hidden />,
          closingDecor: <span className={s.band} aria-hidden />,
          closingEmblem: <Art name="panel" className={s.closingEmblem} />,
          sentArt: <Art name="star" />,
        }}
      />
    </ThemeShell>
  );
}
