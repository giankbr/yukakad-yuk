"use client";
// Theme "Papua Cendrawasih" — burung cendrawasih bergaya gouache dengan bulu hias yang menjuntai, pita ukiran garis
// terinspirasi Asmat (desain orisinal), tekstur rajutan noken, dan tata letak rata kiri bernuansa cetak cukil.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Young Serif", "Josefin Sans:wght@400;600;700", "Mulish:ital,wght@0,400;0,600;0,700;1,400"];
// Painted by /tmp/pen/art/themes/papua-cendrawasih.py (tools/art/themes in the repo).
const Art = makeArt("papua-cendrawasih", { bird: [420, 486], spiral: [260, 29] } as const);

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  attend: { maybe: "Mungkin" },
  opening: {
    kicker: "Selamat Datang",
    title: "Salam Sejahtera",
    intro: "Dengan penuh syukur atas kasih karunia Tuhan, kami mengundang Bapak/Ibu/Saudara/i, ade-kaka sekalian, untuk hadir dan turut memberkati pernikahan kami.",
  },
  roles: ["Mempelai Perempuan", "Mempelai Laki-laki"],
  couple: ["Dua Hati, Satu Noken", "Mempelai"],
  count: ["Hitung Hari", "Menuju Hari Bahagia"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Rangkaian Acara", "Ibadah & Pesta"],
  story: ["Perjalanan Kami", "Kisah Cinta"],
  gallery: ["Galeri", "Cerita dalam Foto"],
  wishes: ["Doa & Kehadiran", "Ucapan & Konfirmasi"],
  gifts: ["Tanda Kasih", "Amplop Digital"],
  closing: { thanks: "Trima Kasih Banyak", text: "Kehadiran dan doa Bapak/Ibu/Saudara/i adalah berkat yang tak ternilai bagi kami dan keluarga besar.", salam: "Tuhan Yesus memberkati" },
  sent: "Trima kasih, doa dan ucapan Anda sudah terkirim.",
};

export default function PapuaCendrawasihTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const table = tableLabel(data.guestTable);
  const photo = data.gallery[0] ?? data.couple.bridePhoto;
  const note = data.couple.note?.trim();
  const initials = `${data.couple.bride.slice(0, 1)}${data.couple.groom.slice(0, 1)}`;

  return (
    <ThemeShell
      fonts={FONTS}
      background="#2a1a12"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.coverTop}>
            <div className={s.coverPanel} aria-hidden><span className={s.ukir} /></div>
            <div className={s.coverPhoto}>{photo ? <Photo src={photo} alt="" /> : <span className={s.coverMono} aria-hidden>{initials}</span>}</div>
            <Art name="bird" eager className={s.coverBird} />
          </div>
          <p className={s.salam}>Selamat Datang</p>
          <p className={s.kicker}>Undangan {label}</p>
          <h1 className={s.coverNames}><span>{data.couple.bride}</span><em>&amp;</em><span>{data.couple.groom}</span></h1>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.guestWrap}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#f3e6cf" />Buka Undangan</button>
          </div>
          <span className={s.coverFoot} aria-hidden />
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        copy={COPY}
        light="#f0c46a"
        dark="#1d1410"
        hero={(
          <header className={photo ? s.hero : `${s.hero} ${s.heroBare}`}>
            <span className={s.heroPanel} aria-hidden />
            {photo && <div className={s.heroPhoto}><Photo src={photo} alt="" /></div>}
            <Art name="bird" className={s.heroBird} />
            <p className={s.kickerDark}>Undangan {label}</p>
            <h1 className={s.heroNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
            <span className={s.ukir} aria-hidden />
          </header>
        )}
        slots={{
          divider: <Art name="spiral" className={s.divider} />,
          amp: <Art name="spiral" />,
          countDecor: <><span className={`${s.ukir} ${s.countDecor} ${s.countDecorT}`} aria-hidden /><span className={`${s.ukir} ${s.countDecor} ${s.countDecorB}`} aria-hidden /></>,
          closingDecor: <span className={s.ukir} aria-hidden />,
          closingEmblem: <Art name="bird" className={s.closingBird} />,
          sentArt: <Art name="spiral" />,
        }}
      />
    </ThemeShell>
  );
}
