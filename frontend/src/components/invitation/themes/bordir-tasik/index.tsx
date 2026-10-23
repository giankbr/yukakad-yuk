"use client";
// Theme "Bordir Tasik" — bordir kerancang Tasikmalaya: sampul berupa muka mukena dari voile katun putih yang tergantung
// di atas linen hijau pupus, tepi bawahnya bergerigi feston dengan lubang kerancang; foto pasangan di dalam medali
// bordir satin. Hero: foto yang ditutup ujung kain bergerigi, kartu acara bertepi tusuk jelujur dengan sulur bordir di
// sudut, hitung mundur di dalam ram sulam kayu, potret dalam bingkai oval bordir. Semua bordiran dilukis setingkat
// benang (satin timbul, tusuk tangkai, lubang feston) oleh /tmp/pen/art/themes/bordir-tasik.py.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Cormorant Upright:wght@400;600", "Sorts Mill Goudy:ital@0;1", "Mrs Saint Delafield", "Amiri"];
const Art = makeArt("bordir-tasik", {
  hem: [780, 185], oval: [543, 736], medal: [487, 491], sprig: [362, 61], bloom: [113, 111], corner: [320, 310],
} as const);

const COPY = {
  ...DEFAULT_COPY,
  opening: {
    arabic: "بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ",
    kicker: "Assalamu'alaikum Warahmatullahi Wabarakatuh",
    title: "Walimatul 'Ursy",
    intro: "Dengan memohon rahmat dan ridha Allah Subhanahu wa Ta'ala, kami bermaksud menyelenggarakan pernikahan putra-putri kami. Merupakan kehormatan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"] as [string, string],
  couple: ["dengan izin Allah", "Kedua Mempelai"] as [string, string],
  count: ["setusuk demi setusuk", "Menuju Hari Akad"] as [string, string],
  units: ["Hari", "Jam", "Menit", "Detik"] as [string, string, string, string],
  events: ["waktu & tempat", "Rangkaian Acara"] as [string, string],
  story: ["perjalanan kami", "Kisah Kami"] as [string, string],
  gallery: ["galeri", "Momen Kami"] as [string, string],
  wishes: ["doa & kehadiran", "Ucapan & Konfirmasi"] as [string, string],
  gifts: ["tanda kasih", "Amplop Digital"] as [string, string],
  closing: {
    thanks: "Hatur Nuhun",
    text: "Atas kehadiran dan doa restu Bapak/Ibu/Saudara/i, kami ucapkan terima kasih. Semoga Allah menjadikan pernikahan ini sakinah, mawaddah, wa rahmah.",
    salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh",
  },
  sent: "Hatur nuhun, doa dan ucapan Anda sudah kami terima.",
  wishPlaceholder: "Tuliskan doa terbaik untuk kedua mempelai…",
  giftIntro: "Doa restu Anda adalah hadiah terindah. Bila berkenan memberi tanda kasih, dapat melalui:",
};

export default function BordirTasikTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Walimatul 'Ursy";
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const coverPhoto = data.gallery[0] ?? data.couple.bridePhoto;
  const heroPhoto = data.gallery[1] ?? data.gallery[0] ?? data.couple.bridePhoto;
  const initials = `${data.couple.bride.slice(0, 1)}${data.couple.groom ? data.couple.groom.slice(0, 1) : ""}`;

  return (
    <ThemeShell
      fonts={FONTS}
      background="#dfe9d3"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Art name="corner" eager className={`${s.coverCorner} ${s.coverCornerL}`} />
          <Art name="corner" eager className={`${s.coverCorner} ${s.coverCornerR}`} />
          <div className={s.panel}>
            <p className={s.coverArabic} lang="ar" dir="rtl">بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ</p>
            <p className={s.coverKicker}>{label}</p>
            <div className={s.medal}>
              <div className={s.medalPhoto}>
                {coverPhoto ? <Photo src={coverPhoto} alt={`${data.couple.bride} & ${data.couple.groom}`} /> : <span className={s.medalMono} aria-hidden>{initials}</span>}
              </div>
              <span aria-hidden><Art name="medal" eager /></span>
            </div>
            <h1 className={s.coverNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#fdfcf7" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#4f6f52"
        dark="#fdfcf7"
        copy={COPY}
        hero={(
          <header className={s.hero}>
            {heroPhoto && (
              <div className={s.heroPhoto}>
                <Photo src={heroPhoto} alt={`${data.couple.bride} & ${data.couple.groom}`} />
                <span className={s.heroHem} aria-hidden />
              </div>
            )}
            <div className={s.heroBody}>
              <p className={s.heroKicker}>{label}</p>
              <h1 className={s.heroNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
              <Art name="sprig" className={s.divider} />
              <p className={s.heroDate}>{formatDate(data.date)}</p>
              {note && <p className={s.heroNote}>{note}</p>}
            </div>
          </header>
        )}
        slots={{
          divider: <Art name="sprig" className={s.divider} />,
          node: <Art name="bloom" />,
          amp: <Art name="bloom" />,
          portrait: <span className={s.ovalRim} aria-hidden><Art name="oval" /></span>,
          countDecor: null,
          closingEmblem: <Art name="bloom" className={s.closingSpray} />,
          sentArt: <Art name="bloom" />,
        }}
      />
    </ThemeShell>
  );
}
