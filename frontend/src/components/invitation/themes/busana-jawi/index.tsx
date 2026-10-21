"use client";
// Theme "Busana Jawi" — foto penuh pasangan berbusana adat Jawa dengan tulisan putih yang tenang, pita batik parang
// berlapis emas, ornamen kembang goyang, dan latar kain sogan bermotif truntum.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, JawiBody, ic, makeArt } from "../_jawi/body";
import s from "./styles.module.css";

const FONTS = ["Cinzel:wght@400;500", "Cormorant Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500", "Pinyon Script"];
// Painted by /tmp/pen/art/themes/busana-jawi.py (tools/art/themes in the repo).
const Art = makeArt("busana-jawi", { ornament: [234, 233] } as const);
/** Fallback cover photo: a couple in Javanese attire (replaced by the couple's own first photo). */
const DEFAULT_PHOTO = "/themes/img/a34.webp";

export default function BusanaJawiTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const cover = data.gallery[0] ?? DEFAULT_PHOTO;
  const hero = data.gallery[1] ?? cover;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#1d140e"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.coverPhoto}><Photo src={cover} alt="" /></div>
          <div className={s.coverTop}>
            <span className={s.band} aria-hidden />
            <p className={s.kickerScript}>Pahargyan Pawiwahan</p>
          </div>
          <Art name="ornament" eager className={s.ornament} />
          <h1 className={s.coverNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <span className={`${s.band} ${s.coverRule}`} aria-hidden />
          <div className={s.guest}>
            <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
            <strong>{guestLabel(data)}</strong>
            {table && <span className={s.table}>{table}</span>}
          </div>
          <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#24180f" />Buka Undangan</button>
        </section>
      )}
    >
      <JawiBody
        {...props}
        s={s}
        light="#ead19a"
        dark="#24180f"
        copy={{ ...DEFAULT_COPY, opening: { ...DEFAULT_COPY.opening, kicker: label, title: "Sugeng Rawuh" } }}
        hero={(
          <header className={s.hero}>
            <div className={s.heroPhoto}><Photo src={hero} alt="" /></div>
            <div className={s.heroBody}>
              <Art name="ornament" className={s.ornament} />
              <p className={s.kickerDark}>Dhaup Ageng</p>
              <h1 className={s.heroNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
              <p className={s.heroDate}>{formatDate(data.date)}</p>
              {note && <p className={s.heroNote}>{note}</p>}
            </div>
            <span className={`${s.band} ${s.heroBand}`} aria-hidden />
          </header>
        )}
        slots={{
          divider: <span className={`${s.band} ${s.divider}`} aria-hidden />,
          node: <Art name="ornament" />,
          amp: <Art name="ornament" />,
          closingEmblem: <Art name="ornament" className={s.closingEmblem} />,
          sentArt: <Art name="ornament" />,
        }}
      />
    </ThemeShell>
  );
}
