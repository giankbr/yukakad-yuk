"use client";
// Theme "Batik Kontemporer" — batik tulis yang dibaca ulang secara kontemporer: parang raksasa jingga di atas kobalt dengan
// lereng mint, kawung besar, mega mendung bergradasi; semuanya kain celup dengan garis malam dan retakan. Tata letak grid
// Swiss: garis tebal, nomor bagian, huruf grotesk tebal rata kiri.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Bricolage Grotesque:opsz,wght@12..96,400;12..96,600;12..96,700;12..96,800", "DM Sans:wght@400;500;700", "Space Mono:wght@400;700"];
// Painted by /tmp/pen/art/themes/batik-kontemporer.py (tools/art/themes in the repo).
const Art = makeArt("batik-kontemporer", { kawung: [320, 320], mega: [420, 220], row: [320, 43] } as const);
// Lucide "arrow-right" (ISC license).
const ARROW = "<path d=\"M5 12h14\" /> <path d=\"m12 5 7 7-7 7\" />";

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    arabic: "بِسْمِ اللّٰهِ الرَّحْمٰنِ الرَّحِيْمِ",
    kicker: "Assalamu'alaikum Warahmatullahi Wabarakatuh",
    title: "Dua Garis, Satu Kain",
    intro: "Dengan memohon rahmat dan ridha Allah SWT, kami bermaksud menyelenggarakan pernikahan kami. Merupakan kehormatan dan kebahagiaan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"],
  couple: ["Mempelai", "Yang Berbahagia"],
  count: ["Hitung Mundur", "Menuju Hari H"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Agenda", "Waktu & Tempat"],
  story: ["Perjalanan", "Cerita Kami"],
  gallery: ["Galeri", "Potret"],
  wishes: ["Buku Tamu", "Doa & Kehadiran"],
  gifts: ["Tanda Kasih", "Amplop Digital"],
  closing: { thanks: "Terima kasih.", text: "Kehadiran dan doa restu Bapak/Ibu/Saudara/i adalah kehormatan dan kebahagiaan bagi kami sekeluarga.", salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh" },
  sent: "Terima kasih, doa dan ucapan Anda sudah kami terima.",
};

export default function BatikKontemporerTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const table = tableLabel(data.guestTable);
  const photo = data.gallery[0] ?? data.couple.bridePhoto;
  const note = data.couple.note?.trim();
  const numeric = formatDate(data.date, { day: "2-digit", month: "2-digit", year: "numeric" }).replace(/\//g, ".");
  const first = data.events[0];
  const last = data.events[data.events.length - 1];

  return (
    <ThemeShell
      fonts={FONTS}
      background="#e6dfcf"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <p className={s.bar}><span>Undangan {label}</span><span>{numeric}</span></p>
          <div className={s.blocks} aria-hidden>
            <div className={s.parangBlock} />
            <div className={s.photoBlock}>{photo && <Photo src={photo} alt="" />}</div>
            <span className={s.kawungWrap}><Art name="kawung" eager /></span>
          </div>
          <h1 className={s.coverNames}><span>{data.couple.bride}</span><em>dan</em><span>{data.couple.groom}</span></h1>
          <p className={s.coverMeta}><span>{formatDate(data.date)}</span>{data.place && <span>{data.place}</span>}</p>
          <div className={s.guestWrap}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}>
              <span><Lucide icon={ic.mailOpen} size={16} color="#f6f1e6" />Buka Undangan</span><Lucide icon={ARROW} size={18} color="#f6f1e6" />
            </button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        copy={COPY}
        light="#f6f1e6"
        dark="#121a3a"
        hero={(
          <header className={s.hero}>
            <div className={s.heroGrid}>
              {photo ? <div className={s.heroPhoto}><Photo src={photo} alt="" /></div> : <div className={s.heroArt} aria-hidden />}
              <div className={s.heroSide} aria-hidden>
                <span><Art name="kawung" /></span>
                <span />
                <span />
              </div>
            </div>
            <p className={s.kickerDark}>Undangan {label}</p>
            <h1 className={s.heroNames}>{data.couple.bride} <em>&amp;</em> {data.couple.groom}</h1>
            <div className={s.heroMeta}>
              <p><b>Tanggal</b>{numeric}</p>
              <p><b>Tempat</b>{data.place || "Segera diumumkan"}</p>
              {first?.time && <p><b>{first.name}</b>{first.time}</p>}
              {last && last !== first && last.time && <p><b>{last.name}</b>{last.time}</p>}
            </div>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="row" className={s.divider} />,
          node: <Art name="kawung" />,
          countDecor: <Art name="mega" className={s.cloud} />,
          closingEmblem: <><span className={s.closingBand} aria-hidden /><Art name="kawung" className={s.closingKawung} /></>,
          sentArt: <Art name="kawung" />,
        }}
      />
    </ThemeShell>
  );
}
