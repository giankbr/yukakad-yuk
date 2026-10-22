"use client";
// Theme "Melati Syari" — walimah syari tanpa foto dengan melati segar (desain orisinal): kanopi hijau daun bergantung
// untaian roncean melati, bunga melati putih dan daun mengilap dalam gouache matte, medali monogram dari lingkar kuncup
// melati, kartu berpotongan daun di atas kertas mint. Tanpa figur makhluk, tanpa kaligrafi yang digambar.
import { Lucide, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Gilda Display", "Lora:ital,wght@0,400;0,500;0,600;1,400", "Parisienne", "Amiri:wght@400"];
// Painted by /tmp/pen/art/themes/melati-syari.py (tools/art/themes in the repo).
const Art = makeArt("melati-syari", {
  curtain: [780, 558], medallion: [400, 403], sprig: [340, 245], divider: [330, 29], bloom: [120, 96],
} as const);
const BISMILLAH = "بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ";

function initial(name?: string) {
  return (name ?? "").trim().slice(0, 1).toUpperCase();
}

function Medal({ bride, groom, eager, className }: { bride: string; groom?: string; eager?: boolean; className?: string }) {
  const b = initial(bride), g = initial(groom);
  return (
    <div className={className ? `${s.medal} ${className}` : s.medal} aria-hidden>
      <Art name="medallion" eager={eager} />
      <div className={s.medalIn}><span className={s.mono}>{b}{g && <><i>&amp;</i>{g}</>}</span></div>
    </div>
  );
}

const COPY = {
  ...DEFAULT_COPY,
  opening: {
    arabic: BISMILLAH,
    kicker: "Assalamu'alaikum Warahmatullahi Wabarakatuh",
    title: "Dengan Rahmat Allah",
    intro: "Dengan memohon rahmat dan rida Allah Subhanahu wa Ta'ala, kami bermaksud menyelenggarakan walimah pernikahan putra-putri kami. Merupakan kehormatan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"] as [string, string],
  couple: ["Dironce dengan Doa", "Kedua Mempelai"] as [string, string],
  count: ["Menghitung Hari", "Menuju Hari Akad"] as [string, string],
  units: ["Hari", "Jam", "Menit", "Detik"] as [string, string, string, string],
  events: ["Waktu & Tempat", "Rangkaian Acara"] as [string, string],
  story: ["Kuntum demi Kuntum", "Perjalanan Kami"] as [string, string],
  gallery: ["Galeri", "Kenangan"] as [string, string],
  wishes: ["Doa & Kehadiran", "Ucapan & Konfirmasi"] as [string, string],
  gifts: ["Tanda Kasih", "Amplop Digital"] as [string, string],
  closing: {
    thanks: "Jazakumullah Khairan",
    text: "Atas kehadiran dan doa restu Bapak/Ibu/Saudara/i, kami ucapkan terima kasih. Semoga Allah membalas setiap kebaikan dengan yang lebih harum dan berlipat.",
    salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh",
  },
  sent: "Jazakumullah khairan, doa dan ucapan Anda sudah terkirim.",
  wishPlaceholder: "Tuliskan doa terbaik untuk kedua mempelai…",
};

export default function MelatiSyariTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Walimatul 'Ursy";
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const { bride, groom } = data.couple;

  return (
    <ThemeShell
      fonts={FONTS}
      background="#f2f7ec"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.canopy}>
            <Art name="curtain" eager className={s.curtain} />
            <p className={s.coverArabic} lang="ar" dir="rtl">{BISMILLAH}</p>
            <p className={s.kicker}>{label}</p>
          </div>
          <Medal bride={bride} groom={groom} eager />
          <h1 className={s.coverNames}><span>{bride}</span>{groom && <><em>&amp;</em><span>{groom}</span></>}</h1>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.coverFoot}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#ffffff" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        noPhotos
        light="#f7f9f1"
        dark="#2c5a3c"
        copy={COPY}
        hero={(
          <header className={s.hero}>
            <Art name="curtain" className={s.curtain} />
            <Medal bride={bride} groom={groom} />
            <p className={s.heroKicker}>{label}</p>
            <h1 className={s.heroNames}>{bride}{groom && <> <em>&amp;</em> {groom}</>}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="divider" className={s.divider} />,
          node: <Art name="bloom" />,
          amp: <Art name="bloom" />,
          portrait: <Art name="medallion" />,
          countDecor: <><Art name="sprig" className={s.countSprig} /><Art name="sprig" className={s.countSprig} /></>,
          closingDecor: <Art name="curtain" className={s.closeCurtain} />,
          closingEmblem: <Medal bride={bride} groom={groom} className={s.closingMedal} />,
          sentArt: <Art name="bloom" />,
        }}
      />
    </ThemeShell>
  );
}
