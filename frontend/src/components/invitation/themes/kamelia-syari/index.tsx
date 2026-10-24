"use client";
// Theme "Kamelia Syari" — syar'i, foto opsional: kertas merah muda pudar, kamelia merah muda semi-ganda dan daun hijau
// tua mengilap dalam gouache dengan benang sari emas. Sampul berupa kanopi hijau tua berpinggir renda yang menjuntaikan
// rangkaian kamelia, nama hijau tua di atas kertas; pita hijau berenda untuk hitung mundur dan penutup; potret
// berbentuk kelopak. Flora saja. Dilukis oleh /tmp/pen/art/themes/kamelia-syari.py.
import { Lucide, ThemeShell, formatDate, guestLabel, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Fraunces:ital,wght@0,500;0,600;1,500;1,600", "Alegreya:ital,wght@0,400;0,700;1,400;1,700", "Amiri"];
const Art = makeArt("kamelia-syari", { rangkaian: [860, 402], setangkai: [480, 393], bunga: [300, 266], garis: [420, 37] } as const);

const WISHES = [
  { id: "w1", name: "Ustadzah Fatimah & Keluarga", attendance: "yes" as Attendance, message: "Barakallahu lakuma wa baraka 'alaikuma wa jama'a bainakuma fii khair. Semoga menjadi keluarga sakinah, mawaddah, warahmah." },
  { id: "w2", name: "Teman Halaqah Al-Hikmah", attendance: "yes" as Attendance, message: "MasyaAllah, ikut bahagia, Kia! Semoga Allah mudahkan setiap langkah kalian dan menjadikan rumah kalian penuh berkah." },
  { id: "w3", name: "Keluarga Bapak Rahmat, Sukabumi", attendance: "maybe" as Attendance, message: "Mohon maaf bila belum bisa hadir. Doa terbaik kami dari jauh, semoga walimahnya lancar." },
];

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    arabic: "السَّلَامُ عَلَيْكُمْ وَرَحْمَةُ اللهِ وَبَرَكَاتُهُ",
    kicker: "Dengan memohon ridha Allah",
    title: "Kami Mengundang Anda",
    intro: "Dengan memohon rahmat dan ridha Allah SWT, kami bermaksud menyelenggarakan walimatul 'ursy putra-putri kami. Merupakan kehormatan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"],
  couple: ["Bismillah", "Kedua Mempelai"],
  count: ["Insyaallah", "Menuju Hari Akad"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Waktu & tempat", "Rangkaian Acara"],
  story: ["Perjalanan", "Ikhtiar Kami"],
  gallery: ["Galeri", "Kenangan"],
  wishes: ["Doa & kehadiran", "Kirim Doa"],
  gifts: ["Tanda kasih", "Amplop Digital"],
  closing: {
    thanks: "Jazakumullahu Khairan",
    text: "Atas kehadiran dan doa Bapak/Ibu/Saudara/i, kami ucapkan terima kasih. Semoga Allah membalas dengan kebaikan yang berlipat.",
    salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh",
  },
  sent: "Jazakumullahu khairan, doa Anda sudah terkirim.",
  wishPlaceholder: "Tuliskan doa untuk kedua mempelai…",
  giftIntro: "Doa Anda adalah hadiah terbaik bagi kami. Jika berkenan memberi tanda kasih, dapat melalui:",
};

export default function KameliaSyariTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel?.trim() || "Walimatul 'Ursy";
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const bride = data.couple.bride?.trim();
  const groom = data.couple.groom?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#1f4a37"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.canopy}>
            <p className={s.coverArabic} lang="ar" dir="rtl">بِسْمِ اللهِ الرَّحْمٰنِ الرَّحِيْمِ</p>
            <p className={s.coverKicker}>{label}</p>
          </div>
          <div className={s.coverBloom} aria-hidden><Art name="rangkaian" eager /></div>
          <div className={s.names}>
            <h1>{bride}</h1>
            {groom && <><span aria-hidden>&amp;</span><h1>{groom}</h1></>}
          </div>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.guest}>
            <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
            <strong>{guestLabel(data)}</strong>
            {table && <span className={s.table}>{table}</span>}
          </div>
          <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={17} color="#fff3f5" />Buka Undangan</button>
          <Art name="setangkai" className={s.coverSprig} eager />
          <Art name="setangkai" className={`${s.coverSprig} ${s.coverSprigL}`} eager />
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        copy={COPY}
        demoWishes={WISHES}
        light="#fff3f5"
        dark="#1f4a37"
        hero={(
          <header className={s.hero}>
            <Art name="setangkai" className={`${s.heroSprig} ${s.heroSprigA}`} eager />
            <Art name="setangkai" className={`${s.heroSprig} ${s.heroSprigB}`} />
            <div className={s.heroCard}>
              <p className={s.heroLabel}>{label}</p>
              <h1 className={s.heroNames}>{bride}{groom && <> <i>&amp;</i> {groom}</>}</h1>
              <p className={s.heroDate}>{formatDate(data.date)}</p>
              {note && <p className={s.heroNote}>{note}</p>}
            </div>
          </header>
        )}
        slots={{
          divider: <Art name="garis" className={s.divider} />,
          node: <Art name="bunga" />,
          portrait: <Art name="bunga" className={s.portraitArt} />,
          countDecor: <><Art name="setangkai" className={s.countDeco} /><Art name="setangkai" className={s.countDeco} /></>,
          closingEmblem: <Art name="bunga" className={s.closeBloom} />,
          sentArt: <Art name="bunga" />,
        }}
      />
    </ThemeShell>
  );
}
