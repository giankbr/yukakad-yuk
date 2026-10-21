"use client";
// Theme "Joglo Marun" — adat Jawa krem & marun: bingkai ukir gebyok berlapis prada, joglo cat air samar,
// dan rangkaian mawar merah, roncean melati, serta anggrek putih yang dilukis tangan.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { JawiBody, ic, makeArt } from "../_jawi/body";
import s from "./styles.module.css";

const FONTS = ["Marcellus", "Cormorant Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500", "Pinyon Script"];
// Painted by /tmp/pen/art/themes/joglo-marun.py (tools/art/themes in the repo).
const Art = makeArt("joglo-marun", { bouquet: [600, 676], cluster: [371, 291], frame: [560, 936], joglo: [640, 452], sprig: [307, 63] } as const);

export default function JogloMarunTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const hero = data.gallery[0];
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#3a0f13"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Art name="cluster" eager className={s.clusterL} />
          <Art name="cluster" eager className={s.clusterR} />
          <div className={s.panel}>
            <div className={s.panelInner}><Art name="joglo" eager className={s.panelJoglo} /></div>
            <Art name="frame" eager className={s.frame} />
            <div className={s.coverBody}>
              <div className={s.coverPhoto}><Photo src={hero} alt="" /></div>
              <p className={s.kicker}>Undangan {label}</p>
              <h1 className={s.coverNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
              <p className={s.coverDate}>{formatDate(data.date)}</p>
            </div>
          </div>
          <div className={s.coverFoot}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#f6e5c4" />Buka Undangan</button>
          </div>
          <Art name="bouquet" eager className={s.bouquetL} />
          <Art name="bouquet" eager className={s.bouquetR} />
        </section>
      )}
    >
      <JawiBody
        {...props}
        s={s}
        light="#ecd394"
        dark="#4a1016"
        hero={(
          <header className={s.hero}>
            <Art name="joglo" className={s.heroJoglo} />
            <div className={s.heroArch}>
              <div className={s.heroPhoto}><Photo src={hero} alt="" /></div>
              <Art name="frame" className={s.frame} />
            </div>
            <Art name="sprig" className={s.heroSprig} />
            <p className={s.kickerDark}>Pahargyan Pawiwahan</p>
            <h1 className={s.heroNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="sprig" className={s.divider} />,
          node: <Art name="cluster" />,
          amp: <Art name="sprig" />,
          portrait: <Art name="cluster" className={s.portraitArt} />,
          countDecor: <><Art name="cluster" className={s.countDecorL} /><Art name="cluster" className={s.countDecorR} /></>,
          closingDecor: <><Art name="joglo" className={s.closingJoglo} /><Art name="bouquet" className={s.closingBouquetL} /><Art name="bouquet" className={s.closingBouquetR} /></>,
          closingEmblem: <Art name="sprig" className={s.closingEmblem} />,
          sentArt: <Art name="cluster" />,
        }}
      />
    </ThemeShell>
  );
}
