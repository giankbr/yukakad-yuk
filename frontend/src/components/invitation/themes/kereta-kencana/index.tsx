"use client";
// Theme "Kereta Kencana" — kemegahan keraton Solo-Jogja dalam hijau tua dan emas: kereta kencana bergaya gouache
// berlapis prada, sepasang payung agung, mahkota ala paes di atas nama, dan sudut ukir emas di atas beludru.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, JawiBody, ic, makeArt } from "../_jawi/body";
import s from "./styles.module.css";

const FONTS = ["Cinzel:wght@400;500", "Cinzel Decorative:wght@400", "Cormorant Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500", "Great Vibes"];
// Painted by /tmp/pen/art/themes/kereta-kencana.py (tools/art/themes in the repo).
const Art = makeArt("kereta-kencana", { corner: [160, 159], kereta: [640, 453], paes: [360, 118], payung: [200, 453] } as const);

function Stage({ className, eager }: { className: string; eager?: boolean }) {
  return (
    <div className={className} aria-hidden>
      <Art name="payung" eager={eager} className={s.payungL} />
      <Art name="kereta" eager={eager} className={s.kereta} />
      <Art name="payung" eager={eager} className={s.payungR} />
    </div>
  );
}

export default function KeretaKencanaTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const hero = data.gallery[0];
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#0a1d17"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Art name="corner" eager className={s.cornerTL} />
          <Art name="corner" eager className={s.cornerTR} />
          <Art name="paes" eager className={s.paes} />
          <p className={s.kicker}>Pahargyan Dalem · {label}</p>
          <h1 className={s.coverNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.guestWrap}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#0f2a22" />Buka Undangan</button>
          </div>
          <Stage className={s.stage} eager />
        </section>
      )}
    >
      <JawiBody
        {...props}
        s={s}
        light="#f0d895"
        dark="#0f2a22"
        copy={{ ...DEFAULT_COPY, opening: { ...DEFAULT_COPY.opening, kicker: "Sugeng Rawuh", title: "Nyuwun Pangestu" }, closing: { ...DEFAULT_COPY.closing, thanks: "Matur Sembah Nuwun" } }}
        hero={(
          <header className={s.hero}>
            <Art name="paes" className={s.paes} />
            {hero && <div className={s.heroPhoto}><Photo src={hero} alt="" /></div>}
            <p className={s.kickerDark}>Pahargyan Dalem</p>
            <h1 className={s.heroNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
            <Art name="kereta" className={s.heroKereta} />
          </header>
        )}
        slots={{
          divider: <Art name="paes" className={s.divider} />,
          node: <Art name="paes" />,
          amp: <Art name="paes" />,
          countDecor: <><Art name="corner" className={`${s.countCorner} ${s.countCornerL}`} /><Art name="corner" className={`${s.countCorner} ${s.countCornerR}`} /></>,
          closingEmblem: <Stage className={s.closingStage} />,
          sentArt: <Art name="paes" />,
        }}
      />
    </ThemeShell>
  );
}
