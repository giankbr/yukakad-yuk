"use client";
// Theme "Batik Garutan" — kain batik Garutan krem gumading: sampul seperti kain terlipat di dua sudut sehingga lereng
// diagonal soga, biru, dan hijau terlihat di lipatannya; serangkai bunga canting berisen cecek; foto dalam bingkai kain
// lereng; potret, kartu, dan galeri berpotongan diagonal; lanskap cat air Gunung Cikuray dan kebun teh Garut.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Castoro:ital@0;1", "Alegreya:ital,wght@0,400;0,700;1,400", "Marcellus SC", "Amiri"];
// Painted by /tmp/pen/art/themes/batik-garutan.py (lereng and kain are CSS background tiles).
const Art = makeArt("batik-garutan", { kembang: [535, 430], kuncup: [160, 160], divider: [440, 62], cikuray: [780, 369] } as const);

const WISHES = [
  { id: "w1", name: "Ceu Iis & Kulawarga", attendance: "yes" as const, message: "Wilujeng nikah Ratna sareng Yusuf. Mugia janten kulawarga sakinah, mawaddah, warahmah, rukun dugi ka pupus." },
  { id: "w2", name: "Kang Dadang, Tarogong", attendance: "yes" as const, message: "Barakallahu lakuma. Insyaallah sumping, hoyong ngaraosan burayot Garut di resepsina." },
  { id: "w3", name: "Teh Nita & Keluarga", attendance: "maybe" as const, message: "Hapunten upami teu tiasa sumping. Doa pangsaéna ti kami kanggo kalian berdua." },
];

export default function BatikGarutanTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const hero = data.gallery[0] ?? data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#efe2c3"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <span className={s.sashTL} aria-hidden />
          <span className={s.sashBR} aria-hidden />
          <Art name="kembang" eager className={s.coverKembang} />
          <p className={s.kicker}>Sampurasun</p>
          <p className={s.coverLabel}>Undangan {label}</p>
          <h1 className={s.coverNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.guestWrap}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#f1e2bf" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#f1e2bf"
        dark="#29425a"
        demoWishes={WISHES}
        copy={{
          ...DEFAULT_COPY,
          opening: {
            arabic: "بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيم",
            kicker: "Assalamu'alaikum Wr. Wb.",
            title: "Neda Pangdu'a",
            sub: "Walimatul 'Ursy",
            intro: "Dengan memohon rahmat dan ridho Allah SWT, kami bermaksud menyelenggarakan pernikahan putra-putri kami. Merupakan kehormatan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
          },
          roles: ["Panganten Istri", "Panganten Pameget"],
          couple: ["Nu Bade Nikah", "Kedua Mempelai"],
          count: ["Ngitung Poé", "Menuju Hari Bahagia"],
          units: ["Poé", "Jam", "Menit", "Detik"],
          events: ["Waktos & Tempat", "Rangkaian Acara"],
          story: ["Lalakon Urang", "Perjalanan Kami"],
          gallery: ["Galeri", "Potret Bahagia"],
          wishes: ["Du'a & Wawaran", "Ucapan & Kehadiran"],
          gifts: ["Tanda Asih", "Amplop Digital"],
          closing: {
            thanks: "Hatur Nuhun",
            text: "Kehadiran dan doa restu Bapak/Ibu/Saudara/i merupakan kebahagiaan yang tak ternilai bagi kami sekeluarga.",
            salam: "Wassalamu'alaikum Wr. Wb.",
          },
          sent: "Hatur nuhun, du'a sareng ucapan parantos kakirim.",
          familyLabel: "Kulawarga Ageung",
        }}
        hero={(
          <header className={s.hero}>
            <p className={s.heroKicker}>Walimatul &apos;Ursy</p>
            <h1 className={s.heroNames}>{data.couple.bride} <em>&amp;</em> {data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {hero && (
              <div className={s.heroFrame}>
                <div className={s.heroPhoto}><Photo src={hero} alt={`${data.couple.bride} dan ${data.couple.groom}`} /></div>
                <Art name="kuncup" className={s.heroKuncup} />
              </div>
            )}
            {note && <p className={s.heroNote}>{note}</p>}
            <Art name="cikuray" className={s.heroLand} />
          </header>
        )}
        slots={{
          divider: <Art name="divider" className={s.divider} />,
          node: <Art name="kuncup" />,
          amp: <Art name="kuncup" />,
          portrait: <span className={s.portraitSash} aria-hidden />,
          countDecor: <span className={s.countLereng} aria-hidden />,
          closingEmblem: <Art name="kembang" className={s.closingEmblem} />,
          closingDecor: <Art name="cikuray" className={s.closingLand} />,
          sentArt: <Art name="kuncup" />,
        }}
      />
    </ThemeShell>
  );
}
