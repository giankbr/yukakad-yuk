"use client";
// Theme "Kawung Biru" — adat Jawa biru nila bergaya toile: pepohonan berukir, joglo, sepasang wayang dengan tatahan,
// bingkai motif kawung, serta lili biru dan anggrek putih yang dilukis tangan.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, JAWA_WISHES, JawiBody, ic, makeArt } from "../_jawi/body";
import s from "./styles.module.css";

const FONTS = ["Cinzel:wght@400;500", "Cormorant Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500", "Italianno"];
// Painted by /tmp/pen/art/themes/kawung-biru.py (tools/art/themes in the repo).
const Art = makeArt("kawung-biru", { divider: [323, 45], joglo: [620, 512], lily: [480, 349], wayang: [154, 580] } as const);

export default function KawungBiruTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const hero = data.gallery[0];
  const table = tableLabel(data.guestTable);

  return (
    <ThemeShell
      fonts={FONTS}
      background="#1c2740"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <span className={s.borderL} aria-hidden />
          <span className={s.borderR} aria-hidden />
          <Art name="lily" eager className={s.lilyL} />
          <Art name="lily" eager className={s.lilyR} />
          <div className={s.coverPhoto}><Photo src={hero} alt="" /></div>
          <p className={s.kicker}>Undangan {label}</p>
          <h1 className={s.coverNames}>{data.couple.bride} <em>&amp;</em> {data.couple.groom}</h1>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.guestWrap}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#eef2f8" />Buka Undangan</button>
          </div>
          <div className={s.stage} aria-hidden>
            <Art name="wayang" eager className={s.wayangL} />
            <Art name="wayang" eager className={s.wayangR} />
            <Art name="joglo" eager className={s.coverJoglo} />
          </div>
          <Art name="lily" eager className={s.lilyBL} />
          <Art name="lily" eager className={s.lilyBR} />
        </section>
      )}
    >
      <JawiBody
        {...props}
        demoWishes={JAWA_WISHES}
        s={s}
        light="#dfe6f4"
        dark="#223150"
        copy={{ ...DEFAULT_COPY, opening: { ...DEFAULT_COPY.opening, title: "Sugeng Rawuh", kicker: "Kawung · Kesucian & Harapan" } }}
        hero={(
          <header className={s.hero}>
            <span className={s.heroScene} aria-hidden />
            <Art name="lily" className={s.heroLilyL} />
            <Art name="lily" className={s.heroLilyR} />
            <div className={s.heroPhoto}><Photo src={hero} alt="" /></div>
            <p className={s.kickerDark}>Pahargyan Pawiwahan</p>
            <h1 className={s.heroNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            <Art name="joglo" className={s.heroJoglo} />
          </header>
        )}
        slots={{
          divider: <Art name="divider" className={s.divider} />,
          node: <Art name="divider" />,
          amp: <Art name="divider" />,
          portrait: <Art name="lily" className={s.portraitArt} />,
          countDecor: <span className={s.countKawung} aria-hidden />,
          closingDecor: <span className={s.closingKawung} aria-hidden />,
          closingEmblem: (
            <div className={s.closingStage} aria-hidden>
              <Art name="wayang" className={s.wayangL} />
              <Art name="wayang" className={s.wayangR} />
              <Art name="joglo" className={s.coverJoglo} />
            </div>
          ),
          sentArt: <Art name="lily" />,
        }}
      />
    </ThemeShell>
  );
}
