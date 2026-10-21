"use client";
// Theme "Gebyok Sogan" — adat Jawa gading & cokelat sogan: gapura gebyok berukir lung-lungan dengan prada tembaga,
// kembar mayang emas, kabut pegunungan dan joglo cat air, serta rangkaian mawar & peoni. Sampul tanpa foto.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, JAWA_WISHES, JawiBody, ic, makeArt } from "../_jawi/body";
import s from "./styles.module.css";

const FONTS = ["Cormorant SC:wght@400;500;600", "EB Garamond:ital,wght@0,400;0,500;0,600;1,400", "Parisienne"];
// Painted by /tmp/pen/art/themes/gebyok-sogan.py (tools/art/themes in the repo).
const Art = makeArt("gebyok-sogan", { bouquet: [700, 325], emblem: [222, 467], gate: [720, 421], mist: [680, 410] } as const);

export default function GebyokSoganTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const hero = data.gallery[0];
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#34200f"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Art name="mist" eager className={s.mist} />
          <Art name="gate" eager className={s.gate} />
          <Art name="emblem" eager className={s.emblem} />
          <p className={s.kicker}>Undangan {label}</p>
          <h1 className={s.coverNames}><span>{data.couple.bride}</span><em>&amp;</em><span>{data.couple.groom}</span></h1>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <span className={`${s.strip} ${s.coverStrip}`} aria-hidden />
          <div className={s.coverFoot}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#f7eedf" />Buka Undangan</button>
          </div>
          <Art name="bouquet" eager className={s.bouquet} />
        </section>
      )}
    >
      <JawiBody
        {...props}
        demoWishes={JAWA_WISHES}
        s={s}
        light="#ecd3a4"
        dark="#4a2f19"
        copy={{ ...DEFAULT_COPY, opening: { ...DEFAULT_COPY.opening, kicker: "Sugeng Rawuh", title: "Nyuwun Donga Pangestu" } }}
        hero={(
          <header className={s.hero}>
            <Art name="mist" className={s.heroMist} />
            <Art name="gate" className={s.gate} />
            {hero ? (
              <div className={s.heroFrame}><Art name="emblem" className={s.heroEmblem} /><div className={s.heroPhoto}><Photo src={hero} alt="" /></div></div>
            ) : <Art name="emblem" className={s.closingEmblem} />}
            <p className={s.kickerDark}>Pahargyan Pawiwahan</p>
            <h1 className={s.heroNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
            <Art name="bouquet" className={s.heroBouquet} />
          </header>
        )}
        slots={{
          divider: <span className={`${s.strip} ${s.divider}`} aria-hidden />,
          node: <Art name="emblem" />,
          amp: <Art name="emblem" />,
          countDecor: <><span className={s.countStripT} aria-hidden /><span className={s.countStripB} aria-hidden /></>,
          closingDecor: <Art name="mist" className={s.closingMist} />,
          closingEmblem: <Art name="emblem" className={s.closingEmblem} />,
          sentArt: <Art name="emblem" />,
        }}
      />
    </ThemeShell>
  );
}
