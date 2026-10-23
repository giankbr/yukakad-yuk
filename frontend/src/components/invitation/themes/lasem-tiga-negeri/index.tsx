"use client";
// Theme "Lasem Tiga Negeri" — selembar kain tiga negeri Lasem: mori krem yang dicelup merah bang-bangan, biru indigo dan
// cokelat sogan, bunga seruni dan sulur latohan dengan garis malam dan cecek, burung hong bergaya batik, serta regol
// rumah tua Tionghoa-Jawa di pesisir Lasem. Sampul berpola kain panjang: kolom papan bercorak di kiri, teks di kain krem.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Libre Caslon Display", "Spectral:ital,wght@0,400;0,600;1,400", "Cormorant Upright:wght@400;500"];
// Painted by /tmp/pen/art/themes/lasem-tiga-negeri.py (tools/art/themes in the repo).
const Art = makeArt("lasem-tiga-negeri", { gate: [680, 496], hong: [555, 419], sprig: [360, 71], seruni: [200, 195] } as const);

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    kicker: "Salam Sejahtera",
    title: "Tiga Warna, Satu Kain",
    intro: "Dengan penuh syukur kepada Tuhan Yang Maha Esa, kami mengundang Bapak/Ibu/Saudara/i untuk hadir dan memberikan restu pada pernikahan kami. Seperti batik tiga negeri yang dicelup berulang kali, kami ingin merajut hidup dari banyak warna dan kasih dua keluarga.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"],
  couple: ["Yang Berbahagia", "Kedua Mempelai"],
  count: ["Menghitung Hari", "Menuju Hari Bahagia"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Waktu & Tempat", "Rangkaian Acara"],
  story: ["Perjalanan", "Kisah Kami"],
  gallery: ["Album", "Potret Kami"],
  wishes: ["Doa & Restu", "Ucapan & Kehadiran"],
  gifts: ["Tanda Kasih", "Amplop Digital"],
  closing: { thanks: "Terima Kasih", text: "Kehadiran dan doa restu Bapak/Ibu/Saudara/i adalah warna terindah di kain kehidupan kami yang baru." },
  sent: "Terima kasih, doa dan ucapan Anda sudah terkirim.",
  attend: { maybe: "Mungkin" },
};

export default function LasemTigaNegeriTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const hero = data.gallery[0] ?? data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#2a1b11"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <span className={s.coverEdge} aria-hidden />
          <span className={s.papan} aria-hidden data-noreveal />
          <div className={s.coverText}>
            <Art name="hong" eager className={s.coverHong} />
            <p className={s.kicker}>Undangan {label}</p>
            <h1 className={s.coverNames}><span>{data.couple.bride}</span><em>&amp;</em><span>{data.couple.groom}</span></h1>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
            <div className={s.guestWrap}>
              <div className={s.guest}>
                <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
                <strong>{guestLabel(data)}</strong>
                {table && <span className={s.table}>{table}</span>}
              </div>
              <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#faf4e6" />Buka Undangan</button>
            </div>
          </div>
          <Art name="gate" eager className={s.coverGate} />
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#f6ecd8"
        dark="#2e1d12"
        copy={COPY}
        hero={(
          <header className={s.hero}>
            <span className={s.heroCloth} aria-hidden />
            {hero && <div className={s.heroPhoto}><Photo src={hero} alt="" /></div>}
            <p className={s.heroKicker}>Undangan {label}</p>
            <h1 className={s.heroNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
            <Art name="gate" className={s.heroGate} />
          </header>
        )}
        slots={{
          divider: <Art name="sprig" className={s.divider} />,
          node: <Art name="seruni" />,
          amp: <Art name="seruni" />,
          closingDecor: <span className={s.closingCloth} aria-hidden />,
          closingEmblem: <Art name="hong" className={s.closingHong} />,
          sentArt: <Art name="seruni" />,
        }}
      />
    </ThemeShell>
  );
}
