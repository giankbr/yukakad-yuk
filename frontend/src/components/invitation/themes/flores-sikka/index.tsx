"use client";
// Theme "Flores Sikka" — pernikahan Katolik di Maumere: tenun ikat Sikka nila-cokelat bermotif halus ditenun benang demi
// benang (ikat lungsin dengan tepi kabur), danau tiga warna Kelimutu dan bukit Flores dalam cat air, foto berbentuk
// danau kawah, hitung mundur dalam empat kolam warna, pita tenun sebagai kelim setiap kartu. Salam damai.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Tenor Sans", "Castoro:ital@0;1", "Mea Culpa"];
// Painted by /tmp/pen/art/themes/flores-sikka.py (tools/art/themes in the repo).
const Art = makeArt("flores-sikka", { kelimutu: [740, 469], bukit: [820, 203], bintang: [180, 180] } as const);

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    kicker: "Salam Damai",
    title: "Dalam Kasih Tuhan",
    intro: "Dengan penuh syukur atas rahmat Tuhan, kami mengundang Bapak/Ibu/Saudara/i untuk hadir dan turut mendoakan Sakramen Perkawinan putra-putri kami.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"],
  couple: ["Kedua Mempelai", "Dua Hati, Satu Tenun"],
  count: ["Menghitung Hari", "Menuju Hari Bahagia"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Waktu & Tempat", "Rangkaian Acara"],
  story: ["Kisah Kami", "Dari Kelimutu"],
  gallery: ["Galeri", "Momen Bahagia"],
  wishes: ["Doa & Kehadiran", "Ucapan & Konfirmasi"],
  gifts: ["Tanda Kasih", "Amplop Digital"],
  closing: { thanks: "Terima Kasih", text: "Kehadiran dan doa Bapak/Ibu/Saudara/i adalah berkat bagi kami sekeluarga.", salam: "Tuhan memberkati" },
  sent: "Terima kasih, doa dan ucapan Anda sudah terkirim.",
  attend: { maybe: "Mungkin" },
};

const WISHES = [
  { id: "w1", name: "Keluarga Bapak Stefanus Ximenes", attendance: "yes" as Attendance, message: "Selamat menempuh hidup baru, Yosi dan Frans. Tuhan memberkati rumah tangga kalian dengan damai dan sukacita." },
  { id: "w2", name: "OMK Paroki St. Yosef", attendance: "yes" as Attendance, message: "Proficiat! Kami siap meramaikan dansa malam nanti." },
  { id: "w3", name: "Suster Maria Goreti", attendance: "maybe" as Attendance, message: "Mungkin hanya bisa hadir di misa. Doa kami menyertai kalian berdua." },
];

export default function FloresSikkaTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const hero = data.gallery[0] ?? data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#2b2130"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <p className={s.kicker}>Undangan {label}</p>
          <h1 className={s.coverNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.lakes}>
            <Art name="kelimutu" eager className={s.lakesArt} />
            {hero && <div className={s.lakePhoto}><Photo src={hero} alt="" /></div>}
          </div>
          <div className={s.guestWrap}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#e8d8b4" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#e8d8b4"
        dark="#2b2130"
        copy={COPY}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            <p className={s.heroKicker}>Salam Damai</p>
            <h1 className={s.heroNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
            <div className={s.heroHills}><Art name="bukit" /></div>
          </header>
        )}
        slots={{
          divider: <span className={s.divider} aria-hidden><i /><Art name="bintang" /><i /></span>,
          node: <Art name="bintang" />,
          amp: <Art name="bintang" />,
          portrait: <Art name="bintang" />,
          closingDecor: <div className={s.closingHills} aria-hidden><Art name="bukit" /></div>,
          closingEmblem: <Art name="bintang" className={s.closingEmblem} />,
          sentArt: <Art name="bintang" />,
        }}
      />
    </ThemeShell>
  );
}
