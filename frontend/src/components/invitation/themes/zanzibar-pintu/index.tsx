"use client";
// Theme "Zanzibar Pintu" — walimah bernuansa pesisir Swahili: pintu jati berukir (rantai bertaut, sulur daun, teratai,
// roset) dengan daun pintu bertabur paku kuningan, dinding batu karang berkapur putih, dan perahu dhow berlayar di
// laut toska. Sampul menaruh nama mempelai pada plakat di daun pintu yang tertutup, foto pembuka terlihat dari balik
// kusen ukir, hitung mundur memakai paku kuningan. Tanpa ornamen makhluk hidup, basmalah sebagai teks.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Forum", "Alegreya Sans:wght@400;500;700;800", "Amiri:wght@400;700"];
const BISMILLAH = "بِسْمِ اللّٰهِ الرَّحْمٰنِ الرَّحِيْمِ";
// Painted by /tmp/pen/art/themes/zanzibar-pintu.py (tools/art/themes in the repo).
const Art = makeArt("zanzibar-pintu", { frame: [480, 720], stud: [64, 64], rosette: [120, 120], divider: [380, 26] } as const);

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    arabic: BISMILLAH,
    kicker: "Assalamu'alaikum",
    title: "Warahmatullahi Wabarakatuh",
    intro: "Dengan memohon rahmat dan ridha Allah SWT, kami bermaksud menyelenggarakan walimatul 'ursy putra-putri kami. Merupakan kehormatan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"],
  couple: ["Di Balik Pintu Ini", "Kedua Mempelai"],
  count: ["Layar Telah Terkembang", "Menuju Hari Bahagia"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Waktu & Tempat", "Akad & Walimah"],
  story: ["Perjalanan", "Kisah Kami"],
  gallery: ["Galeri", "Momen Bahagia"],
  wishes: ["Doa & Kehadiran", "Ucapan & Konfirmasi"],
  gifts: ["Tanda Kasih", "Amplop Digital"],
  closing: { thanks: "Jazakumullahu Khairan", text: "Atas kehadiran dan doa restu Bapak/Ibu/Saudara/i, kami sekeluarga mengucapkan terima kasih. Semoga Allah membalas setiap kebaikan.", salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh" },
  sent: "Jazakumullahu khairan, doa dan ucapan Anda sudah terkirim.",
};

export default function ZanzibarPintuTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Walimatul 'Ursy";
  const table = tableLabel(data.guestTable);
  const photo = data.gallery[0] ?? data.couple.bridePhoto;
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#efe6d4"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <p className={s.coverArabic} lang="ar" dir="rtl">{BISMILLAH}</p>
          <p className={s.salam}>Assalamu&apos;alaikum Wr. Wb.</p>
          <div className={s.door}>
            <span className={s.doorLeaves} aria-hidden />
            <Art name="frame" className={s.doorFrame} eager />
            <div className={s.plaque}>
              <p className={s.kicker}>Undangan {label}</p>
              <h1 className={s.coverNames}><span>{data.couple.bride}</span><em>&amp;</em><span>{data.couple.groom}</span></h1>
              <p className={s.coverDate}>{formatDate(data.date)}</p>
            </div>
          </div>
          <div className={s.guestStep}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#ffffff" />Buka Pintu</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#f4e3b5"
        dark="#2c1a0e"
        copy={COPY}
        hero={(
          <header className={s.hero}>
            <p className={s.heroKicker}>Walimatul &apos;Ursy</p>
            <h1 className={s.heroNames}>{data.couple.bride} <em>&amp;</em> {data.couple.groom}</h1>
            <p className={s.heroDate}><span className={s.stud} aria-hidden />{formatDate(data.date)}<span className={s.stud} aria-hidden /></p>
            <div className={s.heroDoor}>
              <div className={s.heroPhoto}>{photo ? <Photo src={photo} alt={`${data.couple.bride} & ${data.couple.groom}`} /> : <span aria-hidden>{data.couple.bride.slice(0, 1)}</span>}</div>
              <Art name="frame" className={s.doorFrame} />
            </div>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="divider" className={s.divider} />,
          node: <Art name="stud" />,
          amp: <Art name="stud" />,
          closingEmblem: <Art name="rosette" className={s.closingEmblem} />,
          sentArt: <Art name="rosette" />,
        }}
      />
    </ThemeShell>
  );
}
