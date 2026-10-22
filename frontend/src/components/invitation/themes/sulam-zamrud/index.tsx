"use client";
// Theme "Sulam Zamrud" — syari tanpa foto: sutra hijau zamrud bersulam benang emas (tali emas couching, bintang delapan
// sulam satin, bunga satin gading & merah muda). Monogram mempelai dalam karangan daun sulaman, kartu berbingkai tali
// emas, medali sulam dengan kilau benang yang bergerak pelan. Tanpa makhluk bernyawa, tanpa kaligrafi yang dilukis.
import { Lucide, ThemeShell, formatDate, guestLabel, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Prata:wght@400", "Sorts Mill Goudy:ital,wght@0,400;1,400", "Imperial Script:wght@400", "Amiri:wght@400;700"];
// Embroidered by /tmp/pen/art/themes/sulam-zamrud.py (tools/art/themes in the repo).
const Art = makeArt("sulam-zamrud", { medallion: [480, 480], wreath: [420, 430], spray: [420, 334], divider: [320, 39], star: [96, 97] } as const);
const BISMILLAH = "بِسْمِ اللّٰهِ الرَّحْمٰنِ الرَّحِيْمِ";

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    arabic: BISMILLAH,
    kicker: "Assalamu'alaikum",
    title: "Warahmatullahi Wabarakatuh",
    intro: "Dengan memohon rahmat dan ridha Allah SWT, kami bermaksud menyelenggarakan walimah pernikahan putra-putri kami. Merupakan kehormatan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan mendoakan keberkahan.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"],
  couple: ["Dua Benang, Satu Sulaman", "Kedua Mempelai"],
  count: ["Menghitung Hari", "Menuju Hari Akad"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Waktu & Tempat", "Rangkaian Acara"],
  story: ["Perjalanan", "Kisah Kami"],
  gallery: ["Galeri", "Momen Bahagia"],
  wishes: ["Doa & Kehadiran", "Ucapan & Konfirmasi"],
  gifts: ["Tanda Kasih", "Amplop Digital"],
  closing: { thanks: "Jazakumullah Khairan", text: "Atas kehadiran dan doa Bapak/Ibu/Saudara/i, kami sekeluarga mengucapkan terima kasih. Semoga Allah membalas setiap kebaikan dengan yang lebih baik.", salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh" },
  sent: "Jazakallah khairan, doa dan ucapan Anda sudah terkirim.",
};

const WISHES = [
  { id: "w1", name: "Ustadzah Maryam", attendance: "yes" as Attendance, message: "Barakallahu lakuma wa baraka 'alaikuma wa jama'a bainakuma fi khair. Semoga menjadi keluarga yang saling menuntun ke surga." },
  { id: "w2", name: "Keluarga H. Zainal", attendance: "yes" as Attendance, message: "Alhamdulillah, ikut bahagia. Semoga sakinah, mawaddah, warahmah." },
  { id: "w3", name: "Rekan Pondok Al-Hikmah", attendance: "maybe" as Attendance, message: "Insyaallah hadir bila tidak ada halangan. Doa terbaik dari kami semua." },
];

export default function SulamZamrudTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const initials = [data.couple.bride, data.couple.groom].map(name => name?.trim().slice(0, 1)).filter(Boolean);

  return (
    <ThemeShell
      fonts={FONTS}
      background="#0f5b44"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Art name="spray" className={`${s.coverSpray} ${s.coverSprayA}`} eager />
          <Art name="spray" className={`${s.coverSpray} ${s.coverSprayB}`} eager />
          <div className={s.monoWrap}>
            <Art name="wreath" eager />
            <p className={s.mono} aria-hidden>{initials[0]}{initials[1] && <><i>&amp;</i>{initials[1]}</>}</p>
          </div>
          <p className={s.kicker}>Undangan {label}</p>
          <h1 className={s.coverNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.guestCard}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#f2dc9a" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        noPhotos
        light="#f2dc9a"
        dark="#0f5b44"
        copy={COPY}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            <div className={s.medalWrap}>
              <Art name="medallion" />
              <span className={s.medalSheen} aria-hidden />
            </div>
            <p className={s.heroKicker}>{label}</p>
            <h1 className={s.heroNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="divider" className={s.divider} />,
          node: <Art name="star" />,
          portrait: <Art name="wreath" className={s.pWreath} />,
          closingDecor: <><Art name="spray" className={s.closingSpray} /><Art name="spray" className={s.closingSpray} /></>,
          closingEmblem: <Art name="medallion" className={s.closingMedal} />,
          sentArt: <Art name="star" />,
        }}
      />
    </ThemeShell>
  );
}
