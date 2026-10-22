"use client";
// Theme "Pesantren Teduh" — halaman pesantren di sore yang hangat, dilukis cat air dan sedikit guas: surau kayu
// berpanggung umpak dengan atap kampung genteng, serambi bertiang tempat bedug dan kentongan, pohon kamboja yang berbunga,
// halaman berpasir bergaris sapu lidi, padasan wudhu, sandal berjajar, dan bayang daun yang bergeser pelan.
// Tanpa makhluk bernyawa, tanpa kaligrafi yang dilukis (basmalah diketik).
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Kurale", "Literata:ital,wght@0,400;0,600;1,400", "Caveat:wght@500;600", "Amiri:wght@400;700"];
// Painted by /tmp/pen/art/themes/pesantren-teduh.py (tools/art/themes in the repo).
const Art = makeArt("pesantren-teduh", { surau: [780, 569], kamboja: [390, 315], bunga: [72, 72], bedug: [276, 216], divider: [320, 31] } as const);
const BISMILLAH = "بِسْمِ اللّٰهِ الرَّحْمٰنِ الرَّحِيْمِ";

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    arabic: BISMILLAH,
    kicker: "Assalamu'alaikum",
    title: "Warahmatullahi Wabarakatuh",
    intro: "Dengan memohon rahmat dan ridha Allah SWT, serta doa restu para guru, kami bermaksud menyelenggarakan walimah pernikahan putra-putri kami. Merupakan kehormatan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan mendoakan.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"],
  couple: ["dua santri, satu niat", "Kedua Mempelai"],
  count: ["sabar menanti", "Menuju Hari Akad"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["waktu & tempat", "Rangkaian Acara"],
  story: ["perjalanan", "Kisah Kami"],
  gallery: ["kenangan", "Momen Bahagia"],
  wishes: ["doa & kehadiran", "Ucapan & Konfirmasi"],
  gifts: ["tanda kasih", "Amplop Digital"],
  closing: { thanks: "Matur Nuwun", text: "Atas kehadiran dan doa Bapak/Ibu/Saudara/i, kami sekeluarga mengucapkan terima kasih. Jazakumullah khairan katsiran, semoga Allah membalas dengan keberkahan.", salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh" },
  sent: "Jazakallah khairan, doa dan ucapan Anda sudah terkirim.",
};

const WISHES = [
  { id: "w1", name: "Ustadz Mahfudz", attendance: "yes" as Attendance, message: "Barakallahu lakuma wa baraka 'alaikuma wa jama'a bainakuma fi khair. Semoga menjadi keluarga yang istiqamah dan bermanfaat bagi umat." },
  { id: "w2", name: "Santri Kamar Al-Ghazali", attendance: "yes" as Attendance, message: "Alhamdulillah, ikut bahagia Ustadz Hilmi dan Ustadzah Zulfa. Kami siap jadi tim hadrah!" },
  { id: "w3", name: "Alumni Angkatan 2018", attendance: "maybe" as Attendance, message: "Insyaallah sowan bila tidak ada halangan. Doa terbaik dari kami semua." },
];

export default function PesantrenTeduhTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const hero = data.gallery[0] ?? data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#e2cc9e"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <p className={s.arabicCover} lang="ar" dir="rtl">{BISMILLAH}</p>
          <p className={s.kicker}>Assalamu&apos;alaikum Wr. Wb.</p>
          <p className={s.coverLabel}>Undangan {label}</p>
          <h1 className={s.coverNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.scene}>
            <Art name="surau" eager />
            <Art name="bunga" eager className={`${s.fallFlower} ${s.f1}`} />
            <Art name="bunga" eager className={`${s.fallFlower} ${s.f2}`} />
          </div>
          <div className={s.yard}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#fbf4e6" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#f6dcae"
        dark="#5e3b20"
        copy={COPY}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            <p className={s.heroKicker}>{label}</p>
            <h1 className={s.heroNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {hero && (
              <div className={s.papan}>
                <div className={s.heroPhoto}><Photo src={hero} alt="" /></div>
                <Art name="kamboja" className={s.heroSprig} />
                <p className={s.noteCard}>Insyaallah, {formatDate(data.date).replace(/^[^,]+,\s*/, "")}</p>
              </div>
            )}
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="divider" className={s.divider} />,
          node: <Art name="bunga" />,
          amp: <Art name="bunga" />,
          portrait: <Art name="kamboja" className={s.pSprig} />,
          closingDecor: <div className={s.closingDecor} aria-hidden><Art name="kamboja" className={s.clSprig} /><Art name="bunga" className={s.clFlower} /><Art name="bunga" className={s.clFlower} /></div>,
          closingEmblem: <Art name="bedug" className={s.closingBedug} />,
          sentArt: <Art name="bedug" />,
        }}
      />
    </ThemeShell>
  );
}
