"use client";
// Theme "Dallah Kopi" — Arabian coffee hospitality: a brass dallah with a beak spout, porcelain finjan cups of golden
// qahwa with rising steam, a brass tray of dates on a majlis carpet (gouache with polished-brass shading). The cover
// is a lamplit majlis; the hero sets the couple's photo on an engraved brass tray. No figures in the ornament.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["El Messiri:wght@400;500;600;700", "Amiri:ital,wght@0,400;0,700;1,400"];
// Painted by /tmp/pen/art/themes/dallah-kopi.py (tools/art/themes in the repo).
const Art = makeArt("dallah-kopi", {
  still: [820, 476], dallah: [260, 344], finjan: [116, 111], date: [60, 33], ring: [400, 400], divider: [340, 37],
} as const);

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    arabic: "بِسْمِ اللّٰهِ الرَّحْمٰنِ الرَّحِيْمِ",
    kicker: "Assalamu'alaikum Warahmatullahi Wabarakatuh",
    title: "Ahlan wa Sahlan",
    intro: "Dengan memohon rahmat dan ridha Allah SWT, kami bermaksud menyelenggarakan walimah pernikahan putra-putri kami. Merupakan kehormatan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir di majelis kami dan memberikan doa restu.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"],
  couple: ["Bismillah, Kami Menikah", "Kedua Mempelai"],
  count: ["Menanti Hari Bahagia", "Hitung Mundur"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Waktu & Tempat", "Majelis Walimah"],
  story: ["Secangkir Cerita", "Kisah Kami"],
  gallery: ["Galeri", "Momen Bahagia"],
  wishes: ["Doa & Kehadiran", "Ucapan & Konfirmasi"],
  gifts: ["Tanda Kasih", "Amplop Digital"],
  closing: { thanks: "Jazakumullahu Khairan", text: "Atas kehadiran dan doa restu Bapak/Ibu/Saudara/i, kami sekeluarga mengucapkan terima kasih. Semoga Allah membalas kebaikan Anda dengan sebaik-baik balasan.", salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh" },
  sent: "Jazakumullahu khairan, doa dan ucapan Anda sudah terkirim.",
  closedNote: "Terima kasih atas doa dan perhatiannya. Ucapan untuk kedua mempelai masih bisa dikirim lewat form ini.",
};

export default function DallahKopiTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Walimatul 'Ursy";
  const hero = data.gallery[0] ?? data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const groom = data.couple.groom?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#24140c"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <p className={s.coverArabic} lang="ar" dir="rtl">بِسْمِ اللّٰهِ الرَّحْمٰنِ الرَّحِيْمِ</p>
          <p className={s.kicker}>{label}</p>
          <h1 className={s.coverNames}><span>{data.couple.bride}</span>{groom && <><em>&amp;</em><span>{groom}</span></>}</h1>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.guest}>
            <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
            <strong>{guestLabel(data)}</strong>
            {table && <span className={s.table}>{table}</span>}
          </div>
          <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={18} color="#24140c" />Buka Undangan</button>
          <div className={s.still} aria-hidden>
            <span className={s.steam} /><span className={s.steam} /><span className={s.steam} /><span className={s.steam} />
            <Art name="still" eager className={s.stillArt} />
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#fbecd0"
        dark="#24140c"
        copy={COPY}
        hero={(
          <header className={s.hero}>
            <p className={s.heroKicker}>{label}</p>
            {hero
              ? <div className={s.heroTray}><div className={s.heroPhoto}><Photo src={hero} alt="" /></div><Art name="ring" className={s.heroRing} /></div>
              : <Art name="dallah" className={s.heroDallah} />}
            <h1 className={s.heroNames}>{data.couple.bride}{groom && <><em>&amp;</em>{groom}</>}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
            <span className={s.heroCarpet} aria-hidden />
          </header>
        )}
        slots={{
          divider: <Art name="divider" className={s.divider} />,
          node: <Art name="date" />,
          amp: <Art name="date" />,
          closingEmblem: <Art name="dallah" className={s.closingDallah} />,
          sentArt: <Art name="finjan" />,
        }}
      />
    </ThemeShell>
  );
}
