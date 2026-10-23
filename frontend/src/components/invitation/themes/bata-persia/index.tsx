"use client";
// Theme "Bata Persia" — Islami, bata banna'i Persia: dinding bata krem bersusun dengan kisi belah ketupat dari ujung bata
// berglasir pirus dan kobalt (pola geometri murni, tanpa kaligrafi dan tanpa figur), lengkung runcing berplester dengan
// cincin voussoir dan bintang ubin di spandrel. Kartu acara beratap lengkung runcing, monogram dalam relung bata.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Reem Kufi:wght@400;500;600", "Gentium Book Plus:ital,wght@0,400;0,700;1,400", "Amiri:wght@400"];
// Painted by /tmp/pen/art/themes/bata-persia.py (tile.webp and band.webp are CSS backgrounds)
const Art = makeArt("bata-persia", { arch: [540, 720], panel: [220, 220], divider: [280, 45], star: [96, 96] } as const);
const BISMILLAH = "بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ";

export default function BataPersiaTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const { bride, groom } = data.couple;
  const table = tableLabel(data.guestTable);
  const heroSrc = data.gallery[0] || data.couple.bridePhoto || data.couple.groomPhoto;
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#f3e8d6"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.archWrap}>
            <Art name="arch" eager />
            <div className={s.archText}>
              <p className={s.bism} lang="ar" dir="rtl">{BISMILLAH}</p>
              <p className={s.kicker}>{data.eventLabel ?? "Walimatul 'Ursy"}</p>
              <h1 className={s.coverNames}><span>{bride}</span><i>&amp;</i><span>{groom}</span></h1>
              <Art name="star" className={s.coverStar} eager />
              <p className={s.coverDate}>{formatDate(data.date)}</p>
            </div>
          </div>
          <div className={s.plinth}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#fbf5ea" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#f0dfc2"
        dark="#183466"
        demoWishes={[
          { id: "w1", name: "Keluarga Dr. H. Hasan Assegaf", attendance: "yes", message: "Barakallahu lakuma wa baraka 'alaikuma wa jama'a bainakuma fi khair. Semoga menjadi keluarga sakinah, mawaddah, wa rahmah." },
          { id: "w2", name: "Teman studio Arsitektur ITS", attendance: "yes", message: "Akhirnya proyek terbesar kalian dimulai! Semoga rumah tangganya kokoh seperti dinding bata Isfahan." },
          { id: "w3", name: "Ustazah Rahmah", attendance: "maybe", message: "Insyaallah hadir bila tidak ada halangan. Doa terbaik untuk Zahra dan Farhan." },
        ]}
        copy={{
          ...DEFAULT_COPY,
          opening: {
            arabic: BISMILLAH,
            kicker: "Assalamu'alaikum Warahmatullahi Wabarakatuh",
            title: "Dengan Memohon Rahmat Allah",
            intro: "Dengan memohon rahmat dan rida Allah Subhanahu wa Ta'ala, kami bermaksud menyelenggarakan pernikahan putra-putri kami. Merupakan kehormatan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
          },
          roles: ["Mempelai Wanita", "Mempelai Pria"],
          couple: ["Bata demi Bata", "Kedua Mempelai"],
          count: ["Menuju Hari Akad", "Hitung Mundur"],
          units: ["Hari", "Jam", "Menit", "Detik"],
          events: ["Waktu & Tempat", "Rangkaian Acara"],
          story: ["Perjalanan Kami", "Kisah Kami"],
          gallery: ["Galeri", "Momen Bersama"],
          wishes: ["Doa Restu", "Ucapan & Kehadiran"],
          gifts: ["Tanda Kasih", "Amplop Digital"],
          closing: {
            thanks: "Jazakumullah Khairan",
            text: "Kehadiran dan doa restu Bapak/Ibu/Saudara/i merupakan kehormatan dan kebahagiaan bagi kami sekeluarga.",
            salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh",
          },
          sent: "Jazakumullah khairan, doa dan ucapan Anda sudah terkirim.",
        }}
        hero={(
          <header className={s.hero}>
            <p className={s.heroKicker}>Insyaallah kami menikah</p>
            <div className={s.heroFrame}>
              <div className={s.heroPhoto}>{heroSrc ? <Photo src={heroSrc} alt={`${bride} & ${groom}`} /> : <div />}</div>
              <Art name="star" className={s.heroCorner} />
              <Art name="star" className={s.heroCorner} />
              <Art name="star" className={s.heroCorner} />
              <Art name="star" className={s.heroCorner} />
            </div>
            <h1 className={s.heroNames}>{bride} <i>&amp;</i> {groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <span className={s.divider} aria-hidden><Art name="divider" /></span>,
          node: <Art name="star" />,
          amp: <Art name="star" />,
          portrait: <Art name="star" className={s.portraitStar} />,
          closingEmblem: <Art name="panel" className={s.closingPanel} />,
          sentArt: <Art name="star" />,
        }}
      />
    </ThemeShell>
  );
}
