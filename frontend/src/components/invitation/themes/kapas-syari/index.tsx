"use client";
// Theme "Kapas Syari" — tanpa foto (foto sampul opsional): tangkai kapas kering yang merekah putih di atas linen krem.
// Sampul berupa ram sulam kayu (pemidangan) berisi kain linen tempat nama kedua mempelai seolah dijahit, setangkai
// kapas terselip di sisinya. Hero berupa label kain gantung bertali rami dengan seikat kapas di bawahnya (atau foto
// dalam bingkai bulat bila diunggah). Garis jelujur benang sebagai pemisah, mempelai dalam ram kecil, hitung mundur
// di potongan kain bergerigi, kartu acara berjahit tepi. Lembut, ringan, bersahaja.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Della Respira", "Gentium Book Plus:ital,wght@0,400;0,700;1,400", "Ephesis", "Amiri"];
// Painted by /tmp/pen/art/themes/kapas-syari.py (tools/art/themes in the repo).
const Art = makeArt("kapas-syari", {
  stem: [208, 620], spray: [360, 232], hoop: [320, 336], boll: [80, 81], sprig: [170, 44],
} as const);

const COPY = {
  ...DEFAULT_COPY,
  opening: {
    arabic: "بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ",
    kicker: "Assalamu'alaikum Warahmatullahi Wabarakatuh",
    title: "Walimatul 'Ursy",
    intro: "Dengan memohon rahmat dan ridha Allah Subhanahu wa Ta'ala, kami bermaksud menyelenggarakan pernikahan putra-putri kami. Merupakan kehormatan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan mendoakan.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"] as [string, string],
  couple: ["dipertemukan karena Allah", "Kedua Mempelai"] as [string, string],
  count: ["menghitung hari", "Menuju Akad"] as [string, string],
  units: ["Hari", "Jam", "Menit", "Detik"] as [string, string, string, string],
  events: ["waktu & tempat", "Rangkaian Acara"] as [string, string],
  story: ["sehelai demi sehelai", "Kisah Kami"] as [string, string],
  gallery: ["galeri", "Momen Kami"] as [string, string],
  wishes: ["doa & kehadiran", "Ucapan & Konfirmasi"] as [string, string],
  gifts: ["tanda kasih", "Amplop Digital"] as [string, string],
  closing: {
    thanks: "Jazakumullah Khairan",
    text: "Atas kehadiran dan doa Bapak/Ibu/Saudara/i, kami haturkan terima kasih. Semoga Allah menjadikan pernikahan ini sakinah, mawaddah, wa rahmah.",
    salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh",
  },
  sent: "Jazakumullah khairan, doa dan ucapan Anda sudah kami terima.",
  wishPlaceholder: "Tuliskan doa terbaik untuk kedua mempelai…",
  giftIntro: "Doa Anda adalah hadiah terindah bagi kami. Bila berkenan memberi tanda kasih, dapat melalui:",
};

export default function KapasSyariTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Walimatul 'Ursy";
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const photo = data.gallery[0];
  const names = <>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</>;

  return (
    <ThemeShell
      fonts={FONTS}
      background="#e7dcc9"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <p className={s.coverArabic} lang="ar" dir="rtl">بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ</p>
          <div className={s.hoopWrap}>
            <div className={s.cloth}>
              <p className={s.kicker}>{label}</p>
              <h1 className={s.coverNames}>{names}</h1>
              <p className={s.coverDate}>{formatDate(data.date)}</p>
            </div>
            <Art name="hoop" eager className={s.hoopImg} />
            <Art name="boll" eager className={s.coverBoll} />
          </div>
          <Art name="stem" eager className={s.coverStem} />
          <Art name="stem" eager className={s.coverStem2} />
          <div className={s.guest}>
            <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
            <strong>{guestLabel(data)}</strong>
            {table && <span className={s.table}>{table}</span>}
          </div>
          <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="currentColor" />Buka Undangan</button>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        noPhotos
        light="#fbf8f1"
        dark="#5d4330"
        copy={COPY}
        hero={(
          <header className={s.hero}>
            <div className={s.heroTag}>
              <p className={s.heroKicker}>{label}</p>
              <h1 className={s.heroNames}>{names}</h1>
              <p className={s.heroDate}>{formatDate(data.date)}</p>
              {note && <p className={s.heroNote}>{note}</p>}
            </div>
            {photo ? <div className={s.heroPic}><Photo src={photo} alt={`${data.couple.bride} & ${data.couple.groom}`} /></div> : <Art name="spray" className={s.heroSpray} />}
          </header>
        )}
        slots={{
          divider: <Art name="sprig" className={s.divider} />,
          node: <Art name="boll" />,
          amp: <Art name="boll" />,
          portrait: <span className={s.hoopArt} aria-hidden><Art name="hoop" /><Art name="boll" className={s.hoopBoll} /></span>,
          closingEmblem: <Art name="spray" className={s.closingSpray} />,
          sentArt: <Art name="boll" />,
        }}
      />
    </ThemeShell>
  );
}
