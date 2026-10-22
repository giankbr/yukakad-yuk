"use client";
// Theme "Daun Embun" — walimah syari tanpa foto: daun calathea bergaris bulu, sirih gading berbelang krem, dan pakis yang
// basah oleh embun pagi, dilukis cat air botanis dengan tetes embun bening (bayang, pembiasan, kilau). Medali monogram dari
// lingkar pakis, kartu kaca berembun, tata letak rata kiri yang lapang, setetes embun yang jatuh dari ujung daun.
// Tanpa makhluk bernyawa, tanpa kaligrafi yang dilukis (basmalah diketik).
import { Lucide, ThemeShell, formatDate, guestLabel, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Fraunces:ital,wght@0,300;0,400;1,300", "Nunito Sans:wght@400;600;700", "Ephesis", "Amiri:wght@400"];
// Painted by /tmp/pen/art/themes/daun-embun.py (tools/art/themes in the repo).
const Art = makeArt("daun-embun", {
  atas: [531, 552], bawah: [510, 361], medali: [437, 444], tetes: [72, 72], divider: [360, 58], sprig: [162, 340],
} as const);
const BISMILLAH = "بِسْمِ اللّٰهِ الرَّحْمٰنِ الرَّحِيْمِ";

function initial(name?: string) {
  return (name ?? "").trim().slice(0, 1).toUpperCase();
}

function Medal({ bride, groom, eager, className }: { bride: string; groom?: string; eager?: boolean; className?: string }) {
  const b = initial(bride), g = initial(groom);
  return (
    <div className={className ? `${s.medal} ${className}` : s.medal} aria-hidden>
      <Art name="medali" eager={eager} />
      <div className={s.medalIn}><span className={s.mono}>{b}{g && <><i>&amp;</i>{g}</>}</span></div>
    </div>
  );
}

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    arabic: BISMILLAH,
    kicker: "Assalamu'alaikum Warahmatullahi Wabarakatuh",
    title: "Seperti embun yang Allah turunkan di setiap pagi",
    intro: "Dengan memohon rahmat dan rida Allah Subhanahu wa Ta'ala, kami bermaksud menyelenggarakan walimah pernikahan putra-putri kami. Merupakan kehormatan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"],
  couple: ["Dua Helai, Satu Dahan", "Kedua Mempelai"],
  count: ["Menanti Pagi Itu", "Menuju Hari Akad"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Waktu & Tempat", "Rangkaian Acara"],
  story: ["Tumbuh Perlahan", "Perjalanan Kami"],
  gallery: ["Galeri", "Kenangan"],
  wishes: ["Doa & Kehadiran", "Ucapan & Konfirmasi"],
  gifts: ["Tanda Kasih", "Amplop Digital"],
  closing: {
    thanks: "Jazakumullah Khairan",
    text: "Atas kehadiran dan doa restu Bapak/Ibu/Saudara/i, kami ucapkan terima kasih. Semoga Allah menyejukkan hati kita semua seperti embun menyejukkan daun.",
    salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh",
  },
  sent: "Jazakumullah khairan, doa dan ucapan Anda sudah terkirim.",
  wishPlaceholder: "Tuliskan doa terbaik untuk kedua mempelai…",
};

const WISHES = [
  { id: "w1", name: "Ustazah Rahmah", attendance: "yes" as Attendance, message: "Barakallahu lakuma wa baraka 'alaikuma wa jama'a bainakuma fi khair. Semoga menjadi keluarga sakinah yang selalu tumbuh dalam ketaatan." },
  { id: "w2", name: "Tim Relawan Kebun Raya", attendance: "yes" as Attendance, message: "Dari mendata pakis sampai ke pelaminan! Ikut bahagia, Salsa dan Fathan. Sampai jumpa di Bogor." },
  { id: "w3", name: "Keluarga Om Dedi, Bandung", attendance: "maybe" as Attendance, message: "Insyaallah kami usahakan hadir. Doa terbaik dari kami sekeluarga." },
];

export default function DaunEmbunTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Walimatul 'Ursy";
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const { bride, groom } = data.couple;

  return (
    <ThemeShell
      fonts={FONTS}
      background="#eef3ea"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Art name="atas" eager className={s.leafTop} />
          <Art name="bawah" eager className={s.leafBottom} />
          <span className={s.fall} aria-hidden><Art name="tetes" eager /></span>
          <div className={s.coverIn}>
            <p className={s.arabicCover} lang="ar" dir="rtl">{BISMILLAH}</p>
            <p className={s.kicker}>Assalamu&apos;alaikum Wr. Wb.</p>
            <Medal bride={bride} groom={groom} eager className={s.coverMedal} />
            <p className={s.coverLabel}>{label}</p>
            <h1 className={s.coverNames}><span>{bride}</span>{groom && <><em>&amp;</em><span>{groom}</span></>}</h1>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
            <div className={s.coverFoot}>
              <div className={s.guest}>
                <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
                <strong>{guestLabel(data)}</strong>
                {table && <span className={s.table}>{table}</span>}
              </div>
              <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#f1f7ec" />Buka Undangan</button>
            </div>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        noPhotos
        light="#f1f7ec"
        dark="#1f4a36"
        copy={COPY}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            <div className={s.heroCard}>
              <Art name="sprig" className={s.heroLeaf} />
              <Medal bride={bride} groom={groom} />
              <p className={s.heroKicker}>{label}</p>
              <h1 className={s.heroNames}>{bride}{groom && <> <em>&amp;</em> {groom}</>}</h1>
              <p className={s.heroDate}>{formatDate(data.date)}</p>
              {note && <p className={s.heroNote}>{note}</p>}
            </div>
          </header>
        )}
        slots={{
          divider: <Art name="divider" className={s.divider} />,
          node: <Art name="tetes" />,
          amp: <Art name="tetes" />,
          portrait: <Art name="medali" className={s.pMedal} />,
          countDecor: <><Art name="atas" className={s.countLeaf} /><Art name="bawah" className={s.countLeaf} /></>,
          closingDecor: <><Art name="atas" className={s.clTop} /><Art name="bawah" className={s.clBottom} /></>,
          closingEmblem: <Medal bride={bride} groom={groom} className={s.closingMedal} />,
          sentArt: <Art name="sprig" />,
        }}
      />
    </ThemeShell>
  );
}
