"use client";
// Theme "Letterpress" — cetak timbul satu tinta merah marun di atas kertas katun tebal: huruf Bodoni yang tertekan
// (bayangan impresi), karangan daun blind deboss tanpa tinta, fleuron hedera dan garis ornamen, composing stick berisi
// huruf timah di bawah kartu sampul, kartu acara bergaris ganda, formulir balasan bergaris, dan pita tinta penuh.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Bodoni Moda:ital,wght@0,400;0,600;1,400", "Sorts Mill Goudy:ital@0;1", "Cormorant SC:wght@500;600"];
// Painted by /tmp/pen/art/themes/letterpress.py (cotton paper tile is a CSS background)
const Art = makeArt("letterpress", { stick: [720, 141], sort: [130, 211], fleuron: [111, 120], rule: [340, 39], wreath: [420, 383] } as const);

export default function LetterpressTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const { bride, groom } = data.couple;
  const table = tableLabel(data.guestTable);
  const photo = data.gallery[0];
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#e7dfd1"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.sheet}>
            <p className={s.colophon}>undangan pernikahan</p>
            <div className={s.wreathBox}>
              <Art name="wreath" eager className={s.wreath} />
              <h1 className={s.coverNames}><span>{bride}</span><em>dan</em><span>{groom}</span></h1>
            </div>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
            <Art name="rule" eager className={s.coverRule} />
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#f3eee4" />Buka Undangan</button>
          </div>
          <Art name="stick" eager className={s.stick} />
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#f3eee4"
        dark="#6e1a24"
        copy={{
          ...DEFAULT_COPY,
          opening: {
            kicker: "dengan hormat",
            title: "Kabar Bahagia",
            intro: "Dengan penuh syukur kepada Tuhan Yang Maha Esa, kami bermaksud menyelenggarakan pernikahan kami. Merupakan kehormatan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
          },
          roles: ["Mempelai Wanita", "Mempelai Pria"],
          couple: ["yang berbahagia", "Kedua Mempelai"],
          count: ["menuju hari itu", "Hitung Mundur"],
          units: ["Hari", "Jam", "Menit", "Detik"],
          events: ["waktu & tempat", "Rangkaian Acara"],
          story: ["tersusun huruf demi huruf", "Kisah Kami"],
          gallery: ["lembar kenangan", "Galeri"],
          wishes: ["mohon balasan", "Ucapan & Konfirmasi"],
          gifts: ["tanda kasih", "Hadiah Pernikahan"],
          closing: { thanks: "Terima Kasih", text: "Atas kehadiran dan doa restu Bapak/Ibu/Saudara/i, kami ucapkan terima kasih yang tertulis paling dalam." },
          sent: "Terima kasih. Balasan Anda sudah kami terima.",
          attend: { maybe: "Mungkin" },
        }}
        hero={(
          <header className={s.hero}>
            <p className={s.heroKicker}>sebuah kabar, dicetak dengan tangan</p>
            {photo ? <div className={s.heroFrame}><div className={s.heroPhoto}><Photo src={photo} alt={`${bride} & ${groom}`} /></div></div> : <Art name="wreath" className={s.heroBlind} />}
            <h1 className={s.heroNames}>{bride} <em>dan</em> {groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            <Art name="rule" className={s.divider} />
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="rule" className={s.divider} />,
          node: <Art name="fleuron" />,
          amp: <Art name="fleuron" />,
          closingEmblem: <Art name="sort" className={s.emblem} />,
          sentArt: <Art name="fleuron" />,
        }}
      />
    </ThemeShell>
  );
}
