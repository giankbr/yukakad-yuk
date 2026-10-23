"use client";
// Theme "Kampung Naga" — lembah kampung adat Sunda di Tasikmalaya dalam cat air berkabut: deretan rumah panggung
// seragam beratap ijuk hitam dan berdinding bilik kapur, sawah berundak, tangga batu, dan Sungai Ciwulan. Nama
// mempelai di langit berkabut, foto dalam jendela berbentuk rumah, kartu acara beratap ijuk, dan batu sungai di lini
// masa. Kabut bergeser pelan di sampul.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Young Serif", "Gentium Book Plus:ital,wght@0,400;0,700;1,400", "Jost:wght@400;500", "Amiri"];
// Painted by /tmp/pen/art/themes/kampung-naga.py (lembah and sawah are CSS backgrounds).
const Art = makeArt("kampung-naga", { imah: [360, 288], divider: [300, 24], batu: [72, 51] } as const);

const WISHES = [
  { id: "w1", name: "Ceu Imas & Kulawarga", attendance: "yes" as const, message: "Wilujeng nikah Wulan sareng Dadan. Mugia janten kulawarga sakinah, mawaddah, warahmah, rukun salawasna." },
  { id: "w2", name: "Kang Yayan, Garut", attendance: "yes" as const, message: "Barakallahu lakuma. Insyaallah hadir, sekalian ngarasakeun nasi liwetna." },
  { id: "w3", name: "Teh Rina & Keluarga", attendance: "maybe" as const, message: "Hapunten upami teu tiasa sumping. Doa terbaik ti kami kanggo kalian berdua." },
];

export default function KampungNagaTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const hero = data.gallery[0] ?? data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#c9d6c8"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <span className={s.mist} aria-hidden />
          <p className={s.kicker}>Undangan {label}</p>
          <p className={s.salam}>Assalamu&apos;alaikum Wr. Wb.</p>
          <h1 className={s.coverNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.guestWrap}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#f6f3ea" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#f4efe2"
        dark="#2e2622"
        demoWishes={WISHES}
        copy={{
          ...DEFAULT_COPY,
          opening: {
            arabic: "بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيم",
            kicker: "Assalamu'alaikum Wr. Wb.",
            title: "Neda Pidu'a",
            intro: "Dengan memohon rahmat dan ridho Allah SWT, kami bermaksud menyelenggarakan pernikahan putra-putri kami. Merupakan kehormatan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
          },
          roles: ["Panganten Istri", "Panganten Pameget"],
          couple: ["Panganten", "Kedua Mempelai"],
          count: ["Ngitung Poé", "Menuju Hari Bahagia"],
          units: ["Poé", "Jam", "Menit", "Detik"],
          events: ["Runtuyan Acara", "Waktu & Tempat"],
          story: ["Lalakon", "Perjalanan Kami"],
          gallery: ["Galeri", "Potret Kami"],
          wishes: ["Du'a & Wawaran", "Ucapan & Kehadiran"],
          gifts: ["Tanda Asih", "Amplop Digital"],
          closing: {
            thanks: "Hatur Nuhun",
            text: "Kehadiran dan doa restu Bapak/Ibu/Saudara/i merupakan kebahagiaan yang tak ternilai bagi kami sekeluarga.",
            salam: "Wassalamu'alaikum Wr. Wb.",
          },
          sent: "Hatur nuhun, doa sareng ucapan parantos kakirim.",
          familyLabel: "Kulawarga Ageung",
        }}
        hero={(
          <header className={s.hero}>
            <p className={s.heroKicker}>Walimatul &apos;Ursy</p>
            <h1 className={s.heroNames}>{data.couple.bride} <em>&amp;</em> {data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {hero && <div className={s.heroPhoto}><Photo src={hero} alt={`${data.couple.bride} dan ${data.couple.groom}`} /></div>}
            <Art name="imah" className={s.heroImah} />
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="divider" className={s.divider} />,
          node: <Art name="batu" />,
          amp: <Art name="batu" />,
          portrait: <span className={s.portraitArt} aria-hidden />,
          closingEmblem: <Art name="imah" className={s.closingEmblem} />,
          sentArt: <Art name="imah" />,
        }}
      />
    </ThemeShell>
  );
}
