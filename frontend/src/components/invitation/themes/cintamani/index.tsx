"use client";
// Theme "Cintamani" — sarung bantal (yastık) Utsmani dari sutra gading: motif cintamani (tiga bola dan sepasang
// gelombang) dari beludru merah delima berpinggiran benang emas. Sampul berupa yastık dengan panel lengkung di kedua
// ujung dan kartusa lonjong di tengah; hero berupa panel beludru dengan medali; tanpa foto mempelai dan tanpa figur.
// Tekstil dirender oleh /tmp/pen/art/themes/cintamani.py.
import { Lucide, ThemeShell, formatDate, guestLabel, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,500;0,9..144,600;1,9..144,400;1,9..144,600", "EB Garamond:ital,wght@0,400;0,500;1,400", "Tenor Sans", "Amiri:wght@400;700"];
const Art = makeArt("cintamani", { motif: [300, 329], border: [480, 44] } as const);

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    arabic: "بِسْمِ اللّٰهِ الرَّحْمٰنِ الرَّحِيْمِ",
    kicker: "Assalamu'alaikum Wr. Wb.",
    title: "Dengan Rahmat Allah",
    sub: "kami mengundang dengan penuh hormat",
    intro: "Maha Suci Allah yang menciptakan makhluk-Nya berpasang-pasangan. Dengan memohon ridha-Nya, kami bermaksud menyelenggarakan walimatul 'ursy putra-putri kami. Kehadiran dan doa Bapak/Ibu/Saudara/i adalah kehormatan bagi kami.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"],
  couple: ["Dua jiwa", "Kedua Mempelai"],
  count: ["Menanti hari", "Menuju Akad"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Waktu & tempat", "Rangkaian Acara"],
  story: ["Perjalanan", "Kisah Kami"],
  gallery: ["Galeri", "Lembar Kenangan"],
  wishes: ["Doa & kehadiran", "Ucapan & Konfirmasi"],
  gifts: ["Tanda kasih", "Amplop Digital"],
  closing: { thanks: "Jazakumullah Khairan", text: "Atas kehadiran dan doa restu Bapak/Ibu/Saudara/i, kami ucapkan terima kasih. Semoga Allah membalas kebaikan Anda.", salam: "Wassalamu'alaikum Wr. Wb." },
  sent: "Jazakumullah khairan, doa Anda sudah kami terima.",
  wishPlaceholder: "Tuliskan doa terbaik untuk kedua mempelai…",
};

const WISHES = [
  { id: "w1", name: "Keluarga Ustadz Hanif", attendance: "yes" as Attendance, message: "Barakallahu lakuma wa baraka 'alaikuma wa jama'a bainakuma fi khair. Semoga sakinah, mawaddah, warahmah." },
  { id: "w2", name: "Nadia, teman kuliah Sejarah", attendance: "yes" as Attendance, message: "Safiya! Ternyata motif cintamani skripsimu jadi undangan juga. Bahagia selalu berdua." },
  { id: "w3", name: "Tim Laboratorium Ilham", attendance: "maybe" as Attendance, message: "Insyaallah kami usahakan hadir. Selamat menempuh hidup baru, semoga langgeng." },
];

export default function CintamaniTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Walimatul 'Ursy";
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const groom = data.couple.groom?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#2c0a10"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <span className={s.coverSheen} aria-hidden />
          <div className={s.cartouche}>
            <Art name="motif" eager className={s.coverMotif} />
            <p className={s.kicker}>{label}</p>
            <h1 className={s.coverNames}>
              <span>{data.couple.bride}</span>
              {groom && <><em>&amp;</em><span>{groom}</span></>}
            </h1>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
          </div>
          <div className={s.guest}>
            <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
            <strong>{guestLabel(data)}</strong>
            {table && <span className={s.table}>{table}</span>}
          </div>
          <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#ead08a" />Buka Undangan</button>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        copy={COPY}
        demoWishes={WISHES}
        noPhotos
        light="#ead08a"
        dark="#4a0711"
        hero={(
          <header className={s.hero}>
            <p className={s.kickerHero}>{label}</p>
            <div className={s.medallion}><Art name="motif" /></div>
            <h1 className={s.heroNames}><span>{data.couple.bride}</span>{groom && <><em>&amp;</em><span>{groom}</span></>}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="border" className={s.divider} />,
          node: <Art name="motif" />,
          amp: <Art name="motif" />,
          closingEmblem: <Art name="motif" className={s.closingMotif} />,
          sentArt: <Art name="motif" />,
        }}
      />
    </ThemeShell>
  );
}
