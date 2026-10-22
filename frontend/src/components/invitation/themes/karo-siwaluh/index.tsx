"use client";
// Theme "Karo Siwaluh" — pernikahan Kristen adat Karo. Lukisan gouache rumah siwaluh jabu beratap ijuk dengan ayo-ayo
// anyaman bambu dan tanduk, berdiri di depan dataran tinggi Berastagi dan Sinabung; uis Karo merah-hitam-emas yang
// ditenun benang demi benang menjadi pita, bingkai foto, dan kartu. Bentuk atap (gable) mengulang di potret dan angka.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Zilla Slab:wght@500;600;700", "Literata:ital,wght@0,400;0,600;1,400"];
// Painted and woven by /tmp/pen/art/themes/karo-siwaluh.py (tools/art/themes in the repo).
const Art = makeArt("karo-siwaluh", { rumah: [560, 593], jeruk: [260, 156], divider: [336, 95] } as const);

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  attend: { maybe: "Mungkin" },
  opening: {
    kicker: "Salam Sejahtera",
    title: "Mejuah-juah!",
    sub: "Shalom dalam kasih Tuhan",
    intro: "Dengan sukacita dan syukur kepada Tuhan Yang Maha Kasih, kami bersama sangkep nggeluh kedua keluarga mengundang Bapak/Ibu/Saudara/i untuk hadir dan memberkati pernikahan kami.",
  },
  roles: ["Pengantin Perempuan", "Pengantin Laki-laki"],
  couple: ["Sada Rumah, Sada Ate", "Kedua Mempelai"],
  count: ["Menghitung Hari", "Menuju Erdemu Bayu"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Waktu & Tempat", "Pemberkatan & Pesta Adat"],
  story: ["Perjalanan Kami", "Kisah dari Berastagi"],
  gallery: ["Galeri", "Kenangan Kami"],
  wishes: ["Doa & Kehadiran", "Ucapan & Konfirmasi"],
  gifts: ["Tanda Kasih", "Amplop Digital"],
  closing: { thanks: "Bujur Melala", text: "Kehadiran dan doa Bapak/Ibu/Saudara/i adalah sukacita besar bagi kami dan seluruh sangkep nggeluh.", salam: "Mejuah-juah kita kerina!" },
  sent: "Bujur melala, doa dan ucapan Anda sudah terkirim.",
  wishPlaceholder: "Tuliskan doa dan berkat untuk kedua mempelai…",
};

const WISHES = [
  { id: "w1", name: "Bapak Edison Perangin-angin & Keluarga", attendance: "yes" as Attendance, message: "Mejuah-juah! Selamat menempuh hidup baru, Ruth dan Andreas. Tuhan memberkati rumah tangga kalian." },
  { id: "w2", name: "Permata GBKP Berastagi", attendance: "yes" as Attendance, message: "Selamat ya kakak dan abang! Kami siap landek bersama di jambur. Tuhan Yesus memberkati." },
  { id: "w3", name: "Nande Tua Br Sinulingga", attendance: "maybe" as Attendance, message: "Bujur melala undangannya. Semoga kalian rukun seperti delapan jabu di bawah satu atap." },
];

export default function KaroSiwaluhTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const table = tableLabel(data.guestTable);
  const photo = data.gallery[0] ?? data.couple.bridePhoto;
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#1f1918"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.coverScene}>
            <p className={s.mejuah}>Mejuah-juah!</p>
            <Art name="rumah" className={s.coverRumah} eager />
          </div>
          <div className={s.coverUis} aria-hidden />
          <div className={s.coverPanel}>
            <p className={s.kicker}>Undangan {label}</p>
            <h1 className={s.coverNames}>{data.couple.bride} <em>&amp;</em> {data.couple.groom}</h1>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#f1d38b" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#f1d38b"
        dark="#1f1918"
        copy={COPY}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            <p className={s.heroKicker}>Erdemu Bayu</p>
            <h1 className={s.heroNames}>{data.couple.bride} <em>&amp;</em> {data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            <div className={s.heroFrame}>
              <div className={s.heroPhoto}>{photo ? <Photo src={photo} alt={`${data.couple.bride} & ${data.couple.groom}`} /> : <span aria-hidden>{data.couple.bride.slice(0, 1)}</span>}</div>
              <Art name="jeruk" className={s.heroJeruk} />
            </div>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="divider" className={s.divider} />,
          node: <Art name="jeruk" />,
          amp: <Art name="jeruk" />,
          closingEmblem: <Art name="rumah" className={s.closingEmblem} />,
          sentArt: <Art name="jeruk" />,
        }}
      />
    </ThemeShell>
  );
}
