"use client";
// Theme "Mutiara Damaskus" — pernikahan Islami bernuansa mebel Damaskus: kayu walnut bertatah kerang mutiara, tulang,
// dan kayu aprikot (roset bintang dua belas, rantai belah ketupat), mawar damask cat air yang lembut. Foto dalam medali
// bundar bertatah, pelat mutiara yang berkilau pelan. Tanpa makhluk bernyawa, tanpa kaligrafi yang dilukis.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Della Respira:wght@400", "Castoro:ital,wght@0,400;1,400", "Marcellus SC:wght@400", "Amiri:wght@400;700"];
// Inlaid and painted by /tmp/pen/art/themes/mutiara-damaskus.py (tools/art/themes in the repo).
const Art = makeArt("mutiara-damaskus", { ring: [400, 400], rosette: [400, 400], roses: [440, 293], bud: [111, 93], divider: [300, 38] } as const);
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
  couple: ["Bertatah Satu", "Kedua Mempelai"],
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
  { id: "w1", name: "Keluarga H. Mahdi Alaydrus", attendance: "yes" as Attendance, message: "Barakallahu lakuma wa baraka 'alaikuma wa jama'a bainakuma fi khair. Selamat Salma dan Rayyan." },
  { id: "w2", name: "Syarifah Nur", attendance: "yes" as Attendance, message: "Masyaallah, cantik sekali seperti kotak mutiara itu. Semoga sakinah, mawaddah, warahmah." },
  { id: "w3", name: "Ami Faruq", attendance: "maybe" as Attendance, message: "Insyaallah hadir sepulang umrah. Doa terbaik untuk kalian berdua." },
];

export default function MutiaraDamaskusTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const cover = data.gallery[0] ?? data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#3b2416"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.medal}>
            <div className={s.medalPhoto}>{cover ? <Photo src={cover} alt="" /> : <span aria-hidden>{data.couple.bride.slice(0, 1)}</span>}</div>
            <Art name="ring" eager />
            <Art name="roses" className={s.medalRosesB} eager />
            <Art name="roses" className={s.medalRoses} eager />
          </div>
          <p className={s.kicker}>Undangan {label}</p>
          <h1 className={s.coverNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.plate}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#f0dcc4" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#f0dcc4"
        dark="#3b2416"
        copy={COPY}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            <div className={s.rosetteWrap}>
              <Art name="rosette" />
              <span className={s.rosetteGlint} aria-hidden />
            </div>
            <p className={s.heroKicker}>The Wedding of</p>
            <h1 className={s.heroNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
            <Art name="roses" className={s.heroRoses} />
          </header>
        )}
        slots={{
          divider: <Art name="divider" className={s.divider} />,
          node: <Art name="bud" />,
          amp: <Art name="bud" />,
          portrait: <Art name="ring" className={s.pRing} />,
          closingDecor: <Art name="roses" className={s.closingRoses} />,
          closingEmblem: <Art name="rosette" className={s.closingRosette} />,
          sentArt: <Art name="rosette" />,
        }}
      />
    </ThemeShell>
  );
}
