"use client";
// Theme "Rumi Seljuk" — ornamen Seljuk Anatolia, tanpa figur dan tanpa kaligrafi lukis. Sampul berupa medan ubin
// bintang-dan-salib berglasir kobalt-pirus; di tengahnya portal batu kapur berlengkung runcing dengan pita sulur rumi
// berukir, nama di dalam relung, dan anak tangga batu. Halaman: jendela berlengkung runcing untuk foto di bawah strip ubin,
// medali rumi berglasir, hitung mundur di ubin bintang delapan, acara sebagai prasasti batu berpita ukir.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Gilda Display", "Gentium Book Plus:ital,wght@0,400;0,700;1,400", "Tenor Sans", "Amiri:wght@400;700"];
// Painted by /tmp/pen/art/themes/rumi-seljuk.py
const Art = makeArt("rumi-seljuk", { arch: [680, 532], medallion: [300, 300], divider: [360, 48] } as const);

const WISHES = [
  { id: "w1", name: "Ustadzah Rahmah & Keluarga", attendance: "yes" as const, message: "Barakallahu lakuma wa baraka 'alaikuma wa jama'a bainakuma fii khair. Semoga menjadi keluarga sakinah, mawaddah, wa rahmah." },
  { id: "w2", name: "Teman Studio Arsitektur", attendance: "yes" as const, message: "Akhirnya dua tukang gambar ubin bersatu! Semoga rumah tangganya kokoh seperti portal batu dan indah seperti glasirnya." },
  { id: "w3", name: "Keluarga Bapak Hasyim", attendance: "maybe" as const, message: "Mohon maaf bila belum dapat hadir. Doa terbaik kami untuk Kamila dan Faruq, semoga Allah mudahkan segala urusan." },
];

export default function RumiSeljukTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Walimatul 'Ursy";
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#13265c"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.portal}>
            <Art name="arch" eager className={s.arch} />
            <div className={s.portalBody}>
              <p className={s.basmalah} lang="ar" dir="rtl">بِسْمِ اللّٰهِ الرَّحْمٰنِ الرَّحِيْمِ</p>
              <p className={s.kicker}>{label}</p>
              <h1 className={s.coverNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
              <Art name="divider" eager className={s.coverDivider} />
              <p className={s.coverDate}>{formatDate(data.date)}</p>
              <Art name="medallion" eager className={s.coverMedal} />
              <div className={s.guestBox}>
                <div className={s.guest}>
                  <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
                  <strong>{guestLabel(data)}</strong>
                  {table && <span className={s.table}>{table}</span>}
                </div>
                <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#ffffff" />Buka Undangan</button>
              </div>
            </div>
            <span className={s.step0} aria-hidden />
            <span className={s.step1} aria-hidden />
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#a6ddd4"
        dark="#1f3c8c"
        demoWishes={WISHES}
        copy={{
          ...DEFAULT_COPY,
          opening: {
            arabic: "بِسْمِ اللّٰهِ الرَّحْمٰنِ الرَّحِيْمِ",
            kicker: "Assalamu'alaikum Warahmatullahi Wabarakatuh",
            title: "Walimatul 'Ursy",
            intro: "Dengan memohon rahmat dan ridho Allah SWT, kami bermaksud menyelenggarakan pernikahan putra-putri kami. Merupakan kehormatan dan kebahagiaan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
          },
          roles: ["Mempelai Wanita", "Mempelai Pria"],
          couple: ["Dengan Ridho Allah", "Kedua Mempelai"],
          count: ["Menuju Akad", "Hitung Mundur"],
          units: ["Hari", "Jam", "Menit", "Detik"],
          events: ["Waktu & Tempat", "Rangkaian Acara"],
          story: ["Perjalanan", "Kisah Kami"],
          gallery: ["Galeri", "Potret Bahagia"],
          wishes: ["Doa & Kehadiran", "Ucapan & Konfirmasi"],
          gifts: ["Tanda Kasih", "Hadiah Pernikahan"],
          closing: {
            thanks: "Jazakumullah Khairan",
            text: "Merupakan suatu kebahagiaan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
            salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh",
          },
          sent: "Jazakumullah khairan, doa dan ucapan Anda telah kami terima.",
          wishPlaceholder: "Tuliskan doa untuk kedua mempelai…",
        }}
        hero={(
          <header className={s.hero}>
            <span className={s.heroTiles} aria-hidden />
            <div className={s.heroWindow}>
              {data.gallery[0] ? <div className={s.heroPhoto}><Photo src={data.gallery[0]} alt="" /></div> : <div className={s.heroEmpty} aria-hidden />}
            </div>
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
          portrait: <Art name="medallion" className={s.portraitMedal} />,
          closingEmblem: <Art name="medallion" className={s.closingMedal} />,
          sentArt: <Art name="medallion" />,
        }}
      />
    </ThemeShell>
  );
}
