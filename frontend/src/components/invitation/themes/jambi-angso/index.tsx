"use client";
// Theme "Jambi Angso Duo" — sampul berupa sehelai batik Jambi (angso duo merah sepang, nila, kuning, malam canting)
// dengan panel kain krem bertepi tumpal; di dalam, senja di Batanghari dengan rumah Kajang Leko beratap lengkung
// perahu. Pembuka Islami (basmalah + salam). Angso duo adalah motif batik adat, bukan ornamen keagamaan.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Prata", "Work Sans:ital,wght@0,400;0,500;0,600;1,400", "Amiri:wght@400;700"];
// Painted by /tmp/pen/art/themes/jambi-angso.py (tools/art/themes in the repo).
const Art = makeArt("jambi-angso", { river: [780, 520], angso: [220, 201], divider: [300, 24] } as const);
const BISMILLAH = "بِسْمِ اللّٰهِ الرَّحْمٰنِ الرَّحِيْمِ";

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    arabic: BISMILLAH,
    kicker: "Assalamu'alaikum",
    title: "Warahmatullahi Wabarakatuh",
    intro: "Dengan memohon rahmat dan ridha Allah SWT, kami bermaksud menyelenggarakan pernikahan putra-putri kami. Merupakan kehormatan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"],
  couple: ["Angso Duo", "Kedua Mempelai"],
  count: ["Menghitung Hari", "Menuju Hari Bahagia"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Waktu & Tempat", "Rangkaian Acara"],
  story: ["Perjalanan", "Kisah Kami"],
  gallery: ["Galeri", "Momen Bahagia"],
  wishes: ["Doa & Kehadiran", "Ucapan & Konfirmasi"],
  gifts: ["Tanda Kasih", "Amplop Digital"],
  closing: { thanks: "Terimo Kasih", text: "Atas kehadiran dan doa restu Bapak/Ibu/Saudara/i, kami sekeluarga mengucapkan terima kasih. Semoga Allah membalas setiap kebaikan.", salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh" },
  sent: "Terimo kasih, doa dan ucapan Anda sudah terkirim.",
};

export default function JambiAngsoTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const hero = data.gallery[0] ?? data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#5a2218"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.panel}>
            <p className={s.arabicCover} lang="ar" dir="rtl">{BISMILLAH}</p>
            <p className={s.kicker}>Assalamu&apos;alaikum Wr. Wb.</p>
            {hero && <div className={s.egg}><Photo src={hero} alt="" /></div>}
            <p className={s.coverLabel}>{label}</p>
            <h1 className={s.coverNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
            <div className={s.guestWrap}>
              <div className={s.guest}>
                <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
                <strong>{guestLabel(data)}</strong>
                {table && <span className={s.table}>{table}</span>}
              </div>
              <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#f6ead2" />Buka Undangan</button>
            </div>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#f2cf74"
        dark="#1f2a4c"
        copy={COPY}
        hero={(
          <header className={s.hero}>
            <div className={s.heroScene}>
              <div className={s.heroText}>
                <p className={s.heroKicker}>Undangan {label}</p>
                <h1 className={s.heroNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
                <p className={s.heroDate}>{formatDate(data.date)}</p>
              </div>
            </div>
            {hero && <div className={s.heroPhoto}><Photo src={hero} alt="" /></div>}
            <Art name="angso" className={s.heroAngso} />
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="divider" className={s.divider} />,
          node: <Art name="angso" />,
          amp: <Art name="angso" />,
          closingDecor: <Art name="river" className={s.closingRiver} />,
          sentArt: <Art name="angso" />,
        }}
      />
    </ThemeShell>
  );
}
