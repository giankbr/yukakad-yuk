"use client";
// Theme "Girih Emas" — ubin girih Persia (desagon, dasi kupu-kupu, pentagon; garis Hankin 54 derajat) yang ditekan
// sebagai emas tempa di atas biru malam: medali roset girih yang berputar sangat pelan, bingkai iwan berujung lancip
// untuk foto, pita frieze, kartu gading bergaris emas ganda. Tanpa makhluk bernyawa, tanpa kaligrafi yang dilukis.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Marcellus", "EB Garamond:ital,wght@0,400;0,600;1,400", "Amiri:wght@400"];
// Painted by /tmp/pen/art/themes/girih-emas.py (tools/art/themes in the repo).
const Art = makeArt("girih-emas", {
  rosette: [440, 440], iwan: [320, 410], divider: [320, 47], bintang: [64, 67],
} as const);
const BISMILLAH = "بِسْمِ اللّٰهِ الرَّحْمٰنِ الرَّحِيْمِ";

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    arabic: BISMILLAH,
    kicker: "Assalamu'alaikum Warahmatullahi Wabarakatuh",
    title: "Dua garis yang dipertemukan Allah dalam satu pola",
    intro: "Dengan memohon rahmat dan rida Allah Subhanahu wa Ta'ala, kami bermaksud menyelenggarakan walimah pernikahan putra-putri kami. Merupakan kehormatan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"],
  couple: ["Bismillah, Kami Bersatu", "Kedua Mempelai"],
  count: ["Menghitung Hari", "Menuju Hari Akad"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Waktu & Tempat", "Rangkaian Acara"],
  story: ["Garis yang Bertemu", "Kisah Kami"],
  gallery: ["Galeri", "Potret Bahagia"],
  wishes: ["Doa & Kehadiran", "Ucapan & Konfirmasi"],
  gifts: ["Tanda Kasih", "Amplop Digital"],
  closing: {
    thanks: "Jazakumullah Khairan",
    text: "Atas kehadiran dan doa restu Bapak/Ibu/Saudara/i, kami ucapkan terima kasih. Semoga Allah merangkai rumah tangga kami seindah dan seteguh pola yang tak berujung.",
    salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh",
  },
  sent: "Jazakumullah khairan, doa dan ucapan Anda sudah terkirim.",
  wishPlaceholder: "Tuliskan doa terbaik untuk kedua mempelai…",
};

const WISHES = [
  { id: "w1", name: "Keluarga Bapak H. Syamsul Bahri", attendance: "yes" as Attendance, message: "Barakallahu lakuma wa baraka 'alaikuma wa jama'a bainakuma fi khair. Semoga menjadi keluarga sakinah, mawaddah, wa rahmah." },
  { id: "w2", name: "Tim Restorasi Masjid Pacinan", attendance: "yes" as Attendance, message: "Dari mengukur sudut ubin sampai ke pelaminan! Ikut bahagia, Laila dan Haidar. Sampai jumpa di Sasana Kriya." },
  { id: "w3", name: "Dina & Raka, Yogyakarta", attendance: "maybe" as Attendance, message: "Insyaallah kami usahakan hadir di resepsi malam. Doa terbaik dari Jogja." },
];

function initials(bride: string, groom?: string) {
  const b = bride.trim().slice(0, 1), g = groom?.trim().slice(0, 1);
  return g ? `${b}${g}` : b;
}

export default function GirihEmasTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Walimatul 'Ursy";
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const { bride, groom } = data.couple;
  const photo = data.gallery[0] ?? data.couple.bridePhoto;

  return (
    <ThemeShell
      fonts={FONTS}
      background="#060d22"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <p className={s.arabicCover} lang="ar" dir="rtl">{BISMILLAH}</p>
          <div className={s.rosetteWrap}><Art name="rosette" eager className={s.rosette} /></div>
          <p className={s.kicker}>{label}</p>
          <h1 className={s.coverNames}><span>{bride}</span>{groom && <><em>&amp;</em><span>{groom}</span></>}</h1>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.cartouche}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#0b1633" />Buka Undangan</button>
          </div>
          <span className={s.frieze} aria-hidden />
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#ecd59a"
        dark="#0b1633"
        copy={COPY}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            <div className={s.iwanBox}>
              <div className={s.heroPhoto}>
                {photo ? <Photo src={photo} alt={`${bride} & ${groom}`} /> : <span className={s.heroMono} aria-hidden>{initials(bride, groom)}</span>}
              </div>
              <Art name="iwan" className={s.heroIwan} />
            </div>
            <p className={s.heroKicker}>{label}</p>
            <h1 className={s.heroNames}>{bride}{groom && <> <em>&amp;</em> {groom}</>}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
            <span className={s.frieze} aria-hidden />
          </header>
        )}
        slots={{
          divider: <Art name="divider" className={s.divider} />,
          node: <Art name="bintang" />,
          amp: <Art name="bintang" />,
          portrait: <Art name="iwan" className={s.pIwan} />,
          closingEmblem: <Art name="rosette" className={s.closingRosette} />,
          sentArt: <Art name="bintang" />,
        }}
      />
    </ThemeShell>
  );
}
