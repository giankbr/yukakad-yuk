"use client";
// Theme "Tasbih Mutiara" — walimah syari tanpa foto: untaian mutiara yang dilukis (kilau lembut, pelangi tipis di tepinya),
// mawar cat air putih-blush dengan daun sage, dan medali cincin mutiara berisi monogram di atas kertas mutiara.
import { Lucide, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Italiana", "EB Garamond:ital,wght@0,400;0,500;1,400", "Pinyon Script", "Amiri:wght@400"];
// Painted by /tmp/pen/art/themes/tasbih-mutiara.py
const Art = makeArt("tasbih-mutiara", { strand: [780, 330], medallion: [600, 606], roses: [560, 456], divider: [340, 38], pearl: [64, 60] } as const);
const BISMILLAH = "بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ";

function initial(name?: string) {
  return (name ?? "").trim().slice(0, 1).toUpperCase();
}

function Medal({ bride, groom, label, eager }: { bride: string; groom: string; label?: string; eager?: boolean }) {
  const b = initial(bride), g = initial(groom);
  return (
    <div className={s.medal}>
      <Art name="medallion" eager={eager} />
      <div className={s.medalIn}>
        {label && <small>{label}</small>}
        <span className={s.mono}>{b}{g && <><i>&amp;</i>{g}</>}</span>
      </div>
    </div>
  );
}

export default function TasbihMutiaraTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Walimatul 'Ursy";
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const { bride, groom } = data.couple;

  return (
    <ThemeShell
      fonts={FONTS}
      background="#f7f4ee"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Art name="strand" eager className={s.strand} />
          <Art name="roses" eager className={s.rosesBL} />
          <Art name="roses" eager className={s.rosesBR} />
          <Medal bride={bride} groom={groom} label={label} eager />
          <p className={s.coverArabic} lang="ar" dir="rtl">{BISMILLAH}</p>
          <h1 className={s.coverNames}><span>{bride}</span>{groom && <><em>dan</em><span>{groom}</span></>}</h1>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.guestWrap}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#f7f4ee" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        noPhotos
        light="#f7f4ee"
        dark="#3e5644"
        copy={{
          ...DEFAULT_COPY,
          opening: {
            arabic: BISMILLAH,
            kicker: "Assalamu'alaikum Warahmatullahi Wabarakatuh",
            title: "Dengan Rahmat Allah",
            intro: "Dengan memohon rahmat dan rida Allah Subhanahu wa Ta'ala, kami bermaksud menyelenggarakan walimah pernikahan putra-putri kami. Merupakan kehormatan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
          },
          roles: ["Mempelai Wanita", "Mempelai Pria"],
          couple: ["Dua Butir, Satu Untaian", "Kedua Mempelai"],
          count: ["Menghitung Hari", "Menuju Hari Akad"],
          units: ["Hari", "Jam", "Menit", "Detik"],
          events: ["Waktu & Tempat", "Rangkaian Acara"],
          story: ["Dirangkai dengan Doa", "Perjalanan Kami"],
          gallery: ["Galeri", "Kenangan"],
          wishes: ["Doa & Kehadiran", "Ucapan & Konfirmasi"],
          gifts: ["Tanda Kasih", "Amplop Digital"],
          closing: {
            thanks: "Jazakumullah Khairan",
            text: "Atas kehadiran dan doa restu Bapak/Ibu/Saudara/i, kami ucapkan terima kasih. Semoga Allah membalas dengan kebaikan yang berlipat.",
            salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh",
          },
          sent: "Jazakumullah khairan, doa dan ucapan Anda sudah terkirim.",
        }}
        hero={(
          <header className={s.hero}>
            <Art name="strand" className={s.strand} />
            <div className={s.heroCard}>
              <Medal bride={bride} groom={groom} />
              <p className={s.heroKicker}>{label}</p>
              <h1 className={s.heroNames}>{bride}{groom && <><em>&amp;</em>{groom}</>}</h1>
              <p className={s.heroDate}>{formatDate(data.date)}</p>
              {note && <p className={s.heroNote}>{note}</p>}
              <Art name="roses" className={s.heroRoses} />
            </div>
          </header>
        )}
        slots={{
          divider: <Art name="divider" className={s.divider} />,
          amp: <Art name="pearl" />,
          portrait: <Art name="medallion" className={s.portraitRing} />,
          countDecor: <Art name="strand" className={s.countStrand} />,
          closingDecor: <Art name="strand" className={s.closingStrand} />,
          closingEmblem: <div className={s.closingEmblem}><Art name="medallion" /><span>{initial(bride)}{groom ? ` ${initial(groom)}` : ""}</span></div>,
          sentArt: <Art name="medallion" />,
        }}
      />
    </ThemeShell>
  );
}
