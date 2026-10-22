"use client";
// Theme "Hydrangea Biru" — airy cool watercolour: lush blue-violet mophead hydrangeas, each painted from hundreds of
// four-petal florets, with sage leaves and a dusty-blue silk ribbon whose sheen is painted in; oval portraits,
// ribbon-tab event cards and cobalt bands.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, toDate, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Cormorant Garamond:ital,wght@0,500;0,600;1,500", "Mulish:wght@400;600;700", "Pinyon Script", "Amiri"];
// Painted by /tmp/pen/art/themes/hydrangea-biru.py (tools/art/themes in the repo).
const Art = makeArt("hydrangea-biru", { spray: [420, 330], posy: [400, 254], bloom: [260, 235], sprig: [110, 95], ribbon: [360, 48], bow: [200, 163] } as const);

const COPY = {
  ...DEFAULT_COPY,
  opening: {
    arabic: "بِسْمِ اللّٰهِ الرَّحْمٰنِ الرَّحِيْمِ",
    kicker: "Assalamu'alaikum Warahmatullahi Wabarakatuh",
    title: "Bismillah, dengan Rahmat-Nya",
    intro: "Maha Suci Allah yang telah menciptakan makhluk-Nya berpasang-pasangan. Dengan memohon rahmat dan ridha Allah SWT, kami bermaksud menyelenggarakan pernikahan putra-putri kami dan mengharap kehadiran serta doa restu Bapak/Ibu/Saudara/i.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"] as [string, string],
  couple: ["Dengan Ridha-Nya", "Kedua Mempelai"] as [string, string],
  count: ["Menghitung Hari", "Menuju Hari Bahagia"] as [string, string],
  units: ["Hari", "Jam", "Menit", "Detik"] as [string, string, string, string],
  events: ["Waktu & Tempat", "Rangkaian Acara"] as [string, string],
  story: ["Kisah Kami", "Tumbuh Bersama"] as [string, string],
  gallery: ["Galeri", "Di Antara Hortensia"] as [string, string],
  wishes: ["Doa & Kehadiran", "Kirim Doa Restu"] as [string, string],
  gifts: ["Tanda Kasih", "Amplop Digital"] as [string, string],
  closing: {
    thanks: "Jazakumullah Khairan",
    text: "Merupakan kehormatan dan kebahagiaan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
    salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh",
  },
  sent: "Jazakumullah khairan, doa dan ucapan Anda sudah kami terima.",
};

export default function HydrangeaBiruTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const photo = data.gallery[0] ?? data.couple.bridePhoto ?? data.couple.groomPhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const year = toDate(data.date)?.getFullYear();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#e3e8f3"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.oval} aria-hidden>
            <div className={s.ovalPhoto}>{photo ? <Photo src={photo} alt="" /> : <div />}</div>
            <Art name="spray" eager className={s.spray} />
            <Art name="posy" eager className={s.posy} />
          </div>
          <p className={s.kicker}>Undangan Pernikahan</p>
          <h1 className={s.coverNames}><span>{data.couple.bride}</span><em>&amp;</em><span>{data.couple.groom}</span></h1>
          <p className={s.coverDate}><span aria-hidden />{formatDate(data.date)}<span aria-hidden /></p>
          <div className={s.guest}>
            <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
            <strong>{guestLabel(data)}</strong>
            {table && <span className={s.table}>{table}</span>}
          </div>
          <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={15} color="#ffffff" />Buka Undangan</button>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#f1f4fc"
        dark="#252c52"
        copy={COPY}
        hero={(
          <header className={s.hero}>
            <p className={s.heroKicker}>{year ? `${label} · ${year}` : label}</p>
            <div className={s.heroFrame}>
              {photo && <div className={s.heroPhoto}><Photo src={photo} alt={`${data.couple.bride} & ${data.couple.groom}`} /></div>}
              <Art name="spray" className={s.heroSpray} />
              <Art name="bow" className={s.heroBow} />
            </div>
            <h1 className={s.heroNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="ribbon" className={s.divider} />,
          node: <Art name="sprig" />,
          amp: <Art name="sprig" />,
          portrait: <Art name="sprig" className={s.portraitBloom} />,
          countDecor: <Art name="bloom" className={s.countDeco} />,
          closingEmblem: <span className={s.closeBloom}><Art name="bloom" /></span>,
          sentArt: <Art name="bow" />,
        }}
      />
    </ThemeShell>
  );
}
