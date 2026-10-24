"use client";
// Theme "Keraton Sumenep" — the Labang Mesem gate of the Sumenep palace painted in gouache (white plaster, jade posts,
// chrome-yellow trims, a sweeping roof with a red curled ridge) standing on a green Madura-batik courtyard, red
// lanterns swaying from a painted Madura carving, and the names on a red lacquer plaque.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Rozha One", "Alegreya:ital,wght@0,400;0,500;0,700;0,800;1,400;1,500"];
// Painted by /tmp/pen/art/themes/keraton-sumenep.py (tools/art/themes in the repo).
const Art = makeArt("keraton-sumenep", {
  gate: [770, 592], lantern: [102, 233], ukir: [840, 120], kembang: [260, 259], divider: [360, 55],
} as const);

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    arabic: "بِسْمِ اللّٰهِ الرَّحْمٰنِ الرَّحِيْمِ",
    kicker: "Assalamu'alaikum Wr. Wb.",
    title: "Dengan Hormat Kami Mengundang",
    intro: "Dengan memohon rahmat dan ridha Allah SWT, kami bermaksud menyelenggarakan pernikahan putra-putri kami. Merupakan kehormatan bagi kami sekeluarga apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"],
  couple: ["Dua Hati, Satu Gerbang", "Kedua Mempelai"],
  count: ["Menghitung Hari", "Menuju Hari Bahagia"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Waktu & Tempat", "Rangkaian Acara"],
  story: ["Jejak Langkah", "Kisah Kami"],
  gallery: ["Galeri", "Potret Bahagia"],
  wishes: ["Doa & Kehadiran", "Ucapan & Konfirmasi"],
  gifts: ["Tanda Kasih", "Amplop Digital"],
  closing: { thanks: "Mator Sakalangkong", text: "Atas kehadiran dan doa restu Bapak/Ibu/Saudara/i, kami sekeluarga mengucapkan terima kasih yang sebesar-besarnya.", salam: "Wassalamu'alaikum Wr. Wb." },
  sent: "Mator sakalangkong, doa dan ucapan Anda sudah terkirim.",
  closedNote: "Terima kasih atas doa dan perhatiannya. Ucapan untuk kedua mempelai masih bisa dikirim lewat form ini.",
};

export default function KeratonSumenepTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const hero = data.gallery[0] ?? data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const groom = data.couple.groom?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#174334"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Art name="ukir" eager className={s.ukirTop} />
          <div className={s.lanterns} aria-hidden>
            <Art name="lantern" eager className={s.lantern} />
            <Art name="lantern" eager className={s.lantern} />
          </div>
          <div className={s.coverHead}>
            <p className={s.kicker}>Assalamu&apos;alaikum Wr. Wb.</p>
            <p className={s.coverLabel}>Undangan {label}</p>
          </div>
          <Art name="gate" eager className={s.gate} />
          <div className={s.ground}>
            <div className={s.plaque}>
              <h1 className={s.coverNames}><span>{data.couple.bride}</span>{groom && <><em>&amp;</em><span>{groom}</span></>}</h1>
              <p className={s.coverDate}>{formatDate(data.date)}</p>
            </div>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={18} color="#7a1419" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#fff6e0"
        dark="#7a1419"
        copy={COPY}
        hero={(
          <header className={s.hero}>
            <p className={s.heroKicker}>Undangan {label}</p>
            {hero
              ? <div className={s.heroArch}><div className={s.heroPhoto}><Photo src={hero} alt="" /></div></div>
              : <Art name="kembang" className={s.heroEmblem} />}
            <h1 className={s.heroNames}>{data.couple.bride}{groom && <><em>&amp;</em>{groom}</>}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
            <Art name="ukir" className={s.heroUkir} />
          </header>
        )}
        slots={{
          divider: <Art name="divider" className={s.divider} />,
          node: <Art name="kembang" />,
          closingDecor: <Art name="ukir" className={s.closingUkir} />,
          closingEmblem: <Art name="kembang" className={s.closingEmblem} />,
          sentArt: <Art name="kembang" />,
        }}
      />
    </ThemeShell>
  );
}
