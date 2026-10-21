"use client";
// Theme "Wayang Mega" — adat Jawa tanpa foto di atas kertas kraft: awan mega mendung bergradasi yang dilukis gouache,
// sepasang wayang kulit (desain orisinal) berlapis prada, medali ukir untuk monogram, dan pinggiran tumpal batik.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, JAWA_WISHES, JawiBody, ic, makeArt } from "../_jawi/body";
import s from "./styles.module.css";

const FONTS = ["Marcellus SC", "Lora:ital,wght@0,400;0,500;0,600;1,400", "Sacramento"];
// Painted by /tmp/pen/art/themes/wayang-mega.py (tools/art/themes in the repo).
const Art = makeArt("wayang-mega", { "mega-a": [560, 191], "mega-b": [420, 143], putra: [151, 579], putri: [99, 561] } as const);

function Stage({ initials, className, eager }: { initials: string; className: string; eager?: boolean }) {
  return (
    <div className={className} aria-hidden>
      <Art name="putra" eager={eager} className={s.wayL} />
      <span className={s.stageMedal}>{initials}</span>
      <Art name="putri" eager={eager} className={s.wayR} />
    </div>
  );
}

export default function WayangMegaTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const table = tableLabel(data.guestTable);
  const initials = `${data.couple.bride.slice(0, 1)}${data.couple.groom.slice(0, 1)}`;

  return (
    <ThemeShell
      fonts={FONTS}
      background="#4a1d0f"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Art name="mega-a" eager className={s.megaA} />
          <Art name="mega-b" eager className={s.megaB} />
          <Art name="mega-a" eager className={s.megaC} />
          <p className={s.salam}>Sugeng Rawuh</p>
          <p className={s.kicker}>Undangan {label}</p>
          <h1 className={s.coverNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.guestWrap}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#f7ecd6" />Buka Undangan</button>
          </div>
          <div className={s.stage}>
            <Stage initials={initials} className={s.stageInner} eager />
            <span className={s.strip} aria-hidden />
          </div>
        </section>
      )}
    >
      <JawiBody
        {...props}
        demoWishes={JAWA_WISHES}
        s={s}
        noPhotos
        light="#f1d79a"
        dark="#4a1d0f"
        copy={{ ...DEFAULT_COPY, opening: { ...DEFAULT_COPY.opening, kicker: "Lakon Katresnan", title: "Nyuwun Pangestu" } }}
        hero={(
          <header className={s.hero}>
            <Art name="mega-a" className={s.megaA} />
            <Art name="mega-b" className={s.megaB} />
            {data.gallery[0] ? <div className={s.heroPhoto}><Photo src={data.gallery[0]} alt="" /></div> : <div className={s.heroMedal} aria-hidden>{initials}</div>}
            <p className={s.kickerDark}>Pahargyan Pawiwahan</p>
            <h1 className={s.heroNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            <span className={`${s.strip} ${s.heroStrip}`} aria-hidden />
          </header>
        )}
        slots={{
          divider: <span className={`${s.strip} ${s.divider}`} aria-hidden />,
          node: <Art name="mega-b" />,
          amp: <Art name="mega-b" />,
          countDecor: <><Art name="mega-a" className={`${s.countMega} ${s.countMegaL}`} /><Art name="mega-b" className={`${s.countMega} ${s.countMegaR}`} /></>,
          closingEmblem: <Stage initials={initials} className={s.closingStage} />,
          sentArt: <Art name="mega-a" />,
        }}
      />
    </ThemeShell>
  );
}
