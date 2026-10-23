"use client";
// Theme "Mawar Debu" — tanpa foto: seikat mawar kering dusty rose diikat pita satin mauve, bersandar di atas kartu
// kertas katun yang sedikit miring; judul Bodoni miring rata kiri, medali kameo bermonogram dengan pita, kartu acara
// berpita di sudut, pita satin panjang yang bergoyang pelan. Lembut, hangat, tenang.
import { Lucide, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Bodoni Moda:ital,wght@0,400;0,500;1,400;1,500", "Lustria", "Monsieur La Doulaise", "Amiri"];
// Painted by /tmp/pen/art/themes/mawar-debu.py (tools/art/themes in the repo).
const Art = makeArt("mawar-debu", {
  bundle: [620, 857], bow: [260, 296], ribbon: [180, 700], rose: [167, 184], sprig: [440, 71],
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
  couple: ["atas izin Allah", "Kedua Mempelai"] as [string, string],
  count: ["menghitung hari", "Menuju Akad"] as [string, string],
  units: ["Hari", "Jam", "Menit", "Detik"] as [string, string, string, string],
  events: ["waktu & tempat", "Rangkaian Acara"] as [string, string],
  story: ["perjalanan", "Kisah Kami"] as [string, string],
  gallery: ["galeri", "Momen Kami"] as [string, string],
  wishes: ["doa & kehadiran", "Ucapan & Konfirmasi"] as [string, string],
  gifts: ["tanda kasih", "Amplop Digital"] as [string, string],
  closing: {
    thanks: "Jazakumullah Khairan",
    text: "Atas kehadiran dan doa restu Bapak/Ibu/Saudara/i, kami ucapkan terima kasih. Semoga Allah menjadikan pernikahan ini sakinah, mawaddah, wa rahmah.",
    salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh",
  },
  sent: "Jazakumullah khairan, doa dan ucapan Anda sudah kami terima.",
  wishPlaceholder: "Tuliskan doa terbaik untuk kedua mempelai…",
  giftIntro: "Doa restu Anda adalah hadiah terindah. Bila berkenan memberi tanda kasih, dapat melalui:",
};

export default function MawarDebuTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Walimatul 'Ursy";
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#e6d3cf"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Art name="ribbon" eager className={s.coverRibbon} />
          <div className={s.card}>
            <p className={s.kicker}>{label}</p>
            <h1 className={s.coverNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={15} color="currentColor" />Buka Undangan</button>
          </div>
          <Art name="bundle" eager className={s.coverBundle} />
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        noPhotos
        light="#fbf1f2"
        dark="#6f4a5e"
        copy={COPY}
        hero={(
          <header className={s.hero}>
            <Art name="bow" className={s.heroBow} />
            <p className={s.heroKicker}>{label}</p>
            <h1 className={s.heroNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="sprig" className={s.divider} />,
          node: <Art name="rose" />,
          amp: <Art name="rose" />,
          portrait: <Art name="bow" className={s.bowTop} />,
          countDecor: <><Art name="ribbon" className={`${s.countRibbon} ${s.countRibbonL}`} /><Art name="ribbon" className={`${s.countRibbon} ${s.countRibbonR}`} /></>,
          closingEmblem: <Art name="bundle" className={s.closingBundle} />,
          sentArt: <Art name="bow" />,
        }}
      />
    </ThemeShell>
  );
}
