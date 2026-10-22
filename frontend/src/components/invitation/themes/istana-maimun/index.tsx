"use client";
// Theme "Istana Maimun" — pernikahan Melayu Deli kuning diraja: lengkung istana bertatah ukiran emas membingkai
// kedua mempelai di atas songket Deli, rumbai lebah bergantung di setiap ruang, istana berkubah hijau dilukis melintang
// halaman, kartu acara berbentuk lengkung. Pembuka Islami (basmalah + salam), ornamen arsitektur & flora saja.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Gilda Display", "Crimson Pro:ital,wght@0,400;0,500;0,600;1,400", "Great Vibes", "Amiri:wght@400;700"];
// Painted by /tmp/pen/art/themes/istana-maimun.py (tools/art/themes in the repo).
const Art = makeArt("istana-maimun", { arch: [360, 482], istana: [720, 364], divider: [300, 35] } as const);
const BISMILLAH = "بِسْمِ اللّٰهِ الرَّحْمٰنِ الرَّحِيْمِ";

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    arabic: BISMILLAH,
    kicker: "Assalamu'alaikum",
    title: "Warahmatullahi Wabarakatuh",
    intro: "Dengan memohon rahmat dan ridha Allah SWT, kami bermaksud menyelenggarakan majelis pernikahan putra-putri kami. Merupakan suatu kehormatan apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
  },
  roles: ["Pengantin Perempuan", "Pengantin Lelaki"],
  couple: ["Raja & Ratu Sehari", "Kedua Mempelai"],
  count: ["Menghitung Hari", "Menuju Hari Bersanding"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Waktu & Tempat", "Rangkaian Majelis"],
  story: ["Hikayat", "Kisah Kami"],
  gallery: ["Galeri", "Momen Bahagia"],
  wishes: ["Doa & Kehadiran", "Ucapan & Konfirmasi"],
  gifts: ["Tanda Kasih", "Amplop Digital"],
  closing: { thanks: "Terima Kasih", text: "Atas kehadiran dan doa restu Bapak/Ibu/Saudara/i, kami sekeluarga menghaturkan terima kasih. Semoga Allah membalas setiap kebaikan.", salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh" },
  sent: "Terima kasih, doa dan ucapan Anda sudah terkirim.",
};

const WISHES = [
  { id: "w1", name: "Datuk H. Mahmud Lubis", attendance: "yes" as Attendance, message: "Barakallahu lakuma. Semoga rumah tangga Ananda berdua sakinah, mawaddah, warahmah, dan kekal hingga ke anak cucu." },
  { id: "w2", name: "Kak Ira & Bang Rizki", attendance: "yes" as Attendance, message: "Selamat bersanding, Aini dan Fikri! Pulau Pandan jauh di tengah, semoga cinta kalian tak berubah." },
  { id: "w3", name: "Keluarga Siregar", attendance: "maybe" as Attendance, message: "Insyaallah kami hadir selepas Zuhur. Doa terbaik untuk kedua mempelai." },
];

export default function IstanaMaimunTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const hero = data.gallery[0] ?? data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#163329"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.archWrap}>
            <div className={s.archPhoto}>{hero ? <Photo src={hero} alt="" /> : null}</div>
            <span className={s.archGlow} aria-hidden data-noreveal />
            <Art name="arch" eager />
          </div>
          <p className={s.kicker}>Undangan {label}</p>
          <h1 className={s.coverNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.guestWrap}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#f3d77e" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#f3d77e"
        dark="#21463a"
        copy={COPY}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            <p className={s.heroKicker}>The Wedding of</p>
            <h1 className={s.heroNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <Art name="istana" className={s.heroIstana} />
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="divider" className={s.divider} />,
          node: <i className={s.nodeMark} />,
          amp: <Art name="divider" />,
          portrait: <Art name="arch" />,
          closingEmblem: <Art name="divider" className={s.closingDiv} />,
          closingDecor: <div className={s.closingIstana} aria-hidden><Art name="istana" /></div>,
          sentArt: <Art name="divider" />,
        }}
      />
    </ThemeShell>
  );
}
