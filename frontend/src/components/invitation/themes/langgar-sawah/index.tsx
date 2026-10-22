"use client";
// Theme "Langgar Sawah" — langgar kayu kecil berpanggung di tepi sawah pada sore yang hangat (desain orisinal, cat air):
// langit keemasan, gunung biru, petak sawah dan pematang, kolam ikan di bawah langgar, pohon kelapa, dinding gedek anyaman
// bambu, atap ijuk, dan bedug serta kentongan di serambi. Tanpa makhluk bernyawa, tanpa kaligrafi yang dilukis
// (basmalah diketik).
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Alegreya:ital,wght@0,500;0,700;1,500", "Alegreya Sans:wght@400;700", "Caveat Brush", "Amiri:wght@400"];
// Painted by /tmp/pen/art/themes/langgar-sawah.py (tools/art/themes in the repo).
const Art = makeArt("langgar-sawah", { padi: [340, 78], bedug: [240, 175], kelapa: [200, 423] } as const);
const BISMILLAH = "بِسْمِ اللّٰهِ الرَّحْمٰنِ الرَّحِيْمِ";

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    arabic: BISMILLAH,
    kicker: "Assalamu'alaikum Warahmatullahi Wabarakatuh",
    title: "Dari Langgar di Tepi Sawah",
    intro: "Dengan memohon rahmat dan rida Allah SWT, kami bermaksud menyelenggarakan walimah pernikahan putra-putri kami. Merupakan kehormatan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"],
  couple: ["sepetak sawah, dua hati", "Kedua Mempelai"],
  count: ["menunggu bedug ditabuh", "Menuju Hari Akad"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["waktu & tempat", "Rangkaian Acara"],
  story: ["dari mengaji sampai ngalamar", "Kisah Kami"],
  gallery: ["kenangan", "Momen Bahagia"],
  wishes: ["doa & kehadiran", "Ucapan & Konfirmasi"],
  gifts: ["tanda kasih", "Amplop Digital"],
  closing: {
    thanks: "Hatur Nuhun",
    text: "Atas kehadiran dan doa restu Bapak/Ibu/Saudara/i, kami sekeluarga mengucapkan terima kasih. Jazakumullah khairan, semoga Allah membalas setiap kebaikan dengan panen berkah yang melimpah.",
    salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh",
  },
  sent: "Jazakumullah khairan, doa dan ucapan Anda sudah terkirim.",
};

const WISHES = [
  { id: "w1", name: "Abah Ustaz Ma'mun", attendance: "yes" as Attendance, message: "Barakallahu lakuma wa baraka 'alaikuma wa jama'a bainakuma fi khair. Muga jadi keluarga sakinah, rukun, sareng barokah." },
  { id: "w2", name: "Barudak Karang Taruna Sukaresmi", attendance: "yes" as Attendance, message: "Wilujeng Kang Asep sareng Teh Fitri! Siap bantu botram jeung nyusun korsi." },
  { id: "w3", name: "Keluarga Mang Oman, Bandung", attendance: "maybe" as Attendance, message: "Insyaallah kami usahakan pulang kampung. Doa terbaik dari Bandung." },
];

export default function LanggarSawahTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Walimatul 'Ursy";
  const hero = data.gallery[0] ?? data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#d9b97c"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.scene}>
            <span className={s.light} aria-hidden />
            <p className={s.arabicCover} lang="ar" dir="rtl">{BISMILLAH}</p>
            <p className={s.kicker}>Assalamu&apos;alaikum Wr. Wb.</p>
            <p className={s.coverLabel}>Undangan {label}</p>
            <h1 className={s.coverNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
          </div>
          <div className={s.coverFoot}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#fbf5e6" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#f6dc9a"
        dark="#3f6b2a"
        copy={COPY}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            <p className={s.heroKicker}>{label}</p>
            <h1 className={s.heroNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {hero && (
              <div className={s.postcard}>
                <div className={s.heroPhoto}><Photo src={hero} alt="" /></div>
                <Art name="padi" className={s.heroPadi} />
                <p>salam dari kampung</p>
              </div>
            )}
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="padi" className={s.divider} />,
          node: <Art name="padi" />,
          amp: <Art name="padi" />,
          portrait: <Art name="padi" className={s.pPadi} />,
          closingDecor: <div className={s.closingDecor} aria-hidden><Art name="kelapa" /><Art name="kelapa" /></div>,
          closingEmblem: <Art name="bedug" className={s.closingBedug} />,
          sentArt: <Art name="bedug" />,
        }}
      />
    </ThemeShell>
  );
}
