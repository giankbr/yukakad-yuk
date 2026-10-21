"use client";
// Theme "Terrazzo Modern" — a polished terrazzo slab (sage, terracotta, sand and marble chips in cream cement) with
// Bauhaus-ish gouache arches, discs and half-moons on an asymmetric, left-aligned grid set in a clean sans.
import { Lucide, Photo, ThemeShell, dateParts, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Outfit:wght@300;400;500;600", "Fraunces:ital,wght@1,400"];
// Painted by /tmp/pen/art/themes/terrazzo-modern.py (tools/art/themes in the repo).
const Art = makeArt("terrazzo-modern", { arch: [300, 426], disc: [220, 221], half: [260, 131], row: [260, 42] } as const);

const COPY = {
  ...DEFAULT_COPY,
  opening: {
    arabic: "بِسْمِ اللّٰهِ الرَّحْمٰنِ الرَّحِيْمِ",
    kicker: "Assalamu'alaikum Warahmatullahi Wabarakatuh",
    title: "Dengan penuh syukur",
    intro: "Dengan memohon rahmat dan ridha Allah SWT, kami bermaksud menyelenggarakan pernikahan kami. Kehadiran dan doa Bapak/Ibu/Saudara/i akan melengkapi hari kami.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"] as [string, string],
  couple: ["Kami berdua", "Mempelai"] as [string, string],
  count: ["Menuju hari H", "Hitung mundur"] as [string, string],
  units: ["Hari", "Jam", "Menit", "Detik"] as [string, string, string, string],
  events: ["Jadwal", "Waktu & tempat"] as [string, string],
  story: ["Cerita", "Perjalanan kami"] as [string, string],
  gallery: ["Galeri", "Potret"] as [string, string],
  wishes: ["RSVP", "Ucapan & kehadiran"] as [string, string],
  gifts: ["Hadiah", "Amplop digital"] as [string, string],
  closing: { thanks: "Terima kasih", text: "Merupakan kebahagiaan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.", salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh" },
  sent: "Terima kasih! Ucapan dan doa Anda sudah terkirim.",
};

export default function TerrazzoModernTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const photo = data.gallery[0] ?? data.couple.bridePhoto ?? data.couple.groomPhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const d = dateParts(data.date);
  const short = d.day ? `${d.day.padStart(2, "0")} ${d.monthShort} ${d.year}` : "";
  const first = data.events[0];

  return (
    <ThemeShell
      fonts={FONTS}
      background="#e4dccd"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.coverTop}><span>{data.eventLabel ?? "Pernikahan"}</span>{short && <b>{short}</b>}</div>
          <div className={s.coverStage} aria-hidden>
            <Art name="arch" eager className={s.cArchArt} />
            {photo && <div className={s.coverPhoto}><Photo src={photo} alt="" /></div>}
            <Art name="half" eager className={s.cHalfArt} />
            <Art name="disc" eager className={s.cDiscArt} />
          </div>
          <h1 className={s.coverNames}>{data.couple.bride}<br /><em>&amp;</em> {data.couple.groom}</h1>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.guestBox}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#fbf8f2" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#fbf8f2"
        dark="#2f2b28"
        copy={COPY}
        hero={(
          <header className={s.hero}>
            {photo && <div className={s.heroPhoto}><Photo src={photo} alt={`${data.couple.bride} & ${data.couple.groom}`} /></div>}
            {photo && <Art name="disc" className={s.heroDisc} />}
            <div className={s.heroText}>
              <p className={s.heroKicker}>The Wedding</p>
              <h1 className={s.heroNames}>{data.couple.bride} <em>&amp;</em> {data.couple.groom}</h1>
              <dl className={s.heroMeta}>
                <dt>Tanggal</dt><dd>{formatDate(data.date)}</dd>
                {(data.place || first?.venue) && <><dt>Tempat</dt><dd>{data.place || first?.venue}</dd></>}
              </dl>
              {note && <p className={s.heroNote}>{note}</p>}
            </div>
          </header>
        )}
        slots={{
          divider: <Art name="row" className={s.divider} />,
          portrait: <Art name="disc" className={s.portraitDot} />,
          countDecor: <Art name="half" className={s.countHalf} />,
          closingEmblem: (
            <div className={s.closingShapes} aria-hidden>
              <Art name="arch" className={s.cArch} />
              <Art name="half" className={s.cHalf} />
              <Art name="disc" className={s.cDisc} />
            </div>
          ),
          sentArt: <Art name="row" />,
        }}
      />
    </ThemeShell>
  );
}
