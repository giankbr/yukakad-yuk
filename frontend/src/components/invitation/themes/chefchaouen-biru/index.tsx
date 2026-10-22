"use client";
// Theme "Chefchaouen Biru" — lorong kota tua bercat kapur biru (desain orisinal, dilukis guas dan cat air): tangga berundak
// bertepi kapur putih, pintu lengkung biru tua berpaku, pot geranium merah yang tergantung dan berayun pelan, dinding kapur
// biru berlapis di atas kapur putih. Lengkung pintu jadi bingkai foto, kartu, dan galeri. Tanpa makhluk bernyawa, tanpa
// kaligrafi yang dilukis (basmalah diketik).
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["El Messiri:wght@400;600", "Spectral:ital,wght@0,400;0,600;1,400", "Italianno", "Amiri:wght@400"];
// Painted by /tmp/pen/art/themes/chefchaouen-biru.py (tools/art/themes in the repo).
const Art = makeArt("chefchaouen-biru", { lorong: [640, 900], pintu: [360, 512], pot: [150, 194], divider: [340, 68] } as const);
const BISMILLAH = "بِسْمِ اللّٰهِ الرَّحْمٰنِ الرَّحِيْمِ";

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    arabic: BISMILLAH,
    kicker: "Assalamu'alaikum Warahmatullahi Wabarakatuh",
    title: "Setiap Lorong Punya Jalan Pulang",
    intro: "Dengan memohon rahmat dan rida Allah SWT, kami bermaksud menyelenggarakan walimah pernikahan putra-putri kami. Merupakan kehormatan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"],
  couple: ["bertemu di tangga biru", "Kedua Mempelai"],
  count: ["menghitung anak tangga", "Menuju Hari Akad"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["waktu & tempat", "Rangkaian Acara"],
  story: ["lorong demi lorong", "Kisah Kami"],
  gallery: ["jendela kenangan", "Momen Bahagia"],
  wishes: ["doa & kehadiran", "Ucapan & Konfirmasi"],
  gifts: ["tanda kasih", "Amplop Digital"],
  closing: {
    thanks: "Jazakumullah Khairan",
    text: "Atas kehadiran dan doa restu Bapak/Ibu/Saudara/i, kami sekeluarga mengucapkan terima kasih. Semoga Allah membalas setiap kebaikan dengan rumah yang teduh dan pintu rezeki yang lapang.",
    salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh",
  },
  sent: "Jazakumullah khairan, doa dan ucapan Anda sudah terkirim.",
};

const WISHES = [
  { id: "w1", name: "Ustazah Maryam", attendance: "yes" as Attendance, message: "Barakallahu lakuma wa baraka 'alaikuma wa jama'a bainakuma fi khair. Semoga menjadi rumah yang selalu terbuka bagi ilmu dan kebaikan." },
  { id: "w2", name: "Alumni Program Studi Rabat 2023", attendance: "yes" as Attendance, message: "Yang dulu tersesat di tangga biru akhirnya menemukan arah! Mabruk, Hana dan Rasyid." },
  { id: "w3", name: "Keluarga Bang Ucok, Medan", attendance: "maybe" as Attendance, message: "Insyaallah kami terbang ke Jakarta bila tiket aman. Doa terbaik dari Medan." },
];

export default function ChefchaouenBiruTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Walimatul 'Ursy";
  const hero = data.gallery[0] ?? data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#e6eef4"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <p className={s.arabicCover} lang="ar" dir="rtl">{BISMILLAH}</p>
          <p className={s.kicker}>Assalamu&apos;alaikum Wr. Wb.</p>
          <div className={s.archWin}>
            <div><span className={s.alley} aria-hidden /></div>
            <Art name="pot" eager className={s.coverPot} />
            <Art name="pot" eager className={s.coverPot} />
          </div>
          <p className={s.coverLabel}>Undangan {label}</p>
          <h1 className={s.coverNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.coverFoot}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#1d2c46" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#f6f9fb"
        dark="#24508f"
        copy={COPY}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            <p className={s.heroKicker}>{label}</p>
            <h1 className={s.heroNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {hero && (
              <div className={s.door}>
                <div className={s.heroPhoto}><Photo src={hero} alt="" /></div>
                <span className={s.doorFrame}><Art name="pintu" /></span>
                <Art name="pot" className={s.heroPot} />
              </div>
            )}
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="divider" className={s.divider} />,
          node: <Art name="pot" />,
          amp: <Art name="pot" />,
          portrait: <Art name="pot" className={s.pPot} />,
          countDecor: <><Art name="pot" className={s.countPot} /><Art name="pot" className={s.countPot} /></>,
          closingDecor: <div className={s.closingScene} aria-hidden><Art name="lorong" /></div>,
          sentArt: <Art name="pot" />,
        }}
      />
    </ThemeShell>
  );
}
