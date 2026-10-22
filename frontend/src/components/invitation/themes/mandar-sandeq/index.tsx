"use client";
// Theme "Mandar Sandeq" — cahaya pesisir Sulawesi Barat: armada perahu sandeq berlayar segitiga di laut biru cat air,
// sarung sutra lipaq saqbe bermotif kotak yang ditenun sampai ke benang, dan bentuk layar (sudut melengkung) sebagai
// bahasa bentuk. Sampul: langit pagi, Bismillah, nama, lalu laut dengan sandeq dan kartu tamu di atas ombak.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Prata", "Karla:ital,wght@0,400;0,600;0,700;0,800;1,400", "Amiri:wght@400;700"];
// Painted by /tmp/pen/art/themes/mandar-sandeq.py (tools/art/themes in the repo).
const Art = makeArt("mandar-sandeq", { sea: [680, 638], boat: [240, 210], wave: [360, 40] } as const);

const BISMILLAH = "بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ";

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    arabic: BISMILLAH,
    kicker: "Assalamu'alaikum Wr. Wb.",
    title: "Siwaliparri",
    sub: "Bahu-membahu dalam suka dan duka, seperti layar dan cadik yang menjaga sandeq tetap melaju.",
    intro: "Dengan memohon rahmat dan ridha Allah SWT, kami bermaksud menyelenggarakan pernikahan putra-putri kami. Merupakan kehormatan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"],
  couple: ["Dengan Izin Allah", "Kedua Mempelai"],
  count: ["Layar Terkembang", "Menuju Hari Bahagia"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Waktu & Tempat", "Rangkaian Acara"],
  story: ["Arah Angin", "Perjalanan Kami"],
  gallery: ["Galeri", "Potret Pesisir"],
  wishes: ["Doa & Kehadiran", "Ucapan & Konfirmasi"],
  gifts: ["Tanda Kasih", "Amplop Digital"],
  closing: { thanks: "Terima Kasih", text: "Atas kehadiran dan doa restu Bapak/Ibu/Saudara/i, kami sekeluarga mengucapkan terima kasih. Semoga Allah membalas segala kebaikan.", salam: "Wassalamu'alaikum Wr. Wb." },
  sent: "Terima kasih, doa dan ucapan Anda sudah terkirim.",
};

export default function MandarSandeqTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const hero = data.gallery[0] ?? data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#d6e4e6"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.coverText}>
            <p className={s.coverArabic} lang="ar" dir="rtl">{BISMILLAH}</p>
            <p className={s.coverKicker}>Assalamu&apos;alaikum Wr. Wb.</p>
            <p className={s.coverLabel}>Undangan {label}</p>
            <h1 className={s.coverNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
          </div>
          <Art name="sea" eager className={s.coverSea} />
          <div className={s.coverGuest}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={17} color="#fff" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#f6f1e6"
        dark="#14283c"
        copy={COPY}
        hero={(
          <header className={s.hero}>
            <p className={s.heroKicker}>Undangan {label}</p>
            <h1 className={s.heroNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {hero && <div className={s.heroPhoto}><Photo src={hero} alt="" /></div>}
            {note && <p className={s.heroNote}>{note}</p>}
            <Art name="wave" className={s.heroWave} />
          </header>
        )}
        slots={{
          divider: <Art name="wave" className={s.divider} />,
          node: <Art name="boat" />,
          closingEmblem: <Art name="boat" className={s.closingBoat} />,
          closingDecor: <Art name="sea" className={s.closingSea} />,
          sentArt: <Art name="boat" />,
        }}
      />
    </ThemeShell>
  );
}
