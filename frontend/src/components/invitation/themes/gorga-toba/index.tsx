"use client";
// Theme "Gorga Toba" — adat Batak Toba. Papan gorga hitam dengan ukiran spiral merah-putih bercetak cukil dan desa na
// ualu di tengah, jendela bergambar Danau Toba dari pantai Samosir (cat air), plakat nama hitam yang menindih jendela.
// Bingkai potret berbentuk muka rumah adat yang melebar ke atas, pita ipon-ipon untuk hitung mundur dan kartu.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Zilla Slab:ital,wght@0,500;0,600;0,700;1,600;1,700", "Alegreya:ital,wght@0,400;0,500;1,400"];
// Painted by /tmp/pen/art/themes/gorga-toba.py
const Art = makeArt("gorga-toba", { lintel: [880, 234], desa: [220, 221] } as const);

const WISHES = [
  { id: "w1", name: "Keluarga Tambunan", attendance: "yes" as const, message: "Horas! Selamat menempuh hidup baru, Tiurma dan Hotman. Gabe jala horas, Tuhan Yesus memberkati rumah tangga kalian." },
  { id: "w2", name: "Naposo HKBP Medan Kota", attendance: "yes" as const, message: "Akhirnya sopran dan bas bersatu juga! Kami siap menyanyi di pemberkatan. Selamat, Tuhan memberkati." },
  { id: "w3", name: "Amangboru Situmorang", attendance: "maybe" as const, message: "Mauliate atas undangannya. Semoga bisa menyeberang ke Samosir. Sai horas ma hamu, saur matua." },
];

export default function GorgaTobaTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const { bride, groom } = data.couple;
  const label = data.eventLabel ?? "Pernikahan";
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const hero = data.gallery[0] ?? data.couple.bridePhoto;

  return (
    <ThemeShell
      fonts={FONTS}
      background="#efe9dd"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <p className={s.horas}>Horas!</p>
          <p className={s.coverKicker}>Undangan {label}</p>
          <Art name="lintel" eager className={s.lintel} />
          <div className={s.window} aria-hidden />
          <div className={s.plaque}>
            <p className={s.plaqueLabel}>Adat Batak Toba</p>
            <h1 className={s.coverNames}><span>{bride}</span>{groom && <><i>dohot</i><span>{groom}</span></>}</h1>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
          </div>
          <div className={s.guestBox}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#ffffff" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#f1ebdf"
        dark="#1d1916"
        demoWishes={WISHES}
        copy={{
          ...DEFAULT_COPY,
          opening: {
            kicker: "Horas jala gabe",
            title: "Syalom!",
            sub: "Salam sejahtera dalam kasih Tuhan Yesus Kristus",
            intro: "Dengan penuh sukacita dan atas berkat Tuhan Yang Maha Kasih, kami mengundang Bapak/Ibu/Saudara/i untuk hadir dalam pemberkatan nikah dan pesta adat putra-putri kami. Kehadiran dan doa restu Anda adalah kehormatan bagi kami.",
          },
          roles: ["Boru", "Anak"],
          couple: ["Na marhite holong", "Kedua Mempelai"],
          count: ["Menuju hari bahagia", "Hitung Mundur"],
          units: ["Hari", "Jam", "Menit", "Detik"],
          events: ["Ulaon", "Rangkaian Acara"],
          story: ["Dalan ni holong", "Kisah Kami"],
          gallery: ["Galeri", "Momen Bersama"],
          wishes: ["Hata pasu-pasu", "Ucapan & Kehadiran"],
          gifts: ["Tanda kasih", "Amplop Digital"],
          closing: {
            thanks: "Mauliate Godang",
            text: "Kehadiran dan doa restu Bapak/Ibu/Saudara/i adalah sukacita yang tak ternilai bagi kami dan keluarga besar.",
            salam: "Horas! Horas! Horas!",
          },
          attend: { maybe: "Mungkin" },
          sent: "Mauliate! Ucapan dan doa Anda sudah terkirim.",
          wishPlaceholder: "Tuliskan ucapan dan doa untuk kedua mempelai…",
          familyLabel: "Kami yang berbahagia",
        }}
        hero={(
          <header className={s.hero}>
            <Art name="desa" className={s.heroDesa} />
            <p className={s.heroKicker}>Pesta Unjuk</p>
            <h1 className={s.heroNames}>{bride}{groom && <><i>dohot</i>{groom}</>}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {hero && (
              <div className={s.heroFrame}>
                <Art name="lintel" className={s.lintel} />
                <div className={s.heroPhoto}><Photo src={hero} alt={`${bride} dan ${groom}`} /></div>
              </div>
            )}
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <span className={s.divider} aria-hidden><Art name="desa" /></span>,
          node: <Art name="desa" />,
          amp: <Art name="desa" />,
          closingDecor: <><div className={s.closingLake} aria-hidden /><Art name="lintel" className={s.closingLintel} /></>,
          sentArt: <Art name="desa" />,
        }}
      />
    </ThemeShell>
  );
}
