"use client";
// Theme "Anggrek Syari" — tanpa foto: anggrek bulan (puspa pesona Indonesia) putih dan ungu dalam cat air di atas krem
// bersih. Setangkai anggrek putih melengkung di atas sampul, setangkai ungu tumbuh dari bawah, dan nama ditulis di atas
// "bulan" cat air yang pucat. Monogram berlatar bulan dengan sekuntum anggrek.
import { Lucide, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Gilda Display", "Nunito Sans:ital,wght@0,400;0,600;0,700;0,800;1,400", "Pinyon Script", "Amiri"];
// Painted by /tmp/pen/art/themes/anggrek-syari.py (bulan.webp is a CSS background).
const Art = makeArt("anggrek-syari", { putih: [820, 517], ungu: [680, 475], bloom: [260, 227], divider: [440, 77] } as const);

const COPY = {
  ...DEFAULT_COPY,
  opening: {
    arabic: "بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ",
    kicker: "Assalamu'alaikum Warahmatullahi Wabarakatuh",
    title: "Bismillah",
    sub: "Dengan memohon rahmat dan ridha Allah",
    intro: "Maha Suci Allah yang menciptakan makhluk-Nya berpasang-pasangan. Dengan memohon ridha-Nya, kami bermaksud menyelenggarakan walimah pernikahan putra-putri kami. Kehadiran serta doa Bapak/Ibu/Saudara/i adalah kebahagiaan bagi kami.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"] as [string, string],
  couple: ["Atas izin Allah", "Kedua Mempelai"] as [string, string],
  count: ["Menuju hari akad", "Hitung Mundur"] as [string, string],
  units: ["Hari", "Jam", "Menit", "Detik"] as [string, string, string, string],
  events: ["Waktu & tempat", "Rangkaian Acara"] as [string, string],
  story: ["Perjalanan kami", "Menjemput Takdir"] as [string, string],
  gallery: ["Galeri", "Kenangan"] as [string, string],
  wishes: ["Doa & kehadiran", "Ucapan & Konfirmasi"] as [string, string],
  gifts: ["Tanda kasih", "Amplop Digital"] as [string, string],
  closing: {
    thanks: "Jazakumullah Khairan",
    text: "Merupakan kehormatan bagi kami atas kehadiran dan doa restu Bapak/Ibu/Saudara/i. Semoga Allah membalas setiap kebaikan dengan keberkahan.",
    salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh",
  },
  sent: "Jazakumullah khairan, doa Anda sudah kami terima.",
  wishPlaceholder: "Tuliskan doa terbaik untuk kedua mempelai…",
  familyLabel: "Kami yang berbahagia",
};

const WISHES = [
  { id: "w1", name: "Ummi Aisyah & Keluarga", attendance: "yes" as const, message: "Barakallahu lakuma wa baraka 'alaikuma wa jama'a bainakuma fi khair. Semoga menjadi keluarga sakinah, mawaddah, wa rahmah." },
  { id: "w2", name: "Akhwat Kajian Ahad Pagi", attendance: "yes" as const, message: "MasyaAllah, ikut bahagia untuk Nabila. Semoga Allah mudahkan segala urusan, sampai jumpa di walimah." },
  { id: "w3", name: "Keluarga Nasution, Medan", attendance: "maybe" as const, message: "Mohon maaf jika belum bisa hadir dari Medan. Doa terbaik kami menyertai kedua mempelai." },
];

export default function AnggrekSyariTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Walimatul 'Ursy";
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#fbf7f0"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <span className={s.coverMoon} aria-hidden />
          <Art name="putih" eager className={s.coverTop} />
          <Art name="ungu" eager className={s.coverBottom} />
          <div className={s.coverBody}>
            <p className={s.arabicTop} lang="ar" dir="rtl">بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ</p>
            <p className={s.kicker}>{label}</p>
            <h1 className={s.coverNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
            <div className={s.guestWrap}>
              <div className={s.guest}>
                <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
                <strong>{guestLabel(data)}</strong>
                {table && <span className={s.table}>{table}</span>}
              </div>
              <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#fbf3fb" />Buka Undangan</button>
            </div>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        noPhotos
        light="#fbf3fb"
        dark="#5e2a70"
        copy={COPY}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            <Art name="putih" className={s.heroSpray} />
            <p className={s.kickerDark}>{label}</p>
            <h1 className={s.heroNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="divider" className={s.divider} />,
          node: <Art name="bloom" />,
          amp: <Art name="bloom" />,
          portrait: <Art name="bloom" />,
          countDecor: <Art name="ungu" className={s.countSpray} />,
          closingEmblem: <Art name="ungu" className={s.closingSpray} />,
          sentArt: <Art name="bloom" />,
        }}
      />
    </ThemeShell>
  );
}
