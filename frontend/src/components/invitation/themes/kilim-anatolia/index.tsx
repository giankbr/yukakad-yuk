"use client";
// Theme "Kilim Anatolia" — pernikahan Islami bernuansa kilim tenun datar Anatolia: tenunan wol merah bata, nila, kunyit
// dan krem (celah slit-tapestry, belah ketupat bertangga, pita gigi gergaji, rumbai). Foto dalam jendela belah ketupat
// tenun, medali gul di pembuka dan penutup. Murni geometris, tanpa makhluk bernyawa, tanpa kaligrafi yang dilukis.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Reem Kufi:wght@400;500;600;700", "Vollkorn:ital,wght@0,400;0,500;0,600;1,400", "Amiri:wght@400;700"];
// Woven by /tmp/pen/art/themes/kilim-anatolia.py (tools/art/themes in the repo).
const Art = makeArt("kilim-anatolia", { frame: [480, 557], gul: [345, 370], divider: [200, 44] } as const);
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
  couple: ["Lungsin & Pakan", "Kedua Mempelai"],
  count: ["Menghitung Hari", "Menuju Hari Bahagia"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Waktu & Tempat", "Rangkaian Acara"],
  story: ["Jejak Langkah", "Kisah Kami"],
  gallery: ["Galeri", "Momen Bahagia"],
  wishes: ["Doa & Kehadiran", "Ucapan & Konfirmasi"],
  gifts: ["Tanda Kasih", "Amplop Digital"],
  closing: { thanks: "Jazakumullah Khairan", text: "Atas kehadiran dan doa restu Bapak/Ibu/Saudara/i, kami sekeluarga mengucapkan terima kasih. Semoga Allah membalas setiap kebaikan dengan yang lebih baik.", salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh" },
  sent: "Jazakallah khairan, doa dan ucapan Anda sudah terkirim.",
};

const WISHES = [
  { id: "w1", name: "Keluarga H. Irwan Nasution", attendance: "yes" as Attendance, message: "Barakallahu lakuma wa baraka 'alaikuma wa jama'a bainakuma fi khair. Selamat Zahra dan Fikri." },
  { id: "w2", name: "Teman-teman PPI Konya", attendance: "yes" as Attendance, message: "Masyaallah, dari pasar kain tua sampai pelaminan! Semoga sakinah, mawaddah, warahmah." },
  { id: "w3", name: "Bu Laila", attendance: "maybe" as Attendance, message: "Insyaallah hadir bila tidak ada halangan. Doa terbaik untuk kalian berdua." },
];

export default function KilimAnatoliaTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const cover = data.gallery[0] ?? data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#a23a24"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <span className={s.fringeTop} aria-hidden />
          <div className={s.coverWindow}>
            <div className={s.coverPhoto}>{cover ? <Photo src={cover} alt="" /> : <span aria-hidden>{data.couple.bride.slice(0, 1)}</span>}</div>
            <Art name="frame" eager />
          </div>
          <div className={s.coverPanel}>
            <p className={s.kicker}>Undangan {label}</p>
            <h1 className={s.coverNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
            <span className={s.coverRule} aria-hidden />
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#f0c86a" />Buka Undangan</button>
          </div>
          <span className={s.fringeBottom} aria-hidden />
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#f0c86a"
        dark="#2a3263"
        copy={COPY}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            <Art name="gul" className={s.heroGul} />
            <p className={s.heroKicker}>The Wedding of</p>
            <h1 className={s.heroNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="divider" className={s.divider} />,
          node: <i className={s.nodeMark} />,
          portrait: <Art name="frame" className={s.pFrame} />,
          closingEmblem: <Art name="gul" className={s.closingGul} />,
          sentArt: <Art name="gul" />,
        }}
      />
    </ThemeShell>
  );
}
