"use client";
// Theme "Aurora Utara" — a northern night: painted starry sky, green-violet aurora curtains (a separate painted layer in
// screen blend that drifts slowly), snowy ridges, snow-laden pines and a frozen lake. The couple's photo hangs in the
// sky as a round moon; portraits are moons with an aurora ring, cards are frosted ice panes with a glowing top line.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Bellefair:wght@400", "Mulish:wght@400;600;700"];
// Painted by /tmp/pen/art/themes/aurora-utara.py (langit.webp + aurora.webp are CSS backgrounds)
const Art = makeArt("aurora-utara", { hutan: [620, 468], pinus: [160, 136] } as const);

export default function AuroraUtaraTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const photo = data.gallery[0] || data.couple.bridePhoto || data.couple.groomPhoto;

  return (
    <ThemeShell
      fonts={FONTS}
      background="#08121f"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <span className={s.coverAurora} aria-hidden />
          <div className={s.coverForest} aria-hidden><Art name="hutan" eager /></div>
          {photo ? <div className={s.moon}><Photo src={photo} alt={`${data.couple.bride} & ${data.couple.groom}`} /></div> : <span className={`${s.moon} ${s.moonEmpty}`} aria-hidden />}
          <div className={s.coverBody}>
            <p className={s.kicker}>The Wedding of</p>
            <h1 className={s.names}>{data.couple.bride}<span>&amp;</span>{data.couple.groom}</h1>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
          </div>
          <div className={s.guestWrap}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={15} color="#0c1828" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#8ef0c4"
        dark="#0c1828"
        copy={{
          ...DEFAULT_COPY,
          opening: {
            kicker: "Dengan penuh sukacita",
            title: "Di Bawah Langit yang Sama",
            intro: "Seperti cahaya utara yang datang setelah malam panjang, kami percaya hal terindah layak dinanti. Dengan bahagia kami mengundang Bapak/Ibu/Saudara/i untuk hadir dan menjadi saksi hari pernikahan kami.",
          },
          roles: ["Mempelai Wanita", "Mempelai Pria"],
          couple: ["Dua Hati", "Kedua Mempelai"],
          count: ["Menanti Malam Itu", "Hitung Mundur"],
          units: ["Hari", "Jam", "Menit", "Detik"],
          events: ["Waktu & Tempat", "Rangkaian Acara"],
          story: ["Perjalanan", "Kisah Kami"],
          gallery: ["Galeri", "Cahaya & Kenangan"],
          wishes: ["Ucapan & Kehadiran", "Kirim Doa & Ucapan"],
          gifts: ["Tanda Kasih", "Amplop Digital"],
          closing: { thanks: "Terima Kasih", text: "Kehadiran dan doa Bapak/Ibu/Saudara/i adalah cahaya paling hangat di malam bahagia kami." },
          sent: "Terima kasih, ucapan Anda sudah kami terima dengan hangat.",
          attend: { maybe: "Mungkin" },
          wishPlaceholder: "Tuliskan ucapan dan doa untuk kami berdua…",
        }}
        hero={(
          <header className={s.hero}>
            <span className={s.heroAurora} aria-hidden />
            <p className={s.heroKicker}>{data.eventLabel ?? "Pernikahan"}</p>
            {photo && <div className={s.heroPhoto}><Photo src={photo} alt={`${data.couple.bride} & ${data.couple.groom}`} /></div>}
            <h1 className={s.heroNames}>{data.couple.bride} <span>&amp;</span> {data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <span className={s.divider} aria-hidden><Art name="pinus" /></span>,
          node: <Art name="pinus" />,
          amp: <Art name="pinus" />,
          countDecor: <span className={s.countAurora} aria-hidden />,
          closingDecor: <><span className={s.closingAurora} aria-hidden /><Art name="hutan" className={s.closingForest} /></>,
          closingEmblem: <Art name="pinus" className={s.closingPine} />,
          sentArt: <Art name="pinus" />,
        }}
      />
    </ThemeShell>
  );
}
