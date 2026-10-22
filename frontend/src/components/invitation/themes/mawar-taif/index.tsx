"use client";
// Theme "Mawar Taif" — musim mawar di dataran tinggi Hijaz, dilukis cat air: punggung bukit granit lilac-abu, teras
// dinding batu kering yang melengkung, barisan semak mawar damask berbintik merah muda, mawar besar di latar depan,
// botol pemercik air mawar dari kaca, dan kelopak yang berjatuhan. Lengkung Hijazi pada kartu. Tanpa makhluk bernyawa.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["El Messiri:wght@400;500;600", "Spectral:ital,wght@0,400;0,500;1,400", "Parisienne", "Amiri:wght@400;700"];
// Painted by /tmp/pen/art/themes/mawar-taif.py (tools/art/themes in the repo).
const Art = makeArt("mawar-taif", { valley: [780, 461], spray: [420, 360], petal: [48, 48], bottle: [180, 360], divider: [320, 33] } as const);
const BISMILLAH = "بِسْمِ اللّٰهِ الرَّحْمٰنِ الرَّحِيْمِ";

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    arabic: BISMILLAH,
    kicker: "Assalamu'alaikum",
    title: "Warahmatullahi Wabarakatuh",
    intro: "Dengan memohon rahmat dan ridha Allah SWT, kami bermaksud menyelenggarakan walimah pernikahan putra-putri kami. Merupakan kehormatan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"],
  couple: ["Dua Kuntum Sebatang", "Kedua Mempelai"],
  count: ["Menanti Musim Mekar", "Menuju Hari Akad"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Waktu & Tempat", "Rangkaian Acara"],
  story: ["Perjalanan", "Kisah Kami"],
  gallery: ["Galeri", "Momen Bahagia"],
  wishes: ["Doa & Kehadiran", "Ucapan & Konfirmasi"],
  gifts: ["Tanda Kasih", "Amplop Digital"],
  closing: { thanks: "Jazakumullah Khairan", text: "Atas kehadiran dan doa Bapak/Ibu/Saudara/i, kami sekeluarga mengucapkan terima kasih. Semoga kebaikan Anda kembali seharum mawar di musim panennya.", salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh" },
  sent: "Jazakallah khairan, doa dan ucapan Anda sudah terkirim.",
};

const WISHES = [
  { id: "w1", name: "Syarifah Fatimah Alaydrus", attendance: "yes" as Attendance, message: "Barakallahu lakuma wa baraka 'alaikuma wa jama'a bainakuma fi khair. Semoga menjadi keluarga yang harum akhlaknya." },
  { id: "w2", name: "Rekan Alumni Madinah", attendance: "yes" as Attendance, message: "Mabruk ya akhi Yusuf! Semoga Allah mudahkan semuanya sampai jannah." },
  { id: "w3", name: "Keluarga Bawazier Gresik", attendance: "maybe" as Attendance, message: "Insyaallah hadir. Doa terbaik dari kami sekeluarga untuk Humaira dan Yusuf." },
];

export default function MawarTaifTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const hero = data.gallery[0] ?? data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#fbf1ee"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Art name="spray" eager className={s.coverSpray} />
          {[s.p1, s.p2, s.p3, s.p4].map(c => <Art key={c} name="petal" eager className={`${s.coverPetal} ${c}`} />)}
          <p className={s.arabicCover} lang="ar" dir="rtl">{BISMILLAH}</p>
          <p className={s.kicker}>Assalamu&apos;alaikum Wr. Wb.</p>
          <p className={s.coverLabel}>{label}</p>
          <h1 className={s.coverNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.valley}>
            <Art name="valley" eager />
          </div>
          <div className={s.arch}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#fff6f4" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#fbe3e8"
        dark="#b4456a"
        copy={COPY}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            <p className={s.heroKicker}>{label}</p>
            <h1 className={s.heroNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {hero && (
              <div className={s.heroArch}>
                <div className={s.heroPhoto}><Photo src={hero} alt="" /></div>
                <Art name="spray" className={s.heroSpray} />
                <Art name="bottle" className={s.heroBottle} />
              </div>
            )}
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="divider" className={s.divider} />,
          node: <Art name="petal" />,
          amp: <Art name="petal" />,
          portrait: <Art name="spray" className={s.pRose} />,
          countDecor: <><Art name="petal" className={s.cdPetal} /><Art name="petal" className={s.cdPetal} /><Art name="petal" className={s.cdPetal} /></>,
          closingDecor: <div className={s.closingDecor} aria-hidden><Art name="spray" className={s.clSpray} /><Art name="spray" className={s.clSpray} /><Art name="petal" className={s.clPetal} /><Art name="petal" className={s.clPetal} /></div>,
          closingEmblem: <Art name="bottle" className={s.closingBottle} />,
          sentArt: <Art name="bottle" />,
        }}
      />
    </ThemeShell>
  );
}
