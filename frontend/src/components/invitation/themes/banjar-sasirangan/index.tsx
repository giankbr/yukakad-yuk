"use client";
// Theme "Banjar Sasirangan" — kertas krem bernoda celup: selembar kain sasirangan (jelujur, gigi haruan, kulat
// kurikit) tergantung di tepi sampul, foto berbingkai bercak pewarna, dan sungai cat air dengan rumah Bubungan Tinggi
// serta jukung bermuatan buah yang terapung pelan. Ramah nuansa Islami, tanpa figur manusia/hewan.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Playfair Display:ital,wght@0,400;0,500;1,400;1,500", "Nunito Sans:wght@400;600;700;800", "Parisienne", "Amiri:wght@400"];
// Painted by /tmp/pen/art/themes/banjar-sasirangan.py (tools/art/themes in the repo).
const Art = makeArt("banjar-sasirangan", { kain: [140, 770], sungai: [720, 416], jukung: [220, 61], divider: [300, 35] } as const);

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    arabic: "بِسْمِ اللّٰهِ الرَّحْمٰنِ الرَّحِيْمِ",
    kicker: "Assalamu'alaikum Wr. Wb.",
    title: "Salam Sabarataan",
    intro: "Dengan memohon rahmat dan ridha Allah SWT, kami bermaksud menyelenggarakan pernikahan putra-putri kami. Merupakan kehormatan bagi kami apabila Bapak/Ibu/Saudara/i, pian sabarataan, berkenan hadir dan memberikan doa restu.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"],
  couple: ["Bubuhan Pengantin", "Kedua Mempelai"],
  count: ["Menghitung Hari", "Menuju Hari Bahagia"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Waktu & Tempat", "Rangkaian Acara"],
  story: ["Kisah", "Perjalanan Kami"],
  gallery: ["Galeri", "Momen Bahagia"],
  wishes: ["Doa & Kehadiran", "Ucapan & Konfirmasi"],
  gifts: ["Tanda Kasih", "Amplop Digital"],
  closing: { thanks: "Tarima Kasih Banar", text: "Atas kehadiran dan doa restu pian sabarataan, kami sekeluarga mengucapkan terima kasih yang sebesar-besarnya.", salam: "Wassalamu'alaikum Wr. Wb." },
  sent: "Tarima kasih banar, doa dan ucapan pian sudah terkirim.",
};

export default function BanjarSasiranganTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const hero = data.gallery[0] ?? data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#e8dcc0"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <span className={s.kainRod} aria-hidden />
          <Art name="kain" eager className={s.kain} />
          <p className={s.kicker}>Assalamu&apos;alaikum</p>
          <p className={s.coverLabel}>Undangan {label}</p>
          {hero && <div className={s.coverPhoto}><Photo src={hero} alt="" /></div>}
          <h1 className={s.coverNames}><span>{data.couple.bride}</span><em>dan</em><span>{data.couple.groom}</span></h1>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.guestWrap}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#fbf5e4" />Buka Undangan</button>
          </div>
          <div className={s.river} aria-hidden>
            <Art name="sungai" eager className={s.sungai} />
            <Art name="jukung" eager className={s.jukungFloat} />
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#fbf5e4"
        dark="#1d4626"
        copy={COPY}
        hero={(
          <header className={s.hero}>
            <span className={s.heroBand} aria-hidden />
            <div className={s.heroTop}>
              <p className={s.heroKicker}>Undangan {label}</p>
              <h1 className={s.heroNames}>{data.couple.bride}<em>dan</em>{data.couple.groom}</h1>
              <p className={s.heroDate}>{formatDate(data.date)}</p>
            </div>
            {hero && <div className={s.heroPhoto}><Photo src={hero} alt="" /></div>}
            {note && <p className={s.heroNote}>{note}</p>}
            <div className={s.heroRiver} aria-hidden>
              <Art name="sungai" className={s.sungai} />
              <Art name="jukung" className={s.jukungFloat} />
            </div>
          </header>
        )}
        slots={{
          divider: <Art name="divider" className={s.divider} />,
          amp: <Art name="divider" />,
          node: <Art name="jukung" />,
          closingEmblem: <><Art name="sungai" className={s.closingSungai} /><Art name="jukung" className={s.closingJukung} /></>,
          sentArt: <Art name="jukung" />,
        }}
      />
    </ThemeShell>
  );
}
