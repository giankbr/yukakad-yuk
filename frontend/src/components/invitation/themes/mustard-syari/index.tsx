"use client";
// Theme "Mustard Syari" — undangan syar'i yang hangat dan modern: krem, kuning mustard dan karat dengan untaian daun
// ginkgo, daun karat dan rumput kering bercat air. Cover dibuka girlanda daun yang tergantung di atas nama, kartu tamu
// duduk di atas sapuan mustard bertepi gelombang, monogram dalam karangan ginkgo, dan beberapa daun gugur perlahan.
// Tanpa figur makhluk hidup; foto opsional (monogram bila tidak ada foto).
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Zen Old Mincho:wght@400;600;700", "Work Sans:wght@400;500;600", "Mea Culpa", "Amiri"];
// Painted by /tmp/pen/art/themes/mustard-syari.py (tools/art/themes in the repo).
const Art = makeArt("mustard-syari", {
  garland: [780, 368], corner: [295, 296], wreath: [400, 415], divider: [360, 64], leaf: [96, 110],
} as const);

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    arabic: "بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ",
    kicker: "Assalamu'alaikum Warahmatullahi Wabarakatuh",
    title: "Dengan Rahmat Allah",
    intro: "Maha Suci Allah yang telah menciptakan makhluk-Nya berpasang-pasangan. Dengan memohon rahmat dan ridha-Nya, kami bermaksud menyelenggarakan walimatul 'ursy putra-putri kami. Merupakan kehormatan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan mendoakan.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"],
  couple: ["Insyaallah", "Kedua Mempelai"],
  count: ["Menuju Hari Akad", "Hitung Mundur"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Waktu & Tempat", "Rangkaian Acara"],
  story: ["Perjalanan", "Ikhtiar Kami"],
  gallery: ["Galeri", "Momen Kami"],
  wishes: ["Doa & Kehadiran", "Ucapan & Konfirmasi"],
  gifts: ["Tanda Kasih", "Amplop Digital"],
  closing: { thanks: "Jazakumullah Khairan", text: "Atas kehadiran dan doa Bapak/Ibu/Saudara/i, kami ucapkan terima kasih. Semoga Allah membalas dengan kebaikan yang berlipat.", salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh" },
  sent: "Jazakumullah khairan, doa dan ucapan Anda sudah terkirim.",
  wishPlaceholder: "Tuliskan doa untuk kedua mempelai…",
  closedNote: "Jazakumullah khairan atas doa dan perhatiannya. Ucapan masih bisa dikirim lewat form ini.",
  giftIntro: "Doa Anda adalah hadiah terindah bagi kami. Jika berkenan memberi tanda kasih, dapat melalui:",
};

const WISHES = [
  { id: "w1", name: "Ustadzah Khadijah & Keluarga", attendance: "yes" as Attendance, message: "Barakallahu lakuma wa baraka 'alaikuma wa jama'a bainakuma fi khair. Semoga menjadi keluarga sakinah, mawaddah, warahmah." },
  { id: "w2", name: "Teman Halaqah Al-Furqan", attendance: "yes" as Attendance, message: "MasyaAllah, ikut bahagia, Annisa! Semoga Allah mudahkan semuanya sampai hari akad." },
  { id: "w3", name: "Keluarga Bapak Ridwan", attendance: "maybe" as Attendance, message: "Mohon maaf bila belum bisa hadir. Doa terbaik kami untuk Hafiz dan Annisa." },
];

export default function MustardSyariTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Walimatul 'Ursy";
  const table = tableLabel(data.guestTable);
  const photo = data.gallery[0];
  const note = data.couple.note?.trim();
  const noPhotos = !data.couple.bridePhoto && !data.couple.groomPhoto;

  return (
    <ThemeShell
      fonts={FONTS}
      background="#8e3f22"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Art name="garland" className={s.garland} eager />
          <Art name="leaf" className={s.fall} />
          <Art name="leaf" className={s.fall} />
          <p className={s.coverArabic} lang="ar" dir="rtl">بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ</p>
          <p className={s.salam}>Assalamu&apos;alaikum Wr. Wb.</p>
          <p className={s.kicker}>{label}</p>
          <h1 className={s.coverNames}><span>{data.couple.bride}</span><em>&amp;</em><span>{data.couple.groom}</span></h1>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.foot}>
            <Art name="corner" className={s.corner} eager />
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#fff4e0" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#fff4e0"
        dark="#8e3f22"
        copy={COPY}
        demoWishes={WISHES}
        noPhotos={noPhotos}
        hero={(
          <header className={s.hero}>
            <p className={s.heroKicker}>{label}</p>
            <div className={s.wreathWrap}>
              <Art name="wreath" className={s.wreath} />
              {photo ? <div className={s.heroPhoto}><Photo src={photo} alt={`${data.couple.bride} & ${data.couple.groom}`} /></div> : (
                <p className={s.mono} aria-hidden><span>{data.couple.bride.slice(0, 1)}</span><i /><span>{data.couple.groom.slice(0, 1)}</span></p>
              )}
            </div>
            <h1 className={s.heroNames}>{data.couple.bride} <em>&amp;</em> {data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="divider" className={s.divider} />,
          node: <Art name="leaf" />,
          amp: <Art name="leaf" />,
          portrait: <Art name="leaf" className={s.portraitArt} />,
          countDecor: <><Art name="leaf" className={s.fall} /><Art name="leaf" className={s.fall} /></>,
          closingDecor: <Art name="corner" className={s.closingCorner} />,
          closingEmblem: <Art name="leaf" className={s.closingEmblem} />,
          sentArt: <Art name="leaf" />,
        }}
      />
    </ThemeShell>
  );
}
