"use client";
// Theme "Gading Syari" — tanpa foto: kartu gading dengan bingkai ganda dari garis foil emas setipis rambut, simpul bintang
// delapan di setiap sudut, medali geometri kecil yang berputar sangat pelan, monogram dalam cincin foil, kartu acara dan
// hitung mundur berbingkai foil, serta ruang kosong yang lapang. Geometri saja, tanpa figur.
import { Lucide, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Prata", "EB Garamond:ital,wght@0,400;0,500;1,400", "Gilda Display", "Tenor Sans", "Amiri"];
// Painted by /tmp/pen/art/themes/gading-syari.py (foil and paper are CSS background tiles).
const Art = makeArt("gading-syari", { medallion: [398, 398], corner: [300, 300], divider: [502, 46] } as const);

const WISHES = [
  { id: "w1", name: "Ustadzah Fatimah & Keluarga", attendance: "yes" as const, message: "Barakallahu lakuma wa baraka 'alaikuma wa jama'a bainakuma fii khair. Semoga menjadi keluarga yang sakinah, mawaddah, warahmah." },
  { id: "w2", name: "Nabila & Fauzan", attendance: "yes" as const, message: "Alhamdulillah, ikut berbahagia. Semoga Allah mudahkan setiap langkah dan menjadikan rumah kalian penuh cahaya." },
  { id: "w3", name: "Keluarga Bapak Mahfud, Klaten", attendance: "maybe" as const, message: "Mohon maaf bila belum bisa hadir. Doa terbaik kami dari jauh, semoga walimahnya lancar dan berkah." },
];

export default function GadingSyariTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Walimatul 'Ursy";
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#f7f1e3"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <span className={s.frame} aria-hidden />
          <Art name="corner" eager className={`${s.corner} ${s.cTL}`} />
          <Art name="corner" eager className={`${s.corner} ${s.cTR}`} />
          <Art name="corner" eager className={`${s.corner} ${s.cBL}`} />
          <Art name="corner" eager className={`${s.corner} ${s.cBR}`} />
          <Art name="medallion" eager className={s.medal} />
          <p className={s.arabicTop} lang="ar" dir="rtl">بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيم</p>
          <p className={s.kicker}>{label}</p>
          <h1 className={s.coverNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
          <Art name="divider" eager className={s.coverDivider} />
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.guestWrap}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={15} color="#fbf8ef" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        noPhotos
        light="#8a6a32"
        dark="#fbf8ef"
        demoWishes={WISHES}
        copy={{
          ...DEFAULT_COPY,
          opening: {
            arabic: "السَّلَامُ عَلَيْكُمْ وَرَحْمَةُ اللهِ وَبَرَكَاتُهُ",
            kicker: "Dengan Rahmat Allah",
            title: "Kami Memohon Doa Restu",
            intro: "Dengan memohon rahmat dan ridho Allah SWT, kami bermaksud menyelenggarakan walimatul 'ursy putra-putri kami. Merupakan kehormatan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan mendoakan.",
          },
          roles: ["Mempelai Wanita", "Mempelai Pria"],
          couple: ["Bismillah", "Kedua Mempelai"],
          count: ["Menghitung Hari", "Menuju Akad"],
          units: ["Hari", "Jam", "Menit", "Detik"],
          events: ["Waktu & Tempat", "Rangkaian Acara"],
          story: ["Perjalanan", "Ikhtiar Kami"],
          gallery: ["Galeri", "Kenangan"],
          wishes: ["Doa & Kehadiran", "Kirim Doa"],
          gifts: ["Tanda Kasih", "Amplop Digital"],
          closing: {
            thanks: "Jazakumullahu Khairan",
            text: "Atas kehadiran dan doa Bapak/Ibu/Saudara/i, kami ucapkan terima kasih. Semoga Allah membalas dengan kebaikan.",
            salam: "Wassalamu'alaikum Wr. Wb.",
          },
          sent: "Jazakumullahu khairan, doa Anda sudah terkirim.",
          wishPlaceholder: "Tuliskan doa untuk kedua mempelai…",
          giftIntro: "Doa Anda adalah hadiah terbaik bagi kami. Jika berkenan memberi tanda kasih, dapat melalui:",
        }}
        hero={(
          <header className={s.hero}>
            <Art name="medallion" className={s.heroMedal} />
            <p className={s.heroKicker}>{label}</p>
            <h1 className={s.heroNames}>{data.couple.bride} <em>&amp;</em> {data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="divider" className={s.divider} />,
          node: <Art name="medallion" />,
          amp: <Art name="medallion" />,
          portrait: <Art name="medallion" className={s.portraitMedal} />,
          closingEmblem: <Art name="medallion" className={s.closingEmblem} />,
          sentArt: <Art name="medallion" />,
        }}
      />
    </ThemeShell>
  );
}
