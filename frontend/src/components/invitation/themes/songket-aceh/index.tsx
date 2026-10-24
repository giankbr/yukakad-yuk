"use client";
// Theme "Songket Aceh" — sehelai songket Aceh: benang emas ditenun di atas merah tua dan hitam. Sampul berupa kain dengan
// kepala kain pucuk rebung di atas dan bawah, badan hitam bertabur bungong emas, dan medali belah ketupat tenun; foto
// mempelai dalam bingkai belah ketupat, kartu bersudut anak tangga, pita tenun sebagai pembatas, Rumoh Aceh di penutup.
// Semua tenunan dirender per helai benang oleh /tmp/pen/art/themes/songket-aceh.py.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Prata", "Alegreya:ital,wght@0,400;0,500;0,700;1,400", "Marcellus SC", "Amiri:wght@400;700"];
const Art = makeArt("songket-aceh", { medal: [336, 340], divider: [352, 36], rumoh: [520, 412] } as const);

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    arabic: "بِسْمِ اللّٰهِ الرَّحْمٰنِ الرَّحِيْمِ",
    kicker: "Assalamu'alaikum Wr. Wb.",
    title: "Peumulia Jamee",
    sub: "Memuliakan tamu adalah adat kami",
    intro: "Dengan memohon rahmat dan ridha Allah SWT, kami bermaksud menyelenggarakan walimatul 'ursy putra-putri kami. Merupakan kehormatan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
  },
  roles: ["Dara Baro", "Linto Baro"],
  couple: ["Dua insan, satu ikatan", "Mempelai"],
  count: ["Menghitung hari", "Menuju Hari Bahagia"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Waktu & tempat", "Rangkaian Acara"],
  story: ["Sehelai demi sehelai", "Kisah Kami"],
  gallery: ["Galeri", "Potret Bahagia"],
  wishes: ["Doa & kehadiran", "Ucapan & Konfirmasi"],
  gifts: ["Tanda kasih", "Amplop Digital"],
  closing: { thanks: "Terima Kasih", text: "Kehadiran dan doa restu Bapak/Ibu/Saudara/i merupakan kehormatan dan kebahagiaan bagi kami sekeluarga.", salam: "Wassalamu'alaikum Wr. Wb." },
  sent: "Terima kasih, doa dan ucapan Anda sudah kami terima.",
  wishPlaceholder: "Tuliskan doa restu untuk dara baro dan linto baro…",
};

const WISHES = [
  { id: "w1", name: "Keluarga Tgk. Abdullah", attendance: "yes" as Attendance, message: "Barakallahu lakuma wa baraka 'alaikuma. Semoga menjadi keluarga sakinah, mawaddah, warahmah." },
  { id: "w2", name: "Rahmi & teman FK Unsyiah", attendance: "yes" as Attendance, message: "Selamat Humaira! Akhirnya ya. Sampai jumpa di Anjong Mon Mata, kami siap ramaikan." },
  { id: "w3", name: "Bang Fauzan, Lhokseumawe", attendance: "maybe" as Attendance, message: "Insyaallah menyusul kalau dinas selesai. Doa terbaik untuk Haikal dan keluarga." },
];

export default function SongketAcehTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Walimatul 'Ursy";
  const hero = data.gallery[0] ?? data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const groom = data.couple.groom?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#120b0b"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <span className={s.coverShade} aria-hidden />
          <span className={s.selvedge} aria-hidden />
          <Art name="medal" eager className={s.coverMedal} />
          <p className={s.coverArabic} lang="ar" dir="rtl">بِسْمِ اللّٰهِ الرَّحْمٰنِ الرَّحِيْمِ</p>
          <p className={s.kicker}>{label}</p>
          <h1 className={s.coverNames}>
            <span>{data.couple.bride}</span>
            {groom && <><em>dan</em><span>{groom}</span></>}
          </h1>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.guest}>
            <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
            <strong>{guestLabel(data)}</strong>
            {table && <span className={s.table}>{table}</span>}
          </div>
          <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#241008" />Buka Undangan</button>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        copy={COPY}
        demoWishes={WISHES}
        light="#ecc97e"
        dark="#191112"
        hero={(
          <header className={s.hero}>
            <p className={s.kickerHero}>{label}</p>
            <div className={s.diamond}>
              <div className={s.diamondFrame}>
                {hero ? <div className={s.heroPhoto}><Photo src={hero} alt={`${data.couple.bride} dan ${groom ?? ""}`.trim()} /></div>
                  : <div className={s.heroMonogram} aria-hidden><span>{data.couple.bride.slice(0, 1)}</span></div>}
              </div>
            </div>
            <h1 className={s.heroNames}><span>{data.couple.bride}</span>{groom && <><em>dan</em><span>{groom}</span></>}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="divider" className={s.divider} />,
          node: <Art name="medal" />,
          amp: <Art name="medal" />,
          closingEmblem: <Art name="rumoh" className={s.rumoh} />,
          sentArt: <Art name="medal" />,
        }}
      />
    </ThemeShell>
  );
}
