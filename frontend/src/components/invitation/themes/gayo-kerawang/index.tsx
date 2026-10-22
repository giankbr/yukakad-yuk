"use client";
// Theme "Gayo Kerawang" — dataran tinggi Gayo, Aceh Tengah (desain orisinal): kain hitam bersulam kerawang Gayo
// (pucuk rebung, emun berangkat, sarak opat) dengan benang merah, kuning, hijau, dan putih; ranting kopi arabika berceri
// merah; Danau Lut Tawar berkabut pagi dengan pinus di punggung bukit. Tanpa makhluk bernyawa, basmalah diketik.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Gloock", "Marcellus SC", "Gentium Book Plus:ital,wght@0,400;0,700;1,400", "Amiri:wght@400"];
// Painted by /tmp/pen/art/themes/gayo-kerawang.py (tools/art/themes in the repo).
const Art = makeArt("gayo-kerawang", { kopi: [560, 268], emblem: [220, 221], divider: [300, 41] } as const);
const BISMILLAH = "بِسْمِ اللّٰهِ الرَّحْمٰنِ الرَّحِيْمِ";

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    arabic: BISMILLAH,
    kicker: "Assalamu'alaikum Warahmatullahi Wabarakatuh",
    title: "Dari Tanoh Gayo, dengan Doa",
    intro: "Dengan memohon rahmat dan rida Allah SWT, kami bermaksud menyelenggarakan walimah pernikahan putra-putri kami. Merupakan kehormatan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"],
  couple: ["Dua Benang, Satu Sulaman", "Kedua Mempelai"],
  count: ["Menghitung Hari", "Menuju Akad"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Waktu & Tempat", "Rangkaian Acara"],
  story: ["Dari Kebun Kopi", "Kisah Kami"],
  gallery: ["Kenangan", "Galeri Foto"],
  wishes: ["Doa & Kehadiran", "Ucapan & Konfirmasi"],
  gifts: ["Tanda Kasih", "Amplop Digital"],
  closing: {
    thanks: "Terima Kasih",
    text: "Atas kehadiran dan doa restu Bapak/Ibu/Saudara/i, kami sekeluarga mengucapkan terima kasih. Semoga Allah membalas setiap kebaikan dengan berkah yang berlimpah.",
    salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh",
  },
  sent: "Jazakumullah khairan, doa dan ucapan Anda sudah terkirim.",
};

const WISHES = [
  { id: "w1", name: "Tgk. Imam Kampung Kemili", attendance: "yes" as Attendance, message: "Barakallahu lakuma wa baraka 'alaikuma wa jama'a bainakuma fi khair. Semoga menjadi keluarga sakinah, mawaddah, wa rahmah." },
  { id: "w2", name: "Kawan Koperasi Kopi Bener Meriah", attendance: "yes" as Attendance, message: "Selamat Rahmah dan Iqbal! Semoga cintanya seharum kopi Gayo yang baru disangrai. Kami datang rombongan." },
  { id: "w3", name: "Keluarga Bang Hasan, Banda Aceh", attendance: "maybe" as Attendance, message: "Insyaallah kami usahakan naik ke Takengon. Doa terbaik dari Banda Aceh." },
];

export default function GayoKerawangTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Walimatul 'Ursy";
  const hero = data.gallery[0] ?? data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#15120e"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.scene}>
            <Art name="kopi" eager className={s.coverKopi} />
            <span className={s.mistDrift} aria-hidden />
            <p className={s.arabicCover} lang="ar" dir="rtl">{BISMILLAH}</p>
            <p className={s.kicker}>Assalamu&apos;alaikum Wr. Wb.</p>
          </div>
          <div className={s.panel}>
            <span className={s.panelBand} aria-hidden />
            <p className={s.coverLabel}>Undangan {label}</p>
            <h1 className={s.coverNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#fff7e6" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#f3cf5a"
        dark="#15120e"
        copy={COPY}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            <p className={s.heroKicker}>{label}</p>
            <h1 className={s.heroNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {hero && (
              <div className={s.window}>
                <div className={s.heroPhoto}><Photo src={hero} alt="" /></div>
                <span className={s.windowBand} aria-hidden />
                <Art name="kopi" className={s.heroKopi} />
              </div>
            )}
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="divider" className={s.divider} />,
          node: <Art name="emblem" />,
          amp: <Art name="emblem" />,
          portrait: <span className={s.pBand} aria-hidden />,
          closingDecor: <div className={s.closingLake} aria-hidden><Art name="kopi" className={s.closingKopi} /></div>,
          closingEmblem: <Art name="emblem" className={s.closingEmblem} />,
          sentArt: <Art name="emblem" />,
        }}
      />
    </ThemeShell>
  );
}
