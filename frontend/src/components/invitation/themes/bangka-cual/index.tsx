"use client";
// Theme "Bangka Cual" — tenun cual Bangka: sampul berupa kain sutra merah lembut dengan bunga tenun benang emas dan merah
// muda (tekstur tenun dilukis), tepian tumpal pucuk rebung, dan label gading yang "dijahit" di atas kain. Pantai granit
// bertoska dengan rumah panggung Melayu hanya muncul sebagai pemandangan penutup.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Gilda Display:wght@400", "Lora:ital,wght@0,400;0,500;0,600;1,400", "Pinyon Script:wght@400", "Amiri:wght@400"];
// Painted by /tmp/pen/art/themes/bangka-cual.py (cual cloth, tumpal and the beach scene are CSS backgrounds)
const Art = makeArt("bangka-cual", { kembang: [280, 280] } as const);

const WISHES = [
  { id: "w1", name: "Datuk Usman & Keluarga", attendance: "yes" as const, message: "Barakallahu lakuma wa baraka 'alaikuma. Semoga rumah tangga kalian kokoh seperti batu granit di Pantai Tikus, tenang seperti lautnya." },
  { id: "w2", name: "Kak Nadia (Sanggar Serumpun Sebalai)", attendance: "yes" as const, message: "Akhirnya! Anak-anak sanggar sudah latihan tari Campak untuk arak-arakan. Bahagia selalu, Aisyah dan Rizky." },
  { id: "w3", name: "Fikri, rekan kerja di Palembang", attendance: "maybe" as const, message: "Insyaallah menyeberang ke Bangka kalau cuti disetujui. Doa terbaik untuk kalian berdua, semoga sakinah mawaddah wa rahmah." },
];

export default function BangkaCualTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const hero = data.gallery[0] || data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const label = data.eventLabel?.trim() || "Walimatul 'Ursy";

  return (
    <ThemeShell
      fonts={FONTS}
      background="#5e1822"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <span className={s.sheen} aria-hidden />
          <div className={s.label}>
            <Art name="kembang" eager className={s.coverFlower} />
            <p className={s.bismillah} lang="ar" dir="rtl">بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيم</p>
            <p className={s.kicker}>{label}</p>
            <h1 className={s.coverNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
          </div>
          <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#5e1822" />Buka Undangan</button>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#f0d898"
        dark="#5e1822"
        demoWishes={WISHES}
        copy={{
          ...DEFAULT_COPY,
          opening: {
            arabic: "السَّلَامُ عَلَيْكُمْ وَرَحْمَةُ اللهِ وَبَرَكَاتُهُ",
            kicker: "Assalamu'alaikum Wr. Wb.",
            title: "Dengan Memohon Rahmat Allah",
            intro: "Dengan memohon rahmat dan ridha Allah SWT, kami bermaksud menyelenggarakan walimatul 'ursy putra-putri kami. Merupakan kehormatan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
          },
          roles: ["Mempelai Perempuan", "Mempelai Laki-laki"],
          couple: ["Dua Helai Benang", "Kedua Mempelai"],
          count: ["Menghitung Hari", "Menuju Hari Bahagia"],
          units: ["Hari", "Jam", "Menit", "Detik"],
          events: ["Waktu & Tempat", "Rangkaian Acara"],
          story: ["Tenunan Kisah", "Perjalanan Kami"],
          gallery: ["Galeri", "Potret Bahagia"],
          wishes: ["Doa & Kehadiran", "Ucapan & Konfirmasi"],
          gifts: ["Tanda Kasih", "Amplop Digital"],
          closing: {
            thanks: "Terima Kasih",
            text: "Kehadiran dan doa restu Bapak/Ibu/Saudara/i merupakan kebahagiaan yang tak ternilai bagi kami sekeluarga.",
            salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh",
          },
          sent: "Terima kasih, doa dan ucapan Anda sudah kami terima.",
          wishPlaceholder: "Tuliskan doa restu untuk kedua mempelai…",
          familyLabel: "Kami yang berbahagia",
        }}
        hero={(
          <header className={hero ? s.hero : `${s.hero} ${s.heroBare}`}>
            <span className={s.heroCloth} aria-hidden />
            {hero && (
              <div className={s.heroPhotoWrap}>
                <div className={s.heroPhoto}><Photo src={hero} alt={`${data.couple.bride} dan ${data.couple.groom}`} /></div>
                <Art name="kembang" className={s.heroBadge} />
              </div>
            )}
            <p className={s.heroKicker}>{label}</p>
            <h1 className={s.heroNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <span className={s.divider} aria-hidden><Art name="kembang" /></span>,
          node: <Art name="kembang" />,
          amp: <Art name="kembang" />,
          portrait: <Art name="kembang" className={s.portraitBadge} />,
          closingDecor: <span className={s.closingScene} aria-hidden />,
          closingEmblem: <Art name="kembang" className={s.closingFlower} />,
          sentArt: <Art name="kembang" />,
        }}
      />
    </ThemeShell>
  );
}
