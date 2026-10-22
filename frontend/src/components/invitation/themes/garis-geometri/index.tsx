"use client";
// Theme "Garis Geometri" — editorial monokrom: pola bintang delapan Islami (pola 4.8.8, garis bertemu pada 67,5°)
// digambar dengan pena teknik tinta hitam di atas garis bantu pensil, satu aksen cat air merah bata di bintang tengah.
// Halaman putih lapang, tipografi majalah, foto hitam-putih yang berwarna saat disentuh. Tanpa makhluk bernyawa.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Instrument Serif:ital@0;1", "Hanken Grotesk:wght@400;500;600;700", "Amiri:wght@400;700"];
// Drafted by /tmp/pen/art/themes/garis-geometri.py (tools/art/themes in the repo).
const Art = makeArt("garis-geometri", { rosette: [600, 600], band: [900, 99], divider: [320, 36], star: [96, 96], corner: [320, 320] } as const);
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
  couple: ["Mempelai", "Dua Garis, Satu Pola"],
  count: ["Hitung Mundur", "Menuju Hari Akad"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Acara", "Waktu & Tempat"],
  story: ["Kisah", "Perjalanan Kami"],
  gallery: ["Galeri", "Arsip Momen"],
  wishes: ["Doa", "Ucapan & Kehadiran"],
  gifts: ["Tanda Kasih", "Amplop Digital"],
  closing: { thanks: "Terima kasih.", text: "Atas kehadiran dan doa restu Bapak/Ibu/Saudara/i, kami sekeluarga mengucapkan terima kasih. Jazakumullah khairan katsiran.", salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh" },
  sent: "Jazakallah khairan. Ucapan Anda sudah kami terima.",
};

const WISHES = [
  { id: "w1", name: "Studio Garis Arsitek", attendance: "yes" as Attendance, message: "Barakallahu lakuma. Semoga rumah tangga kalian kokoh strukturnya dan indah polanya." },
  { id: "w2", name: "Nadia Pramesti", attendance: "yes" as Attendance, message: "Akhirnya! Selamat Salsa dan Rafi, semoga sakinah, mawaddah, warahmah." },
  { id: "w3", name: "Keluarga Om Hendra", attendance: "maybe" as Attendance, message: "Insyaallah hadir bila tidak ada halangan. Doa terbaik dari Medan." },
];

export default function GarisGeometriTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const hero = data.gallery[0] ?? data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const year = data.date ? (/^(\d{4})/.exec(data.date)?.[1] ?? "") : "";

  return (
    <ThemeShell
      fonts={FONTS}
      background="#fbfaf7"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Art name="rosette" eager className={s.coverRosette} />
          <p className={s.mast}><span>Undangan</span><span>{label}</span></p>
          <p className={s.arabicCover} lang="ar" dir="rtl">{BISMILLAH}</p>
          <p className={s.kicker}>Assalamu&apos;alaikum Wr. Wb.</p>
          <p className={s.coverLabel}>Pernikahan</p>
          <h1 className={s.coverNames}>{data.couple.bride}<em>&amp; {data.couple.groom}</em></h1>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <Art name="band" eager className={s.coverBand} />
          <div className={s.guestRow}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><span>Buka Undangan</span><Lucide icon={ic.mailOpen} size={16} color="#fbfaf7" /></button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#fbfaf7"
        dark="#141414"
        copy={COPY}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            <p className={s.heroTop}><span>{label}</span><span>{year}</span></p>
            <h1 className={s.heroNames}>{data.couple.bride} <em>&amp;</em> {data.couple.groom}</h1>
            {hero && (
              <div className={s.plate}>
                <div className={s.heroPhoto}><Photo src={hero} alt="" /></div>
                <Art name="corner" className={s.plateCorner} />
              </div>
            )}
            <p className={s.caption}><span>{formatDate(data.date)}</span>{data.place && <span>{data.place.split(",")[0]}</span>}</p>
            {note && <p className={s.heroNote}>{note}</p>}
            <Art name="rosette" className={s.heroRosette} />
          </header>
        )}
        slots={{
          divider: <Art name="divider" className={s.divider} />,
          node: <Art name="star" />,
          portrait: <Art name="corner" className={s.pCorner} />,
          closingDecor: <div className={s.closingDecor} aria-hidden><Art name="corner" className={s.clA} /></div>,
          closingEmblem: <Art name="star" className={s.closingStar} />,
          sentArt: <Art name="star" />,
        }}
      />
    </ThemeShell>
  );
}
