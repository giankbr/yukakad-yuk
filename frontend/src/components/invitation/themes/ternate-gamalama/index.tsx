"use client";
// Theme "Ternate Gamalama" — pernikahan Islami di Ternate: Kedaton Kesultanan di bukitnya dan kerucut Gamalama yang
// menjulang dari laut Halmahera, dilukis cat air dan dilihat lewat jendela lengkung runcing berbingkai emas; ranting pala
// dengan fuli merah dan cengkih di ambangnya; bintang delapan berlapis emas sebagai pemisah. Biru tua dan merah pala.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Gilda Display", "Spectral:ital,wght@0,400;0,600;0,700;1,400", "Amiri:wght@400;700"];
// Painted by /tmp/pen/art/themes/ternate-gamalama.py (tools/art/themes in the repo).
const Art = makeArt("ternate-gamalama", { gamalama: [540, 639], rempah: [600, 309], cengkih: [180, 248], bintang: [120, 120] } as const);

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    arabic: "بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ",
    kicker: "Assalamu'alaikum Wr. Wb.",
    title: "Dengan Rahmat Allah",
    intro: "Dengan memohon rahmat dan rida Allah Subhanahu wa Ta'ala, kami bermaksud menyelenggarakan akad nikah dan walimah putra-putri kami. Merupakan kehormatan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"],
  couple: ["Kedua Mempelai", "Pala & Cengkih"],
  count: ["Menghitung Hari", "Menuju Hari Bahagia"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Waktu & Tempat", "Rangkaian Acara"],
  story: ["Kisah Kami", "Di Kaki Gamalama"],
  gallery: ["Galeri", "Momen Bahagia"],
  wishes: ["Doa & Kehadiran", "Ucapan & Konfirmasi"],
  gifts: ["Tanda Kasih", "Amplop Digital"],
  closing: { thanks: "Jazakumullahu Khairan", text: "Atas kehadiran dan doa restu Bapak/Ibu/Saudara/i, kami ucapkan terima kasih. Semoga Allah membalas dengan kebaikan.", salam: "Wassalamu'alaikum Wr. Wb." },
  sent: "Terima kasih, doa dan ucapan Anda sudah terkirim.",
  wishPlaceholder: "Tuliskan doa terbaik untuk kedua mempelai…",
};

const WISHES = [
  { id: "w1", name: "Keluarga H. Abdurrahman Sangaji", attendance: "yes" as Attendance, message: "Barakallahu lakuma wa baraka 'alaikuma wa jama'a bainakuma fi khair. Selamat Fitri dan Rizal." },
  { id: "w2", name: "Teman-teman Farmasi Unkhair", attendance: "yes" as Attendance, message: "Selamat ya Fitri! Semoga menjadi keluarga sakinah, mawaddah, warahmah." },
  { id: "w3", name: "Om Udin & Keluarga, Tidore", attendance: "maybe" as Attendance, message: "Insyaallah kami menyeberang dari Tidore. Doa terbaik untuk kalian berdua." },
];

export default function TernateGamalamaTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const hero = data.gallery[0] ?? data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#102f52"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <p className={s.bismillah} lang="ar" dir="rtl">بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ</p>
          <p className={s.salam}>Assalamu&apos;alaikum Wr. Wb.</p>
          <p className={s.kicker}>Undangan {label}</p>
          <div className={s.window} aria-hidden>
            <div className={s.windowPane}><Art name="gamalama" eager className={s.windowArt} /></div>
            <Art name="rempah" eager className={s.spray} />
            <Art name="cengkih" eager className={s.sprig} />
          </div>
          <h1 className={s.coverNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.guestWrap}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#102f52" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#ecd49a"
        dark="#123a63"
        copy={COPY}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            <div className={s.heroArch}>
              {hero && <div className={s.heroPhoto}><Photo src={hero} alt="" /></div>}
              <Art name="rempah" className={s.heroSpray} />
            </div>
            <p className={s.heroKicker}>Walimatul &apos;Ursy</p>
            <h1 className={s.heroNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <span className={s.divider} aria-hidden><i /><Art name="bintang" /><i /></span>,
          node: <Art name="bintang" />,
          amp: <Art name="cengkih" />,
          portrait: <Art name="cengkih" />,
          countDecor: <><Art name="rempah" className={s.countSpray} /><Art name="rempah" className={`${s.countSpray} ${s.countSprayR}`} /></>,
          closingDecor: <Art name="rempah" className={s.closingSpray} />,
          closingEmblem: <Art name="bintang" className={s.closingEmblem} />,
          sentArt: <Art name="cengkih" />,
        }}
      />
    </ThemeShell>
  );
}
