"use client";
// Theme "Sage Syari" — walimah syar'i tanpa foto: ranting kayu putih (eucalyptus) dan daun kering yang dilukis cat air,
// diletakkan di atas kartu linen bertepi jahitan putus-putus; segel lilin sage bermonogram menggantikan foto. Kartu
// mempelai berbentuk label gantung berlubang tali, tata letak rata kiri yang tenang. Tanpa makhluk bernyawa, tanpa
// kaligrafi yang dilukis (basmalah diketik).
import { Lucide, ThemeShell, formatDate, guestLabel, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Bellefair", "Mulish:ital,wght@0,400;0,600;0,700;1,400", "Mrs Saint Delafield", "Amiri:wght@400"];
// Painted by /tmp/pen/art/themes/sage-syari.py (tools/art/themes in the repo).
const Art = makeArt("sage-syari", {
  ranting: [700, 419], segel: [300, 292], divider: [320, 62], daun: [110, 56], tangkai: [170, 613],
} as const);
const BISMILLAH = "بِسْمِ اللّٰهِ الرَّحْمٰنِ الرَّحِيْمِ";

function initial(name?: string) {
  return (name ?? "").trim().slice(0, 1).toUpperCase();
}

function Seal({ bride, groom, eager, className }: { bride: string; groom?: string; eager?: boolean; className?: string }) {
  const b = initial(bride), g = initial(groom);
  return (
    <div className={className ? `${s.seal} ${className}` : s.seal} aria-hidden>
      <Art name="segel" eager={eager} />
      <b>{b}{g && <><i>&amp;</i>{g}</>}</b>
    </div>
  );
}

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    arabic: BISMILLAH,
    kicker: "Assalamu'alaikum Warahmatullahi Wabarakatuh",
    title: "Dengan tenang, kami memulai babak yang baru",
    intro: "Dengan memohon rahmat dan rida Allah Subhanahu wa Ta'ala, kami bermaksud menyelenggarakan walimah pernikahan putra-putri kami. Merupakan kehormatan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"],
  couple: ["Dua Nama, Satu Ikatan", "Kedua Mempelai"],
  count: ["Menanti dengan Sabar", "Menuju Hari Akad"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Waktu & Tempat", "Rangkaian Acara"],
  story: ["Perlahan Tumbuh", "Perjalanan Kami"],
  gallery: ["Galeri", "Kenangan"],
  wishes: ["Doa & Kehadiran", "Ucapan & Konfirmasi"],
  gifts: ["Tanda Kasih", "Amplop Digital"],
  closing: {
    thanks: "Jazakumullah Khairan",
    text: "Atas kehadiran dan doa restu Bapak/Ibu/Saudara/i, kami ucapkan terima kasih. Semoga Allah menumbuhkan keberkahan di rumah kami dan di rumah kita semua.",
    salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh",
  },
  sent: "Jazakumullah khairan, doa dan ucapan Anda sudah terkirim.",
  wishPlaceholder: "Tuliskan doa terbaik untuk kedua mempelai…",
};

const WISHES = [
  { id: "w1", name: "Ustazah Hj. Maemunah", attendance: "yes" as Attendance, message: "Barakallahu lakuma wa baraka 'alaikuma wa jama'a bainakuma fi khair. Semoga menjadi keluarga sakinah, mawaddah, wa rahmah." },
  { id: "w2", name: "Pengajar Rumah Tahfiz Al-Hikmah", attendance: "yes" as Attendance, message: "Dari satu majelis ke satu rumah tangga. Ikut bahagia, Ustazah Alya dan Ustaz Rasyid. Sampai jumpa di Semarang." },
  { id: "w3", name: "Keluarga Pakde Harun, Kudus", attendance: "maybe" as Attendance, message: "Insyaallah kami usahakan hadir. Doa terbaik dari kami sekeluarga di Kudus." },
];

export default function SageSyariTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Walimatul 'Ursy";
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const { bride, groom } = data.couple;

  return (
    <ThemeShell
      fonts={FONTS}
      background="#e3e2d8"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <p className={s.arabicCover} lang="ar" dir="rtl">{BISMILLAH}</p>
          <p className={s.kicker}>Assalamu&apos;alaikum Wr. Wb.</p>
          <div className={s.card}>
            <p className={s.coverLabel}>{label}</p>
            <h1 className={s.coverNames}><span>{bride}</span>{groom && <><em>&amp;</em><span>{groom}</span></>}</h1>
            <p className={s.coverDate}><Art name="daun" eager />{formatDate(data.date)}</p>
            <Seal bride={bride} groom={groom} eager className={s.coverSeal} />
          </div>
          <Art name="ranting" eager className={s.coverBranch} />
          <div className={s.coverFoot}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#f1f0e6" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        noPhotos
        light="#f1f0e6"
        dark="#4d6044"
        copy={COPY}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            <Art name="tangkai" className={s.heroSprig} />
            <Seal bride={bride} groom={groom} />
            <p className={s.heroKicker}>{label}</p>
            <h1 className={s.heroNames}>{bride}{groom && <> <em>&amp;</em> {groom}</>}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="divider" className={s.divider} />,
          node: <Art name="daun" />,
          amp: <Art name="daun" />,
          portrait: <Art name="segel" className={s.pSeal} />,
          countDecor: <Art name="tangkai" className={s.countSprig} />,
          closingDecor: <Art name="ranting" className={s.clBranch} />,
          closingEmblem: <Seal bride={bride} groom={groom} className={s.closingSeal} />,
          sentArt: <Art name="divider" />,
        }}
      />
    </ThemeShell>
  );
}
