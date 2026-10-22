"use client";
// Theme "Pualam Hitam" — pernikahan Islami di atas pualam hitam Nero Marquina berurat putih, bertatah bilah kuningan:
// bintang delapan (khatam), medali oktagon berjalin yang berputar sangat pelan, bingkai foto oktagon, pita tatahan di
// setiap peralihan. Murni geometris, tanpa makhluk bernyawa, tanpa kaligrafi yang dilukis.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Italiana:wght@400", "Bellefair:wght@400", "Tenor Sans:wght@400", "Amiri:wght@400;700"];
// Rendered by /tmp/pen/art/themes/pualam-hitam.py (tools/art/themes in the repo).
const Art = makeArt("pualam-hitam", { medallion: [440, 440], frame: [360, 465], divider: [426, 54] } as const);
const BISMILLAH = "بِسْمِ اللّٰهِ الرَّحْمٰنِ الرَّحِيْمِ";

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    arabic: BISMILLAH,
    kicker: "Assalamu'alaikum",
    title: "Warahmatullahi Wabarakatuh",
    intro: "Dengan memohon rahmat dan ridha Allah SWT, kami bermaksud menyelenggarakan pernikahan putra-putri kami. Merupakan kehormatan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"],
  couple: ["Dua Hati, Satu Arah", "Kedua Mempelai"],
  count: ["Menghitung Hari", "Menuju Hari Bahagia"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Waktu & Tempat", "Rangkaian Acara"],
  story: ["Perjalanan", "Kisah Kami"],
  gallery: ["Galeri", "Momen Bahagia"],
  wishes: ["Doa & Kehadiran", "Ucapan & Konfirmasi"],
  gifts: ["Tanda Kasih", "Amplop Digital"],
  closing: { thanks: "Jazakumullah Khairan", text: "Atas kehadiran dan doa restu Bapak/Ibu/Saudara/i, kami sekeluarga mengucapkan terima kasih. Semoga Allah membalas setiap kebaikan dengan yang lebih baik.", salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh" },
  sent: "Jazakallah khairan, doa dan ucapan Anda sudah terkirim.",
};

const WISHES = [
  { id: "w1", name: "Keluarga H. Ridwan Syamsudin", attendance: "yes" as Attendance, message: "Barakallahu lakuma wa baraka 'alaikuma wa jama'a bainakuma fi khair. Selamat Nadia dan Hamzah." },
  { id: "w2", name: "Tim Studio Ruang Teduh", attendance: "yes" as Attendance, message: "Dari satu meja gambar ke satu rumah. Semoga menjadi keluarga sakinah, mawaddah, warahmah." },
  { id: "w3", name: "Om Faisal & Tante Rini", attendance: "maybe" as Attendance, message: "Insyaallah menyusul dari Medan. Doa terbaik untuk kalian berdua." },
];

export default function PualamHitamTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const cover = data.gallery[0] ?? data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#111113"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <p className={s.kicker}>Undangan {label}</p>
          <div className={s.coverWindow}>
            <div className={s.coverPhoto}>{cover ? <Photo src={cover} alt="" /> : <span aria-hidden>{data.couple.bride.slice(0, 1)}</span>}</div>
            <Art name="frame" eager />
          </div>
          <h1 className={s.coverNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <Art name="divider" className={s.coverDivider} eager />
          <div className={s.guest}>
            <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
            <strong>{guestLabel(data)}</strong>
            {table && <span className={s.table}>{table}</span>}
          </div>
          <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={15} color="#111113" />Buka Undangan</button>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#ead7a4"
        dark="#111113"
        copy={COPY}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            <div className={s.heroStage}>
              <Art name="medallion" className={s.heroMedal} />
              <div className={s.heroText}>
                <p className={s.heroKicker}>The Wedding of</p>
                <h1 className={s.heroNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
                <p className={s.heroDate}>{formatDate(data.date)}</p>
              </div>
            </div>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="divider" className={s.divider} />,
          node: <i className={s.nodeMark} />,
          portrait: <Art name="frame" className={s.pFrame} />,
          closingEmblem: <Art name="medallion" className={s.closingMedal} />,
          sentArt: <Art name="medallion" />,
        }}
      />
    </ThemeShell>
  );
}
