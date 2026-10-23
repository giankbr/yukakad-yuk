"use client";
// Theme "Zaitun Syari" — walimah syar'i tanpa foto: ranting zaitun hijau perak dengan buah zaitun gelap, dilukis cat
// air dan diletakkan seperti spesimen herbarium di atas lembar kertas linen. Label ketik ala museum, karangan zaitun
// oval sebagai bingkai monogram. Tanpa makhluk bernyawa, tanpa kaligrafi yang dilukis (basmalah diketik).
import { Lucide, ThemeShell, formatDate, guestLabel, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Marcellus", "Karla:ital,wght@0,400;0,600;0,700;1,400", "Courier Prime:ital@0;1", "Amiri:wght@400"];
// Painted by /tmp/pen/art/themes/zaitun-syari.py (tools/art/themes in the repo).
const Art = makeArt("zaitun-syari", { branch: [820, 487], sprig: [340, 64], pair: [120, 110], wreath: [420, 538] } as const);
const BISMILLAH = "بِسْمِ اللّٰهِ الرَّحْمٰنِ الرَّحِيْمِ";

function initial(name?: string) {
  return (name ?? "").trim().slice(0, 1).toUpperCase();
}

function specimenNo(date?: string) {
  const m = /^(\d{4})-(\d{2})-(\d{2})/.exec(date ?? "");
  return m ? `${m[3]}.${m[2]}.${m[1]}` : "—";
}

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    arabic: BISMILLAH,
    kicker: "Assalamu'alaikum Warahmatullahi Wabarakatuh",
    title: "Tumbuh perlahan, berbuah keberkahan",
    intro: "Dengan memohon rahmat dan rida Allah Subhanahu wa Ta'ala, kami bermaksud menyelenggarakan walimah pernikahan putra-putri kami. Merupakan kehormatan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"],
  couple: ["dua ranting, satu pohon", "Kedua Mempelai"],
  count: ["menghitung hari", "Menuju Hari Akad"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["waktu & tempat", "Rangkaian Acara"],
  story: ["catatan perjalanan", "Kisah Kami"],
  gallery: ["galeri", "Kenangan"],
  wishes: ["doa & kehadiran", "Ucapan & Konfirmasi"],
  gifts: ["tanda kasih", "Amplop Digital"],
  closing: {
    thanks: "Jazakumullah Khairan",
    text: "Atas kehadiran dan doa restu Bapak/Ibu/Saudara/i, kami ucapkan terima kasih. Semoga Allah menjadikan rumah kami seperti pohon yang baik: akarnya kuat dan buahnya memberi manfaat.",
    salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh",
  },
  sent: "Jazakumullah khairan, doa dan ucapan Anda sudah terkirim.",
  wishPlaceholder: "Tuliskan doa terbaik untuk kedua mempelai…",
};

const WISHES = [
  { id: "w1", name: "Ustazah Hj. Khadijah", attendance: "yes" as Attendance, message: "Barakallahu lakuma wa baraka 'alaikuma wa jama'a bainakuma fi khair. Semoga menjadi keluarga sakinah, mawaddah, wa rahmah." },
  { id: "w2", name: "Rekan Apoteker RS Salak", attendance: "yes" as Attendance, message: "Ikut bahagia, Zahra dan Irfan. Semoga rumah tangganya teduh dan saling menguatkan. Sampai jumpa di Bogor." },
  { id: "w3", name: "Keluarga Om Rahman, Depok", attendance: "maybe" as Attendance, message: "Insyaallah kami usahakan hadir. Doa terbaik dari kami sekeluarga." },
];

export default function ZaitunSyariTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Walimatul 'Ursy";
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const { bride, groom } = data.couple;
  const b = initial(bride), g = initial(groom);

  return (
    <ThemeShell
      fonts={FONTS}
      background="#ece6d8"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <p className={s.arabicCover} lang="ar" dir="rtl">{BISMILLAH}</p>
          <p className={s.kicker}>Assalamu&apos;alaikum Wr. Wb.</p>
          <Art name="branch" eager className={s.coverBranch} />
          <div className={s.sheet}>
            <p className={s.coverLabel}>{label}</p>
            <h1 className={s.coverNames}><span>{bride}</span>{groom && <><em>&amp;</em><span>{groom}</span></>}</h1>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
            <p className={s.specimen}><i>Olea europaea</i><span>No. {specimenNo(data.date)}</span></p>
          </div>
          <div className={s.coverFoot}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#eef0e6" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        noPhotos
        light="#eef0e6"
        dark="#3e4a33"
        copy={COPY}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            <div className={s.heroWreath} aria-hidden>
              <Art name="wreath" />
              <b>{b}{g && <><i>&amp;</i>{g}</>}</b>
            </div>
            <p className={s.heroKicker}>{label}</p>
            <h1 className={s.heroNames}>{bride}{groom && <> <em>&amp;</em> {groom}</>}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="sprig" className={s.divider} />,
          node: <Art name="pair" />,
          amp: <Art name="pair" />,
          portrait: <Art name="wreath" className={s.pWreath} />,
          countDecor: <Art name="branch" className={s.countBranch} />,
          closingDecor: <Art name="branch" className={s.clBranch} />,
          closingEmblem: <div className={s.clWreath} aria-hidden><Art name="wreath" /><b>{b}{g && `·${g}`}</b></div>,
          sentArt: <Art name="sprig" />,
        }}
      />
    </ThemeShell>
  );
}
