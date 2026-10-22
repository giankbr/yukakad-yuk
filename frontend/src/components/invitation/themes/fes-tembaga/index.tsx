"use client";
// Theme "Fes Tembaga" — pernikahan Islami bernuansa riad Fes di malam hari: lentera tembaga berlubang yang dipalu,
// cahayanya pecah menjadi titik-titik bintang di dinding tadelakt saffron dan mawar, di bawah frieze kayu cedar berukir
// geometri. Potret dalam bingkai kapsul tembaga, hitung mundur pada cakram tembaga. Tanpa makhluk bernyawa, tanpa
// kaligrafi yang dilukis.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Cormorant Upright:wght@500;600;700", "Gentium Book Plus:ital,wght@0,400;0,700;1,400", "Tenor Sans", "Amiri:wght@400;700"];
// Painted by /tmp/pen/art/themes/fes-tembaga.py (tools/art/themes in the repo).
const Art = makeArt("fes-tembaga", { lantern: [260, 665], medal: [110, 110], divider: [300, 78] } as const);
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
  couple: ["Dua Cahaya", "Kedua Mempelai"],
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
  { id: "w1", name: "Keluarga H. Umar Assegaf", attendance: "yes" as Attendance, message: "Barakallahu lakuma wa baraka 'alaikuma wa jama'a bainakuma fi khair. Selamat Zahra dan Fikri." },
  { id: "w2", name: "Studio Rumah Laweyan", attendance: "yes" as Attendance, message: "Masyaallah, dari kusen tua sampai pelaminan. Semoga rumah tangganya kokoh dan hangat seperti lentera itu." },
  { id: "w3", name: "Ustadzah Rahma", attendance: "maybe" as Attendance, message: "Insyaallah hadir bila urusan di Solo selesai lebih awal. Semoga sakinah, mawaddah, warahmah." },
];

export default function FesTembagaTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const table = tableLabel(data.guestTable);
  const photo = data.gallery[0] ?? data.couple.bridePhoto;
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#26120a"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <span className={s.coverDots} aria-hidden />
          <div className={s.lanternWrap}><Art name="lantern" eager /></div>
          <p className={s.kicker}>Undangan {label}</p>
          <h1 className={s.coverNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.coverSpacer} />
          <div className={s.plate}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#ffdca0" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#ffdca0"
        dark="#26120a"
        copy={COPY}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            <p className={s.heroKicker}>The Wedding of</p>
            <h1 className={s.heroNames}>{data.couple.bride} <em>&amp;</em> {data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            <div className={s.heroFrame}>
              <div className={s.heroPhoto}>{photo ? <Photo src={photo} alt={`${data.couple.bride} & ${data.couple.groom}`} /> : <span aria-hidden>{data.couple.bride.slice(0, 1)}</span>}</div>
              <Art name="lantern" className={s.heroLantern} />
            </div>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="divider" className={s.divider} />,
          node: <Art name="medal" />,
          amp: <Art name="medal" />,
          portrait: <Art name="medal" className={s.portraitMedal} />,
          closingEmblem: <Art name="lantern" className={s.closingEmblem} />,
          sentArt: <Art name="medal" />,
        }}
      />
    </ThemeShell>
  );
}
