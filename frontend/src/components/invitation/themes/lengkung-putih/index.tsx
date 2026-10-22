"use client";
// Theme "Lengkung Putih" — modern syar'i in ivory: the cover is a painted corridor of white arches receding into soft
// light (slow dolly-in), every arch face inlaid with a thin gold line; cards, portraits, countdown and gifts all carry
// the same round-headed arch, and a painted arcade closes the countdown band and the page. Photo optional.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Gilda Display:wght@400", "Jost:wght@300;400;500", "Amiri:wght@400"];
// Painted by /tmp/pen/art/themes/lengkung-putih.py (lorong.webp is the cover background)
const Art = makeArt("lengkung-putih", { arkade: [640, 243], lengkung: [260, 66], bintang: [120, 120] } as const);
const BISMILLAH = "بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ";

export default function LengkungPutihTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Walimatul 'Ursy";
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const photo = data.gallery[0] || data.couple.bridePhoto || data.couple.groomPhoto;
  const hasPhotos = !!(data.couple.bridePhoto || data.couple.groomPhoto);

  return (
    <ThemeShell
      fonts={FONTS}
      background="#e9dfcf"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <span className={s.corridor} aria-hidden />
          <div className={s.coverBody}>
            <p className={s.coverAr} lang="ar" dir="rtl">{BISMILLAH}</p>
            <p className={s.kicker}>{label}</p>
            <h1 className={s.names}>{data.couple.bride}<i>dan</i>{data.couple.groom}</h1>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
          </div>
          <div className={s.guestWrap}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={15} color="#fcf9f3" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        noPhotos={!hasPhotos}
        light="#96773f"
        dark="#fcf9f3"
        copy={{
          ...DEFAULT_COPY,
          opening: {
            arabic: BISMILLAH,
            kicker: "Assalamu'alaikum Warahmatullahi Wabarakatuh",
            title: label,
            intro: "Maha Suci Allah yang menciptakan segala sesuatu berpasang-pasangan. Dengan memohon rahmat dan ridha Allah Subhanahu wa Ta'ala, kami bermaksud menyelenggarakan walimah pernikahan putra-putri kami. Merupakan kehormatan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan mendoakan.",
          },
          roles: ["Mempelai Wanita", "Mempelai Pria"],
          couple: ["Dengan Izin Allah", "Kedua Mempelai"],
          count: ["Menuju Hari Akad", "Hitung Mundur"],
          units: ["Hari", "Jam", "Menit", "Detik"],
          events: ["Waktu & Tempat", "Rangkaian Acara"],
          story: ["Atas Takdir-Nya", "Perjalanan Kami"],
          gallery: ["Galeri", "Momen Kami"],
          wishes: ["Doa & Kehadiran", "Kirim Doa Restu"],
          gifts: ["Tanda Kasih", "Amplop Digital"],
          closing: {
            thanks: "Jazakumullahu Khairan",
            text: "Merupakan kebahagiaan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu. Semoga Allah menghimpun kita dalam kebaikan.",
            salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh",
          },
          sent: "Jazakumullahu khairan, doa Anda telah kami terima.",
          wishPlaceholder: "Tuliskan doa terbaik untuk kedua mempelai…",
          giftIntro: "Doa Bapak/Ibu/Saudara/i adalah hadiah terindah. Bila berkenan berbagi tanda kasih, dapat melalui:",
        }}
        hero={(
          <header className={s.hero}>
            <Art name="arkade" eager className={s.heroArcade} />
            <p className={s.heroKicker}>{label}</p>
            {photo ? <div className={s.heroArch}><Photo src={photo} alt={`${data.couple.bride} & ${data.couple.groom}`} /></div> : <Art name="bintang" className={s.heroStar} />}
            <h1 className={s.heroNames}>{data.couple.bride} <span>&amp;</span> {data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="lengkung" className={s.divider} />,
          node: <Art name="bintang" />,
          amp: <Art name="bintang" />,
          countDecor: <Art name="arkade" className={s.countArcade} />,
          closingDecor: <Art name="arkade" className={s.closingArcade} />,
          closingEmblem: <Art name="bintang" className={s.closingStar} />,
          sentArt: <Art name="bintang" />,
        }}
      />
    </ThemeShell>
  );
}
